"""Chunk storage and similarity search in Postgres with the pgvector extension.

Search is exact (a sequential scan ordered by cosine distance). At a few
thousand chunks that takes milliseconds; an HNSW index is the next step when a
corpus grows past roughly a hundred thousand chunks.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

import psycopg


@dataclass
class Hit:
    document: str
    title: str
    page: int
    heading: str
    text: str
    score: float  # cosine similarity, 1.0 is identical


def _vec(values: list[float]) -> str:
    return "[" + ",".join(f"{v:.6f}" for v in values) + "]"


class PgVectorStore:
    def __init__(self, database_url: str, dim: int, table: str = "chunks") -> None:
        if not table.isidentifier():
            raise ValueError("table name must be a plain identifier")
        self.url = database_url
        self.dim = dim
        self.table = table

    def connect(self) -> psycopg.Connection:
        return psycopg.connect(self.url)

    def wait_until_ready(self, attempts: int = 30, delay: float = 2.0) -> None:
        for attempt in range(attempts):
            try:
                with self.connect():
                    return
            except psycopg.OperationalError:
                if attempt == attempts - 1:
                    raise
                time.sleep(delay)

    def init_schema(self) -> None:
        with self.connect() as conn:
            conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.table} (
                    id bigserial PRIMARY KEY,
                    collection text NOT NULL,
                    document text NOT NULL,
                    title text NOT NULL,
                    page integer NOT NULL,
                    heading text NOT NULL DEFAULT '',
                    body text NOT NULL,
                    embedding vector({self.dim}) NOT NULL
                )
                """
            )
            conn.execute(f"CREATE INDEX IF NOT EXISTS {self.table}_collection_idx ON {self.table} (collection)")
            conn.execute(
                f"CREATE INDEX IF NOT EXISTS {self.table}_fts_idx ON {self.table} "
                "USING gin (to_tsvector('english', heading || ' ' || body))"
            )

    def count(self, collection: str) -> int:
        with self.connect() as conn:
            row = conn.execute(f"SELECT count(*) FROM {self.table} WHERE collection = %s", (collection,)).fetchone()
            return int(row[0])

    def delete_collection(self, collection: str) -> None:
        with self.connect() as conn:
            conn.execute(f"DELETE FROM {self.table} WHERE collection = %s", (collection,))

    def add(self, collection: str, rows: list[tuple[str, str, int, str, str, list[float]]]) -> None:
        """rows: (document, title, page, heading, body, embedding)"""
        with self.connect() as conn, conn.cursor() as cur:
            cur.executemany(
                f"INSERT INTO {self.table} (collection, document, title, page, heading, body, embedding) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s::vector)",
                [(collection, d, t, p, h, b, _vec(e)) for d, t, p, h, b, e in rows],
            )

    def search(self, collection: str, embedding: list[float], k: int) -> list[Hit]:
        with self.connect() as conn:
            rows = conn.execute(
                f"SELECT document, title, page, heading, body, 1 - (embedding <=> %s::vector) AS score "
                f"FROM {self.table} WHERE collection = %s ORDER BY embedding <=> %s::vector LIMIT %s",
                (_vec(embedding), collection, _vec(embedding), k),
            ).fetchall()
        return [Hit(document=r[0], title=r[1], page=r[2], heading=r[3], text=r[4], score=float(r[5])) for r in rows]

    def search_hybrid(self, collection: str, embedding: list[float], words: list[str], k: int, pool: int = 30, keyword_weight: float = 1.0
    ) -> list[Hit]:
        """Vector search and Postgres full-text search, merged by reciprocal rank fusion.

        The score on each hit is still its cosine similarity, so the refusal threshold means the same thing in both modes.
        """
        words = [w for w in words if w.isalnum()]
        if not words:
            return self.search(collection, embedding, k)
        fts = "to_tsvector('english', heading || ' ' || body)"
        sql = f"""
            WITH q AS (SELECT %(vec)s::vector AS v, to_tsquery('english', %(tsq)s) AS t),
            vec AS (
                SELECT id, row_number() OVER (ORDER BY embedding <=> q.v) AS r
                FROM {self.table}, q WHERE collection = %(c)s ORDER BY embedding <=> q.v LIMIT %(pool)s
            ),
            kw AS (
                SELECT id, row_number() OVER (ORDER BY ts_rank_cd({fts}, q.t) DESC, id) AS r
                FROM {self.table}, q WHERE collection = %(c)s AND {fts} @@ q.t
                ORDER BY ts_rank_cd({fts}, q.t) DESC, id LIMIT %(pool)s
            ),
            fused AS (
                SELECT id, sum(w / (60 + r)) AS rrf
                FROM (SELECT id, r, 1.0 AS w FROM vec UNION ALL SELECT id, r, %(kw)s AS w FROM kw) u GROUP BY id
            )
            SELECT document, title, page, heading, body, 1 - (embedding <=> q.v) AS score
            FROM fused JOIN {self.table} USING (id), q
            ORDER BY rrf DESC, score DESC LIMIT %(k)s
        """
        params = {"vec": _vec(embedding), "tsq": " | ".join(words), "c": collection, "pool": pool, "k": k, "kw": keyword_weight}
        with self.connect() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [Hit(document=r[0], title=r[1], page=r[2], heading=r[3], text=r[4], score=float(r[5])) for r in rows]

    def missing_terms(self, collection: str, terms: list[str]) -> list[str]:
        """Terms that occur in no chunk of the collection (case-insensitive substring match)."""
        missing = []
        with self.connect() as conn:
            for term in terms:
                row = conn.execute(
                    f"SELECT EXISTS (SELECT 1 FROM {self.table} WHERE collection = %s AND body ILIKE %s)",
                    (collection, f"%{term}%"),
                ).fetchone()
                if not row[0]:
                    missing.append(term)
        return missing

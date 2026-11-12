"""Chunk storage and similarity search in Postgres with the pgvector extension.

Search is exact by default: a scan ordered by cosine distance. With use_index
an HNSW index is built and Postgres uses it. A trigram index on the chunk text
serves the word lookups of the refusal check.
"""

from __future__ import annotations

import threading
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
    rerank_score: float | None = None  # cross-encoder score, set when the reranker is on


def _vec(values: list[float]) -> str:
    return "[" + ",".join(f"{v:.6f}" for v in values) + "]"


class PgVectorStore:
    def __init__(self, database_url: str, dim: int, table: str = "chunks", use_index: bool = False) -> None:
        if not table.isidentifier():
            raise ValueError("table name must be a plain identifier")
        self.url = database_url
        self.dim = dim
        self.table = table
        self.use_index = use_index
        self._conn: psycopg.Connection | None = None
        self._lock = threading.Lock()
        self._apply_index_setting()

    def _apply_index_setting(self) -> None:
        """Make the database match the setting: an HNSW index when use_index is on, none (exact search) when it is off."""
        with self.connect() as conn:
            if not conn.execute("SELECT to_regclass(%s)", (self.table,)).fetchone()[0]:
                return
        if self.use_index:
            self.create_index()
        else:
            self.drop_index()

    def connect(self) -> psycopg.Connection:
        return psycopg.connect(self.url)

    def _query(self, sql: str, params: tuple | dict = ()) -> list[tuple]:
        """Run a read query on one long-lived connection, reconnecting once if it has dropped."""
        with self._lock:
            for attempt in (0, 1):
                try:
                    if self._conn is None or self._conn.closed:
                        # No server-side prepared statements: with a generic plan Postgres cannot use the trigram index for ILIKE.
                        self._conn = psycopg.connect(self.url, autocommit=True, prepare_threshold=None)
                        # The HNSW index holds every collection, so the scan has to keep going until k rows pass the filter.
                        self._conn.execute("SET hnsw.iterative_scan = strict_order")
                        self._conn.execute("SET hnsw.ef_search = 100")
                    return self._conn.execute(sql, params).fetchall()
                except psycopg.OperationalError:
                    self._conn = None
                    if attempt:
                        raise
        return []

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
        self.create_text_index()

    def create_text_index(self) -> None:
        """A trigram index makes "does this word occur anywhere" a fast lookup instead of a scan of every chunk."""
        with self.connect() as conn:
            conn.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
            conn.execute(f"CREATE INDEX IF NOT EXISTS {self.table}_body_trgm_idx ON {self.table} USING gin (body gin_trgm_ops)")

    def drop_text_index(self) -> None:
        with self.connect() as conn:
            conn.execute(f"DROP INDEX IF EXISTS {self.table}_body_trgm_idx")

    def create_index(self) -> float:
        """Build an HNSW index for cosine distance. Returns the build time in seconds."""
        start = time.perf_counter()
        with self.connect() as conn:
            conn.execute(f"CREATE INDEX IF NOT EXISTS {self.table}_hnsw_idx ON {self.table} USING hnsw (embedding vector_cosine_ops)")
        return time.perf_counter() - start

    def drop_index(self) -> None:
        with self.connect() as conn:
            conn.execute(f"DROP INDEX IF EXISTS {self.table}_hnsw_idx")

    def count(self, collection: str) -> int:
        return int(self._query(f"SELECT count(*) FROM {self.table} WHERE collection = %s", (collection,))[0][0])

    def stats(self, collection: str) -> dict:
        """Row count and stored size of one collection, plus the size of the whole table with its indexes."""
        rows, size = self._query(
            f"SELECT count(*), coalesce(sum(pg_column_size(c.*)), 0) FROM {self.table} c WHERE collection = %s", (collection,)
        )[0]
        total = self._query("SELECT pg_total_relation_size(%s::regclass)", (self.table,))[0][0]
        return {"chunks": int(rows), "collection_bytes": int(size), "table_with_indexes_bytes": int(total)}

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
        rows = self._query(
            f"SELECT document, title, page, heading, body, 1 - (embedding <=> %s::vector) AS score "
            f"FROM {self.table} WHERE collection = %s ORDER BY embedding <=> %s::vector LIMIT %s",
            (_vec(embedding), collection, _vec(embedding), k),
        )
        return [Hit(document=r[0], title=r[1], page=r[2], heading=r[3], text=r[4], score=float(r[5])) for r in rows]

    def missing_terms(self, collection: str, terms: list[str]) -> list[str]:
        """Terms that occur in no chunk of the collection (case-insensitive substring match)."""
        missing = []
        for term in terms:
            found = self._query(
                f"SELECT EXISTS (SELECT 1 FROM {self.table} WHERE collection = %s AND body ILIKE %s)", (collection, f"%{term}%")
            )[0][0]
            if not found:
                missing.append(term)
        return missing

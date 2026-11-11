# rag-pdf-demo

A small question answering service over a folder of PDFs. You ask a question, it finds the passages that answer it, and it replies with the document name and page number for each passage it used. If nothing in the documents is close enough to the question, it says so and does not guess.

This is a demonstration built by Cedarwood Studio on public documents. It is not client work and contains no client data.

## What is in the box

- **Ingestion** (`ragdemo/pdf.py`, `ragdemo/chunking.py`): reads each PDF page by page, removes running headers and footers, finds section headings from font weight and numbering, and cuts the text into chunks that start at headings and never cross a page.
- **Metadata**: every chunk is stored with its file name, document title, page number and heading path (for example `3. Handling an Incident > 3.1 Preparation`).
- **Vector store** (`ragdemo/store.py`): Postgres 16 with the pgvector extension. Vectors sit in the same table as the document and page metadata. Search is by cosine similarity.
- **Embeddings** (`ragdemo/embed.py`): `BAAI/bge-small-en-v1.5` (384 dimensions) running on CPU through fastembed. No API key is needed.
- **Refusal path** (`ragdemo/pipeline.py`): if the best passage scores below a similarity threshold, the reply is "I could not find this in the documents." with no citations. A question that uses a word found nowhere in the corpus has to clear a stricter threshold.
- **Answer step** (`ragdemo/answer.py`), two providers behind one interface:
  - **Extractive** (default, no key): returns the best passages word for word, each with its document and page.
  - **Generated** (when `OPENAI_API_KEY` is set): sends the passages to an OpenAI-compatible chat completions endpoint and asks for an answer that cites passages by number. An answer that cites nothing is turned into a refusal.
- **API** (`ragdemo/api.py`): FastAPI with `POST /chat`, `GET /health`, and a plain chat page at `/`.
- **Evaluation** (`ragdemo/eval.py`): a fixed question set scored by script. Results are in [EVAL.md](EVAL.md).
- **Tests and CI**: pytest against a real pgvector database, ruff for lint, run by GitHub Actions on every push.

## Run it

Requirements: Docker with the compose plugin (or podman with podman-compose), and about 2 GB of disk. With podman, use `podman-compose` in place of `docker compose`, and `make COMPOSE=podman-compose` for the make targets.

```sh
docker compose up -d --build
```

The first start downloads the 12 PDFs (17 MB) from nist.gov, verifies their checksums, embeds them on CPU and stores them. That took about 9 minutes on a 4-core ARM machine. Follow it with `docker compose logs -f app`. Later starts skip ingestion.

Then open http://localhost:8000, or use curl:

```sh
curl -s localhost:8000/chat -H 'content-type: application/json' \
  -d '{"question": "What is a tabletop exercise?"}'
```

The response has these fields:

- `answer`: the reply text
- `refused`: `true` when the documents do not cover the question
- `mode`: `extractive` or `generated`
- `citations`: a list, each with `document`, `title`, `page`, `heading`, `score` and a `snippet`
- `top_score` and `threshold`: the best similarity score and the refusal cut-off it was compared with
- `unknown_terms`: words of the question that appear nowhere in the corpus

To use a language model for the answer step, set a key before starting:

```sh
OPENAI_API_KEY=sk-... OPENAI_MODEL=gpt-4o-mini docker compose up -d
```

`OPENAI_BASE_URL` points the same code at any other OpenAI-compatible endpoint.

## Evaluation

```sh
make eval            # tuned configuration
make ingest-baseline # builds the fixed-size chunk collection (about 8 minutes on CPU)
make eval-baseline   # baseline configuration
make eval-steps      # the intermediate steps in EVAL.md
make eval-heldout    # questions written after the settings were fixed
```

The question set is `eval/questions.json`: 26 questions whose answer is in the corpus, each with the expected document and the pages where the answer is stated, and 8 questions whose answer is not in the corpus. Page numbers are positions in the PDF file (what a PDF viewer shows), not the numbers printed on the page.

The recorded runs used the **extractive** answer mode: no language model wrote any answer. "Before" is fixed-size chunks with a guessed refusal threshold. "After" is heading and page aware chunks, a threshold chosen from a sweep, and a check for question words that appear nowhere in the corpus.

| Metric | Before | After |
| --- | --- | --- |
| Expected page is the top result | 13/26 (50%) | 16/26 (62%) |
| Expected page in top 3 | 21/26 (81%) | 22/26 (85%) |
| Expected page in top 5 | 22/26 (85%) | 22/26 (85%) |
| Answered with a citation to an accepted page | 21/26 (81%) | 22/26 (85%) |
| False refusals (in corpus) | 0/26 (0%) | 0/26 (0%) |
| Refusals (out of corpus, higher is better) | 1/8 (12%) | 8/8 (100%) |

Two things the table does not say on its own:

- The thresholds were tuned on these same questions. On 12 held-out questions written afterwards, retrieval and citations held (6 of 6 in-corpus questions cited correctly), but only 1 of 6 on-topic questions that the documents do not answer was refused. Refusing on retrieval scores catches off-topic questions, not near misses.
- One change that was tried made things worse (hybrid keyword and vector search) and was left switched off. It is recorded with its numbers.

Full tables, question by question, are in [EVAL.md](EVAL.md) and `eval/results/`.

## Corpus

Twelve NIST publications on information security for organizations, 805 pages in total. They are works of the US Government and are not subject to copyright in the United States (17 U.S.C. 105). The PDFs are not stored in this repository. `python -m ragdemo.corpus` downloads them from nist.gov and checks each file against the SHA-256 recorded in `corpus/sources.json`.

| Series | Title | Pages | Source |
| --- | --- | --- | --- |
| NIST CSWP 29 | The NIST Cybersecurity Framework (CSF) 2.0 | 32 | [NIST.CSWP.29.pdf](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf) |
| NISTIR 7621 Rev. 1 | Small Business Information Security: The Fundamentals | 55 | [NIST.IR.7621r1.pdf](https://nvlpubs.nist.gov/nistpubs/ir/2016/NIST.IR.7621r1.pdf) |
| NIST SP 800-12 Rev. 1 | An Introduction to Information Security | 101 | [NIST.SP.800-12r1.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-12r1.pdf) |
| NIST SP 800-34 Rev. 1 | Contingency Planning Guide for Federal Information Systems | 149 | [nistspecialpublication800-34r1.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf) |
| NIST SP 800-40 Rev. 4 | Guide to Enterprise Patch Management Planning | 28 | [NIST.SP.800-40r4.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-40r4.pdf) |
| NIST SP 800-46 Rev. 2 | Guide to Enterprise Telework, Remote Access, and Bring Your Own Device (BYOD) Security | 53 | [NIST.SP.800-46r2.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-46r2.pdf) |
| NIST SP 800-50 | Building an Information Technology Security Awareness and Training Program | 71 | [nistspecialpublication800-50.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-50.pdf) |
| NIST SP 800-61 Rev. 2 | Computer Security Incident Handling Guide | 80 | [NIST.SP.800-61r2.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r2.pdf) |
| NIST SP 800-63B | Digital Identity Guidelines: Authentication and Lifecycle Management | 80 | [NIST.SP.800-63b.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-63b.pdf) |
| NIST SP 800-83 Rev. 1 | Guide to Malware Incident Prevention and Handling for Desktops and Laptops | 47 | [NIST.SP.800-83r1.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-83r1.pdf) |
| NIST SP 800-88 Rev. 1 | Guidelines for Media Sanitization | 65 | [NIST.SP.800-88r1.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-88r1.pdf) |
| NIST SP 800-114 Rev. 1 | User's Guide to Telework and Bring Your Own Device (BYOD) Security | 44 | [NIST.SP.800-114r1.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-114r1.pdf) |

## Tests

```sh
docker compose up -d db
pip install -r requirements-dev.txt
DATABASE_URL=postgresql://rag:rag@localhost:54329/rag pytest -q
ruff check .
```

The tests build a three-page PDF, ingest it into a temporary pgvector table and check that chunks keep their page numbers, that `/chat` returns the right document and page, and that an out-of-corpus question is refused. They use a hashing embedder so that CI does not download a model.

## Limits

- **The recorded evaluation used the extractive answer mode.** No language model wrote any answer in the recorded runs, because the build environment had no API key. The generated mode is implemented and unit tested against a mocked endpoint, but its answer quality is not measured here. With a key, "citation correctness" would also have to check that the model's cited passage numbers are right, which the same script does.
- **The scores measure retrieval, citations and refusals, not the wording of answers.** There is no faithfulness or answer-relevance scoring (RAGAS or similar).
- **The question set is small and we wrote it ourselves.** 26 in-corpus and 8 out-of-corpus questions, with expected pages found by reading the PDFs. The thresholds were tuned on this same set, so the tuned numbers are optimistic. A client project would tune on one set of questions and report on another.
- **Refusal is a similarity threshold plus a word check, and it misses near misses.** A question that is on the corpus topic but not answered by it still gets passages back: 5 of 6 such questions in the held-out set were not refused. A language model in the answer step is the usual second line of defence, and that is the part not measured here.
- **The word check is crude.** It trims a few English endings and looks for the word as a substring. A misspelled word counts as unknown and raises the bar for that question.
- **Text PDFs only.** Scanned pages need OCR, which is not included. Tables are read as plain text lines, and figures are ignored.
- **Heading detection is a heuristic** (bold or larger font, section numbering). It is covered by tests and reads most sections of these twelve documents correctly, but not all: some title-page lines are taken as headings, and a numbered template in an appendix of SP 800-34 is read as a section. A new document family may need its rules adjusted.
- **Search is exact, with no vector index.** That is fast at this size (about 2,500 chunks). An HNSW index is a one-line addition for larger collections.
- **English only**, because of the embedding model.
- **No authentication, rate limiting or conversation memory.** Each question is answered on its own.
- **It does not use LangChain or LlamaIndex.** The pipeline is about 1,000 lines of plain Python, which keeps each step visible. Moving retrieval behind either library is straightforward if a project needs it.
- **Not deployed anywhere.** It runs with Docker Compose on one machine.

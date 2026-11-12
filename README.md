# rag-pdf-demo

A question answering service over a folder of PDFs. You ask a question, it finds the passages that answer it, and it replies with the document name and page number for each passage it used. If nothing in the documents answers the question, it says so and does not guess.

This repository is the **plain-Python implementation**: no RAG framework, each step is one short module. The same system built on LangChain is in [rag-pdf-demo-langchain](https://github.com/cedarwood-studio/rag-pdf-demo-langchain). The two repositories share their layout, file names, corpus, question sets, Makefile targets and evaluation output, so the matching files can be opened side by side.

This is a demonstration built by Cedarwood Studio on public documents. It is not client work and contains no client data.

## How a question is answered

1. **Retrieve** (`ragdemo/retrieval.py`, `ragdemo/store.py`): the question is embedded on CPU with `BAAI/bge-small-en-v1.5` and the 10 nearest chunks are read from Postgres with pgvector.
2. **Refuse early** (`ragdemo/refusal.py`): if the best chunk is below a similarity threshold, the reply is "I could not find this in the documents." A question that uses a word found nowhere in the corpus has to clear a stricter threshold.
3. **Rerank** (`ragdemo/rerank.py`): a small cross-encoder reads the question together with each of the 10 chunks and reorders them. The best 5 are kept. If even the best one scores low, the question is refused. This check is aimed at questions that are on the corpus topic but not answered by it.
4. **Answer** (`ragdemo/answer.py`), in one of two modes:
   - **Extractive** (default, no key): the best passages are returned word for word, each with its document and page.
   - **Generated** (when `OPENAI_API_KEY` is set): the passages go to an OpenAI-compatible chat model, which must cite passages by number and must refuse if they do not state the answer. An answer that cites nothing is turned into a refusal.
5. **Cite** (`ragdemo/pipeline.py`): every answer carries the file name, document title, page number and section heading of each passage it used.

Ingestion (`ragdemo/pdf.py`, `ragdemo/chunking.py`, `ragdemo/ingest.py`) reads each PDF page by page, removes running headers and footers, finds section headings from font weight and numbering, and cuts the text into chunks that start at headings and never cross a page.

## The two implementations, file by file

| File | What it does | Plain Python | lines | LangChain | lines |
| --- | --- | --- | --- | --- | --- |
| `ragdemo/pdf.py` | PDF text with page numbers and fonts | pypdf, one visitor function | 80 | The same file. LangChain's PDF loaders return page text without font data, and the heading detection needs the fonts. | 80 |
| `ragdemo/chunking.py` | Heading and page aware chunks | Own code | 167 | The same file. Nothing in LangChain splits on detected headings while keeping the page. | 167 |
| `ragdemo/ingest.py` | Read, chunk, embed, store | A loop over the files | 96 | The chunker wrapped as a `BaseLoader` that yields `Document` objects. The baseline uses `PyPDFLoader` and `RecursiveCharacterTextSplitter`. | 147 |
| `ragdemo/embed.py` | Embedding model and cache | A small protocol around fastembed | 124 | The same model behind LangChain's `Embeddings` interface. | 129 |
| `ragdemo/store.py` | pgvector table, insert, search, index | SQL written by hand | 158 | `PGVectorStore` from langchain-postgres creates the table, inserts, searches and builds the HNSW index. Counts, sizes and the word lookup are still SQL. | 131 |
| `ragdemo/retrieval.py` | Question to scored passages | One class | 25 | A `BaseRetriever` subclass, because the stock retriever drops the scores. | 45 |
| `ragdemo/rerank.py` | Cross-encoder reranking | fastembed cross-encoder | 33 | The same model as a `BaseDocumentCompressor`. | 45 |
| `ragdemo/refusal.py` | The refusal checks | Own code | 70 | The same logic, reading scores from document metadata. | 70 |
| `ragdemo/answer.py` | Extractive and generated answers | A prompt string and a parser | 75 | `ChatPromptTemplate`, the chat model and `StrOutputParser` joined with the pipe operator. Same parser. | 82 |
| `ragdemo/llm.py` | Chat model client, token count, spend cap | An httpx client with retries | 92 | `ChatOpenAI` plus a callback handler for the spend cap. | 84 |
| `ragdemo/pipeline.py` | The whole path, wired together | One method of about 25 lines | 135 | One LCEL chain with a `RunnableBranch` for the refusal path. | 166 |
| `ragdemo/api.py` | FastAPI app | FastAPI | 70 | The same file. | 70 |
| `ragdemo/eval.py` | Retrieval, citation and refusal scoring | Own code | 231 | The same, reading document metadata. | 231 |
| `ragdemo/eval_answers.py` | Answer correctness and faithfulness grading | Two prompts and a JSON reply | 195 | The grader is a chain: prompt, model in JSON mode, `JsonOutputParser`. | 207 |
| `ragdemo/bench.py` | Latency and size | Own code | 107 | The same. | 107 |
| `ragdemo/config.py` | Settings from the environment | Own code | 62 | The same, apart from the default database port. | 62 |
| `ragdemo/corpus.py` | Download and checksum the PDFs | Own code | 53 | The same file. | 53 |
| Total | | | 1,773 | | 1,876 |

Line counts are of the files in `ragdemo/`, comments and blank lines included.

## Run it

Requirements: Docker with the compose plugin (or podman with podman-compose), and about 3 GB of disk. With podman, use `podman-compose` in place of `docker compose`, and `make COMPOSE=podman-compose` for the make targets.

```sh
docker compose up -d --build
```

The first start downloads the 12 core PDFs (17 MB) from nist.gov, verifies their checksums, embeds them on CPU and stores them. That takes about 9 minutes on a 4-core ARM machine. Follow it with `docker compose logs -f app`. Later starts skip ingestion.

Then open http://localhost:8000, or use curl:

```sh
curl -s localhost:8000/chat -H 'content-type: application/json' \
  -d '{"question": "What is a tabletop exercise?"}'
```

The response has these fields:

- `answer`: the reply text
- `refused`: `true` when the documents do not answer the question
- `refused_by`: which check refused (`similarity`, `unknown word`, `rerank` or `model`), empty otherwise
- `mode`: `extractive` or `generated`
- `citations`: a list, each with `document`, `title`, `page`, `heading`, `score` and a `snippet`
- `top_score` and `threshold`: the best similarity score and the cut-off it was compared with
- `rerank_score`: the best cross-encoder score, when the reranker ran
- `unknown_terms`: words of the question that appear nowhere in the corpus

To load all 100 PDFs and serve them:

```sh
make ingest-full                      # over an hour on a 4-core CPU the first time
CORPUS=full docker compose up -d
```

To use a language model for the answer step, set a key in your shell before starting. It is read from the environment only and is never written to a file by this code.

```sh
OPENAI_API_KEY=... OPENAI_MODEL=gpt-4o-mini docker compose up -d
```

`OPENAI_BASE_URL` points the same code at any other OpenAI-compatible endpoint.

## Results

Every number in this section is from the **extractive** answer mode: no language model wrote any answer. Generated answers are built and tested but not measured, because the OpenAI key supplied for this work had no credit (details in [EVAL.md](EVAL.md)).

The 26 answerable and 8 off-topic questions of `eval/questions.json`, in both implementations, at 12 and at 100 PDFs:

| Metric | Plain, 12 PDFs | LangChain, 12 PDFs | Plain, 100 PDFs | LangChain, 100 PDFs |
| --- | --- | --- | --- | --- |
| Expected page is the top result | 20/26 (77%) | 20/26 (77%) | 17/26 (65%) | 17/26 (65%) |
| Expected page in top 3 | 21/26 (81%) | 21/26 (81%) | 20/26 (77%) | 20/26 (77%) |
| Expected page in top 5 | 23/26 (88%) | 23/26 (88%) | 20/26 (77%) | 20/26 (77%) |
| Answered with a citation to an accepted page | 21/26 (81%) | 21/26 (81%) | 20/26 (77%) | 20/26 (77%) |
| False refusals (answerable questions) | 0/26 (0%) | 0/26 (0%) | 1/26 (4%) | 1/26 (4%) |
| Refusals (unanswerable questions, higher is better) | 8/8 (100%) | 8/8 (100%) | 7/8 (88%) | 7/8 (88%) |

- **Both implementations give the same result on every question.** They share chunks, vectors and thresholds. LangChain changes the wiring, not the output.
- **Growing the corpus eight times cost about one question in eight.** The added documents are on the same subject and compete for every question. One of the "misses" at 100 PDFs is a correct answer from a different document, and one is an answer from an outdated version of a document. Both are discussed in EVAL.md.
- **Held-out questions written after the settings were fixed:** 9 of 10 answerable questions cited correctly at 12 PDFs, 8 of 10 at 100, no false refusals.
- **The refusal path is the weak part.** Off-topic questions are refused (8 of 8, and 7 of 8 at 100 PDFs). Of 10 held-out questions that are on the corpus topic but not answered by it, 5 were refused at 12 PDFs and 4 at 100. Without the reranker it was 3 and 2. The remaining cases need a language model to read the passages, and that step is the one not yet measured.

Size and speed on 4 CPU cores, no GPU:

| | 12 PDFs | 100 PDFs |
| --- | --- | --- |
| Pages / chunks | 805 / 2,448 | 6,252 / 18,205 |
| Stored size before indexes | 6 MB | 42 MB |
| First ingest, embedding on CPU | about 9 minutes | about 72 minutes |
| Vector search, exact, p50 (plain / LangChain) | 15 / 20 ms | 103 / 108 ms |
| Vector search, HNSW index, p50 (plain / LangChain) | 3 / 21 ms | 2 / 6 ms |
| Whole answer with reranker, p50 / p95 (plain) | 774 / 1016 ms | 941 / 2135 ms |
| Whole answer with reranker, p50 / p95 (LangChain) | 817 / 1280 ms | 835 / 1299 ms |

The reranker, not the database, sets the response time: about 0.7 seconds of CPU per question. The full tables, the index comparison and the method are in [EVAL.md](EVAL.md).

## What LangChain changed

This section is the same in both repositories.

**Size.** The `ragdemo` package is 1,773 lines in plain Python and 1,876 lines with LangChain. The framework did not make the code shorter. It moved where the lines are: `store.py` shrank from 158 to 131 lines and `llm.py` from 92 to 84, while `pipeline.py` grew from 135 to 166 and `ingest.py` from 96 to 147. Four files are identical, and `config.py` differs only in the default database port. Installed with its test tools, the plain version pulls in 51 Python packages (324 MB) and the LangChain version 91 (504 MB).

**What got simpler.**

- **The vector store.** `PGVectorStore` creates the table, inserts rows, runs the similarity query and builds the HNSW index in one call each. The plain version writes that SQL by hand, including a pgvector setting needed to combine an index with a filter on the collection.
- **The model call.** `ChatOpenAI` replaces a hand-written HTTP client: retries, JSON replies and token usage come with it. The prompt, model and parser join with one operator.
- **Testing the model path.** LangChain's fake chat model stands in for the API in tests with one line.
- **A first baseline.** The stock PDF loader and text splitter give a working ingestion in about ten lines.

**What got harder, or had to be worked around.**

- **Scores are dropped by the stock retriever.** The refusal path needs the similarity score of every passage, so the retriever is a subclass that calls the store's scored search.
- **There is no refusal path to reuse.** The thresholds, the unknown-word check and the rerank check are the same hand-written logic in both repositories. LangChain contributes the branch that routes around the answer step.
- **The chain is harder to follow than the function it replaces.** State travels through the chain as a dictionary, and a mistake in a key shows up at run time inside the framework's call stack.
- **A threading surprise.** The vector store calls the embedder from a worker thread. The SQLite embedding cache that worked in the plain version failed there until it was given a lock.
- **Reranking.** LangChain's own cross-encoder reranker loads models through PyTorch. To keep the small ONNX model, the reranker is a custom document compressor.
- **SQL did not go away.** Row counts, storage size and the word lookup for the refusal check use a second database connection beside the vector store.
- **Dependency churn.** The stock PDF loader lives in `langchain-community`, which prints a notice on import that the package is being retired.

**Scores.** Identical on every question set at both corpus sizes with exact search. With the HNSW index at 100 PDFs the LangChain version lost one correct citation and gained one false refusal, and the plain version did not change. LangChain's stock loader and splitter, used as the baseline, gave a correct citation for 19 of 26 questions against 22 for this project's chunker, which is why both versions use the same chunker.

**Speed.** No difference that matters. Vector search through LangChain costs about 3 ms more per question with the index and nothing measurable without it. Writing 18,205 chunks took about one and a half times as long through LangChain. Both are dominated by the reranker.

**In short:** for this brief LangChain is a reasonable way to hold the pipeline together and the client asked for it by name, so it is the version to build on. It did not remove the parts that decide accuracy (chunking, thresholds, refusal, evaluation), and those are the same code in both repositories.

## Evaluation commands

```sh
make ingest ingest-full ingest-baseline   # the three collections
make eval eval-full eval-baseline         # retrieval, citations and refusals, extractive answers
make eval-norerank                        # the same with the reranker off
make eval-heldout                         # two question sets written after settings were fixed
make bench                                # latency and storage, exact search and HNSW index
OPENAI_API_KEY=... make eval-answers PY=.venv/bin/python   # generated answers, graded
```

Every run writes a JSON file and a Markdown table, question by question, to `eval/results/`. The method and the full history are in [EVAL.md](EVAL.md).

The question sets:

- `eval/questions.json`: 26 questions answered by the core documents and 8 off-topic questions. Used for tuning.
- `eval/questions-heldout.json`: 6 answerable and 6 on-topic unanswerable questions. Written as a held-out set in the first round, then used to set the rerank threshold.
- `eval/questions-heldout2.json`: 10 answerable, 10 on-topic unanswerable and 2 off-topic questions. Written after all settings were fixed and run once.

Each answerable question lists the document and the pages where its answer is stated, and a short reference answer. Page numbers are positions in the PDF file (what a PDF viewer shows), not the numbers printed on the page.

## Corpus

100 NIST publications on information security, 6,252 pages. They are works of the US Government and are not subject to copyright in the United States (17 U.S.C. 105). The PDFs are not stored in this repository: `python -m ragdemo.corpus` downloads them from nist.gov and checks each against the SHA-256 in `corpus/sources.json`. The full list with links is in [corpus/SOURCES.md](corpus/SOURCES.md).

- **Core set:** 12 documents, 805 pages. All evaluation questions are answered from these.
- **Extended set:** 88 more documents on the same subject, 5,447 pages. They are there to compete with the core set at scale.

## Tests

```sh
docker compose up -d db
pip install -r requirements-dev.txt
pytest -q
ruff check .
```

The tests build a three-page PDF, ingest it into a temporary pgvector table and check that chunks keep their page numbers, that `/chat` returns the right document and page, that an out-of-corpus question is refused, that the reranker can reorder and refuse, and that the generated-answer path and its spend cap behave, using a mocked model. They use a hashing embedder so that CI downloads no model. GitHub Actions runs lint and tests on every push.

## Limits

- **Generated answers are not measured.** The answer-quality evaluation is ready and has not run, because the API key supplied had no credit. Every number in this repository is from extractive mode.
- **The refusal path misses about half of the on-topic unanswerable questions** in extractive mode. Off-topic questions are refused reliably at 12 PDFs and mostly at 100.
- **Accuracy fell as the corpus grew** from 12 to 100 PDFs, under thresholds tuned at 12 and not retuned.
- **Old and new versions of a document compete.** With two versions of the Cybersecurity Framework in the corpus, a question about the current one was answered from the old one. Nothing here detects or prefers the newer document.
- **The question sets are small and we wrote them.** 26 plus 8 for tuning, 22 held out. The expected pages were spot-checked by a second automated reader, not by a person.
- **One answer takes about a second on CPU** because of the reranker, before any language model call. `RERANK=0` turns it off and gives back the accuracy shown in EVAL.md.
- **The first ingest of 100 PDFs takes over an hour on 4 CPU cores.** Embedding on CPU is the cost. An embedding API or a GPU removes most of it.
- **Text PDFs only.** Scanned pages need OCR, which is not included. Tables are read as plain text lines, and figures are ignored.
- **Heading detection is a heuristic** (bold or larger font, section numbering). It is covered by tests and reads most sections of these documents correctly, but not all: some title-page lines are taken as headings, and a numbered template in an appendix of SP 800-34 is read as a section.
- **The unknown-word check is crude.** It trims a few English endings and looks for the word as a substring. A misspelled word counts as unknown and raises the bar for that question. It also weakens as the corpus grows, because more words occur somewhere.
- **English only**, because of the embedding and reranking models.
- **No authentication, rate limiting or conversation memory.** Each question is answered on its own.
- **Not deployed anywhere.** It runs with Docker Compose on one machine, and was run here with podman.

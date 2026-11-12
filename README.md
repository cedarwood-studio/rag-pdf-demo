# rag-pdf-demo

A question answering service over a folder of PDFs. You ask a question, it finds the passages that answer it, and it replies with the document name and page number for each passage it used. If nothing in the documents answers the question, it says so and does not guess.

This repository is the **plain-Python implementation**: no RAG framework, each step is one short module. The same system built on LangChain is in [rag-pdf-demo-langchain](https://github.com/cedarwood-studio/rag-pdf-demo-langchain). The two repositories share their layout, file names, corpus, question sets, Makefile targets and evaluation output, so the matching files can be opened side by side.

This is a demonstration built by Cedarwood Studio on public documents. It is not client work and contains no client data.

## How a question is answered

1. **Retrieve** (`ragdemo/retrieval.py`, `ragdemo/store.py`): the question is embedded on CPU with `BAAI/bge-small-en-v1.5` and the 5 nearest chunks are read from Postgres with pgvector.
2. **Refuse early** (`ragdemo/refusal.py`): if the best chunk is below a similarity threshold, the reply is "I could not find this in the documents." A question that uses a word found nowhere in the corpus has to clear a stricter threshold.
3. **Answer** (`ragdemo/answer.py`), in one of two modes:
   - **Extractive** (default, no key): the best passages are returned word for word, each with its document and page.
   - **Generated** (when `OPENAI_API_KEY` is set): the passages go to a chat model, which must cite passages by number and must refuse if they do not state the answer. An answer that cites nothing is turned into a refusal.
4. **Cite** (`ragdemo/pipeline.py`): every answer carries the file name, document title, page number and section heading of each passage it used.

An **optional reranker** (`ragdemo/rerank.py`, `RERANK=1`) sits between steps 2 and 3. A small cross-encoder reads the question together with each of the 10 nearest chunks, reorders them, keeps the best 5, and refuses the question if even the best one scores low. It is off by default because of the licence position of its model (see Licences). Results are given with and without it.

Ingestion (`ragdemo/pdf.py`, `ragdemo/chunking.py`, `ragdemo/ingest.py`) reads each PDF page by page, removes running headers and footers, finds section headings from font weight and numbering, and cuts the text into chunks that start at headings and never cross a page.

## The two implementations, file by file

| File | What it does | Plain Python | lines | LangChain | lines |
| --- | --- | --- | --- | --- | --- |
| `ragdemo/pdf.py` | PDF text with page numbers and fonts | pypdf, one visitor function | 80 | The same file. LangChain's PDF loaders return page text without font data, and the heading detection needs the fonts. | 80 |
| `ragdemo/chunking.py` | Heading and page aware chunks | Own code | 167 | The same file. Nothing in LangChain splits on detected headings while keeping the page. | 167 |
| `ragdemo/ingest.py` | Read, chunk, embed, store | A loop over the files | 96 | The chunker wrapped as a `BaseLoader` that yields `Document` objects. The baseline uses `PyPDFLoader` and `RecursiveCharacterTextSplitter`. | 147 |
| `ragdemo/embed.py` | Embedding model and cache | A small protocol around fastembed | 124 | The same model behind LangChain's `Embeddings` interface. | 129 |
| `ragdemo/store.py` | pgvector table, insert, search, index | SQL written by hand | 167 | `PGVectorStore` from langchain-postgres creates the table, inserts, searches and builds the HNSW index. Counts, sizes and the word lookup are still SQL. | 135 |
| `ragdemo/retrieval.py` | Question to scored passages | One class | 25 | A `BaseRetriever` subclass, because the stock retriever drops the scores. | 45 |
| `ragdemo/rerank.py` | Cross-encoder reranking | fastembed cross-encoder | 33 | The same model as a `BaseDocumentCompressor`. | 45 |
| `ragdemo/refusal.py` | The refusal checks | Own code | 70 | The same logic, reading scores from document metadata. | 70 |
| `ragdemo/answer.py` | Extractive and generated answers | A prompt string and a parser | 75 | `ChatPromptTemplate`, the chat model and `StrOutputParser` joined with the pipe operator. Same parser. | 82 |
| `ragdemo/llm.py` | Chat model client, token count, spend cap | An httpx client with retries | 92 | `ChatOpenAI` plus a callback handler for the spend cap. | 84 |
| `ragdemo/pipeline.py` | The whole path, wired together | One method of about 25 lines | 135 | One LCEL chain with a `RunnableBranch` for the refusal path. | 166 |
| `ragdemo/api.py` | FastAPI app | FastAPI | 70 | The same file. | 70 |
| `ragdemo/eval.py` | Retrieval, citation and refusal scoring | Own code | 231 | The same, reading document metadata. | 231 |
| `ragdemo/eval_answers.py` | Answer correctness and faithfulness grading | Two prompts and a JSON reply | 199 | The grader is a chain: prompt, model in JSON mode, `JsonOutputParser`. | 211 |
| `ragdemo/bench.py` | Latency and size | Own code | 106 | The same. | 106 |
| `ragdemo/config.py` | Settings from the environment | Own code | 63 | The same file. | 63 |
| `ragdemo/corpus.py` | Download and checksum the PDFs | Own code | 53 | The same file. | 53 |
| Total | | | 1,786 | | 1,884 |

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
- `rerank_score`: the best cross-encoder score, when the optional reranker ran
- `unknown_terms`: words of the question that appear nowhere in the corpus

To load all 100 PDFs and serve them:

```sh
make ingest-full                      # over an hour on a 4-core CPU the first time
CORPUS=full docker compose up -d
```

### Generated answers

Set a key in your shell before starting. It is read from the environment only and is never written to a file by this code.

```sh
OPENAI_API_KEY=... docker compose up -d
```

The defaults are the OpenAI API and `gpt-4o-mini`. Any OpenAI-compatible endpoint works by setting three variables: `OPENAI_BASE_URL`, `ANSWER_MODEL`, and that endpoint's key in `OPENAI_API_KEY`. The generated-answer numbers below were produced this way through OpenRouter:

```sh
OPENAI_API_KEY=... OPENAI_BASE_URL=https://openrouter.ai/api/v1 ANSWER_MODEL=openai/gpt-4o-mini docker compose up -d
```

## Results

Two answer modes were measured, and every table says which one it shows.

- **Extractive:** no language model. The reply quotes the best passages with their pages.
- **Generated:** `openai/gpt-4o-mini` writes the answer from the passages and must cite them or refuse. It was called through OpenRouter's OpenAI-compatible endpoint, and the same model graded the answers.

All numbers are with the default configuration: exact vector search, no reranker. The two implementations are shown side by side at 12 and at 100 PDFs.

**Retrieval and citations, extractive mode.** The 26 answerable and 8 off-topic questions of `eval/questions.json`:

| Metric | Plain, 12 PDFs | LangChain, 12 PDFs | Plain, 100 PDFs | LangChain, 100 PDFs |
| --- | --- | --- | --- | --- |
| Expected page is the top result | 16/26 (62%) | 16/26 (62%) | 13/26 (50%) | 13/26 (50%) |
| Expected page in top 3 | 22/26 (85%) | 22/26 (85%) | 18/26 (69%) | 18/26 (69%) |
| Expected page in top 5 | 22/26 (85%) | 22/26 (85%) | 20/26 (77%) | 20/26 (77%) |
| Answered with a citation to an accepted page | 22/26 (85%) | 22/26 (85%) | 18/26 (69%) | 18/26 (69%) |
| False refusals (answerable questions) | 0/26 (0%) | 0/26 (0%) | 0/26 (0%) | 0/26 (0%) |
| Refusals (unanswerable questions, higher is better) | 8/8 (100%) | 8/8 (100%) | 4/8 (50%) | 4/8 (50%) |

**Answers, generated mode.** The same questions:

| Metric | Plain, 12 PDFs | LangChain, 12 PDFs | Plain, 100 PDFs | LangChain, 100 PDFs |
| --- | --- | --- | --- | --- |
| Answer correct | 18/26 (69%) | 18/26 (69%) | 16/26 (62%) | 16/26 (62%) |
| Answer partly correct | 5/26 (19%) | 5/26 (19%) | 7/26 (27%) | 7/26 (27%) |
| Answer incorrect | 0/26 (0%) | 0/26 (0%) | 0/26 (0%) | 0/26 (0%) |
| False refusals (answerable questions) | 3/26 (12%) | 3/26 (12%) | 3/26 (12%) | 3/26 (12%) |
| Answered with a citation to an accepted page | 21/26 (81%) | 21/26 (81%) | 20/26 (77%) | 20/26 (77%) |
| Faithful to its cited passages (of answers given) | 20/23 (87%) | 20/23 (87%) | 17/23 (74%) | 17/23 (74%) |
| Partly faithful (of answers given) | 3/23 (13%) | 3/23 (13%) | 6/23 (26%) | 6/23 (26%) |
| Unfaithful (of answers given) | 0/23 (0%) | 0/23 (0%) | 0/23 (0%) | 0/23 (0%) |
| Refusals (unanswerable questions, higher is better) | 8/8 (100%) | 8/8 (100%) | 8/8 (100%) | 8/8 (100%) |
| of which refused by the model itself | 0/8 (0%) | 0/8 (0%) | 4/8 (50%) | 4/8 (50%) |

**The hard case: questions on the corpus topic that the documents do not answer.** Ten such questions from the held-out set written after all settings were fixed:

| On-topic unanswerable questions refused | Plain, 12 PDFs | LangChain, 12 PDFs | Plain, 100 PDFs | LangChain, 100 PDFs |
| --- | --- | --- | --- | --- |
| Extractive mode | 3/10 | 3/10 | 2/10 | 2/10 |
| Generated mode | 9/10 (3 by checks, 6 by the model) | 9/10 (3 by checks, 6 by the model) | 9/10 (2 by checks, 7 by the model) | 9/10 (2 by checks, 7 by the model) |

What to take from this:

- **Both implementations behave the same.** Extractive results are identical question for question. Generated results differ by a question here and there, because the model is not perfectly repeatable.
- **The model is what makes the refusal path work.** Retrieval checks alone refuse 3 of 10 on-topic unanswerable questions (2 at 100 PDFs). With the model, 9 of 10. The tenth was a mistake in our question set: the document does give the answer, and the model found it.
- **No generated answer was graded unsupported by its cited passages.** Most were graded fully supported and the rest partly.
- **Answers were graded correct for 18 of 26 questions at 12 PDFs and 16 of 26 at 100,** with 5 and 7 partly correct and none incorrect. On the held-out set one answer in ten was graded incorrect at 100 PDFs.
- **Generated mode refuses 3 of 26 answerable questions** where extractive mode refuses none. In those cases retrieval had not found the right page, and the model declined instead of answering from the wrong one.
- **Growing the corpus eight times cost four correct citations out of 26 in extractive mode** (22 to 18) and halved the off-topic refusals of the retrieval checks (8 to 4 of 8). The model still refused all 8.
- **The grader is the same model that wrote the answers,** so the correctness and faithfulness figures are optimistic until a person has read a sample.

Size and speed on 4 CPU cores, no GPU (extractive mode, so no model call is included):

| | 12 PDFs | 100 PDFs |
| --- | --- | --- |
| Pages / chunks | 805 / 2,448 | 6,252 / 18,205 |
| Stored size before indexes | 6 MB | 42 MB |
| First ingest, embedding on CPU | about 9 minutes | about 72 minutes |
| Vector search, exact, p50 (plain / LangChain) | 15 / 21 ms | 103 / 108 ms |
| Vector search, HNSW index, p50 (plain / LangChain) | 3 / 22 ms | 2 / 6 ms |
| Whole answer path, p50 / p95 (plain) | 110 / 200 ms | 139 / 294 ms |
| Whole answer path, p50 / p95 (LangChain) | 60 / 101 ms | 147 / 192 ms |

The generated-mode runs of both repositories together cost an estimated $0.13 (680,081 input and 40,170 output tokens), computed from the token counts the API returned.

The held-out sets, the optional reranker, the index comparison, the baselines and the method are in [EVAL.md](EVAL.md).

## What LangChain changed

This section is the same in both repositories.

**Size.** The `ragdemo` package is 1,786 lines in plain Python and 1,884 lines with LangChain. The framework did not make the code shorter. It moved where the lines are: `store.py` shrank from 167 to 135 lines and `llm.py` from 92 to 84, while `pipeline.py` grew from 135 to 166 and `ingest.py` from 96 to 147. Four files are identical, and `config.py` differs only in the default database port. Installed with its test tools, the plain version pulls in 51 Python packages (324 MB) and the LangChain version 91 (504 MB).

**What got simpler.**

- **The vector store.** `PGVectorStore` creates the table, inserts rows, runs the similarity query and builds the HNSW index in one call each. The plain version writes that SQL by hand, including a pgvector setting needed to combine an index with a filter on the collection.
- **The model call.** `ChatOpenAI` replaces a hand-written HTTP client: retries, JSON replies and token usage come with it. The prompt, model and parser join with one operator. Pointing it at another OpenAI-compatible endpoint was a base URL in both versions.
- **Testing the model path.** LangChain's fake chat model stands in for the API in tests with one line.
- **A first baseline.** The stock PDF loader and text splitter give a working ingestion in about ten lines.

**What got harder, or had to be worked around.**

- **Scores are dropped by the stock retriever.** The refusal path needs the similarity score of every passage, so the retriever is a subclass that calls the store's scored search.
- **There is no refusal path to reuse.** The thresholds, the unknown-word check and the rerank check are the same hand-written logic in both repositories. LangChain contributes the branch that routes around the answer step.
- **The chain is harder to follow than the function it replaces.** State travels through the chain as a dictionary, and a mistake in a key shows up at run time inside the framework's call stack.
- **A threading surprise.** The vector store calls the embedder from a worker thread. The SQLite embedding cache that worked in the plain version failed there until it was given a lock.
- **Reranking.** LangChain's own cross-encoder reranker loads models through PyTorch. To keep the small ONNX model, the optional reranker is a custom document compressor.
- **SQL did not go away.** Row counts, storage size and the word lookup for the refusal check use a second database connection beside the vector store.
- **Dependency churn.** The stock PDF loader lives in `langchain-community`, which prints a notice on import that the package is being retired.

**Scores.** Extractive results are identical on every question set at both corpus sizes with exact search. Generated results agree to within a question or two per set, which is the run-to-run variation of the model. With the HNSW index at 100 PDFs retrieval and citation scores were unchanged in both, and the LangChain version refused one more off-topic question. LangChain's stock loader and splitter, used as the baseline, gave a correct citation for 19 of 26 questions against 22 for this project's chunker, which is why both versions use the same chunker.

**Speed.** No difference that matters. Vector search through LangChain costs a few milliseconds more per question. At 12 PDFs the plain version's whole answer path is the slower one (110 against 60 ms at the median), because it keeps all three collections in one table and filters, where LangChain has a table per collection. Writing 18,205 chunks took about one and a half times as long through LangChain.

**In short:** for this brief LangChain is a reasonable way to hold the pipeline together and the client asked for it by name, so it is the version to build on. It did not remove the parts that decide accuracy (chunking, thresholds, refusal, evaluation), and those are the same code in both repositories.

## Evaluation commands

```sh
make ingest ingest-full ingest-baseline   # the three collections
make eval eval-full eval-baseline         # retrieval, citations and refusals, extractive answers
make eval-heldout                         # two question sets written after settings were fixed
make eval-rerank                          # the same runs with the optional reranker on
make bench                                # latency and storage: exact search, HNSW index, reranker
OPENAI_API_KEY=... make eval-answers eval-answers-rerank PY=.venv/bin/python   # generated answers, graded
```

Every run writes a JSON file and a Markdown table, question by question, to `eval/results/`. The method and the full history are in [EVAL.md](EVAL.md).

The question sets:

- `eval/questions.json`: 26 questions answered by the core documents and 8 off-topic questions. Used for tuning.
- `eval/questions-heldout.json`: 6 answerable and 6 on-topic unanswerable questions. Written as a held-out set in the first round, then used to set the rerank threshold.
- `eval/questions-heldout2.json`: 10 answerable, 10 on-topic unanswerable and 2 off-topic questions. Written after all settings were fixed.

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

## Licences

This section records what was checked before these repositories could be made public. It is a reading of licence statements, not legal advice.

- **This code** has no licence file yet. The repository is private. A licence has to be chosen before it is published.
- **The corpus** is US Government work, not subject to copyright in the United States (17 U.S.C. 105). The PDFs are fetched by script and are not in the repository.
- **Embedding model, in the default path:** `BAAI/bge-small-en-v1.5`. fastembed downloads it from the Hugging Face repository `Qdrant/bge-small-en-v1.5-onnx-Q`. The model card of that repository and the card of the original model both state `license: mit`. Neither card lists the training data. The container image includes these weights.
- **Reranker model, optional and off by default:** `Xenova/ms-marco-MiniLM-L-6-v2`.
  - It is an ONNX conversion of `cross-encoder/ms-marco-MiniLM-L6-v2`. The card of the conversion states no licence. The card of the original states `license: apache-2.0` and lists its training data as `sentence-transformers/msmarco`.
  - The MS MARCO terms say: "The MS MARCO datasets are intended for non-commercial research purposes only ... and is made available free of charge without extending any license or other intellectual property rights."
  - Whether a dataset's terms reach a model trained on it is not settled, and the exact files we download carry no licence statement of their own. So the reranker is off by default, its weights are not in the container image, and they are downloaded only when `RERANK=1` is set. All headline numbers are without it, and EVAL.md gives the numbers with it.
  - Two Apache 2.0 cross-encoders were tried as replacements and scored lower (EVAL.md). Their cards do not list training data either.
- **Chat model:** called over an API (`gpt-4o-mini`). No model weights are involved. The provider's terms of service apply to whoever supplies the key.
- **Python dependencies.** The licence field of every installed package was read from its metadata. All are MIT, BSD, Apache 2.0, ISC or PSF except these:
  - `psycopg` and `psycopg-binary`, the Postgres driver: LGPL-3.0-only. It is used unmodified as a library, which the LGPL allows without affecting the licence of this code. Anyone shipping a container image passes on the LGPL's terms for that component.
  - `certifi`: MPL-2.0. `tqdm`: `MPL-2.0 AND MIT`. Both are used unmodified, and MPL's conditions apply only to changes to their own files.
  - `py_rust_stemmers`, pulled in by fastembed: no licence in its package metadata. Its source repository on GitHub is marked MIT.
- **Postgres and pgvector** are both under the PostgreSQL License, which is permissive.
- **The method** was a script over package metadata and a reading of five model cards. Transitive licence texts were not read in full, and container base images were not audited.

## Limits

- **Generated answers were graded by the model that wrote them.** No person has read the graded answers, apart from the rows quoted in EVAL.md.
- **Without a language model the refusal path is weak for on-topic questions.** In extractive mode the retrieval checks refuse 3 of 10 on-topic unanswerable questions, and 2 of 10 at 100 PDFs. With the model it is 9 of 10.
- **With a language model, some answerable questions are refused:** 3 of 26 on the main set, where retrieval had not found the right page.
- **Accuracy fell as the corpus grew** from 12 to 100 PDFs, under thresholds tuned at 12 and not retuned.
- **Old and new versions of a document compete, and documents can disagree.** With two versions of the Cybersecurity Framework in the corpus, passages from the old one were retrieved for a question about the current one. Two documents give opposite advice on changing passwords, and the generated answer reports both. Nothing here detects or prefers the newer document.
- **The question sets are small and we wrote them.** 26 plus 8 for tuning, 34 held out. The expected pages were spot-checked by a second automated reader, not by a person, and one question labelled unanswerable turned out to be answerable.
- **The OpenAI API itself was not exercised.** The default endpoint in the code is OpenAI's, but the account available had no credit, so generated mode was run through OpenRouter with the same model.
- **The first ingest of 100 PDFs takes over an hour on 4 CPU cores.** Embedding on CPU is the cost. An embedding API or a GPU removes most of it.
- **Text PDFs only.** Scanned pages need OCR, which is not included. Tables are read as plain text lines, and figures are ignored.
- **Heading detection is a heuristic** (bold or larger font, section numbering). It is covered by tests and reads most sections of these documents correctly, but not all: some title-page lines are taken as headings, and a numbered template in an appendix of SP 800-34 is read as a section.
- **The unknown-word check is crude.** It trims a few English endings and looks for the word as a substring. A misspelled word counts as unknown and raises the bar for that question. It also weakens as the corpus grows, because more words occur somewhere.
- **English only**, because of the embedding model.
- **No authentication, rate limiting or conversation memory.** Each question is answered on its own.
- **Not deployed anywhere.** It runs with Docker Compose on one machine, and was run here with podman.

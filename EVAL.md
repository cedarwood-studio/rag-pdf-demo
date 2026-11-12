# Evaluation

Every number on this page comes from a script in this repository or in its twin, [rag-pdf-demo-langchain](https://github.com/cedarwood-studio/rag-pdf-demo-langchain). The raw output of every run, question by question, is in `eval/results/` of each repository. This page is the same in both.

## Read this first: which answer mode each number came from

- **Extractive mode** means no language model wrote anything. The answer is the best passages quoted word for word, and the citations are the pages those passages came from. All retrieval, citation, refusal, latency and scale numbers on this page are from extractive mode.
- **Generated mode** means an OpenAI chat model wrote the answer from the retrieved passages, and a second call graded it. **No generated-mode number exists yet.** The OpenAI key supplied for this work was valid but its account had no credit: every chat and embedding request returned "You have no credits remaining". The generated-answer chain and its evaluation are built and unit tested against mocked models, and both implementations were run against the live API as far as that error. Nothing was spent.

Common settings for every run unless a table says otherwise:

- Embedding model: `BAAI/bge-small-en-v1.5` on CPU (384 dimensions)
- Reranker: `Xenova/ms-marco-MiniLM-L-6-v2` cross-encoder on CPU, applied to the 10 nearest chunks, best 5 kept
- Up to 3 passages cited in extractive mode
- Similarity threshold 0.62, strict threshold 0.75 for questions with a word found nowhere in the corpus, rerank threshold -1.5
- Machine: 4 ARM cores, 8 GB of memory, no GPU

## Metrics

- **Retrieval hit rate at k:** an accepted page of the expected document is among the top k chunks.
- **Citation correctness:** the system answered, and at least one cited passage is on an accepted page of the expected document.
- **False refusals:** answerable questions the system declined to answer.
- **Refusals out of corpus:** unanswerable questions the system declined to answer. Higher is better.
- **Answer correctness** (generated mode): a grader model compares the answer with a short reference answer written by hand: correct, partial or incorrect.
- **Faithfulness** (generated mode): a grader model checks whether every claim in the answer is supported by the passages the answer cites.

## Question sets and ground truth

- `eval/questions.json`: 26 answerable questions and 8 off-topic ones. All tuning was done on this set.
- `eval/questions-heldout.json`: 6 answerable and 6 on-topic unanswerable questions. Written in round 1 as a held-out set. In round 2 it was used to choose the rerank threshold, so it is no longer held out.
- `eval/questions-heldout2.json`: 10 answerable, 10 on-topic unanswerable and 2 off-topic questions. Written after every setting was fixed, and run once per configuration.

The answerable questions are all answered by the 12 core documents. The expected pages were found by reading the PDFs before any retrieval run.

**Independent check of the ground truth.** A second reader, given only the questions and the PDFs and not the expected pages, located the answer pages for 10 of the 26 main questions (including the four that the system got wrong in round 1). It agreed with the recorded pages on all 10 and found two more valid pages that had been missed: the glossary page of the CSF document for in-13 and the executive summary of SP 800-50 for in-20. Both were added. Neither changed a score. The second reader was another instance of the same assistant that built the system, working without access to the expected answers, not a person.

**A limit that grows with the corpus.** At 100 PDFs, other documents sometimes state the same fact as the expected one. The scoring only accepts the expected document, so a correct citation to a different document counts as a miss. We read the six main-set misses at 100 PDFs. One is this case: the tabletop exercise question (in-06) is answered from SP 800-84, the NIST guide on exercises, whose passage does define the term. One is the opposite and more instructive: the question about the six functions of the Cybersecurity Framework (in-13) is answered from documents built on version 1.1 of the framework, which has five functions. A corpus that holds an old and a new version of the same document will do this unless the old one is removed or marked. Three cite a related page that does not state the answer, and one is a false refusal.

## Results at 12 and at 100 PDFs, both implementations

Answer mode: extractive. Questions: `eval/questions.json`.

| Metric | Plain, 12 PDFs | LangChain, 12 PDFs | Plain, 100 PDFs | LangChain, 100 PDFs |
| --- | --- | --- | --- | --- |
| Expected page is the top result | 20/26 (77%) | 20/26 (77%) | 17/26 (65%) | 17/26 (65%) |
| Expected page in top 3 | 21/26 (81%) | 21/26 (81%) | 20/26 (77%) | 20/26 (77%) |
| Expected page in top 5 | 23/26 (88%) | 23/26 (88%) | 20/26 (77%) | 20/26 (77%) |
| Answered with a citation to an accepted page | 21/26 (81%) | 21/26 (81%) | 20/26 (77%) | 20/26 (77%) |
| False refusals (answerable questions) | 0/26 (0%) | 0/26 (0%) | 1/26 (4%) | 1/26 (4%) |
| Refusals (unanswerable questions, higher is better) | 8/8 (100%) | 8/8 (100%) | 7/8 (88%) | 7/8 (88%) |

- **The two implementations score the same**, question for question, at both sizes. They store the same chunks and vectors and apply the same thresholds, so this is the expected result. LangChain changes how the steps are wired, not what they return.
- **Going from 12 to 100 PDFs cost about one question in eight.** The expected page is the top result for 20 of 26 questions at 12 PDFs and 17 of 26 at 100. Correct citations go from 21 to 20. One answerable question is refused at 100 PDFs (the cross-encoder scored its passages low), and one off-topic question is answered: "WhatsApp" now occurs somewhere in the larger corpus, so the unknown-word check no longer fires for it.
- **Why it drops.** The 88 added documents are on the same subject. Several restate or summarise what the core documents say, so they outrank the expected page. See the review of misses above.

## Scale: ingest time, size and latency

Answer mode: extractive. Latency is measured in process over the 34 main questions, three passes each (one pass for the reranker rows).

| | Plain, 12 PDFs | LangChain, 12 PDFs | Plain, 100 PDFs | LangChain, 100 PDFs |
| --- | --- | --- | --- | --- |
| Documents | 12 | 12 | 100 | 100 |
| Pages | 805 | 805 | 6,252 | 6,252 |
| Chunks | 2,448 | 2,448 | 18,205 | 18,205 |
| Stored size of the collection (text, metadata, vectors) | 6 MB | 6 MB | 42 MB | 42 MB |
| Ingest from nothing, embedding on CPU | 529 s (measured in round 1) | not measured separately | 4,349 s, about 72 minutes | not measured separately |
| Re-ingest with embeddings cached (parse PDFs, write rows) | 48 s | 80 s | 284 s | 423 s |
| Vector search, exact, p50 / p95 ms | 15 / 20 | 20 / 32 | 103 / 118 | 108 / 119 |
| Vector search, HNSW index, p50 / p95 ms | 3 / 5 | 21 / 32 | 2 / 4 | 6 / 19 |
| HNSW top-5 results shared with exact search | 94% | 100% | 97% | 97% |
| HNSW index build, seconds | 3.6 (one index over all collections) | 0.6 | 3.6 (one index over all collections) | 2.9 |
| Question embedding, p50 / p95 ms | 13 / 34 | 19 / 52 | 14 / 40 | 16 / 45 |
| Whole answer path without reranker, word lookup unindexed, p50 / p95 ms | 141 / 223 | 66 / 133 | 146 / 453 | 162 / 421 |
| Whole answer path without reranker, exact search, p50 / p95 ms | 112 / 191 | 61 / 98 | 134 / 290 | 144 / 182 |
| Whole answer path without reranker, HNSW, p50 / p95 ms | 98 / 176 | 61 / 96 | 34 / 190 | 43 / 98 |
| Rerank step alone, p50 / p95 ms | 658 / 893 | 743 / 1202 | 761 / 1997 | 667 / 1106 |
| Whole answer path with reranker (the default), p50 / p95 ms | 774 / 1016 | 817 / 1280 | 941 / 2135 | 835 / 1299 |

How to read the timings:

- **Embedding dominates ingestion.** Embedding 18,205 chunks on 4 CPU cores took about 72 minutes, at 4.3 chunks per second when nothing else was running. The figure is assembled from two runs: the first stopped after 93 documents on a NUL byte inside one PDF (now stripped in `pdf.py`), and other jobs shared the CPU during its first 14 documents. An embedding API or a GPU would change this number more than anything else here. The 12-PDF figure of 529 seconds is from round 1. Both implementations call the same embedding code, so the cold run was not repeated for LangChain.
- **Re-ingest with cached embeddings** shows what the rest of ingestion costs: parsing the PDFs and writing rows. LangChain's vector store took about one and a half times as long to write the same rows (423 against 284 seconds for 100 PDFs, one run each).
- **Exact vector search grows with the corpus**, from about 15 ms to about 105 ms. An HNSW index brings it to 2 to 6 ms. At 100 PDFs the index returned 97% of the same top-5 passages as exact search.
- **The index is not the default, and it was not the real latency problem.** Two other things were:
  - The unknown-word check looked up each question word with a pattern match over every chunk. For questions with rare words that put the 95th percentile of the whole answer path at 420 to 450 ms at 100 PDFs. A trigram index on the chunk text brought it to 182 to 290 ms. That index is now created at ingestion.
  - The reranker costs about 0.7 seconds per question on this CPU, and more in the tail. With it, a whole answer takes about 0.8 to 0.9 seconds at the median and 1.0 to 2.1 seconds at the 95th percentile, at either corpus size. This is the price of the accuracy shown in the next section.
- **Scores with the HNSW index at 100 PDFs** (`eval/results/full-hnsw.md`): unchanged in the plain implementation. In the LangChain implementation one more question lost its correct citation (19 of 26 against 20) and one more was falsely refused (2 against 1). Approximate search returns slightly different candidates, and the two implementations lay out their indexes differently: plain Python keeps one table with one index and asks pgvector to keep scanning until enough rows of the collection are found, LangChain keeps one table and one index per collection.
- **Storage** is about 2.3 KB per chunk including the 384-number vector: 42 MB for 100 PDFs before indexes.
- **Latency is in-process**, on the machine described above, with no concurrent load. It does not include HTTP or a language model call.

## What the reranker changed

Answer mode: extractive. The same collections and questions, with the reranker switched off (`--no-rerank`) and on.

Reranker off:

| Metric | Plain, 12 PDFs | LangChain, 12 PDFs | Plain, 100 PDFs | LangChain, 100 PDFs |
| --- | --- | --- | --- | --- |
| Expected page is the top result | 16/26 (62%) | 16/26 (62%) | 13/26 (50%) | 13/26 (50%) |
| Expected page in top 3 | 22/26 (85%) | 22/26 (85%) | 18/26 (69%) | 18/26 (69%) |
| Expected page in top 5 | 22/26 (85%) | 22/26 (85%) | 20/26 (77%) | 20/26 (77%) |
| Answered with a citation to an accepted page | 22/26 (85%) | 22/26 (85%) | 18/26 (69%) | 18/26 (69%) |
| False refusals (answerable questions) | 0/26 (0%) | 0/26 (0%) | 0/26 (0%) | 0/26 (0%) |
| Refusals (unanswerable questions, higher is better) | 8/8 (100%) | 8/8 (100%) | 4/8 (50%) | 4/8 (50%) |

Reranker on (the default, same as the main table):

| Metric | Plain, 12 PDFs | LangChain, 12 PDFs | Plain, 100 PDFs | LangChain, 100 PDFs |
| --- | --- | --- | --- | --- |
| Expected page is the top result | 20/26 (77%) | 20/26 (77%) | 17/26 (65%) | 17/26 (65%) |
| Expected page in top 3 | 21/26 (81%) | 21/26 (81%) | 20/26 (77%) | 20/26 (77%) |
| Expected page in top 5 | 23/26 (88%) | 23/26 (88%) | 20/26 (77%) | 20/26 (77%) |
| Answered with a citation to an accepted page | 21/26 (81%) | 21/26 (81%) | 20/26 (77%) | 20/26 (77%) |
| False refusals (answerable questions) | 0/26 (0%) | 0/26 (0%) | 1/26 (4%) | 1/26 (4%) |
| Refusals (unanswerable questions, higher is better) | 8/8 (100%) | 8/8 (100%) | 7/8 (88%) | 7/8 (88%) |

- **The reranker puts the right page first more often.** Top-result accuracy rises from 62% to 77% at 12 PDFs and from 50% to 65% at 100.
- **It does not raise citation correctness at 12 PDFs** (22 of 26 without it, 21 with it): the expected page is cited when it is among the top 3, and the reranker moved one expected page out of the top 3 while moving four into first place. At 100 PDFs it helps on both counts (18 to 20).
- **It restores most of the refusals lost at scale.** Without it, only 4 of 8 off-topic questions are refused at 100 PDFs, because the larger corpus contains more of their words and offers closer-looking passages. With it, 7 of 8.
- **It introduced the one false refusal at 100 PDFs.**

## Held-out questions

Answer mode: extractive.

`eval/questions-heldout2.json`, written after all settings were fixed:

| Metric | Plain, 12 PDFs | LangChain, 12 PDFs | Plain, 100 PDFs | LangChain, 100 PDFs |
| --- | --- | --- | --- | --- |
| Expected page is the top result | 9/10 (90%) | 9/10 (90%) | 8/10 (80%) | 8/10 (80%) |
| Expected page in top 3 | 9/10 (90%) | 9/10 (90%) | 8/10 (80%) | 8/10 (80%) |
| Expected page in top 5 | 9/10 (90%) | 9/10 (90%) | 8/10 (80%) | 8/10 (80%) |
| Answered with a citation to an accepted page | 9/10 (90%) | 9/10 (90%) | 8/10 (80%) | 8/10 (80%) |
| False refusals (answerable questions) | 0/10 (0%) | 0/10 (0%) | 0/10 (0%) | 0/10 (0%) |
| Refusals (unanswerable questions, higher is better) | 7/12 (58%) | 7/12 (58%) | 6/12 (50%) | 6/12 (50%) |

`eval/questions-heldout.json`, the round 1 held-out set, later used to choose the rerank threshold:

| Metric | Plain, 12 PDFs | LangChain, 12 PDFs | Plain, 100 PDFs | LangChain, 100 PDFs |
| --- | --- | --- | --- | --- |
| Expected page is the top result | 6/6 (100%) | 6/6 (100%) | 6/6 (100%) | 6/6 (100%) |
| Expected page in top 3 | 6/6 (100%) | 6/6 (100%) | 6/6 (100%) | 6/6 (100%) |
| Expected page in top 5 | 6/6 (100%) | 6/6 (100%) | 6/6 (100%) | 6/6 (100%) |
| Answered with a citation to an accepted page | 6/6 (100%) | 6/6 (100%) | 6/6 (100%) | 6/6 (100%) |
| False refusals (answerable questions) | 0/6 (0%) | 0/6 (0%) | 0/6 (0%) | 0/6 (0%) |
| Refusals (unanswerable questions, higher is better) | 3/6 (50%) | 3/6 (50%) | 3/6 (50%) | 3/6 (50%) |

Answerable questions in the newer set: 9 of 10 cited correctly at 12 PDFs and 8 of 10 at 100, with no false refusals. One of the two misses at 100 PDFs (the number of control baselines) cites SP 800-53B, the document that defines the baselines, which is probably a correct answer from a different document. We did not grade it.

The unanswerable questions are the point of this set. Ten of its twelve are on the corpus topic and use its vocabulary ("Which mobile device management product should we buy?"). Counting only those ten:

| On-topic unanswerable questions refused | 12 PDFs | 100 PDFs |
| --- | --- | --- |
| Without the reranker | 3/10 | 2/10 |
| With the reranker (the default) | 5/10 | 4/10 |

Both off-topic questions in the set were refused in every configuration.

So the weak spot found in round 1 (1 of 6 refused) is improved and not fixed. In extractive mode about half of the on-topic questions that the documents cannot answer still get passages back. The reply then quotes passages that are visibly about the subject and visibly do not answer the question, with their pages, so a reader is not misled about a fact, but it is not the refusal the brief asks for. Retrieval scores cannot tell "about this" from "answers this" reliably. A language model reading the passages can, and that is the check that has not been measured yet (see Generated answers).

On the older set the refusals went from 1 of 6 in round 1 to 3 of 6. The rerank threshold was chosen on that set, so this number is optimistic and the newer set is the one to quote.

## Generated answers

**No generated-mode number exists yet.** The OpenAI key supplied for this work was valid but its account had no credit: every chat and embedding request returned "You have no credits remaining". The generated-answer chain and its evaluation are built and unit tested against mocked models, and both implementations were run against the live API as far as that error. Nothing was spent.

What is ready to run, in each repository, once the key has credit:

```sh
OPENAI_API_KEY=... make eval-answers PY=.venv/bin/python
```

That one command runs six evaluations: the main set and both held-out sets, each at 12 and at 100 PDFs. For every question it:

- answers with `gpt-4o-mini` from up to 5 retrieved passages, under a prompt that requires numbered citations and an exact refusal sentence when the passages do not state the answer
- grades correctness against the hand-written reference answer (correct, partial, incorrect)
- grades faithfulness of the answer to the passages it cites (supported, partial, unsupported)
- records citation correctness, false refusals, and refusals of unanswerable questions, split into those refused by the retrieval checks and those refused by the model

It writes `eval/results/answers-*.json` and `.md`, each with the token counts reported by the API and the estimated spend.

- **Expected cost:** about 10 cents per repository, estimated from passage sizes (roughly 3,500 input and 200 output tokens per question, 136 question runs). The prices in the code are 0.15 and 0.60 US dollars per million input and output tokens, which were `gpt-4o-mini` list prices when this was written and were not rechecked.
- **Hard ceiling:** each of the six runs stops at `MAX_SPEND_USD`, 0.40 by default, so both repositories together cannot pass 4.80 dollars.
- **The key** is read from the environment variable only. It is not written to any file, log or image by this code. With the `PY=.venv/bin/python` form above it never enters a container.
- **Caveat on the grader:** the same model family writes and grades the answers. That tends to flatter the scores. A sample should be read by a person before the numbers are quoted.

The weak spot this is expected to help with is the on-topic unanswerable question. The prompt tells the model to refuse when the passages are on the subject but do not state the answer. Whether it does is exactly what the run will show.

## Baselines: what the chunker is worth

Answer mode: extractive, reranker off, 12 PDFs, threshold 0.50 and no other refusal check (the untuned starting point).

| Metric | Plain baseline (fixed windows) | LangChain baseline (stock loader and splitter) |
| --- | --- | --- |
| Expected page is the top result | 13/26 (50%) | 17/26 (65%) |
| Expected page in top 3 | 21/26 (81%) | 19/26 (73%) |
| Expected page in top 5 | 22/26 (85%) | 22/26 (85%) |
| Answered with a citation to an accepted page | 21/26 (81%) | 19/26 (73%) |
| False refusals (answerable questions) | 0/26 (0%) | 0/26 (0%) |
| Refusals (unanswerable questions, higher is better) | 1/8 (12%) | 1/8 (12%) |

- **Plain baseline:** fixed windows of 1,000 characters with 150 overlap inside each page.
- **LangChain baseline:** `PyPDFLoader` and `RecursiveCharacterTextSplitter` with 1,000 characters and 200 overlap, the usual starting point in LangChain tutorials.
- **Heading chunks:** this project's chunker, in the same no-reranker setting, for comparison (from the "reranker off" table above, 12 PDFs): top result 16/26, top 3 22/26, correct citation 22/26.

LangChain's stock splitter put the expected page first slightly more often than our chunker (17 against 16) and clearly more often than our fixed-window baseline (13). It did worse where it counts for this brief: a correct citation in 19 of 26 answers against 22 of 26. The LangChain implementation therefore keeps our heading and page aware chunker as its default loader and keeps the stock loader as the baseline. The gap is three questions on a set of 26, so it is an indication and not a proof.

## Round 1 history: tuning at 12 PDFs

These numbers are from the first version of the plain-Python implementation (commit `a5c0c6a` of rag-pdf-demo), before the reranker existed. Answer mode: extractive.

| Metric | Baseline | Step 1: heading chunks | Step 2: hybrid search (rejected) | Step 3: threshold 0.62 | Step 4: unknown-word check |
| --- | --- | --- | --- | --- | --- |
| Expected page is the top result | 13/26 (50%) | 16/26 (62%) | 14/26 (54%) | 16/26 (62%) | 16/26 (62%) |
| Expected page in top 3 | 21/26 (81%) | 22/26 (85%) | 19/26 (73%) | 22/26 (85%) | 22/26 (85%) |
| Expected page in top 5 | 22/26 (85%) | 22/26 (85%) | 20/26 (77%) | 22/26 (85%) | 22/26 (85%) |
| Answered with a citation to an accepted page | 21/26 (81%) | 22/26 (85%) | 19/26 (73%) | 22/26 (85%) | 22/26 (85%) |
| False refusals (in corpus) | 0/26 (0%) | 0/26 (0%) | 0/26 (0%) | 0/26 (0%) | 0/26 (0%) |
| Refusals (out of corpus) | 1/8 (12%) | 1/8 (12%) | 1/8 (12%) | 4/8 (50%) | 8/8 (100%) |

- **Baseline.** Fixed windows of 1,000 characters with 150 overlap, cut inside each page, headers and footers left in. Refusal threshold 0.50, a guess made before any run.
- **Step 1, heading and page aware chunks.** Chunks start at section headings, never cross a page, running headers and footers are removed, and the heading path is embedded together with the text.
- **Step 2, hybrid search. Tried and rejected.** Postgres full-text search was merged with vector search by reciprocal rank fusion. It pushed correct pages down, because common words in the question matched many unrelated chunks. The code was removed after this round and is in the history at commit `a5c0c6a`.
- **Step 3, refusal threshold raised from 0.50 to 0.62,** the highest value in the sweep with no false refusals.
- **Step 4, unknown-word check.** If a content word of the question appears in no chunk at all (for example "GDPR"), the question must clear a stricter threshold of 0.75.

The round 1 held-out check then showed the weak spot that round 2 worked on: only 1 of 6 on-topic unanswerable questions was refused.

## What the numbers do not show

- **Nothing here measures a generated answer.** Every number is from extractive mode.
- **The question sets are small.** One question is about 4 percentage points on the main set and 10 on the newer held-out set. Differences of one or two questions are within what a different set of questions could reverse.
- **We wrote the questions and the reference answers ourselves.** A client's own questions are the real test.
- **Scoring accepts only the expected document.** At 100 PDFs that undercounts correct answers found elsewhere, as the review of misses shows.
- **Thresholds were tuned at 12 PDFs and not retuned at 100.** The 100-PDF columns show what happens when the corpus grows under settings chosen for a smaller one.
- **Latency was measured on one small machine with no concurrent users.**
- **The cross-encoder was trained on MS MARCO**, a dataset released for non-commercial research. The model itself carries an Apache 2.0 licence. A commercial deployment should check that position or swap the model.

## Reproduce

```sh
docker compose up -d --build
make ingest-full ingest-baseline
make eval eval-full eval-baseline eval-norerank eval-heldout bench
OPENAI_API_KEY=... make eval-answers PY=.venv/bin/python
```

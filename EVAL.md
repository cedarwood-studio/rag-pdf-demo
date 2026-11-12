# Evaluation

The numbers on this page come from the scripts in this repository and in its twin, [rag-pdf-demo-langchain](https://github.com/cedarwood-studio/rag-pdf-demo-langchain). The raw output of every run, question by question, is in `eval/results/` of each repository. This page is the same in both.

Three groups of numbers were not written by a script at the current commit, and each is marked where it appears: the round 1 history (its result files are in commit `a5c0c6a` of rag-pdf-demo), the cold ingest time for 100 PDFs (assembled from two runs and recorded by hand) and a probe of two other rerankers (output not saved).

## Read this first: which answer mode each number came from

- **Extractive mode** means no language model wrote anything. The answer is the best passages quoted word for word, and the citations are the pages those passages came from. All retrieval, latency and scale numbers on this page are from extractive mode.
- **Generated mode** means a chat model wrote the answer from the retrieved passages, and a second call to the same model graded it. Those numbers are in the section "Generated answers" and nowhere else. The model was `openai/gpt-4o-mini`, called through OpenRouter's OpenAI-compatible endpoint.

Every table says which mode it is.

Common settings for every run unless a table says otherwise:

- Embedding model: `BAAI/bge-small-en-v1.5` on CPU (384 dimensions)
- 5 nearest chunks retrieved by exact search. Up to 3 passages cited in extractive mode, up to 5 handed to the model in generated mode
- Similarity threshold 0.62, strict threshold 0.75 for questions with a word found nowhere in the corpus
- Reranker off. Where a table says "reranker on": `Xenova/ms-marco-MiniLM-L-6-v2` cross-encoder on CPU, applied to the 10 nearest chunks, best 5 kept, rerank threshold -1.5
- Machine: 4 ARM cores, 8 GB of memory, no GPU

## Metrics

- **Retrieval hit rate at k:** an accepted page of the expected document is among the top k chunks.
- **Citation correctness:** the system answered, and at least one cited passage is on an accepted page of the expected document.
- **False refusals:** answerable questions the system declined to answer.
- **Refusals of unanswerable questions:** higher is better. In generated mode they are split into refusals by the retrieval checks (before any model call) and refusals by the model.
- **Answer correctness** (generated mode): the grader compares the answer with the short reference answer stored with each question and returns correct, partial or incorrect.
- **Faithfulness** (generated mode): the grader checks whether every claim in the answer is supported by the passages the answer cites.

## Question sets and ground truth

- `eval/questions.json`: 26 answerable questions and 8 off-topic ones. All tuning was done on this set.
- `eval/questions-heldout.json`: 6 answerable and 6 on-topic unanswerable questions. Written in round 1 as a held-out set. In round 2 it was used to choose the rerank threshold, so it is held out only for the runs without the reranker.
- `eval/questions-heldout2.json`: 10 answerable, 10 on-topic unanswerable and 2 off-topic questions. Written after every setting was fixed. No setting was changed after its first run.

The answerable questions are all answered by the 12 core documents. The expected pages were found by reading the PDFs before any retrieval run.

**Independent check of the ground truth.** A second reader, given only the questions and the PDFs and not the expected pages, located the answer pages for 10 of the 26 main questions (including the four that the system got wrong in round 1). It agreed with the recorded pages on all 10 and found two more valid pages that had been missed: the glossary page of the CSF document for in-13 and the executive summary of SP 800-50 for in-20. Both were added. Neither changed a score. The second reader was another instance of the AI assistant that built the system, working without access to the expected answers. No person repeated the check.

**A limit that grows with the corpus.** At 100 PDFs, other documents sometimes state the same fact as the expected one. The scoring only accepts the expected document, so a correct citation to a different document counts as a miss. We read the eight main-set questions that lack a correct citation at 100 PDFs. One is this case: the tabletop exercise question (in-06) is answered from SP 800-84, the NIST guide on exercises, whose passage does define the term. One is the opposite and more instructive: the question about the six functions of the Cybersecurity Framework (in-13) pulls in documents built on version 1.1 of the framework, which has five functions. A corpus that holds an old and a new version of the same document will do this unless the old one is removed or marked. For the other six we did not check whether the cited page of a different document also answers the question; the four that are also missed at 12 PDFs cite a related page that does not state the answer.

## Retrieval, citations and refusals at 12 and at 100 PDFs

These runs are in extractive mode with the reranker off (the default), on the questions of `eval/questions.json`.

| Metric | Plain, 12 PDFs | LangChain, 12 PDFs | Plain, 100 PDFs | LangChain, 100 PDFs |
| --- | --- | --- | --- | --- |
| Expected page is the top result | 16/26 (62%) | 16/26 (62%) | 13/26 (50%) | 13/26 (50%) |
| Expected page in top 3 | 22/26 (85%) | 22/26 (85%) | 18/26 (69%) | 18/26 (69%) |
| Expected page in top 5 | 22/26 (85%) | 22/26 (85%) | 20/26 (77%) | 20/26 (77%) |
| Answered with a citation to an accepted page | 22/26 (85%) | 22/26 (85%) | 18/26 (69%) | 18/26 (69%) |
| False refusals (answerable questions) | 0/26 (0%) | 0/26 (0%) | 0/26 (0%) | 0/26 (0%) |
| Refusals (unanswerable questions, higher is better) | 8/8 (100%) | 8/8 (100%) | 4/8 (50%) | 4/8 (50%) |

- **The two implementations score the same**, question for question, at both sizes. They store the same chunks and vectors and apply the same thresholds, so this is the expected result. LangChain changes how the steps are wired. What they return is the same.
- **Going from 12 to 100 PDFs cost four questions out of 26.** Correct citations go from 22 to 18, and the expected page is the top result for 13 questions where it was 16.
- **Off-topic refusals halve at 100 PDFs**, from 8 of 8 to 4 of 8. The larger corpus contains more of the questions' words ("GDPR", "WhatsApp"), so the unknown-word check fires less often, and it offers passages that look closer. In generated mode the model catches all of these (next section).
- **Why retrieval drops.** The 88 added documents are on the same subject. Several restate or summarize what the core documents say, so they outrank the expected page. See the review of misses above.

## Generated answers

These runs are in generated mode. `openai/gpt-4o-mini`, called through OpenRouter, wrote the answers and graded them. The reranker is off (the default).

Main question set, `eval/questions.json` (26 answerable, 8 off-topic):

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

Held-out set written after all settings were fixed, `eval/questions-heldout2.json` (10 answerable, 10 on-topic unanswerable, 2 off-topic):

| Metric | Plain, 12 PDFs | LangChain, 12 PDFs | Plain, 100 PDFs | LangChain, 100 PDFs |
| --- | --- | --- | --- | --- |
| Answer correct | 8/10 (80%) | 8/10 (80%) | 7/10 (70%) | 7/10 (70%) |
| Answer partly correct | 2/10 (20%) | 2/10 (20%) | 1/10 (10%) | 1/10 (10%) |
| Answer incorrect | 0/10 (0%) | 0/10 (0%) | 1/10 (10%) | 1/10 (10%) |
| False refusals (answerable questions) | 0/10 (0%) | 0/10 (0%) | 1/10 (10%) | 1/10 (10%) |
| Answered with a citation to an accepted page | 9/10 (90%) | 9/10 (90%) | 7/10 (70%) | 7/10 (70%) |
| Faithful to its cited passages (of answers given) | 10/11 (91%) | 10/11 (91%) | 8/10 (80%) | 8/10 (80%) |
| Partly faithful (of answers given) | 1/11 (9%) | 1/11 (9%) | 2/10 (20%) | 2/10 (20%) |
| Unfaithful (of answers given) | 0/11 (0%) | 0/11 (0%) | 0/10 (0%) | 0/10 (0%) |
| Refusals (unanswerable questions, higher is better) | 11/12 (92%) | 11/12 (92%) | 11/12 (92%) | 11/12 (92%) |
| of which refused by the model itself | 6/12 (50%) | 6/12 (50%) | 7/12 (58%) | 7/12 (58%) |

Round 1 held-out set, `eval/questions-heldout.json` (6 answerable, 6 on-topic unanswerable):

| Metric | Plain, 12 PDFs | LangChain, 12 PDFs | Plain, 100 PDFs | LangChain, 100 PDFs |
| --- | --- | --- | --- | --- |
| Answer correct | 4/6 (67%) | 3/6 (50%) | 6/6 (100%) | 4/6 (67%) |
| Answer partly correct | 2/6 (33%) | 3/6 (50%) | 0/6 (0%) | 2/6 (33%) |
| Answer incorrect | 0/6 (0%) | 0/6 (0%) | 0/6 (0%) | 0/6 (0%) |
| False refusals (answerable questions) | 0/6 (0%) | 0/6 (0%) | 0/6 (0%) | 0/6 (0%) |
| Answered with a citation to an accepted page | 6/6 (100%) | 6/6 (100%) | 5/6 (83%) | 5/6 (83%) |
| Faithful to its cited passages (of answers given) | 6/6 (100%) | 6/6 (100%) | 6/6 (100%) | 6/6 (100%) |
| Partly faithful (of answers given) | 0/6 (0%) | 0/6 (0%) | 0/6 (0%) | 0/6 (0%) |
| Unfaithful (of answers given) | 0/6 (0%) | 0/6 (0%) | 0/6 (0%) | 0/6 (0%) |
| Refusals (unanswerable questions, higher is better) | 6/6 (100%) | 6/6 (100%) | 6/6 (100%) | 6/6 (100%) |
| of which refused by the model itself | 5/6 (83%) | 5/6 (83%) | 6/6 (100%) | 6/6 (100%) |

**On-topic questions the documents do not answer.** Extractive mode, the same questions and settings, is shown beside generated mode:

| On-topic unanswerable questions refused | Plain, 12 PDFs | LangChain, 12 PDFs | Plain, 100 PDFs | LangChain, 100 PDFs |
| --- | --- | --- | --- | --- |
| Newer set, extractive | 3/10 | 3/10 | 2/10 | 2/10 |
| Newer set, generated | 9/10 (3 by checks, 6 by the model) | 9/10 (3 by checks, 6 by the model) | 9/10 (2 by checks, 7 by the model) | 9/10 (2 by checks, 7 by the model) |
| Round 1 set, extractive | 1/6 | 1/6 | 0/6 | 0/6 |
| Round 1 set, generated | 6/6 (1 by checks, 5 by the model) | 6/6 (1 by checks, 5 by the model) | 6/6 (0 by checks, 6 by the model) | 6/6 (0 by checks, 6 by the model) |

What these runs show:

- **The model closes most of the refusal gap.** Told to refuse when the passages are on the subject but do not state the answer, it refused 9 of the 10 newer on-topic unanswerable questions where the retrieval checks alone refused 3 (2 at 100 PDFs), and all 6 of the round 1 set.
- **The one it answered was a mistake in our question set.** "On what date will the incident handling guide be withdrawn?" was written as unanswerable. The withdrawal notice on page 1 of SP 800-61 Rev. 2 gives the date, and the model answered with it and cited that page. The question is left in the set as written, so the tables count it against the system.
- **No answer was graded unsupported by its passages,** in any run. Between 74% and 100% of answers were graded fully supported, and the rest partly: typically a correct answer with one added detail that the cited passage does not contain.
- **Answers are right more often than not, and less often at 100 PDFs.** On the main set 18 of 26 were graded correct at 12 PDFs and 16 at 100, with 5 and 7 partly correct and none incorrect. On the newer set, 8 of 10 at 12 PDFs and 7 of 10 at 100, where one answer was graded incorrect in each implementation (the system should allow passwords of at least 64 characters; the answer gave the 8-character minimum instead).
- **Partial answers often trace to the documents, not the model.** For "Should we force users to change their passwords on a regular schedule?" one document in the corpus says yes and another says no. The model reported both, which the grader marked partly correct against a reference taken from one of them.

What got worse in generated mode:

- **False refusals appear.** On the main set the model declined 3 of 26 answerable questions at both sizes, where extractive mode declined none. In each case retrieval had not put the page with the answer among the passages, so the model was right that the passages did not state it. Extractive mode "answers" those questions by quoting the wrong passages. Even so, a user gets no answer to a question the documents do cover.
- **Citation correctness did not improve.** It is 21 of 26 and 20 of 26 on the main set, against 22 and 18 in extractive mode. The model can only cite what retrieval hands it.
- **Each answer needs a paid model call.** The time that call adds was not measured.

How far to trust these numbers:

- **The grader is the same model that wrote the answers.** That tends to flatter the scores. Nobody has read the graded answers by hand apart from the few rows quoted here.
- **The two implementations send the same prompt and passages, and still differ by a question or two** on the smaller sets (for example correct answers on the round 1 set). The model and the grader are not perfectly repeatable at temperature 0 through this endpoint. Differences of that size between columns are noise.
- **Cost.** All 1,070 model calls of both repositories, including the reranker variant below, used 680,081 input and 40,170 output tokens. At OpenRouter's listed price for `openai/gpt-4o-mini` when the runs were made (0.15 and 0.60 US dollars per million input and output tokens) that is an estimated $0.13. The figure is computed from the token counts the API returned, not read from an invoice.

With the optional reranker switched on, generated mode (`eval/results/answers-*-rerank.md`):

| Metric | Plain, 12 PDFs | LangChain, 12 PDFs | Plain, 100 PDFs | LangChain, 100 PDFs |
| --- | --- | --- | --- | --- |
| Answer correct | 20/26 (77%) | 20/26 (77%) | 18/26 (69%) | 17/26 (65%) |
| Answer partly correct | 4/26 (15%) | 4/26 (15%) | 5/26 (19%) | 6/26 (23%) |
| Answer incorrect | 1/26 (4%) | 1/26 (4%) | 1/26 (4%) | 1/26 (4%) |
| False refusals (answerable questions) | 1/26 (4%) | 1/26 (4%) | 2/26 (8%) | 2/26 (8%) |
| Answered with a citation to an accepted page | 22/26 (85%) | 22/26 (85%) | 20/26 (77%) | 20/26 (77%) |
| Refusals (unanswerable questions, higher is better) | 8/8 (100%) | 8/8 (100%) | 8/8 (100%) | 8/8 (100%) |
| of which refused by the model itself | 0/8 (0%) | 0/8 (0%) | 1/8 (12%) | 1/8 (12%) |

| On-topic unanswerable questions refused | Plain, 12 PDFs | LangChain, 12 PDFs | Plain, 100 PDFs | LangChain, 100 PDFs |
| --- | --- | --- | --- | --- |
| Newer set, generated, reranker on | 9/10 (5 by checks, 4 by the model) | 9/10 (5 by checks, 4 by the model) | 9/10 (4 by checks, 5 by the model) | 9/10 (4 by checks, 5 by the model) |

With the reranker on, more answers were graded correct on the main set: 20 of 26 at 12 PDFs, and 18 (plain) and 17 (LangChain) at 100, against 18 and 16 without it. False refusals fell from 3 to 1 at 12 PDFs and to 2 at 100. One answer per run was graded incorrect where none was before. On-topic unanswerable refusals stayed at 9 of 10, with more of them made by the retrieval checks and fewer left to the model. The gain is about two questions in 26, and it comes with the license caveat and about 0.7 seconds more per question.

## Held-out questions

These runs are in extractive mode with the reranker off (the default).

`eval/questions-heldout2.json`:

| Metric | Plain, 12 PDFs | LangChain, 12 PDFs | Plain, 100 PDFs | LangChain, 100 PDFs |
| --- | --- | --- | --- | --- |
| Expected page is the top result | 6/10 (60%) | 6/10 (60%) | 5/10 (50%) | 5/10 (50%) |
| Expected page in top 3 | 8/10 (80%) | 8/10 (80%) | 6/10 (60%) | 6/10 (60%) |
| Expected page in top 5 | 9/10 (90%) | 9/10 (90%) | 7/10 (70%) | 7/10 (70%) |
| Answered with a citation to an accepted page | 8/10 (80%) | 8/10 (80%) | 6/10 (60%) | 6/10 (60%) |
| False refusals (answerable questions) | 0/10 (0%) | 0/10 (0%) | 0/10 (0%) | 0/10 (0%) |
| Refusals (unanswerable questions, higher is better) | 5/12 (42%) | 5/12 (42%) | 4/12 (33%) | 4/12 (33%) |

`eval/questions-heldout.json`:

| Metric | Plain, 12 PDFs | LangChain, 12 PDFs | Plain, 100 PDFs | LangChain, 100 PDFs |
| --- | --- | --- | --- | --- |
| Expected page is the top result | 5/6 (83%) | 5/6 (83%) | 4/6 (67%) | 4/6 (67%) |
| Expected page in top 3 | 6/6 (100%) | 6/6 (100%) | 6/6 (100%) | 6/6 (100%) |
| Expected page in top 5 | 6/6 (100%) | 6/6 (100%) | 6/6 (100%) | 6/6 (100%) |
| Answered with a citation to an accepted page | 6/6 (100%) | 6/6 (100%) | 6/6 (100%) | 6/6 (100%) |
| False refusals (answerable questions) | 0/6 (0%) | 0/6 (0%) | 0/6 (0%) | 0/6 (0%) |
| Refusals (unanswerable questions, higher is better) | 1/6 (17%) | 1/6 (17%) | 0/6 (0%) | 0/6 (0%) |

Answerable questions in the newer set: 8 of 10 cited correctly at 12 PDFs and 6 of 10 at 100, with no false refusals.

The unanswerable questions are the point of these sets. Ten of the twelve in the newer set, and all six in the round 1 set, are on the corpus topic and use its vocabulary ("Which mobile device management product should we buy?"). In extractive mode the retrieval checks refuse few of them: 3 of 10 and 1 of 6 at 12 PDFs, 2 of 10 and 0 of 6 at 100. Both off-topic questions in the newer set are refused at both sizes.

So in extractive mode most on-topic questions that the documents cannot answer still get passages back. The reply quotes passages that are visibly about the subject and visibly do not answer the question, with their pages, so a reader is not misled about a fact, but it is not the refusal the brief asks for. Retrieval scores cannot tell "about this" from "answers this". A language model reading the passages can, and the generated-mode runs above measure that: 9 of 10 and 6 of 6.

## Scale: ingest time, size and latency

These runs are in extractive mode. Latency is measured in process over the 34 main questions, three passes each (one pass for the reranker rows).

| | Plain, 12 PDFs | LangChain, 12 PDFs | Plain, 100 PDFs | LangChain, 100 PDFs |
| --- | --- | --- | --- | --- |
| Documents | 12 | 12 | 100 | 100 |
| Pages | 805 | 805 | 6,252 | 6,252 |
| Chunks | 2,448 | 2,448 | 18,205 | 18,205 |
| Stored size of the collection (text, metadata, vectors) | 6 MB | 6 MB | 42 MB | 42 MB |
| Ingest from nothing, embedding on CPU | 535 s | 586 s | 4,349 s, about 72 minutes (assembled from two runs) | not measured |
| Re-ingest with embeddings cached (parse PDFs, write rows) | 31 s | 52 s | 271 s | 429 s |
| Vector search, exact, p50 / p95 ms | 15 / 22 | 21 / 33 | 103 / 119 | 108 / 120 |
| Vector search, HNSW index, p50 / p95 ms | 3 / 5 | 22 / 32 | 2 / 5 | 6 / 14 |
| HNSW top-5 results shared with exact search | 94% | 100% | 98% | 96% |
| HNSW index build, seconds | 3.6 (one index over all collections) | 0.5 | 3.9 (one index over all collections) | 2.7 |
| Question embedding, p50 / p95 ms | 13 / 40 | 19 / 48 | 15 / 38 | 18 / 45 |
| Whole answer path, word lookup without trigram index, p50 / p95 ms | 149 / 213 | 75 / 108 | 152 / 501 | 160 / 464 |
| Whole answer path (the default: exact search, no reranker), p50 / p95 ms | 110 / 200 | 60 / 101 | 139 / 294 | 147 / 192 |
| Whole answer path with HNSW index, p50 / p95 ms | 103 / 182 | 67 / 113 | 36 / 190 | 48 / 98 |
| Optional rerank step alone, p50 / p95 ms | 712 / 1058 | 762 / 1080 | 714 / 1582 | 681 / 936 |
| Whole answer path with the optional reranker, p50 / p95 ms | 840 / 1186 | 816 / 1170 | 918 / 1842 | 846 / 1085 |

How to read the timings:

- **Embedding dominates ingestion.** Embedding 18,205 chunks on 4 CPU cores took about 72 minutes, at 4.3 chunks per second when nothing else was running. The figure is assembled from two runs: the first stopped after 93 documents on a NUL byte inside one PDF (now stripped in `pdf.py`), and other jobs shared the CPU during its first 14 documents. An embedding API or a GPU would change this number more than anything else here. That run has no result file of its own: its figures are recorded by hand in the `cold_run` entry of `eval/results/ingest-full.json` in rag-pdf-demo. The 100-PDF cold run was not repeated for LangChain, which calls the same embedding code. The 12-PDF figures are one first start of each container from an empty database and an empty cache (`eval/results/ingest-core.json`), of which 503 and 532 seconds were embedding.
- **Re-ingest with cached embeddings** shows what the rest of ingestion costs: parsing the PDFs and writing rows. LangChain's vector store took about one and a half times as long to write the same rows (429 against 271 seconds for 100 PDFs, one run each, in `eval/results/ingest-full-cached.json`).
- **Exact vector search grows with the corpus**, from about 15 ms to about 105 ms. At 100 PDFs an HNSW index brings it to 2 to 6 ms and returns 96 to 98% of the same top-5 passages as exact search. At 12 PDFs LangChain's table is small enough that Postgres scans it without the index either way.
- **Scores with the HNSW index at 100 PDFs** (`eval/results/full-hnsw.md`): with the first build of each index, retrieval and citation scores were the same as with exact search in both implementations, and the LangChain run refused one more off-topic question (5 of 8 against 4), because approximate search returned a slightly different nearest passage for it. An HNSW index is approximate and two builds of it are not the same. A second build (`eval/results/full-hnsw-rebuild.md`) left the LangChain scores where they were and gave the plain-Python version one more correct citation (19 of 26) and one more off-topic refusal (5 of 8). A difference of one question between these runs is variation from build to build. The two implementations lay out their indexes differently: plain Python keeps one table with one index over all collections and asks pgvector to keep scanning until enough rows of the collection are found, LangChain keeps one table and one index per collection.
- **The index is not the default.** At this size exact search is fast enough, and it is exact. The index is one setting (`USE_INDEX=1`) and becomes worth its small loss somewhere past a hundred thousand chunks.
- **The slow part of the default path was not vector search.** The unknown-word check looked up each question word with a pattern match over every chunk. For questions with rare words that put the 95th percentile of the whole answer path at 460 to 500 ms at 100 PDFs. A trigram index on the chunk text brought it to under 300 ms. That index is now created at ingestion.
- **The optional reranker costs about 0.7 seconds per question** on this CPU, and more in the tail.
- **Storage** is about 2.3 KB per chunk including the 384-number vector: 42 MB for 100 PDFs before indexes.
- **Latency is in-process**, on the machine described above, with no concurrent load. It does not include HTTP or a language model call.

## The optional reranker

These runs are in extractive mode, on the same collections and questions as the main table, with the reranker switched on (`RERANK=1`).

| Metric | Plain, 12 PDFs | LangChain, 12 PDFs | Plain, 100 PDFs | LangChain, 100 PDFs |
| --- | --- | --- | --- | --- |
| Expected page is the top result | 20/26 (77%) | 20/26 (77%) | 17/26 (65%) | 17/26 (65%) |
| Expected page in top 3 | 21/26 (81%) | 21/26 (81%) | 20/26 (77%) | 20/26 (77%) |
| Expected page in top 5 | 23/26 (88%) | 23/26 (88%) | 20/26 (77%) | 20/26 (77%) |
| Answered with a citation to an accepted page | 21/26 (81%) | 21/26 (81%) | 20/26 (77%) | 20/26 (77%) |
| False refusals (answerable questions) | 0/26 (0%) | 0/26 (0%) | 1/26 (4%) | 1/26 (4%) |
| Refusals (unanswerable questions, higher is better) | 8/8 (100%) | 8/8 (100%) | 7/8 (88%) | 7/8 (88%) |

Compared with the main table (reranker off):

- **The right page comes first more often.** Top-result accuracy rises from 62% to 77% at 12 PDFs and from 50% to 65% at 100.
- **Citation correctness is mixed.** At 12 PDFs it is one question lower (21 against 22): the reranker moved four expected pages into first place and one out of the top 3. At 100 PDFs it is two higher (20 against 18).
- **It restores most of the off-topic refusals lost at scale**: 7 of 8 at 100 PDFs against 4 of 8.
- **It introduces one false refusal at 100 PDFs.**
- **On-topic unanswerable questions (newer held-out set, extractive):** 5 of 10 refused at 12 PDFs and 4 of 10 at 100, against 3 and 2 without it. The rerank threshold was chosen on the round 1 held-out set, where it lifts refusals from 1 of 6 to 3 of 6 (0 to 3 at 100 PDFs).
- **It costs about 0.7 seconds per question** (see the scale table).

Why it is off by default: the license position of its model is not clean enough for a public repository (see Licenses in the README). Two cross-encoders with an Apache 2.0 license on their own model cards were tried as replacements on the 32 answerable questions of the main and round 1 sets at 12 PDFs, as a quick probe and not a full evaluation: `jinaai/jina-reranker-v1-tiny-en` put the expected page first for 24, `jinaai/jina-reranker-v1-turbo-en` for 22, against 26 for the MiniLM model and 21 for vector search alone, and both separated answerable from unanswerable questions less well. Neither was adopted. The probe was run by hand and its output was not saved, so these counts have no file in `eval/results/`. With a language model in the answer step the reranker matters less: the model sees five passages and does the refusing.

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
- **Heading chunks,** this project's chunker, for comparison (main table, 12 PDFs): top result 16/26, top 3 22/26, correct citation 22/26.

LangChain's stock splitter put the expected page first slightly more often than our chunker (17 against 16) and clearly more often than our fixed-window baseline (13). It did worse where it counts for this brief: a correct citation in 19 of 26 answers against 22 of 26. The LangChain implementation therefore keeps our heading and page aware chunker as its default loader and keeps the stock loader as the baseline. The gap is three questions on a set of 26, so it is an indication and not a proof.

## Round 1 history: tuning at 12 PDFs

These numbers are from the first version of the plain-Python implementation (commit `a5c0c6a` of rag-pdf-demo). Answer mode: extractive.

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

The round 1 held-out check then showed the weak spot that the later rounds worked on: only 1 of 6 on-topic unanswerable questions was refused.

## What the numbers do not show

- **Generated answers were graded by the model that wrote them,** not by a person.
- **The question sets are small.** One question is about 4 percentage points on the main set and 10 on the newer held-out set. Differences of one or two questions are within what a different set of questions, or a second run of the model, could reverse.
- **We wrote the questions and the reference answers ourselves,** and one "unanswerable" question turned out to be answerable. A client's own questions are the real test.
- **Scoring accepts only the expected document.** At 100 PDFs that undercounts correct answers found elsewhere, as the review of misses shows.
- **Thresholds were tuned at 12 PDFs and not retuned at 100.** The 100-PDF columns show what happens when the corpus grows under settings chosen for a smaller one.
- **Latency was measured on one small machine with no concurrent users,** and excludes the language model call.
- **One model, one endpoint.** Generated mode was run with `openai/gpt-4o-mini` through OpenRouter. The OpenAI API directly, the default in the code, was not exercised beyond an authentication check, because that account had no credit.

## Reproduce

```sh
docker compose up -d --build
make ingest-full ingest-baseline
make eval eval-full eval-baseline eval-heldout eval-rerank bench
OPENAI_API_KEY=... make eval-answers eval-answers-rerank PY=.venv/bin/python
```

# Evaluation

All numbers on this page come from `python -m ragdemo.eval`, run inside the app container against the pgvector database. The raw output of every run, question by question, is in `eval/results/`.

## What was measured, and in which mode

- **Answer mode: extractive.** No language model wrote any answer in these runs. The answer is the best passages quoted word for word, and the citations are the pages those passages came from. The generated mode (an OpenAI-compatible model writes the answer from the passages) exists in the code but was not evaluated, because no API key was available when this was built.
- **Embedding model:** `BAAI/bge-small-en-v1.5` on CPU.
- **Retrieval depth:** top 5 chunks retrieved, up to 3 cited.
- **Questions:** `eval/questions.json`, 26 with the answer in the corpus and 8 without. Each in-corpus question lists the document and the pages where its answer is stated. The expected pages were found by reading the PDFs, before any retrieval run.

The metrics:

- **Retrieval hit rate at k:** an accepted page of the expected document is among the top k chunks.
- **Citation correctness:** the system answered, and at least one cited passage is on an accepted page of the expected document.
- **False refusals:** in-corpus questions the system declined to answer.
- **Refusals out of corpus:** out-of-corpus questions the system declined to answer. Higher is better.

## Before and after

| Metric | Baseline | Step 1: heading chunks | Step 2: hybrid search (rejected) | Step 3: threshold 0.62 | Step 4: unknown-word check (final) |
| --- | --- | --- | --- | --- | --- |
| Expected page is the top result | 13/26 (50%) | 16/26 (62%) | 14/26 (54%) | 16/26 (62%) | 16/26 (62%) |
| Expected page in top 3 | 21/26 (81%) | 22/26 (85%) | 19/26 (73%) | 22/26 (85%) | 22/26 (85%) |
| Expected page in top 5 | 22/26 (85%) | 22/26 (85%) | 20/26 (77%) | 22/26 (85%) | 22/26 (85%) |
| Answered with a citation to an accepted page | 21/26 (81%) | 22/26 (85%) | 19/26 (73%) | 22/26 (85%) | 22/26 (85%) |
| False refusals (in corpus) | 0/26 (0%) | 0/26 (0%) | 0/26 (0%) | 0/26 (0%) | 0/26 (0%) |
| Refusals (out of corpus, higher is better) | 1/8 (12%) | 1/8 (12%) | 1/8 (12%) | 4/8 (50%) | 8/8 (100%) |

What each step changed:

- **Baseline.** Fixed windows of 1,000 characters with 150 overlap, cut inside each page, headers and footers left in. Vector search only. Refusal threshold 0.50, a guess made before any run.
- **Step 1, heading and page aware chunks.** Chunks start at section headings, never cross a page, running headers and footers are removed, and the heading path is embedded together with the text. The expected page became the top result for 3 more questions (13 to 16 of 26), and one more question got a correct citation.
- **Step 2, hybrid search. Tried and rejected.** Postgres full-text search was merged with vector search by reciprocal rank fusion. On this corpus it pushed correct pages down, because common words in the question matched many unrelated chunks. Keyword weights of 0.2 and 0.4 were also tried on the first version of the chunker and were no better than vector search alone. The code stays in the repository behind `HYBRID=1`, switched off.
- **Step 3, refusal threshold raised from 0.50 to 0.62.** Chosen from the threshold sweep that every run prints: 0.62 is the highest value in the sweep (steps of 0.02) with no false refusals on the in-corpus questions.
- **Step 4, unknown-word check.** A similarity threshold alone could not separate the two groups: out-of-corpus questions scored up to 0.67, while two genuine questions scored below 0.64. The check looks up each content word of the question in the corpus. If a word appears in no chunk at all (for example "GDPR" or "Salesforce" here), the question must clear a stricter threshold of 0.75.

## Held-out check

The thresholds above were tuned on the same 34 questions they are scored on, which flatters them. So after the settings were fixed, 12 new questions were written (`eval/questions-heldout.json`) and run once. The 6 out-of-corpus questions in this set were chosen to be harder: they are on the corpus topic and use its vocabulary, but no document answers them.

| Metric | Baseline settings | Tuned settings |
| --- | --- | --- |
| Expected page is the top result | 5/6 (83%) | 5/6 (83%) |
| Expected page in top 3 | 6/6 (100%) | 6/6 (100%) |
| Expected page in top 5 | 6/6 (100%) | 6/6 (100%) |
| Answered with a citation to an accepted page | 6/6 (100%) | 6/6 (100%) |
| False refusals (in corpus) | 0/6 (0%) | 0/6 (0%) |
| Refusals (out of corpus, higher is better) | 0/6 (0%) | 1/6 (17%) |

Retrieval and citations held up on the new in-corpus questions. The refusal path did not: only 1 of the 6 on-topic unanswerable questions was refused. "Which antivirus product is the best choice for a small business?" scores 0.73 against passages that discuss antivirus software without naming a product, and every word of it is in the corpus, so neither check fires.

This is the honest limit of refusing on retrieval scores alone. Off-topic questions are caught (8 of 8 on the main set). On-topic questions that the documents do not answer are mostly not caught, and the reply is then a list of related passages with their pages. In extractive mode that is visible to the reader, since the passages are quoted and plainly do not answer the question. The usual fix is the generated mode, where the model is told to refuse when the passages do not contain the answer. That path is implemented but its refusal rate is not measured here.

## What the numbers do not show

- Nothing here measures the wording or faithfulness of a generated answer.
- The question sets are small. One question is worth about 4 percentage points on the main set and 17 on the held-out set.
- Four in-corpus questions still miss in the final configuration (in-01, in-08, in-16, in-17). In each case the system answered with passages from a related page, not the page that states the answer. Two of them lose the top spot to a different document that covers the same subject in more general terms.
- "Citation correctness" in extractive mode is close to retrieval hit rate at 3 by construction, because the cited passages are the top passages above the threshold.

## Reproduce

```sh
docker compose up -d --build
make ingest-baseline
make eval-baseline eval-steps eval eval-heldout
```

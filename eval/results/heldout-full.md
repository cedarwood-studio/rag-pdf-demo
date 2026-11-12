# Evaluation run: heldout-full

- Questions: `eval/questions-heldout.json`
- Collection: `full`
- Answer mode: extractive
- Implementation: plain Python
- Search: exact
- Reranker: Xenova/ms-marco-MiniLM-L-6-v2, pool 10, threshold -1.5
- Embedding model: BAAI/bge-small-en-v1.5
- Refusal threshold: 0.62
- Strict threshold for questions with a word found nowhere in the corpus: 0.75
- Chunks in collection: 18205
- Run at: 2026-11-12T00:34:21+00:00

| Metric | Result |
| --- | --- |
| retrieval_hit@1 | 6/6 (100%) |
| retrieval_hit@3 | 6/6 (100%) |
| retrieval_hit@5 | 6/6 (100%) |
| citation_correct | 6/6 (100%) |
| top_citation_correct | 6/6 (100%) |
| false_refusals_in_corpus | 0/6 (0%) |
| refusals_out_of_corpus | 3/6 (50%) |

| Id | Question | Expected | Top score | Rerank score | Unknown words | Outcome | Cited |
| --- | --- | --- | --- | --- | --- | --- | --- |
| held-in-01 | What is a rootkit? | NIST.SP.800-83r1.pdf p.15 | 0.748 | 7.65 | - | citation correct | NIST.SP.800-83r1.pdf p.15; NIST.SP.800-83r1.pdf p.44; NIST.SP.800-150.pdf p.38 |
| held-in-02 | What is a blended attack? | NIST.SP.800-83r1.pdf p.14 | 0.721 | 7.05 | - | citation correct | NIST.SP.800-83r1.pdf p.14; NIST.SP.800-187.pdf p.35; NIST.SP.800-12r1.pdf p.31 |
| held-in-03 | What does maximum tolerable downtime mean? | nistspecialpublication800-34r1.pdf p.31,121,144 | 0.724 | 6.93 | - | citation correct | nistspecialpublication800-34r1.pdf p.144; nistspecialpublication800-34r1.pdf p.121; nistspecialpublication800-34r1.pdf p.125 |
| held-in-04 | What is the difference between an event and an incident? | NIST.SP.800-61r2.pdf p.16 | 0.771 | 5.07 | - | citation correct | NIST.SP.800-61r2.pdf p.16; NIST.SP.800-61r2.pdf p.75; NIST.SP.800-61r2.pdf p.38 |
| held-in-05 | How long does the salt need to be when password hashes are stored? | NIST.SP.800-63b.pdf p.26 | 0.777 | 2.11 | - | citation correct | NIST.SP.800-63b.pdf p.26; nistspecialpublication800-115.pdf p.35; NIST.SP.800-63b.pdf p.26 |
| held-in-06 | How frequently should incremental backups run in a small business? | NIST.IR.7621r1.pdf p.33 | 0.848 | 4.15 | - | citation correct | NIST.IR.7621r1.pdf p.33; nistspecialpublication800-123.pdf p.42; nistspecialpublication800-34r1.pdf p.35 |
| held-out-01 | Which antivirus product is the best choice for a small business? | not in corpus | 0.730 | -2.09 | - | refused by rerank check (right) | none |
| held-out-02 | How much does a hot site cost per month? | not in corpus | 0.637 | -5.29 | - | refused by rerank check (right) | none |
| held-out-03 | Who is the current director of NIST? | not in corpus | 0.689 | 4.16 | - | answered (wrong) | NIST.SP.800-207.pdf p.2; nistspecialpublication800-39.pdf p.1; nistspecialpublication800-30r1.pdf p.5 |
| held-out-04 | What is the penalty for failing to report an incident within 72 hours? | not in corpus | 0.693 | -4.3 | - | refused by rerank check (right) | none |
| held-out-05 | How many people work on the incident response team at NIST? | not in corpus | 0.724 | 2.75 | - | answered (wrong) | NIST.SP.800-61r2.pdf p.23; NIST.SP.800-61r2.pdf p.24; NIST.SP.800-61r2.pdf p.24 |
| held-out-06 | What password does the default administrator account use? | not in corpus | 0.761 | 3.87 | - | answered (wrong) | nistspecialpublication800-48r1.pdf p.34; nistspecialpublication800-123.pdf p.28; NIST.IR.7621r1.pdf p.38 |

## Threshold sweep

| Threshold | False refusals (in corpus) | Refusals (out of corpus) |
| --- | --- | --- |
| 0.50 | 0/6 | 0/6 |
| 0.52 | 0/6 | 0/6 |
| 0.54 | 0/6 | 0/6 |
| 0.56 | 0/6 | 0/6 |
| 0.58 | 0/6 | 0/6 |
| 0.60 | 0/6 | 0/6 |
| 0.62 | 0/6 | 0/6 |
| 0.64 | 0/6 | 1/6 |
| 0.66 | 0/6 | 1/6 |
| 0.68 | 0/6 | 1/6 |
| 0.70 | 0/6 | 3/6 |
| 0.72 | 0/6 | 3/6 |
| 0.74 | 2/6 | 5/6 |
| 0.76 | 3/6 | 5/6 |
| 0.78 | 5/6 | 6/6 |
| 0.80 | 5/6 | 6/6 |

## Rerank threshold sweep

Only questions that passed the similarity checks reach the reranker, so only those are counted here.

| Rerank threshold | False refusals (in corpus) | Refusals (out of corpus) |
| --- | --- | --- |
| -4.0 | 0/6 | 2/6 |
| -3.5 | 0/6 | 2/6 |
| -3.0 | 0/6 | 2/6 |
| -2.5 | 0/6 | 2/6 |
| -2.0 | 0/6 | 3/6 |
| -1.5 | 0/6 | 3/6 |
| -1.0 | 0/6 | 3/6 |
| -0.5 | 0/6 | 3/6 |
| 0.0 | 0/6 | 3/6 |
| 0.5 | 0/6 | 3/6 |
| 1.0 | 0/6 | 3/6 |
| 1.5 | 0/6 | 3/6 |
| 2.0 | 0/6 | 3/6 |
| 2.5 | 1/6 | 3/6 |
| 3.0 | 1/6 | 4/6 |
| 3.5 | 1/6 | 4/6 |
| 4.0 | 1/6 | 5/6 |

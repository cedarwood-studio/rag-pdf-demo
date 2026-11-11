# Evaluation run: heldout-baseline

- Questions: `eval/questions-heldout.json`
- Collection: `fixed`
- Answer mode: extractive
- Retrieval: vector only
- Embedding model: BAAI/bge-small-en-v1.5
- Refusal threshold: 0.5
- Strict threshold for questions with a word found nowhere in the corpus: off
- Chunks in collection: 2740
- Run at: 2026-11-11T22:29:05+00:00

| Metric | Result |
| --- | --- |
| retrieval_hit@1 | 5/6 (83%) |
| retrieval_hit@3 | 6/6 (100%) |
| retrieval_hit@5 | 6/6 (100%) |
| citation_correct | 6/6 (100%) |
| top_citation_correct | 5/6 (83%) |
| false_refusals_in_corpus | 0/6 (0%) |
| refusals_out_of_corpus | 0/6 (0%) |

| Id | Question | Expected | Top score | Unknown words | Outcome | Cited |
| --- | --- | --- | --- | --- | --- | --- |
| held-in-01 | What is a rootkit? | NIST.SP.800-83r1.pdf p.15 | 0.745 | - | citation correct | NIST.SP.800-83r1.pdf p.15; NIST.SP.800-83r1.pdf p.44; NIST.SP.800-114r1.pdf p.27 |
| held-in-02 | What is a blended attack? | NIST.SP.800-83r1.pdf p.14 | 0.695 | - | citation correct | NIST.SP.800-83r1.pdf p.14; NIST.SP.800-12r1.pdf p.31; NIST.SP.800-61r2.pdf p.12 |
| held-in-03 | What does maximum tolerable downtime mean? | nistspecialpublication800-34r1.pdf p.31,121,144 | 0.792 | - | citation correct | nistspecialpublication800-34r1.pdf p.31; nistspecialpublication800-34r1.pdf p.31; nistspecialpublication800-34r1.pdf p.121 |
| held-in-04 | What is the difference between an event and an incident? | NIST.SP.800-61r2.pdf p.16 | 0.736 | - | citation correct | NIST.SP.800-61r2.pdf p.38; NIST.SP.800-61r2.pdf p.16; NIST.SP.800-61r2.pdf p.75 |
| held-in-05 | How long does the salt need to be when password hashes are stored? | NIST.SP.800-63b.pdf p.26 | 0.784 | - | citation correct | NIST.SP.800-63b.pdf p.26; NIST.SP.800-63b.pdf p.27; NIST.SP.800-63b.pdf p.79 |
| held-in-06 | How frequently should incremental backups run in a small business? | NIST.IR.7621r1.pdf p.33 | 0.831 | - | citation correct | NIST.IR.7621r1.pdf p.33; NIST.IR.7621r1.pdf p.33; nistspecialpublication800-34r1.pdf p.58 |
| held-out-01 | Which antivirus product is the best choice for a small business? | not in corpus | 0.725 | - | answered (wrong) | NIST.IR.7621r1.pdf p.30; NIST.SP.800-83r1.pdf p.22; NIST.SP.800-114r1.pdf p.27 |
| held-out-02 | How much does a hot site cost per month? | not in corpus | 0.654 | - | answered (wrong) | nistspecialpublication800-34r1.pdf p.36; nistspecialpublication800-34r1.pdf p.61; nistspecialpublication800-34r1.pdf p.36 |
| held-out-03 | Who is the current director of NIST? | not in corpus | 0.678 | - | answered (wrong) | NIST.SP.800-40r4.pdf p.2; nistspecialpublication800-34r1.pdf p.2; NIST.SP.800-63b.pdf p.3 |
| held-out-04 | What is the penalty for failing to report an incident within 72 hours? | not in corpus | 0.673 | - | answered (wrong) | NIST.SP.800-61r2.pdf p.63; NIST.SP.800-61r2.pdf p.49; NIST.SP.800-61r2.pdf p.43 |
| held-out-05 | How many people work on the incident response team at NIST? | not in corpus | 0.740 | - | answered (wrong) | NIST.CSWP.29.pdf p.27; NIST.SP.800-61r2.pdf p.75; NIST.SP.800-61r2.pdf p.24 |
| held-out-06 | What password does the default administrator account use? | not in corpus | 0.719 | - | answered (wrong) | NIST.SP.800-114r1.pdf p.24; NIST.IR.7621r1.pdf p.38; nistspecialpublication800-34r1.pdf p.84 |

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
| 0.64 | 0/6 | 0/6 |
| 0.66 | 0/6 | 1/6 |
| 0.68 | 0/6 | 3/6 |
| 0.70 | 1/6 | 3/6 |
| 0.72 | 1/6 | 4/6 |
| 0.74 | 2/6 | 6/6 |
| 0.76 | 3/6 | 6/6 |
| 0.78 | 3/6 | 6/6 |
| 0.80 | 5/6 | 6/6 |

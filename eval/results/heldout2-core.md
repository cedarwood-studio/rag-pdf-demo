# Evaluation run: heldout2-core

- Questions: `eval/questions-heldout2.json`
- Collection: `core`
- Answer mode: extractive
- Implementation: plain Python
- Search: exact
- Reranker: Xenova/ms-marco-MiniLM-L-6-v2, pool 10, threshold -1.5
- Embedding model: BAAI/bge-small-en-v1.5
- Refusal threshold: 0.62
- Strict threshold for questions with a word found nowhere in the corpus: 0.75
- Chunks in collection: 2448
- Run at: 2026-11-11T23:49:10+00:00

| Metric | Result |
| --- | --- |
| retrieval_hit@1 | 9/10 (90%) |
| retrieval_hit@3 | 9/10 (90%) |
| retrieval_hit@5 | 9/10 (90%) |
| citation_correct | 9/10 (90%) |
| top_citation_correct | 9/10 (90%) |
| false_refusals_in_corpus | 0/10 (0%) |
| refusals_out_of_corpus | 7/12 (58%) |

| Id | Question | Expected | Top score | Rerank score | Unknown words | Outcome | Cited |
| --- | --- | --- | --- | --- | --- | --- | --- |
| held2-in-01 | What is an attrition attack? | NIST.SP.800-61r2.pdf p.12,35 | 0.818 | 8.15 | - | citation correct | NIST.SP.800-61r2.pdf p.12; NIST.SP.800-61r2.pdf p.35; NIST.SP.800-12r1.pdf p.31 |
| held2-in-02 | What is a portal in a remote access setup? | NIST.SP.800-46r2.pdf p.17 | 0.791 | 6.34 | - | citation correct | NIST.SP.800-46r2.pdf p.17; NIST.SP.800-46r2.pdf p.18; NIST.SP.800-46r2.pdf p.24 |
| held2-in-03 | What are the steps in the life cycle of a security awareness and training program? | nistspecialpublication800-50.pdf p.11 | 0.838 | 8.09 | - | citation correct | nistspecialpublication800-50.pdf p.11; nistspecialpublication800-50.pdf p.23; nistspecialpublication800-50.pdf p.43 |
| held2-in-04 | What types of compiled viruses are there? | NIST.SP.800-83r1.pdf p.13 | 0.796 | 6.09 | - | citation correct | NIST.SP.800-83r1.pdf p.13; NIST.SP.800-12r1.pdf p.33; NIST.SP.800-83r1.pdf p.13 |
| held2-in-05 | What should a small business do when an employee leaves? | NIST.IR.7621r1.pdf p.25 | 0.642 | 3.73 | - | citation correct | NIST.IR.7621r1.pdf p.25; NIST.IR.7621r1.pdf p.29; NIST.IR.7621r1.pdf p.21 |
| held2-in-06 | What does an Organizational Profile describe? | NIST.CSWP.29.pdf p.11 | 0.744 | 7.65 | - | citation correct | NIST.CSWP.29.pdf p.11; NIST.CSWP.29.pdf p.12; NIST.CSWP.29.pdf p.16 |
| held2-in-07 | How long a password should a system let users choose? | NIST.SP.800-63b.pdf p.24,64 | 0.805 | 3.69 | - | citation wrong | NIST.IR.7621r1.pdf p.38; NIST.SP.800-114r1.pdf p.24; NIST.SP.800-63b.pdf p.79 |
| held2-in-08 | How often should staff with contingency plan roles be trained? | nistspecialpublication800-34r1.pdf p.42 | 0.813 | 7.04 | - | citation correct | nistspecialpublication800-34r1.pdf p.42; nistspecialpublication800-34r1.pdf p.28; nistspecialpublication800-34r1.pdf p.128 |
| held2-in-09 | Which wireless security option is preferred for a home network? | NIST.SP.800-114r1.pdf p.21 | 0.815 | 6.93 | - | citation correct | NIST.SP.800-114r1.pdf p.21; NIST.SP.800-114r1.pdf p.20; NIST.SP.800-114r1.pdf p.19 |
| held2-in-10 | How many security control baselines are there and what do they correspond to? | NIST.SP.800-12r1.pdf p.53 | 0.782 | 2.99 | - | citation correct | NIST.SP.800-12r1.pdf p.53; NIST.SP.800-12r1.pdf p.53; NIST.SP.800-63b.pdf p.19 |
| held2-out-01 | Which mobile device management product should we buy? | not in corpus | 0.714 | 1.22 | - | answered (wrong) | NIST.SP.800-46r2.pdf p.34; NIST.SP.800-46r2.pdf p.35; NIST.SP.800-46r2.pdf p.35 |
| held2-out-02 | How much does an uninterruptible power supply cost for a small office? | not in corpus | 0.671 | -3.38 | - | refused by rerank check (right) | none |
| held2-out-03 | What is the email address of the incident response team? | not in corpus | 0.772 | 3.62 | - | answered (wrong) | NIST.SP.800-61r2.pdf p.75; NIST.SP.800-61r2.pdf p.32; NIST.SP.800-61r2.pdf p.29 |
| held2-out-04 | Which company makes the most reliable degausser? | not in corpus | 0.607 | - | - | refused by similarity check (right) | none |
| held2-out-05 | What salary does an incident response team manager earn? | not in corpus | 0.733 | 0.99 | - | answered (wrong) | NIST.SP.800-61r2.pdf p.26; NIST.SP.800-61r2.pdf p.25; NIST.SP.800-61r2.pdf p.75 |
| held2-out-06 | Which VPN vendor has had the fewest vulnerabilities? | not in corpus | 0.677 | - | fewest | refused by unknown word check (right) | none |
| held2-out-07 | Which training vendor offers the cheapest security awareness course? | not in corpus | 0.677 | - | cheapest | refused by unknown word check (right) | none |
| held2-out-08 | On what date will the incident handling guide be withdrawn? | not in corpus | 0.736 | 6.37 | - | answered (wrong) | NIST.SP.800-61r2.pdf p.1; NIST.SP.800-61r2.pdf p.51; NIST.SP.800-61r2.pdf p.49 |
| held2-out-09 | Which cloud provider is approved for storing our backups? | not in corpus | 0.738 | 4.91 | - | answered (wrong) | NIST.IR.7621r1.pdf p.32; nistspecialpublication800-34r1.pdf p.64; nistspecialpublication800-34r1.pdf p.71 |
| held2-out-10 | How many passwords were stolen in the largest breach on record? | not in corpus | 0.699 | -6.26 | - | refused by rerank check (right) | none |
| held2-out-11 | What is the boiling point of water at sea level? | not in corpus | 0.505 | - | boil | refused by similarity check (right) | none |
| held2-out-12 | Who won the football World Cup in 2018? | not in corpus | 0.439 | - | football | refused by similarity check (right) | none |

## Threshold sweep

| Threshold | False refusals (in corpus) | Refusals (out of corpus) |
| --- | --- | --- |
| 0.50 | 0/10 | 4/12 |
| 0.52 | 0/10 | 4/12 |
| 0.54 | 0/10 | 4/12 |
| 0.56 | 0/10 | 4/12 |
| 0.58 | 0/10 | 4/12 |
| 0.60 | 0/10 | 4/12 |
| 0.62 | 0/10 | 5/12 |
| 0.64 | 0/10 | 5/12 |
| 0.66 | 1/10 | 5/12 |
| 0.68 | 1/10 | 6/12 |
| 0.70 | 1/10 | 7/12 |
| 0.72 | 1/10 | 8/12 |
| 0.74 | 1/10 | 11/12 |
| 0.76 | 2/10 | 11/12 |
| 0.78 | 2/10 | 12/12 |
| 0.80 | 5/10 | 12/12 |

## Rerank threshold sweep

Only questions that passed the similarity checks reach the reranker, so only those are counted here.

| Rerank threshold | False refusals (in corpus) | Refusals (out of corpus) |
| --- | --- | --- |
| -4.0 | 0/10 | 1/7 |
| -3.5 | 0/10 | 1/7 |
| -3.0 | 0/10 | 2/7 |
| -2.5 | 0/10 | 2/7 |
| -2.0 | 0/10 | 2/7 |
| -1.5 | 0/10 | 2/7 |
| -1.0 | 0/10 | 2/7 |
| -0.5 | 0/10 | 2/7 |
| 0.0 | 0/10 | 2/7 |
| 0.5 | 0/10 | 2/7 |
| 1.0 | 0/10 | 3/7 |
| 1.5 | 0/10 | 4/7 |
| 2.0 | 0/10 | 4/7 |
| 2.5 | 0/10 | 4/7 |
| 3.0 | 1/10 | 4/7 |
| 3.5 | 1/10 | 4/7 |
| 4.0 | 3/10 | 5/7 |

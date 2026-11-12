# Evaluation run: heldout2-full

- Questions: `eval/questions-heldout2.json`
- Collection: `full`
- Answer mode: extractive
- Implementation: plain Python
- Search: exact
- Reranker: off
- Embedding model: BAAI/bge-small-en-v1.5
- Refusal threshold: 0.62
- Strict threshold for questions with a word found nowhere in the corpus: 0.75
- Chunks in collection: 18205
- Run at: 2026-11-12T01:34:48+00:00

| Metric | Result |
| --- | --- |
| retrieval_hit@1 | 5/10 (50%) |
| retrieval_hit@3 | 6/10 (60%) |
| retrieval_hit@5 | 7/10 (70%) |
| citation_correct | 6/10 (60%) |
| top_citation_correct | 5/10 (50%) |
| false_refusals_in_corpus | 0/10 (0%) |
| refusals_out_of_corpus | 4/12 (33%) |

| Id | Question | Expected | Top score | Rerank score | Unknown words | Outcome | Cited |
| --- | --- | --- | --- | --- | --- | --- | --- |
| held2-in-01 | What is an attrition attack? | NIST.SP.800-61r2.pdf p.12,35 | 0.818 | - | - | citation correct | NIST.SP.800-61r2.pdf p.12; nistspecialpublication800-30r1.pdf p.72; NIST.SP.800-61r2.pdf p.35 |
| held2-in-02 | What is a portal in a remote access setup? | NIST.SP.800-46r2.pdf p.17 | 0.791 | - | - | citation correct | NIST.SP.800-46r2.pdf p.17; NIST.SP.800-46r2.pdf p.18; NIST.SP.800-46r2.pdf p.17 |
| held2-in-03 | What are the steps in the life cycle of a security awareness and training program? | nistspecialpublication800-50.pdf p.11 | 0.838 | - | - | citation correct | nistspecialpublication800-50.pdf p.23; nistspecialpublication800-50.pdf p.43; nistspecialpublication800-50.pdf p.11 |
| held2-in-04 | What types of compiled viruses are there? | NIST.SP.800-83r1.pdf p.13 | 0.796 | - | - | citation correct | NIST.SP.800-83r1.pdf p.13; NIST.SP.800-83r1.pdf p.13; NIST.SP.800-12r1.pdf p.33 |
| held2-in-05 | What should a small business do when an employee leaves? | NIST.IR.7621r1.pdf p.25 | 0.642 | - | - | citation wrong | NIST.IR.7621r1.pdf p.21; NIST.IR.7621r1.pdf p.35; NIST.IR.7621r1.pdf p.29 |
| held2-in-06 | What does an Organizational Profile describe? | NIST.CSWP.29.pdf p.11 | 0.760 | - | - | citation wrong | NIST.CSWP.04162018.pdf p.11; NIST.CSWP.29.pdf p.12; nistspecialpublication800-39.pdf p.10 |
| held2-in-07 | How long a password should a system let users choose? | NIST.SP.800-63b.pdf p.24,64 | 0.805 | - | - | citation wrong | NIST.SP.800-114r1.pdf p.24; NIST.IR.7621r1.pdf p.38; nistspecialpublication800-123.pdf p.29 |
| held2-in-08 | How often should staff with contingency plan roles be trained? | nistspecialpublication800-34r1.pdf p.42 | 0.813 | - | - | citation correct | nistspecialpublication800-34r1.pdf p.42; nistspecialpublication800-34r1.pdf p.127; nistspecialpublication800-35.pdf p.49 |
| held2-in-09 | Which wireless security option is preferred for a home network? | NIST.SP.800-114r1.pdf p.21 | 0.815 | - | - | citation correct | NIST.SP.800-114r1.pdf p.21; NIST.SP.800-114r1.pdf p.20; NIST.SP.800-114r1.pdf p.20 |
| held2-in-10 | How many security control baselines are there and what do they correspond to? | NIST.SP.800-12r1.pdf p.53 | 0.844 | - | - | citation wrong | NIST.SP.800-53B.pdf p.4; NIST.SP.800-53B.pdf p.39; NIST.SP.800-53B.pdf p.12 |
| held2-out-01 | Which mobile device management product should we buy? | not in corpus | 0.722 | - | - | answered (wrong) | NIST.SP.800-163r1.pdf p.28; NIST.SP.800-46r2.pdf p.35; NIST.SP.800-46r2.pdf p.35 |
| held2-out-02 | How much does an uninterruptible power supply cost for a small office? | not in corpus | 0.754 | - | - | answered (wrong) | nistspecialpublication800-58.pdf p.13; nistspecialpublication800-58.pdf p.29; NIST.IR.7621r1.pdf p.25 |
| held2-out-03 | What is the email address of the incident response team? | not in corpus | 0.775 | - | - | answered (wrong) | nistspecialpublication800-86.pdf p.93; NIST.SP.800-61r2.pdf p.29; NIST.SP.800-61r2.pdf p.23 |
| held2-out-04 | Which company makes the most reliable degausser? | not in corpus | 0.607 | - | - | refused by similarity check (right) | none |
| held2-out-05 | What salary does an incident response team manager earn? | not in corpus | 0.733 | - | - | answered (wrong) | NIST.SP.800-61r2.pdf p.75; NIST.SP.800-61r2.pdf p.25; NIST.SP.800-61r2.pdf p.26 |
| held2-out-06 | Which VPN vendor has had the fewest vulnerabilities? | not in corpus | 0.696 | - | fewest | refused by unknown word check (right) | none |
| held2-out-07 | Which training vendor offers the cheapest security awareness course? | not in corpus | 0.691 | - | - | answered (wrong) | nistspecialpublication800-35.pdf p.53; nistspecialpublication800-50.pdf p.41; nistspecialpublication800-50.pdf p.33 |
| held2-out-08 | On what date will the incident handling guide be withdrawn? | not in corpus | 0.736 | - | - | answered (wrong) | NIST.SP.800-61r2.pdf p.1; NIST.SP.800-61r2.pdf p.45; NIST.SP.800-47r1.pdf p.36 |
| held2-out-09 | Which cloud provider is approved for storing our backups? | not in corpus | 0.738 | - | - | answered (wrong) | NIST.IR.7621r1.pdf p.32; NIST.SP.800-209.pdf p.68; nistspecialpublication800-144.pdf p.42 |
| held2-out-10 | How many passwords were stolen in the largest breach on record? | not in corpus | 0.699 | - | - | answered (wrong) | NIST.SP.800-63b.pdf p.79; NIST.SP.800-171r3.pdf p.46; NIST.SP.800-63b.pdf p.78 |
| held2-out-11 | What is the boiling point of water at sea level? | not in corpus | 0.550 | - | - | refused by similarity check (right) | none |
| held2-out-12 | Who won the football World Cup in 2018? | not in corpus | 0.449 | - | football | refused by similarity check (right) | none |

## Threshold sweep

| Threshold | False refusals (in corpus) | Refusals (out of corpus) |
| --- | --- | --- |
| 0.50 | 0/10 | 2/12 |
| 0.52 | 0/10 | 2/12 |
| 0.54 | 0/10 | 2/12 |
| 0.56 | 0/10 | 3/12 |
| 0.58 | 0/10 | 3/12 |
| 0.60 | 0/10 | 3/12 |
| 0.62 | 0/10 | 4/12 |
| 0.64 | 0/10 | 4/12 |
| 0.66 | 1/10 | 4/12 |
| 0.68 | 1/10 | 4/12 |
| 0.70 | 1/10 | 6/12 |
| 0.72 | 1/10 | 6/12 |
| 0.74 | 1/10 | 10/12 |
| 0.76 | 1/10 | 11/12 |
| 0.78 | 2/10 | 12/12 |
| 0.80 | 4/10 | 12/12 |

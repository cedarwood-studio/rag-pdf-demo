# Evaluation run: core

- Questions: `eval/questions.json`
- Collection: `core`
- Answer mode: extractive
- Implementation: plain Python
- Search: exact
- Reranker: Xenova/ms-marco-MiniLM-L-6-v2, pool 10, threshold -1.5
- Embedding model: BAAI/bge-small-en-v1.5
- Refusal threshold: 0.62
- Strict threshold for questions with a word found nowhere in the corpus: 0.75
- Chunks in collection: 2448
- Run at: 2026-11-11T23:47:19+00:00

| Metric | Result |
| --- | --- |
| retrieval_hit@1 | 20/26 (77%) |
| retrieval_hit@3 | 21/26 (81%) |
| retrieval_hit@5 | 23/26 (88%) |
| citation_correct | 21/26 (81%) |
| top_citation_correct | 20/26 (77%) |
| false_refusals_in_corpus | 0/26 (0%) |
| refusals_out_of_corpus | 8/8 (100%) |

| Id | Question | Expected | Top score | Rerank score | Unknown words | Outcome | Cited |
| --- | --- | --- | --- | --- | --- | --- | --- |
| in-01 | What is the minimum length for a password that a user chooses themselves? | NIST.SP.800-63b.pdf p.24 | 0.774 | 3.49 | - | citation wrong | NIST.SP.800-63b.pdf p.79; NIST.SP.800-63b.pdf p.78; NIST.SP.800-114r1.pdf p.24 |
| in-02 | Should we force users to change their passwords on a regular schedule? | NIST.SP.800-63b.pdf p.25,65 | 0.805 | 2.69 | - | citation wrong | NIST.IR.7621r1.pdf p.38; NIST.SP.800-114r1.pdf p.25; NIST.SP.800-114r1.pdf p.33 |
| in-03 | At authenticator assurance level 2, after how long without activity does a user have to sign in again? | NIST.SP.800-63b.pdf p.19,22 | 0.768 | 2.38 | - | citation correct | NIST.SP.800-63b.pdf p.19; NIST.SP.800-63b.pdf p.21; NIST.SP.800-63b.pdf p.64 |
| in-04 | What is the difference between a cold site, a warm site and a hot site? | nistspecialpublication800-34r1.pdf p.36,37,61,62 | 0.780 | 6.63 | - | citation correct | nistspecialpublication800-34r1.pdf p.61; nistspecialpublication800-34r1.pdf p.36; nistspecialpublication800-34r1.pdf p.61 |
| in-05 | What does recovery point objective mean? | nistspecialpublication800-34r1.pdf p.31,121,144 | 0.779 | 6.79 | - | citation correct | nistspecialpublication800-34r1.pdf p.144; nistspecialpublication800-34r1.pdf p.121; nistspecialpublication800-34r1.pdf p.31 |
| in-06 | What is a tabletop exercise? | nistspecialpublication800-34r1.pdf p.43 | 0.771 | 7.57 | - | citation correct | nistspecialpublication800-34r1.pdf p.43; nistspecialpublication800-34r1.pdf p.43 |
| in-07 | What is the difference between clearing, purging and destroying media? | NIST.SP.800-88r1.pdf p.18 | 0.814 | 2.49 | - | citation correct | NIST.SP.800-88r1.pdf p.18; NIST.SP.800-88r1.pdf p.52; NIST.SP.800-88r1.pdf p.34 |
| in-08 | What record should be filled in after a drive has been sanitized? | NIST.SP.800-88r1.pdf p.31,32,65 | 0.775 | -0.61 | - | citation correct | NIST.SP.800-88r1.pdf p.43; NIST.SP.800-88r1.pdf p.44; NIST.SP.800-88r1.pdf p.32 |
| in-09 | What is the difference between a precursor and an indicator of an incident? | NIST.SP.800-61r2.pdf p.36 | 0.875 | 8.46 | - | citation correct | NIST.SP.800-61r2.pdf p.36; NIST.SP.800-61r2.pdf p.38; NIST.SP.800-61r2.pdf p.60 |
| in-10 | How soon after an incident should the lessons learned meeting take place? | NIST.SP.800-61r2.pdf p.48 | 0.814 | 5.93 | - | citation correct | NIST.SP.800-61r2.pdf p.48; NIST.SP.800-61r2.pdf p.13; NIST.SP.800-61r2.pdf p.54 |
| in-11 | What categories describe how much effort it takes to recover from an incident? | NIST.SP.800-61r2.pdf p.43 | 0.810 | 4.92 | - | citation correct | NIST.SP.800-61r2.pdf p.43; NIST.SP.800-61r2.pdf p.42; NIST.SP.800-61r2.pdf p.52 |
| in-12 | What structures can an incident response team have? | NIST.SP.800-61r2.pdf p.23 | 0.877 | 8.81 | - | citation correct | NIST.SP.800-61r2.pdf p.23; NIST.SP.800-61r2.pdf p.23; NIST.SP.800-61r2.pdf p.11 |
| in-13 | What are the six functions of the Cybersecurity Framework? | NIST.CSWP.29.pdf p.8,31 | 0.805 | 7.03 | - | citation wrong | NIST.CSWP.29.pdf p.9; NIST.IR.7621r1.pdf p.48; NIST.CSWP.29.pdf p.6 |
| in-14 | What are the four tiers called? | NIST.CSWP.29.pdf p.12,29,31 | 0.638 | 2.66 | - | citation correct | NIST.CSWP.29.pdf p.12 |
| in-15 | What are the main kinds of remote access methods for teleworkers? | NIST.SP.800-46r2.pdf p.14 | 0.821 | 8.2 | - | citation correct | NIST.SP.800-46r2.pdf p.14; NIST.SP.800-114r1.pdf p.13; NIST.SP.800-114r1.pdf p.13 |
| in-16 | How can we find out whether an employee's phone has been jailbroken? | NIST.SP.800-46r2.pdf p.27,35 | 0.635 | -1.05 | - | citation wrong | NIST.IR.7621r1.pdf p.19 |
| in-17 | What should we do about systems that cannot be patched? | NIST.SP.800-40r4.pdf p.19,22,23 | 0.700 | 3.81 | - | citation wrong | NIST.IR.7621r1.pdf p.26; NIST.SP.800-40r4.pdf p.16; NIST.SP.800-40r4.pdf p.20 |
| in-18 | How does emergency patching differ from routine patching? | NIST.SP.800-40r4.pdf p.18,19,22 | 0.816 | 6.09 | - | citation correct | NIST.SP.800-40r4.pdf p.18; NIST.SP.800-40r4.pdf p.22; NIST.SP.800-40r4.pdf p.19 |
| in-19 | What is the difference between security awareness and security training? | nistspecialpublication800-50.pdf p.20,21 | 0.878 | 8.44 | - | citation correct | nistspecialpublication800-50.pdf p.21; nistspecialpublication800-50.pdf p.20; NIST.SP.800-12r1.pdf p.70 |
| in-20 | What models are there for organizing a security awareness and training program? | nistspecialpublication800-50.pdf p.11,23,24 | 0.836 | 7.59 | - | citation correct | nistspecialpublication800-50.pdf p.24; nistspecialpublication800-50.pdf p.44; nistspecialpublication800-50.pdf p.23 |
| in-21 | What is a keystroke logger? | NIST.SP.800-83r1.pdf p.15 | 0.738 | 5.12 | - | citation correct | NIST.SP.800-83r1.pdf p.15; NIST.SP.800-61r2.pdf p.65; NIST.SP.800-12r1.pdf p.91 |
| in-22 | What is sandboxing and how does it limit malware? | NIST.SP.800-83r1.pdf p.9,26 | 0.844 | 7.48 | - | citation correct | NIST.SP.800-83r1.pdf p.26; NIST.SP.800-83r1.pdf p.26; NIST.SP.800-83r1.pdf p.9 |
| in-23 | How often should a small business make a full backup of its data? | NIST.IR.7621r1.pdf p.32 | 0.858 | 5.03 | - | citation correct | NIST.IR.7621r1.pdf p.32; NIST.IR.7621r1.pdf p.33; nistspecialpublication800-34r1.pdf p.35 |
| in-24 | Why should a small business install an uninterruptible power supply? | NIST.IR.7621r1.pdf p.25 | 0.753 | 4.77 | - | citation correct | NIST.IR.7621r1.pdf p.25; NIST.IR.7621r1.pdf p.43; nistspecialpublication800-34r1.pdf p.33 |
| in-25 | Is it safe to check work email from a hotel kiosk computer? | NIST.SP.800-114r1.pdf p.10,37 | 0.720 | 3.5 | - | citation correct | NIST.SP.800-114r1.pdf p.10; NIST.SP.800-46r2.pdf p.31; NIST.SP.800-114r1.pdf p.37 |
| in-26 | What are the three basic types of information security policy? | NIST.SP.800-12r1.pdf p.36 | 0.791 | 8.63 | - | citation correct | NIST.SP.800-12r1.pdf p.36; NIST.SP.800-12r1.pdf p.37; NIST.SP.800-12r1.pdf p.36 |
| out-01 | What is the refund policy for annual subscriptions? | not in corpus | 0.605 | - | refund | refused by similarity check (right) | none |
| out-02 | What is the capital of Australia? | not in corpus | 0.473 | - | - | refused by similarity check (right) | none |
| out-03 | How do I descale an espresso machine? | not in corpus | 0.606 | - | descale, espresso | refused by similarity check (right) | none |
| out-04 | What are the maximum fines under GDPR for a data breach? | not in corpus | 0.657 | - | gdpr | refused by unknown word check (right) | none |
| out-05 | How much does ISO 27001 certification cost? | not in corpus | 0.639 | - | 27001 | refused by unknown word check (right) | none |
| out-06 | What caused the 2017 Equifax breach? | not in corpus | 0.619 | - | equifax | refused by similarity check (right) | none |
| out-07 | Which encryption protocol does WhatsApp use for its messages? | not in corpus | 0.674 | - | whatsapp | refused by unknown word check (right) | none |
| out-08 | How do I configure single sign-on for Salesforce with Okta? | not in corpus | 0.645 | - | salesforce, okta | refused by unknown word check (right) | none |

## Threshold sweep

| Threshold | False refusals (in corpus) | Refusals (out of corpus) |
| --- | --- | --- |
| 0.50 | 0/26 | 8/8 |
| 0.52 | 0/26 | 8/8 |
| 0.54 | 0/26 | 8/8 |
| 0.56 | 0/26 | 8/8 |
| 0.58 | 0/26 | 8/8 |
| 0.60 | 0/26 | 8/8 |
| 0.62 | 0/26 | 8/8 |
| 0.64 | 2/26 | 8/8 |
| 0.66 | 2/26 | 8/8 |
| 0.68 | 2/26 | 8/8 |
| 0.70 | 2/26 | 8/8 |
| 0.72 | 4/26 | 8/8 |
| 0.74 | 5/26 | 8/8 |
| 0.76 | 6/26 | 8/8 |
| 0.78 | 12/26 | 8/8 |
| 0.80 | 13/26 | 8/8 |

## Rerank threshold sweep

Only questions that passed the similarity checks reach the reranker, so only those are counted here.

| Rerank threshold | False refusals (in corpus) | Refusals (out of corpus) |
| --- | --- | --- |
| -4.0 | 0/26 | 0/0 |
| -3.5 | 0/26 | 0/0 |
| -3.0 | 0/26 | 0/0 |
| -2.5 | 0/26 | 0/0 |
| -2.0 | 0/26 | 0/0 |
| -1.5 | 0/26 | 0/0 |
| -1.0 | 1/26 | 0/0 |
| -0.5 | 2/26 | 0/0 |
| 0.0 | 2/26 | 0/0 |
| 0.5 | 2/26 | 0/0 |
| 1.0 | 2/26 | 0/0 |
| 1.5 | 2/26 | 0/0 |
| 2.0 | 2/26 | 0/0 |
| 2.5 | 4/26 | 0/0 |
| 3.0 | 6/26 | 0/0 |
| 3.5 | 7/26 | 0/0 |
| 4.0 | 9/26 | 0/0 |

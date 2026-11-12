# Evaluation run: core-baseline

- Questions: `eval/questions.json`
- Collection: `core-fixed`
- Answer mode: extractive
- Implementation: plain Python
- Search: exact
- Reranker: off
- Embedding model: BAAI/bge-small-en-v1.5
- Refusal threshold: 0.5
- Strict threshold for questions with a word found nowhere in the corpus: off
- Chunks in collection: 2740
- Run at: 2026-11-12T00:43:59+00:00

| Metric | Result |
| --- | --- |
| retrieval_hit@1 | 13/26 (50%) |
| retrieval_hit@3 | 21/26 (81%) |
| retrieval_hit@5 | 22/26 (85%) |
| citation_correct | 21/26 (81%) |
| top_citation_correct | 13/26 (50%) |
| false_refusals_in_corpus | 0/26 (0%) |
| refusals_out_of_corpus | 1/8 (12%) |

| Id | Question | Expected | Top score | Rerank score | Unknown words | Outcome | Cited |
| --- | --- | --- | --- | --- | --- | --- | --- |
| in-01 | What is the minimum length for a password that a user chooses themselves? | NIST.SP.800-63b.pdf p.24 | 0.775 | - | - | citation wrong | NIST.SP.800-63b.pdf p.79; NIST.SP.800-63b.pdf p.79; NIST.SP.800-114r1.pdf p.24 |
| in-02 | Should we force users to change their passwords on a regular schedule? | NIST.SP.800-63b.pdf p.25,65 | 0.810 | - | - | citation wrong | NIST.IR.7621r1.pdf p.38; NIST.IR.7621r1.pdf p.38; NIST.SP.800-114r1.pdf p.33 |
| in-03 | At authenticator assurance level 2, after how long without activity does a user have to sign in again? | NIST.SP.800-63b.pdf p.19,22 | 0.801 | - | - | citation correct | NIST.SP.800-63b.pdf p.22; NIST.SP.800-63b.pdf p.19; NIST.SP.800-63b.pdf p.64 |
| in-04 | What is the difference between a cold site, a warm site and a hot site? | nistspecialpublication800-34r1.pdf p.36,37,61,62 | 0.755 | - | - | citation correct | nistspecialpublication800-34r1.pdf p.36; nistspecialpublication800-34r1.pdf p.61; nistspecialpublication800-34r1.pdf p.61 |
| in-05 | What does recovery point objective mean? | nistspecialpublication800-34r1.pdf p.31,121,144 | 0.785 | - | - | citation correct | nistspecialpublication800-34r1.pdf p.121; nistspecialpublication800-34r1.pdf p.31; nistspecialpublication800-34r1.pdf p.144 |
| in-06 | What is a tabletop exercise? | nistspecialpublication800-34r1.pdf p.43 | 0.767 | - | - | citation correct | nistspecialpublication800-34r1.pdf p.43; nistspecialpublication800-34r1.pdf p.43; nistspecialpublication800-34r1.pdf p.85 |
| in-07 | What is the difference between clearing, purging and destroying media? | NIST.SP.800-88r1.pdf p.18 | 0.819 | - | - | citation correct | NIST.SP.800-88r1.pdf p.18; NIST.SP.800-88r1.pdf p.34; NIST.SP.800-88r1.pdf p.40 |
| in-08 | What record should be filled in after a drive has been sanitized? | NIST.SP.800-88r1.pdf p.31,32,65 | 0.763 | - | - | citation correct | NIST.SP.800-88r1.pdf p.44; NIST.SP.800-88r1.pdf p.32; NIST.SP.800-88r1.pdf p.44 |
| in-09 | What is the difference between a precursor and an indicator of an incident? | NIST.SP.800-61r2.pdf p.36 | 0.851 | - | - | citation correct | NIST.SP.800-61r2.pdf p.36; NIST.SP.800-61r2.pdf p.36; NIST.SP.800-61r2.pdf p.37 |
| in-10 | How soon after an incident should the lessons learned meeting take place? | NIST.SP.800-61r2.pdf p.48 | 0.849 | - | - | citation correct | NIST.SP.800-61r2.pdf p.48; NIST.SP.800-61r2.pdf p.13; NIST.SP.800-61r2.pdf p.49 |
| in-11 | What categories describe how much effort it takes to recover from an incident? | NIST.SP.800-61r2.pdf p.43 | 0.711 | - | - | citation correct | NIST.SP.800-61r2.pdf p.49; NIST.SP.800-61r2.pdf p.43; NIST.IR.7621r1.pdf p.48 |
| in-12 | What structures can an incident response team have? | NIST.SP.800-61r2.pdf p.23 | 0.851 | - | - | citation correct | NIST.SP.800-61r2.pdf p.23; NIST.SP.800-61r2.pdf p.75; NIST.SP.800-61r2.pdf p.56 |
| in-13 | What are the six functions of the Cybersecurity Framework? | NIST.CSWP.29.pdf p.8,31 | 0.805 | - | - | citation wrong | NIST.IR.7621r1.pdf p.48; NIST.CSWP.29.pdf p.9; NIST.IR.7621r1.pdf p.22 |
| in-14 | What are the four tiers called? | NIST.CSWP.29.pdf p.12,29,31 | 0.651 | - | - | citation correct | NIST.SP.800-46r2.pdf p.42; NIST.CSWP.29.pdf p.7; NIST.CSWP.29.pdf p.12 |
| in-15 | What are the main kinds of remote access methods for teleworkers? | NIST.SP.800-46r2.pdf p.14 | 0.820 | - | - | citation wrong | NIST.SP.800-114r1.pdf p.13; NIST.SP.800-46r2.pdf p.12; NIST.SP.800-114r1.pdf p.13 |
| in-16 | How can we find out whether an employee's phone has been jailbroken? | NIST.SP.800-46r2.pdf p.27,35 | 0.663 | - | - | citation wrong | NIST.SP.800-114r1.pdf p.36; NIST.SP.800-88r1.pdf p.37; NIST.SP.800-88r1.pdf p.38 |
| in-17 | What should we do about systems that cannot be patched? | NIST.SP.800-40r4.pdf p.19,22,23 | 0.752 | - | - | citation correct | NIST.SP.800-40r4.pdf p.16; NIST.SP.800-40r4.pdf p.19; NIST.SP.800-40r4.pdf p.25 |
| in-18 | How does emergency patching differ from routine patching? | NIST.SP.800-40r4.pdf p.18,19,22 | 0.819 | - | - | citation correct | NIST.SP.800-40r4.pdf p.18; NIST.SP.800-40r4.pdf p.22; NIST.SP.800-40r4.pdf p.19 |
| in-19 | What is the difference between security awareness and security training? | nistspecialpublication800-50.pdf p.20,21 | 0.860 | - | - | citation correct | nistspecialpublication800-50.pdf p.21; nistspecialpublication800-50.pdf p.19; NIST.SP.800-12r1.pdf p.70 |
| in-20 | What models are there for organizing a security awareness and training program? | nistspecialpublication800-50.pdf p.11,23,24 | 0.800 | - | - | citation correct | nistspecialpublication800-50.pdf p.19; nistspecialpublication800-50.pdf p.23; nistspecialpublication800-50.pdf p.19 |
| in-21 | What is a keystroke logger? | NIST.SP.800-83r1.pdf p.15 | 0.741 | - | - | citation correct | NIST.SP.800-12r1.pdf p.91; NIST.SP.800-63b.pdf p.53; NIST.SP.800-83r1.pdf p.15 |
| in-22 | What is sandboxing and how does it limit malware? | NIST.SP.800-83r1.pdf p.9,26 | 0.797 | - | - | citation correct | NIST.SP.800-83r1.pdf p.26; NIST.SP.800-83r1.pdf p.26; NIST.SP.800-83r1.pdf p.9 |
| in-23 | How often should a small business make a full backup of its data? | NIST.IR.7621r1.pdf p.32 | 0.823 | - | - | citation correct | NIST.IR.7621r1.pdf p.33; NIST.IR.7621r1.pdf p.32; NIST.IR.7621r1.pdf p.33 |
| in-24 | Why should a small business install an uninterruptible power supply? | NIST.IR.7621r1.pdf p.25 | 0.765 | - | - | citation correct | nistspecialpublication800-34r1.pdf p.60; NIST.IR.7621r1.pdf p.25; NIST.IR.7621r1.pdf p.43 |
| in-25 | Is it safe to check work email from a hotel kiosk computer? | NIST.SP.800-114r1.pdf p.10,37 | 0.720 | - | - | citation correct | NIST.SP.800-114r1.pdf p.10; NIST.SP.800-12r1.pdf p.39; NIST.SP.800-114r1.pdf p.37 |
| in-26 | What are the three basic types of information security policy? | NIST.SP.800-12r1.pdf p.36 | 0.766 | - | - | citation correct | NIST.SP.800-12r1.pdf p.36; NIST.SP.800-12r1.pdf p.36; NIST.IR.7621r1.pdf p.54 |
| out-01 | What is the refund policy for annual subscriptions? | not in corpus | 0.622 | - | - | answered (wrong) | NIST.SP.800-63b.pdf p.8; NIST.SP.800-63b.pdf p.3; NIST.SP.800-63b.pdf p.47 |
| out-02 | What is the capital of Australia? | not in corpus | 0.484 | - | - | refused by similarity check (right) | none |
| out-03 | How do I descale an espresso machine? | not in corpus | 0.601 | - | - | answered (wrong) | NIST.SP.800-88r1.pdf p.49; NIST.SP.800-88r1.pdf p.42; NIST.SP.800-88r1.pdf p.48 |
| out-04 | What are the maximum fines under GDPR for a data breach? | not in corpus | 0.670 | - | - | answered (wrong) | NIST.SP.800-63b.pdf p.47; NIST.SP.800-63b.pdf p.21; NIST.IR.7621r1.pdf p.49 |
| out-05 | How much does ISO 27001 certification cost? | not in corpus | 0.631 | - | - | answered (wrong) | NIST.IR.7621r1.pdf p.49; NIST.SP.800-12r1.pdf p.68; nistspecialpublication800-50.pdf p.61 |
| out-06 | What caused the 2017 Equifax breach? | not in corpus | 0.645 | - | - | answered (wrong) | NIST.SP.800-12r1.pdf p.7; NIST.SP.800-61r2.pdf p.1; NIST.IR.7621r1.pdf p.35 |
| out-07 | Which encryption protocol does WhatsApp use for its messages? | not in corpus | 0.672 | - | - | answered (wrong) | NIST.IR.7621r1.pdf p.28; NIST.SP.800-12r1.pdf p.67; NIST.SP.800-46r2.pdf p.36 |
| out-08 | How do I configure single sign-on for Salesforce with Okta? | not in corpus | 0.661 | - | - | answered (wrong) | NIST.SP.800-63b.pdf p.13; NIST.SP.800-63b.pdf p.66; NIST.SP.800-63b.pdf p.18 |

## Threshold sweep

| Threshold | False refusals (in corpus) | Refusals (out of corpus) |
| --- | --- | --- |
| 0.50 | 0/26 | 1/8 |
| 0.52 | 0/26 | 1/8 |
| 0.54 | 0/26 | 1/8 |
| 0.56 | 0/26 | 1/8 |
| 0.58 | 0/26 | 1/8 |
| 0.60 | 0/26 | 1/8 |
| 0.62 | 0/26 | 2/8 |
| 0.64 | 0/26 | 4/8 |
| 0.66 | 1/26 | 5/8 |
| 0.68 | 2/26 | 8/8 |
| 0.70 | 2/26 | 8/8 |
| 0.72 | 3/26 | 8/8 |
| 0.74 | 4/26 | 8/8 |
| 0.76 | 7/26 | 8/8 |
| 0.78 | 12/26 | 8/8 |
| 0.80 | 14/26 | 8/8 |

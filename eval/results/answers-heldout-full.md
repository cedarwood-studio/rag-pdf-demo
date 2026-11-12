# Answer-quality run: answers-heldout-full

- Implementation: plain Python
- Questions: `eval/questions-heldout.json`
- Collection: `full`
- Answer mode: generated
- Answer and grading model: openai/gpt-4o-mini at https://openrouter.ai/api/v1
- Embedding model: BAAI/bge-small-en-v1.5
- Reranker: off
- Estimated spend: $0.0029 (15936 input and 783 output tokens, 24 calls)
- Run at: 2026-11-12T01:36:49+00:00

| Metric | Result |
| --- | --- |
| answer_correct | 6/6 (100%) |
| answer_partial | 0/6 (0%) |
| answer_incorrect | 0/6 (0%) |
| false_refusals_in_corpus | 0/6 (0%) |
| citation_correct | 5/6 (83%) |
| faithful_of_answered | 6/6 (100%) |
| partly_faithful_of_answered | 0/6 (0%) |
| unfaithful_of_answered | 0/6 (0%) |
| refusals_out_of_corpus | 6/6 (100%) |
| refused_by_model_out_of_corpus | 6/6 (100%) |

| Id | Question | Outcome | Correctness | Faithfulness | Cited | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| held-in-01 | What is a rootkit? | answered | correct | supported | NIST.SP.800-83r1.pdf p.15; NIST.SP.800-83r1.pdf p.44 | A rootkit is a collection of files that is installed on a host to alter its standard functionality in a malicious and stealthy way. It typically makes many changes to a host to hide its existence, making it very difficult to determine that the rootkit is present and to identify what it has changed [ |
| held-in-02 | What is a blended attack? | answered | correct | supported | NIST.SP.800-83r1.pdf p.14 | A blended attack uses multiple infection or transmission methods, combining the propagation methods of viruses and worms. Many instances of malware today are considered blended attacks, which often rely on social engineering to trick individuals into revealing sensitive information or executing mali |
| held-in-03 | What does maximum tolerable downtime mean? | answered | correct | supported | nistspecialpublication800-34r1.pdf p.121 | Maximum Tolerable Downtime (MTD) represents the total amount of time leaders/managers are willing to accept for a mission/business process outage or disruption, including all impact considerations. Determining MTD is important for selecting appropriate recovery methods and developing recovery proced |
| held-in-04 | What is the difference between an event and an incident? | answered | correct | supported | NIST.SP.800-61r2.pdf p.16 | An event is any observable occurrence in a system or network, such as a user connecting to a file share or a server receiving a request for a web page. An incident, on the other hand, is a violation or imminent threat of violation of computer security policies, acceptable use policies, or standard s |
| held-in-05 | How long does the salt need to be when password hashes are stored? | answered | correct | supported | NIST.SP.800-63b.pdf p.27 | The salt value SHALL be at least 32 bits in length when storing password hashes for look-up secrets with fewer than 112 bits of entropy [3]. |
| held-in-06 | How frequently should incremental backups run in a small business? | answered | correct | supported | NIST.IR.7621r1.pdf p.33 | Incremental backups in a small business should be conducted at least once a week, but it may be prudent to conduct them every day or every hour depending on how much information is changed or generated and the potential impact of losing that information [1]. |
| held-out-01 | Which antivirus product is the best choice for a small business? | refused by model | - | - | none | I could not find this in the documents. |
| held-out-02 | How much does a hot site cost per month? | refused by model | - | - | none | I could not find this in the documents. |
| held-out-03 | Who is the current director of NIST? | refused by model | - | - | none | I could not find this in the documents. |
| held-out-04 | What is the penalty for failing to report an incident within 72 hours? | refused by model | - | - | none | I could not find this in the documents. |
| held-out-05 | How many people work on the incident response team at NIST? | refused by model | - | - | none | I could not find this in the documents. |
| held-out-06 | What password does the default administrator account use? | refused by model | - | - | none | I could not find this in the documents. |

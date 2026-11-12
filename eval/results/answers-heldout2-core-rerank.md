# Answer-quality run: answers-heldout2-core-rerank

- Implementation: plain Python
- Questions: `eval/questions-heldout2.json`
- Collection: `core`
- Answer mode: generated
- Answer and grading model: openai/gpt-4o-mini at https://openrouter.ai/api/v1
- Embedding model: BAAI/bge-small-en-v1.5
- Reranker: Xenova/ms-marco-MiniLM-L-6-v2, pool 10, threshold -1.5
- Estimated spend: $0.0042 (23030 input and 1307 output tokens, 36 calls)
- Run at: 2026-11-12T01:46:41+00:00

| Metric | Result |
| --- | --- |
| answer_correct | 9/10 (90%) |
| answer_partial | 1/10 (10%) |
| answer_incorrect | 0/10 (0%) |
| false_refusals_in_corpus | 0/10 (0%) |
| citation_correct | 9/10 (90%) |
| faithful_of_answered | 10/11 (91%) |
| partly_faithful_of_answered | 1/11 (9%) |
| unfaithful_of_answered | 0/11 (0%) |
| refusals_out_of_corpus | 11/12 (92%) |
| refused_by_model_out_of_corpus | 4/12 (33%) |

| Id | Question | Outcome | Correctness | Faithfulness | Cited | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| held2-in-01 | What is an attrition attack? | answered | correct | supported | NIST.SP.800-61r2.pdf p.12; NIST.SP.800-61r2.pdf p.35 | An attrition attack is an attack that employs brute force methods to compromise, degrade, or destroy systems, networks, or services, such as a DDoS intended to impair or deny access to a service or application, or a brute force attack against an authentication mechanism like passwords or CAPTCHAS [1 |
| held2-in-02 | What is a portal in a remote access setup? | answered | correct | supported | NIST.SP.800-46r2.pdf p.17; NIST.SP.800-46r2.pdf p.17 | A portal in a remote access setup is a server that offers access to one or more applications through a single centralized interface, allowing teleworkers to use a portal client on their devices to access the portal. Most portals are web-based, and they provide security features such as authenticatio |
| held2-in-03 | What are the steps in the life cycle of a security awareness and training program? | answered | correct | partial | nistspecialpublication800-50.pdf p.11; nistspecialpublication800-50.pdf p.23; nistspecialpublication800-50.pdf p.43; nistspecialpublication800-50.pdf p.11 | The steps in the life cycle of a security awareness and training program include: 1) Awareness and Training Program Design, which involves conducting a needs assessment and developing a training strategy; 2) Awareness and Training Material Development, focusing on the development of training materia |
| held2-in-04 | What types of compiled viruses are there? | answered | correct | supported | NIST.SP.800-83r1.pdf p.13 | The types of compiled viruses include file infector viruses, boot sector viruses, and multipartite viruses [1]. |
| held2-in-05 | What should a small business do when an employee leaves? | answered | correct | supported | NIST.IR.7621r1.pdf p.25 | When an employee leaves the business, the small business should ensure they no longer have access to the business’s information or systems. This includes collecting their business ID, deleting their username and account from all systems, changing any group passwords or combination locks they may hav |
| held2-in-06 | What does an Organizational Profile describe? | answered | correct | supported | NIST.CSWP.29.pdf p.11 | An Organizational Profile describes an organization’s current and/or target cybersecurity posture in terms of the Core’s outcomes, helping to understand, tailor, assess, prioritize, and communicate those outcomes based on the organization’s mission objectives, stakeholder expectations, threat landsc |
| held2-in-07 | How long a password should a system let users choose? | answered | partial | supported | NIST.SP.800-63b.pdf p.79 | A system should encourage users to make their passwords as lengthy as they want, within reason, as there is no reason not to permit the use of lengthy passwords or passphrases if the user wishes [4]. However, extremely long passwords could require excessive processing time to hash, so it is reasonab |
| held2-in-08 | How often should staff with contingency plan roles be trained? | answered | correct | supported | nistspecialpublication800-34r1.pdf p.42 | Staff with contingency plan roles should be trained at least annually. Additionally, personnel newly appointed to ISCP roles should receive training shortly after their appointment [1]. |
| held2-in-09 | Which wireless security option is preferred for a home network? | answered | correct | supported | NIST.SP.800-114r1.pdf p.21 | The preferred wireless security option for a home network is WPA2 with AES, followed by WPA with AES, and then WPA with TKIP. Wired Equivalent Privacy (WEP) is not recommended due to its serious flaws [1]. |
| held2-in-10 | How many security control baselines are there and what do they correspond to? | answered | correct | supported | NIST.SP.800-12r1.pdf p.53 | There are three security control baselines, which correspond to low-impact, moderate-impact, and high-impact systems [1]. |
| held2-out-01 | Which mobile device management product should we buy? | refused by model | - | - | none | I could not find this in the documents. |
| held2-out-02 | How much does an uninterruptible power supply cost for a small office? | refused by rerank check | - | - | none | I could not find this in the documents. |
| held2-out-03 | What is the email address of the incident response team? | refused by model | - | - | none | I could not find this in the documents. |
| held2-out-04 | Which company makes the most reliable degausser? | refused by similarity check | - | - | none | I could not find this in the documents. |
| held2-out-05 | What salary does an incident response team manager earn? | refused by model | - | - | none | I could not find this in the documents. |
| held2-out-06 | Which VPN vendor has had the fewest vulnerabilities? | refused by unknown word check | - | - | none | I could not find this in the documents. |
| held2-out-07 | Which training vendor offers the cheapest security awareness course? | refused by unknown word check | - | - | none | I could not find this in the documents. |
| held2-out-08 | On what date will the incident handling guide be withdrawn? | answered | - | supported | NIST.SP.800-61r2.pdf p.1 | The incident handling guide will be withdrawn on April 3, 2025 [1]. |
| held2-out-09 | Which cloud provider is approved for storing our backups? | refused by model | - | - | none | I could not find this in the documents. |
| held2-out-10 | How many passwords were stolen in the largest breach on record? | refused by rerank check | - | - | none | I could not find this in the documents. |
| held2-out-11 | What is the boiling point of water at sea level? | refused by similarity check | - | - | none | I could not find this in the documents. |
| held2-out-12 | Who won the football World Cup in 2018? | refused by similarity check | - | - | none | I could not find this in the documents. |

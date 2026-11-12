# Answer-quality run: answers-full

- Implementation: plain Python
- Questions: `eval/questions.json`
- Collection: `full`
- Answer mode: generated
- Answer and grading model: openai/gpt-4o-mini at https://openrouter.ai/api/v1
- Embedding model: BAAI/bge-small-en-v1.5
- Reranker: off
- Estimated spend: $0.0091 (48812 input and 2979 output tokens, 76 calls)
- Run at: 2026-11-12T01:35:37+00:00

| Metric | Result |
| --- | --- |
| answer_correct | 16/26 (62%) |
| answer_partial | 7/26 (27%) |
| answer_incorrect | 0/26 (0%) |
| false_refusals_in_corpus | 3/26 (12%) |
| citation_correct | 20/26 (77%) |
| faithful_of_answered | 17/23 (74%) |
| partly_faithful_of_answered | 6/23 (26%) |
| unfaithful_of_answered | 0/23 (0%) |
| refusals_out_of_corpus | 8/8 (100%) |
| refused_by_model_out_of_corpus | 4/8 (50%) |

| Id | Question | Outcome | Correctness | Faithfulness | Cited | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| in-01 | What is the minimum length for a password that a user chooses themselves? | answered | correct | supported | NIST.SP.800-114r1.pdf p.24 | The minimum length for a password that a user chooses themselves is at least eight characters long [1]. |
| in-02 | Should we force users to change their passwords on a regular schedule? | answered | partial | partial | NIST.SP.800-114r1.pdf p.25; NIST.SP.800-63b.pdf p.65 | The documents suggest that users should change their passwords regularly, based on the interval specified in their organizations’ password policies, especially to protect against unauthorized access if a password is revealed or compromised [2]. However, it is also noted that requiring periodic chang |
| in-03 | At authenticator assurance level 2, after how long without activity does a user have to sign in again? | answered | partial | supported | NIST.SP.800-63b.pdf p.19 | At authenticator assurance level 2, a user has to sign in again after a period of inactivity lasting 30 minutes or longer [1]. |
| in-04 | What is the difference between a cold site, a warm site and a hot site? | answered | correct | supported | nistspecialpublication800-34r1.pdf p.36; nistspecialpublication800-34r1.pdf p.61; nistspecialpublication800-34r1.pdf p.61; nistspecialpublication800-34r1.pdf p.36; nistspecialpublication800-34r1.pdf p.61 | A cold site is a facility with basic infrastructure to support recovery activities but lacks equipment and data, making it the least expensive option. A warm site has some equipment and telecommunications in place but may not have all necessary software or data loaded, allowing for quicker recovery  |
| in-05 | What does recovery point objective mean? | answered | correct | supported | nistspecialpublication800-34r1.pdf p.31 | The Recovery Point Objective (RPO) represents the point in time, prior to a disruption or system outage, to which mission/business process data can be recovered [2]. |
| in-06 | What is a tabletop exercise? | answered | partial | partial | nistspecialpublication800-84.pdf p.25; nistspecialpublication800-84.pdf p.21; nistspecialpublication800-84.pdf p.45 | A tabletop exercise is a discussion-based event where personnel with roles and responsibilities in a particular IT plan meet in a classroom setting or breakout groups to discuss their roles and responses to an emergency situation. These exercises are conducted in an informal environment, guided by a |
| in-07 | What is the difference between clearing, purging and destroying media? | answered | correct | partial | nistspecialpublication800-115.pdf p.61; NIST.SP.800-88r1.pdf p.18; nistspecialpublication800-115.pdf p.61 | Clearing applies logical techniques to sanitize data, making it resistant to simple non-invasive recovery methods, while purging uses physical or logical techniques to render data recovery infeasible using state-of-the-art laboratory techniques. Destruction goes further by physically obliterating th |
| in-08 | What record should be filled in after a drive has been sanitized? | refused by model | - | - | none | I could not find this in the documents. |
| in-09 | What is the difference between a precursor and an indicator of an incident? | answered | correct | supported | NIST.SP.800-61r2.pdf p.36 | A precursor is a sign that an incident may occur in the future, while an indicator is a sign that an incident may have occurred or may be occurring now. Most attacks do not have identifiable precursors, but indicators are more common and can include various signs of malicious activity [1]. |
| in-10 | How soon after an incident should the lessons learned meeting take place? | answered | correct | supported | NIST.SP.800-61r2.pdf p.48 | The lessons learned meeting should be held within several days of the end of the incident [1]. |
| in-11 | What categories describe how much effort it takes to recover from an incident? | answered | correct | supported | NIST.SP.800-61r2.pdf p.43 | The categories that describe the effort required to recover from an incident are: Regular, where recovery time is predictable with existing resources; Supplemented, where recovery time is predictable with additional resources; Extended, where recovery time is unpredictable and requires additional re |
| in-12 | What structures can an incident response team have? | answered | correct | supported | NIST.SP.800-61r2.pdf p.23 | An incident response team can have several structures, including a Central Incident Response Team, which handles incidents throughout the organization; Distributed Incident Response Teams, where multiple teams are responsible for different segments of the organization; and a Coordinating Team, which |
| in-13 | What are the six functions of the Cybersecurity Framework? | refused by model | - | - | none | I could not find this in the documents. |
| in-14 | What are the four tiers called? | answered | correct | supported | NIST.CSWP.29.pdf p.12 | The four tiers are called Partial (Tier 1), Risk Informed (Tier 2), Repeatable (Tier 3), and Adaptive (Tier 4) [4]. |
| in-15 | What are the main kinds of remote access methods for teleworkers? | answered | partial | supported | NIST.SP.800-46r2.pdf p.14; NIST.SP.800-114r1.pdf p.13 | The main kinds of remote access methods for teleworkers include virtual private networks (VPNs), tunneling, portals, remote desktop access, and direct application access [3][4]. |
| in-16 | How can we find out whether an employee's phone has been jailbroken? | refused by model | - | - | none | I could not find this in the documents. |
| in-17 | What should we do about systems that cannot be patched? | answered | partial | partial | NIST.SP.800-171r3.pdf p.81; NIST.SP.800-171r3.pdf p.80 | For systems that cannot be patched, organizations should consider replacing the unsupported components when support is no longer available. If replacement is not an option, they can explore risk mitigation strategies or alternative sources for continued support, such as developing in-house support o |
| in-18 | How does emergency patching differ from routine patching? | answered | partial | supported | NIST.SP.800-40r4.pdf p.22; NIST.SP.800-40r4.pdf p.19; NIST.SP.800-40r4.pdf p.18 | Emergency patching differs from routine patching in that it is conducted under a highly accelerated schedule in response to a crisis, such as a severe vulnerability or active exploitation, whereas routine patching follows a standard release cycle without the same urgency. Additionally, emergency pat |
| in-19 | What is the difference between security awareness and security training? | answered | partial | partial | nistspecialpublication800-50.pdf p.21; nistspecialpublication800-50.pdf p.20 | The difference between security awareness and security training is that awareness focuses on changing behavior and reinforcing good security practices by highlighting security issues, while training aims to teach specific skills and competencies necessary for performing certain functions related to  |
| in-20 | What models are there for organizing a security awareness and training program? | answered | correct | supported | nistspecialpublication800-50.pdf p.23 | There are three common models for organizing a security awareness and training program: Model 1 is a centralized policy, strategy, and implementation; Model 2 is a centralized policy and strategy with distributed implementation; and Model 3 is a centralized policy with distributed strategy and imple |
| in-21 | What is a keystroke logger? | answered | correct | partial | NIST.SP.800-12r1.pdf p.91; NIST.SP.800-83r1.pdf p.15 | A keystroke logger is a tool that monitors and records keyboard use, capturing the keystrokes entered by a computer user and the computer's response during an interactive session. Some keystroke loggers require the attacker to retrieve the data from the host, while others can actively transfer the d |
| in-22 | What is sandboxing and how does it limit malware? | answered | correct | supported | NIST.SP.800-83r1.pdf p.26; NIST.SP.800-83r1.pdf p.9; NIST.SP.800-83r1.pdf p.26 | Sandboxing is a security model where applications are run in a controlled environment that restricts their operations and isolates them from other applications on the same host. It limits malware by prohibiting unauthorized operations and restricting access to system resources, which can prevent mal |
| in-23 | How often should a small business make a full backup of its data? | answered | correct | supported | NIST.IR.7621r1.pdf p.32 | A small business should conduct a full, encrypted backup of the data on each computer and mobile device at least once a month, shortly after a complete virus scan [2]. |
| in-24 | Why should a small business install an uninterruptible power supply? | answered | correct | supported | NIST.IR.7621r1.pdf p.25; nistspecialpublication800-34r1.pdf p.60 | A small business should install an uninterruptible power supply (UPS) to provide a limited amount of battery power during short power outages, allowing time to save data and continue operations. Additionally, a UPS can protect against power fluctuations, ensuring that critical systems remain operati |
| in-25 | Is it safe to check work email from a hotel kiosk computer? | answered | correct | supported | NIST.SP.800-114r1.pdf p.10 | It is not safe to check work email from a hotel kiosk computer, as teleworkers typically do not know if such devices have been secured properly or if they have been compromised, which could lead to the use of a device infected with malware that steals sensitive information [1]. |
| in-26 | What are the three basic types of information security policy? | answered | correct | supported | NIST.SP.800-12r1.pdf p.36; nistspecialpublication800-35.pdf p.45 | The three basic types of information security policy are Program Policy, Issue-Specific Policy, and System-Specific Policy [1][2]. |
| out-01 | What is the refund policy for annual subscriptions? | refused by model | - | - | none | I could not find this in the documents. |
| out-02 | What is the capital of Australia? | refused by similarity check | - | - | none | I could not find this in the documents. |
| out-03 | How do I descale an espresso machine? | refused by similarity check | - | - | none | I could not find this in the documents. |
| out-04 | What are the maximum fines under GDPR for a data breach? | refused by model | - | - | none | I could not find this in the documents. |
| out-05 | How much does ISO 27001 certification cost? | refused by model | - | - | none | I could not find this in the documents. |
| out-06 | What caused the 2017 Equifax breach? | refused by unknown word check | - | - | none | I could not find this in the documents. |
| out-07 | Which encryption protocol does WhatsApp use for its messages? | refused by model | - | - | none | I could not find this in the documents. |
| out-08 | How do I configure single sign-on for Salesforce with Okta? | refused by unknown word check | - | - | none | I could not find this in the documents. |

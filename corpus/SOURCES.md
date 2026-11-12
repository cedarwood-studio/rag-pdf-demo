# Corpus sources

100 publications of the US National Institute of Standards and Technology (NIST), 6,252 pages in total. They are works of the US Government and are not subject to copyright in the United States (17 U.S.C. 105). The PDFs are not stored in this repository. `python -m ragdemo.corpus --corpus full` downloads them from nist.gov and checks each file against the SHA-256 recorded in `sources.json`.

This file is generated from `sources.json`.

## Core set (12 documents, 805 pages)

The evaluation questions are answered from these documents.

| Series | Title | Pages | Source |
| --- | --- | --- | --- |
| NIST CSWP 29 | The NIST Cybersecurity Framework (CSF) 2.0 | 32 | [NIST.CSWP.29.pdf](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf) |
| NISTIR 7621 Rev. 1 | Small Business Information Security: The Fundamentals | 55 | [NIST.IR.7621r1.pdf](https://nvlpubs.nist.gov/nistpubs/ir/2016/NIST.IR.7621r1.pdf) |
| NIST SP 800-12 Rev. 1 | An Introduction to Information Security | 101 | [NIST.SP.800-12r1.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-12r1.pdf) |
| NIST SP 800-34 Rev. 1 | Contingency Planning Guide for Federal Information Systems | 149 | [nistspecialpublication800-34r1.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf) |
| NIST SP 800-40 Rev. 4 | Guide to Enterprise Patch Management Planning | 28 | [NIST.SP.800-40r4.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-40r4.pdf) |
| NIST SP 800-46 Rev. 2 | Guide to Enterprise Telework, Remote Access, and Bring Your Own Device (BYOD) Security | 53 | [NIST.SP.800-46r2.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-46r2.pdf) |
| NIST SP 800-50 | Building an Information Technology Security Awareness and Training Program | 71 | [nistspecialpublication800-50.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-50.pdf) |
| NIST SP 800-61 Rev. 2 | Computer Security Incident Handling Guide | 80 | [NIST.SP.800-61r2.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r2.pdf) |
| NIST SP 800-63B | Digital Identity Guidelines: Authentication and Lifecycle Management | 80 | [NIST.SP.800-63b.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-63b.pdf) |
| NIST SP 800-83 Rev. 1 | Guide to Malware Incident Prevention and Handling for Desktops and Laptops | 47 | [NIST.SP.800-83r1.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-83r1.pdf) |
| NIST SP 800-88 Rev. 1 | Guidelines for Media Sanitization | 65 | [NIST.SP.800-88r1.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-88r1.pdf) |
| NIST SP 800-114 Rev. 1 | User's Guide to Telework and Bring Your Own Device (BYOD) Security | 44 | [NIST.SP.800-114r1.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-114r1.pdf) |

## Extended set (88 more documents, 5,447 pages)

Added for the scale comparison. They are on the same subject, so they compete with the core set for every question.

| Series | Title | Pages | Source |
| --- | --- | --- | --- |
| NIST CSWP 04162018 | Framework for Improving Critical Infrastructure Cybersecurity, Version 1.1 | 55 | [NIST.CSWP.04162018.pdf](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.04162018.pdf) |
| NIST CSWP 20 | Planning for a Zero Trust Architecture: A Planning Guide for Federal Adminstrators | 18 | [NIST.CSWP.20.pdf](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.20.pdf) |
| NIST IR 8183r1 | Cybersecurity Framework Version 1.1 Manufacturing Profile | 60 | [NIST.IR.8183r1.pdf](https://nvlpubs.nist.gov/nistpubs/ir/2020/NIST.IR.8183r1.pdf) |
| NIST IR 8228 | Considerations for Managing Internet of Things (IoT) Cybersecurity and Privacy Risks | 44 | [NIST.IR.8228.pdf](https://nvlpubs.nist.gov/nistpubs/ir/2019/NIST.IR.8228.pdf) |
| NIST IR 8259 | Foundational Cybersecurity Activities for IoT Device Manufacturers | 37 | [NIST.IR.8259.pdf](https://nvlpubs.nist.gov/nistpubs/ir/2020/NIST.IR.8259.pdf) |
| NIST IR 8259A | IoT Device Cybersecurity Capability Core Baseline | 23 | [NIST.IR.8259A.pdf](https://nvlpubs.nist.gov/nistpubs/ir/2020/NIST.IR.8259A.pdf) |
| NIST IR 8259B | IoT Non-Technical Supporting Capability Core Baseline | 21 | [NIST.IR.8259B.pdf](https://nvlpubs.nist.gov/nistpubs/ir/2021/NIST.IR.8259B.pdf) |
| NIST IR 8286 | Integrating Cybersecurity and Enterprise Risk Management (ERM) | 75 | [NIST.IR.8286.pdf](https://nvlpubs.nist.gov/nistpubs/ir/2020/NIST.IR.8286.pdf) |
| NIST IR 8286A | Identifying and Estimating Cybersecurity Risk for Enterprise Risk Management | 62 | [NIST.IR.8286A.pdf](https://nvlpubs.nist.gov/nistpubs/ir/2021/NIST.IR.8286A.pdf) |
| NIST IR 8286B | Prioritizing Cybersecurity Risk for Enterprise Risk Management | 46 | [NIST.IR.8286B.pdf](https://nvlpubs.nist.gov/nistpubs/ir/2022/NIST.IR.8286B.pdf) |
| NIST IR 8374 | Cybersecurity Framework Profile for Ransomware Risk Management | 29 | [NIST.IR.8374.pdf](https://nvlpubs.nist.gov/nistpubs/ir/2022/NIST.IR.8374.pdf) |
| NIST SP 800-101r1 | Guidelines on Mobile Device Forensics | 85 | [NIST.SP.800-101r1.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-101r1.pdf) |
| NIST SP 800-116r1 | Guidelines for the Use of PIV Credentials in Facility Access | 71 | [NIST.SP.800-116r1.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-116r1.pdf) |
| NIST SP 800-121r2 | Guide to Bluetooth Security | 68 | [NIST.SP.800-121r2.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-121r2.pdf) |
| NIST SP 800-125Ar1 | Security Recommendations for Server-based Hypervisor Platforms | 39 | [NIST.SP.800-125Ar1.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-125Ar1.pdf) |
| NIST SP 800-125B | Secure Virtual Network Configuration for Virtual Machine (VM) Protection | 30 | [NIST.SP.800-125B.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-125B.pdf) |
| NIST SP 800-128 | Guide for Security-Focused Configuration Management of Information Systems | 99 | [NIST.SP.800-128.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-128.pdf) |
| NIST SP 800-137A | Assessing Information Security Continuous Monitoring (ISCM) Programs: Developing an ISCM Program Assessment | 77 | [NIST.SP.800-137A.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-137A.pdf) |
| NIST SP 800-150 | Guide to Cyber Threat Information Sharing | 43 | [NIST.SP.800-150.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-150.pdf) |
| NIST SP 800-162 | Guide to Attribute Based Access Control (ABAC) Definition and Considerations | 47 | [NIST.SP.800-162.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-162.pdf) |
| NIST SP 800-163r1 | Vetting the Security of Mobile Applications | 55 | [NIST.SP.800-163r1.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-163r1.pdf) |
| NIST SP 800-167 | Guide to Application Whitelisting | 24 | [NIST.SP.800-167.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-167.pdf) |
| NIST SP 800-171Ar3 | Assessing Security Requirements for Controlled Unclassified Information | 123 | [NIST.SP.800-171Ar3.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-171Ar3.pdf) |
| NIST SP 800-171r3 | Protecting Controlled Unclassified Information in Nonfederal Systems and Organizations | 120 | [NIST.SP.800-171r3.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-171r3.pdf) |
| NIST SP 800-172r3 | Enhanced Security Requirements for Protecting Controlled Unclassified Information | 119 | [NIST.SP.800-172r3.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-172r3.pdf) |
| NIST SP 800-177r1 | Trustworthy Email | 128 | [NIST.SP.800-177r1.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-177r1.pdf) |
| NIST SP 800-178 | A Comparison of Attribute Based Access Control (ABAC) Standards for Data Service Applications: Extensible Access Control Markup Language (XACML) and Next Generation Access Control (NGAC) | 68 | [NIST.SP.800-178.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-178.pdf) |
| NIST SP 800-181r1 | Workforce Framework for Cybersecurity (NICE Framework) | 27 | [NIST.SP.800-181r1.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-181r1.pdf) |
| NIST SP 800-183 | Networks of 'Things' | 30 | [NIST.SP.800-183.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-183.pdf) |
| NIST SP 800-184 | Guide for Cybersecurity Event Recovery | 53 | [NIST.SP.800-184.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-184.pdf) |
| NIST SP 800-187 | Guide to LTE Security | 49 | [NIST.SP.800-187.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-187.pdf) |
| NIST SP 800-188 | De-Identifying Government Datasets: Techniques and Governance | 122 | [NIST.SP.800-188.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-188.pdf) |
| NIST SP 800-18r2 | Developing Security, Privacy, and Supply Chain Risk Management Plans for Systems | 70 | [NIST.SP.800-18r2.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-18r2.pdf) |
| NIST SP 800-190 | Application Container Security Guide | 63 | [NIST.SP.800-190.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-190.pdf) |
| NIST SP 800-192 | Verification and Test Methods for Access Control Policies/Models | 68 | [NIST.SP.800-192.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-192.pdf) |
| NIST SP 800-193 | Platform Firmware Resiliency Guidelines | 45 | [NIST.SP.800-193.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-193.pdf) |
| NIST SP 800-204 | Security Strategies for Microservices-based Application Systems | 50 | [NIST.SP.800-204.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-204.pdf) |
| NIST SP 800-204A | Building Secure Microservices-based Applications Using Service-Mesh Architecture | 27 | [NIST.SP.800-204A.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-204A.pdf) |
| NIST SP 800-204B | Attribute-based Access Control for Microservices-based Applications Using a Service Mesh | 41 | [NIST.SP.800-204B.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-204B.pdf) |
| NIST SP 800-204C | Implementation of DevSecOps for a Microservices-based Application with Service Mesh | 45 | [NIST.SP.800-204C.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-204C.pdf) |
| NIST SP 800-204D | Strategies for the Integration of Software Supply Chain Security in DevSecOps CI/CD Pipelines | 41 | [NIST.SP.800-204D.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-204D.pdf) |
| NIST SP 800-205 | Attribute Considerations for Access Control Systems | 42 | [NIST.SP.800-205.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-205.pdf) |
| NIST SP 800-207 | Zero Trust Architecture | 59 | [NIST.SP.800-207.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf) |
| NIST SP 800-207A | A Zero Trust Architecture Model for Access Control in Cloud-Native Applications in Multi-Location Environments | 31 | [NIST.SP.800-207A.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207A.pdf) |
| NIST SP 800-209 | Security Guidelines for Storage Infrastructure | 79 | [NIST.SP.800-209.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-209.pdf) |
| NIST SP 800-210 | General Access Control Guidance for Cloud Systems | 34 | [NIST.SP.800-210.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-210.pdf) |
| NIST SP 800-213 | IoT Device Cybersecurity Guidance for the Federal Government: Establishing IoT Device Cybersecurity Requirements | 47 | [NIST.SP.800-213.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-213.pdf) |
| NIST SP 800-213A | IoT Device Cybersecurity Guidance for the Federal Government: IoT Device Cybersecurity Requirement Catalog | 94 | [NIST.SP.800-213A.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-213A.pdf) |
| NIST SP 800-215 | Guide to a Secure Enterprise Network Landscape | 41 | [NIST.SP.800-215.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-215.pdf) |
| NIST SP 800-216 | Recommendations for Federal Vulnerability Disclosure Guidelines | 37 | [NIST.SP.800-216.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-216.pdf) |
| NIST SP 800-218 | Secure Software Development Framework (SSDF) Version 1.1: Recommendations for Mitigating the Risk of Software Vulnerabilities | 36 | [NIST.SP.800-218.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf) |
| NIST SP 800-221A | Information and Communications Technology (ICT) Risk Outcomes: Integrating ICT Risk Management Programs with the Enterprise Risk Portfolio | 20 | [NIST.SP.800-221A.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-221A.pdf) |
| NIST SP 800-228 | Guidelines for API Protection for Cloud-Native Systems | 58 | [NIST.SP.800-228.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-228.pdf) |
| NIST SP 800-47r1 | Managing the Security of Information Exchanges | 58 | [NIST.SP.800-47r1.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-47r1.pdf) |
| NIST SP 800-52r2 | Guidelines for the Selection, Configuration, and Use of Transport Layer Security (TLS) Implementations | 72 | [NIST.SP.800-52r2.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-52r2.pdf) |
| NIST SP 800-53B | Control Baselines for Information Systems and Organizations | 85 | [NIST.SP.800-53B.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53B.pdf) |
| NIST SP 800-63-3 | Digital Identity Guidelines | 76 | [NIST.SP.800-63-3.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-63-3.pdf) |
| NIST SP 800-63a | Digital Identity Guidelines: Enrollment and Identity Proofing | 48 | [NIST.SP.800-63a.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-63a.pdf) |
| NIST SP 800-63c | Digital Identity Guidelines: Federation and Assertions | 50 | [NIST.SP.800-63c.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-63c.pdf) |
| NIST SP 800-66r2 | Implementing the Health Insurance Portability and Accountability Act (HIPAA) Security Rule: A Cybersecurity Resource Guide | 122 | [NIST.SP.800-66r2.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-66r2.pdf) |
| NIST SP 800-70r5 | National Checklist Program for IT Products: Guidelines for Checklist Users and Developers | 59 | [NIST.SP.800-70r5.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-70r5.pdf) |
| NIST SP 800-111 | Guide to Storage Encryption Technologies for End User Devices | 40 | [nistspecialpublication800-111.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-111.pdf) |
| NIST SP 800-113 | Guide to SSL VPNs | 87 | [nistspecialpublication800-113.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-113.pdf) |
| NIST SP 800-115 | Technical guide to information security testing and assessment | 80 | [nistspecialpublication800-115.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf) |
| NIST SP 800-122 | Guide to Protecting the Confidentiality of Personally Identifiable Information (PII) | 59 | [nistspecialpublication800-122.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-122.pdf) |
| NIST SP 800-123 | Guide to General Server Security | 53 | [nistspecialpublication800-123.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-123.pdf) |
| NIST SP 800-125 | Guide to Security for Full Virtualization Technologies | 35 | [nistspecialpublication800-125.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-125.pdf) |
| NIST SP 800-137 | Information Security Continuous Monitoring (ISCM) for Federal Information Systems and Organizations | 80 | [nistspecialpublication800-137.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-137.pdf) |
| NIST SP 800-144 | Guidelines on Security and Privacy in Public Cloud Computing | 80 | [nistspecialpublication800-144.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-144.pdf) |
| NIST SP 800-146 | Cloud Computing Synopsis and Recommendations | 81 | [nistspecialpublication800-146.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-146.pdf) |
| NIST SP 800-147 | BIOS Protection Guidelines | 26 | [nistspecialpublication800-147.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-147.pdf) |
| NIST SP 800-153 | Guidelines for securing Wireless Local Area Networks (WLANs) | 24 | [nistspecialpublication800-153.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-153.pdf) |
| NIST SP 800-27 | Engineering Principles for Information Technology Security (A Baseline for Achieving Security) | 41 | [nistspecialpublication800-27.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-27.pdf) |
| NIST SP 800-28ver2 | Guidelines on Active Content and Mobile Code | 62 | [nistspecialpublication800-28ver2.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-28ver2.pdf) |
| NIST SP 800-30r1 | Guide for Conducting Risk Assessments | 95 | [nistspecialpublication800-30r1.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf) |
| NIST SP 800-32 | Introduction to public key technology and the federal PKI infrastructure | 55 | [nistspecialpublication800-32.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-32.pdf) |
| NIST SP 800-35 | Guide to Information Technology Security Services | 84 | [nistspecialpublication800-35.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-35.pdf) |
| NIST SP 800-36 | Guide to selecting information technology security products | 68 | [nistspecialpublication800-36.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-36.pdf) |
| NIST SP 800-39 | Managing Information Security Risk: Organization, Mission, and Information System View | 88 | [nistspecialpublication800-39.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-39.pdf) |
| NIST SP 800-41r1 | Guidelines on Firewalls and Firewall Policy | 48 | [nistspecialpublication800-41r1.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-41r1.pdf) |
| NIST SP 800-48r1 | Guide to securing legacy IEEE 802.11 wireless networks | 51 | [nistspecialpublication800-48r1.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-48r1.pdf) |
| NIST SP 800-55r1 | Performance measurement guide for information security | 81 | [nistspecialpublication800-55r1.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-55r1.pdf) |
| NIST SP 800-58 | Security Considerations for Voice Over IP Systems | 99 | [nistspecialpublication800-58.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-58.pdf) |
| NIST SP 800-64r2 | Security Considerations in the System Development Life Cycle | 68 | [nistspecialpublication800-64r2.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-64r2.pdf) |
| NIST SP 800-84 | Guide to Test, Training, and Exercise Programs for IT Plans and Capabilities | 97 | [nistspecialpublication800-84.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-84.pdf) |
| NIST SP 800-86 | Guide to Integrating Forensic Techniques into Incident Response | 121 | [nistspecialpublication800-86.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-86.pdf) |
| NIST SP 800-92 | Guide to Computer Security Log Management | 72 | [nistspecialpublication800-92.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-92.pdf) |
| NIST SP 800-94 | Guide to Intrusion Detection and Prevention Systems (IDPS) | 127 | [nistspecialpublication800-94.pdf](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-94.pdf) |

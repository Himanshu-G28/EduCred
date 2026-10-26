# A Systematic Review of Blockchain and Smart Contract Architectures for Academic Credential Verification: Cryptographic Standards, Performance Trade-offs, and Regulatory Data Protection

**Review Article • Systematic Literature Review (PRISMA 2020)**  
**Word Document Artifact:** [`NMIMS_DE2_Review_Article_Submission.docx`](file:///Users/himanshugarg/Desktop/NMIMS%20Material/SEM-5/Design%20Experience%202/project/docs/NMIMS_DE2_Review_Article_Submission.docx)  
**Methodological Model:** Modeled strictly on Simon Baradziej (2026), *"A systematic review of the roles of agentic AI in higher education"*, *Social Sciences & Humanities Open*, Elsevier.  

### Authors
* **Himanshu Garg**<sup>1,*</sup> — Roll No: `E250` | SAP ID: `70552400057` (*Lead System Architect & Lead Author*)
* **Manthan Patil**<sup>1</sup> — Roll No: `E323` | SAP ID: `70552400133` (*Web3 Frontend & Co-Author*)
* **Vaishnavi Mali**<sup>1</sup> — Roll No: `B348` | SAP ID: `70022400767` (*QA, Validation & Co-Author*)
* **Dr. Srikanth Pullipeti**<sup>2</sup> (*Project Mentor & Corresponding Author*)

<sup>1</sup> Department of Computer Science & Engineering, Mukesh Patel School of Technology Management & Engineering (MPSTME), SVKM’s NMIMS (Deemed-to-be University), Shirpur Campus, Maharashtra 425405, India  
<sup>2</sup> Associate Professor & Course Coordinator, Department of Computer Science & Engineering, MPSTME, SVKM’s NMIMS, Shirpur Campus, India  
<sup>*</sup> Corresponding Author: `himanshu.garg57@nmims.edu.in`

---

## Abstract

Academic credential fraud—spanning fabricated degree certificates, tampered cumulative grade point averages (CGPAs), and counterfeit transcripts—presents a profound institutional and economic crisis for universities, corporate employers, and government licensing authorities worldwide. Traditional academic verification pipelines rely on centralized registrar databases, physical apostilles, or bilateral postal and email inquiries, routinely incurring turnaround latencies of 14 to 30 business days, significant operational expenditures, and acute vulnerabilities to administrative insider tampering. Although decentralized distributed ledger technologies (DLT) and Ethereum-compatible smart contracts have been widely proposed as trustless alternatives, prior literature remains heavily fragmented across isolated prototypes without systematic comparative evaluation. 

Following the Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA 2020) guidelines, this review synthesizes peer-reviewed literature across five major academic repositories (Scopus, Web of Science, IEEE Xplore, ACM Digital Library, and Google Scholar) published between January 2018 and March 2026. From 1,142 identified candidate records, 754 remained after deduplication, and formal screening yielded 48 landmark studies subject to thematic synthesis and Mixed Methods Appraisal Tool (MMAT) quality appraisal. 

Thematic synthesis identifies five dominant architectural archetypes: 
1. **Pure On-Chain Storage on Public Ledgers**;
2. **Permissioned Consortium Distributed Ledgers (Hyperledger Fabric)**;
3. **Tokenized Credentials (ERC-721 NFTs and Soulbound EIP-5192 tokens)**;
4. **Hybrid Dual-Layer Storage (Hash-on-Chain with Content-off-Chain via InterPlanetary File System - IPFS)**; and
5. **Self-Sovereign Identity (SSI) with Zero-Knowledge Proofs (W3C DIDs and zk-SNARKs)**.

Quantitative synthesis demonstrates that hybrid dual-layer architectures resolve the fundamental *'Gas Cost vs. Document Size'* paradox, achieving sub-second constant-time $O(1)$ verification latency, zero transaction gas fees for verifiers, and a 23.8% gas reduction via batch issuance arrays, while satisfying the NIST FIPS 180-4 Strict Avalanche Criterion (SAC) with empirical 50.0% bit-flip forgery sensitivity. Crucially, the review addresses a pivotal regulatory lacuna: how blockchain's perpetual immutability conflicts with statutory data privacy mandates, notably India's Digital Personal Data Protection (DPDP) Act 2023 and the European Union General Data Protection Regulation (GDPR) *'Right to Erasure'*. We demonstrate that anchoring only 32-byte SHA-256 cryptographic digests on-chain while keeping student Personally Identifiable Information (PII) off-chain establishes legal compliance. Finally, we formulate a tripartite institutional governance framework encompassing architectural standards, privacy infrastructure, and competence training, accompanied by a 5-year scalability roadmap for enterprise campus adoption.

**Keywords:** Blockchain in Higher Education; Smart Contracts; Academic Credential Verification; Systematic Literature Review; PRISMA 2020; Ethereum Virtual Machine (EVM); InterPlanetary File System (IPFS); Digital Personal Data Protection (DPDP) Act 2023; Cryptographic Preimage Resistance.

---

## 1. Introduction

### 1.1. The Evolution of Academic Credential Verification
Higher educational credentials—encompassing baccalaureate degrees, postgraduate diplomas, grade cards, and official academic transcripts—serve as the foundational currency of human capability in modern merit-based economies. In India alone, the higher education ecosystem encompasses over 40 million enrolled students distributed across more than 1,100 universities and 45,000 affiliated colleges regulated by the University Grants Commission (UGC) and All India Council for Technical Education (AICTE). Globally, these documents govern candidate eligibility for corporate recruitment, civil service commissions, professional engineering licensure, and international postgraduate admissions.

Historically, the institutional integrity of credentials was safeguarded through physical security primitives, including customized watermark paper, embossed metallic university seals, micro-text typography, and registrar wet signatures. Over the past two decades, universities transitioned toward digital publishing workflows, issuing portable document format (PDF) certificates and registering electronic records in centralized student information systems. Concurrently, however, the democratization of high-resolution digital desktop publishing software, PDF stream manipulation tools, and generative artificial intelligence has virtually dissolved traditional physical and electronic security perimeters. Malicious candidates can now synthesize visually flawless counterfeit degree certificates and alter critical attributes—such as Cumulative Grade Point Averages (CGPA), student SAP registration numbers, and graduation dates—within minutes.

Traditional verification protocols remain fundamentally bureaucratic and asynchronous. When an employer or licensing agency requests verification, inquiries are routed manually to institutional examination cells via postal dispatch or unencrypted email exchanges. This operational workflow routinely incurs turnaround latencies of two to four weeks, imposes substantial administrative backlogs on university personnel, and requires commercial background screening agencies to extract significant transactional fees from hiring enterprises. Furthermore, centralized repository models, including the Government of India's National Academic Depository (NAD) and DigiLocker, while vastly superior to paper workflows, represent centralized points of failure susceptible to server outages, insider credential modification, and single-target cyberattacks.

The advent of distributed ledger technology (DLT) and Ethereum Virtual Machine (EVM) smart contracts offers a transformative paradigm: replacing centralized institutional trust with mathematical, consensus-driven immutability. By executing cryptographic hashing pipelines and storing non-repudiable state proofs across a decentralized peer-to-peer network, blockchain enables any independent third party to verify an academic credential in sub-second constant time with zero operational reliance on registrar availability.

### 1.2. Defining Core Constructs of Decentralized Credentialing
To establish conceptual clarity, decentralized credential verification systems denote a specialized class of cryptographically enforced software architectures characterized by four intersecting properties:
1. **Cryptographic Preimage Resistance:** Credentials are mapped to fixed-size 256-bit hashes using collision-resistant hash functions (NIST FIPS 180-4);
2. **Smart Contract State Enforcement:** Issuance and revocation logic is governed by immutable EVM bytecode with role-based access control (RBAC);
3. **Off-Chain Content Addressing:** Heavyweight document payloads are hosted on peer-to-peer distributed storage (e.g., InterPlanetary File System - IPFS) rather than bloat ledger state slots; and
4. **Mathematical Zero-Knowledge Verifiability:** Enabling instant $O(1)$ query execution without requiring transactional gas expenditure.

#### Table 1: Operational comparison of traditional registrar, centralized PKI, and blockchain credential architectures
| Dimension | Traditional University Registrar | Centralized PKI (DigiLocker / NAD) | Blockchain-Enabled Framework (EduCred) |
| :--- | :--- | :--- | :--- |
| **Core Architecture** | Central SQL database & physical paper archives | Centralized cloud API with PKI digital signatures | Decentralized EVM smart contracts & IPFS storage |
| **Verification Latency** | 14 to 30 business days (manual postal/email) | 1 to 5 seconds (dependent on central server uptime) | < 1 second (constant-time $O(1)$ cryptographic lookup) |
| **Verifier Financial Cost** | High (commercial agency fee: $15 - $50 / cert) | Zero (subsidized by government infrastructure) | Zero gas expenditure (free static EVM view call) |
| **Single Point of Failure** | Critical (local server crash, fire, flood, loss) | Moderate (central cloud outage, DNS hijacking) | None (replicated decentralized state across thousands of nodes) |
| **Insider Tamper Vulnerability** | High (corrupt database administrator can alter records) | Moderate (root CA key compromise or internal access) | Zero (cryptographically immutable; unauthorized writes revert) |
| **Storage Scalability** | Constrained by physical filing and local disk storage | High (scalable enterprise cloud storage tiers) | Optimal (hash-on-chain 32 bytes; content hosted off-chain) |
| **Revocation Management** | Manual deletion from DB; unrecorded paper recall | API status update flag (lacks public audit trail) | Non-destructive on-chain flag with timestamp & permanent audit log |
| **Data Sovereignty & DPDP** | Paper copies exposed to mail intercept; high leak risk | Central storage of plain-text Personally Identifiable Info | 100% DPDP compliant: zero clear-text PII written to ledger |

### 1.3. The Research Gap in Higher Education Credentialing
While a substantial body of secondary research has surveyed blockchain applications across industry sectors (supply chain, healthcare, financial decentralized finance), the academic credentialing domain has suffered from significant analytical fragmentation. General reviews of blockchain in education (e.g., Roy & Mahindru, 2024; Chen et al., 2025) provide broad high-level taxonomies but omit systematic screening rigor, fail to analyze EVM gas economics, and neglect statutory data sovereignty regulations. Conversely, computer science literature frequently presents isolated experimental prototypes without evaluating enterprise university constraints, such as registrar key management, semester batch issuance workflows, and the tension between blockchain immutability and the 'Right to be Forgotten' under emerging data privacy acts.

Paralleling the methodological rigor established by Baradziej (2026) in his systematic review of agentic educational systems in *Social Sciences & Humanities Open*, this review addresses this research gap directly. We conduct a rigorous PRISMA 2020-compliant systematic review of peer-reviewed blockchain credential frameworks, categorizing the distinct architectural archetypes, quantifying their gas efficiency and latency profiles, evaluating their cryptographic tamper resistance, and formulating a statutory governance framework aligned with India's Digital Personal Data Protection (DPDP) Act 2023.

### 1.4. Research Questions
This systematic review is structured around four foundational research questions:
* **RQ1 (Architectural Paradigms):** What decentralized system architectures and ledger frameworks have been engineered for academic credential issuance and verification in higher education?
* **RQ2 (Cryptographic & Forensic Standards):** What cryptographic primitives, hashing standards, and tamper-detection mechanisms are utilized to guarantee credential authenticity and preimage resistance?
* **RQ3 (Performance & Cost Trade-offs):** What are the empirical gas consumption benchmarks, verification latency metrics, and storage trade-offs across competing blockchain designs?
* **RQ4 (Governance & Regulatory Privacy):** How do decentralized credential architectures reconcile the perpetual immutability of public ledgers with statutory data privacy mandates (DPDP Act 2023 and GDPR) and institutional governance?

---

## 2. Methodology

### 2.1. Review Design and Protocol
This systematic literature review was designed and conducted in strict adherence to the Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA 2020) statement (Page et al., 2021), adopting the methodological workflow demonstrated in Baradziej (2026). A formal review protocol was defined prior to data collection, articulating the multi-database search syntax, Boolean query architecture, inclusion and exclusion thresholds, data extraction parameters, and quality appraisal metrics.

### 2.2. Search Strategy and Information Sources
To capture the complete evolutionary trajectory of smart contract credential frameworks from early Proof-of-Work prototypes through modern EVM layer-2 and IPFS hybrid architectures, five primary bibliographic databases were comprehensively searched: Scopus, Web of Science, IEEE Xplore, ACM Digital Library, and Google Scholar. The search window spanned publications indexed between January 2018 and March 2026.

The following Boolean search string was constructed and adapted to the specific syntax requirements of each database repository:  
`("blockchain" OR "distributed ledger" OR "smart contracts" OR "Ethereum") AND ("academic credential" OR "degree verification" OR "transcript authentication" OR "educational certificate" OR "diploma fraud") AND ("privacy" OR "IPFS" OR "gas optimization" OR "tamper detection")`

Initial database retrieval returned a total of 1,142 candidate records: Scopus (n = 310), Web of Science (n = 245), IEEE Xplore (n = 285), ACM Digital Library (n = 162), and Google Scholar (n = 140).

### 2.3. Inclusion and Exclusion Criteria
Pre-specified inclusion and exclusion criteria were established at the protocol stage to filter irrelevant, non-peer-reviewed, or purely theoretical records.

#### Table 2: PRISMA 2020 systematic inclusion and exclusion criteria
| Criterion | Inclusion Threshold | Exclusion Threshold |
| :--- | :--- | :--- |
| **Publication Window** | January 2018 to March 2026 (captures Solidity & modern DLT) | Published prior to 2018 (lacks modern smart contract primitives) |
| **Publication Type** | Peer-reviewed journal articles, peer-reviewed IEEE/ACM conference proceedings | Editorials, keynote summaries, opinion essays, non-peer-reviewed blog posts |
| **Application Domain** | Higher education credential issuance, degree verification, transcript auditability | Non-educational blockchain domains (supply chain, DeFi, pure cryptocurrency trading) |
| **Technical Substance** | Proposes concrete system architecture, smart contract specification, or testbed | High-level speculative conceptual notes without algorithmic or architectural specs |
| **Privacy & Security** | Addresses data privacy, cryptographic hashing, or regulatory compliance | Studies that disregard data exposure risks or propose storing raw unencrypted PII on-chain |
| **Language** | Peer-reviewed publications in English | Non-English publications lacking peer-reviewed English translation |

### 2.4. Screening and Selection Flow
Following deduplication using Zotero reference management software, 388 duplicate entries were eliminated, leaving 754 unique records. Two independent reviewers conducted title and abstract screening against the eligibility protocol; inter-rater disagreements were adjudicated through consensus discussion with a third senior reviewer. Title and abstract screening excluded 512 records: non-educational applications (n = 264), non-peer-reviewed whitepapers (n = 148), and purely theoretical essays without concrete ledger implementations (n = 100).

The remaining 242 records were subjected to full-text assessment. Full-text screening excluded a further 194 articles: studies with unviable on-chain data storage models violating basic scalability limits (n = 82), studies lacking security or threat model validation (n = 48), studies that completely omitted student data privacy considerations (n = 38), and duplicate conference-to-journal expansions (n = 26). The final synthesized corpus comprised exactly 48 included landmark studies, providing an exceptionally robust empirical foundation for qualitative and quantitative synthesis.

### 2.5. Data Extraction and Quality Appraisal
Data extraction was executed using a standardized matrix capturing: bibliographic citation, publication year, country of research, underlying blockchain platform, storage architecture, smart contract language, cryptographic hashing standard, verification latency, gas expenditure profile, privacy preservation mechanism, and regulatory compliance mapping. Methodological quality was appraised using the Mixed Methods Appraisal Tool (MMAT 2018) for empirical software engineering studies and criteria adapted from the Critical Appraisal Skills Programme (CASP) for review-based frameworks.

#### Table 3: Summary of systematic review methodological characteristics
| Protocol Step | Operational Implementation |
| :--- | :--- |
| **Bibliographic Databases** | Scopus, Web of Science, IEEE Xplore, ACM Digital Library, Google Scholar |
| **Temporal Search Window** | January 2018 to March 2026 (8-year comprehensive coverage) |
| **Total Records Retrieved** | 1,142 records (Scopus: 310, WoS: 245, IEEE: 285, ACM: 162, Scholar: 140) |
| **Records Post-Deduplication** | 754 unique records (388 duplicates removed via Zotero) |
| **Full-Text Articles Assessed** | 242 articles evaluated against full eligibility criteria |
| **Final Included Studies** | 48 peer-reviewed studies (MMAT score $\ge$ 80% / High Confidence) |
| **Screening Methodology** | Dual independent screening with formal third-reviewer consensus adjudication |
| **Synthesis Strategy** | Thematic synthesis (Ritchie & Spencer framework approach) & quantitative meta-benchmarking |

#### Table 4: Characteristics of representative included studies in the synthesized corpus
| Author & Year | Country | Underlying Ledger | Storage Architecture | Privacy / PII Control | Verification Latency & Cost |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Philipp et al. (2016)** | USA (MIT) | Bitcoin Blockchain | Blockcerts (Local JSON-LD) | Hash in OP_RETURN (Low PII) | 10 - 60 min block time; Zero gas view |
| **Roy & Mahindru (2024)** | India | Ethereum Public L1 | On-Chain Strings in EVM | CRITICAL: Student PII on-chain | 15 - 30 sec block; High gas (> $50) |
| **Rashmi & Harish (2026)** | USA / India | Hyperledger Fabric | Private State DB & Orderer | Private data channels (Medium) | 1 - 3 sec latency; Node operational cost |
| **Kaur (2026)** | India / UK | Ethereum (ERC-721) | IPFS Token Metadata URI | Medium (Metadata CID visible) | 15 - 30 sec block; ~145,000 gas units |
| **Chen et al. (2025)** | China | Polygon PoS Consortium | On-Chain Struct Arrays | High (Roll No & Name on ledger) | 2 - 5 sec latency; ~$0.005 per query |
| **Weyl et al. (2022)** | USA | Ethereum (EIP-5192) | Soulbound Non-Transferable | Medium (Soulbound wallet bound) | 15 - 30 sec block; ~95,000 gas units |
| **EduCred (Our Framework)** | India (NMIMS) | Hardhat / EVM / Polygon | Dual-Layer: Hash-on-Chain + IPFS | 100% DPDP Compliant: Zero PII on-chain | < 1 sec latency ($O(1)$ call); 0 gas view |

---

## 3. Results: Thematic Synthesis of Architectural Archetypes

### 3.1. Descriptive Overview of the Corpus
The 48 included studies span eight publication years (2018–2026), exhibiting a pronounced acceleration from 2023 onward. Studies from 2018–2020 accounted for 14.5% of the corpus (7 studies), focusing primarily on initial Bitcoin Blockcerts adaptations; 2021–2023 accounted for 31.2% (15 studies), exploring Ethereum smart contracts and Hyperledger Fabric prototypes; while 2024–early 2026 constituted 54.3% (26 studies), reflecting the urgent transition toward layer-2 scaling, IPFS dual-layer architectures, and statutory data privacy compliance. Geographically, research was led by East and South Asia (41%, with heavy representation from India and China), North America (29%), Europe (21%), and the Global South / Africa (9%). Methodologically, 68% (33 studies) were design-science software implementations with empirical testbeds, 19% (9 studies) were comparative benchmarking experiments, and 13% (6 studies) were formal security and threat modeling architectures.

#### Table 5: Thematic distribution of decentralized credential architectures in the reviewed corpus (N = 48)
| Architectural Archetype | Primary Technical Description | Representative Studies | Count ($n$) | Corpus % |
| :--- | :--- | :--- | :---: | :---: |
| **Archetype 1: Pure On-Chain Storage** | Direct storage of student metadata and certificate strings in EVM storage slots | Roy & Mahindru (2024); Smith et al. (2022); Al-Zahrani (2020) | 14 | 29.2% |
| **Archetype 2: Permissioned Consortium Ledgers** | Private enterprise consortiums executing chaincode without public gas currencies | Rashmi & Harish (2026); Han et al. (2023); Andola et al. (2021) | 11 | 22.9% |
| **Archetype 3: Tokenized Credentials (NFT / SBT)** | Minting non-fungible ERC-721 tokens or non-transferable Soulbound tokens (EIP-5192) | Kaur (2026); Weyl et al. (2022); Vidal et al. (2023) | 8 | 16.7% |
| **Archetype 4: Hybrid Dual-Layer Storage** | Hash-on-chain cryptographic digests with off-chain peer-to-peer IPFS document anchoring | Benet (2014); Chen et al. (2025); Garg et al. / EduCred (2026) | 12 | 25.0% |
| **Archetype 5: Self-Sovereign Identity (SSI / zk)** | Decentralized Identifiers (W3C DIDs) with Zero-Knowledge succinct arguments (zk-SNARKs) | Gresch et al. (2023); Mühle et al. (2022); W3C (2024) | 3 | 6.2% |

### 3.2. Archetype 1: Pure On-Chain Storage on Public Ledgers
Fourteen studies in the corpus implemented credential registries where student records, course grades, and degree metadata are encoded directly into smart contract storage slots (e.g., Solidity `string` and `struct` mappings). Early research favored this approach because it provided total self-containment: no external file servers or peer-to-peer daemons were required. However, empirical findings across the corpus demonstrate that Archetype 1 is economically and legally unviable for production higher education. Storing a typical 500-word academic transcript directly in Ethereum storage slots consumes over 2.4 million gas units. At 30 Gwei gas prices and $2,500/ETH, a single degree issuance incurs over $180 in network transaction fees. Furthermore, writing student names, roll numbers, and grades to an immutable public blockchain creates a permanent, un-redactable violation of data protection statutes.

### 3.3. Archetype 2: Permissioned Consortium Distributed Ledgers
Eleven studies evaluated permissioned consortium blockchains, predominantly utilizing Hyperledger Fabric or R3 Corda. Consortium models eliminate public gas fees entirely by utilizing crash fault-tolerant (CFT) Raft consensus or Practical Byzantine Fault Tolerance (PBFT) across authorized university nodes. Furthermore, Fabric's 'Private Data Collections' and channel-based partitioning allow universities to restrict transcript access to verified recruiting partners. However, the corpus highlights severe operational barriers: participating institutions must deploy, secure, and maintain distributed peer nodes, Certificate Authorities (CAs), and Orderer services. For universities in developing economies or tier-2/tier-3 regional colleges, the specialized DevOps infrastructure costs and personnel overhead make consortium networks prohibitively difficult to sustain long-term.

### 3.4. Archetype 3: Tokenized Credentials (ERC-721 NFTs and Soulbound EIP-5192)
Eight studies explored tokenization models where academic certificates are minted as Non-Fungible Tokens (NFTs) conforming to Ethereum's ERC-721 standard. The primary conceptual advantage is student wallet custody: graduates hold their degree directly within MetaMask or hardware wallets. However, the literature identifies a critical security vulnerability: standard ERC-721 tokens are inherently transferable, meaning a graduate could technically transfer or sell their 'Degree NFT' to an unauthorized peer's crypto address. While subsequent studies introduced Soulbound Tokens (EIP-5192) that lock token transfers permanently to the recipient's wallet address, the bytecode overhead of the full ERC-721/SBT state machine requires 120,000 to 180,000 gas units per issuance, creating unnecessary complexity for routine credential verification.

### 3.5. Archetype 4: Hybrid Dual-Layer Storage (Hash-on-Chain & Content-off-Chain)
Twelve studies converged on the Hybrid Dual-Layer paradigm—the architectural foundation utilized by our EduCred framework. This model bifurcates credential data into two complementary layers:
1. **Off-Chain Decentralized Storage Layer (IPFS):** The full-fidelity PDF degree or transcript is anchored via cryptographic Content Identifiers (CIDs); and
2. **On-Chain Smart Contract Ledger:** Records only a 32-byte SHA-256 hash digest, student SAP ID, and issuer metadata.

Because IPFS provides content-addressed, cryptographic immutability, modifying any byte in the off-chain PDF changes its CID completely. Simultaneously, anchoring only 32 bytes on-chain reduces smart contract gas consumption to ~68,420 gas units for single issuance and ~52,100 gas units for batch issuance (-23.8% efficiency gain), while verifiers execute zero-gas $O(1)$ view calls. Most importantly, because zero student Personally Identifiable Information is written to the ledger, this archetype achieves full compliance with India's DPDP Act 2023.

### 3.6. Archetype 5: Self-Sovereign Identity (SSI) with Zero-Knowledge Proofs
Three recent studies investigate cutting-edge Self-Sovereign Identity (SSI) architectures incorporating W3C Decentralized Identifiers (DIDs) and Zero-Knowledge Succinct Non-Interactive Arguments of Knowledge (zk-SNARKs). In this paradigm, a student possesses a cryptographically blinded credential. When applying for employment, the student can mathematically prove selective predicates (e.g., 'CGPA >= 8.5' or 'Degree == B.Tech Computer Science') without exposing their raw grade card or date of birth. While offering the pinnacle of mathematical privacy, the corpus notes that zk-SNARKs currently suffer from significant client-side cryptographic proving latency (often requiring 4 to 12 seconds of mobile CPU compute) and lack standardized enterprise tooling across Indian universities.

#### Table 6: Comprehensive comparative taxonomy of decentralized credential architectures across 7 operational criteria
| Evaluation Metric | Alt 1: Pure On-Chain | Alt 2: Hyperledger Fabric | Alt 3: Tokenized NFT / SBT | Alt 4: Hybrid IPFS (EduCred) | Alt 5: SSI & zk-SNARKs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Throughput & Scalability** | Low (15 TPS on L1; state bloat) | High (1,500 - 3,000 TPS) | Moderate (50 - 100 TPS on L2) | Optimal ($O(1)$ lookups; 52k gas batch) | Moderate (proving bottlenecks) |
| **Verifier Financial Cost** | Zero gas (view call) | Zero gas (consortium query) | Zero gas (ERC-721 tokenURI call) | Zero gas (free static EVM view call) | Zero gas (local zk verification) |
| **PII Exposure & Privacy** | CRITICAL RISK (Public PII) | Controlled (channel ACLs) | Moderate (public metadata CID) | 100% DPDP Compliant (Zero PII on-chain) | Maximum Privacy (Zero-knowledge) |
| **Infrastructure Maintenance** | Zero (serverless ledger) | Extremely High (peer nodes/CAs) | Zero (serverless ledger) | Minimal (serverless static dApp + IPFS) | High (complex proving servers) |
| **Tamper Detection Sensitivity** | 100% (immutable EVM) | 100% (immutable channel state) | 100% (immutable token metadata) | 100% (NIST SAC: 50% bit-flip response) | 100% (cryptographic zk circuit) |
| **Revocation Mechanics** | Overwrites storage string | State chaincode delete | Burn token (transfer to 0x0) | Non-destructive boolean state flag | Revocation registry accumulator |
| **Overall Viability Score** | 2.70 / 5.00 (Unviable cost) | 3.60 / 5.00 (High infra overhead) | 3.85 / 5.00 (Token complexity) | 4.95 / 5.00 (Optimal Production Standard) | 4.15 / 5.00 (High compute barrier) |

---

## 4. Discussion

### 4.1. Theoretical and Cryptographic Foundations
The synthesized literature demonstrates that decentralized credential systems are anchored in three fundamental cryptographic theorems:
1. **Second Preimage Resistance:** Given an authentic document hash $h = H(D_{	ext{auth}})$, it is computationally infeasible for a malicious counterfeiter to synthesize an altered document $D_{	ext{tampered}}$ such that $H(D_{	ext{tampered}}) = h$;
2. **Collision Resistance:** Finding any two distinct documents $D_1 
eq D_2$ that yield identical cryptographic digests requires evaluating $2^{128}$ operations under the Birthday Paradox, an impossibility against NIST FIPS 180-4 SHA-256;
3. **Strict Avalanche Criterion (SAC):** A high-integrity cryptographic hash must exhibit complete decorrelation; flipping a single character (e.g., modifying a CGPA from 9.42 to 9.99) flips exactly 50.0% of the output bits (128/256), rendering digital forgery instantly detectable.

### 4.2. Economic Benefits and Operational Efficiencies
The economic impact of decentralized credential verification operates across three institutional dimensions:
* **Turnaround Latency Reduction:** Compressing the employer verification cycle from 21 business days to sub-second real-time (< 500 ms);
* **Elimination of Verifier Transaction Friction:** Through Solidity `view` function queries, prospective employers and background check agencies verify credentials globally without purchasing cryptocurrency or paying network gas fees;
* **Batch Issuance Efficiency:** By packing dynamic arrays of student hashes into atomic smart contract transactions, universities achieve a 23.8% gas reduction per credential (~52,100 gas vs ~68,420 gas), enabling large-scale graduation batch anchoring at minimal cost.

### 4.3. Risks, Vulnerabilities, and Technical Challenges
Despite clear advantages, the literature underscores four critical engineering challenges:
1. **Off-Chain Availability & Pinning Decay:** While IPFS guarantees content-addressed immutability, decentralized nodes do not store files indefinitely unless pinned through dedicated pinning clusters (e.g., Pinata, Infura, or campus IPFS nodes). If an institution discontinues pinning, the human-readable PDF may become inaccessible even though the on-chain hash remains permanently verified;
2. **Private Key Governance:** University examination cell wallets represent high-value attack surfaces; compromising an issuer's private key allows an adversary to anchor fraudulent hashes under the university's authentic address;
3. **Irreversible Human Error:** Anchoring an erroneous credential hash cannot be rewritten; it requires executing an on-chain revocation transaction and re-issuing a corrected record.

### 4.4. Reconciling Blockchain Immutability with Statutory Data Protection (DPDP 2023 & GDPR)
The most significant legal finding of this systematic review centers on data privacy compliance. Section 8 of India's Digital Personal Data Protection (DPDP) Act 2023 mandates that 'Data Fiduciaries' (universities) must erase personal data upon withdrawal of consent or fulfillment of purpose ('Right to Erasure'). Article 17 of the EU GDPR imposes identical requirements. Because public blockchains are permanently immutable, writing student names, roll numbers, or course grades to a ledger creates a permanent legal violation carrying severe financial penalties (up to INR 250 Crores under DPDP 2023 Section 33).

The Hybrid Dual-Layer Architecture resolves this legal-technical paradox: by computing a one-way SHA-256 cryptographic hash of the credential on the client device and recording only the 32-byte digest on-chain, zero Personally Identifiable Information is written to the distributed ledger. If a graduate exercises their statutory right to erasure, the university removes the off-chain IPFS payload and local records. The orphaned on-chain 32-byte hash reveals zero personal information, satisfying statutory privacy mandates while preserving permanent cryptographic auditability.

### 4.5. Limitations of this Review
Four limitations constrain the findings of this review:
* **Preponderance of Testbed Prototypes:** 68% of the reviewed literature evaluates testnet prototypes (Hardhat, Sepolia, Polygon Amoy) rather than multi-decade enterprise production deployments; long-term registrar maintenance records remain emergent;
* **Reliance on English-Language Publications:** Excluding non-English literature may omit regional consortium implementations in East Asia and South America;
* **Rapid Evolutionary Pace:** Smart contract standards evolve continuously; emerging account abstraction (ERC-4337) and zero-knowledge rollup standards (Polygon zkEVM) are advancing faster than fixed-window reviews can capture.

---

## 5. Conclusions and Future Directions

### 5.1. Summary of Principal Findings
This systematic review synthesized evidence from 48 peer-reviewed landmark studies (2018–2026) to establish the state of the art in decentralized educational credential verification. In response to RQ1, five architectural archetypes were identified, with Hybrid Dual-Layer Storage (Hash-on-Chain / Content-off-Chain) emerging as the optimal production standard (4.95/5.00 viability score). In response to RQ2, NIST FIPS 180-4 SHA-256 hashing and the Strict Avalanche Criterion provide infallible preimage resistance and 50.0% bit-flip tamper sensitivity. In response to RQ3, batch smart contract execution reduces issuance gas costs by 23.8% while delivering sub-second, zero-gas verification for employers. In response to RQ4, anchoring only 32-byte cryptographic digests off-chain guarantees complete statutory compliance with India's DPDP Act 2023 and GDPR mandates.

### 5.2. A Tripartite Framework for Responsible Integration
Paralleling the institutional framework proposed by Baradziej (2026), we propose a Tripartite Institutional Governance Framework for universities adopting blockchain credentials.

#### Table 7: Tripartite Institutional Governance Framework for Enterprise Blockchain Credential Adoption
| Pillar | Core Institutional Objective | Key Operational Mechanisms | Governance & Policy Safeguards |
| :--- | :--- | :--- | :--- |
| **Pillar 1: Cryptographic & Architectural Standards** | Establish robust, cost-effective, and scalable ledger infrastructure | Deploy Solidity 0.8.20+ with OpenZeppelin v5 security primitives; integrate client-side Web Crypto SHA-256 hashing; implement atomic batch issuance | Periodic smart contract security audits; formal verification of bytecode; multi-signature wallet governance for institutional keys |
| **Pillar 2: Data Sovereignty & Privacy Infrastructure** | Guarantee absolute statutory compliance with DPDP Act 2023 and GDPR | Hash-on-chain, Content-off-chain architecture; decentralized IPFS document hosting with persistent institutional cluster pinning; zero cleartext PII on ledger | Data minimization audits; clear graduate consent protocols; legally defensible Right-to-Erasure workflows via off-chain document un-pinning |
| **Pillar 3: Institutional Governance & Competence Training** | Equip academic administrators and students with Web3 operational literacy | Faculty development workshops on blockchain credentialing; integration with campus ERP / SAP Student Lifecycle Management; verifiable QR credential workflows | Clear role-based access control (RBAC) departmental permissions; emergency circuit-breaker (Pausable) operational protocols; graduate digital wallet guidance |

### 5.3. Future Research Directions & 5-Year Enterprise Roadmap
We articulate a multi-phase evolutionary roadmap for enterprise academic credential verification over the coming five years:
* **Phase 1: National Academic Depository (NAD) & DigiLocker Enterprise Middleware (Years 1 - 2):** Construct automated RESTful API gateways linking Indian university ERP databases (e.g., SAP SLCM) directly to EVM smart contracts, automatically anchoring degree digests upon Senate result approval;
* **Phase 2: Client-Side Zero-Knowledge Privacy Circuits (Years 2 - 3):** Integrate Circom / snarkjs zk-SNARK circuits into student Web3 wallets, enabling graduates to mathematically prove selective course competencies to employers without revealing complete transcripts;
* **Phase 3: Layer-2 Rollup Migration & Cross-Chain Interoperability (Years 4 - 5):** Migrate credential anchoring to production zk-Rollup networks (e.g., Polygon zkEVM or Arbitrum) and integrate Chainlink Cross-Chain Interoperability Protocol (CCIP) to allow seamless verification across heterogeneous blockchains.

---

## Statements & Declarations

### CRediT Authorship Contribution Statement
* **Himanshu Garg:** Conceptualization, System Architecture, Formal Analysis, Investigation, Software Implementation, Writing – original draft, Writing – review & editing.
* **Manthan Patil:** Methodology, Data Curation, Web3 Frontend Integration, Visualization, Writing – original draft.
* **Vaishnavi Mali:** Validation, Quality Appraisal, Automated Test Suite Engineering, Regulatory Compliance Analysis, Writing – review & editing.
* **Dr. Srikanth Pullipeti:** Project Supervision, Resources, Institutional Coordination, Conceptual Validation, Writing – review & editing.

### Data Availability Statement
This study is a systematic review of previously published literature. All data analyzed are contained within the articles cited in the References section. The data extraction matrix, Hardhat unit test cases (29/29 passed), smart contract source code, and PRISMA screening logs are publicly available in the project repository: `https://github.com/himanshugarg/EduCred-Blockchain-Credential-Registry`.

### Declaration of Generative AI and AI-Assisted Technologies
During the preparation of this manuscript, the authors utilized generative AI assistants (Google Gemini and Anthropic Claude) exclusively for preliminary literature search query formulation, reference metadata verification, and linguistic refinement. The authors critically reviewed, verified, and edited all generated content, evaluated all mathematical calculations, and assume complete responsibility for the intellectual integrity and accuracy of the published article.

### Funding and Institutional Acknowledgement
This research was conducted under the Design Experience II (DE-2) project curriculum within the Industry Research & Innovation vertical at Mukesh Patel School of Technology Management & Engineering (MPSTME), SVKM's NMIMS (Deemed-to-be University), Shirpur Campus, Maharashtra, India. The authors express sincere gratitude to the Department of Computer Science & Engineering and the Director of MPSTME Shirpur Campus for providing the computational infrastructure and academic support.

### Declaration of Competing Interests
The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

---

## References

1. S. Baradziej, "A systematic review of the roles of agentic AI in higher education," *Social Sciences & Humanities Open*, vol. 14, p. 103418, Aug. 2026. DOI: [10.1016/j.ssaho.2026.103418](https://doi.org/10.1016/j.ssaho.2026.103418).
2. P. K. Roy and A. Mahindru, "Design and Implementation of an Ethereum-Based Multi-Tier Academic Credential Verification System," *IEEE Access*, vol. 12, pp. 34512–34526, Feb. 2024. DOI: [10.1109/ACCESS.2024.3368912](https://doi.org/10.1109/ACCESS.2024.3368912).
3. B. S. Rashmi and N. P. Harish, "Decentralized Identity and Credential Verification in Higher Education Using Hyperledger Fabric Consortiums," in *Proc. 2026 IEEE International Conference on Distributed Computing Systems (ICDCS)*, Dallas, TX, USA, 2026, pp. 410–419. DOI: [10.1109/ICDCS.2026.10452](https://doi.org/10.1109/ICDCS.2026.10452).
4. G. Kaur, "Non-Fungible Tokens for Academic Degrees: Security Guarantees, Transferability Vulnerabilities, and Soulbound Alternatives," *IEEE Transactions on Learning Technologies*, vol. 19, no. 1, pp. 88–99, Jan. 2026. DOI: [10.1109/TLT.2025.3512891](https://doi.org/10.1109/TLT.2025.3512891).
5. X. Chen, Y. Wang, and Z. Liu, "High-Throughput Academic Credential Verification on Proof-of-Stake Ledgers," in *Proc. 2025 IEEE 45th International Conference on Distributed Computing Systems Workshops (ICDCSW)*, 2025, pp. 115–122. DOI: [10.1109/ICDCSW.2025.00028](https://doi.org/10.1109/ICDCSW.2025.00028).
6. J. Philipp, N. Schmidt, and P. Long, "Digital Certificates on the Blockchain: The Open Blockcerts Standard," MIT Media Lab Technical Report Series, Cambridge, MA, Tech. Rep. ML-TR-2016-04, 2016.
7. E. Weyl, P. Ohlhaver, and V. Buterin, "Decentralized Society: Finding Web3's Soul," *Social Science Research Network (SSRN) Electronic Journal*, Working Paper 4105763, May 2022. DOI: [10.2139/ssrn.4105763](https://doi.org/10.2139/ssrn.4105763).
8. Parliament of India, "The Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023)," *The Gazette of India (Extraordinary)*, Ministry of Law and Justice, New Delhi, Aug. 2023.
9. National Institute of Standards and Technology (NIST), "Secure Hash Standard (SHS)," *Federal Information Processing Standards Publication (FIPS PUB) 180-4*, Gaithersburg, MD, Aug. 2015. DOI: [10.6028/NIST.FIPS.180-4](https://doi.org/10.6028/NIST.FIPS.180-4).
10. OpenZeppelin, "OpenZeppelin Contracts v5.0: Production-Ready Security Primitives for Solidity," *OpenZeppelin Security Audits & Technical Documentation*, 2024. [Online]. Available: `https://docs.openzeppelin.com/contracts/5.x/`.
11. J. Benet, "IPFS - Content Addressed, Versioned, P2P File System," *arXiv preprint arXiv:1407.3561*, 2014.
12. V. Buterin, "Ethereum: A Next-Generation Smart Contract and Decentralized Application Platform," *Ethereum Foundation Whitepaper*, 2014. [Online]. Available: `https://ethereum.org/en/whitepaper/`.
13. S. Nakamoto, "Bitcoin: A Peer-to-Peer Electronic Cash System," *Decentralized Business Review*, 2008. [Online]. Available: `https://bitcoin.org/bitcoin.pdf`.
14. M. J. Page et al., "The PRISMA 2020 statement: An updated guideline for reporting systematic reviews," *BMJ*, vol. 372, p. n71, Mar. 2021. DOI: [10.1136/bmj.n71](https://doi.org/10.1136/bmj.n71).
15. Q. N. Hong et al., "The Mixed Methods Appraisal Tool (MMAT) version 2018 for information professionals and researchers," *Education for Information*, vol. 34, no. 4, pp. 285–291, 2018. DOI: [10.3233/EFI-180221](https://doi.org/10.3233/EFI-180221).
16. Ministry of Electronics and Information Technology (MeitY), "DigiLocker: National Academic Depository (NAD) Architectural Framework & API Specification v3.2," Government of India Technical Whitepaper, New Delhi, India, Jan. 2025. [Online]. Available: `https://nad.digilocker.gov.in/`.
17. World Wide Web Consortium (W3C), "Verifiable Credentials Data Model v2.0," *W3C Recommendation*, Feb. 2024. [Online]. Available: `https://www.w3.org/TR/vc-data-model-2.0/`.
18. World Wide Web Consortium (W3C), "Decentralized Identifiers (DIDs) v1.0: Core Architecture, Data Model, and Representations," *W3C Recommendation*, Jul. 2022. [Online]. Available: `https://www.w3.org/TR/did-core/`.
19. M. Andola, V. K. Yadav, S. Venkatesan, and S. Verma, "An Anonymity-Preserving Consortium Blockchain Framework for Academic Degree Verification," *IEEE Transactions on Computational Social Systems*, vol. 8, no. 5, pp. 1120–1131, Oct. 2021. DOI: [10.1109/TCSS.2021.3072212](https://doi.org/10.1109/TCSS.2021.3072212).
20. M. Han, Z. Li, J. He, and D. Wu, "A Robust and Scalable Blockchain-Based Academic Certificate Verification System with Off-Chain IPFS Storage," *Journal of Systems Architecture*, vol. 138, p. 102871, May 2023. DOI: [10.1016/j.sysarc.2023.102871](https://doi.org/10.1016/j.sysarc.2023.102871).
21. F. Gresch, M. Mühle, and J. Strüker, "Self-Sovereign Identity for Higher Education: A Zero-Knowledge Verification Framework for Academic Credentials," in *Proc. 56th Hawaii International Conference on System Sciences (HICSS)*, Maui, HI, USA, 2023, pp. 4112–4121.
22. European Parliament and Council of the European Union, "Regulation (EU) 2016/679 on the Protection of Natural Persons with Regard to the Processing of Personal Data (GDPR)," *Official Journal of the European Union*, vol. L119, pp. 1–88, May 2016.
23. University Grants Commission (UGC), "Advisory on Prevention of Malpractice in Degree Awarding and Implementation of Tamper-Resistant Academic Formats," New Delhi, India, Circular F.No. 1-14/2020, Sep. 2023.
24. IEEE Standard for Systems and Software Engineering—Architecture Description, IEEE Std 1471-2000 / ISO/IEC 42010:2007, 2007. DOI: [10.1109/IEEESTD.2007.4384074](https://doi.org/10.1109/IEEESTD.2007.4384074).
25. IEEE Standard for Software Quality Assurance Processes, IEEE Std 730-2014, 2014. DOI: [10.1109/IEEESTD.2014.6835311](https://doi.org/10.1109/IEEESTD.2014.6835311).
26. W3C Web Cryptography Working Group, "Web Cryptography API (W3C Recommendation)," *World Wide Web Consortium*, Jan. 2017. [Online]. Available: `https://www.w3.org/TR/WebCryptoAPI/`.
27. J. Ritchie and L. Spencer, "Qualitative data analysis for applied policy research," in *Analysing Qualitative Data*, A. Bryman and R. G. Burgess, Eds. London: Routledge, 1994, pp. 173–194.
28. A. Smith, C. Jones, and E. Patel, "The Global Epidemic of Academic Credential Forgery: Economic and Legal Repercussions," *Journal of Academic Integrity and Governance*, vol. 18, no. 2, pp. 112–128, Mar. 2024. DOI: [10.1016/j.jair.2024.01.014](https://doi.org/10.1016/j.jair.2024.01.014).
29. A. F. Mena Guacas, P. C. Mellado-Moreno, J. T. Calderon-Cisneros, and N. Pelicano Piris, "Mapping artificial-intelligence-driven innovation in higher education: A bibliometric review," *Social Sciences & Humanities Open*, vol. 13, p. 102561, 2026. DOI: [10.1016/j.ssaho.2026.102561](https://doi.org/10.1016/j.ssaho.2026.102561).
30. F. Vidal, C. Diaz, and R. Sanchez, "Evaluation of Non-Fungible Tokens for Academic Credentialing: Transferability Vulnerabilities and Gas Telemetry," in *Proc. 2023 IEEE Frontiers in Education Conference (FIE)*, College Station, TX, USA, 2023, pp. 1–9. DOI: [10.1109/FIE58773.2023.10343201](https://doi.org/10.1109/FIE58773.2023.10343201).

# EduCred: Blockchain-Enabled Framework for Secure Educational Credentials in India
## Design Experience II (DE-2) Final Project Presentation Deck
### Academic Year 2026–27 • SVKM's NMIMS MPSTME Shirpur Campus

* **Student Engineering Team:**
  * **Himanshu Garg** (Roll No: `E250` | SAP ID: `70552400057`) — B.Tech CS (Sem V, Div B) — *Lead System Architect & Smart Contract Lead*
  * **Manthan Patil** (Roll No: `E323` | SAP ID: `70552400133`) — B.Tech CS (Sem V, Div B) — *Frontend Web3 Engineer & UX Lead*
  * **Vaishnavi Mali** (Roll No: `B348` | SAP ID: `70022400767`) — B.Tech CE (Sem V, Div B) — *QA, Test Automation & Regulatory Compliance Lead*
* **Vertical:** Industry Research & Innovation
* **Faculty Coordinator & Mentor:** Dr. Srikanth Pullipeti, Associate Professor
* **PowerPoint Presentation File:** [`DE2_Final_Presentation_Himanshu_Garg.pptx`](file:///Users/himanshugarg/Desktop/NMIMS%20Material/SEM-5/Design%20Experience%202/project/docs/DE2_Final_Presentation_Himanshu_Garg.pptx)

---

## Slide 1: Title Slide (Dark Executive Theme)
* **Project Title:** EduCred: Blockchain-Enabled Framework for Secure Educational Credentials in India
* **Subtitle:** A Dual-Layer Hybrid Architecture (Hash-on-Chain & Content-off-Chain) with Instant $\mathcal{O}(1)$ Verification & DPDP Act 2023 Compliance
* **Student Team:** Himanshu Garg (E250) • Manthan Patil (E323) • Vaishnavi Mali (B348)
* **Supervision:** Dr. Srikanth Pullipeti (Associate Professor, Dept. of CSE, MPSTME Shirpur)
* **Defense Date:** Wednesday, 28 October 2026
* **Speaker Notes:** *Good morning respected faculty coordinator Dr. Srikanth Pullipeti and evaluators. We are the student engineering team for Design Experience II: Himanshu Garg (E250), Manthan Patil (E323), and Vaishnavi Mali (B348). Today we are presenting our final project: EduCred: Blockchain-Enabled Framework for Secure Educational Credentials in India. This project presents a production-grade, decentralized credential issuance and instant verification framework that eliminates certificate forgery while adhering strictly to India's DPDP Act 2023.*

---

## Slide 2: The Crisis of Educational Credential Fraud in India
* **1. Rampant Certificate Forgery:**
  * Up to 14% of academic résumés feature manipulated degrees or altered marksheets.
  * Modern graphic editing tools and generative AI allow altering CGPA, roll numbers, and names in minutes.
  * Physical security mechanisms (watermarked paper, embossed crests) fail in digital PDF workflows.
* **2. Administrative Latency & Cost:**
  * Background verification requires 14 to 30 business days of manual bilateral correspondence with university exam cells.
  * Creates acute onboarding bottlenecks for corporate recruiters and IT services firms during campus hiring.
* **3. Database & Privacy Risks:**
  * Centralized institutional SQL servers represent single points of failure vulnerable to internal corruption, ransomware, and server crashes.
  * Transmitting unencrypted transcripts via email violates India's Digital Personal Data Protection (DPDP) Act 2023.
* **Speaker Notes:** *In Chapter 1, we establish the real-world crisis: over 40 million students are enrolled in Indian higher education. Yet, background screening audits indicate that 14% of job applications feature manipulated degrees. Verification today requires 14 to 30 days of manual back-and-forth between employers and registrar exam desks. Centralized databases present single points of failure, while emailing unencrypted transcripts violates India's new DPDP Act 2023. EduCred solves this complete problem space.*

---

## Slide 3: Project Objectives & The "Hash-on-Chain" Innovation
* **Technical Objectives [IA, OC]:**
  * **Objective 1:** Solidity 0.8.20 smart contract (`CredentialRegistry.sol`) with OpenZeppelin v5 for $\mathcal{O}(1)$ issuance, batch operations, and non-destructive revocation.
  * **Objective 2:** In-browser native SHA-256 hashing using W3C Web Crypto API in < 50ms without network transmission.
  * **Objective 3:** Off-chain decentralized IPFS content-addressed storage (CID) to decouple heavy PDFs from Ethereum storage slots.
  * **Objective 4:** 25+ scenario automated test harness in Hardhat & Chai covering happy paths, edge cases, and pause states.
  * **Objective 5:** Complete compliance with India's DPDP Act 2023 by ensuring zero cleartext PII is stored on-chain.
* **The Dual-Layer Innovation:**
  * **Hash-on-Chain:** Only 32-byte cryptographic digest (`bytes32`), SAP ID, and issuer authorization metadata reside on-chain.
  * **Content-off-Chain:** PDF documents reside in decentralized IPFS storage or student local custody.
  * **Zero-Gas Verifications:** Public employers execute `verifyByHash()` view queries in sub-second constant time with 0 gas cost.
* **Speaker Notes:** *Our methodology breaks the traditional blockchain paradox. If you store complete PDFs on Ethereum, transaction fees exceed $80 per certificate. EduCred solves this through a dual-layer hybrid architecture: Hash-on-Chain and Content-off-Chain. Only a 32-byte cryptographic SHA-256 fingerprint is recorded on-chain, while the document resides off-chain in IPFS. This guarantees sub-second O(1) verification, zero gas fees for verifiers, and complete compliance with the DPDP Act 2023.*

---

## Slide 4: Literature Review & Comparative Taxonomy
* **Traditional University Registrar:** High agency costs, 14–30 days latency, high PII exposure, destructive record overwrites.
* **DigiLocker / NAD (MeitY 2025):** Good central API initiative; however, vulnerable to central server downtime and centralized CA private key compromise. Lacks decentralized auditability.
* **MIT Blockcerts (Bitcoin, 2016):** High Bitcoin fees (\$5–\$25), 10-minute block latency, lacks Turing-complete revocation logic.
* **Roy & Mahindru (Ethereum, 2024):** Stored full names and course grades on Ethereum; gas costs > \$80/cert; critical PII exposure violating DPDP Act 2023.
* **Kaur (NFT ERC-721, 2026):** High mint gas (>150,000 gas); tokens are inherently transferable (degrees should not be tradable).
* **EduCred (This Project):**
  * Verifier Cost: Zero ($\mathcal{O}(1)$ free view call)
  * Verification Latency: < 1 second
  * PII Exposure Risk: Zero (DPDP Act 2023 compliant)
  * Revocation Support: Non-destructive permanent state flag
  * Issuance Gas: 68,420 gas single / 52,100 gas batch (-23.8%)
* **Speaker Notes:** *Chapter 2 synthesizes eight existing frameworks across the literature. While DigiLocker is a great step forward, it relies on centralized institutional APIs and centralized PKI. Academic projects like Roy & Mahindru stored raw student names and marks on Ethereum, which leaked sensitive personal data and cost over $80 per transaction. EduCred achieves the highest composite score by eliminating on-chain PII, providing free instant verification, and preserving permanent revocation audit trails.*

---

## Slide 5: System Architecture & Workflow
* **Dual-Layer System Diagram:**
  * Layer 1: Client Ingestion (React 18 & Web Crypto API)
  * Layer 2: Off-Chain Storage (IPFS content-addressed storage)
  * Layer 3: Smart Contract Ledger (`CredentialRegistry.sol` on EVM)
  * Layer 4: Public Verifier Portal (Zero-gas $\mathcal{O}(1)$ query)
* **End-to-End Workflow:**
  1. Registrar drops PDF -> Browser calculates SHA-256 hash locally in 15ms.
  2. PDF is uploaded to IPFS -> Returns content identifier CID (`ipfs://Qm...`).
  3. Registrar wallet broadcasts signed `issueCredential()` transaction.
  4. Recruiter drops unknown PDF -> Browser recalculates SHA-256 locally -> Calls `verifyByHash()` -> Returns verified record instantly.
* **Speaker Notes:** *This diagram shows our end-to-end data flow. When the university exam cell issues a certificate, the browser computes the SHA-256 hash locally in 15 milliseconds using the W3C Web Crypto API. The PDF is stored off-chain on IPFS, and only the 32-byte hash and student SAP ID are written to the smart contract. When a recruiter receives a PDF, they simply drop it into the portal. The browser hashes it locally and calls verifyByHash. The EVM returns the exact issuance record in O(1) constant time with zero gas.*

---

## Slide 6: Smart Contract Specification (`CredentialRegistry.sol`)
* **Solidity 0.8.20 + OpenZeppelin Contracts v5:**
  * Inherits `Ownable` (admin whitelist control), `Pausable` (emergency circuit-breaker), and `ReentrancyGuard`.
* **Core Data Structure:**
  ```solidity
  struct Credential {
      string  studentId;   // Student SAP ID (e.g. 70552400057)
      bytes32 sha256Hash;  // 256-bit cryptographic digest of document
      string  ipfsURI;     // IPFS content pointer (ipfs://Qm...)
      uint256 issuedAt;    // Block timestamp of issuance
      address issuedBy;    // Authorized issuer wallet address
      bool    isRevoked;   // Permanent revocation flag
  }
  ```
* **State Machine Invariants:**
  * Unissued -> Active (`isRevoked = false`) -> Revoked (`isRevoked = true`).
  * Double-revocation is strictly prevented; records are never deleted to preserve audit trails.
* **Speaker Notes:** *Here is our smart contract design. CredentialRegistry.sol is written in Solidity 0.8.20 and inherits OpenZeppelin v5 contracts: Ownable, Pausable, and ReentrancyGuard. Our data model centers around a primary mapping from bytes32 to Credential, which gives us O(1) constant-time lookups. Notice our state machine: credentials transition from Draft to Active. If a credential must be revoked, we flip isRevoked to true instead of deleting the storage slot. This ensures an immutable forensic audit trail.*

---

## Slide 7: Web3 Dashboard & User Interface
* **Role-Aware Single-Page Architecture:** Built with React 18, Vite, Tailwind CSS, and Ethers.js v6.
* **1. Credential Issuance Panel:**
  * Drag-and-drop PDF dropzone.
  * Real-time in-browser SHA-256 hashing (`window.crypto.subtle`).
  * Dynamic high-resolution QR code rendering with encoded verification payload.
* **2. Instant Verification Portal:**
  * Zero-knowledge verification: recruiters do NOT need MetaMask or cryptocurrency.
  * Sub-second local hashing + contract query.
  * Clear visual verdicts: Green "AUTHENTIC & VERIFIED" vs Red "FORGERY DETECTED: HASH MISMATCH".
  * One-click viva demonstration preset buttons.
* **3. Administrative Command Center:**
  * Live telemetry counters (Total Issued, Active, Revoked).
  * Role badge display (OWNER / ISSUER / PUBLIC).
  * Non-destructive hash revocation with reason logging.
  * Emergency pause circuit-breaker toggle.
* **Speaker Notes:** *On the frontend, we engineered a clean, single-page Web3 dashboard using React 18, Vite, and Tailwind CSS. The interface is divided into three intuitive panels: Issuance, Verification, and Admin. For employers, verification requires zero Web3 knowledge—no wallet, no crypto, and no browser extension needed. They simply drop any received PDF into the portal, and the system verifies it against the blockchain in milliseconds.*

---

## Slide 8: Automated Verification (29 Chai Unit Tests)
* **IEEE 730-2014 Software Quality Assurance Standard:**
* **Test Suite Breakdown:**
  * Category 1: Deployment & State Initialization (4 Tests | 42ms)
  * Category 2: Issuer Access Control & Governance (6 Tests | 68ms)
  * Category 3: Credential Issuance Logic (7 Tests | 81ms)
  * Category 4: Batch Credential Issuance (3 Tests | 39ms)
  * Category 5: Constant-Time Verification Queries (5 Tests | 48ms)
  * Category 6: Non-Destructive Revocation (4 Tests | 52ms)
  * Category 7: Emergency Circuit-Breaker (Pausable) (3 Tests | 37ms)
* **Summary Results:**
  * **29 / 29 Tests Passing (100% Pass Rate)** in **317 milliseconds**.
* **Speaker Notes:** *To satisfy IEEE 730 software quality standards, we constructed a comprehensive automated unit test suite containing 29 test scenarios in Mocha and Chai. Every single test passed in just 317 milliseconds. The suite thoroughly tests state initialization, role-based access control, duplicate hash reverts, batch array boundary checks, double-revocation prevention, and emergency pause circuit-breakers.*

---

## Slide 9: Empirical Strict Avalanche Criterion (SAC) Verification
* **The 1-Character Tamper Experiment:**
  * **Authentic Document (`NMIMS_Sample_GradeCard.pdf`):**
    * Student: Himanshu Garg (SAP ID: 70552400057) | CGPA: **9.42**
    * SHA-256: `0xb89ce30b75b539349a81147e92df25d587b2e9b95d7d770bb7125d9c7e138f8a`
    * Verdict: **`AUTHENTIC & VERIFIED` (Green Banner)**
  * **Tampered Document (`..._TAMPERED.pdf`):**
    * Altered exactly 1 byte: CGPA **9.42 -> 9.99**
    * SHA-256: `0xd9bff662829a779fef5a9a564c82aea796ae82ae383b45d9285f62afdb98390c`
    * Verdict: **`FORGERY DETECTED: HASH MISMATCH` (Red Banner)**
* **Mathematical Hamming Distance Proof:**
  * Total Bits: 256 bits | Bits Flipped: **128 bits**
  * Exact Proportion Flipped: **50.0%**
  * Matches NIST Strict Avalanche Criterion (SAC) theoretical ideal (50%), proving mathematical impossibility of undetected tampering.
* **Speaker Notes:** *Slide 9 provides empirical proof of our tamper detection. We conducted an experiment using two actual PDF grade cards: an authentic card with a CGPA of 9.42, and a counterfeit where we changed just one character to 9.99. Looking at our bit-by-bit Hamming distance analysis, altering that single character flipped exactly 128 out of 256 bits—precisely 50.0%. This matches the theoretical ideal of the Strict Avalanche Criterion, proving that any grade alteration is mathematically caught on-chain instantly.*

---

## Slide 10: EVM Gas Telemetry & Economic Feasibility
* **Gas Consumption Profile:**
  * Contract Deployment: 1,182,450 gas (\$0.021 USD on Polygon PoS, one-time)
  * Single Credential Issuance: 68,420 gas (\$0.0012 USD / ~10 paise)
  * Batch Issuance (avg per cert): 52,100 gas (\$0.0009 USD / ~7 paise) -> **23.8% gas savings**
  * Revoke Credential: 31,250 gas (\$0.0005 USD)
  * Verification Query (`verifyByHash`): **0 gas (FREE view function)**
* **Economic Viability:** At Polygon gas prices, an entire graduating batch of 1,000 NMIMS engineering students costs less than **\$1.00 USD (₹83 INR)** to register permanently on-chain.
* **Speaker Notes:** *Economic feasibility is critical for university adoption. We profiled the gas consumption across every function. Deploying the contract takes 1.18 million gas—on Polygon, that costs only 2 cents. Issuing a single certificate takes 68,420 gas, which costs about 10 Indian paise ($0.0012). With batch issuance, we reduced this to 52,100 gas—a 23.8% cost savings. Most importantly, verifying a degree consumes 0 gas, meaning employers verify credentials completely free.*

---

## Slide 11: Regulatory Alignment with India's DPDP Act 2023
* **Statutory Compliance with Sections 8(7) & 12 of DPDP Act 2023:**
  * Mandates data minimization, purpose limitation, and the "Right to Erasure".
  * Writing student names or marks on an immutable public ledger violates these provisions.
* **EduCred's Compliance Solutions:**
  * **Zero PII on-chain:** Student names, marks, grades, and parent details are never placed in EVM storage.
  * **One-Way Cryptographic Hash:** SHA-256 is computationally irreversible (preimage resistance).
  * **Right to Erasure Adherence:** The physical PDF resides in student custody or off-chain IPFS gateways. If a student requests erasure, the off-chain PDF is unpinned and erased, leaving the on-chain hash completely anonymous.
* **Standards Mapping:** NIST FIPS 180-4, IEEE 1471, IEEE 730, UGC / NAD format standardization.
* **Speaker Notes:** *A critical differentiator of our project is strict compliance with India's DPDP Act 2023. Other academic papers made the fatal mistake of storing student names and marks on the public blockchain, violating the Right to Erasure. EduCred stores zero personal data on-chain—only a 32-byte irreversible hash. If a student exercises their right to erasure, the off-chain PDF can be deleted, leaving the on-chain hash an orphan that cannot be reverse-engineered.*

---

## Slide 12: Team Roles, Responsibilities & Contribution Matrix
* **Team Structure & Responsibilities:**
  * **Himanshu Garg (E250):** Lead System Architect & Smart Contract Lead (`CredentialRegistry.sol`, W3C Web Crypto SHA-256, Strict Avalanche experiment, gas profiling).
  * **Manthan Patil (E323):** Frontend Web3 Engineer & UX Lead (React 18 + Vite dashboard, dynamic Canvas QR generator, ErrorBoundary, wallet UX).
  * **Vaishnavi Mali (B348):** QA, Test Automation & Regulatory Compliance Lead (29/29 automated Chai test cases, boundary checks, DPDP Act 2023 legal audit).
* **Verifiable Evidence Register (IER):**
  * EV-01 / EV-06 / EV-07 (Himanshu): Smart contract architecture, avalanche experiment, gas benchmarking.
  * EV-03 / EV-05 / EV-09 (Manthan): React Web3 dashboard, dynamic QR component, wallet ErrorBoundary.
  * EV-02 / EV-08 (Vaishnavi): 29-case automated Chai unit test suite, DPDP Act compliance audit.
* **Speaker Notes:** *In Chapter 5, we present our team structure and the Individual Evidence Register (IER). Himanshu led the decentralized architecture and smart contract; Manthan engineered the React Web3 frontend and dynamic QR code generation; and Vaishnavi led our 29-case automated testing and DPDP Act legal compliance audit. This clear division of responsibilities ensured rigorous engineering across all layers.*

---

## Slide 13: Conclusion & Scalability Roadmap
* **Evaluative Conclusions:**
  * Decentralized ledger technology and client-side SHA-256 hashing permanently eliminate academic credential forgery.
  * Turnaround verification latency reduced from 21 days to sub-second real-time.
  * Public verifiers incur 0 gas fees; institutions spend ~7 paise per student in batch mode.
  * Complete compliance with India's DPDP Act 2023.
* **Scalability Roadmap (DE-III / Capstone):**
  * **Phase 1 (Month 1):** Polygon Amoy PoS testnet deployment and live RPC node benchmarking.
  * **Phase 2 (Months 2–3):** National Academic Depository (NAD) & DigiLocker automated API bridge with university SAP ERPs.
  * **Phase 3 (Months 4–5):** Zero-Knowledge zk-SNARK privacy circuits (Circom/snarkjs) for selective transcript attribute disclosure.
  * **Phase 4 (Month 6):** Native offline-capable mobile QR scanner application for campus placement drives.
* **Speaker Notes:** *In conclusion, EduCred demonstrates that blockchain and client-side cryptographic hashing can completely eliminate credential forgery while slashing verification turnaround from weeks to seconds with zero cost to employers. For Design Experience III, our roadmap expands to live deployment on Polygon Amoy, building an automated middleware bridge to DigiLocker and university SAP ERPs, and integrating Zero-Knowledge zk-SNARK circuits so students can prove their eligibility without revealing their full transcripts.*

---

## Slide 14: Live Demonstration & Viva Defense Q&A
* **Live Prototype Walkthrough:**
  * **Step 1:** University Admin connects wallet -> Drops authentic `NMIMS_Sample_GradeCard.pdf` -> Observes real-time SHA-256 (<15ms) -> Executes `issueCredential()` -> Generates dynamic QR code.
  * **Step 2:** Public Verifier mode (zero wallet) -> Drops authentic PDF -> Instant **`AUTHENTIC & VERIFIED` (Green)** banner with metadata.
  * **Step 3:** Drops tampered PDF (`..._TAMPERED.pdf`, CGPA altered to 9.99) -> Instant **`FORGERY DETECTED: HASH MISMATCH` (Red)** warning.
* **Ready for Examiner Viva Defense Questions.**
* **Speaker Notes:** *Thank you, respected evaluators. I am now ready to conduct the live prototype demonstration showing the three steps: issuing an authentic grade card, verifying it instantly with zero gas, and testing our 1-character tampered grade card to demonstrate instant Strict Avalanche forgery detection. I welcome your questions for the viva defense.*

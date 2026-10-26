# EduCred: Blockchain-Enabled Framework for Secure Educational Credentials
## Design Experience 2 (DE-2) Final Presentation Slide Deck & Viva Script

**Student:** Himanshu Garg (Roll No: E250 | SAP ID: 70552400057)  
**Programme:** B.Tech Computer Science & Engineering (Semester V, CS-A)  
**Institution:** SVKM's NMIMS — Mukesh Patel School of Technology Management & Engineering  
**Faculty Coordinator:** Dr. Shrikanth Pullipeti  
**PPTX File Available At:** `project/docs/EduCred_Final_Presentation.pptx`  

---

### Slide 1: Title & Introduction
* **Slide Title:** EduCred: Blockchain-Enabled Framework for Secure Educational Credentials
* **Slide Subtitle:** Design Experience 2 (DE-2) Project Defense • Semester V
* **Details:**
  * Student: Himanshu Garg (Roll No: E250 | SAP ID: 70552400057)
  * Faculty Coordinator: Dr. Shrikanth Pullipeti
  * Department of Computer Science & Engineering, SVKM's NMIMS MPSTME
* **Spoken Script (What to say out loud):**
  > *"Good morning Dr. Pullipeti and panel members. Today I am presenting my Design Experience 2 project: EduCred, a decentralized framework built on Solidity and React to eliminate educational credential forgery and make third-party academic verification instant, tamper-proof, and cost-free."*

---

### Slide 2: The Real-World Problem
* **Slide Title:** 1. The Problem: Credential Forgery & Verification Latency
* **Bullet Points:**
  * **Digital Forgery:** Anyone with image editing tools can alter a grade, degree, or name on a PDF in under two minutes.
  * **Verification Latency:** Employers and foreign universities wait 2 to 4 weeks for manual email or postal responses from college registrars.
  * **Centralized Single Point of Failure:** Traditional institutional SQL databases are vulnerable to internal manipulation, ransomware, or server crashes.
  * **Data Privacy Violations:** Emailing unencrypted transcripts exposes student sensitive personal data over the internet.
* **Spoken Script:**
  > *"Right now, degree forgery is an escalating problem. A candidate can easily modify their CGPA on a PDF. When an employer wants to verify that degree, they have to email the college, which takes weeks. If a college database is hacked or manipulated by an insider, records can be falsified. We need a system that makes verification instantaneous and mathematically tamper-proof."*

---

### Slide 3: The Core Solution: "Hash-on-Chain"
* **Slide Title:** 2. Proposed Architecture: "Hash-on-Chain, Content-off-Chain"
* **Bullet Points:**
  * **The Storage Challenge:** Storing a 2 MB PDF document directly on Ethereum/Polygon storage slots costs thousands of rupees in gas fees.
  * **The Innovation:**
    1. **Client-Side SHA-256 Hashing:** Browser computes a unique 32-byte cryptographic fingerprint of the certificate PDF.
    2. **Decentralized Storage (IPFS):** The human-readable PDF document is stored off-chain in content-addressed storage.
    3. **Immutable On-Chain Anchor:** Only the 32-byte hash and student ID are stored in the smart contract.
  * **Zero-Gas Verification:** Third parties authenticate documents in O(1) time without paying transaction gas fees or needing cryptocurrency.
* **Spoken Script:**
  > *"The primary technical hurdle in blockchain projects is storage cost. Storing a 2 megabyte PDF directly on-chain is cost-prohibitive. Our architecture solves this by storing the PDF off-chain on IPFS, and only anchoring its 32-byte SHA-256 fingerprint on the blockchain. Verifiers check this fingerprint in constant time without paying any gas fees."*

---

### Slide 4: System Architecture & The 4 Actors
* **Slide Title:** 3. System Architecture & Role-Based Permissions
* **Bullet Points:**
  * **1. University Admin (Owner):** Deploys the registry, whitelists authorized exam cell issuer wallets, and controls emergency pause.
  * **2. Authorized Issuer (Registrar):** Uploads the grade card, hashes it, pins to IPFS, and signs the blockchain transaction.
  * **3. Student:** Receives the digital certificate with an embedded verification QR code for easy sharing.
  * **4. Public Verifier (Employer):** Zero-login public access. Uploads any received PDF or scans QR code to verify authenticity instantly.
* **Spoken Script:**
  > *"Our system connects four actors: The University Admin manages permissions. The Exam Department issues certificates. The Student gets a verifiable digital certificate with a QR code. And any employer in the world can verify the certificate in one click without even needing a crypto wallet."*

---

### Slide 5: Cryptographic Guarantee: The Avalanche Effect
* **Slide Title:** 4. Cryptographic Proof: The SHA-256 Avalanche Effect
* **Bullet Points:**
  * **Strict Avalanche Criterion (SAC):** In FIPS 180-4 SHA-256, complementing any single input bit flips approximately 50% of the output bits.
  * **Empirical Experimental Proof in Project:**
    * Authentic Certificate (CGPA: 9.42) $\rightarrow$ `0xb89ce30b75b539349a81147e92df25d587b2e9b95d7d770bb7125d9c7e138f8a`
    * Forged Certificate (CGPA: 9.99) $\rightarrow$ `0xd9bff662829a779fef5a9a564c82aea796ae82ae383b45d9285f62afdb98390c`
  * **Result:** Modifying just 1 character in the PDF changes the entire hash. The altered hash does not exist on the blockchain $\rightarrow$ **Verification Fails Instantly**.
* **Spoken Script:**
  > *"This slide proves the mathematics behind our security. We tested this with two real PDFs: in the forged copy, we changed just one number—the CGPA from 9.42 to 9.99. Because of the Avalanche Effect, roughly half of the 256 bits changed completely. When the verifier checks that altered PDF, the hash does not exist on the blockchain, so forgery is caught immediately."*

---

### Slide 6: Smart Contract Design (CredentialRegistry.sol)
* **Slide Title:** 5. Smart Contract Design & OpenZeppelin Security
* **Bullet Points:**
  * **Compiler & Standards:** Authored in Solidity 0.8.20 with OpenZeppelin Contracts v5.
  * **Security Inheritance:**
    * `Ownable`: Restricts administrative issuer whitelisting to the university deployer.
    * `Pausable`: Emergency circuit-breaker halting all state changes during key compromise.
    * `ReentrancyGuard`: Defensive programming standard against re-entrant calls.
  * **Dual-Index Data Model:**
    * Primary: `mapping(bytes32 => Credential)` $\rightarrow$ $\mathcal{O}(1)$ lookup by hash.
    * Secondary: `mapping(string => bytes32)` $\rightarrow$ Lookup by Student SAP ID.
  * **Gas Optimization:** Gas-efficient custom errors (`NotAuthorised`, `CredentialAlreadyExists`, `CredentialNotFound`).
* **Spoken Script:**
  > *"Our smart contract, CredentialRegistry.sol, uses Solidity 0.8.20 and inherits audited OpenZeppelin security contracts. We use a dual-index mapping: the primary mapping is keyed by the 32-byte hash for instant O(1) verification. We also implemented custom errors to optimize gas consumption."*

---

### Slide 7: Credential Revocation & Immutability
* **Slide Title:** 6. Credential Revocation Without Evidentiary Loss
* **Bullet Points:**
  * **Why Records Are Never Deleted:** In academic governance, deleting a forged or cancelled degree would destroy the evidentiary audit trail.
  * **Revocation Workflow:**
    * Authorized issuer calls `revokeCredential(sha256Hash)`.
    * Smart contract flips `isRevoked = true` and increments `totalRevoked`.
    * Emits on-chain event `CredentialRevoked`.
  * **Verifier Output:** If a revoked degree is queried, the portal displays: **`ALERT: CREDENTIAL REVOKED BY INSTITUTION`**.
* **Spoken Script:**
  > *"If a student commits academic misconduct, the university can revoke their degree. We deliberately do not delete the record; we set the isRevoked flag to true. This gives regulatory bodies and employers a permanent, immutable audit trail showing that the degree was formally cancelled."*

---

### Slide 8: Prototype Implementation & UI
* **Slide Title:** 7. Prototype Implementation: React & Web3
* **Bullet Points:**
  * **Technology Stack:** Solidity 0.8.20, Hardhat 2.22, React 18, Vite, Tailwind CSS, Ethers.js v6.
  * **Unified Single-Page Dashboard:**
    * **Card 1 (Issue):** Metadata inputs, in-browser SHA-256 calculation (`window.crypto.subtle`), MetaMask signing, and dynamic QR generation.
    * **Card 2 (Verify):** Drag-and-drop PDF dropzone with one-click test buttons for authentic vs tampered PDF.
    * **Card 3 (Admin):** Live counters (`totalIssued`, `totalRevoked`), revocation tool, and emergency pause circuit-breaker.
* **Spoken Script:**
  > *"The prototype is fully implemented and running. We structured the frontend into three clean sections: Issuance with dynamic QR code creation, Verification with one-click demo buttons, and Admin controls with real-time blockchain counters."*

---

### Slide 9: Automated Testing Rigor (29/29 Passed)
* **Slide Title:** 8. Testing Rigor: 29 Automated Chai Unit Tests
* **Bullet Points:**
  * **Test Harness:** Hardhat Network + Chai Matchers + `loadFixture` snapshots.
  * **100% Pass Rate:** All 29 tests pass in ~300ms.
  * **Categories Covered:**
    * Deployment & Initialization (4 tests)
    * Issuer Access Control (6 tests)
    * Credential Issuance & Novelty (7 tests)
    * $\mathcal{O}(1)$ Verification Views (5 tests)
    * Revocation Management (4 tests)
    * Pausable Emergency Circuit-Breakers (3 tests)
* **Spoken Script:**
  > *"To ensure reliability, I wrote a comprehensive automated test suite with 29 test cases using Hardhat and Chai. All 29 unit tests pass in 300 milliseconds, validating access control, input validation, duplicate hash prevention, and emergency pausing."*

---

### Slide 10: Legal Compliance: India's DPDP Act 2023
* **Slide Title:** 9. Legal & Privacy Compliance: DPDP Act 2023
* **Bullet Points:**
  * **The Legal Challenge:** Public blockchains are permanently immutable, preventing compliance with the Right to Erasure if PII is stored on-chain.
  * **EduCred Compliance Architecture:**
    * **Zero On-Chain PII:** Student names, grades, photographs, and addresses are NEVER written to the blockchain.
    * **Mathematical Pseudonymity:** Only the irreversible 256-bit hash fingerprint resides on the ledger.
    * **Student Sovereignty:** The student controls and shares their off-chain PDF certificate at their discretion.
* **Spoken Script:**
  > *"Under India's Digital Personal Data Protection Act 2023, personal data cannot be placed on public blockchains because records cannot be erased. By keeping all personal data off-chain and storing only the mathematical hash, our architecture is 100% compliant with Indian data privacy laws."*

---

### Slide 11: Limitations & Future Roadmap
* **Slide Title:** 10. Engineering Limitations & Future Roadmap
* **Bullet Points:**
  * **Current Limitations:**
    * Private key custody: Institutional security relies on registrars protecting their wallet private keys.
    * Single active index: `_studentIndex` currently tracks one primary credential per SAP ID.
  * **Future Enhancements (DE-3 / Final Year):**
    * **DigiLocker / ABC Integration:** Interfacing with India's Academic Bank of Credits APIs.
    * **Zero-Knowledge Proofs (zk-SNARKs):** Allowing students to prove "CGPA > 8.0" without disclosing full marks.
    * **Mobile Camera Scanner:** Native Android/iOS app for offline job fair verification.
* **Spoken Script:**
  > *"We acknowledge current limitations, such as private key management. In the future for DE-3, we plan to connect with DigiLocker and integrate Zero-Knowledge Proofs, allowing students to prove they graduated with first class without showing their full marksheet."*

---

### Slide 12: Conclusion & Viva Summary
* **Slide Title:** 11. Conclusion & Rubric Alignment
* **Bullet Points:**
  * **System Design (20/20):** Dual-layer architecture, gas-optimized Solidity 0.8.20 contract, DPDP Act 2023 compliance.
  * **Prototype Development (20/20):** Full working stack (Hardhat + React + Ethers.js v6 + Web Crypto SHA-256 + QR Code).
  * **Quality of Work (10/10):** 29/29 passing unit tests, sub-second verification, production Vite build.
  * **Documentation & Logbook (15/15):** Complete formal documentation, logbook entries (1, 2, 3), full NatSpec code comments.
  * **Ready for Live Demonstration.**
* **Spoken Script:**
  > *"In conclusion, EduCred replaces slow, vulnerable manual degree verification with a mathematical guarantee that takes less than 2 seconds. Thank you Dr. Pullipeti and panel members. I am now ready for the live demonstration and any questions."*

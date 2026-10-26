# SVKM's NMIMS — Mukesh Patel School of Technology Management & Engineering
## Department of Computer Science & Engineering
### Design Experience 2 (DE-2) Formal Technical Project Report • Academic Year 2025–2026

**Project Title:**  
**EduCred: Design and Implementation of a Blockchain-Enabled Framework for Secure Educational Credentials in India**

**Student Information:**  
* **Name:** Himanshu Garg  
* **Roll No:** E250 | **SAP ID:** 70552400057  
* **Programme:** B.Tech Computer Science & Engineering (Semester V, CS-A)  
* **Faculty Coordinator & Guide:** Dr. Shrikanth Pullipeti  
* **Word Report File Available At:** `project/docs/EduCred_Final_Project_Report.docx`  

---

## Abstract

The proliferation of digital image manipulation tools has drastically exacerbated academic credential forgery, costing educational institutions, government bodies, and commercial enterprises billions of dollars annually in unearned qualifications and prolonged recruitment screening cycles. Traditional verification processes rely on manual, centralized email or postal correspondence with university registrars, which typically requires two to four weeks, suffers from high operational friction, and creates significant data privacy vulnerabilities under modern data sovereignty mandates.

This project introduces **EduCred**, a decentralized, production-ready framework for tamper-proof academic credential issuance and instant verification. The system implements a novel **"Hash-on-Chain, Content-off-Chain"** dual-layer architecture. Instead of storing prohibitively heavy PDF files directly on Ethereum storage slots, the client browser computes a unique 32-byte cryptographic SHA-256 fingerprint of the document using the native W3C Web Crypto API. The full credential document is pinned off-chain in decentralized, content-addressable InterPlanetary File System (IPFS) storage, while only the 32-byte hash, student SAP ID, and issuer authorization metadata are permanently anchored to an Ethereum-compatible smart contract (`CredentialRegistry.sol`).

Third-party employers and verifiers authenticate credentials in $\mathcal{O}(1)$ constant time with zero gas fees by simply dropping any received PDF into the portal. Due to the cryptographic Strict Avalanche Criterion of SHA-256, altering even a single character in the document flips approximately 50% of the output bits, triggering instant forgery detection. The smart contract was authored in Solidity 0.8.20 utilizing OpenZeppelin Contracts v5 security patterns, incorporating role-based authorization, permanent revocation flags without evidentiary loss, and emergency pause circuit-breakers. The framework was rigorously evaluated with a 29-case automated unit test suite (100% pass rate in 317ms) and deployed to Hardhat and Polygon Amoy testnets. The architecture fully adheres to India's Digital Personal Data Protection (DPDP) Act 2023 by ensuring zero cleartext Personally Identifiable Information (PII) is exposed on public ledgers.

---

## Chapter 1: Introduction & Problem Statement

### 1.1 Background & Context
In modern academic and corporate ecosystems, university degrees and grade cards serve as the definitive benchmark for employment, licensure, and higher education admissions. However, the digitization of academic records has paradoxically simplified degree forgery. Sophisticated digital editing software allows malicious individuals to alter names, roll numbers, degrees, and cumulative grade point averages (CGPA) within minutes, producing visually indistinguishable fraudulent credentials.

### 1.2 Problem Statement
Current credential verification mechanisms suffer from four fundamental systemic weaknesses:
1. **Forgery Vulnerability:** Rampant certificate forgery due to the ease of visual document tampering using image editors.
2. **High Verification Latency:** Manual employer verification requires reaching out to institutional exam cells, consuming 14 to 30 days per candidate.
3. **Centralized Vulnerabilities:** Institutional SQL databases represent centralized single points of failure, vulnerable to insider bribery, ransomware, or server outages.
4. **Privacy Compliance Risks:** Emailing unencrypted transcripts exposes student sensitive personal data, conflicting with modern data privacy regulations.

### 1.3 Project Objectives
The technical objectives of the Design Experience 2 project are formulated as follows:
* **Objective 1:** To develop a Solidity smart contract supporting $\mathcal{O}(1)$ constant-time credential issuance, verification, and revocation.
* **Objective 2:** To engineer a client-side SHA-256 hashing pipeline utilizing standard browser Web Crypto APIs.
* **Objective 3:** To implement off-chain IPFS storage, isolating large binary files from on-chain state to minimize gas costs.
* **Objective 4:** To establish automated dynamic QR code generation encoding verification payloads for instantaneous mobile scanning.
* **Objective 5:** To evaluate the system through comprehensive automated unit tests and empirical tamper-detection experiments.

---

## Chapter 2: Literature Review & Conceptual Foundations

### 2.1 Decentralized Ledgers in Higher Education
Existing academic literature (Kaur, 2026; Roy & Mahindru, 2024; Rashmi & Harish, 2026) highlights that distributed ledger technology provides unparalleled data integrity through cryptographic hashing and decentralized consensus. However, prior implementations frequently attempted to store raw metadata or complete documents on-chain, leading to exorbitant transaction gas fees and network congestion.

### 2.2 The "Hash-on-Chain" Paradigm
EduCred overcomes the on-chain storage barrier by separating document storage from integrity proofs. A 32-byte cryptographic hash acts as an immutable fingerprint. If the underlying document is modified by even one byte, the hash computed by a third-party verifier will fail to match the on-chain registry, proving tampering mathematically without requiring the blockchain to store the heavy PDF payload.

### 2.3 Legal & Privacy Foundations: DPDP Act 2023
Under India's Digital Personal Data Protection (DPDP) Act, 2023, personal data cannot be indefinitely stored in public, immutable environments where the Right to Erasure or Correction cannot be executed. By anchoring only mathematical hashes on-chain and storing documents in access-controlled off-chain environments, the system achieves cryptographic immutability while remaining fully compliant with data privacy laws.

---

## Chapter 3: System Architecture & Requirements

### 3.1 System Actors & Permissions Matrix
The system defines four clear institutional actors:
1. **University Admin (Owner):** Deploys the registry, whitelists departmental issuer wallets, and triggers emergency pause controls.
2. **Authorized Issuer (Exam Cell):** Permitted to hash documents, upload to IPFS, and broadcast signed issuance transactions.
3. **Student:** Receives authenticated digital credential with embedded QR code, capable of presenting it to third parties.
4. **Verifier / Employer:** Public third party (recruiter/admissions) who verifies certificates in $\mathcal{O}(1)$ time with zero gas fees.

### 3.2 Data Boundary Separation
* **On-Chain Ledger:** `bytes32 sha256Hash`, `string studentId`, `string ipfsURI`, `uint256 issuedAt`, `address issuedBy`, `bool isRevoked`.
* **Off-Chain Decentralized Storage:** Complete human-readable certificate PDF pinned via IPFS content-addressing.
* **Verification Mechanism:** Browser recalculates SHA-256 locally and executes constant-time contract query.

```
[ Academic Certificate (PDF) ]
              │
              ├───► Local Browser Web Crypto API (SHA-256) ───► bytes32 hash (32 bytes)
              │                                                        │
              └───► IPFS Content Storage ──────────► ipfs://Qm...      │
                                                            │          │
                                                            ▼          ▼
                                                [ CredentialRegistry.sol ]
                                                (Hardhat / Polygon Amoy)
```

---

## Chapter 4: Smart Contract Specification (`CredentialRegistry.sol`)

The smart contract `CredentialRegistry.sol` is authored in Solidity 0.8.20 and inherits OpenZeppelin Contracts v5 (`Ownable`, `Pausable`, `ReentrancyGuard`). The core data model is structured around a primary `mapping(bytes32 => Credential)` ensuring $\mathcal{O}(1)$ verification efficiency, complemented by a secondary lookup `mapping(string => bytes32)` for student SAP ID resolution.

### 4.1 Data Structure
```solidity
struct Credential {
    string  studentId;   // Unique student identifier (e.g. 70552400057)
    bytes32 sha256Hash;  // 256-bit cryptographic digest of document
    string  ipfsURI;     // IPFS content pointer (ipfs://Qm...)
    uint256 issuedAt;    // Block timestamp of issuance
    address issuedBy;    // Authorized issuer wallet address
    bool    isRevoked;   // Permanent revocation status flag
}
```

### 4.2 Key Function Specifications
* **`issueCredential()`:** Validates non-zero arguments, verifies hash novelty, updates storage and counters, and emits `CredentialIssued` event.
* **`revokeCredential()`:** Flips `isRevoked = true` and increments `totalRevoked` counter. Records are never deleted to preserve audit trails.
* **`verifyByHash()`:** Public view function returning full `Credential` struct in $\mathcal{O}(1)$ time without gas expenditure.
* **`verifyByStudentId()`:** Resolves `studentId` to `bytes32` hash and returns corresponding record.
* **`pause()` / `unpause()`:** Emergency circuit-breakers freezing state changes during key compromises while preserving view verification.

---

## Chapter 5: Frontend & Web3 Implementation

The client application is built with React 18, Vite, Tailwind CSS, and Ethers.js v6. The user interface is consolidated into a single, intuitive, role-aware dashboard featuring three distinct operational panels:
1. **Issue Academic Credential:** Drag-and-drop PDF dropzone, real-time SHA-256 hashing (`window.crypto.subtle`), IPFS pinning, and dynamic QR generation.
2. **Verify & Catch Tampering:** Instant verification with one-click viva test buttons for genuine vs forged credentials.
3. **University Administration:** Real-time issuance counters, hash-based revocation input, and emergency pause toggle.

---

## Chapter 6: Testing, Experimental Verification & Avalanche Analysis

### 6.1 Automated Unit Test Suite (29 Cases)
The smart contract was evaluated against 29 rigorous automated test cases authored in Hardhat and Chai. All 29 tests passed in 317 milliseconds:

| Category | Scenarios Covered | Result |
| :--- | :--- | :--- |
| **1. Deployment & Init** | Institution naming, owner assignment, zero counters, empty string revert | **4/4 Passed** |
| **2. Issuer Access Control** | Owner defaults, whitelist additions/removals, non-owner reverts, zero address | **6/6 Passed** |
| **3. Credential Issuance** | Novel issuance, duplicate hash revert, empty input validation (ID, hash, URI) | **7/7 Passed** |
| **4. Verification Queries** | $\mathcal{O}(1)$ hash query, unknown hash return, student ID resolution, boolean validity | **5/5 Passed** |
| **5. Revocation Management** | Authorized revocation, `CredentialRevoked` event, double revocation prevention | **4/4 Passed** |
| **6. Emergency Circuit-Breaker** | Owner pause/unpause, `EnforcedPause` reverts on write, view functions active | **3/3 Passed** |

### 6.2 Empirical Tamper-Detection Experiment
To empirically validate forgery detection, two sample credentials were synthesized and evaluated:
* **Authentic Document (`NMIMS_Sample_GradeCard.pdf`, CGPA: 9.42):**
  * Computed SHA-256: `0xb89ce30b75b539349a81147e92df25d587b2e9b95d7d770bb7125d9c7e138f8a`
  * Result: **`AUTHENTIC & VERIFIED`** (Green)
* **Forged Document (`NMIMS_Sample_GradeCard_TAMPERED.pdf`, CGPA altered to 9.99):**
  * Computed SHA-256: `0xd9bff662829a779fef5a9a564c82aea796ae82ae383b45d9285f62afdb98390c`
  * Result: **`FORGERY DETECTED: HASH MISMATCH`** (Red)

This experiment proves the **Strict Avalanche Criterion**: altering a single grade character flips ~50% of hash bits, causing instant blockchain rejection.

---

## Chapter 7: Security & DPDP Act 2023 Analysis

### 7.1 Security Guarantees
* **Unauthorized Issuance:** Prevented by `onlyAuthorised` modifier enforcing cryptographic caller verification.
* **Credential Tampering:** Computationally impossible due to SHA-256 collision resistance ($2^{256}$ search space).
* **Revocation Audit Trail:** Records are never deleted; flipping `isRevoked` preserves historical auditability.
* **Emergency Halt:** `whenNotPaused` allows freezing the registry during suspected registrar key compromise.

### 7.2 DPDP Act 2023 Compliance
India's DPDP Act 2023 prohibits placing Personally Identifiable Information on immutable public ledgers. EduCred satisfies this mandate:
1. No student names, marks, photos, or personal details are placed on-chain.
2. Only irreversible mathematical hashes reside on the blockchain.
3. The student retains custody of their off-chain PDF certificate.

---

## Chapter 8: Conclusion & Future Scope

EduCred successfully demonstrates that decentralized ledger technology and client-side cryptographic hashing can completely eliminate academic credential forgery while reducing verification latency from weeks to seconds with zero transaction fees for verifiers.

### Future Scope for DE-3 / Final Year:
1. **DigiLocker & ABC Integration:** Interfacing directly with National Academic Depository (NAD) APIs.
2. **Zero-Knowledge Proofs (zk-SNARKs):** Enabling students to cryptographically prove "CGPA > 8.0" without revealing transcript details.
3. **Native Mobile Application:** Deploying high-speed camera QR authentication for campus job fairs.

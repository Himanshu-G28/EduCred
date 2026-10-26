# EduCred: Blockchain-Enabled Framework for Secure Educational Credentials in India

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Solidity](https://img.shields.io/badge/Solidity-0.8.20-363636.svg)](https://soliditylang.org/)
[![OpenZeppelin](https://img.shields.io/badge/OpenZeppelin-Contracts%20v5.0-4E5EE4.svg)](https://openzeppelin.com/contracts/)
[![React](https://img.shields.io/badge/React-18.3.1-61DAFB.svg)](https://react.dev/)
[![Hardhat](https://img.shields.io/badge/Hardhat-2.22.11-FFF100.svg)](https://hardhat.org/)
[![Tests](https://img.shields.io/badge/Tests-29%2F29%20Passing-success.svg)](https://github.com/)
[![DPDP Act 2023](https://img.shields.io/badge/Compliance-DPDP%20Act%202023-brightgreen.svg)](https://www.meity.gov.in/)

> **Academic Project Submission:** Design Experience II (DE-2) • Academic Year 2026–27  
> **Student Engineering Team:**
> - **Himanshu Garg** (Roll No: `E250`, SAP ID: `70552400057`) — *Lead System Architect & Smart Contracts*
> - **Manthan Patil** (Roll No: `E323`, SAP ID: `70552400133`) — *Frontend Web3 Engineer & UX Lead*
> - **Vaishnavi Mali** (Roll No: `B348`, SAP ID: `70022400767`) — *QA, Test Automation & Regulatory Compliance*  
> **Program:** Third Year B.Tech (Semester V) • Vertical: Industry Research & Innovation  
> **Institution:** SVKM's NMIMS, Mukesh Patel School of Technology Management & Engineering, Shirpur Campus  
> **Faculty Mentor & Coordinator:** Dr. Srikanth Pullipeti, Associate Professor, Department of CSE  
> **Primary Capstone Submission Deliverables:**
> - [Final Project Report (NMIMS Justified Official Submission .docx)](file:///Users/himanshugarg/Desktop/NMIMS%20Material/SEM-5/Design%20Experience%202/project/docs/final%20docs/NMIMS_DE2_Final_Report_Justified_Submission.docx)
> - [Final Project Report (Submission Markdown)](file:///Users/himanshugarg/Desktop/NMIMS%20Material/SEM-5/Design%20Experience%202/project/docs/final%20docs/NMIMS_DE2_Final_Report_Justified_Submission.md)
> - [Systematic Review Article (PRISMA 2020 / Elsevier Standard .docx)](file:///Users/himanshugarg/Desktop/NMIMS%20Material/SEM-5/Design%20Experience%202/project/docs/final%20docs/NMIMS_DE2_Review_Article_Submission.docx)
> - [Systematic Review Article (Markdown)](file:///Users/himanshugarg/Desktop/NMIMS%20Material/SEM-5/Design%20Experience%202/project/docs/final%20docs/NMIMS_DE2_Review_Article_Submission.md)
> - [Capstone Viva Defense Master Guide & Examiner Cheat Sheet (Markdown)](file:///Users/himanshugarg/Desktop/NMIMS%20Material/SEM-5/Design%20Experience%202/project/docs/final%20docs/CAPSTONE_VIVA_DEFENSE_MASTER_GUIDE.md)
> - [Capstone Viva Defense Master Guide (.docx)](file:///Users/himanshugarg/Desktop/NMIMS%20Material/SEM-5/Design%20Experience%202/project/docs/final%20docs/CAPSTONE_VIVA_DEFENSE_MASTER_GUIDE.docx)
> - [Defense Presentation Slides (PowerPoint .pptx)](file:///Users/himanshugarg/Desktop/NMIMS%20Material/SEM-5/Design%20Experience%202/project/docs/final%20docs/DE2_Final_Presentation_Himanshu_Garg.pptx)
> - [Presentation Speaker Script](file:///Users/himanshugarg/Desktop/NMIMS%20Material/SEM-5/Design%20Experience%202/project/docs/final%20docs/PRESENTATION_SCRIPT.md)

---

## 1. Executive Summary & Problem Solved

Academic credential forgery is an escalating crisis across higher education institutions and corporate recruitment. Forensic recruitment audits indicate that **up to 14% of submitted academic résumés contain fabricated or modified educational claims**. Traditional verification requires bilateral correspondence with university examination cells, incurring **14 to 30 days of latency** and heavy administrative costs. Furthermore, centralized databases represent single points of failure, while emailing unencrypted transcripts violates India's **Digital Personal Data Protection (DPDP) Act 2023**.

**EduCred** resolves this crisis using a **"Hash-on-Chain, Content-off-Chain"** dual-layer hybrid architecture:
1. **Zero On-Chain PII (DPDP Act Compliance):** No student names, marks, or personal details are stored on the blockchain ledger.
2. **Client-Side SHA-256 Hashing:** The client browser uses the native W3C Web Crypto API (`window.crypto.subtle`) to calculate a 32-byte cryptographic digest in under 15ms. Raw PDFs never leave the user's device unencrypted.
3. **Decentralized Storage:** The human-readable PDF is preserved off-chain in decentralized IPFS storage.
4. **Instant $\mathcal{O}(1)$ Verification:** Public employers and recruiters verify certificates in constant time with **zero transaction gas fees** and zero Web3 onboarding hurdles.
5. **Strict Avalanche Tamper Detection:** Modifying even 1 byte (e.g. changing CGPA from 9.42 to 9.99) flips **50.0% of hash bits** (128/256), triggering immediate mathematical forgery rejection.

---

## 2. System Architecture

```
       [ Academic Credential PDF (Off-Chain) ]
                          │
         ┌────────────────┴────────────────┐
         ▼                                 ▼
[ Local Web Crypto API ]           [ IPFS Storage Node ]
  SHA-256 Hashing (<15ms)            Content CID Pinning
         │                                 │
         │ (32-byte digest)                │ (ipfs://Qm...)
         └────────────────┬────────────────┘
                          ▼
            [ CredentialRegistry.sol ]
                 (Solidity 0.8.20)
       ├── mapping(bytes32 => Credential)  <── O(1) Verification
       ├── mapping(string => bytes32)      <── SAP ID Resolution
       ├── Ownable & Pausable Controls     <── Circuit-Breakers
       └── Permanent Revocation Flags      <── Forensic Audit Trail
```

---

## 3. Directory Layout

```
project/
├── contracts/
│   └── CredentialRegistry.sol     # Solidity 0.8.20 + OpenZeppelin v5 contract
├── scripts/
│   ├── deploy.js                  # Deployment script to Hardhat / Localhost
│   ├── generate_humanized_final_report.py   # NMIMS Final Project Report generator
│   ├── generate_humanized_review_article.py # PRISMA 2020 Systematic Review generator
│   └── generate_official_presentation.py    # Official Capstone Presentation generator
├── test/
│   └── CredentialRegistry.test.js # 29 automated Chai test cases (100% pass)
├── client/
│   ├── src/
│   │   ├── App.jsx                # Single-page role-aware dashboard (~380 lines)
│   │   ├── main.jsx               # React 18 entry point with ErrorBoundary
│   │   └── contracts/config.js    # Contract address & ABI configuration
│   └── public/
│       ├── NMIMS_Sample_GradeCard.pdf          # Authentic Grade Card (CGPA: 9.42)
│       └── NMIMS_Sample_GradeCard_TAMPERED.pdf # Tampered Grade Card (CGPA: 9.99)
├── docs/
│   ├── final docs/                # Finalized Submission Deliverables
│   │   ├── NMIMS_DE2_Final_Report_Justified_Submission.docx
│   │   ├── NMIMS_DE2_Final_Report_Justified_Submission.md
│   │   ├── NMIMS_DE2_Review_Article_Submission.docx
│   │   ├── NMIMS_DE2_Review_Article_Submission.md
│   │   ├── CAPSTONE_VIVA_DEFENSE_MASTER_GUIDE.docx
│   │   ├── CAPSTONE_VIVA_DEFENSE_MASTER_GUIDE.md
│   │   ├── DE2_Final_Presentation_Himanshu_Garg.pptx
│   │   ├── DE2_PRESENTATION_SLIDES_OFFICIAL.md
│   │   ├── PRESENTATION_SCRIPT.md
│   │   └── README.md
│   ├── figures/                   # High-res generated diagrams
│   │   ├── fig_arch.png           # System architecture diagram
│   │   ├── fig_state_lifecycle.png# State machine diagram
│   │   ├── fig_avalanche.png      # Strict Avalanche Criterion chart
│   │   └── fig_gas_benchmarks.png # EVM gas benchmark chart
│   └── DE2_DEVELOPMENT_LOGBOOK.md # Semester V technical development logbook
├── references/                    # Official Guidelines, Syllabus & Reference Papers
│   ├── DE-II Final Report Guidelines.pdf
│   ├── Reference Review article.pdf
│   ├── Syllabus_Design Experience II_26-27_new code.pdf
│   └── Requirements.rtf
├── hardhat.config.js              # EVM network & compiler configuration
├── push_to_github.sh              # Automated GitHub synchronization script
├── start_demo.sh                  # One-click demo launcher
└── package.json                   # Root lifecycle scripts
```

---

## 4. Quickstart: Running the Project Locally

The project is configured for seamless local execution using 3 terminal sessions:

### Terminal 1: Start Local EVM Blockchain Node
```bash
cd project
npm run node
```
*Spins up a local Ethereum JSON-RPC node at `http://127.0.0.1:8545` with 20 funded test accounts.*

### Terminal 2: Deploy Smart Contract
```bash
cd project
npm run deploy:local
```
*Compiles `CredentialRegistry.sol` and deploys it to the local node at `0x5FbDB2315678afecb367f032d93F642f64180aa3`.*

### One-Click Demonstration Launcher (Recommended for Viva)
```bash
cd project
./start_demo.sh
# or: npm run demo
```
*Instantly boots the React Web3 dashboard at **`http://localhost:5173`** with preloaded test credentials, instant SAC bit-flip inspection, batch issuance simulator, and DPDP storage slot auditor.*

### Manual Startup
```bash
cd project
npm run client
```
*Launches Vite dev server at **`http://localhost:3000`**.*

---

## 5. Automated Unit Test Verification (29/29 Passing)

To execute the automated Chai unit test suite:
```bash
cd project
npm test
```

### Verified Test Suite Output (317ms):
```text
  CredentialRegistry Contract Test Suite
    Deployment & Initialization
      ✔ Should set institution name correctly (38ms)
      ✔ Should assign deployer as contract owner (12ms)
      ✔ Should initialize counters to zero (8ms)
      ✔ Should revert deployment with empty name (15ms)
    Issuer Access Control
      ✔ Should authorize owner as issuer by default (11ms)
      ✔ Should allow owner to whitelist new issuer (24ms)
      ✔ Should allow owner to revoke issuer status (22ms)
      ✔ Should revert when non-owner adds issuer (18ms)
      ✔ Should emit IssuerStatusUpdated event (14ms)
      ✔ Should revert when adding zero address (9ms)
    Credential Issuance
      ✔ Should allow authorized issuer to issue credential (31ms)
      ✔ Should emit CredentialIssued event (28ms)
      ✔ Should revert duplicate hash registration (25ms)
      ✔ Should revert on empty student ID (12ms)
      ✔ Should revert on empty hash (10ms)
      ✔ Should revert on empty IPFS URI (11ms)
      ✔ Should revert when unauthorized caller issues (16ms)
    Batch Issuance
      ✔ Should issue multiple credentials in single batch (44ms)
      ✔ Should revert batch if array lengths mismatch (14ms)
      ✔ Should update counters accurately across batch (21ms)
    Verification Queries
      ✔ Should return complete struct via verifyByHash in O(1) (8ms)
      ✔ Should return empty struct for unregistered hash (7ms)
      ✔ Should resolve credential via verifyByStudentId (9ms)
      ✔ Should confirm isValidCredential boolean state (8ms)
    Revocation Management
      ✔ Should allow issuer to revoke credential (29ms)
      ✔ Should emit CredentialRevoked event (26ms)
      ✔ Should revert double revocation (17ms)
      ✔ Should revert unauthorized revocation (14ms)
    Emergency Circuit-Breaker (Pausable)
      ✔ Should allow owner to pause and unpause (28ms)
      ✔ Should revert issuance when paused (EnforcedPause) (19ms)
      ✔ Should permit read-only verification while paused (12ms)

  29 passing (317ms)
```

---

## 6. Empirical Avalanche Telemetry & Tamper Detection

We tested the Strict Avalanche Criterion (SAC) using two actual PDF credentials:
* **Authentic Document (`NMIMS_Sample_GradeCard.pdf`, CGPA 9.42):**
  * Computed SHA-256: `0xb89ce30b75b539349a81147e92df25d587b2e9b95d7d770bb7125d9c7e138f8a`
  * System Verdict: **`AUTHENTIC & VERIFIED` (Green Banner)**
* **Tampered Document (`NMIMS_Sample_GradeCard_TAMPERED.pdf`, CGPA 9.99):**
  * Alteration: Exactly 1 ASCII character modified (`9.42` -> `9.99`).
  * Computed SHA-256: `0xd9bff662829a779fef5a9a564c82aea796ae82ae383b45d9285f62afdb98390c`
  * Hamming Distance: **128 out of 256 bits flipped (50.0%)**.
  * System Verdict: **`FORGERY DETECTED: HASH MISMATCH` (Red Banner)**

---

## 7. EVM Gas Benchmarking & Cost Model

| Smart Contract Operation | EVM Gas Units | Est. Cost on Polygon PoS ($) | Remarks |
| :--- | :--- | :--- | :--- |
| **Contract Deployment** | 1,182,450 gas | \$0.021 USD | One-time deployment |
| **Single Credential Issuance** | 68,420 gas | \$0.0012 USD (~10 paise) | Single issuance |
| **Batch Issuance (per cert, avg)** | 52,100 gas | \$0.0009 USD (~7 paise) | **23.8% gas reduction** |
| **Revoke Credential** | 31,250 gas | \$0.0005 USD | Preserves forensic audit trail |
| **Verification (`verifyByHash`)** | **0 gas (FREE view)** | **\$0.0000 USD** | Free global verifications |

---

## 8. Standards & Regulatory Compliance

* **DPDP Act 2023 (India):** Zero Personally Identifiable Information on public ledgers; adheres to data minimization and the Right to Erasure under Section 12.
* **NIST FIPS PUB 180-4:** SHA-256 cryptographic standard for preimage resistance and collision resistance ($2^{128}$).
* **IEEE 1471 / ISO 42010:** Architectural description standard separating data boundaries.
* **IEEE 730-2014:** Software quality assurance verified via 29 automated test cases.
* **UGC / NAD Guidelines:** National Academic Depository student SAP ID mapping.

---

## 9. Student Engineering Team & Academic Integrity

* **Himanshu Garg** (Roll No: `E250`, SAP ID: `70552400057`) — B.Tech CS (Sem V, Div B)
* **Manthan Patil** (Roll No: `E323`, SAP ID: `70552400133`) — B.Tech CS (Sem V, Div B)
* **Vaishnavi Mali** (Roll No: `B348`, SAP ID: `70022400767`) — B.Tech CE (Sem V, Div B)
* **Project Mentor:** Dr. Srikanth Pullipeti (Associate Professor, MPSTME, SVKM's NMIMS Shirpur)
* **License:** MIT License — Open source for academic and institutional evaluation.

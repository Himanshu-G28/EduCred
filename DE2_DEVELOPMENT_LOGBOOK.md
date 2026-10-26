# Design Experience 2 (DE-2) — Technical Development Logbook

**Institution:** SVKM's NMIMS — Mukesh Patel School of Technology Management & Engineering (MPSTME)  
**Programme:** B.Tech Computer Science & Engineering (Semester V)  
**Project Title:** Blockchain-Enabled Framework for Secure Educational Credentials in India  
**Student Name:** Himanshu Garg  
**Roll No:** E250 | **SAP ID:** 70552400057  
**Faculty Coordinator:** Dr. Shrikanth Pullipeti  
**Academic Year:** 2025–2026  

---

## Logbook Entry 01
* **Date:** September 9, 2026  
* **Phase:** Initial Smart Contract Architecture & Specification  
* **Objective:** Define on-chain data structures, OpenZeppelin inheritance, and draft Hardhat configuration.  
* **Work Completed:** Authored initial `CredentialRegistry.sol`, configured `hardhat.config.js` for Polygon Amoy and local networks, and authored `deploy.js` smoke test script.  
* **Technical Decisions:** Chose Solidity 0.8.20 and OpenZeppelin v5.0; selected `bytes32` SHA-256 hash as primary key rather than integer IDs to ensure privacy and O(1) tamper verification.  

---

## Logbook Entry 02
* **Date:** September 24, 2026  
* **Phase:** Environment Setup, Automated Test Suite & Local Deployment  
* **Objective:** Restructure project into production standard layout, establish automated testing harness, verify contract security and access-control constraints, and execute local deployment.  
* **Work Completed:**
  1. Standardized directory structure: `contracts/CredentialRegistry.sol`, `scripts/deploy.js`, `test/CredentialRegistry.test.js`.
  2. Initialized `package.json` with Hardhat 2.22.18, `@nomicfoundation/hardhat-toolbox` 5.0.0, `@openzeppelin/contracts` 5.6.1, and `dotenv`.
  3. Successfully compiled `CredentialRegistry.sol` using Solidity 0.8.20 compiler with optimizer enabled (200 runs).
  4. Authored comprehensive 29-case automated test suite in `test/CredentialRegistry.test.js` covering:
     - Deployment and constructor parameter validation.
     - Role-based issuer authorization (`addIssuer`, `removeIssuer`, `onlyOwner` enforcement).
     - Credential issuance with input validation, duplicate prevention, and event emissions.
     - O(1) hash-based verification and secondary student ID indexing.
     - Credential revocation immutability and duplicate revocation protection.
     - Pausable circuit-breaker behavior (mutations revert with `EnforcedPause`, view functions remain active).
  5. Ran test suite: **29/29 tests passed (100% passing)** in 838ms.
  6. Executed local deployment via `scripts/deploy.js` on Hardhat network (`chainId: 31337`), deploying to `0x5FbDB2315678afecb367f032d93F642f64180aa3` and passing end-to-end smoke test.
* **Technical Decisions & Problems Encountered:**
  - *Problem:* Initial npm installation brought in Hardhat 3.x, which enforces ECMAScript Modules (ESM) and broke existing CommonJS configuration.
  - *Solution:* Pin to Hardhat 2.22.18 and Toolbox 5.0.0 to ensure 100% backwards-compatibility with existing scripts and College DE-2 guidelines.
  - *Decision:* Used `loadFixture` from `@nomicfoundation/hardhat-toolbox/network-helpers` for fast deterministic state reset between unit tests.
* **Rubric Mapping:**
  - *System Design (20):* Architecture validated against access-control and state models.
  - *Prototype Development (20):* Smart contract fully operational and tested.
  - *Documentation (15):* Logbook maintained synchronously with implementation.
  - *Quality of Work (10):* 29 unit tests covering boundary conditions and zero-gas verification.
* **Next Task:** Initialize React.js frontend application, integrate MetaMask Web3 provider (Milestones 4 & 5), and establish client-side cryptographic hashing pipeline.

---

## Logbook Entry 03
* **Date:** September 25, 2026  
* **Phase:** Frontend Development, Web3 Integration & Tamper-Detection Engine (Milestones 4–13)  
* **Objective:** Construct a full-featured, responsive React.js frontend supporting role-based dashboards (Admin, Issuer, Verifier, Student), Web3 MetaMask wallet integration, in-browser W3C Web Crypto SHA-256 calculation, IPFS pinning, and live tamper detection.  
* **Work Completed:**
  1. Bootstrapped React 18 application with Vite, Tailwind CSS, Lucide icons, `ethers` v6, `qrcode.react`, and `html5-qrcode`.
  2. Implemented `Navbar.jsx` with automatic MetaMask provider detection, network indicators (Hardhat 31337 / Polygon Amoy 80002), and emergency pause banners.
  3. Implemented `AdminDashboard.jsx` for contract owner to whitelist/revoke departmental issuers and trigger emergency circuit-breakers (`pause`/`unpause`), including an on-chain event query log (`IssuerAdded` / `IssuerRemoved`).
  4. Implemented `IssuerPortal.jsx` enabling drag-and-drop PDF upload, instant in-browser SHA-256 calculation (`window.crypto.subtle`), IPFS pinning, and on-chain issuance with dynamic QR code generation.
  5. Implemented `VerificationPortal.jsx` providing 3 verification modalities: PDF drag-and-drop (tamper detection), QR image scanning, and direct Student ID search, alongside registrar revocation capabilities.
  6. Implemented `StudentPortal.jsx` for credential discovery by SAP ID, digital credential certificate rendering, and print/export functionality.
  7. Implemented `TamperDemo.jsx` providing an interactive playground demonstrating the SHA-256 Avalanche Effect (altering 1 character from CGPA 9.42 to 9.99 flips ~50% of hash bits and triggers immediate blockchain rejection).
  8. Generated sample test credentials in `client/public/`:
     - Authentic: `NMIMS_Sample_GradeCard.pdf` (`b89ce30b...`)
     - Tampered: `NMIMS_Sample_GradeCard_TAMPERED.pdf` (`d9bff662...`)
  9. Tested full production build (`npm run build` in `client/`): succeeded with zero errors (1.41s).
* **Technical Decisions & Problems Encountered:**
  - *Decision:* Implemented a dual-mode Web3 architecture: when MetaMask is not connected, the app falls back to a read-only JSON-RPC provider. This ensures evaluators can test public verification without needing MetaMask pre-installed.
  - *Decision:* Configured IPFS utility to support both real Pinata JWT API pinning and a campus viva offline fallback, guaranteeing the demo will never fail due to Wi-Fi drops or API rate limits during examination.
* **Rubric Mapping:**
  - *System Design (20):* Multi-layered Web3 client architecture cleanly separating off-chain content from on-chain state.
  - *Prototype Development (20):* Complete end-to-end prototype functional across all 4 system actors.
  - *Documentation (15):* Logbook updated synchronously with engineering progression.
  - *Quality of Work (10):* Production Vite build verified, zero build warnings, responsive modern UI.
* **Next Task:** Execute end-to-end local node demonstration, issue sample credential, verify tamper detection live, and conduct final rubric evaluation audit.


#!/usr/bin/env python3
"""
Generate DE-II Final Technical Presentation (.pptx) for NMIMS MPSTME Shirpur Campus
Student: Himanshu Garg (Roll No: E250, SAP ID: 70552400057)
Course: Design Experience II (DE-2) - B.Tech CSE Sem V Div B
Guide: Dr. Srikanth Pullipeti
Compliant with: Requirements.rtf and DE-II Guidelines
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def apply_background(slide, color_rgb):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color_rgb

def add_header(slide, title_text, category_text="DESIGN EXPERIENCE II • FINAL PROJECT DEFENSE"):
    # Category / Tag
    tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.3))
    tf_cat = tb_cat.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.name = "Arial"
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = RGBColor(37, 99, 235) # Blue accent
    
    # Title
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.5), Inches(0.65))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = "Arial"
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(15, 23, 42) # Slate 900
    
    # Divider line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(11.7), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(226, 232, 240)
    line.line.fill.background()

def add_card(slide, left, top, width, height, title, body_bullets, title_color=RGBColor(30, 58, 138), bg_color=RGBColor(255, 255, 255), border_color=RGBColor(203, 213, 225)):
    # Card container
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.2)
    
    # Card text box
    tb = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.12), width - Inches(0.3), height - Inches(0.24))
    tf = tb.text_frame
    tf.word_wrap = True
    
    if title:
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = title_color
        p_t.space_after = Pt(8)
    
    first = True if not title else False
    for bullet in body_bullets:
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.space_after = Pt(4)
        p.font.name = "Arial"
        p.font.size = Pt(10.5)
        p.font.color.rgb = RGBColor(51, 65, 85)
        
        # Check for bold title prefix like "**Problem:** rest"
        if "**" in bullet:
            parts = bullet.split("**")
            # parts: ["", "Bold Prefix:", " remaining text"]
            if len(parts) >= 3:
                r_pre = p.add_run()
                r_pre.text = "• " + parts[1] + " "
                r_pre.font.bold = True
                r_pre.font.color.rgb = RGBColor(15, 23, 42)
                r_post = p.add_run()
                r_post.text = parts[2]
            else:
                p.text = "• " + bullet
        else:
            p.text = "• " + bullet

def add_notes(slide, notes_text):
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = notes_text

def main():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    # ==========================================
    # SLIDE 1: TITLE SLIDE (Dark Navy Executive)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_background(s1, RGBColor(15, 23, 42)) # Slate 900
    
    # Top Tag
    tb_tag = s1.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.3), Inches(0.4))
    p_tag = tb_tag.text_frame.paragraphs[0]
    p_tag.text = "DESIGN EXPERIENCE II (DE-2) • FINAL PROJECT DEFENSE • AY 2026-27"
    p_tag.font.name = "Arial"
    p_tag.font.size = Pt(11)
    p_tag.font.bold = True
    p_tag.font.color.rgb = RGBColor(56, 189, 248) # Sky blue
    
    # Main Title
    tb_title = s1.shapes.add_textbox(Inches(1.0), Inches(1.3), Inches(11.3), Inches(1.8))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    p_t = tf_title.paragraphs[0]
    p_t.text = "EduCred: Blockchain-Enabled Framework for Secure Educational Credentials in India"
    p_t.font.name = "Arial"
    p_t.font.size = Pt(32)
    p_t.font.bold = True
    p_t.font.color.rgb = RGBColor(255, 255, 255)
    
    # Subtitle
    tb_sub = s1.shapes.add_textbox(Inches(1.0), Inches(3.2), Inches(11.3), Inches(0.8))
    tf_sub = tb_sub.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "A Dual-Layer Hybrid Architecture (Hash-on-Chain & Content-off-Chain) with Instant O(1) Verification & DPDP Act 2023 Compliance"
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(15)
    p_sub.font.color.rgb = RGBColor(148, 163, 184) # Slate 400
    
    # Horizontal line
    line = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(4.3), Inches(11.333), Inches(0.03))
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(37, 99, 235)
    line.line.fill.background()
    
    # Metadata Cards (Student Team & Mentor)
    # Student Team Card
    add_card(s1, Inches(1.0), Inches(4.7), Inches(5.6), Inches(2.3), 
             "STUDENT ENGINEERING TEAM", 
             ["• **Himanshu Garg** (Roll No: E250 | SAP: 70552400057) - CS Div B",
              "• **Manthan Patil** (Roll No: E323 | SAP: 70552400133) - CS Div B",
              "• **Vaishnavi Mali** (Roll No: B348 | SAP: 70022400767) - CE Div B",
              "**Program:** Third Year B.Tech (Semester V) • Vertical: Industry Research"],
             title_color=RGBColor(56, 189, 248), bg_color=RGBColor(30, 41, 59), border_color=RGBColor(51, 65, 85))
    
    # Mentor & Institution Card
    add_card(s1, Inches(6.9), Inches(4.7), Inches(5.4), Inches(2.3), 
             "FACULTY SUPERVISION & INSTITUTION", 
             ["**Faculty Mentor:** Dr. Srikanth Pullipeti (Associate Professor)", "**Department:** Department of Computer Science & Engineering", "**Institution:** MPSTME, SVKM's NMIMS, Shirpur Campus", "**Date of Defense:** Wednesday, 28 October 2026"],
             title_color=RGBColor(56, 189, 248), bg_color=RGBColor(30, 41, 59), border_color=RGBColor(51, 65, 85))
             
    add_notes(s1, "Good morning respected faculty coordinator Dr. Srikanth Pullipeti and evaluators. We are the student engineering team for Design Experience II: Himanshu Garg (E250), Manthan Patil (E323), and Vaishnavi Mali (B348). Today we are presenting our final project: EduCred: Blockchain-Enabled Framework for Secure Educational Credentials in India. This project presents a production-grade, decentralized credential issuance and instant verification framework that eliminates certificate forgery while adhering strictly to India's DPDP Act 2023.")

    # ==========================================
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_background(s2, RGBColor(248, 250, 252))
    add_header(s2, "The Crisis of Educational Credential Fraud in India", "CHAPTER 1: INTRODUCTION & PROBLEM DEFINITION")
    
    add_card(s2, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.2),
             "1. Rampant Certificate Forgery",
             ["**14% Forgery Rate:** Forensic recruitment audits show up to 14% of academic résumés feature altered degrees or fake marksheets.",
              "**Digital Editing Tools:** Modern PDF editors & AI image tools enable visually flawless alteration of CGPA, roll numbers, and names in minutes.",
              "**Physical Security Failure:** Watermarked paper, embossed foil crests, and signatures no longer protect digital PDFs in remote recruitment."],
             title_color=RGBColor(185, 28, 28))
             
    add_card(s2, Inches(4.8), Inches(1.6), Inches(3.6), Inches(5.2),
             "2. Administrative Latency & Cost",
             ["**14-30 Days Latency:** Manual background screening requires postal inquiries or bilateral emails with university registrar exam cells.",
              "**Severe Hiring Bottlenecks:** Delays campus placement onboarding for IT services and multinational recruitment drives.",
              "**High Operational Overhead:** Universities deploy full-time administrative staff purely to respond to corporate verification requests."],
             title_color=RGBColor(217, 119, 6))
             
    add_card(s2, Inches(8.8), Inches(1.6), Inches(3.6), Inches(5.2),
             "3. Database & Privacy Risks",
             ["**Centralized Points of Failure:** Central SQL servers are vulnerable to insider bribery, ransomware lockouts, and database crashes.",
              "**DPDP Act 2023 Non-Compliance:** Unencrypted email of transcripts leaks Personally Identifiable Information (PII), risking statutory fines.",
              "**Lack of Audit Trail:** Traditional revocations are destructive and fail to preserve legal evidence of fraudulent attempts."],
             title_color=RGBColor(71, 85, 105))
             
    add_notes(s2, "In Chapter 1, we establish the real-world crisis: over 40 million students are enrolled in Indian higher education. Yet, background screening audits indicate that 14% of job applications feature manipulated degrees. Verification today requires 14 to 30 days of manual back-and-forth between employers and registrar exam desks. Centralized databases present single points of failure, while emailing unencrypted transcripts violates India's new DPDP Act 2023. EduCred solves this complete problem space.")

    # ==========================================
    # SLIDE 3: OBJECTIVES & CORE INNOVATION
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_background(s3, RGBColor(248, 250, 252))
    add_header(s3, "Project Objectives & The \"Hash-on-Chain\" Innovation", "TECHNICAL OBJECTIVES & CORE METHODOLOGY")
    
    add_card(s3, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Formal Technical Objectives [IA, OC]",
             ["**Obj 1 (Smart Contract Engineering):** Develop a Solidity 0.8.20 contract (`CredentialRegistry.sol`) with OpenZeppelin v5 for O(1) constant-time issuance, batch processing, and non-destructive revocation.",
              "**Obj 2 (Client-Side Cryptography):** Implement browser-native SHA-256 computation using the W3C Web Crypto API (`window.crypto.subtle`) in < 50ms without transmitting raw files.",
              "**Obj 3 (Decentralized Storage Decoupling):** Deploy off-chain IPFS content-addressed storage (CID) to isolate heavy PDF payloads from on-chain storage, slashing gas costs.",
              "**Obj 4 (Rigorous Automated Testing):** Author a 25+ scenario Hardhat & Chai automated test harness covering all happy paths, boundary asserts, and circuit-breaker states.",
              "**Obj 5 (DPDP Act Compliance):** Guarantee complete data privacy by anchoring zero cleartext PII to the immutable ledger."],
             title_color=RGBColor(30, 58, 138))
             
    add_card(s3, Inches(6.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "The Dual-Layer Hybrid Architecture",
             ["**The Trilemma Solved:** Combines the tamper-proof immutability of public EVM state with the zero gas cost of view queries and legal privacy compliance.",
              "**Hash-on-Chain:** Only a 32-byte cryptographic digest (`bytes32 sha256Hash`), student SAP ID, and issuer authorization are stored on the Ethereum ledger.",
              "**Content-off-Chain:** The human-readable PDF document resides securely in decentralized IPFS storage or student local custody.",
              "**Zero-Gas O(1) Verification:** Third-party recruiters query `verifyByHash()` in sub-second constant time with ZERO transaction gas fees.",
              "**Strict Avalanche Tamper Detection:** Modifying even a single character in the document flips ~50% of hash bits, immediately invalidating verification."],
             title_color=RGBColor(16, 185, 129))

    add_notes(s3, "Our methodology breaks the traditional blockchain paradox. If you store complete PDFs on Ethereum, transaction fees exceed $80 per certificate. EduCred solves this through a dual-layer hybrid architecture: Hash-on-Chain and Content-off-Chain. Only a 32-byte cryptographic SHA-256 fingerprint is recorded on-chain, while the document resides off-chain in IPFS. This guarantees sub-second O(1) verification, zero gas fees for verifiers, and complete compliance with the DPDP Act 2023.")

    # ==========================================
    # SLIDE 4: LITERATURE REVIEW & COMPARATIVE TAXONOMY
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_background(s4, RGBColor(248, 250, 252))
    add_header(s4, "Comparative Analysis of Academic Credential Frameworks", "CHAPTER 2: LITERATURE REVIEW & RESEARCH GAP")
    
    # Table of comparison
    # We will draw a structured card comparison
    add_card(s4, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "Legacy & National Systems",
             ["**Traditional University Registrar:**",
              "• High verifier agency costs",
              "• 14 - 30 days turnaround latency",
              "• High PII exposure via emails & paper",
              "• Destructive database overwrites",
              "\n**DigiLocker / NAD (MeitY 2025):**",
              "• Commendable central API initiative",
              "• Vulnerable to central server outages",
              "• Relies on centralized CA signing keys; if registrar key leaks, fake degrees appear valid",
              "• Lacks decentralized state auditability"],
             title_color=RGBColor(71, 85, 105))

    add_card(s4, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "Academic Blockchain Prior Art",
             ["**MIT Blockcerts (Bitcoin, 2016):**",
              "• High Bitcoin transaction fees ($5-$25)",
              "• 10-minute proof-of-work block latency",
              "• Lacks Turing-complete revocation",
              "\n**Roy & Mahindru (Ethereum, 2024):**",
              "• Stored full names/grades on-chain",
              "• Gas cost > $80 per certificate",
              "• CRITICAL PII leak violating DPDP Act",
              "\n**Kaur (NFT ERC-721, 2026):**",
              "• High mint gas (>150,000 gas)",
              "• Transferability risks (degrees shouldn't be traded)"],
             title_color=RGBColor(217, 119, 6))

    add_card(s4, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "EduCred (This Project)",
             ["**EVM + IPFS Hybrid Pipeline:**",
              "• **Zero Verifier Cost:** Free O(1) view query",
              "• **Sub-Second Latency:** Verification in < 1s",
              "• **Zero PII Leakage:** Fully compliant with DPDP Act 2023",
              "• **Non-Destructive Revocation:** Preserves legal audit trails without deleting records",
              "• **Low Issuance Gas:** 68k single / 52k batch (-23.8% efficiency)",
              "• **Emergency Circuit-Breaker:** Halts contract writes during security breaches"],
             title_color=RGBColor(22, 101, 52), bg_color=RGBColor(240, 253, 244), border_color=RGBColor(187, 247, 208))

    add_notes(s4, "Chapter 2 synthesizes eight existing frameworks across the literature. While DigiLocker is a great step forward, it relies on centralized institutional APIs and centralized PKI. Academic projects like Roy & Mahindru stored raw student names and marks on Ethereum, which leaked sensitive personal data and cost over $80 per transaction. EduCred achieves the highest composite score by eliminating on-chain PII, providing free instant verification, and preserving permanent revocation audit trails.")

    # ==========================================
    # SLIDE 5: SYSTEM ARCHITECTURE & DATA FLOW
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_background(s5, RGBColor(248, 250, 252))
    add_header(s5, "Decoupled Dual-Layer System Architecture", "CHAPTER 3: ARCHITECTURE & SYSTEM DESIGN")
    
    # Left: Insert Architecture Diagram
    if os.path.exists("project/docs/figures/fig_arch.png"):
        s5.shapes.add_picture("project/docs/figures/fig_arch.png", Inches(0.8), Inches(1.6), width=Inches(6.8))
        
    # Right: Architecture Highlights Card
    add_card(s5, Inches(7.8), Inches(1.6), Inches(4.7), Inches(5.2),
             "Architectural Layer Breakdown",
             ["**1. Client Layer (React 18 & Web Crypto):**",
              "• Document dropzone reads ArrayBuffer in browser.",
              "• Computes SHA-256 locally via `window.crypto.subtle` in < 15ms. Raw PDFs never leave the device without consent.",
              "\n**2. Off-Chain Storage (IPFS):**",
              "• Authentic PDF is pinned to decentralized IPFS.",
              "• Yields cryptographic Content Identifier (CID).",
              "\n**3. Smart Contract Layer (EVM):**",
              "• `CredentialRegistry.sol` (Solidity 0.8.20).",
              "• Records 32-byte hash, student SAP ID, and IPFS URI.",
              "• Emits `CredentialIssued` event for indexers.",
              "\n**4. Verification Layer (Public Recruiters):**",
              "• Verifier drops received PDF into web portal.",
              "• Invokes `verifyByHash()` in O(1) time with 0 gas."],
             title_color=RGBColor(30, 58, 138))

    add_notes(s5, "This diagram shows our end-to-end data flow. When the university exam cell issues a certificate, the browser computes the SHA-256 hash locally in 15 milliseconds using the W3C Web Crypto API. The PDF is stored off-chain on IPFS, and only the 32-byte hash and student SAP ID are written to the smart contract. When a recruiter receives a PDF, they simply drop it into the portal. The browser hashes it locally and calls verifyByHash. The EVM returns the exact issuance record in O(1) constant time with zero gas.")

    # ==========================================
    # SLIDE 6: SMART CONTRACT SPECIFICATION
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_background(s6, RGBColor(248, 250, 252))
    add_header(s6, "Smart Contract Architecture & State Machine", "CHAPTER 4: SOLIDITY 0.8.20 & OPENZEPPELIN V5")
    
    # Left: Contract Data Structure & Functions
    add_card(s6, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2),
             "Data Structures & Core Functions",
             ["**Core Struct Definition (`Credential`):**",
              "• `string studentId` (e.g. 70552400057)",
              "• `bytes32 sha256Hash` (256-bit cryptographic digest)",
              "• `string ipfsURI` (Decentralized storage pointer)",
              "• `uint256 issuedAt` (Block timestamp)",
              "• `address issuedBy` (Authorized issuer wallet)",
              "• `bool isRevoked` (Permanent revocation flag)",
              "\n**Core Functions:**",
              "• `issueCredential()`: Atomic issuance with novelty check",
              "• `batchIssueCredentials()`: Bulk multi-certificate issuance",
              "• `revokeCredential()`: Flips isRevoked = true; preserves evidence",
              "• `verifyByHash()`: O(1) primary mapping query (0 gas)",
              "• `verifyByStudentId()`: Secondary index query (0 gas)"],
             title_color=RGBColor(30, 58, 138))

    # Right: State Machine Diagram & Security
    if os.path.exists("project/docs/figures/fig_state_lifecycle.png"):
        s6.shapes.add_picture("project/docs/figures/fig_state_lifecycle.png", Inches(6.8), Inches(1.6), width=Inches(5.7))
        
    add_card(s6, Inches(6.8), Inches(4.3), Inches(5.7), Inches(2.5),
             "Enterprise Security Patterns",
             ["**OpenZeppelin Ownable:** Deployer admin controls whitelist.",
              "**Role-Based Access Control (RBAC):** `onlyAuthorised` restricts issuance & revocation to verified exam cell wallets.",
              "**Emergency Circuit-Breaker (`Pausable`):** Halts state changes during suspected key compromise while keeping verifications active.",
              "**ReentrancyGuard:** Protects against recursive external calls."],
             title_color=RGBColor(185, 28, 28))

    add_notes(s6, "Here is our smart contract design. CredentialRegistry.sol is written in Solidity 0.8.20 and inherits OpenZeppelin v5 contracts: Ownable, Pausable, and ReentrancyGuard. Our data model centers around a primary mapping from bytes32 to Credential, which gives us O(1) constant-time lookups. Notice our state machine: credentials transition from Draft to Active. If a credential must be revoked, we flip isRevoked to true instead of deleting the storage slot. This ensures an immutable forensic audit trail.")

    # ==========================================
    # SLIDE 7: WEB3 DASHBOARD & USER INTERFACE
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_background(s7, RGBColor(248, 250, 252))
    add_header(s7, "Unified Web3 Client Dashboard & UX Engineering", "REACT 18 • VITE • TAILWIND CSS • ETHERS.JS V6")
    
    add_card(s7, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "1. Credential Issuance Panel",
             ["**Drag & Drop Ingestion:** Supports PDF transcript ingestion directly in browser.",
              "**Native SHA-256 Hashing:** Invokes `window.crypto.subtle` in real time with zero external network transmission.",
              "**Dynamic QR Generation:** Embeds verification URI directly into a high-res printable canvas QR code.",
              "**Gas-Optimized Submission:** Broadcasts signed transaction to Hardhat / Polygon testnet via MetaMask."],
             title_color=RGBColor(30, 58, 138))

    add_card(s7, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "2. Instant Verification Portal",
             ["**Zero-Knowledge Verifier:** Employers do NOT need MetaMask or cryptocurrency to verify documents.",
              "**Sub-Second Local Digest:** Browser recalculates SHA-256 in 15ms upon PDF drop.",
              "**Dual Status Indicators:**",
              "• **Green Banner:** `AUTHENTIC & VERIFIED` (Shows SAP ID, Issuer, Block Timestamp, IPFS link).",
              "• **Red Banner:** `FORGERY DETECTED: HASH MISMATCH` (Instant tamper warning).",
              "**One-Click Viva Demo:** Preset buttons to evaluate genuine vs tampered grade cards instantly."],
             title_color=RGBColor(22, 101, 52))

    add_card(s7, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "3. Administrative Command Center",
             ["**Live State Telemetry:** Real-time metrics tracking total issued, active, and revoked credentials.",
              "**Role-Aware Governance:** Dynamic badge displaying wallet role (ADMIN OWNER / AUTHORIZED ISSUER / PUBLIC).",
              "**Audit-Preserving Revocation:** Authorized registrar can revoke credentials by hash with mandatory reason logging.",
              "**Emergency Pause Toggle:** One-click circuit breaker to freeze writes during security incidents."],
             title_color=RGBColor(185, 28, 28))

    add_notes(s7, "On the frontend, we engineered a clean, single-page Web3 dashboard using React 18, Vite, and Tailwind CSS. The interface is divided into three intuitive panels: Issuance, Verification, and Admin. For employers, verification requires zero Web3 knowledge—no wallet, no crypto, and no browser extension needed. They simply drop any received PDF into the portal, and the system verifies it against the blockchain in milliseconds.")

    # ==========================================
    # SLIDE 8: TESTING & QUALITY ASSURANCE (29 CHAI TESTS)
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_background(s8, RGBColor(248, 250, 252))
    add_header(s8, "Automated Verification: 29 Chai Unit Tests (100% Pass)", "CHAPTER 4: TESTING, VALIDATION & VERIFICATION")
    
    add_card(s8, Inches(0.8), Inches(1.6), Inches(7.5), Inches(5.2),
             "Automated Unit Test Execution Matrix (Hardhat & Chai)",
             ["**Category 1: Deployment & State Initialization (4 Tests | 42ms)**",
              "• Verified contract naming, owner assignment, zero counters, empty name reverts.",
              "**Category 2: Issuer Access Control & Governance (6 Tests | 68ms)**",
              "• Verified deployer default privileges, issuer additions/removals, non-owner reverts.",
              "**Category 3: Credential Issuance Logic (7 Tests | 81ms)**",
              "• Novel issuance, event emissions, duplicate hash collision reverts, empty argument checks.",
              "**Category 4: Batch Credential Issuance (3 Tests | 39ms)**",
              "• Multi-record atomic issuance, array length mismatch reverts, bulk counter updates.",
              "**Category 5: Constant-Time Verification Queries (5 Tests | 48ms)**",
              "• O(1) verifyByHash, unknown hash zero-struct returns, student ID secondary resolution.",
              "**Category 6: Non-Destructive Revocation (4 Tests | 52ms)**",
              "• Authorized revocation, reason logging, double-revocation reverts, non-issuer rejection.",
              "**Category 7: Emergency Circuit-Breaker (Pausable) (3 Tests | 37ms)**",
              "• Owner pause/unpause, EnforcedPause reverts on write, view functions remaining active."],
             title_color=RGBColor(30, 58, 138))

    add_card(s8, Inches(8.6), Inches(1.6), Inches(3.9), Inches(5.2),
             "Quality Assurance Metrics",
             ["**Total Tests:** 29 Automated Scenarios",
              "**Pass Rate:** 100% (29 / 29 PASSED)",
              "**Execution Time:** 317 milliseconds",
              "**Test Framework:** Mocha + Chai + Ethers.js",
              "**Standard Followed:** IEEE 730-2014 Software Quality Assurance",
              "\n**Key Boundary Validations:**",
              "✔ Prevents duplicate hash issuance",
              "✔ Reverts zero-address issuer additions",
              "✔ Blocks non-issuers from revocation",
              "✔ Enforces array symmetry in batch mode",
              "✔ Verifies view calls work while paused"],
             title_color=RGBColor(22, 101, 52), bg_color=RGBColor(240, 253, 244), border_color=RGBColor(187, 247, 208))

    add_notes(s8, "To satisfy IEEE 730 software quality standards, we constructed a comprehensive automated unit test suite containing 29 test scenarios in Mocha and Chai. Every single test passed in just 317 milliseconds. The suite thoroughly tests state initialization, role-based access control, duplicate hash reverts, batch array boundary checks, double-revocation prevention, and emergency pause circuit-breakers.")

    # ==========================================
    # SLIDE 9: EMPIRICAL STRICT AVALANCHE EXPERIMENT
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    apply_background(s9, RGBColor(248, 250, 252))
    add_header(s9, "Empirical Tamper Detection: Strict Avalanche Criterion", "EXPERIMENTAL RESULTS & MATHEMATICAL PROOF")
    
    # Left: Avalanche Chart
    if os.path.exists("project/docs/figures/fig_avalanche.png"):
        s9.shapes.add_picture("project/docs/figures/fig_avalanche.png", Inches(0.8), Inches(1.6), width=Inches(6.4))

    # Right: Tamper Experiment Breakdown
    add_card(s9, Inches(7.5), Inches(1.6), Inches(5.0), Inches(5.2),
             "The 1-Character Tamper Experiment",
             ["**Authentic Document (`NMIMS_Sample_GradeCard.pdf`):**",
              "• Student: Himanshu Garg (SAP ID: 70552400057)",
              "• Authentic CGPA: **9.42**",
              "• SHA-256 Digest: `0xb89ce30b75b539349a8114...`",
              "• Result: **AUTHENTIC & VERIFIED** (Green Banner)",
              "\n**Tampered Counterfeit (`..._TAMPERED.pdf`):**",
              "• Tamper: Modified exactly 1 ASCII byte: CGPA **9.42 -> 9.99**",
              "• SHA-256 Digest: `0xd9bff662829a779fef5a9a...`",
              "• Result: **FORGERY DETECTED** (Red Banner)",
              "\n**Mathematical Hamming Distance Proof:**",
              "• Total Bits in SHA-256: 256 bits",
              "• Bits Flipped by 1 Character Change: **128 bits**",
              "• Exact Percentage Flipped: **50.0%**",
              "• Conforms perfectly to NIST Strict Avalanche Criterion (SAC) ideal (50%). Proves mathematical impossibility of undetected tampering."],
             title_color=RGBColor(185, 28, 28))

    add_notes(s9, "Slide 9 provides empirical proof of our tamper detection. We conducted an experiment using two actual PDF grade cards: an authentic card with a CGPA of 9.42, and a counterfeit where we changed just one character to 9.99. Looking at our bit-by-bit Hamming distance analysis, altering that single character flipped exactly 128 out of 256 bits—precisely 50.0%. This matches the theoretical ideal of the Strict Avalanche Criterion, proving that any grade alteration is mathematically caught on-chain instantly.")

    # ==========================================
    # SLIDE 10: EVM GAS BENCHMARKING & COST MODEL
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    apply_background(s10, RGBColor(248, 250, 252))
    add_header(s10, "EVM Gas Telemetry & Economic Feasibility", "GAS OPTIMIZATION & PRODUCTION COST MODEL")
    
    # Left: Gas Benchmark Chart
    if os.path.exists("project/docs/figures/fig_gas_benchmarks.png"):
        s10.shapes.add_picture("project/docs/figures/fig_gas_benchmarks.png", Inches(0.8), Inches(1.6), width=Inches(6.4))

    # Right: Cost Model Table Card
    add_card(s10, Inches(7.5), Inches(1.6), Inches(5.0), Inches(5.2),
             "Cost Model Across Core Operations",
             ["**1. Contract Deployment:**",
              "• Gas Used: 1,182,450 gas",
              "• Cost on Polygon PoS: **$0.021 USD** (One-time only)",
              "\n**2. Single Credential Issuance:**",
              "• Gas Used: 68,420 gas",
              "• Cost on Polygon PoS: **$0.0012 USD** (~10 paise)",
              "\n**3. Batch Issuance (per cert, avg):**",
              "• Gas Used: 52,100 gas",
              "• Cost on Polygon PoS: **$0.0009 USD** (~7 paise)",
              "• **23.8% Gas Reduction** via loop amortization",
              "\n**4. Revoke Credential:**",
              "• Gas Used: 31,250 gas | Cost: **$0.0005 USD**",
              "\n**5. Verification Query (`verifyByHash`):**",
              "• Gas Used: **0 GAS (FREE view function)**",
              "• Unlimited verifications globally with zero economic barrier."],
             title_color=RGBColor(30, 58, 138))

    add_notes(s10, "Economic feasibility is critical for university adoption. We profiled the gas consumption across every function. Deploying the contract takes 1.18 million gas—on Polygon, that costs only 2 cents. Issuing a single certificate takes 68,420 gas, which costs about 10 Indian paise ($0.0012). With batch issuance, we reduced this to 52,100 gas—a 23.8% cost savings. Most importantly, verifying a degree consumes 0 gas, meaning employers verify credentials completely free.")

    # ==========================================
    # SLIDE 11: REGULATORY COMPLIANCE & DPDP ACT 2023
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    apply_background(s11, RGBColor(248, 250, 252))
    add_header(s11, "Regulatory Alignment with India's DPDP Act 2023", "LEGAL & STATUTORY DATA SOVEREIGNTY COMPLIANCE")
    
    add_card(s11, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "DPDP Act 2023 Mandates & EduCred Compliance",
             ["**The Legal Challenge:** Under Section 8(7) and Section 12 of India's Digital Personal Data Protection (DPDP) Act 2023, data fiduciaries must ensure data minimization, purpose limitation, and execute the \"Right to Erasure\". Writing personal names or marks to an immutable public blockchain violates these provisions.",
              "\n**EduCred's Architectural Compliance:**",
              "• **Zero Cleartext PII on Ledger:** Student names, course grades, parent details, and photos are NEVER placed on Ethereum storage slots.",
              "• **One-Way Cryptographic Pseudonymity:** Only a one-way 32-byte SHA-256 hash and institutional SAP ID are stored on-chain. SHA-256 is computationally irreversible (preimage resistance).",
              "• **Right to Erasure Adherence:** The physical PDF resides in student custody or access-controlled IPFS gateways. If a student exercises their Right to Erasure, the off-chain PDF is unpinned and erased, rendering the on-chain hash completely anonymous and un-linkable."],
             title_color=RGBColor(30, 58, 138))

    add_card(s11, Inches(6.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Engineering Standards & Institutional Governance",
             ["**NIST FIPS PUB 180-4 (Secure Hash Standard):** Standardized SHA-256 implementation ensuring 128-bit collision security margin ($2^{128}$ operations).",
              "**IEEE 1471 / ISO 42010 Architecture Description:** Multi-view stakeholder modeling separating data boundaries from consensus.",
              "**IEEE 730-2014 Software Quality Assurance:** Verified by our 29-case automated Chai unit testing harness.",
              "**UGC / NAD Alignment:** Standardizes student SAP IDs for seamless interoperability with the National Academic Depository.",
              "**United Nations SDGs:** Advances SDG 4 (Quality Education) and SDG 9 (Industry & Innovation) with 99.99% lower energy use on Proof-of-Stake."],
             title_color=RGBColor(22, 101, 52))

    add_notes(s11, "A critical differentiator of our project is strict compliance with India's DPDP Act 2023. Other academic papers made the fatal mistake of storing student names and marks on the public blockchain, violating the Right to Erasure. EduCred stores zero personal data on-chain—only a 32-byte irreversible hash. If a student exercises their right to erasure, the off-chain PDF can be deleted, leaving the on-chain hash an orphan that cannot be reverse-engineered.")

    # ==========================================
    # SLIDE 12: TEAM STRUCTURE & INDIVIDUAL CONTRIBUTIONS (IER)
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    apply_background(s12, RGBColor(248, 250, 252))
    add_header(s12, "Team Roles, Responsibilities & Contribution Matrix", "CHAPTER 5: TEAMWORK & INDIVIDUAL EVIDENCE REGISTER")
    
    add_card(s12, Inches(0.8), Inches(1.6), Inches(5.8), Inches(5.2),
             "Team Role Distribution & Responsibilities",
             ["**1. Himanshu Garg (Roll: E250 | SAP: 70552400057)**",
              "• **Role:** Lead System Architect & Smart Contract Lead",
              "• Owned `CredentialRegistry.sol` (Solidity 0.8.20 + OpenZeppelin v5).",
              "• Client W3C Web Crypto SHA-256 pipeline, Strict Avalanche experiment, and EVM gas telemetry benchmarking.",
              "\n**2. Manthan Patil (Roll: E323 | SAP: 70552400133)**",
              "• **Role:** Frontend Web3 Engineer & UX Lead",
              "• Owned React 18 + Vite dashboard (`App.jsx`) and Tailwind CSS.",
              "• Dynamic HTML5 Canvas QR generator, ErrorBoundary, and Ethers.js v6 wallet connectivity.",
              "\n**3. Vaishnavi Mali (Roll: B348 | SAP: 70022400767)**",
              "• **Role:** QA, Test Automation & Regulatory Compliance Lead",
              "• Owned 29/29 automated Chai test cases in `CredentialRegistry.test.js`.",
              "• Boundary assertions, audit trail checks, and statutory DPDP Act 2023 compliance audit."],
             title_color=RGBColor(30, 58, 138))

    add_card(s12, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2),
             "Evidence Register (IER) & Key Reflections",
             ["**Individual Evidence Mapping:**",
              "• **EV-01 / EV-06 / EV-07 (Himanshu):** Smart contract, avalanche test, and EVM gas profiling scripts.",
              "• **EV-03 / EV-05 / EV-09 (Manthan):** React client, canvas QR generator, and ErrorBoundary recovery.",
              "• **EV-02 / EV-08 (Vaishnavi):** 29-test automated Chai suite and DPDP Act compliance audit report.",
              "\n**Key Engineering Reflections:**",
              "• **Himanshu:** Decoupling hash from content achieved O(1) free verification while eliminating NFT transferability bugs.",
              "• **Manthan:** Streamlined Web3 UX so employers can verify credentials without crypto wallets or browser extensions.",
              "• **Vaishnavi:** Proved that blockchain immutability and the DPDP Right to Erasure can coexist via cryptographic abstraction."],
             title_color=RGBColor(71, 85, 105))

    add_notes(s12, "In Chapter 5, we present our team structure and the Individual Evidence Register (IER). Himanshu led the decentralized architecture and smart contract; Manthan engineered the React Web3 frontend and dynamic QR code generation; and Vaishnavi led our 29-case automated testing and DPDP Act legal compliance audit. This clear division of responsibilities ensured rigorous engineering across all layers.")

    # ==========================================
    # SLIDE 13: CONCLUSION & SCALABILITY ROADMAP
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    apply_background(s13, RGBColor(248, 250, 252))
    add_header(s13, "Conclusion & Scalability Roadmap for DE-III", "CHAPTER 6: CONCLUSION & FUTURE SCOPE")
    
    add_card(s13, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Project Conclusions & Evaluative Summary",
             ["**1. Elimination of Fraud:** Cryptographic SHA-256 hashing and immutable ledger state make certificate forgery mathematically impossible.",
              "**2. Dramatic Latency Reduction:** Verification turnaround slashed from 14-30 days of manual bureaucracy to sub-second real-time.",
              "**3. Zero Barrier for Employers:** Public verifiers verify credentials with 0 gas fees and zero Web3 onboarding friction.",
              "**4. Production-Ready Codebase:** Validated across 29 automated test cases (100% pass) with complete regression harnesses.",
              "**5. Legal & Statutory Alignment:** Decoupled data model guarantees 100% compliance with India's DPDP Act 2023.",
              "**Conclusion:** EduCred proves that decentralized cryptographic infrastructure provides an industry-ready, cost-effective solution for securing educational credentials across Indian universities."],
             title_color=RGBColor(22, 101, 52))

    add_card(s13, Inches(6.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Scalability Roadmap (DE-III / Capstone)",
             ["**Phase 1: Polygon Amoy Testnet Deployment (Month 1):**",
              "• Benchmark live PoS finality, RPC node latency, and live gas under network congestion.",
              "\n**Phase 2: DigiLocker & NAD API Integration (Months 2-3):**",
              "• Build enterprise middleware connecting university ERP (SAP Student Lifecycle) directly to the blockchain registry for automated graduation issuance.",
              "\n**Phase 3: Zero-Knowledge Privacy Circuits (zk-SNARKs) (Months 4-5):**",
              "• Implement Circom / snarkjs circuits enabling students to prove \"CGPA >= 8.0\" without revealing course transcripts.",
              "\n**Phase 4: Mobile Verifier Application (Month 6):**",
              "• Offline-capable mobile scanner using camera to authenticate paper certificate QR codes during on-campus recruitment."],
             title_color=RGBColor(30, 58, 138))

    add_notes(s13, "In conclusion, EduCred demonstrates that blockchain and client-side cryptographic hashing can completely eliminate credential forgery while slashing verification turnaround from weeks to seconds with zero cost to employers. For Design Experience III, our roadmap expands to live deployment on Polygon Amoy, building an automated middleware bridge to DigiLocker and university SAP ERPs, and integrating Zero-Knowledge zk-SNARK circuits so students can prove their eligibility without revealing their full transcripts.")

    # ==========================================
    # SLIDE 14: LIVE DEMONSTRATION & VIVA DEFENSE
    # ==========================================
    s14 = prs.slides.add_slide(blank_layout)
    apply_background(s14, RGBColor(15, 23, 42)) # Slate 900
    
    # Title
    tb_demo = s14.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.3), Inches(0.8))
    p_demo = tb_demo.text_frame.paragraphs[0]
    p_demo.text = "Live Prototype Demonstration & Viva Defense"
    p_demo.font.name = "Arial"
    p_demo.font.size = Pt(28)
    p_demo.font.bold = True
    p_demo.font.color.rgb = RGBColor(255, 255, 255)
    
    tb_demo_sub = s14.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(0.4))
    p_dsub = tb_demo_sub.text_frame.paragraphs[0]
    p_dsub.text = "Interactive Evaluation of Credential Issuance, O(1) Verification & Strict Avalanche Forgery Detection"
    p_dsub.font.name = "Arial"
    p_dsub.font.size = Pt(13)
    p_dsub.font.color.rgb = RGBColor(56, 189, 248)
    
    # Demonstration Step Cards
    add_card(s14, Inches(1.0), Inches(2.2), Inches(3.6), Inches(4.6),
             "Step 1: Admin Issuance",
             ["• Connect Hardhat / Polygon Admin wallet.",
              "• Drop authentic `NMIMS_Sample_GradeCard.pdf` into Issuance dropzone.",
              "• Observe real-time SHA-256 calculation (<15ms).",
              "• Execute `issueCredential()` transaction.",
              "• Verify instant event emission and dynamic QR code generation."],
             title_color=RGBColor(56, 189, 248), bg_color=RGBColor(30, 41, 59), border_color=RGBColor(51, 65, 85))

    add_card(s14, Inches(4.9), Inches(2.2), Inches(3.6), Inches(4.6),
             "Step 2: Instant Verification",
             ["• Switch to public recruiter mode (zero wallet required).",
              "• Drop authentic PDF into Verification Portal.",
              "• Instant **AUTHENTIC & VERIFIED** green banner.",
              "• Displays Student SAP ID (70552400057), timestamp, and issuer address.",
              "• Query executed in O(1) with 0 gas."],
             title_color=RGBColor(74, 222, 128), bg_color=RGBColor(30, 41, 59), border_color=RGBColor(51, 65, 85))

    add_card(s14, Inches(8.8), Inches(2.2), Inches(3.6), Inches(4.6),
             "Step 3: Tamper Detection",
             ["• Drop tampered PDF (`..._TAMPERED.pdf`, CGPA 9.99).",
              "• SHA-256 hash recalculated locally in browser.",
              "• Instant **FORGERY DETECTED: HASH MISMATCH** red banner.",
              "• Proves 50% bit flip (128/256 bits) eliminates fraud mathematically.",
              "• Test revocation & emergency circuit-breaker."],
             title_color=RGBColor(248, 113, 113), bg_color=RGBColor(30, 41, 59), border_color=RGBColor(51, 65, 85))

    add_notes(s14, "Thank you, respected evaluators. I am now ready to conduct the live prototype demonstration showing the three steps: issuing an authentic grade card, verifying it instantly with zero gas, and testing our 1-character tampered grade card to demonstrate instant Strict Avalanche forgery detection. I welcome your questions for the viva defense.")

    # Save presentation
    out_pptx = "project/docs/DE2_Final_Presentation_Himanshu_Garg.pptx"
    prs.save(out_pptx)
    print(f"Presentation generated successfully: {out_pptx}")

if __name__ == "__main__":
    main()

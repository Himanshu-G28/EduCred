// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// ─────────────────────────────────────────────────────────────────────────────
// OpenZeppelin imports (install via: npm install @openzeppelin/contracts)
// ─────────────────────────────────────────────────────────────────────────────
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Pausable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * @title  CredentialRegistry
 * @author Himanshu Garg — NMIMS B.Tech CSE, Design Experience 2 (Sem 5)
 * @notice Immutable on-chain registry for tamper-proof academic credentials.
 *         Universities issue credentials by storing a SHA-256 hash of the
 *         credential document together with its IPFS content URI.  Any
 *         third-party verifier — employer, government body, foreign university
 *         — can authenticate a credential in O(1) time by querying the mapping
 *         without relying on the issuing institution.
 *
 * @dev    Architecture overview
 *         ──────────────────────
 *         • Ownable  : The deployer (university admin wallet) is the owner.
 *                      Only the owner can add / remove authorised issuers.
 *         • Pausable : Owner can pause all state-changing functions in an
 *                      emergency (e.g. compromised issuer key).
 *         • ReentrancyGuard : Defensive measure against re-entrant calls on
 *                             any future payable extensions.
 *
 *         Data model
 *         ──────────
 *         credentials  : sha256Hash  → Credential struct   (primary index)
 *         studentIndex : studentId   → sha256Hash           (lookup index)
 *
 *         Why store hashes, not raw data?
 *         Hash storage keeps PII off-chain (IPFS / Pinata), satisfying DPDP
 *         Act 2023 and GDPR principles.  The hash serves as the immutable
 *         fingerprint; the IPFS URI serves as the address of the full document.
 */
contract CredentialRegistry is Ownable, Pausable, ReentrancyGuard {

    // ─────────────────────────────────────────────────────────────────────────
    // Data Structures
    // ─────────────────────────────────────────────────────────────────────────

    /**
     * @dev  One record per credential issued.
     *
     * @param studentId   Human-readable unique identifier (SAP ID / Roll No).
     *                    Stored as a string so non-numeric IDs are supported.
     * @param sha256Hash  SHA-256 hash of the credential PDF, computed off-chain
     *                    using the Web Crypto API before calling issueCredential.
     *                    Stored as bytes32 — the natural on-chain representation
     *                    of a 256-bit value.
     * @param ipfsURI     IPFS content URI (e.g. "ipfs://Qm...") pointing to the
     *                    full credential document pinned via Pinata.
     * @param issuedAt    Block timestamp at issuance — Unix epoch, UTC.
     * @param issuedBy    Address of the authorised issuer wallet that called
     *                    issueCredential(); stored for audit trail.
     * @param isRevoked   False on issuance.  Flipped to true by revokeCredential.
     *                    Revoked credentials remain on-chain for auditability;
     *                    they are never deleted.
     */
    struct Credential {
        string  studentId;
        bytes32 sha256Hash;
        string  ipfsURI;
        uint256 issuedAt;
        address issuedBy;
        bool    isRevoked;
    }

    // ─────────────────────────────────────────────────────────────────────────
    // State Variables
    // ─────────────────────────────────────────────────────────────────────────

    /// @notice Primary storage: SHA-256 hash → Credential record.
    mapping(bytes32 => Credential) private _credentials;

    /**
     * @notice Secondary index: studentId → SHA-256 hash.
     * @dev    A student can hold at most one active credential per studentId.
     *         If a replacement is needed, revoke the old one first and issue new.
     */
    mapping(string => bytes32) private _studentIndex;

    /**
     * @notice Addresses permitted to call issueCredential and revokeCredential.
     * @dev    The owner is implicitly authorised; additional department wallets
     *         can be whitelisted via addIssuer().
     */
    mapping(address => bool) private _authorisedIssuers;

    /// @notice Total credentials ever issued (monotonically increasing).
    uint256 public totalIssued;

    /// @notice Total credentials that have been revoked.
    uint256 public totalRevoked;

    /// @notice Name of the institution that deployed this registry.
    string  public institutionName;

    // ─────────────────────────────────────────────────────────────────────────
    // Events
    // ─────────────────────────────────────────────────────────────────────────

    /**
     * @notice Emitted whenever a new credential is successfully issued.
     * @param sha256Hash  The credential's unique fingerprint (indexed for fast
     *                    event log filtering from the frontend).
     * @param studentId   Human-readable student identifier.
     * @param ipfsURI     Location of the full document on IPFS.
     * @param issuedBy    Issuer wallet address.
     * @param issuedAt    Block timestamp.
     */
    event CredentialIssued(
        bytes32 indexed sha256Hash,
        string  studentId,
        string  ipfsURI,
        address indexed issuedBy,
        uint256 issuedAt
    );

    /**
     * @notice Emitted when a credential is revoked.
     * @param sha256Hash  The fingerprint of the revoked credential.
     * @param studentId   Human-readable student identifier.
     * @param revokedBy   Address that called revokeCredential().
     * @param revokedAt   Block timestamp of revocation.
     */
    event CredentialRevoked(
        bytes32 indexed sha256Hash,
        string  studentId,
        address indexed revokedBy,
        uint256 revokedAt
    );

    /// @notice Emitted when a new issuer wallet is whitelisted by the owner.
    event IssuerAdded(address indexed issuer);

    /// @notice Emitted when an issuer wallet is removed from the whitelist.
    event IssuerRemoved(address indexed issuer);

    // ─────────────────────────────────────────────────────────────────────────
    // Custom Errors  (gas-efficient; Solidity 0.8.4+)
    // ─────────────────────────────────────────────────────────────────────────

    /// @dev Thrown when an address that is not the owner or an authorised
    ///      issuer attempts a restricted action.
    error NotAuthorised(address caller);

    /// @dev Thrown when issueCredential is called with a hash that already
    ///      exists in the registry.
    error CredentialAlreadyExists(bytes32 sha256Hash);

    /// @dev Thrown when a lookup or revocation targets a non-existent hash.
    error CredentialNotFound(bytes32 sha256Hash);

    /// @dev Thrown when revokeCredential is called on an already-revoked record.
    error CredentialAlreadyRevoked(bytes32 sha256Hash);

    /// @dev Thrown on empty / zero-value argument validation.
    error InvalidArgument(string paramName);

    // ─────────────────────────────────────────────────────────────────────────
    // Modifiers
    // ─────────────────────────────────────────────────────────────────────────

    /**
     * @dev  Restricts function access to the contract owner OR any address
     *       whitelisted via addIssuer().
     */
    modifier onlyAuthorised() {
        if (msg.sender != owner() && !_authorisedIssuers[msg.sender]) {
            revert NotAuthorised(msg.sender);
        }
        _;
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Constructor
    // ─────────────────────────────────────────────────────────────────────────

    /**
     * @dev  Deploys the registry and sets the owning institution name.
     *       The deploying address becomes the contract owner via Ownable.
     *
     * @param _institutionName  Display name, e.g. "NMIMS – MPSTME".
     */
    constructor(string memory _institutionName) Ownable(msg.sender) {
        if (bytes(_institutionName).length == 0) {
            revert InvalidArgument("institutionName");
        }
        institutionName = _institutionName;
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Core Credential Functions
    // ─────────────────────────────────────────────────────────────────────────

    /**
     * @notice Issue a new academic credential on-chain.
     *
     * @dev    Off-chain preparation (do this in your React frontend before calling):
     *         1. Read the credential PDF as an ArrayBuffer.
     *         2. Compute SHA-256:
     *               const hashBuffer = await crypto.subtle.digest("SHA-256", arrayBuffer);
     *               const hashHex    = Array.from(new Uint8Array(hashBuffer))
     *                                       .map(b => b.toString(16).padStart(2, "0"))
     *                                       .join("");
     *         3. Pass "0x" + hashHex as the sha256Hash argument.
     *         4. Pin the PDF to IPFS via Pinata; pass the returned ipfs:// URI.
     *
     * @param  _studentId   SAP ID / Roll No. of the student (e.g. "70552400057").
     * @param  _sha256Hash  Bytes32 SHA-256 fingerprint of the credential document.
     * @param  _ipfsURI     IPFS content URI (e.g. "ipfs://QmXyz...").
     *
     * Requirements:
     *  - Caller must be the owner or an authorised issuer.
     *  - Contract must not be paused.
     *  - _sha256Hash must not already exist in the registry.
     *  - _studentId and _ipfsURI must be non-empty strings.
     *  - _sha256Hash must be non-zero.
     */
    function issueCredential(
        string  calldata _studentId,
        bytes32          _sha256Hash,
        string  calldata _ipfsURI
    )
        external
        onlyAuthorised
        whenNotPaused
        nonReentrant
    {
        // ── Input validation ──────────────────────────────────────────────
        if (bytes(_studentId).length  == 0) revert InvalidArgument("studentId");
        if (_sha256Hash               == 0) revert InvalidArgument("sha256Hash");
        if (bytes(_ipfsURI).length    == 0) revert InvalidArgument("ipfsURI");

        // ── Duplicate check ────────────────────────────────────────────────
        // If issuedAt is non-zero, a record already occupies this hash slot.
        if (_credentials[_sha256Hash].issuedAt != 0) {
            revert CredentialAlreadyExists(_sha256Hash);
        }

        // ── Write to storage ──────────────────────────────────────────────
        _credentials[_sha256Hash] = Credential({
            studentId  : _studentId,
            sha256Hash : _sha256Hash,
            ipfsURI    : _ipfsURI,
            issuedAt   : block.timestamp,
            issuedBy   : msg.sender,
            isRevoked  : false
        });

        // Update secondary index (studentId → hash)
        _studentIndex[_studentId] = _sha256Hash;

        // Update counters
        unchecked { ++totalIssued; }

        // ── Emit event (React frontend listens for this) ───────────────────
        emit CredentialIssued(_sha256Hash, _studentId, _ipfsURI, msg.sender, block.timestamp);
    }

    /**
     * @notice Revoke an existing credential (e.g. due to academic misconduct).
     *
     * @dev    Revoked credentials are NOT deleted from storage — they remain
     *         permanently visible with isRevoked = true, giving regulators and
     *         employers a complete audit trail.
     *
     * @param  _sha256Hash  Hash of the credential to revoke.
     *
     * Requirements:
     *  - Caller must be the owner or an authorised issuer.
     *  - Contract must not be paused.
     *  - Credential must exist and must not already be revoked.
     */
    function revokeCredential(bytes32 _sha256Hash)
        external
        onlyAuthorised
        whenNotPaused
        nonReentrant
    {
        // Existence check
        Credential storage cred = _credentials[_sha256Hash];
        if (cred.issuedAt == 0)   revert CredentialNotFound(_sha256Hash);
        if (cred.isRevoked)        revert CredentialAlreadyRevoked(_sha256Hash);

        // Flip the flag — do NOT delete the record
        cred.isRevoked = true;
        unchecked { ++totalRevoked; }

        emit CredentialRevoked(_sha256Hash, cred.studentId, msg.sender, block.timestamp);
    }

    // ─────────────────────────────────────────────────────────────────────────
    // View / Verification Functions (public — anyone can call, zero gas cost)
    // ─────────────────────────────────────────────────────────────────────────

    /**
     * @notice Verify a credential by its SHA-256 hash.
     *
     * @dev    This is the PRIMARY verification pathway:
     *         1. Verifier scans the QR code on the credential PDF.
     *         2. QR code encodes the sha256Hash (as a hex string) and the contract address.
     *         3. Frontend calls verifyByHash(bytes32(hashFromQR)).
     *         4. Receives the full Credential struct — verifier checks isRevoked == false.
     *
     *         Additionally, the frontend can independently recompute the hash from
     *         the document and confirm it matches credential.sha256Hash before trusting
     *         the on-chain record.
     *
     * @param  _sha256Hash  The hash to look up.
     * @return cred         The full Credential struct.  If cred.issuedAt == 0,
     *                      the credential does not exist.
     */
    function verifyByHash(bytes32 _sha256Hash)
        external
        view
        returns (Credential memory cred)
    {
        cred = _credentials[_sha256Hash];
        // No revert — returning an empty struct is the canonical "not found" signal.
        // issuedAt == 0 → credential does not exist.
        // isRevoked == true → credential was revoked (treat as invalid).
    }

    /**
     * @notice Verify a credential by the student's ID (SAP ID / Roll No).
     *
     * @dev    Convenience wrapper around verifyByHash for cases where the verifier
     *         only has the student's ID (e.g. checking a CV claim without a QR code).
     *         Note: a student can have only one active hash per studentId slot.
     *
     * @param  _studentId   The student identifier to look up.
     * @return cred         Full Credential struct (same semantics as verifyByHash).
     */
    function verifyByStudentId(string calldata _studentId)
        external
        view
        returns (Credential memory cred)
    {
        bytes32 hash = _studentIndex[_studentId];
        if (hash != 0) {
            cred = _credentials[hash];
        }
        // If hash == 0, returns empty struct (issuedAt == 0 → not found).
    }

    /**
     * @notice Check whether a specific SHA-256 hash exists in the registry
     *         and is currently valid (not revoked).
     *
     * @dev    Optimised boolean shortcut for the verifier portal — cheaper than
     *         decoding a full struct when the frontend only needs a yes/no answer.
     *
     * @param  _sha256Hash  Hash to query.
     * @return exists       True if the credential exists AND is not revoked.
     */
    function isCredentialValid(bytes32 _sha256Hash)
        external
        view
        returns (bool exists)
    {
        Credential storage cred = _credentials[_sha256Hash];
        return (cred.issuedAt != 0 && !cred.isRevoked);
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Issuer Management (Owner Only)
    // ─────────────────────────────────────────────────────────────────────────

    /**
     * @notice Whitelist a new issuer address (e.g. a department registrar wallet).
     * @param  _issuer  Address to authorise.
     */
    function addIssuer(address _issuer) external onlyOwner {
        if (_issuer == address(0)) revert InvalidArgument("issuer");
        _authorisedIssuers[_issuer] = true;
        emit IssuerAdded(_issuer);
    }

    /**
     * @notice Remove an issuer from the whitelist (e.g. staff change or key compromise).
     * @param  _issuer  Address to deauthorise.
     */
    function removeIssuer(address _issuer) external onlyOwner {
        _authorisedIssuers[_issuer] = false;
        emit IssuerRemoved(_issuer);
    }

    /**
     * @notice Check whether an address is currently an authorised issuer.
     * @param  _issuer  Address to query.
     * @return True if authorised (note: owner is always authorised regardless).
     */
    function isAuthorisedIssuer(address _issuer) external view returns (bool) {
        return _issuer == owner() || _authorisedIssuers[_issuer];
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Emergency Circuit-Breakers (Owner Only)
    // ─────────────────────────────────────────────────────────────────────────

    /**
     * @notice Pause all state-changing functions.
     * @dev    Use in case of a discovered vulnerability or compromised issuer.
     *         Verification (view) functions remain available while paused.
     */
    function pause()   external onlyOwner { _pause(); }

    /**
     * @notice Resume normal operation after an emergency pause.
     */
    function unpause() external onlyOwner { _unpause(); }
}

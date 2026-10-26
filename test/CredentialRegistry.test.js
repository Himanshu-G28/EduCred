const { expect } = require("chai");
const { ethers } = require("hardhat");
const { loadFixture } = require("@nomicfoundation/hardhat-toolbox/network-helpers");

describe("CredentialRegistry Smart Contract Unit Tests", function () {
  const INSTITUTION_NAME = "NMIMS – MPSTME";
  const TEST_STUDENT_ID = "70552400057";
  const TEST_STUDENT_ID_2 = "70552400058";
  const TEST_HASH_1 = "0x" + "a".repeat(64);
  const TEST_HASH_2 = "0x" + "b".repeat(64);
  const TEST_IPFS_URI = "ipfs://QmXoypizjW3WknFiJnKLwHCnL72vedxjQkDDP1mXWo6uco";

  // Reusable fixture to set up test environment cleanly for each test
  async function deployCredentialRegistryFixture() {
    const [owner, issuer, unauthorizedUser, student] = await ethers.getSigners();

    const CredentialRegistry = await ethers.getContractFactory("CredentialRegistry");
    const registry = await CredentialRegistry.deploy(INSTITUTION_NAME);
    await registry.waitForDeployment();

    return { registry, owner, issuer, unauthorizedUser, student };
  }

  // ───────────────────────────────────────────────────────────────────────────
  // 1. Deployment & Initialization Tests
  // ───────────────────────────────────────────────────────────────────────────
  describe("1. Deployment & Initialization", function () {
    it("Should deploy successfully and set the correct institution name", async function () {
      const { registry } = await loadFixture(deployCredentialRegistryFixture);
      expect(await registry.institutionName()).to.equal(INSTITUTION_NAME);
    });

    it("Should assign the deployer as the contract owner", async function () {
      const { registry, owner } = await loadFixture(deployCredentialRegistryFixture);
      expect(await registry.owner()).to.equal(owner.address);
    });

    it("Should initialize totalIssued and totalRevoked counters to 0", async function () {
      const { registry } = await loadFixture(deployCredentialRegistryFixture);
      expect(await registry.totalIssued()).to.equal(0n);
      expect(await registry.totalRevoked()).to.equal(0n);
    });

    it("Should revert deployment if institutionName is empty", async function () {
      const CredentialRegistry = await ethers.getContractFactory("CredentialRegistry");
      await expect(CredentialRegistry.deploy(""))
        .to.be.revertedWithCustomError(CredentialRegistry, "InvalidArgument")
        .withArgs("institutionName");
    });
  });

  // ───────────────────────────────────────────────────────────────────────────
  // 2. Issuer Management Tests
  // ───────────────────────────────────────────────────────────────────────────
  describe("2. Issuer Authorization Management", function () {
    it("Owner should be an authorized issuer by default", async function () {
      const { registry, owner } = await loadFixture(deployCredentialRegistryFixture);
      expect(await registry.isAuthorisedIssuer(owner.address)).to.be.true;
    });

    it("Non-authorized address should not be an authorized issuer", async function () {
      const { registry, issuer } = await loadFixture(deployCredentialRegistryFixture);
      expect(await registry.isAuthorisedIssuer(issuer.address)).to.be.false;
    });

    it("Owner can add a new issuer and emit IssuerAdded event", async function () {
      const { registry, issuer } = await loadFixture(deployCredentialRegistryFixture);
      await expect(registry.addIssuer(issuer.address))
        .to.emit(registry, "IssuerAdded")
        .withArgs(issuer.address);
      expect(await registry.isAuthorisedIssuer(issuer.address)).to.be.true;
    });

    it("Owner can remove an issuer and emit IssuerRemoved event", async function () {
      const { registry, issuer } = await loadFixture(deployCredentialRegistryFixture);
      await registry.addIssuer(issuer.address);
      expect(await registry.isAuthorisedIssuer(issuer.address)).to.be.true;

      await expect(registry.removeIssuer(issuer.address))
        .to.emit(registry, "IssuerRemoved")
        .withArgs(issuer.address);
      expect(await registry.isAuthorisedIssuer(issuer.address)).to.be.false;
    });

    it("Reverts if adding zero address as issuer", async function () {
      const { registry } = await loadFixture(deployCredentialRegistryFixture);
      await expect(registry.addIssuer(ethers.ZeroAddress))
        .to.be.revertedWithCustomError(registry, "InvalidArgument")
        .withArgs("issuer");
    });

    it("Non-owner cannot add or remove an issuer", async function () {
      const { registry, unauthorizedUser, issuer } = await loadFixture(deployCredentialRegistryFixture);
      await expect(registry.connect(unauthorizedUser).addIssuer(issuer.address))
        .to.be.revertedWithCustomError(registry, "OwnableUnauthorizedAccount")
        .withArgs(unauthorizedUser.address);
    });
  });

  // ───────────────────────────────────────────────────────────────────────────
  // 3. Credential Issuance Tests
  // ───────────────────────────────────────────────────────────────────────────
  describe("3. Credential Issuance", function () {
    it("Allows owner to issue a credential successfully", async function () {
      const { registry, owner } = await loadFixture(deployCredentialRegistryFixture);

      const tx = await registry.issueCredential(TEST_STUDENT_ID, TEST_HASH_1, TEST_IPFS_URI);
      const receipt = await tx.wait();
      const block = await ethers.provider.getBlock(receipt.blockNumber);

      await expect(tx)
        .to.emit(registry, "CredentialIssued")
        .withArgs(TEST_HASH_1, TEST_STUDENT_ID, TEST_IPFS_URI, owner.address, block.timestamp);

      expect(await registry.totalIssued()).to.equal(1n);
    });

    it("Allows whitelisted issuer to issue a credential", async function () {
      const { registry, issuer } = await loadFixture(deployCredentialRegistryFixture);
      await registry.addIssuer(issuer.address);

      await expect(
        registry.connect(issuer).issueCredential(TEST_STUDENT_ID, TEST_HASH_1, TEST_IPFS_URI)
      ).to.emit(registry, "CredentialIssued");

      expect(await registry.totalIssued()).to.equal(1n);
    });

    it("Reverts if unauthorized caller attempts to issue credential", async function () {
      const { registry, unauthorizedUser } = await loadFixture(deployCredentialRegistryFixture);

      await expect(
        registry.connect(unauthorizedUser).issueCredential(TEST_STUDENT_ID, TEST_HASH_1, TEST_IPFS_URI)
      )
        .to.be.revertedWithCustomError(registry, "NotAuthorised")
        .withArgs(unauthorizedUser.address);
    });

    it("Reverts if studentId is empty", async function () {
      const { registry } = await loadFixture(deployCredentialRegistryFixture);
      await expect(registry.issueCredential("", TEST_HASH_1, TEST_IPFS_URI))
        .to.be.revertedWithCustomError(registry, "InvalidArgument")
        .withArgs("studentId");
    });

    it("Reverts if sha256Hash is zero", async function () {
      const { registry } = await loadFixture(deployCredentialRegistryFixture);
      await expect(registry.issueCredential(TEST_STUDENT_ID, ethers.ZeroHash, TEST_IPFS_URI))
        .to.be.revertedWithCustomError(registry, "InvalidArgument")
        .withArgs("sha256Hash");
    });

    it("Reverts if ipfsURI is empty", async function () {
      const { registry } = await loadFixture(deployCredentialRegistryFixture);
      await expect(registry.issueCredential(TEST_STUDENT_ID, TEST_HASH_1, ""))
        .to.be.revertedWithCustomError(registry, "InvalidArgument")
        .withArgs("ipfsURI");
    });

    it("Reverts if duplicate sha256Hash is issued", async function () {
      const { registry } = await loadFixture(deployCredentialRegistryFixture);
      await registry.issueCredential(TEST_STUDENT_ID, TEST_HASH_1, TEST_IPFS_URI);

      await expect(registry.issueCredential(TEST_STUDENT_ID_2, TEST_HASH_1, TEST_IPFS_URI))
        .to.be.revertedWithCustomError(registry, "CredentialAlreadyExists")
        .withArgs(TEST_HASH_1);
    });
  });

  // ───────────────────────────────────────────────────────────────────────────
  // 4. Verification View Functions Tests
  // ───────────────────────────────────────────────────────────────────────────
  describe("4. Verification & Lookup", function () {
    it("Verifies credential by hash correctly", async function () {
      const { registry, owner } = await loadFixture(deployCredentialRegistryFixture);
      await registry.issueCredential(TEST_STUDENT_ID, TEST_HASH_1, TEST_IPFS_URI);

      const cred = await registry.verifyByHash(TEST_HASH_1);
      expect(cred.studentId).to.equal(TEST_STUDENT_ID);
      expect(cred.sha256Hash).to.equal(TEST_HASH_1);
      expect(cred.ipfsURI).to.equal(TEST_IPFS_URI);
      expect(cred.issuedBy).to.equal(owner.address);
      expect(cred.isRevoked).to.be.false;
      expect(cred.issuedAt).to.be.gt(0);
    });

    it("Returns empty struct when verifying non-existent hash", async function () {
      const { registry } = await loadFixture(deployCredentialRegistryFixture);
      const cred = await registry.verifyByHash(TEST_HASH_2);
      expect(cred.issuedAt).to.equal(0n);
      expect(cred.studentId).to.equal("");
    });

    it("Verifies credential by studentId correctly", async function () {
      const { registry } = await loadFixture(deployCredentialRegistryFixture);
      await registry.issueCredential(TEST_STUDENT_ID, TEST_HASH_1, TEST_IPFS_URI);

      const cred = await registry.verifyByStudentId(TEST_STUDENT_ID);
      expect(cred.studentId).to.equal(TEST_STUDENT_ID);
      expect(cred.sha256Hash).to.equal(TEST_HASH_1);
    });

    it("Returns empty struct when verifying non-existent studentId", async function () {
      const { registry } = await loadFixture(deployCredentialRegistryFixture);
      const cred = await registry.verifyByStudentId("NON_EXISTENT_ID");
      expect(cred.issuedAt).to.equal(0n);
    });

    it("isCredentialValid returns true for active credential and false for unknown hash", async function () {
      const { registry } = await loadFixture(deployCredentialRegistryFixture);
      await registry.issueCredential(TEST_STUDENT_ID, TEST_HASH_1, TEST_IPFS_URI);

      expect(await registry.isCredentialValid(TEST_HASH_1)).to.be.true;
      expect(await registry.isCredentialValid(TEST_HASH_2)).to.be.false;
    });
  });

  // ───────────────────────────────────────────────────────────────────────────
  // 5. Credential Revocation Tests
  // ───────────────────────────────────────────────────────────────────────────
  describe("5. Credential Revocation", function () {
    it("Allows authorized issuer to revoke a credential and emits CredentialRevoked", async function () {
      const { registry, owner } = await loadFixture(deployCredentialRegistryFixture);
      await registry.issueCredential(TEST_STUDENT_ID, TEST_HASH_1, TEST_IPFS_URI);

      const tx = await registry.revokeCredential(TEST_HASH_1);
      const receipt = await tx.wait();
      const block = await ethers.provider.getBlock(receipt.blockNumber);

      await expect(tx)
        .to.emit(registry, "CredentialRevoked")
        .withArgs(TEST_HASH_1, TEST_STUDENT_ID, owner.address, block.timestamp);

      expect(await registry.totalRevoked()).to.equal(1n);

      const cred = await registry.verifyByHash(TEST_HASH_1);
      expect(cred.isRevoked).to.be.true;
      expect(await registry.isCredentialValid(TEST_HASH_1)).to.be.false;
    });

    it("Reverts if unauthorized caller attempts to revoke", async function () {
      const { registry, unauthorizedUser } = await loadFixture(deployCredentialRegistryFixture);
      await registry.issueCredential(TEST_STUDENT_ID, TEST_HASH_1, TEST_IPFS_URI);

      await expect(registry.connect(unauthorizedUser).revokeCredential(TEST_HASH_1))
        .to.be.revertedWithCustomError(registry, "NotAuthorised")
        .withArgs(unauthorizedUser.address);
    });

    it("Reverts if attempting to revoke a non-existent credential", async function () {
      const { registry } = await loadFixture(deployCredentialRegistryFixture);
      await expect(registry.revokeCredential(TEST_HASH_1))
        .to.be.revertedWithCustomError(registry, "CredentialNotFound")
        .withArgs(TEST_HASH_1);
    });

    it("Reverts if credential is already revoked", async function () {
      const { registry } = await loadFixture(deployCredentialRegistryFixture);
      await registry.issueCredential(TEST_STUDENT_ID, TEST_HASH_1, TEST_IPFS_URI);
      await registry.revokeCredential(TEST_HASH_1);

      await expect(registry.revokeCredential(TEST_HASH_1))
        .to.be.revertedWithCustomError(registry, "CredentialAlreadyRevoked")
        .withArgs(TEST_HASH_1);
    });
  });

  // ───────────────────────────────────────────────────────────────────────────
  // 6. Emergency Circuit-Breaker (Pausable) Tests
  // ───────────────────────────────────────────────────────────────────────────
  describe("6. Emergency Circuit-Breaker (Pause / Unpause)", function () {
    it("Owner can pause and unpause the contract", async function () {
      const { registry } = await loadFixture(deployCredentialRegistryFixture);
      expect(await registry.paused()).to.be.false;

      await registry.pause();
      expect(await registry.paused()).to.be.true;

      await registry.unpause();
      expect(await registry.paused()).to.be.false;
    });

    it("Non-owner cannot pause or unpause", async function () {
      const { registry, unauthorizedUser } = await loadFixture(deployCredentialRegistryFixture);
      await expect(registry.connect(unauthorizedUser).pause())
        .to.be.revertedWithCustomError(registry, "OwnableUnauthorizedAccount");
    });

    it("Reverts issuance and revocation when paused, but allows verification", async function () {
      const { registry } = await loadFixture(deployCredentialRegistryFixture);
      await registry.issueCredential(TEST_STUDENT_ID, TEST_HASH_1, TEST_IPFS_URI);

      await registry.pause();

      // State-changing calls must revert with EnforcedPause
      await expect(registry.issueCredential(TEST_STUDENT_ID_2, TEST_HASH_2, TEST_IPFS_URI))
        .to.be.revertedWithCustomError(registry, "EnforcedPause");

      await expect(registry.revokeCredential(TEST_HASH_1))
        .to.be.revertedWithCustomError(registry, "EnforcedPause");

      // Read-only verification functions must remain functional while paused
      const cred = await registry.verifyByHash(TEST_HASH_1);
      expect(cred.studentId).to.equal(TEST_STUDENT_ID);
      expect(await registry.isCredentialValid(TEST_HASH_1)).to.be.true;
    });
  });
});

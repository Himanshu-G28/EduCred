// scripts/deploy.js
// ─────────────────────────────────────────────────────────────────────────────
// Deployment script for CredentialRegistry.sol
// Compatible with: Ethers.js v6  +  Hardhat 2.22+
//
// HOW TO RUN
// ──────────
//   Local Hardhat Network (ephemeral, no node needed):
//     npx hardhat run scripts/deploy.js
//
//   Persistent local node (keep node running in another terminal):
//     npx hardhat run scripts/deploy.js --network localhost
//
//   Polygon Amoy Testnet:
//     npx hardhat run scripts/deploy.js --network polygon_amoy
//
// ─────────────────────────────────────────────────────────────────────────────

const { ethers } = require("hardhat");

// ─── Configuration ────────────────────────────────────────────────────────────
// Change this to match your institution name before deploying to a testnet.
const INSTITUTION_NAME = "NMIMS – Mukesh Patel School of Technology Management & Engineering";

// ─────────────────────────────────────────────────────────────────────────────
async function main() {

  // ── 1. Print environment info ───────────────────────────────────────────────
  console.log("\n" + "═".repeat(65));
  console.log("  CredentialRegistry — Deployment Script");
  console.log("  DE-2 | NMIMS B.Tech CSE | Himanshu Garg (E250)");
  console.log("═".repeat(65));

  // Get the network name and block info for logging
  const network = await ethers.provider.getNetwork();
  console.log(`\n📡 Network     : ${network.name} (chainId: ${network.chainId})`);

  const blockNumber = await ethers.provider.getBlockNumber();
  console.log(`📦 Block number: ${blockNumber}`);

  // ── 2. Get the deployer account ─────────────────────────────────────────────
  // ethers.getSigners() returns all accounts configured for this network.
  // accounts[0] is the deployer — it pays the deployment gas fee.
  const [deployer] = await ethers.getSigners();
  const deployerAddress = await deployer.getAddress();

  console.log(`\n🔑 Deployer address : ${deployerAddress}`);

  // Show deployer balance (useful to confirm the account is funded on testnet)
  const balanceWei = await ethers.provider.getBalance(deployerAddress);
  const balanceEth = ethers.formatEther(balanceWei);
  console.log(`💰 Deployer balance : ${balanceEth} ETH / MATIC`);

  if (parseFloat(balanceEth) === 0) {
    // Only warn — don't abort; on a local Hardhat network the balance reads
    // as 10000 ETH by default, so this branch won't trigger locally.
    console.warn("\n⚠️  WARNING: Deployer balance is zero. On a live testnet this");
    console.warn("   deployment will fail. Get test tokens from the faucet first.\n");
  }

  // ── 3. Compile & get ContractFactory ────────────────────────────────────────
  console.log("\n⚙️  Compiling CredentialRegistry.sol ...");

  // getContractFactory resolves the compiled artifact from the /artifacts folder.
  // If you haven't compiled yet, run: npx hardhat compile
  const CredentialRegistry = await ethers.getContractFactory("CredentialRegistry");

  // ── 4. Deploy ────────────────────────────────────────────────────────────────
  console.log(`\n🚀 Deploying with institution name: "${INSTITUTION_NAME}"`);
  console.log("   (waiting for transaction to be mined...)");

  // The constructor argument is INSTITUTION_NAME.
  // deploy() broadcasts the transaction and returns a Contract object.
  const registry = await CredentialRegistry.deploy(INSTITUTION_NAME);

  // waitForDeployment() (Ethers v6) waits until the contract is mined.
  // In Ethers v5 this was called .deployed().
  await registry.waitForDeployment();

  // Resolve the deployed contract address
  const contractAddress = await registry.getAddress();

  // ── 5. Post-deployment verification reads ────────────────────────────────────
  const deployedName   = await registry.institutionName();
  const deployedOwner  = await registry.owner();
  const totalIssued    = await registry.totalIssued();
  const deployTxHash   = registry.deploymentTransaction().hash;

  console.log("\n✅ Deployment SUCCESSFUL");
  console.log("─".repeat(65));
  console.log(`   Contract address : ${contractAddress}`);
  console.log(`   Transaction hash : ${deployTxHash}`);
  console.log(`   Institution name : ${deployedName}`);
  console.log(`   Owner (admin)    : ${deployedOwner}`);
  console.log(`   Total issued     : ${totalIssued.toString()}`);
  console.log("─".repeat(65));

  // ── 6. Quick smoke test — issue one test credential ──────────────────────────
  console.log("\n🧪 Running smoke test: issueCredential ...");

  // Sample data — in production these come from the React frontend
  const testStudentId   = "70552400057";                   // SAP ID
  const testSHA256Hash  =                                  // Dummy SHA-256 (32 bytes)
    "0x" + "a".repeat(64);                                 // All 0xaaa... for testing
  const testIPFSUri     = "ipfs://QmTestHash000000000000"; // Dummy IPFS URI

  // Call issueCredential from the deployer (who is the owner = authorised)
  const issueTx = await registry.issueCredential(
    testStudentId,
    testSHA256Hash,
    testIPFSUri
  );
  await issueTx.wait(); // Wait for the transaction to be mined

  console.log("   ✔ issueCredential() — mined in tx: " + issueTx.hash);

  // ── 7. Smoke test — verify the credential just issued ─────────────────────────
  const result = await registry.verifyByStudentId(testStudentId);
  const isValid = await registry.isCredentialValid(testSHA256Hash);

  console.log("   ✔ verifyByStudentId() returned:");
  console.log(`       studentId  : ${result.studentId}`);
  console.log(`       sha256Hash : ${result.sha256Hash}`);
  console.log(`       ipfsURI    : ${result.ipfsURI}`);
  console.log(`       issuedAt   : ${new Date(Number(result.issuedAt) * 1000).toISOString()}`);
  console.log(`       isRevoked  : ${result.isRevoked}`);
  console.log(`   ✔ isCredentialValid()  : ${isValid}`);

  // ── 8. Print .env hint for the React frontend ─────────────────────────────────
  console.log("\n─".repeat(65));
  console.log("📋 Add this to your React frontend .env:");
  console.log(`   REACT_APP_CONTRACT_ADDRESS=${contractAddress}`);
  console.log(`   REACT_APP_NETWORK_CHAIN_ID=${network.chainId}`);

  // ── 9. Testnet verification hint ──────────────────────────────────────────────
  if (network.name !== "hardhat" && network.name !== "localhost") {
    console.log("\n🔍 Verify on Polygonscan (wait ~30s for indexing first):");
    console.log(
      `   npx hardhat verify --network ${network.name} ${contractAddress} "${INSTITUTION_NAME}"`
    );
  }

  console.log("\n" + "═".repeat(65) + "\n");
}

// ─── Entry Point ──────────────────────────────────────────────────────────────
// Standard Hardhat error-handling wrapper.
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("\n❌ Deployment FAILED:");
    console.error(error);
    process.exit(1);
  });

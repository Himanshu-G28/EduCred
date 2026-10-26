// hardhat.config.js
// ─────────────────────────────────────────────────────────────────────────────
// Hardhat configuration for CredentialRegistry
// Project: Design and Implementation of a Blockchain Enabled Framework
//          for Secure Educational Credentials in India
// Author : Himanshu Garg — NMIMS B.Tech CSE, DE-2 (Sem 5)
// ─────────────────────────────────────────────────────────────────────────────
//
// SETUP INSTRUCTIONS (run once in your project root):
// ────────────────────────────────────────────────────
//   npm init -y
//   npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox
//   npm install @openzeppelin/contracts
//   npm install dotenv
//
// Then create a .env file (NEVER commit this to Git!):
//   PRIVATE_KEY=0xYOUR_METAMASK_PRIVATE_KEY_HERE
//   POLYGON_AMOY_RPC_URL=https://rpc-amoy.polygon.technology
//   POLYGONSCAN_API_KEY=YOUR_POLYGONSCAN_KEY
//
// ─────────────────────────────────────────────────────────────────────────────

require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

// ── Read secrets from .env ──────────────────────────────────────────────────
// If the variable is missing we fall back to a dummy key so `npx hardhat compile`
// still works without a .env file.  Deployment to a live network will fail
// gracefully (Ethers will throw "invalid private key") rather than crashing
// the config loader.
const PRIVATE_KEY =
  process.env.PRIVATE_KEY ||
  "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"; // Hardhat default account #0

const POLYGON_AMOY_RPC_URL =
  process.env.POLYGON_AMOY_RPC_URL || "https://rpc-amoy.polygon.technology";

const POLYGONSCAN_API_KEY = process.env.POLYGONSCAN_API_KEY || "";

// ─────────────────────────────────────────────────────────────────────────────
/** @type {import('hardhat/config').HardhatUserConfig} */
module.exports = {

  // ── Solidity compiler ──────────────────────────────────────────────────────
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,  // 200 = balanced between deployment cost and call cost
      },
      // Enable ABIEncoderV2 for returning structs from view functions
      // (automatically enabled in 0.8.x; explicit here for clarity)
      viaIR: false,
    },
  },

  // ── Network configurations ─────────────────────────────────────────────────
  networks: {

    // ── 1. Hardhat built-in network (default for tests and local scripts) ──
    // No config needed — `npx hardhat run scripts/deploy.js` uses this automatically.
    // 20 pre-funded accounts, instant mining, deterministic addresses.
    hardhat: {
      chainId: 31337,
      // Uncomment to fork Polygon mainnet for realistic testing:
      // forking: {
      //   url: "https://polygon-rpc.com",
      //   blockNumber: 59000000,
      // },
    },

    // ── 2. Local Hardhat node (npx hardhat node) ──────────────────────────
    // Use this when you want a PERSISTENT local node that stays running
    // in a separate terminal (so MetaMask can connect to localhost:8545).
    //   Terminal 1: npx hardhat node
    //   Terminal 2: npx hardhat run scripts/deploy.js --network localhost
    localhost: {
      url: "http://127.0.0.1:8545",
      chainId: 31337,
    },

    // ── 3. Polygon Amoy Testnet (replaces Mumbai as of 2024) ─────────────
    // Free test MATIC from: https://faucet.polygon.technology/
    // Block explorer:       https://amoy.polygonscan.com/
    polygon_amoy: {
      url: POLYGON_AMOY_RPC_URL,
      chainId: 80002,
      accounts: [PRIVATE_KEY],
      gasPrice: "auto",
    },

    // ── 4. Sepolia Testnet (Ethereum) — alternative for testing ───────────
    // Free ETH from: https://sepoliafaucet.com/
    // sepolia: {
    //   url: process.env.SEPOLIA_RPC_URL || "https://rpc.sepolia.org",
    //   chainId: 11155111,
    //   accounts: [PRIVATE_KEY],
    // },
  },

  // ── Etherscan / Polygonscan verification ───────────────────────────────────
  // After deploying to Amoy, verify with:
  //   npx hardhat verify --network polygon_amoy DEPLOYED_ADDRESS "NMIMS – MPSTME"
  etherscan: {
    apiKey: {
      polygon_amoy: POLYGONSCAN_API_KEY,
      // sepolia: process.env.ETHERSCAN_API_KEY || "",
    },
    customChains: [
      {
        network: "polygon_amoy",
        chainId: 80002,
        urls: {
          apiURL:    "https://api-amoy.polygonscan.com/api",
          browserURL: "https://amoy.polygonscan.com",
        },
      },
    ],
  },

  // ── Gas reporter (optional — shows gas usage per function after tests) ─────
  // npm install --save-dev hardhat-gas-reporter
  // gasReporter: {
  //   enabled: true,
  //   currency: "USD",
  //   coinmarketcap: process.env.CMC_API_KEY,
  // },

  // ── Paths (Hardhat defaults — listed here for clarity) ────────────────────
  paths: {
    sources:   "./contracts",
    tests:     "./test",
    cache:     "./cache",
    artifacts: "./artifacts",
  },
};

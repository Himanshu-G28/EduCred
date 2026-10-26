import { ethers } from 'ethers';
import CredentialRegistryArtifact from './CredentialRegistry.json';

export const CONTRACT_ABI = CredentialRegistryArtifact.abi;

// Default to local Hardhat node contract address; allows override via Vite env
export const DEFAULT_CONTRACT_ADDRESS = 
  import.meta.env.VITE_CONTRACT_ADDRESS || "0x5FbDB2315678afecb367f032d93F642f64180aa3";

export const SUPPORTED_NETWORKS = {
  31337: {
    chainId: "0x7a69",
    name: "Hardhat Localhost",
    rpcUrl: "http://127.0.0.1:8545",
    currency: "GO",
    symbol: "ETH",
    explorer: null,
  },
  80002: {
    chainId: "0x13882",
    name: "Polygon Amoy Testnet",
    rpcUrl: "https://rpc-amoy.polygon.technology",
    currency: "MATIC",
    symbol: "MATIC",
    explorer: "https://amoy.polygonscan.com",
  },
};

/**
 * Instantiate an ethers.Contract instance with a Signer or Provider.
 */
export function getContractInstance(address, signerOrProvider) {
  const targetAddress = address || DEFAULT_CONTRACT_ADDRESS;
  return new ethers.Contract(targetAddress, CONTRACT_ABI, signerOrProvider);
}

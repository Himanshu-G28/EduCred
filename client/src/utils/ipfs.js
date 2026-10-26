/**
 * IPFS storage utility for credential documents.
 * Supports:
 * 1. Live pinning via Pinata REST API (when PINATA_JWT is provided).
 * 2. Deterministic offline/demo IPFS fallback (for isolated campus viva / local evaluations).
 */

const PINATA_JWT = import.meta.env.VITE_PINATA_JWT || '';

// In-memory/session cache for mock pinned documents
const mockIpfsStore = new Map();

/**
 * Uploads a credential PDF file to IPFS.
 * @param {File} file - The PDF file object
 * @param {string} studentId - Student identifier for Pinata metadata
 * @returns {Promise<{ ipfsURI: string, gatewayURL: string, isMock: boolean }>}
 */
export async function uploadToIPFS(file, studentId) {
  // If a Pinata JWT is configured in environment, use real Pinata IPFS
  if (PINATA_JWT && PINATA_JWT.trim() !== '') {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const metadata = JSON.stringify({
        name: `Credential_${studentId}_${file.name}`,
        keyvalues: {
          studentId: studentId,
          timestamp: Date.now().toString(),
          institution: "NMIMS MPSTME"
        }
      });
      formData.append('pinataMetadata', metadata);

      const res = await fetch('https://api.pinata.cloud/pinning/pinFileToIPFS', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${PINATA_JWT}`
        },
        body: formData
      });

      if (!res.ok) {
        throw new Error(`Pinata upload failed with status ${res.status}`);
      }

      const data = await res.json();
      const ipfsHash = data.IpfsHash;
      return {
        ipfsURI: `ipfs://${ipfsHash}`,
        gatewayURL: `https://gateway.pinata.cloud/ipfs/${ipfsHash}`,
        isMock: false
      };
    } catch (err) {
      console.warn("Pinata upload failed, falling back to local IPFS simulation:", err);
    }
  }

  // Robust College Viva Offline / Simulation Mode:
  // Generate deterministic CIDv0 based on content and store in memory
  const arrayBuffer = await file.arrayBuffer();
  const hashBuffer = await window.crypto.subtle.digest('SHA-256', arrayBuffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hexHash = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  
  // Base58-like pseudo CIDv0 for demonstration
  const mockCID = `Qm${hexHash.substring(0, 44)}`;
  const ipfsURI = `ipfs://${mockCID}`;
  
  // Create downloadable object URL
  const blob = new Blob([arrayBuffer], { type: 'application/pdf' });
  const objectUrl = URL.createObjectURL(blob);
  mockIpfsStore.set(ipfsURI, objectUrl);

  return {
    ipfsURI,
    gatewayURL: objectUrl,
    isMock: true
  };
}

/**
 * Resolves an ipfs:// URI to an HTTP gateway URL for browser viewing.
 */
export function resolveIPFSUrl(ipfsURI) {
  if (!ipfsURI) return '';
  if (mockIpfsStore.has(ipfsURI)) {
    return mockIpfsStore.get(ipfsURI);
  }
  if (ipfsURI.startsWith('ipfs://')) {
    const cid = ipfsURI.replace('ipfs://', '');
    return `https://ipfs.io/ipfs/${cid}`;
  }
  return ipfsURI;
}

/**
 * Cryptographic utility functions using the native W3C Web Crypto API.
 * Guarantees standard FIPS 180-4 SHA-256 calculation without external dependencies.
 */

/**
 * Computes the SHA-256 hash of a File or Blob.
 * @param {File | Blob} file
 * @returns {Promise<{ hexHash: string, bytes32: string, arrayBuffer: ArrayBuffer }>}
 */
export async function calculateFileSHA256(file) {
  const arrayBuffer = await file.arrayBuffer();
  return computeBufferSHA256(arrayBuffer);
}

/**
 * Computes the SHA-256 hash of an ArrayBuffer.
 * @param {ArrayBuffer} buffer
 * @returns {Promise<{ hexHash: string, bytes32: string, arrayBuffer: ArrayBuffer }>}
 */
export async function computeBufferSHA256(buffer) {
  const hashBuffer = await window.crypto.subtle.digest('SHA-256', buffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hexHash = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  const bytes32 = '0x' + hexHash;
  return {
    hexHash,
    bytes32,
    buffer
  };
}

/**
 * Simulates bit-level tampering on a file buffer for the DE-2 live defense demo.
 * Inverts the very first byte of the file, demonstrating the SHA-256 Avalanche Effect.
 * @param {ArrayBuffer} originalBuffer
 * @returns {ArrayBuffer} tamperedBuffer
 */
export function simulateTampering(originalBuffer) {
  const copy = originalBuffer.slice(0);
  const view = new Uint8Array(copy);
  if (view.length > 0) {
    // Flip least-significant bit of first byte
    view[0] = view[0] ^ 0x01;
  }
  return copy;
}

/**
 * Helper to truncate long Ethereum addresses or hashes for UI display.
 */
export function truncateAddress(address, start = 6, end = 4) {
  if (!address) return '';
  if (address.length <= start + end) return address;
  return `${address.substring(0, start)}...${address.substring(address.length - end)}`;
}

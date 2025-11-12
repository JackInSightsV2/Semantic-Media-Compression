/**
 * NOTE: Story Protocol registration is now handled by the backend via Python SDK.
 * This file is kept for utility functions that may still be needed (like NFT collection creation scripts).
 * 
 * All IP Asset registration should go through the backend API: /api/registration/register-story
 */

import { StoryClient, StoryConfig } from '@story-protocol/core-sdk';
import { http } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';

let storyClient: StoryClient | null = null;

/**
 * Get Story Protocol client (for utility scripts only, not for registration)
 * @deprecated Registration should use backend API instead
 */
export function getStoryClient() {
 if (!storyClient) {
  const rawPk = process.env.NEXT_PUBLIC_WALLET_PRIVATE_KEY as string;
  if (!rawPk) {
    throw new Error('Wallet private key env is not set');
  }

  // Normalize common formats (with/without 0x, accidental quotes/whitespace)
  const normalizePrivateKey = (pk: string): `0x${string}` => {
    const trimmed = pk.trim().replace(/^['"]|['"]$/g, '');
    const prefixed = trimmed.startsWith('0x') ? trimmed : `0x${trimmed}`;
    if (!/^0x[0-9a-fA-F]{64}$/.test(prefixed)) {
      throw new Error('Wallet private key appears malformed (expected 64 hex chars)');
    }
    return prefixed as `0x${string}`;
  };

  const privateKey = normalizePrivateKey(rawPk);
  
   if (!privateKey) {
     throw new Error('NEXT_PUBLIC_WALLET_PRIVATE_KEY is not set');
   }

   const config: StoryConfig = {
     account: privateKeyToAccount(privateKey),
     transport: http(process.env.NEXT_PUBLIC_STORY_RPC_URL),
     chainId: 'aeneid', // Story testnet (iliad was renamed to aeneid)
   };

   storyClient = StoryClient.newClient(config);
 }
  return storyClient;
}

/**
 * @deprecated Use backend API /api/registration/register-story instead
 * Story Protocol registration is now handled by the backend Python SDK
 */
export async function registerIPAsset(params: {
  ipMetadataURI: string;
  ipMetadataHash: `0x${string}`;
  nftMetadataURI: string;
  nftMetadataHash: `0x${string}`;
}) {
  throw new Error(
    'registerIPAsset is deprecated. Use backend API: POST /api/registration/register-story ' +
    'The backend now handles all Story Protocol registration via Python SDK.'
  );
}

/**
 * @deprecated Dispute filing should be handled by backend API
 * This is kept as a placeholder but should be moved to backend
 */
export async function fileDispute(
 originalIpId: string,
 suspectedIpId: string,
 evidenceIpfsHash: string
) {
  throw new Error(
    'fileDispute is deprecated. Dispute filing should be handled by the backend API.'
  );
}



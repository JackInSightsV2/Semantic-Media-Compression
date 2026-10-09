import type { StoryClient } from '@story-protocol/core-sdk';

// Archived browser demo: no private-key signing or simulated transaction success.
const WRITE_DISABLED = 'Story writes are disabled: an authenticated server-side credentials integration or user-wallet signing is required. No transaction was submitted.';

export function getStoryClient(): StoryClient {
  throw new Error(WRITE_DISABLED);
}

export async function registerIPAsset(_params: {
  ipMetadataURI: string;
  ipMetadataHash: `0x${string}`;
  nftMetadataURI: string;
  nftMetadataHash: `0x${string}`;
}): Promise<{ ipAssetId: string; txHash: string; tokenId: string }> {
  throw new Error(WRITE_DISABLED);
}

export async function fileDispute(
  _originalIpId: string,
  _suspectedIpId: string,
  _evidenceIpfsHash: string
): Promise<{ disputeId: string; txHash: string; evidenceIPFS: string }> {
  throw new Error(WRITE_DISABLED);
}

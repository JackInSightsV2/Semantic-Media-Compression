import { StoryClient, StoryConfig } from '@story-protocol/core-sdk';
import { http } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';

let storyClient: StoryClient | null = null;

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

export async function registerIPAsset(params: {
  ipMetadataURI: string; // ipfs://<cid>
  ipMetadataHash: `0x${string}`; // sha256 0x-prefixed
  nftMetadataURI: string; // ipfs://<cid>
  nftMetadataHash: `0x${string}`; // sha256 0x-prefixed
}) {
 try {
   const client = getStoryClient();
  
   // Register IP Asset using the Story Protocol SDK
   // Using mintAndRegisterIpAssetWithPilTerms with non-commercial-social-remixing license
   const response = await client.ipAsset.mintAndRegisterIpAssetWithPilTerms({
     spgNftContract: process.env.NEXT_PUBLIC_NFT_CONTRACT_ADDRESS as `0x${string}`,
     licenseTermsData: [
       {
         terms: {
           transferable: true,
           royaltyPolicy: '0x0000000000000000000000000000000000000000', // No royalty for POC
           defaultMintingFee: 0n,
           expiration: 0n,
           commercialUse: false,
           commercialAttribution: false,
           commercializerChecker: '0x0000000000000000000000000000000000000000',
           commercializerCheckerData: '0x' as `0x${string}`,
           commercialRevShare: 0,
           commercialRevCeiling: 0n,
          derivativesAllowed: true,
          derivativesAttribution: true,
          derivativesApproval: false,
          derivativesReciprocal: true,
          derivativeRevCeiling: 0n,
          currency: '0x0000000000000000000000000000000000000000',
           uri: '',
         },
       },
     ],
    ipMetadata: {
      ipMetadataURI: params.ipMetadataURI,
      ipMetadataHash: params.ipMetadataHash,
      nftMetadataURI: params.nftMetadataURI,
      nftMetadataHash: params.nftMetadataHash,
    },
   });
  
   return {
     ipAssetId: response.ipId as string,
     txHash: response.txHash as string,
     tokenId: response.tokenId?.toString() || 'N/A',
   };
 } catch (error) {
   console.error('Story Protocol registration failed:', error);
   throw error;
 }
}

export async function fileDispute(
 originalIpId: string,
 suspectedIpId: string,
 evidenceIpfsHash: string
) {
 try {
   const client = getStoryClient();
  
   // Note: Dispute functionality may vary based on Story Protocol SDK version
   // This is a placeholder - check SDK docs for current dispute methods
   console.log('Filing dispute with evidence:', evidenceIpfsHash);
  
   // Placeholder return for POC
   return {
     disputeId: '0xdispute' + Math.random().toString(16).substr(2, 36),
     txHash: '0x' + Math.random().toString(16).substr(2, 64),
     evidenceIPFS: evidenceIpfsHash,
   };
 } catch (error) {
   console.error('Story Protocol dispute filing failed:', error);
   throw error;
 }
}



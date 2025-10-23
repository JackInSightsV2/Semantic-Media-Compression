import { StoryClient, StoryConfig } from '@story-protocol/core-sdk';
import { http } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';

let storyClient: StoryClient | null = null;

export function getStoryClient() {
 if (!storyClient) {
   const privateKey = process.env.NEXT_PUBLIC_WALLET_PRIVATE_KEY as `0x${string}`;
  
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

export async function registerIPAsset(metadata: {
 name: string;
 description: string;
 ipfsHash: string;
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
           derivativeRevCelling: 0n,
           currency: '0x0000000000000000000000000000000000000000',
           uri: '',
         },
       },
     ],
     ipMetadata: {
       ipMetadataURI: `ipfs://${metadata.ipfsHash}`,
       ipMetadataHash: `0x${metadata.ipfsHash}` as `0x${string}`,
       nftMetadataURI: `ipfs://${metadata.ipfsHash}`,
       nftMetadataHash: `0x${metadata.ipfsHash}` as `0x${string}`,
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



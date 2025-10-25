import { getStoryClient } from './StoryProtocol';

/**
* Creates a new SPG NFT Collection for registering IP Assets
* This only needs to be done ONCE per application
*
* @returns The contract address of the newly created SPG NFT collection
*/
export async function createSPGNFTCollection() {
 try {
   const client = getStoryClient();
  
   // Get the wallet address from the environment
   const walletAddress = process.env.NEXT_PUBLIC_WALLET_ADDRESS;
   if (!walletAddress) {
     throw new Error('NEXT_PUBLIC_WALLET_ADDRESS is not set in .env file');
   }
  
   console.log('📦 Creating SPG NFT Collection...');
   console.log('   Owner:', walletAddress);
  
   // Create a new SPG NFT collection
   const response = await client.nftClient.createNFTCollection({
     name: 'Semantic IP Collection',
     symbol: 'SIP',
     isPublicMinting: true, // Allow public minting
     mintOpen: true, // Open for minting
     mintFeeRecipient: walletAddress as `0x${string}`, // Where mint fees go (if any)
     contractURI: '', // Contract metadata URI (empty for now)
     maxSupply: 1000, // Maximum number of NFTs that can be minted
     owner: walletAddress as `0x${string}`,
   });
  
   console.log('✅ SPG NFT Collection Created!');
   console.log('   Contract Address:', response.spgNftContract);
   console.log('   Transaction Hash:', response.txHash);
  
   return {
     nftContractAddress: response.spgNftContract as string,
     txHash: response.txHash as string,
   };
 } catch (error) {
   console.error('❌ Failed to create SPG NFT Collection:', error);
   throw error;
 }
}

/**
* Checks if an NFT collection address is valid
*/
export async function isValidNFTCollection(address: string): Promise<boolean> {
 try {
   // Basic validation: check if it looks like an Ethereum address
   if (!address || !address.startsWith('0x') || address.length !== 42) {
     return false;
   }
   // For now, just validate the format. 
   // Could add more sophisticated checks if needed in the future.
   return true;
 } catch (error) {
   return false;
 }
}



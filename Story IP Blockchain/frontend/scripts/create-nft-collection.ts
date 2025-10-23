/**
 * Script to create an SPG NFT Collection for Story Protocol
 * Run this ONCE before using the registration features
 * 
 * Usage:
 *   npx tsx scripts/create-nft-collection.ts
 */

// Load environment variables from .env file
import { config } from 'dotenv';
import { resolve } from 'path';

// Load .env file from the frontend directory
config({ path: resolve(__dirname, '../.env') });

import { createSPGNFTCollection } from '../blocklibs/nftCollection';

async function main() {
  console.log('========================================');
  console.log('Story Protocol - Create NFT Collection');
  console.log('========================================\n');
  
  console.log('This will create a new SPG NFT Collection for your semantic IP assets.');
  console.log('You only need to do this ONCE.\n');
  
  try {
    const result = await createSPGNFTCollection();
    
    console.log('\n========================================');
    console.log('✅ SUCCESS!');
    console.log('========================================\n');
    
    console.log('📝 ADD THIS TO YOUR .env FILE:\n');
    console.log(`NEXT_PUBLIC_NFT_CONTRACT_ADDRESS=${result.nftContractAddress}\n`);
    
    console.log('🔍 View on Explorer:');
    console.log(`https://aeneid.storyscan.io/address/${result.nftContractAddress}\n`);
    
    console.log('🔗 Transaction:');
    console.log(`https://aeneid.storyscan.io/tx/${result.txHash}\n`);
    
    console.log('✨ You can now use the registration features!\n');
    
  } catch (error: any) {
    console.error('\n❌ ERROR:', error.message);
    console.error('\nTroubleshooting:');
    console.error('1. Make sure your .env file has all required variables');
    console.error('2. Check that your wallet has testnet tokens');
    console.error('3. Verify you\'re connected to Story testnet (aeneid)');
    console.error('4. Check the RPC URL is correct: https://testnet.storyrpc.io\n');
    process.exit(1);
  }
}

main();


# Story Protocol Integration - Setup & Testing Guide

## Overview
This guide will help you test the Story Protocol integration with IPFS for semantic IP registration.

## Prerequisites Checklist

### ✅ Step 1: MetaMask Wallet Setup
- [ ] Created a new MetaMask account for testnet (or using existing)
- [ ] Added Story Protocol testnet to MetaMask:
  - Network Name: `Story Protocol Testnet`
  - RPC URL: `https://testnet.storyrpc.io`
  - Chain ID: `1513`
  - Currency Symbol: `IP`
  - Block Explorer: `https://testnet.storyscan.xyz`
- [ ] Copied private key and address to `.env` file
- [ ] Funded wallet with testnet tokens from Story faucet

### ✅ Step 2: Pinata IPFS Setup
- [ ] Signed up at https://pinata.cloud (free tier)
- [ ] Created API key with `pinFileToIPFS` permission
- [ ] Copied API Key, Secret Key, and JWT to `.env` file

### ✅ Step 3: Create Your SPG NFT Collection
**Important**: Story Protocol doesn't have a shared test NFT contract. You need to create your own SPG NFT Collection:
- [ ] Run `npm run create-collection` to create your NFT collection
- [ ] Copy the generated contract address
- [ ] Added contract address to `.env` file as `NEXT_PUBLIC_NFT_CONTRACT_ADDRESS`
- [ ] Verify on Story Explorer: https://aeneid.storyscan.io

### ✅ Step 4: Dependencies
- [ ] Run `npm install` in the frontend directory

## Environment Variables

Your `.env` file should contain:

```bash
# Wallet (from MetaMask)
NEXT_PUBLIC_WALLET_PRIVATE_KEY=0x...
NEXT_PUBLIC_WALLET_ADDRESS=0x...

# Story Protocol Testnet
NEXT_PUBLIC_STORY_RPC_URL=https://testnet.storyrpc.io
NEXT_PUBLIC_STORY_CHAIN_ID=1513

# NFT Contract for Story Protocol
NEXT_PUBLIC_NFT_CONTRACT_ADDRESS=0x...

# Pinata IPFS
NEXT_PUBLIC_PINATA_API_KEY=...
NEXT_PUBLIC_PINATA_SECRET_KEY=...
NEXT_PUBLIC_PINATA_JWT=...
```

## Testing the Integration

### Test 1: IPFS Upload (Independent Test)

Before running the full app, test IPFS upload independently:

```bash
# In frontend directory
node -e "
const axios = require('axios');
const fs = require('fs');

const testData = { test: 'hello from Story Protocol!' };
const blob = JSON.stringify(testData);

const FormData = require('form-data');
const formData = new FormData();
formData.append('file', Buffer.from(blob), 'test.json');

axios.post('https://api.pinata.cloud/pinning/pinFileToIPFS', formData, {
  headers: {
    'Authorization': 'Bearer ' + process.env.NEXT_PUBLIC_PINATA_JWT,
    ...formData.getHeaders()
  }
}).then(res => {
  console.log('✅ IPFS Upload Success!');
  console.log('IPFS Hash:', res.data.IpfsHash);
  console.log('View at: https://gateway.pinata.cloud/ipfs/' + res.data.IpfsHash);
}).catch(err => {
  console.error('❌ IPFS Upload Failed:', err.response?.data || err.message);
});
"
```

### Test 2: Run Development Server

```bash
cd frontend
npm run dev
```

Open http://localhost:3000

### Test 3: Register Content Flow

1. Navigate to `/register` page
2. Select one of the demo content options
3. Click "Register IP Asset on Story Protocol"
4. **Watch the browser console** for:
   ```
   📤 Uploading semantic JSON to IPFS...
   ✅ Uploaded to IPFS: QmXXX...
   ⛓️  Registering on Story Protocol...
   ✅ Registered on Story Protocol!
      IP Asset ID: 0xXXX...
      Token ID: XXX
      Transaction Hash: 0xXXX...
   ```

5. **Expected outcomes:**
   - **Success**: Green "✅ Live Blockchain" badge appears
   - **Fallback**: Yellow "⚠️ Mock Mode (Demo)" badge appears if blockchain fails
   - Links to blockchain explorer should work (if success)
   - IPFS hash link should work (if success)

### Test 4: Compare Content Flow

1. Navigate to `/compare` page
2. **Option A - Mock Mode (Default)**:
   - Select original and suspected content from dropdowns
   - Click "Compare Semantic Fingerprints"
   - View similarity analysis results

3. **Option B - IPFS Mode** (if you registered content):
   - Check "Fetch from IPFS" checkbox
   - Enter the IPFS hash from your registration (from Test 3)
   - Enter another IPFS hash (or use the same one)
   - Click "Compare Semantic Fingerprints"
   - Should fetch content from IPFS and compare

### Test 5: Dispute Filing (Optional)

1. Navigate to `/dispute` page
2. Select original and suspected IP assets
3. Click "Submit Dispute to Story Protocol"
4. Currently uses mock data (real dispute integration is placeholder)

## Troubleshooting

### IPFS Upload Fails

**Error: "Authorization failed"**
- Check `NEXT_PUBLIC_PINATA_JWT` is correct
- Verify JWT has `pinFileToIPFS` permission
- Try regenerating JWT in Pinata dashboard

**Error: "File size too large"**
- Semantic JSONs are ~2MB which should be fine
- Free tier limit is 100MB per file
- Check if you hit total storage limit (1GB free tier)

### Story Protocol Registration Fails

**Error: "Wallet has insufficient funds"**
- Get more testnet tokens from Story faucet
- Check you're on Story testnet network

**Error: "NFT contract not found"**
- Verify `NEXT_PUBLIC_NFT_CONTRACT_ADDRESS` is correct
- Contract must be deployed on Story testnet
- Try using Story's official test NFT contract

**Error: "Private key invalid"**
- Ensure private key starts with `0x`
- Private key should be 66 characters (0x + 64 hex chars)
- Don't include quotes in `.env` file

**Error: "Cannot read properties of undefined"**
- Story Protocol SDK might have changed
- Check SDK version in `package.json`
- Refer to latest Story Protocol docs

### Fallback to Mock Mode

If blockchain fails, the app falls back to mock mode automatically:
- This is **expected behavior** for demo safety
- Check console for error details
- Yellow "⚠️ Mock Mode" badge will appear
- UI flow continues normally for demo purposes

## Demo Script

When presenting:

```
1. "Let me show you the registration process..."
   [Navigate to /register]

2. "We have three demo pieces of content with full semantic fingerprints"
   [Show the semantic layers - Narrative, Character, Thematic]

3. "Let me register this on Story Protocol..."
   [Click register button]
   [Show console logs]

4. "First, we upload the 2MB semantic JSON to IPFS..."
   "Now we register the IP Asset on Story Protocol testnet..."
   
5. [Show success screen with blockchain links]
   "The semantic fingerprint is permanently stored and verifiable on-chain"
   [Click explorer link to show on blockchain]

6. "Now let's detect plagiarism..."
   [Navigate to /compare]
   [Compare original with copycat]
   
7. "Even though the images are completely different, the semantic 
    meaning is 91% identical across 3 dimensions"
   [Show similarity breakdown]

8. If blockchain fails:
   "We have fallback mock data for demo reliability, but the flow 
    is identical to the real blockchain process"
```

## Key Features Implemented

### ✅ Hybrid Blockchain + Fallback
- Tries real Story Protocol transaction first
- Falls back to mock data if blockchain fails
- Visual indicator shows which mode is active

### ✅ IPFS Integration
- Uploads 2MB semantic JSONs to Pinata
- Stores IPFS CID on Story Protocol
- Fetches content from IPFS for comparison (optional)

### ✅ Story Protocol Integration
- Registers IP Assets on testnet
- Links to blockchain explorer
- Shows transaction hashes and IP Asset IDs

### ✅ Semantic Comparison
- Calculates cosine similarity across 3 dimensions
- Shows matching semantic elements
- Provides legal evidence for disputes

## Useful Links

- **Story Protocol Docs**: https://docs.story.foundation
- **Story Testnet Explorer**: https://testnet.storyscan.xyz
- **Pinata Dashboard**: https://app.pinata.cloud
- **Story Discord**: (check docs for invite link)
- **Story Faucet**: (check docs/Discord for current faucet URL)

## Next Steps

After successful testing:
1. Test multiple registrations to see blockchain history
2. Register content and use IPFS hashes in comparison
3. Verify transactions on Story Explorer
4. Prepare demo script for presentation
5. Consider adding error handling improvements
6. Add loading states for better UX
7. Implement real dispute filing if SDK supports it

## Support

If you encounter issues:
1. Check browser console for detailed error messages
2. Verify all environment variables are set correctly
3. Ensure wallet has testnet funds
4. Check Story Protocol Discord for testnet status
5. Verify Pinata API key has correct permissions


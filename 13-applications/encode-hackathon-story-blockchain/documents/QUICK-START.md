# Quick Start Guide - Story Protocol Integration

## ⚡ Get Running in 5 Minutes

### Step 1: Check Your Environment File
Your `.env` file should have these variables:

```bash
# Wallet
NEXT_PUBLIC_WALLET_PRIVATE_KEY=0x...
NEXT_PUBLIC_WALLET_ADDRESS=0x...

# Story Protocol
NEXT_PUBLIC_STORY_RPC_URL=https://testnet.storyrpc.io
NEXT_PUBLIC_STORY_CHAIN_ID=1513
NEXT_PUBLIC_NFT_CONTRACT_ADDRESS=0x...  # ← Get this from Story Protocol docs

# Pinata IPFS
NEXT_PUBLIC_PINATA_API_KEY=...
NEXT_PUBLIC_PINATA_SECRET_KEY=...
NEXT_PUBLIC_PINATA_JWT=...
```

### Step 2: Install & Run

```bash
cd "Story IP Blockchain/frontend"
npm install  # Already done
npm run dev
```

### Step 3: Open Browser
```
http://localhost:3000
```

### Step 4: Test It

1. **Test Mock Mode** (works immediately):
   ```
   → Go to /register
   → Select demo content
   → Click register
   → See mock data with yellow "Mock Mode" badge
   ```

2. **Test Blockchain Mode** (needs NFT contract):
   ```
   → Same steps as above
   → If NFT contract configured: see green "Live Blockchain" badge
   → Click explorer links to verify on blockchain
   ```

3. **Test Comparison**:
   ```
   → Go to /compare
   → Select original and copycat
   → Click compare
   → See 91% similarity across 3 dimensions
   ```

## 🎯 What Works Right Now

✅ Full UI/UX  
✅ IPFS Upload (via Pinata)  
✅ Semantic Analysis  
✅ Similarity Calculations  
✅ Mock Fallback Mode  
⚠️ Story Protocol Registration (needs NFT contract address)  

## 🔑 Missing Piece: Create Your NFT Collection

You need to create your own SPG NFT Collection (one-time setup).

**To get it:**
```bash
cd frontend
npm run create-collection
```

This creates YOUR NFT collection and gives you the contract address. Add it to `.env`:
```bash
NEXT_PUBLIC_NFT_CONTRACT_ADDRESS=0x...
```

See `CREATE-NFT-COLLECTION.md` for detailed instructions.

**Without it:**
- App runs fine
- Falls back to mock mode
- Still shows full demo flow
- Just shows yellow "Mock Mode" badge instead of green "Live Blockchain"

## 📱 Demo Flow

### For Judges/Presentation:

```
"Let me show you semantic IP protection..."

[Navigate to /register]
"Here we have content with full semantic fingerprints - 
 narrative structure, character essence, and themes"

[Click register]
"We're uploading this 2MB semantic JSON to IPFS..."
[Show console: IPFS hash]

"Now registering the IP on Story Protocol blockchain..."
[Show console: transaction]

[Show results]
"The semantic fingerprint is permanently stored and verifiable"
[Click explorer link - if blockchain mode]

[Navigate to /compare]
"Let's detect plagiarism. These images look completely different..."
[Compare original with copycat]

"But look - 91% semantic similarity across all dimensions"
[Show breakdown: Narrative 94%, Character 89%, Thematic 88%]

"This is meaning-level plagiarism that traditional tools miss"
```

## 🐛 Troubleshooting

### Mock Mode Appears
**This is normal!** Hybrid system working as designed.
- Check NFT contract address is set
- Check wallet has testnet funds
- Check network connection

### Can't Start Dev Server
```bash
cd "Story IP Blockchain/frontend"
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Environment Variables Not Loading
- File must be named `.env` or `.env.local`
- Must be in `frontend/` directory
- Restart dev server after changes
- Variables must start with `NEXT_PUBLIC_`

## 📋 Quick Reference

### Commands
```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

### URLs
```bash
# Local
http://localhost:3000

# Pages
http://localhost:3000/register
http://localhost:3000/compare
http://localhost:3000/dispute

# Story Explorer
https://testnet.storyscan.xyz

# Pinata
https://app.pinata.cloud
```

### Console Commands (for debugging)
```javascript
// In browser console while app is running

// Check environment variables
console.log({
  wallet: process.env.NEXT_PUBLIC_WALLET_ADDRESS,
  rpc: process.env.NEXT_PUBLIC_STORY_RPC_URL,
  nft: process.env.NEXT_PUBLIC_NFT_CONTRACT_ADDRESS,
  pinata: !!process.env.NEXT_PUBLIC_PINATA_JWT
});
```

## 💡 Tips

1. **Mock mode is your friend** - Always works for demos
2. **Console is your guide** - Watch for upload/registration logs
3. **Test before demo** - Run through flow at least once
4. **Have backup** - If blockchain fails, mock mode continues
5. **Show the meaning** - Emphasize semantic layers, not just tech

## 🆘 Need Help?

1. Check `/SETUP-GUIDE.md` for detailed instructions
2. Check `/IMPLEMENTATION-SUMMARY.md` for what's implemented
3. Story Protocol docs: https://docs.story.foundation
4. Story Discord: (get invite from docs)

## ✨ Success Looks Like

### With Blockchain (NFT Contract Set):
```
✅ Uploaded to IPFS: QmXXX...
✅ Registered on Story Protocol!
   IP Asset ID: 0xXXX...
   Token ID: 123
   Transaction Hash: 0xXXX...
   
[Green Badge: ✅ Live Blockchain]
[Working explorer links]
```

### Without Blockchain (Mock Mode):
```
⚠️ Blockchain failed, using mock
   
[Yellow Badge: ⚠️ Mock Mode (Demo)]
[Same UI, just fallback data]
```

Both are perfectly fine for demos! The hybrid system ensures you're covered either way.

---

**You're ready to go!** 🚀

Just run `npm run dev` and navigate to `http://localhost:3000`


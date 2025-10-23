# Create Your NFT Collection (One-Time Setup)

## Why You Need This

Story Protocol requires an SPG NFT Collection contract to mint and register IP assets. You create this **once** and use it for all your registrations.

## Quick Steps

### 1. Install tsx (if not already installed)
```bash
cd frontend
npm install
```

### 2. Create Your Collection
```bash
npm run create-collection
```

This will:
- Create an SPG NFT Collection called "Semantic IP Collection" 
- Print the contract address
- Show you the transaction on the blockchain

### 3. Copy the Address
You'll see output like:
```
✅ SPG NFT Collection Created!
   Contract Address: 0xABC123...

📝 ADD THIS TO YOUR .env FILE:

NEXT_PUBLIC_NFT_CONTRACT_ADDRESS=0xABC123...
```

### 4. Add to .env
Copy that address into your `.env` file:
```bash
NEXT_PUBLIC_NFT_CONTRACT_ADDRESS=0xABC123...
```

### 5. Done!
You can now use `/register` to mint NFTs from this collection and register them as IP assets.

## That's It!

You only do this **once**. Then you can register as many semantic IP assets as you want using that collection.

## Troubleshooting

**"Wallet has insufficient funds"**
- Get testnet tokens from Story faucet

**"Cannot read environment variables"**
- Make sure your `.env` file has `NEXT_PUBLIC_WALLET_PRIVATE_KEY` and `NEXT_PUBLIC_WALLET_ADDRESS`

**"Transaction failed"**
- Check you're on Story testnet (aeneid)
- Verify RPC URL: `https://testnet.storyrpc.io`


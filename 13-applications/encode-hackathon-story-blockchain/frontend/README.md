## Semantic IP Protection + Story Protocol (Frontend)

Interactive demo to register “Semantic IP” on the Story Protocol Aeneid testnet. The flow:
- Upload a document (demo uses pre-bundled JSON examples)
- Build a semantic fingerprint (mocked for UI demonstration)
- Upload fingerprint JSON to IPFS via Pinata and generate a QR PNG (also pinned)
- Register an IP Asset on Story Protocol using separate IP and NFT metadata

This is a Next.js App Router app tailored for a hackathon-style POC. Do not use real funds or production keys.

### Tech stack
- Next.js 15, React 19, TypeScript
- Tailwind CSS 4 (via `@tailwindcss/postcss`)
- Story Protocol Core SDK (`@story-protocol/core-sdk`) + `viem`
- IPFS via Pinata (`axios` for HTTP)
- `qrcode` for QR generation, `recharts` for simple charts

## Quick start

1) Install dependencies
```bash
npm install
```

2) Create `.env` in this `frontend` folder (There is an example.env to copy from)
```bash
# Story testnet (Aeneid) — demo only, use a burner key
NEXT_PUBLIC_WALLET_PRIVATE_KEY=0xYOUR_TEST_PRIVATE_KEY
NEXT_PUBLIC_STORY_RPC_URL=https://aeneid.storyrpc.io

# Pinata (required for IPFS uploads)
NEXT_PUBLIC_PINATA_JWT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...  # your Pinata JWT

# Story Protocol NFT contract address to mint against (Aeneid testnet)
NEXT_PUBLIC_NFT_CONTRACT_ADDRESS=0xbAc50238B65bc4F55c3729406e508f9174525d33
```

Notes
- Keys are prefixed with `NEXT_PUBLIC_` and are exposed to the browser. This is intentional for the demo only. Use burner credentials and no real value.
- The app targets the Story Protocol Aeneid testnet (`chainId: 'aeneid'`).

3) Run the dev server
```bash
npm run dev
```

Open http://localhost:3000 and navigate to Register to try the flow.

## Scripts
```json
{
  "dev": "next dev --turbopack",
  "build": "next build --turbopack",
  "start": "next start",
  "create-collection": "tsx scripts/create-nft-collection.ts"
}
```
- `dev`: start local development
- `build`: production build
- `start`: run production server
- `create-collection`: optional script (if provided) to help set up contracts

## Key files
- `app/register/page.tsx`: main registration UI and flow
- `blocklibs/ipfs.ts`: IPFS and Pinata helpers (JSON and PNG uploads)
- `blocklibs/qr.ts`: QR PNG generation
- `blocklibs/StoryProtocol.ts`: Story Protocol client and IP asset registration
- `blocklibs/utils.ts`: explorer/IPFS/IP asset URL helpers

## How it works (high level)
1. Upload or select demo content; show a preview of semantic attributes (mocked for UI)
2. Pin full semantic JSON to IPFS (Pinata)
3. Generate a QR PNG that encodes `ipfs://<semanticCid>` and pin it
4. Build IP metadata and NFT metadata JSON; compute SHA-256 of both
5. Call Story Protocol SDK `mintAndRegisterIpAssetWithPilTerms` with CIDs and hashes
6. If on-chain call fails, the UI falls back to a mock result for demo continuity

## Troubleshooting
- Wallet private key env not set: ensure `NEXT_PUBLIC_WALLET_PRIVATE_KEY` is in `.env.local`
- IPFS upload failed: verify `NEXT_PUBLIC_PINATA_JWT` and that your Pinata account is active
- Story Protocol registration failed: check RPC URL, contract address, and testnet availability
- Asset/Explorer links: the app builds URLs for Aeneid testnet and Pinata gateways

## Security and disclaimers
- Do not use production/private assets or real funds; this demo exposes keys in the browser
- Use a fresh burner account and minimal balances on testnet only

## License
Apache-2.0

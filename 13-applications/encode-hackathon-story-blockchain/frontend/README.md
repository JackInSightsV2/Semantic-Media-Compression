## Semantic IP Protection + Story Protocol (Frontend)

Interactive demo to register "Semantic IP" on the Story Protocol Aeneid testnet. The flow:
- Upload a document (demo uses pre-bundled JSON examples)
- Build a semantic fingerprint via backend API
- Backend uploads fingerprint to IPFS and generates QR code (if needed)
- Backend registers IP Asset on Story Protocol using Python SDK
- Frontend displays registration results

**Note:** Story Protocol registration is now handled entirely by the backend Python SDK. The frontend only calls backend APIs.

This is a Next.js App Router app tailored for a hackathon-style POC. Do not use real funds or production keys.

### Tech stack
- Next.js 15, React 19, TypeScript
- Tailwind CSS 4 (via `@tailwindcss/postcss`)
- Backend API integration (FastAPI)
- IPFS via Pinata (`axios` for HTTP) - for frontend utilities only
- `qrcode` for QR generation (frontend utilities), `recharts` for simple charts

## Quick start

1) Install dependencies
```bash
npm install
```

2) Create `.env` in this `frontend` folder (There is an example.env to copy from)
```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000

# Pinata (optional, for frontend utilities)
NEXT_PUBLIC_PINATA_JWT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...  # your Pinata JWT

# Story Protocol (only needed for utility scripts like create-nft-collection)
# Registration is handled by backend, so these are optional
NEXT_PUBLIC_WALLET_PRIVATE_KEY=0xYOUR_TEST_PRIVATE_KEY  # Only for utility scripts
NEXT_PUBLIC_STORY_RPC_URL=https://aeneid.storyrpc.io
NEXT_PUBLIC_NFT_CONTRACT_ADDRESS=0xbAc50238B65bc4F55c3729406e508f9174525d33
```

Notes
- **Backend handles all Story Protocol registration** via Python SDK
- Frontend only needs `NEXT_PUBLIC_API_URL` to connect to backend
- Story Protocol env vars are only needed for utility scripts (like creating NFT collections)
- Keys are prefixed with `NEXT_PUBLIC_` and are exposed to the browser. Use burner credentials only.

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
- `lib/api.ts`: Backend API client (all registration goes through backend)
- `blocklibs/ipfs.ts`: IPFS and Pinata helpers (for frontend utilities only)
- `blocklibs/qr.ts`: QR PNG generation (for frontend utilities only)
- `blocklibs/StoryProtocol.ts`: **Deprecated** - kept only for utility scripts
- `blocklibs/utils.ts`: explorer/IPFS/IP asset URL helpers

## How it works (high level)
1. User uploads content via frontend
2. Frontend calls backend API: `POST /api/registration/uploads`
3. Backend processes content, builds semantic fingerprint
4. Backend uploads fingerprint to IPFS (encrypted or plaintext based on content type)
5. Backend generates public metadata and uploads to IPFS
6. User chooses: upload cover image OR use auto-generated QR code
7. Frontend calls backend API: `POST /api/registration/register-story` (with optional cover image)
8. **Backend registers on Story Protocol** using Python SDK
9. Backend returns registration results (IP Asset ID, transaction hash, etc.)
10. Frontend displays results

## Troubleshooting
- Backend not running: ensure backend is running on `NEXT_PUBLIC_API_URL` (default: http://127.0.0.1:8000)
- API connection failed: check backend health at `/healthz` endpoint
- Story Protocol registration failed: check backend logs (backend handles all blockchain interactions)
- Asset/Explorer links: the app builds URLs for Aeneid testnet and IPFS gateways

## Security and disclaimers
- Do not use production/private assets or real funds; this demo exposes keys in the browser
- Use a fresh burner account and minimal balances on testnet only

## License
Apache-2.0

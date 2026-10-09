# Semantic IP hackathon frontend — archived demonstration

Reviewed 8 October 2026. This Next.js app demonstrates a proposed semantic-fingerprint registration flow using pre-bundled document fixtures. Uploading a file or URL selects sample data; it does not run a recognition model. Comparison can use synthetic hash-based vectors, so displayed similarity is not a measured semantic-detection score.

## Security status

Browser signing and Pinata uploads are disabled. `blocklibs/StoryProtocol.ts` and the upload exports in `blocklibs/ipfs.ts` now throw clear errors without reading secrets or submitting writes. The collection CLI uses the same disabled Story client. Public IPFS reads remain available.

Never put wallet private keys, Pinata JWTs or API secrets in `NEXT_PUBLIC_*` variables. Previous versions did so; remove old public-secret configuration and treat credentials included in a distributed browser build as exposed. No authenticated server endpoint or wallet-connect signing flow has been implemented. Adding server-only environment variables does not enable writes.

The existing UI can fall back to a simulated registration result with random identifiers after an error. That display is not a blockchain receipt or an IPFS upload. Dispute screens also contain mock results. This remains a historical demo, not an operational protection or infringement-detection service.

## Local inspection

`example.env` contains only optional public configuration. Dependencies are locked but require security maintenance before any deployment. The October 2026 audit does not establish a clean dependency baseline or verify a current production build.

```bash
npm ci
npm run dev
```

These are reproduction instructions; dependency installation and a frontend build were not performed in the implementation audit. Browse the local demo at `http://localhost:3000`. Do not enter confidential assets or real credentials.

## Next work

Implement authenticated, authorized server-side uploads and user-wallet signing (or a carefully scoped server signer), remove simulated success paths, replace fixtures with evaluated recognition and embedding models, upgrade vulnerable dependencies, and add integration tests before re-enabling writes.

See [the implementation audit](../../../12-research-documents/2026-10-08-implementation-review.md) for source evidence and limitations.

## License

Apache-2.0.

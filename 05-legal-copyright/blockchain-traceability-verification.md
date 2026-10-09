# Traceability and verification boundaries

Refreshed 8 October 2026. A proposed ledger can provide tamper-evident records under its network and key-security assumptions. It cannot automatically provide copyright ownership, truth, lawful licensing or immunity from liability.

## Record separately

- Content bytes and hashes: test integrity against a known reference.
- Signatures and keys: establish what a key signed; identity still requires evidence.
- Submission timestamps and chain state: record network events, not necessarily original creation time.
- Licence assertions and documents: record claimed terms, with scope and authority independently checked.
- Disputes and corrections: preserve the difference between an assertion and an adjudicated result.
- Availability: retain and fund accessible copies; a content address alone is not persistence.

A smart contract can execute encoded rules, but cannot infer that the input facts or licence grant are lawful. Token ownership differs from IP ownership. [Official NFT study](https://www.copyright.gov/policy/nft-study/). IPFS data needs retained/pinned copies for continued availability. [IPFS documentation](https://docs.ipfs.tech/concepts/persistence/).

The hackathon application is a historical demo with simulated UI completion and disabled credentialed browser writes. No live on-chain evidence from this audit establishes the proposed provenance system. See [implementation review](../12-research-documents/2026-10-08-implementation-review.md).

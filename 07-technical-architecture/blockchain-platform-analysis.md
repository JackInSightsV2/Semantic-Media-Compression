# Blockchain storage options: requirements before ranking

Refreshed 8 October 2026. The earlier fixed dollar quotes, TPS rankings and Solana recommendation were not based on a reproducible project benchmark. A 10 MB blueprint stored for about $2.50 and an entire lifecycle below $5 are withdrawn as measured claims.

## Distinguish payload and commitment

Store actual bytes in a system with explicit availability and retention guarantees. If a ledger adds value, record a hash, signed rights assertions and references to retained payloads. Compare this with conventional signed records before adding chain dependencies.

Account capacity is not transaction capacity. Solana documents a 10 MiB account-data limit separately from much smaller transaction limits, storage minimum balances and transaction fees. A pseudocode call passing a 10 MB vector in a single transaction is not a working implementation. [Accounts](https://solana.com/docs/core/accounts), [transactions](https://solana.com/docs/core/transactions).

Block cadence is not finality. State the commitment level, confirmation policy, cluster/version and failure model. Token-denominated fees and refundable storage balances are different costs; dollar conversions need a dated exchange rate. [Solana account structure](https://solana.com/docs/core/accounts/account-structure).

IPFS content addresses do not ensure future availability without retained copies. Ethereum gas prices vary. [IPFS persistence](https://docs.ipfs.tech/concepts/persistence/), [Ethereum gas](https://ethereum.org/gas/).

## Required comparison

Measure payload size, chunking and transaction count, write/read success, retrieval latency, deposits, nonrefundable fees, ongoing pinning/storage, availability and finality assumptions. No ledger is selected as the universally cheapest or best platform by this audit.

See [legal/business source review](../12-research-documents/2026-10-08-legal-business-review.md) for the distinction between provenance and legal title.

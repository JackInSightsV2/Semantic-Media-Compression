# Legal, commercial and blockchain claims review

Review date: 2026-10-08. This is a documentation evidence audit, not a legal opinion or a tested commercial forecast. Selected high-impact claims were checked against primary sources; it is not a comprehensive survey of every jurisdiction or court decision. Paths and quoted numbers below identify the pre-refresh source material.

## Findings requiring correction

| Priority | Repository source | Finding | Required treatment |
|---|---|---|---|
| High | `05-legal-copyright/semantic-plagiarism-detection.md`, especially “Enforceable Copyright Protection” | The 95% threshold purports to shift a legal burden; the introduction claims protection for the same ideas and concepts. No cited law establishes these numerical thresholds. | Remove the legal standard. Label scores as unvalidated retrieval/triage signals; evaluate false positives on shared tropes, public-domain material and independent creation. Never automatically equate a score with infringement. |
| High | `05-legal-copyright/blockchain-traceability-verification.md`; corresponding summary in `legal-framework-analysis.md` | Cryptographic records are described as indisputable ownership proof, automatic enforcement, liability protection and a route to legal compliance. | A ledger can preserve submitted assertions and changes. It cannot establish that the submitter owned the underlying rights, that the licence covers a particular act, or that an output is lawful. Separate identity, chain of title, licence scope, provenance and adjudication. |
| High | `05-legal-copyright/quantified-risk-matrices.md` | Unsupported 75% infringement probabilities, percentage-point mitigation adjustments and 0% public-domain risk are presented as data-driven estimates. | Withdraw empirical interpretation. Use qualitative risks, or explicitly hypothetical inputs with no predictive validity; require a dataset, denominator, jurisdiction and estimation method before quantitative claims. |
| High | `05-legal-copyright/legal-framework-analysis.md`; `untested-legal-territory.md` | “6.2%” precedent coverage with “±4.8” confidence appears without an auditable sampling frame. Existing law is described too broadly as a legal vacuum. | Remove numeric authority unless reproducible research is supplied. Explain that existing rights and exceptions apply, while particular applications remain contested. |
| High | `07-technical-architecture/blockchain-platform-analysis.md` | Solana 10 MB storage at about $2.50 and a lifecycle below $5 are asserted without a cluster quote or working implementation. A 10 MB vector is passed in one illustrative transaction. | Treat as nonfunctional conceptual pseudocode. Account capacity is not transaction capacity. Use chunking and measured deposits/fees if implemented; prefer off-chain payloads with optional hashes pending requirements. |
| Medium | Same blockchain platform file | “400ms block times” is treated as finality; TPS and fixed dollar fees support a primary platform recommendation without workload measurements. | Specify commitment, finality, transaction type, congestion, failed transactions and token exchange rate. Withdraw ranking until like-for-like measured. |
| Medium | `06-business-applications/economic-stress-testing.md` | Despite an existing theoretical disclaimer, the body calls unsupported prices “Current costs”, gives $40–100B accessible markets, fictional survey responses and explicit scenario probabilities. | Keep only as labelled assumptions, not observations. Replace “current” with a dated quoted model/SKU, or “illustrative”. Survey percentages need provenance or an explicit fictional label at point of use. |
| Medium | `06-business-applications/economic-validation-analysis.md` | 3.2x cost ratio is labelled ROI; energy savings of 90–99% are assumed from smaller transferred/stored payloads. | Distinguish cost ratio, net saving and investment return. Include extraction, generation, retries, hardware utilisation, storage lifecycle and human review before energy/cost comparisons. |
| Medium | `05-legal-copyright/legal-framework-analysis.md` | Templates are “ready-to-implement”; blanket pre-1928 public-domain guidance is stale and underspecified. | Treat templates as draft discussion aids. Check rights per work, edition, recording, territory and use; avoid a single year rule for all media. |

The economic overview and several economic analyses already carry theoretical disclaimers. The problem is inconsistent wording within them, not absence of all qualification. No supporting market study, user survey, live storage benchmark or validated probability model was identified in the reviewed material.

## Primary-source refresh

### Copyright scope and AI authorship

US copyright protects original expression, not underlying ideas, methods or concepts. Thus thematic or narrative similarity alone cannot constitute a numerical legal infringement test. Conversely, changing format or using a semantic intermediate does not establish permission to reproduce protected expression. See the [US Copyright Office explanation](https://www.copyright.gov/what-is-copyright/) and [17 USC chapter 1](https://www.copyright.gov/title17/92chap1.html).

The US Copyright Office’s January 2025 Part 2 report says sufficient human control of expressive elements can support copyright; prompts alone do not establish it. Human-authored selection, arrangement or modification may qualify. This addresses output copyrightability, not automatic clearance of source material or training. See [official Part 2 announcement](https://www.copyright.gov/newsnet/2025/1060.html).

The UK government published its copyright/AI report on 18 March 2026. It withdrew preference for a broad training exception with opt-out and proposed further evidence gathering. The report also discusses UK computer-generated works, illustrating why US authorship conclusions cannot simply be treated as worldwide rules. It is a policy report, not itself a newly enacted permission for semantic compression. See [official report](https://www.gov.uk/government/publications/report-and-impact-assessment-on-copyright-and-artificial-intelligence/report-on-copyright-and-artificial-intelligence). No subsequent legal change is asserted by this limited review.

### Provenance is not title

The joint USPTO/USCO NFT report describes confusion between token ownership and IP rights, and limitations of blockchain records as substitutes for copyright registration and transfer formalities. This directly undermines the repo’s guaranteed ownership/compliance language. See [official study](https://www.copyright.gov/policy/nft-study/) and [full report](https://www.copyright.gov/policy/nft-study/Joint-USPTO-USCO-Report-on-NFTs-and-Intellectual-Property.pdf).

Recommended architecture language: “A registry records signed rights assertions and licence references with tamper-evident history. Rights verification depends on external evidence and applicable law. Similarity analysis may prioritize human review.” This is an audit recommendation, not a claim that the repo implements that registry.

### Storage and chain costs

Solana’s current documentation distinguishes the 10 MiB account-data limit from transaction-size limits (1,232 bytes for legacy/v0; its current docs also describe a 4,096-byte v1 format). Neither allows a 10 MB vector in one transaction. Account storage requires a refundable minimum balance proportional to size, separate from transaction fees. A dollar quote needs cluster/version, byte count, quote time and exchange rate. See [accounts](https://solana.com/docs/core/accounts), [account structure](https://solana.com/docs/core/accounts/account-structure) and [transactions](https://solana.com/docs/core/transactions). This review did not submit a chain transaction or validate v1 activation on any cluster.

IPFS content addressing does not guarantee continued availability; pinning and retained copies require operational responsibility and costs. See [IPFS persistence documentation](https://docs.ipfs.tech/concepts/persistence/). Ethereum network fees vary with congestion, so historical dollar costs cannot serve as fixed operating guarantees. See [official gas explanation](https://ethereum.org/gas/).

## Evidence needed before reinstating claims

1. Each benchmark fixture records source licence or ownership basis, permitted evaluation use, and redistribution restrictions separately from its content hash.
2. Legal similarity experiments measure precision/recall with reviewed labels; no automated takedowns or burden-shifting claims derive from a numerical score.
3. Business experiments report total dollars per accepted output, quality threshold, retries, human review time and actual baseline costs. A compact intermediate alone is not demonstrated economic advantage.
4. Storage experiments report payload bytes, cluster/protocol version, transactions, storage deposit, paid fees, retrieval availability and measured latency. Blockchain is optional until its benefit over signed conventional records is tested.
5. Model/dataset licences, inference processing, generation and downstream distribution are assessed separately. “Company-owned” and “university-owned” must be verified for each corpus rather than assumed.

Research method: JEV scans selected candidate files; targeted source reads established the findings. Agent Reach’s Exa CLI was unavailable, so primary sources were checked through browser search and its documented Jina web reader. No credentials or paid model APIs were used.

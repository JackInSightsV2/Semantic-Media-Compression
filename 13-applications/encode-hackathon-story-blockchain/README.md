# Semantic Copyright Guardian — historical hackathon demo

<!--
Copyright 2024-2025 Stephen Henry JackInSightsV2

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Author: Stephen Henry JackInSightsV2
Fingerprint: SH:JI2:5d8f1a4c7e0b3d6f9a2c5e8b1d4f7a0
-->

Audit refresh: 8 October 2026. This directory is a demonstration of semantic comparison and proposed Story Protocol workflows, not a validated copyright-detection product.

## Current status

- The quick-scan flow selects prepared fixture data and simulates progress; it is not live semantic analysis of an arbitrary upload or URL.
- Similarity code and demo comparisons do not establish copying, infringement or ownership.
- Registration and dispute UI paths can return simulated identifiers. A success screen is not evidence of a confirmed on-chain transaction.
- Browser-side helpers previously referenced `NEXT_PUBLIC_WALLET_PRIVATE_KEY` and `NEXT_PUBLIC_PINATA_JWT`. This audit removes credentialed client writes and makes those helper operations fail closed pending a secure integration. Do not put secrets in any `NEXT_PUBLIC_*` variable.
- The dependency audit found unresolved advisories. This demo is not approved for production deployment by this audit. See [the implementation review](../../12-research-documents/2026-10-08-implementation-review.md) and [repository audit](../../AUDIT.md).

## Local historical demo

Source is under `frontend/`. Dependency versions, service APIs and setup notes require review before installation or deployment. Public fixture browsing is separate from authenticated blockchain or storage operations. A server-side integration or user-controlled wallet flow must be designed and tested before real writes are restored.

The earlier setup command using `Story IP Blockchain/frontend` named a directory that does not exist in this checkout. From this directory, the actual frontend path is `frontend`.

## Research boundaries

A cryptographic commitment can support checking whether bytes changed. It cannot establish the truth of the content, the lawful owner, creation history before registration or infringement. Common ideas and similarity scores require contextual assessment; they are not mathematical proof of plagiarism. Refer to the [legal review](../../12-research-documents/2026-10-08-legal-business-review.md).

The maintained runnable compression experiments are elsewhere: [model harness](../../11-validation-tests/model_harness/README.md).

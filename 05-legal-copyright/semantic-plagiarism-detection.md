# Semantic similarity as a review tool

Refreshed 8 October 2026. Earlier claims that numerical similarity establishes plagiarism, proves infringement or shifts the burden of proof are withdrawn. The repository has no validated legal classifier.

## What a comparison system could do

A model can rank candidate similarities, expose aligned passages or narrative elements and help a reviewer inspect evidence. It should distinguish shared topics, standard methods, stock tropes, authorised reuse, independent creation and potentially copied expression. Scores require a labelled dataset and false-positive/false-negative analysis.

US copyright does not protect ideas and concepts as such. Similarity to an idea is not sufficient to establish infringement, and a transformed output is not automatically non-infringing. Legal standards depend on jurisdiction and facts. [US Copyright Office](https://www.copyright.gov/what-is-copyright/).

## Proposed output

A useful report records source identifiers, evidence excerpts, model/configuration version, comparison method, uncertainty, limitations and reviewer disposition. Avoid fields such as `legal_admissible: true` or `plagiarism_detected: score > 0.85`; neither is established by a model score.

Blockchain timestamps may help establish when a commitment was submitted, under the system's assumptions. They cannot establish original authorship, truth, prior creation time or title by themselves. [USPTO/USCO NFT study](https://www.copyright.gov/policy/nft-study/).

## Validation gate

Before deploying a review assistant, evaluate rights-cleared labelled examples with independent expert review. Measure false accusations, ambiguity, bias, missed similarities and reviewer workload. Keep legal action separate from automated similarity ranking. No benchmark in the current repository has passed that gate.

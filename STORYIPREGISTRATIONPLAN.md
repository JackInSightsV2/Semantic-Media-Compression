## Story IP Registration Plan

### Goals
- Demonstrate ABV.dev–native Story Protocol registration for hackathon compliance.
- Preserve the existing encode backend Story pipeline while showing added dispute value.
- Provide a deterministic duplicate scenario to highlight semantic similarity enforcement.

### Registration Strategy
- **Primary (Hackathon-compliant):** Final semantic artifact (distilled JSON, reinflated narrative, or chosen canonical output) is sent to ABV via `abv.trace`/`abv.ip.register` with `register_on_story` metadata enabled; ABV auto-mints on Story.
- **Secondary (Encode backend mirror):** Optionally send the same artifact through the legacy encode backend Story flow to maintain continuity for the broader app.
- **Artifact choice:** Prefer the distilled semantic JSON because it is compact, stable, and carries your semantic fingerprint; alternatively, register prompts or reinflated narratives when needed.

### Trace Instrumentation
- Emit ABV traces for each major pipeline stage (`distillation_pass_n`, `reinflation`, `comparison`, etc.) for provenance.
- Only the final trace needs the IP registration flag; earlier traces provide transparency and auditability.
- Include metadata fields: content hash, IPFS URI (if available), artifact type (e.g., `semantic_blueprint`), pipeline version.

### Duplicate & Dispute Demonstration
- Register the canonical artifact via ABV and mirror it once through the encode backend to create two identical Story assets.
- Use the `_pipeline_testing` similarity workflow to scan Story assets; identical semantic JSON should produce a 100 % match.
- Trigger the dispute/escalation logic on the duplicate registration to showcase enforcement (log capture, UI badge, or alert).
- Clearly communicate to judges that ABV’s registration is the authoritative record; the duplicate exists solely to demonstrate dispute handling.

### Operational Notes
- Maintain a toggle (env flag or CLI arg) to switch between “ABV registration mode” and “encode backend mode,” enabling hybrid deployments.
- Capture evidence for submission: ABV trace logs/screenshots, Story asset IDs, similarity report highlighting the 100 % match, and dispute workflow output.
- Future-friendly path: keep both registration routes but prioritize ABV for any hackathon or production scenario requiring official Story compliance.

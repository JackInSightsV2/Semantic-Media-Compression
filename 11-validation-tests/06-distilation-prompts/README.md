## Distillation Prompt Library

This directory contains **media-specific semantic distillation prompts** used for validation, benchmarking, and future automation.

- **Goal**: Move from generic "semantic summary" prompts to **precisely scoped distillation templates** tuned to each media type and subtype.
- **Structure**:
  - `text/` – Detailed prompt templates for different text genres and use-cases
  - `audio/` – Initial prompts focused on speech and sound semantics
  - `video/` – Initial prompts focused on visual and temporal semantics

Each prompt file is written as **LLM-ready templates** that can be copy-pasted directly into tests or wired into programmatic calls.



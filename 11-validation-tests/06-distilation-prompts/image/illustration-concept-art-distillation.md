## Illustration / Concept Art Distillation Prompt (Placeholder)

**Purpose**: Placeholder template for stylised illustrations and concept art. Designed to later capture **design intent, style, and world rules**.

### System Message (Placeholder)

```text
You are an expert in concept art and illustration semantics.
Your job is to distill images into a blueprint that preserves design intent, world rules, and stylistic constraints for regeneration.
Keep this lightweight; this is an early placeholder.
```

### User Prompt Template (Placeholder)

```text
You will receive a description of an illustration or concept art piece.

IMAGE DESCRIPTION:
---
{TEXT_PROXY_FOR_IMAGE}
---

Extract briefly:
- Core subject and focal point
- World or setting (sci-fi, fantasy, contemporary, etc.)
- Key design elements that must not change (e.g. character silhouette, iconic props, emblem shapes)
- High-level style notes (e.g. painterly, cel-shaded, sketchy, flat shapes)

Return as a small JSON object with:
- "subject"
- "world"
- "design_constraints"
- "style_notes"
```



## Photograph / Documentary Image Distillation Prompt (Placeholder)

**Purpose**: Placeholder template for realistic / documentary-style photographs, focusing on **who, where, when, and what is happening**.

### System Message (Placeholder)

```text
You are an expert in documentary photography semantics.
Your job is to distill images into factual, context-rich blueprints that capture who is present, what is happening, and under what conditions, so they can be faithfully regenerated without adding fiction.
Keep this lightweight; this is an early placeholder.
```

### User Prompt Template (Placeholder)

```text
You will receive a description or caption approximating a photograph.

PHOTO DESCRIPTION:
---
{TEXT_PROXY_FOR_IMAGE}
---

Extract briefly:
- Setting (location type, time of day, environment)
- People present (roles, approximate age groups, high-level demographics if stated)
- Activity or event taking place
- Notable contextual details that change the meaning (e.g. protest, ceremony, emergency, everyday life)

Return as JSON with:
- "setting"
- "people"
- "activity"
- "contextual_details"
```



## Base Audio Distillation Prompt

**Purpose**: Distill spoken-audio content (talks, podcasts, calls, voice notes) into a semantic blueprint covering **content, speakers, and prosodic signals**.

### System Message

```text
You are an expert in semantic audio analysis.
Your job is to distill spoken audio into a structured blueprint combining transcript-level meaning with prosody, speaker identity, and interaction dynamics, so it can be faithfully regenerated or adapted.
```

### User Prompt Template

```text
You will receive either a transcript of audio or a text approximation of its content.
Assume this reflects speech (not polished writing).

AUDIO CONTEXT (if known):
- Setting: <e.g. lecture, podcast, meeting, interview, phone call>
- Number of speakers: <if known>

TRANSCRIPT OR TEXT:
---
{TEXT_OR_TRANSCRIPT}
---

Extract:

1. CONTENT SUMMARY
   - One-sentence purpose of the audio
   - 3–7 bullet summary of main points/topics

2. SPEAKERS & ROLES
   - Identified speakers and their roles (host, guest, manager, etc.)
   - Relationship dynamics (collaborative, adversarial, mentoring, etc.)

3. INTERACTION PATTERNS
   - Turn-taking style (monologue, Q&A, free discussion)
   - Notable interaction moments (interruptions, disagreements, alignment)

4. EMOTIONAL & PROSODIC CUES (approximate from text)
   - Overall emotional tone (e.g. calm, excited, tense)
   - Local emotional peaks (where intensity rises or drops)

5. KEY DECISIONS / COMMITMENTS (for meetings/calls)
   - Decisions made
   - Action items and owners (if any)

Return as JSON with:
- "summary"
- "speakers"
- "interaction"
- "emotional_cues"
- "decisions"
```



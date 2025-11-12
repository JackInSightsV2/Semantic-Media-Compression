### 1. Semantic Encoding for Your Own Content

Goal: create a **canonical semantic fingerprint** for each work you publish to the Story chain, using the same pipeline that you’ll apply to external sources.

#### Step 1 – Ingest

Accept and store any of these input types:

* Text (scripts, lyrics, descriptions)
* Image (artwork, frames, covers)
* Audio (music, narration, sound design)
* Video (films, clips, animation)

Each item gets a unique ID and a manifest linking the original file and all derivative data.

#### Step 2 – Normalize and Pre-process

| Type  | Action                                             | Output                  |
| ----- | -------------------------------------------------- | ----------------------- |
| Text  | Strip markup, detect language, segment sentences   | clean plain text        |
| Image | Resize to model spec, center-crop, normalize       | RGB tensor              |
| Audio | Convert to mono 16 kHz WAV                         | normalized waveform     |
| Video | Sample keyframes every N seconds and extract audio | frame set + audio track |

#### Step 3 – Semantic Feature Extraction

Use the **exact same models** you will later use for external media.

| Domain     | Model / Tool                                             | Output Field                                  |
| ---------- | -------------------------------------------------------- | --------------------------------------------- |
| Linguistic | embedding model (`text-embedding-3-large` or equivalent) | `text_semantics.entities`, `themes`, `tone`   |
| Visual     | CLIP / BLIP                                              | `visual_semantics.objects`, `style`, `scene`  |
| Audio      | Whisper + audio-embedding                                | `audio_semantics.transcript`, `mood`, `tempo` |
| Metadata   | Manual / auto                                            | `metadata`                                    |
| Fusion     | weighted vector mean of all modality embeddings          | `embedding`                                   |

Canonical JSON (stored off-chain, hashed on-chain):

```json
{
  "id": "uuid",
  "creator": "Jack",
  "text_semantics": {"entities":["forest"],"themes":["growth"],"tone":"serene"},
  "visual_semantics": {"objects":["trees","mist"],"style":"painterly"},
  "audio_semantics": {"mood":"calm","tempo":72},
  "metadata": {"timestamp":"2025-11-12T12:00Z","tags":["fantasy","dreamscape"]},
  "embedding":[0.143,0.527,...]
}
```

Hash this JSON → record `{hash, creator, uri}` on Story.
Store the full JSON and original file in IPFS or cloud storage.
Maintain a local vector index keyed by the on-chain hash for similarity search.

---

### 2. External Platform Fetching

You only pull **metadata and textual fields** that allow the same semantic extraction; you do not process all media.

#### YouTube Data API v3

**Endpoints and Fields**

1. `search.list` → query by `q=<keyword>` (derived from your own content’s entities + themes)

   * Keep: `videoId`, `title`, `description`, `publishedAt`
2. `videos.list?id=<id>&part=snippet,contentDetails`

   * Keep: `snippet.title`, `snippet.description`, `snippet.tags`
3. `captions.download` (if available)

   * Keep: full caption text (critical semantic input)
4. `commentThreads.list?videoId=<id>`

   * Keep: top comments text

Combine all text fields into one string → send to your semantic extraction pipeline.
Resulting JSON has the same structure as your own content’s JSON.

#### Instagram Graph API

**Endpoints and Fields**

1. `/me/media?fields=id,caption,media_url,media_type,timestamp`

   * Keep: `caption` text, `media_url`
2. `/{media-id}/comments`

   * Keep: comment text
3. `/ig_hashtag_search?q=<keyword>` + `/v12.0/{hashtag-id}/recent_media`

   * Keep: captions for each post matching your keywords

Only download `media_url` if the caption filter passes a lexical similarity test to your content.

#### TikTok Research API

**Endpoints and Fields**

1. `/research/video/query/?keyword=<keyword>`

   * Keep: `video_id`, `desc`, `create_time`
2. `/research/comment/query/?video_id=<id>`

   * Keep: comment text

Use captions and comments for semantic extraction.
Fetch the actual video file only if textual similarity to one of your works exceeds threshold T.

---

### 3. Cost-Aware Comparison Workflow

1. For each on-chain Story item:

   * Generate a keyword / hashtag list from its semantic JSON (`entities`, `themes`).
2. Query each API weekly using those terms.
3. Collect returned text metadata.
4. Run **fast lexical pre-filter** (token overlap > X %) to drop irrelevant posts.
5. Pass remaining items through your semantic extraction to produce comparable JSONs.
6. Compute cosine similarity between `embedding`s.
7. If similarity ≥ threshold → record “potential semantic match” event and store `{platform, url, score}`.

---

### 4. Key Implementation Rules

* One unified extraction stack for both owned and fetched content.
* Identical normalization and embedding dimension.
* Only fetch and process public data allowed by each API’s TOS.
* Store minimal external data (text, hash, score) to stay compliant.
* Run scans periodically, not continuously, to control cost.

This gives you an economically realistic, fully symmetric system:
**same pipeline in → same semantic JSON out → direct, cost-bounded comparison.**

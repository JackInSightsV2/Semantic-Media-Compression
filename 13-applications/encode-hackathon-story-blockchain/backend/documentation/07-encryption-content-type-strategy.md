# Encryption and Content Type Strategy

## Overview

The system now implements a content-type-aware encryption strategy that balances privacy needs with Story Protocol compatibility. Encryption is only used when it makes sense for the content type and user preference.

## Design Principles

### When Encryption Makes Sense

Encryption is automatically enabled for content types where hiding the content is important:

- **Text**: Books, scripts, documents, lyrics
- **Video**: Movies, TV shows, films
- **Audio**: Audiobooks, narration (when user requests it)

### When Encryption Doesn't Make Sense

Encryption is typically disabled for content meant to be consumed:

- **Images**: Art is meant to be viewed
- **Music**: Songs are meant to be listened to

## Architecture: Hybrid Approach

The system uses a **two-tier IPFS storage** approach:

### 1. Public Metadata (Always Readable)

Stored separately on IPFS, always in plaintext. Contains:

```json
{
  "title": "Asset Title",
  "asset_type": "text",
  "creator": "Creator Name",
  "created_at": "2024-01-01T00:00:00Z",
  "tags": ["tag1", "tag2"],
  "canonical_hash": "hash_of_full_fingerprint",
  "fingerprint_cid": "ipfs_cid_of_fingerprint",
  "fingerprint_hash": "hash_of_fingerprint",
  "encryption_mode": "encrypted|plaintext",
  "summary": "Brief summary",
  "themes": ["theme1", "theme2"],
  "keywords": ["keyword1", "keyword2"]
}
```

**Purpose**: Story Protocol can read this to:
- Verify ownership
- Track derivatives
- Enable licensing
- Display basic information

### 2. Semantic Fingerprint (Conditionally Encrypted)

The full semantic fingerprint is stored separately:

- **Plaintext**: For images, music, or when user opts out
- **Encrypted**: For text, video, audiobooks (when user requests)

**Purpose**: Contains the complete semantic analysis (themes, narrative structure, embeddings, etc.)

## Implementation Details

### Content Type Detection

The `_should_encrypt()` method determines encryption based on:

1. **User Preference**: If user explicitly disables encryption, it's disabled
2. **Content Type**:
   - `TEXT` → Always encrypt (if user wants)
   - `VIDEO` → Always encrypt (if user wants)
   - `AUDIO` → Respect user preference (could be music or audiobook)
   - `IMAGE` → Never encrypt (art is meant to be viewed)

### Storage Flow

```
1. Process content → Generate semantic fingerprint
2. Determine encryption need → _should_encrypt()
3. Store fingerprint → IPFS (encrypted or plaintext)
4. Create public metadata → Include fingerprint reference
5. Store public metadata → IPFS (always plaintext)
6. Register on Story Protocol → Use public metadata CID
```

### Story Protocol Integration

Story Protocol receives:

- **IP Metadata URI**: Points to public metadata (readable)
- **IP Metadata Hash**: Hash of public metadata (for verification)

This allows Story Protocol to:
- ✅ Read basic asset information
- ✅ Verify authenticity via hash
- ✅ Track derivative relationships
- ✅ Enable licensing based on public metadata
- ✅ Display asset information in UIs

## Benefits

### Privacy Protection

- Sensitive content (books, scripts, movies) can be encrypted
- Full semantic fingerprint hidden from unauthorized access
- Encryption keys stored separately (not on-chain)

### Story Protocol Compatibility

- Public metadata always readable by Story Protocol
- Enables full derivative tracking
- Supports licensing and dispute resolution
- Maintains verifiability via cryptographic hashes

### Flexibility

- User can override automatic encryption decisions
- Content creators choose privacy level
- System adapts to content type automatically

## Data Structure

### Semantic Fingerprint Payload

```json
{
  "canonical": { /* full semantic signature */ },
  "canonical_hash": "hash",
  "encryption_mode": "encrypted|plaintext",
  "fingerprint_cid": "ipfs_cid_of_fingerprint",
  "public_metadata_cid": "ipfs_cid_of_public_metadata",
  "public_metadata_hash": "hash_of_public_metadata",
  "zk_proof": "hash_of_fingerprint",
  "ipfs_cid": "public_metadata_cid (backward compat)",
  "encryption": {
    "key_digest": "hash_of_key",
    "nonce": "encryption_nonce"
  }
}
```

## Usage Examples

### Text Document (Encrypted)

```python
# User uploads a book manuscript
asset_type = "text"
encrypt = True  # User wants encryption

# Result:
# - Fingerprint: Encrypted on IPFS
# - Public Metadata: Plaintext on IPFS
# - Story Protocol: Can read metadata, verify ownership
# - Content: Protected from unauthorized access
```

### Artwork (Plaintext)

```python
# User uploads artwork
asset_type = "image"
encrypt = True  # User preference, but system overrides

# Result:
# - Fingerprint: Plaintext on IPFS (art is meant to be viewed)
# - Public Metadata: Plaintext on IPFS
# - Story Protocol: Can read everything
# - Content: Accessible for viewing
```

### Music Track (Plaintext)

```python
# User uploads music
asset_type = "audio"
encrypt = False  # Music is meant to be heard

# Result:
# - Fingerprint: Plaintext on IPFS
# - Public Metadata: Plaintext on IPFS
# - Story Protocol: Can read everything
# - Content: Accessible for listening
```

## Security Considerations

1. **Encryption Keys**: Stored separately, never on-chain
2. **Public Metadata**: Contains only safe-to-expose information
3. **Hash Verification**: Both public metadata and fingerprint have verifiable hashes
4. **Zero-Knowledge**: Original content never stored on-chain, only hashes

## Future Enhancements

1. **Audio Subtype Detection**: Distinguish between music and audiobooks
2. **Selective Encryption**: Encrypt only sensitive parts of fingerprint
3. **Access Control**: Fine-grained permissions for fingerprint access
4. **Key Management**: Enterprise key management integration


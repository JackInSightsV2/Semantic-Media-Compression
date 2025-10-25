# Semantic Copyright Guardian

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

A demonstration project showcasing how Story Protocol blockchain can protect semantic intellectual property through mathematical fingerprinting and on-chain dispute resolution.

## 🎯 Project Overview

This project demonstrates a novel approach to copyright protection: instead of matching pixels or text, we detect **semantic plagiarism** - when someone steals your _meaning_ and concepts, not just your exact words or images.

### Key Features

- **Multi-layer Semantic Fingerprints**: Captures narrative structure, character essence, and thematic content
- **Story Protocol Integration**: Immutable IP registration on blockchain
- **Mathematical Similarity Detection**: Cosine similarity across semantic dimensions
- **On-chain Dispute Filing**: Cryptographic proof for plagiarism claims
- **Beautiful UI**: Polished interface showcasing the vision

## 🏗️ Architecture

### Mock Semantics Approach (Hackathon)
For this demo, semantic extraction is **mocked** using hand-crafted JSON files. This protects the proprietary research while demonstrating the concept and Story Protocol integration.

**What's Real:**
- ✅ Story Protocol blockchain integration (coming soon)
- ✅ IPFS storage (coming soon)
- ✅ Similarity calculation algorithms
- ✅ Beautiful UI and user experience

**What's Mocked:**
- 🔨 Semantic extraction (hand-crafted JSON files)
- 🔨 AI model integration (to be implemented)

## 📁 Project Structure

```
Story IP Blockchain/
├── demo-data/              # Hand-crafted semantic JSONs
│   ├── original-1-semantic.json
│   ├── copycat-1-semantic.json
│   └── ...
├── frontend/               # Next.js application
│   ├── app/
│   │   ├── page.tsx       # Dashboard
│   │   ├── register/      # IP registration
│   │   ├── compare/       # Plagiarism detection
│   │   └── dispute/       # Dispute filing
│   └── components/
│       ├── SemanticDisplay.tsx
│       └── SimilarityScore.tsx
└── backend/                # Node.js/Express (coming soon)
    └── src/
        └── services/
            ├── storyProtocol.ts
            ├── ipfs.ts
            └── similarity.ts
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm
- (Optional) Story Protocol testnet wallet

### Installation

```bash
# Navigate to frontend directory
cd "Story IP Blockchain/frontend"

# Install dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the demo.

## 🎨 Features Walkthrough

### 1. Register Semantic IP
- Select demo content
- Preview 3-layer semantic fingerprint (Narrative, Character, Themes)
- Register on Story Protocol blockchain (mocked for now)
- Receive IP Asset ID and IPFS hash

### 2. Detect Plagiarism
- Compare original vs suspected copycat content
- View side-by-side semantic analysis
- Calculate similarity across dimensions:
  - Narrative Structure (40% weight)
  - Character Essence (40% weight)
  - Thematic Content (20% weight)
- See matching elements highlighted

### 3. File Dispute
- Select registered IP assets
- Review evidence package
- Submit dispute to Story Protocol (mocked for now)
- Receive dispute ID and transaction proof

## 🔬 Semantic Fingerprint Structure

Each piece of content is analyzed across 3 dimensions:

```json
{
  "narrative": {
    "genre": "psychological thriller",
    "story_arc": "individual confronting moral crisis",
    "themes": ["choice and consequence", "identity under pressure"],
    "dramatic_progression": "contemplation → crisis → resolution"
  },
  "characters": {
    "protagonist": {
      "archetype": "reluctant hero",
      "traits": ["analytical", "conflicted", "determined"],
      "arc": "isolated → forced to engage → transformed"
    }
  },
  "themes": {
    "primary": "consequences of choice",
    "secondary": ["isolation vs connection", "duty vs desire"],
    "emotional_tone": "tense contemplation building to resolve",
    "visual_metaphors": ["crossroads", "heights suggesting risk"]
  }
}
```

Mathematical embeddings enable precise similarity calculation.

## 📊 Similarity Detection

### Algorithm
- Cosine similarity on semantic embedding vectors
- Multi-dimensional weighted scoring
- Thresholds:
  - **> 85%**: HIGH plagiarism risk
  - **70-85%**: MODERATE similarity
  - **< 70%**: LOW similarity

### Example Results
Original vs Copycat 1:
- Narrative: 94% similar
- Character: 89% similar  
- Thematic: 88% similar
- **Overall: 91% - HIGH PLAGIARISM DETECTED** ⚠️

## 🌟 Why Story Protocol?

Story Protocol provides the perfect infrastructure for semantic IP:

1. **Immutable Registration**: Cryptographic proof of ownership
2. **Dispute Resolution**: On-chain evidence and adjudication
3. **IPFS Integration**: Decentralized storage for semantic fingerprints
4. **Transparency**: Public, verifiable IP ownership

## 🔮 Future Roadmap

### Phase 1: Current Demo (Hackathon)
- ✅ Mock semantic analysis
- ✅ Beautiful UI
- 🔜 Story Protocol integration
- 🔜 IPFS storage

### Phase 2: Real Semantic Extraction
- Advanced AI model integration
- Proprietary semantic analysis algorithms
- Multi-layer temporal synchronization
- Production-quality extraction

### Phase 3: Automated Monitoring
- Real-time plagiarism scanning
- Cross-platform detection
- Automated dispute filing
- Legal evidence generation

## 🎓 Research Foundation

This project is based on extensive research in semantic compression and meaning extraction. The full research is proprietary, but demonstrates:

- Multi-layer semantic analysis frameworks
- Vector-based meaning representation
- Cultural adaptation through mathematics
- Temporal synchronization for media

## 🏆 Built for Encode Hackathon

**Category**: IP Enforcement  
**Focus**: Story Protocol blockchain integration  
**Goal**: Demonstrate semantic copyright protection concept

## 📝 License

This is a demonstration project. Semantic extraction methodology is proprietary.

## 🤝 Acknowledgments

- Story Protocol for blockchain IP infrastructure
- Encode Hackathon for the opportunity
- Semantic compression research community

---

**Note**: This is a proof-of-concept demonstration. Semantic extraction is mocked for IP protection. The vision is real, the implementation is in progress.


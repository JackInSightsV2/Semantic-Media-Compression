# Dashboard & Library Design Document

## 1. Conceptual Overview

The **Dashboard** and **Library** are the two primary internal spaces for a logged-in creator on Semantical.Ink.

*   **The Dashboard ("The Cockpit")**: Focuses on *time* (what happened recently, what needs attention) and *status* (credits, earnings). It is the landing point for returning users.
*   **The Library ("The Vault")**: Focuses on *assets* (your blueprints, derivatives, uploads). It is where organization, management, and deep-diving into content genealogy happens.
*   **The Marketplace ("The Gallery")**: A public feed of blueprints where creators can discover, license, and remix existing IP.

---

## 2. The Dashboard
**Goal**: Provide an at-a-glance view of the user's creative ecosystem and quick entry points to key tasks.

### Core Widgets

1.  **User Status Card**
    *   **Greeting**: "Welcome back, [Name]"
    *   **Credit Balance**: "150 Credits available" (CTA: "Buy More")
    *   **Tier**: "Pro Creator"

2.  **Quick Actions (Fab / Row)**
    *   **"New Blueprint"**: Links to `/produce` (Upload flow).
    *   **"Scan for Infringement"**: Triggers a semantic search across the internet/database for unlicensed usage of your IP.
    *   **"Register IP"**: Quick link to Story Protocol registration for existing drafts.
    *   **"Update Contract"**: Modify licensing terms (e.g., change royalty %, allow/disallow AI training) for existing assets.

3.  **Recent Activity Feed**
    *   *Format*: Timeline or list.
    *   *Events*:
        *   "Analysis completed for 'Project X'" (System)
        *   "Your blueprint 'Space Opera' was purchased by @User123" (Commerce)
        *   "New derivative created from 'Project X': 'Anime Script'" (Genealogy)
        *   "Story Protocol registration confirmed (Tx: 0x123...)" (Blockchain)
        *   "Potential infringement detected: 85% match found on YouTube" (Protection)

4.  **Analytics Snapshot** (Mini-Charts)
    *   **IP Reach**: Number of derivatives created from your work.
    *   **Earnings**: Revenue from marketplace sales (if applicable).
    *   **Storage**: Space used by assets.

### User Flow
1.  User logs in.
2.  Sees "Potential infringement detected" alert.
3.  Clicks "Scan Details" -> Reviews the match -> Clicks "Issue Takedown" or "Offer License".

---

## 3. The Library
**Goal**: Manage the lifecycle of Semantic Blueprints and visualize their relationships.

### Views
The Library has two main modes: **All Assets (Grid/List)** and **Asset Detail (Genealogy)**.

#### A. Main Library View (`/library`)
*   **Search & Filter Sidebar**:
    *   *Search*: Text input for title/tags.
    *   *Type*: Original, Derivative.
    *   *Format*: Text, Script, Comic, Audio.
    *   *Status*: Processing, Ready, Registered, Listed.
*   **Asset Grid**:
    *   Cards representing each project.
    *   **Card Content**:
        *   Thumbnail (AI generated or uploaded cover).
        *   Title & Format Icon.
        *   Status Badge (e.g., "On-Chain").
        *   "Quick Actions" menu (three dots): Rename, Delete, View Details, **Share to Social**.

#### B. Asset Detail View (`/library/[id]`)
This is the "Power View" for a specific piece of IP.

*   **Header**: Title, Version, Story Protocol ID (link to explorer).
*   **Tabs**:
    1.  **Overview**: Metadata, Description, Tags.
    2.  **The Blueprint**:
        *   Visualizer for the Semantic JSON.
        *   Accordion views for "Narrative Arcs", "Characters", "Themes".
        *   *Action*: "Edit Blueprint" (Refine the extraction).
    3.  **Genealogy (The Tree)**:
        *   **Visual Graph**: Shows the current asset in the center.
        *   *Parents*: Lines going up to source material (if this is a derivative).
        *   *Children*: Lines going down to derivatives created from this.
        *   *Siblings*: Other derivatives from the same parent.
        *   *Interaction*: Clicking a node navigates to that asset.
    4.  **Marketplace Listing**:
        *   Toggle: "List on Marketplace".
        *   Settings: Price, Licensing Terms (Update Contracts).
    5.  **Protection**:
        *   Log of infringement scans.
        *   Status of blockchain registration.

### Actions in Library
*   **"Generate Derivative"**: One of the primary actions on an asset page. Takes the current Blueprint and sends it to the `/produce` flow as the *Source*.
*   **"Protect/Register"**: If status is "Draft", triggers the Story Protocol registration transaction.
*   **"Scan"**: Run a targeted infringement check for this specific asset.
*   **"Social Share"**: Generate a "Share Card" with a link to the public marketplace listing, optimized for Twitter/LinkedIn.

---

## 4. The Marketplace (Remix Engine)
**Goal**: A Midjourney-style feed where "Prompts" are replaced by "Blueprints".

*   **The Feed**: Infinite scroll of high-quality cover art representing Blueprints.
*   **Interaction**:
    1.  User clicks a Blueprint ("Space Opera Novel").
    2.  Sees the **"Remix"** button (instead of just "Copy").
    3.  **Remix Flow**:
        *   "I want to turn this [Novel] into a [Cyberpunk Anime Script]."
        *   "Let AI decide" (Surprise Me mode).
    4.  **Pipeline**:
        *   System fetches the licensed Semantic JSON.
        *   Injects it into a generative pipeline (e.g., Nano Banana for audio, Stable Diffusion for art, LLM for script).
        *   Generates the derivative.
        *   **Auto-Licenses**: Automatically registers the new derivative on Story Protocol as a child of the original, respecting the royalty contract.

---

## 5. Integration with Produce Flow
*   **Produce (`/produce`)** is the *verb* (Process).
*   **Library (`/library`)** is the *noun* (Result).

**Flow**:
1.  User goes to **Produce**.
2.  Uploads file -> "Processing...".
3.  Once finished, the user is redirected to the **Library Detail View** of the new asset to review the generated Blueprint.

---

## 6. Technical Requirements (Frontend)

### Components Needed
*   `DashboardLayout`: Sidebar nav + Header.
*   `ActivityFeed`: List component with icon types.
*   `AssetCard`: Reusable card with image, badges, dropdown.
*   `GenealogyTree`: D3.js or React Flow component for visualizing parent/child relationships.
*   `BlueprintViewer`: Syntax highlighter or "JSON-to-UI" mapper (Cards for characters, etc.).
*   `FilterBar`: Faceted search component.
*   `ScanWidget`: UI for initiating and viewing infringement scans.
*   `ContractEditor`: Form for updating Story Protocol licensing terms.

### Data Structure (Mock for UI)
```typescript
interface Asset {
  id: string;
  title: string;
  type: 'original' | 'derivative';
  format: 'novel' | 'comic' | 'script' | 'game';
  status: 'processing' | 'draft' | 'registered' | 'listed';
  thumbnailUrl: string;
  storyProtocolId?: string;
  createdAt: string;
  parentId?: string; // For genealogy
  childrenIds?: string[]; // For genealogy
  infringementStatus?: 'clean' | 'detecting' | 'flagged';
}

interface Activity {
  id: string;
  type: 'system' | 'commerce' | 'social' | 'blockchain' | 'alert';
  message: string;
  timestamp: string;
  link?: string;
}
```

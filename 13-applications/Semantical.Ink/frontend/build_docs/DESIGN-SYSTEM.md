# Semantical.Ink - Design System & UX Guidelines

## 1. Core Philosophy
The design language of Semantical.Ink balances **Creative Playfulness** with **Professional Power**.
*   **Playful**: Uses vibrant, neon-inspired colors to signal creativity, "remixing," and future-tech.
*   **Grounded**: Uses deep dark backgrounds (`brand-dark`) and clean white surfaces to ensure the tool feels stable and trustworthy for professional IP management.
*   **Fluid**: Uses organic shapes (waves, rounded corners, pills) to represent the malleability of semantic data.

---

## 2. Color Palette

### Primary Brand Colors
These define the personality of the application.

| Color Name | Hex Code | Usage | Meaning |
| :--- | :--- | :--- | :--- |
| **Brand Dark** | `#0F172A` | Backgrounds, Text on Light | The "Canvas" of the universe. Stability, Depth. |
| **Brand Yellow** | `#FDE047` | Highlights, Accents, Icons | "Spark." Ideas, Energy, Attention. |
| **Brand Pink** | `#EC4899` | Primary CTAs, Gradients | "Soul." Creativity, Emotion, Human element. |
| **Brand Cyan** | `#06B6D4` | Tech accents, Links, Buttons | "Future." AI, Technology, Structure. |
| **Brand Purple** | `#4C1D95` | Deep accents, Gradients | "Magic." The transformation process. |
| **Brand Cream** | `#FEFCE8` | Light Backgrounds, Cards | Warmth. A softer alternative to pure white. |

### Functional Colors
*   **Success**: `#22C55E` (Green-500) - Registration confirmed, Analysis complete.
*   **Warning**: `#F59E0B` (Amber-500) - Pending action, Potential match found.
*   **Error**: `#EF4444` (Red-500) - Infringement detected, Failed upload.
*   **Text (Dark)**: `#0F172A` (Slate-900) - Primary text on light backgrounds.
*   **Text (Light)**: `#F8FAFC` (Slate-50) - Primary text on dark backgrounds.
*   **Muted**: `#94A3B8` (Slate-400) - Secondary text, borders.

---

## 3. Typography
Currently leveraging the system default sans-serif stack (Inter/Roboto/San Francisco) for maximum legibility and performance.

### Hierarchy
*   **Display Headings** (`text-5xl`, `text-7xl`): **Extra Bold** (`font-black`). Used for Hero sections. often white on dark or dark on light.
*   **Page Titles** (`text-3xl`, `text-4xl`): **Bold** (`font-bold`). Used for section headers.
*   **Subheadings** (`text-xl`): **Medium/Semi-Bold**. Used for card titles and lead paragraphs.
*   **Body Copy** (`text-base`): **Regular**. High contrast for readability.
*   **Labels/Badges** (`text-xs`, `text-sm`): **Bold, Uppercase, Tracking-Wide**. Used for UI tags (e.g., "OPERATING SYSTEM FOR IP").

---

## 4. Shapes & Geometry

### Corner Radius
*   **Cards & Containers**: `rounded-3xl` (Large, friendly curves).
*   **Buttons**: `rounded-full` (Pill shape).
*   **Inputs/Small Elements**: `rounded-xl` or `rounded-2xl`.

*Rationale: Avoid sharp edges. Semantic data is fluid, not rigid.*

### Dividers
*   **Wavy Separators**: Use SVG wave patterns to transition between contrasting sections (e.g., Dark Hero $\to$ Light Feature Section).
*   **Gradients**: Use subtle radial gradients or "glows" behind elements rather than hard borders where possible.

---

## 5. UI Component Patterns

### Buttons
*   **Primary (Action)**: Brand Pink or Cyan background, White text, `rounded-full`. Hover: Scale 105%, Shadow.
    *   *Example*: "Launch Studio", "Create Derivative".
*   **Secondary (Nav/Info)**: White or Transparent background, Border (White/10 or Gray/20), `rounded-full`.
    *   *Example*: "Read Docs", "View Details".
*   **Icon Buttons**: Circular containers (`w-10 h-10 rounded-full`) with centered icons.

### Cards (The "Asset" Metaphor)
The core unit of the Library and Marketplace.
*   **Container**: White or `bg-[#111]` (Dark Mode).
*   **Border**: Thin, subtle (`border-gray-200` or `border-white/10`).
*   **Shadow**: Soft, diffuse shadows (`shadow-xl`) on hover.
*   **Interaction**: Cards should lift (`-translate-y-1`) or glow on hover to invite clicking.

### Badges & Tags
*   **Style**: Pill-shaped, colored background with low opacity (`bg-brand-cyan/10`), colored text (`text-brand-cyan`).
*   **Usage**: Status indicators (e.g., "PROCESSING", "REGISTERED").

### Visual Effects
*   **Glassmorphism**: Used for floating panels or overlays. `backdrop-blur-md`, `bg-white/5`, `border-white/10`.
*   **Glows**: Colored "blobs" (`filter blur-[100px]`) placed behind key images or text to create depth.

---

## 6. Layout Principles

### "Breathing Room"
*   **Spacing**: Use generous padding (`py-24`, `py-32`) between major sections.
*   **Margins**: Content should never touch the edges of the screen on mobile (`px-4`).

### The "Dark Mode" Studio
*   The **Produce/Studio** and **Dashboard** pages should default to **Dark Mode** (Brand Dark background) to minimize eye strain during deep work and make the colorful content "pop."
*   The **Landing Page** and **Marketplace** can use lighter sections (Brand Cream/White) to feel more open and welcoming.

---

## 7. Iconography
*   **Style**: Filled or Thick Stroke icons (using `react-icons/fa` currently).
*   **Color**: Icons typically carry the Brand Color associated with their function (e.g., Cyan for Tech, Pink for Creative, Yellow for Highlights).
*   **Container**: Often placed inside a rounded square or circle with a matching light-opacity background.

---

## 8. Interaction States
*   **Hover**: Elements should react. Scale up slightly (`scale-105`), brighten, or show a colored border.
*   **Active/Focus**: Brand Cyan ring.
*   **Loading**: Pulse animations (`animate-pulse`) on skeletons or status indicators.

---

## Summary Checklist for Developers
When building new pages:
1.  [ ] Are you using `bg-brand-dark` for "Pro" interfaces?
2.  [ ] Are buttons `rounded-full`?
3.  [ ] Are main headings `font-black`?
4.  [ ] Are you using the defined Brand Colors for accents, not generic "blue" or "red"?
5.  [ ] Do sections have Wavy Separators if they switch background colors?


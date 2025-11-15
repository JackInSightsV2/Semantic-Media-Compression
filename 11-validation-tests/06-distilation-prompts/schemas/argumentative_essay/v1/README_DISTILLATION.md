# Argumentative Essay Distillation Script

Multi-pass semantic distillation script using OpenRouter (grok-4-fast) to extract structured blueprints from argumentative essays.

## Setup

1. **Create virtual environment:**
   ```bash
   python -m venv .venv
   ```

2. **Activate virtual environment:**
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   Create a `.env` file in this directory with:
   ```
   OPENROUTER_KEY=your_openrouter_api_key_here
   ```
   
   Or on Windows, you can create it manually or use:
   ```powershell
   echo "OPENROUTER_KEY=your_key_here" > .env
   ```

## Usage

1. **Place PDF in `data/` folder:**
   ```bash
   # The script will automatically find the first PDF in data/
   cp /path/to/essay.pdf data/
   ```

2. **Run distillation:**
   ```bash
   python distill_essay.py
   ```

## How It Works

The script performs **4 passes** to build the complete blueprint:

### Pass 1: Thesis + Outline
- Extracts central thesis and problem statement
- Identifies high-level essay structure (sections with IDs, labels, purposes)
- **Output**: Small JSON with `thesis` + `structure_and_rhetoric.outline`

### Pass 2: Claim Hierarchy
- Uses outline from Pass 1 to guide extraction
- Extracts all main claims, sub-claims, and dependencies
- **Output**: `claim_hierarchy` with `main_claims` array

### Pass 3: Evidence + Counterarguments
- Uses claim IDs from Pass 2
- Extracts evidence supporting each claim
- Extracts counterarguments and author's responses
- **Output**: `evidence` + `counterarguments` arrays

### Pass 4: Final Elements
- Extracts assumptions, value judgments, key definitions
- Extracts practical implications and recommendations
- Extracts sensitivities and misinterpretation risks
- Extracts rhetorical techniques
- **Output**: `assumptions_and_values`, `implications`, `sensitivities`, `rhetorical_techniques`

### Final Step: Merge + Validate
- Combines all passes into single blueprint
- Validates against full JSON Schema
- Saves to `output/blueprint_TIMESTAMP.json`

## Output Structure

### Response Files (`responses/`)
Each API call is saved with:
- `pass{number}_attempt{number}_{timestamp}_{description}.json`
- Contains full API response + metadata
- Use these to analyze model behavior and refine prompts

### Final Blueprint (`output/`)
```json
{
  "schema_id": "argumentative_essay_distillation",
  "schema_version": "1.0.0",
  "generated_at": "2025-11-15T10:52:00Z",
  "source": {
    "type": "text",
    "media_id": "essay_filename",
    "filename": "essay.pdf"
  },
  "blueprint": {
    "thesis": { ... },
    "claim_hierarchy": { ... },
    "evidence": [ ... ],
    "counterarguments": [ ... ],
    "assumptions_and_values": { ... },
    "structure_and_rhetoric": { ... },
    "implications": { ... },
    "sensitivities": { ... }
  }
}
```

**Next steps after generation:**
1. Add hash to `source.hash` (SHA256 of original PDF)
2. Add any final processing metadata
3. Validate against schema capsule if needed

## Error Handling

- Each pass retries up to 3 times on validation failure
- All responses are saved even if validation fails (for analysis)
- Final blueprint may have warnings but will still be saved

## Adjusting Prompts

To refine the distillation:
1. Review saved responses in `responses/`
2. Edit prompts in `distill_essay.py` (each pass has its own prompt)
3. Adjust schema snippets if needed
4. Re-run and compare results

## Schema Validation

The script validates:
- Each pass result against its schema snippet
- Final merged blueprint against full schema

If validation fails, the response is still saved for analysis, but the script will retry or warn.


"""Generic reinflation logic - loads all templates from prompt.md."""

import time
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from schema_loader import load_prompt, extract_prompt_template
from llm_client import call_openrouter, extract_json_from_response
from config import RESPONSES_DIR


def save_reinflation_response(response: Dict[str, Any], pass_number: int, attempt_number: int, description: str, run_timestamp: str) -> Path:
    """Save reinflation API response to file."""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_responses_dir = RESPONSES_DIR / run_timestamp
    run_responses_dir.mkdir(exist_ok=True)
    
    filename = f"pass{pass_number}_attempt{attempt_number}_{timestamp}_{description}.json"
    filepath = run_responses_dir / filename
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump({
            "metadata": {
                "pass_number": pass_number,
                "attempt_number": attempt_number,
                "timestamp": timestamp,
                "description": description,
                "model": response.get("model", "unknown")
            },
            "response": response
        }, f, indent=2)
    
    print(f"  [OK] Saved response to: {filename}")
    return filepath


def reinflate_section(
    template_name: str,
    blueprint: Dict[str, Any],
    prompt_path: Path,
    run_timestamp: str,
    section_data: Optional[Dict[str, Any]] = None,
    temperature: float = 0.4,  # Balanced temperature for faithfulness and completeness
    used_content: Optional[Dict[str, Any]] = None,  # Track content already used in other sections
    previously_generated_sections: Optional[List[str]] = None  # Previously generated sections to avoid repetition
) -> str:
    """
    Generic section reinflation using prompt template.
    
    Args:
        template_name: Name of template in prompt.md (e.g., "Introduction", "Body Sections", "Conclusion")
        blueprint: Full blueprint dictionary
        prompt_path: Path to prompt.md
        run_timestamp: Timestamp for this run
        section_data: Optional additional data to pass to template
        temperature: LLM temperature
    
    Returns:
        Reinflated text
    """
    prompt_md = load_prompt(prompt_path)
    
    try:
        system_msg, user_template = extract_prompt_template(prompt_md, template_name, default_system_msg=None)
    except ValueError as e:
        # Template not found, return placeholder
        print(f"  [DEBUG] Template lookup error: {e}")
        return f"<!-- {template_name} template not found in prompt.json -->"
    
    # Build template variables from blueprint
    template_vars = _build_template_vars(blueprint, section_data, used_content, previously_generated_sections)
    
    # Format template
    try:
        user_msg = user_template.format(**template_vars)
    except KeyError as e:
        # Missing placeholder, return error message
        return f"<!-- Template '{template_name}' missing placeholder: {e} -->"
    
    # Generate content
    attempt = 1
    while attempt <= 3:
        try:
            response = call_openrouter(system_msg, user_msg, temperature=temperature, response_format_json=False)
            save_reinflation_response(response, 5, attempt, f"reinflate_{template_name.lower().replace(' ', '_')}", run_timestamp)
            
            content = response["choices"][0]["message"]["content"]
            if content.startswith("```"):
                lines = content.split("\n")
                content = "\n".join(lines[1:-1]) if len(lines) > 2 else content
            
            return content.strip()
        except Exception as e:
            print(f"  [ERROR] Error: {e}")
            attempt += 1
            if attempt > 3:
                return f"<!-- {template_name} generation failed after 3 attempts -->"
            time.sleep(1)
    
    return f"<!-- {template_name} generation failed -->"


def _build_template_vars(
    blueprint: Dict[str, Any], 
    section_data: Optional[Dict[str, Any]] = None,
    used_content: Optional[Dict[str, Any]] = None,
    previously_generated_sections: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Build template variables from blueprint and optional section data.
    
    Args:
        blueprint: Full blueprint dictionary
        section_data: Optional section-specific data
        used_content: Dictionary tracking content already used in other sections
                     Format: {'quotes': set(), 'key_phrases': set(), 'examples': set()}
    """
    if used_content is None:
        used_content = {'quotes': set(), 'key_phrases': set(), 'examples': set()}
    
    vars_dict = {}
    
    # Extract nested values to top-level for easy template access
    # Problem & Motivation
    if 'problem_and_motivation' in blueprint:
        pm = blueprint['problem_and_motivation']
        vars_dict.update({
            'problem': pm.get('problem', ''),
            'why_it_matters': pm.get('why_it_matters', ''),
            'scope': pm.get('scope', ''),
        })
    
    # Prior Work
    if 'prior_work' in blueprint:
        pw = blueprint['prior_work']
        vars_dict.update({
            'summary': pw.get('summary', ''),
            'limitations': json.dumps(pw.get('limitations_in_prior_work', []), indent=2) if pw.get('limitations_in_prior_work') else 'None',
        })
    
    # Document Structure
    if 'document_structure' in blueprint:
        structure = blueprint['document_structure']
        title_page = structure.get('title_page', {})
        references = structure.get('references', [])
        vars_dict.update({
            'title': title_page.get('title', ''),
            'author': title_page.get('author', ''),
            'dedication': title_page.get('dedication', '') or 'None',
            'acknowledgments': title_page.get('acknowledgments', '') or 'None',
            'sections': structure.get('sections', []),
            'figures': structure.get('figures', []),
            'tables': structure.get('tables', []),
            'references_json': json.dumps(references, indent=2, ensure_ascii=False) if references else '[]',
            'reference_count': len(references),
        })
    
    # Layout Metadata
    if 'layout_metadata' in blueprint:
        layout = blueprint['layout_metadata']
        vars_dict.update({
            'format_type': layout.get('format_type', 'academic paper'),
            'copyright_notice': layout.get('copyright_notice', ''),
            'has_footnotes': layout.get('has_footnotes', False),
            'typography_style': layout.get('typography_style', 'formatted'),
            'section_numbering_style': layout.get('section_numbering_style', 'arabic'),
            'heading_style': layout.get('heading_style', 'numbered'),
            'abstract_placement': layout.get('abstract_placement', 'after_title'),
            'citation_style_in_text': layout.get('citation_style_in_text', 'author_year'),
            'reference_section_style': layout.get('reference_section_style', 'numbered_list'),
            'paragraph_spacing': layout.get('paragraph_spacing', 'spaced'),
            'list_formatting': layout.get('list_formatting', 'bullets'),
            'document_flow_pattern': layout.get('document_flow_pattern', 'thematic'),
        })
        
        # Format layout guidance for templates
        layout_guidance = []
        if layout.get('section_numbering_style'):
            layout_guidance.append(f"Section numbering: {layout.get('section_numbering_style')}")
        if layout.get('heading_style'):
            layout_guidance.append(f"Heading style: {layout.get('heading_style')}")
        if layout.get('paragraph_spacing'):
            layout_guidance.append(f"Paragraph spacing: {layout.get('paragraph_spacing')}")
        if layout.get('document_flow_pattern'):
            layout_guidance.append(f"Document flow: {layout.get('document_flow_pattern')}")
        
        vars_dict['layout_guidance'] = '; '.join(layout_guidance) if layout_guidance else 'Standard academic format'
    else:
        vars_dict.update({
            'format_type': 'academic paper',
            'copyright_notice': '',
            'has_footnotes': False,
            'typography_style': 'formatted',
            'section_numbering_style': 'arabic',
            'heading_style': 'numbered',
            'abstract_placement': 'after_title',
            'citation_style_in_text': 'author_year',
            'reference_section_style': 'numbered_list',
            'paragraph_spacing': 'spaced',
            'list_formatting': 'bullets',
            'document_flow_pattern': 'thematic',
            'layout_guidance': 'Standard academic format',
        })
    
    # Examples and Case Studies
    if 'examples_and_case_studies' in blueprint:
        examples = blueprint['examples_and_case_studies']
        # Filter examples by section if section_data provided
        if section_data and section_data.get('section_id'):
            section_id = section_data.get('section_id')
            relevant_examples = [e for e in examples if e.get('section_id') == section_id]
        else:
            relevant_examples = examples
        
        # Format examples for template
        examples_text = []
        for ex in relevant_examples:
            ex_text = f"- {ex.get('description', '')}"
            if ex.get('specific_details'):
                ex_text += f" (Details: {', '.join(ex.get('specific_details', []))})"
            if ex.get('citations'):
                ex_text += f" [Cited: {', '.join(ex.get('citations', []))}]"
            examples_text.append(ex_text)
        
        vars_dict['examples'] = '\n'.join(examples_text) if examples_text else 'None'
        vars_dict['examples_and_case_studies'] = relevant_examples
    else:
        vars_dict['examples'] = 'None'
        vars_dict['examples_and_case_studies'] = []
    
    # Contributions - filter to section-relevant only
    if 'contributions' in blueprint and section_data:
        section_title = section_data.get('section_title', '').lower()
        relevant_contributions = []
        for contrib in blueprint['contributions']:
            contrib_desc = contrib.get('description', '').lower()
            # Only include if relevant to section title
            if any(word in contrib_desc for word in section_title.split() if len(word) > 4):
                relevant_contributions.append(contrib)
        if relevant_contributions:
            vars_dict['contributions'] = json.dumps(relevant_contributions, indent=2)
        else:
            vars_dict['contributions'] = 'None (not relevant to this section)'
    elif 'contributions' in blueprint:
        vars_dict['contributions'] = json.dumps(blueprint['contributions'], indent=2)
    
    # Setup & Assumptions - filter to section-relevant only
    if 'setup_and_assumptions' in blueprint and section_data:
        section_title = section_data.get('section_title', '').lower()
        setup = blueprint['setup_and_assumptions']
        # Only include if section is about setup/methodology
        if any(word in section_title for word in ['method', 'setup', 'assumption', 'approach', 'design']):
            vars_dict['setup'] = json.dumps(setup, indent=2)
        else:
            vars_dict['setup'] = 'None (not relevant to this section)'
    elif 'setup_and_assumptions' in blueprint:
        vars_dict['setup'] = json.dumps(blueprint['setup_and_assumptions'], indent=2)
    
    # Methodology - filter to section-relevant only
    if 'methodology' in blueprint and section_data:
        section_title = section_data.get('section_title', '').lower()
        # Only include if section is about methodology
        if any(word in section_title for word in ['method', 'approach', 'design', 'experiment', 'analysis', 'model']):
            vars_dict['methodology'] = json.dumps(blueprint['methodology'], indent=2)
        else:
            vars_dict['methodology'] = 'None (not relevant to this section)'
    elif 'methodology' in blueprint:
        vars_dict['methodology'] = json.dumps(blueprint['methodology'], indent=2)
    
    # Results - filter to section-relevant only
    if 'results' in blueprint and section_data:
        section_title = section_data.get('section_title', '').lower()
        # Only include if section is about results
        if any(word in section_title for word in ['result', 'finding', 'outcome', 'performance', 'evaluation']):
            vars_dict['results'] = json.dumps(blueprint['results'], indent=2)
        else:
            vars_dict['results'] = 'None (not relevant to this section)'
    elif 'results' in blueprint:
        vars_dict['results'] = json.dumps(blueprint['results'], indent=2)
    
    # Limitations
    if 'limitations' in blueprint:
        lim = blueprint['limitations']
        vars_dict.update({
            'stated': json.dumps(lim.get('stated', []), indent=2) if lim.get('stated') else 'None',
            'implied': json.dumps(lim.get('implied', []), indent=2) if lim.get('implied') else 'None',
            'failure_modes': json.dumps(lim.get('failure_modes', []), indent=2) if lim.get('failure_modes') else 'None',
        })
    
    # Implications
    if 'implications' in blueprint:
        imp = blueprint['implications']
        vars_dict.update({
            'recommended_uses': json.dumps(imp.get('recommended_uses', []), indent=2) if imp.get('recommended_uses') else 'None',
            'misuse_risks': json.dumps(imp.get('misuse_risks', []), indent=2) if imp.get('misuse_risks') else 'None',
            'future_work': json.dumps(imp.get('future_work', []), indent=2) if imp.get('future_work') else 'None',
        })
    
    # Quotes - use section-specific if provided, filter out already-used quotes
    if section_data and section_data.get('section_quotes'):
        quotes_list = section_data['section_quotes']
    else:
        quotes_list = blueprint.get('quotes_and_anecdotes', [])
    
    # Filter out quotes already used in other sections
    if quotes_list:
        unused_quotes = []
        for q in quotes_list:
            quote_text = q.get('text', '')
            # Use first 50 chars as identifier
            quote_id = quote_text[:50] if quote_text else ''
            if quote_id and quote_id not in used_content['quotes']:
                unused_quotes.append(q)
                used_content['quotes'].add(quote_id)
        
        if unused_quotes:
            quotes_text = "\n".join([f"- \"{q.get('text', '')}\"" for q in unused_quotes[:5]])
            vars_dict['quotes'] = quotes_text
        else:
            vars_dict['quotes'] = 'None (all relevant quotes already used in other sections)'
    else:
        vars_dict['quotes'] = 'None'
    
    # Tone Metadata - filter out already-used key phrases
    if 'tone_metadata' in blueprint:
        tone = blueprint['tone_metadata']
        all_key_phrases = tone.get('key_phrases', [])
        # Filter out already-used phrases
        unused_phrases = [p for p in all_key_phrases if p not in used_content['key_phrases']]
        # Mark some as used (but keep a few for later sections)
        for phrase in unused_phrases[:2]:  # Use 2 phrases per section
            used_content['key_phrases'].add(phrase)
        
        vars_dict.update({
            'style': tone.get('style', 'academic paper'),
            'urgency': tone.get('urgency_level', 'medium'),
            'formality': tone.get('formality', 'formal'),
            'key_phrases': ', '.join(unused_phrases[:3]) or 'None',  # Show up to 3 unused phrases
        })
    else:
        vars_dict.update({
            'style': 'academic paper',
            'urgency': 'medium',
            'formality': 'formal',
            'key_phrases': 'None',
        })
    
    # Add section-specific data if provided
    if section_data:
        vars_dict.update(section_data)
        # Extract section-specific values
        vars_dict.update({
            'section_id': section_data.get('section_id', ''),
            'section_title': section_data.get('section_title', ''),
            'section_numbering': section_data.get('section_numbering', '') or 'None',
            'level': section_data.get('level', 1),
        })
        
        # Build heading
        heading_prefix = '#' * min(section_data.get('level', 1), 6)
        if section_data.get('section_numbering'):
            heading = f"{heading_prefix} {section_data['section_numbering']}. {section_data.get('section_title', '')}"
        else:
            heading = f"{heading_prefix} {section_data.get('section_title', '')}"
        vars_dict['heading'] = heading
    
    # Add previously generated sections to avoid repetition
    if previously_generated_sections:
        # Format previously generated sections for template
        prev_sections_text = "\n\n".join([
            f"## {i+1}. Previously Generated Section:\n{section}" 
            for i, section in enumerate(previously_generated_sections)
        ])
        vars_dict['previously_generated_sections'] = prev_sections_text
    else:
        vars_dict['previously_generated_sections'] = 'None (this is the first section)'
    
    # Add common convenience variables
    vars_dict.update({
        'section_or_subsection': section_data.get('is_subsection', False) and 'subsection' or 'section' if section_data else 'section',
        'SECTION_OR_SUBSECTION': section_data.get('is_subsection', False) and 'SUBSECTION' or 'SECTION' if section_data else 'SECTION',
    })
    
    # Default values for missing variables
    defaults = {
        'section_title': '',
        'section_numbering': '',
        'level': 1,
        'title': '',
        'author': '',
        'dedication': 'None',
        'acknowledgments': 'None',
        'problem': '',
        'why_it_matters': '',
        'scope': '',
        'summary': '',
        'limitations': 'None',
        'figures': 'None',
        'tables': 'None',
        'quotes': 'None',
        'heading': '# Introduction',
    }
    
    for key, default_value in defaults.items():
        if key not in vars_dict:
            vars_dict[key] = default_value
    
    return vars_dict


def reinflate_document(
    blueprint: Dict[str, Any],
    prompt_path: Path,
    run_timestamp: str,
    run_output_dir: Path
) -> Path:
    """
    Reinflate complete document from blueprint.
    Uses templates from prompt.json to determine structure.
    """
    print("\n" + "=" * 60)
    print("Reinflating Document from Blueprint")
    print("=" * 60)
    
    try:
        sections = []
        
        # Extract title
        title = "Document"
        structure = blueprint.get('document_structure', {})
        title_page = structure.get('title_page', {})
        if title_page.get('title'):
            title = title_page['title']
        elif 'story_overview' in blueprint:
            title = blueprint['story_overview'].get('title', 'Document')
        elif 'executive_summary' in blueprint:
            title = blueprint['executive_summary'].get('overview', 'Document')[:80]
        
        # Add copyright notice if present (before title for working papers)
        layout_meta = blueprint.get('layout_metadata', {})
        if layout_meta.get('copyright_notice'):
            sections.append(f"{layout_meta['copyright_notice']}\n\n")
        
        sections.append(f"# {title}\n\n")
        
        # Add author and affiliations if available
        if title_page.get('author'):
            author_line = f"*{title_page['author']}*"
            if title_page.get('author_affiliations'):
                author_line += f"\n{', '.join(title_page['author_affiliations'])}"
            sections.append(author_line + "\n\n")
        
        # Try Introduction template (only if no Introduction section in body)
        doc_sections = structure.get('sections', [])
        has_intro_section = any(s.get('title', '').lower() in ['introduction', 'abstract'] for s in doc_sections)
        
        # Initialize used_content tracking before any sections
        used_content = {
            'quotes': set(),
            'key_phrases': set(),
            'examples': set(),
        }
        
        if not has_intro_section:
            try:
                print("\n[Reinflation] Generating introduction...")
                intro = reinflate_section(
                    "Introduction", 
                    blueprint, 
                    prompt_path, 
                    run_timestamp,
                    temperature=0.4,
                    used_content=used_content
                )
                if intro and not intro.startswith("<!--"):
                    sections.append(intro)
                    print("  [OK] Introduction generated")
            except Exception as e:
                print(f"  [ERROR] Introduction failed: {e}")
        else:
            print("\n[Reinflation] Skipping Introduction template (found in body sections)")
        
        # Try Body Sections - iterate through document structure
        # (used_content already initialized above)
        # Deduplicate sections by title before reinflating (with Unicode normalization)
        import unicodedata
        def normalize_title(title):
            """Normalize Unicode for better duplicate detection."""
            normalized = unicodedata.normalize('NFKD', title.lower())
            # Remove combining characters and normalize whitespace
            normalized = ''.join(c for c in normalized if not unicodedata.combining(c))
            normalized = ' '.join(normalized.split())  # Normalize whitespace
            # Remove numbering prefix (e.g., "4. " or "1. ")
            import re
            normalized = re.sub(r'^\d+\.\s*', '', normalized)
            return normalized
        
        seen_titles = set()
        unique_sections = []
        for section in doc_sections:
            title = section.get('title', '')
            normalized_title = normalize_title(title)
            if normalized_title not in seen_titles:
                seen_titles.add(normalized_title)
                unique_sections.append(section)
            else:
                print(f"  [SKIP] Duplicate section '{title}' skipped (normalized: '{normalized_title}')")
        
        try:
            print("\n[Reinflation] Generating body sections...")
            if unique_sections:
                print(f"  [INFO] Found {len(unique_sections)} unique sections to reinflate (removed {len(doc_sections) - len(unique_sections)} duplicates)")
                previously_generated = []  # Track generated sections
                section_counter = 1  # Track sequential section numbers to avoid duplicates
                for section in unique_sections:
                    section_title_lower = section.get('title', '').lower()
                    # Skip if we already generated Introduction/Abstract
                    if section_title_lower in ['introduction', 'abstract'] and not has_intro_section:
                        continue
                    
                    # Skip "References" section - it's handled separately
                    if section_title_lower == 'references':
                        continue
                    
                    # Use sequential numbering to avoid duplicate section numbers
                    # Only use original numbering if it's a valid sequential number
                    original_numbering = section.get('numbering', '')
                    # Extract number from numbering (e.g., "4" from "4." or "IV" from "IV.")
                    try:
                        if original_numbering and original_numbering.strip():
                            # Try to extract numeric part
                            import re
                            num_match = re.match(r'^(\d+)', original_numbering.strip())
                            if num_match and int(num_match.group(1)) == section_counter:
                                # Original numbering matches our counter, use it
                                section_numbering = original_numbering
                            else:
                                # Use sequential numbering instead
                                section_numbering = str(section_counter)
                        else:
                            section_numbering = str(section_counter)
                    except:
                        section_numbering = str(section_counter)
                    
                    section_data = {
                        'section_id': section.get('id', ''),
                        'section_title': section.get('title', ''),
                        'section_numbering': section_numbering,  # Use sequential numbering
                        'level': section.get('level', 2),
                        'is_subsection': section.get('level', 2) > 2,
                    }
                    
                    # Filter quotes to only those relevant to this section
                    section_quotes = []
                    if 'quotes_and_anecdotes' in blueprint:
                        section_id = section.get('id', '')
                        for quote in blueprint['quotes_and_anecdotes']:
                            if quote.get('section_id') == section_id or not quote.get('section_id'):
                                section_quotes.append(quote)
                    
                    # Add section-specific quote filtering to section_data
                    section_data['section_quotes'] = section_quotes[:5]  # Limit to 5 quotes per section
                    
                    # Pass used_content and previously_generated to track what's been used
                    body_content = reinflate_section(
                        "Body Sections", 
                        blueprint, 
                        prompt_path, 
                        run_timestamp, 
                        section_data,
                        temperature=0.4,  # Balanced temperature
                        used_content=used_content,  # Track used content
                        previously_generated_sections=previously_generated  # Pass previously generated sections
                    )
                    if body_content and not body_content.startswith("<!--"):
                        sections.append(body_content)
                        # Add to previously generated list (keep last 5 to manage context size)
                        previously_generated.append(body_content)
                        if len(previously_generated) > 5:
                            previously_generated.pop(0)  # Keep only last 5 sections
                        section_counter += 1  # Increment for next section
                        print(f"  [OK] Section '{section.get('title', '')}' generated (numbered as {section_numbering})")
                    time.sleep(0.5)  # Rate limiting
            else:
                # No sections, try generic body template
                body = reinflate_section("Body Sections", blueprint, prompt_path, run_timestamp, previously_generated_sections=[])
                if body and not body.startswith("<!--"):
                    sections.append(body)
                    print("  [OK] Body sections generated")
        except Exception as e:
            print(f"  [ERROR] Body sections failed: {e}")
            import traceback
            traceback.print_exc()
        
        # Try Conclusion template (only if no Conclusion section in body)
        has_conclusion_section = any(s.get('title', '').lower() in ['conclusion', 'conclusions'] for s in doc_sections)
        
        if not has_conclusion_section:
            try:
                print("\n[Reinflation] Generating conclusion...")
                # Pass previously generated sections to conclusion (all body sections)
                conclusion_previously_generated = [s for s in sections if not s.startswith('# Document') and not s.startswith('Copyright')]
                conclusion = reinflate_section(
                    "Conclusion", 
                    blueprint, 
                    prompt_path, 
                    run_timestamp,
                    temperature=0.4,
                    used_content=used_content,  # Use same tracking to avoid repetition
                    previously_generated_sections=conclusion_previously_generated[-5:] if conclusion_previously_generated else []  # Last 5 sections
                )
                if conclusion and not conclusion.startswith("<!--"):
                    sections.append(conclusion)
                    print("  [OK] Conclusion generated")
            except Exception as e:
                print(f"  [ERROR] Conclusion failed: {e}")
        else:
            print("\n[Reinflation] Skipping Conclusion template (found in body sections)")
        
        # Add Acknowledgements if present
        if title_page.get('acknowledgments'):
            sections.append(f"## Acknowledgements\n\n{title_page['acknowledgments']}\n\n")
            print("  [OK] Acknowledgements added")
        
        # Add References if present - use LLM template for proper formatting
        references = structure.get('references', [])
        if references:
            try:
                print("\n[Reinflation] Formatting references section...")
                # Build template variables for references
                references_json = json.dumps(references, indent=2, ensure_ascii=False)
                ref_template_vars = {
                    'references_json': references_json,
                    'reference_count': len(references),
                    'style': blueprint.get('tone_metadata', {}).get('style', 'academic paper'),
                    'formality': blueprint.get('tone_metadata', {}).get('formality', 'formal'),
                }
                
                # Try to use References template
                try:
                    formatted_refs = reinflate_section(
                        "References",
                        blueprint,
                        prompt_path,
                        run_timestamp,
                        section_data=None,
                        temperature=0.4,  # Balanced temperature for faithful citation formatting
                        used_content=None
                    )
                    
                    # Post-process to clean up any remaining line breaks in citations
                    if formatted_refs and not formatted_refs.startswith("<!--"):
                        # Remove \n characters that appear in the middle of citations (but keep blank lines between refs)
                        lines = formatted_refs.split('\n')
                        cleaned_lines = []
                        in_reference = False
                        current_ref = []
                        
                        for line in lines:
                            line_stripped = line.strip()
                            # Check if this is a reference line (starts with [number] or similar)
                            if line_stripped and (line_stripped.startswith('[') or (line_stripped and not line_stripped.startswith('##'))):
                                if current_ref:
                                    # Join previous reference parts and add
                                    cleaned_ref = ' '.join(current_ref).replace('\\n', ' ').replace('\n', ' ')
                                    cleaned_lines.append(cleaned_ref)
                                current_ref = [line_stripped]
                                in_reference = True
                            elif in_reference and line_stripped:
                                # Continuation of current reference
                                current_ref.append(line_stripped.replace('\\n', ' ').replace('\n', ' '))
                            elif not line_stripped:
                                # Blank line - end current reference if we have one
                                if current_ref:
                                    cleaned_ref = ' '.join(current_ref).replace('\\n', ' ').replace('\n', ' ')
                                    cleaned_lines.append(cleaned_ref)
                                    cleaned_lines.append('')
                                    current_ref = []
                                    in_reference = False
                                else:
                                    cleaned_lines.append('')
                            else:
                                # Other content (like headers)
                                if current_ref:
                                    cleaned_ref = ' '.join(current_ref).replace('\\n', ' ').replace('\n', ' ')
                                    cleaned_lines.append(cleaned_ref)
                                    current_ref = []
                                cleaned_lines.append(line)
                                in_reference = False
                        
                        # Handle any remaining reference
                        if current_ref:
                            cleaned_ref = ' '.join(current_ref).replace('\\n', ' ').replace('\n', ' ')
                            cleaned_lines.append(cleaned_ref)
                        
                        formatted_refs = '\n'.join(cleaned_lines)
                    
                    if formatted_refs and not formatted_refs.startswith("<!--"):
                        sections.append(formatted_refs)
                        print(f"  [OK] References formatted ({len(references)} entries)")
                    else:
                        # Fallback to simple formatting if template fails
                        print("  [WARNING] References template not found, using simple formatting")
                        sections.append("## References\n\n")
                        for ref in references:
                            citation = ref.get('citation', '')
                            ref_id = ref.get('id', '')
                            if ref_id:
                                sections.append(f"[{ref_id}] {citation}\n\n")
                            else:
                                sections.append(f"{citation}\n\n")
                        sections.append("\n")
                        print(f"  [OK] References added ({len(references)} entries)")
                except Exception as e:
                    print(f"  [WARNING] References template failed: {e}, using simple formatting")
                    # Fallback to simple formatting
                    sections.append("## References\n\n")
                    for ref in references:
                        citation = ref.get('citation', '')
                        ref_id = ref.get('id', '')
                        if ref_id:
                            sections.append(f"[{ref_id}] {citation}\n\n")
                        else:
                            sections.append(f"{citation}\n\n")
                    sections.append("\n")
                    print(f"  [OK] References added ({len(references)} entries)")
            except Exception as e:
                print(f"  [ERROR] References formatting failed: {e}")
                # Last resort: simple formatting
                sections.append("## References\n\n")
                for ref in references:
                    citation = ref.get('citation', '')
                    ref_id = ref.get('id', '')
                    if ref_id:
                        sections.append(f"[{ref_id}] {citation}\n\n")
                    else:
                        sections.append(f"{citation}\n\n")
                sections.append("\n")
                print(f"  [OK] References added ({len(references)} entries)")
        
        # If no templates worked, create basic structure from blueprint
        if len(sections) <= 1:  # Only title
            print("  [WARNING] No templates succeeded, using fallback structure")
            for key, value in blueprint.items():
                if key not in ['document_structure', 'tone_metadata'] and isinstance(value, dict):
                    section_title = key.replace('_', ' ').title()
                    sections.append(f"## {section_title}\n\n{json.dumps(value, indent=2)}\n\n")
        
        # Combine sections
        reinflated_content = "\n\n".join(sections)
        
        # Save reinflated markdown
        reinflated_path = run_output_dir / f"reinflated_{run_timestamp}.md"
        with open(reinflated_path, "w", encoding="utf-8") as f:
            f.write(reinflated_content)
        
        print(f"\n[OK] Reinflated document saved to: {reinflated_path}")
        return reinflated_path
        
    except Exception as e:
        print(f"\n[ERROR] Reinflation failed: {e}")
        import traceback
        traceback.print_exc()
        raise


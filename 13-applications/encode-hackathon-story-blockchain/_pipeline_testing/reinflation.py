"""Generic reinflation logic - loads all templates from prompt.json."""

import time
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
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
    previously_generated_sections: Optional[List[str]] = None,  # Previously generated sections to avoid repetition
    logging_service: Optional[Any] = None  # Optional logging service for metrics
) -> str:
    """
    Generic section reinflation using prompt template.
    
    Args:
        template_name: Name of template in prompt.json (e.g., "Introduction", "Body Sections", "Conclusion")
        blueprint: Full blueprint dictionary
        prompt_path: Path to prompt.json
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
            response, metrics = call_openrouter(system_msg, user_msg, temperature=temperature, response_format_json=False)
            save_reinflation_response(response, 5, attempt, f"reinflate_{template_name.lower().replace(' ', '_')}", run_timestamp)
            
            # Log metrics if logging service is provided
            if logging_service:
                usage = metrics.get("usage", {})
                response_time_ms = metrics.get("response_time_ms", 0)
                logging_service.record_llm_call(response, response_time_ms)
            
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
            section_title = section_data.get('section_title', '').lower()
            
            # First, try exact section_id match
            relevant_examples = [e for e in examples if e.get('section_id') == section_id]
            
            # If no matches, try fuzzy matching on section title
            if not relevant_examples and section_title:
                for ex in examples:
                    ex_section = (ex.get('section_id') or '').lower()
                    ex_desc = (ex.get('description') or '').lower()
                    # Check if section title keywords appear in example's section or description
                    title_words = [w for w in section_title.split() if len(w) > 4]
                    if any(word in ex_section or word in ex_desc for word in title_words):
                        relevant_examples.append(ex)
            
            # For reports, also include policy/legislation examples that might be relevant
            # even if not explicitly linked to this section
            if not relevant_examples or len(relevant_examples) < 5:
                policy_examples = [e for e in examples if 'policy' in e.get('type', '').lower() or 
                                  'legislation' in e.get('description', '').lower() or
                                  any(term in e.get('description', '').lower() for term in 
                                      ['act', 'framework', 'recommendation 114', 'scotland', 'wales', 'northern ireland'])]
                # Add policy examples that aren't already included
                for ex in policy_examples:
                    if ex not in relevant_examples:
                        relevant_examples.append(ex)
        else:
            # For reports, include all examples as they contain critical policy/statistical details
            # that may be relevant across sections
            relevant_examples = examples
        
        # Format examples for template - make details more prominent
        examples_text = []
        for ex in relevant_examples[:50]:  # Limit to 50 most relevant to avoid token overflow
            ex_type = ex.get('type', 'example')
            ex_desc = ex.get('description', '')
            ex_text = f"**[{ex_type.upper()}]** {ex_desc}"
            if ex.get('specific_details'):
                # Make specific details VERY prominent - these contain policy names, dates, stats
                details_str = ' | '.join(ex.get('specific_details', []))
                ex_text += f"\n  → **KEY DETAILS**: {details_str}"
            if ex.get('citations'):
                ex_text += f"\n  → Citations: {', '.join(ex.get('citations', []))}"
            if ex.get('section_id'):
                ex_text += f"\n  → Section: {ex.get('section_id')}"
            examples_text.append(ex_text)
        
        vars_dict['examples'] = '\n\n'.join(examples_text) if examples_text else 'None'
        vars_dict['examples_and_case_studies'] = relevant_examples[:50]
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
    
    # Results - include quantitative results for reports (they contain policy names, statistics)
    if 'results' in blueprint:
        results = blueprint['results']
        # For reports, always include quantitative results as they contain critical policy/statistical details
        # Format quantitative results for easy reference - make them VERY prominent
        quantitative = results.get('quantitative', [])
        if quantitative:
            quant_text = []
            for q in quantitative:
                desc = q.get('description', '')
                compared = q.get('compared_to', '')
                # Highlight policy names, dates, statistics in the description
                quant_text.append(f"**QUANTITATIVE RESULT**: {desc}")
                if compared:
                    quant_text.append(f"  → Compared to: {compared}")
            vars_dict['quantitative_results'] = '\n\n'.join(quant_text) if quant_text else 'None'
        else:
            vars_dict['quantitative_results'] = 'None'
        
        # Full results JSON for detailed access
        vars_dict['results'] = json.dumps(results, indent=2)
    else:
        vars_dict['results'] = 'None'
        vars_dict['quantitative_results'] = 'None'
    
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
    
    # Business Plan Fields
    # Executive Summary
    if 'executive_summary' in blueprint:
        es = blueprint['executive_summary']
        # Format executive summary as readable text for templates
        exec_summary_text = f"Overview: {es.get('overview', '')}\n"
        exec_summary_text += f"Mission: {es.get('mission', '')}\n"
        if es.get('vision'):
            exec_summary_text += f"Vision: {es.get('vision', '')}\n"
        if es.get('key_objectives'):
            exec_summary_text += f"Key Objectives:\n" + '\n'.join([f"  - {obj}" for obj in es.get('key_objectives', [])]) + "\n"
        if es.get('value_proposition'):
            exec_summary_text += f"Value Proposition: {es.get('value_proposition', '')}\n"
        
        vars_dict.update({
            'executive_summary': exec_summary_text,
            'overview': es.get('overview', ''),
            'mission': es.get('mission', ''),
            'vision': es.get('vision', '') or 'None',
            'key_objectives': json.dumps(es.get('key_objectives', []), indent=2) if es.get('key_objectives') else 'None',
            'value_proposition': es.get('value_proposition', '') or 'None',
        })
    else:
        vars_dict['executive_summary'] = 'None'
    
    # Company Description
    if 'company_description' in blueprint:
        cd = blueprint['company_description']
        # Format as readable text
        company_text = f"Company Name: {cd.get('company_name', '')}\n"
        company_text += f"Legal Structure: {cd.get('legal_structure', '')}\n"
        if cd.get('location'):
            company_text += f"Location: {cd.get('location', '')}\n"
        if cd.get('founding_date'):
            company_text += f"Founding Date: {cd.get('founding_date', '')}\n"
        if cd.get('history'):
            company_text += f"History: {cd.get('history', '')}\n"
        if cd.get('current_status'):
            company_text += f"Current Status: {cd.get('current_status', '')}\n"
        
        vars_dict.update({
            'company_description': company_text,
            'company_name': cd.get('company_name', ''),
            'legal_structure': cd.get('legal_structure', ''),
            'location': cd.get('location', '') or 'None',
            'founding_date': cd.get('founding_date', '') or 'None',
            'history': cd.get('history', '') or 'None',
            'current_status': cd.get('current_status', '') or 'None',
        })
    else:
        vars_dict['company_description'] = 'None'
    
    # Market Analysis
    if 'market_analysis' in blueprint:
        ma = blueprint['market_analysis']
        # Format as readable text
        market_text = f"Target Market: {ma.get('target_market', '')}\n"
        if ma.get('market_size'):
            market_text += f"Market Size: {ma.get('market_size', '')}\n"
        if ma.get('market_trends'):
            market_text += f"Market Trends:\n" + '\n'.join([f"  - {trend}" for trend in ma.get('market_trends', [])]) + "\n"
        if ma.get('competition'):
            market_text += f"Competition:\n"
            for comp in ma.get('competition', []):
                market_text += f"  - {comp.get('competitor_name', '')}: {comp.get('competitive_advantage', '')}\n"
        if ma.get('market_opportunity'):
            market_text += f"Market Opportunity: {ma.get('market_opportunity', '')}\n"
        
        vars_dict['market_analysis'] = market_text
        vars_dict['target_market'] = ma.get('target_market', '')
        vars_dict['market_size'] = ma.get('market_size', '') or 'None'
        vars_dict['market_opportunity'] = ma.get('market_opportunity', '') or 'None'
    else:
        vars_dict['market_analysis'] = 'None'
        vars_dict['target_market'] = ''
        vars_dict['market_size'] = 'None'
        vars_dict['market_opportunity'] = 'None'
    
    # Products and Services
    if 'products_and_services' in blueprint:
        ps = blueprint['products_and_services']
        # Format as readable text
        products_text = ""
        if ps.get('offerings'):
            products_text += "Offerings:\n"
            for offering in ps.get('offerings', []):
                products_text += f"  - {offering.get('name', '')}: {offering.get('description', '')}\n"
                if offering.get('features'):
                    products_text += f"    Features: {', '.join(offering.get('features', []))}\n"
                if offering.get('pricing_model'):
                    products_text += f"    Pricing: {offering.get('pricing_model', '')}\n"
        if ps.get('development_stage'):
            products_text += f"Development Stage: {ps.get('development_stage', '')}\n"
        if ps.get('intellectual_property'):
            products_text += f"Intellectual Property: {', '.join(ps.get('intellectual_property', []))}\n"
        
        vars_dict['products_and_services'] = products_text if products_text else 'None'
    else:
        vars_dict['products_and_services'] = 'None'
    
    # Marketing Strategy
    if 'marketing_strategy' in blueprint:
        ms = blueprint['marketing_strategy']
        # Format as readable text
        marketing_text = f"Strategy: {ms.get('strategy', '')}\n"
        if ms.get('channels'):
            marketing_text += f"Channels: {', '.join(ms.get('channels', []))}\n"
        if ms.get('pricing_strategy'):
            marketing_text += f"Pricing Strategy: {ms.get('pricing_strategy', '')}\n"
        if ms.get('sales_process'):
            marketing_text += f"Sales Process: {ms.get('sales_process', '')}\n"
        if ms.get('customer_acquisition'):
            marketing_text += f"Customer Acquisition: {ms.get('customer_acquisition', '')}\n"
        if ms.get('brand_positioning'):
            marketing_text += f"Brand Positioning: {ms.get('brand_positioning', '')}\n"
        
        vars_dict['marketing_strategy'] = marketing_text
    else:
        vars_dict['marketing_strategy'] = 'None'
    
    # Operations
    if 'operations' in blueprint:
        ops = blueprint['operations']
        # Format as readable text
        ops_text = f"Operational Model: {ops.get('operational_model', '')}\n"
        if ops.get('facilities'):
            ops_text += f"Facilities: {', '.join(ops.get('facilities', []))}\n"
        if ops.get('supply_chain'):
            ops_text += f"Supply Chain: {ops.get('supply_chain', '')}\n"
        if ops.get('technology'):
            ops_text += f"Technology: {', '.join(ops.get('technology', []))}\n"
        if ops.get('key_partnerships'):
            ops_text += f"Key Partnerships: {', '.join(ops.get('key_partnerships', []))}\n"
        
        vars_dict['operations'] = ops_text
    else:
        vars_dict['operations'] = 'None'
    
    # Management Team
    if 'management_team' in blueprint:
        mt = blueprint['management_team']
        # Format as readable text
        mgmt_text = ""
        if mt.get('team_members'):
            mgmt_text += "Team Members:\n"
            for member in mt.get('team_members', []):
                mgmt_text += f"  - {member.get('name', '')} ({member.get('role', '')}): {member.get('background', '') or ''}\n"
                if member.get('expertise'):
                    mgmt_text += f"    Expertise: {', '.join(member.get('expertise', []))}\n"
        if mt.get('organizational_structure'):
            mgmt_text += f"Organizational Structure: {mt.get('organizational_structure', '')}\n"
        if mt.get('advisory_board'):
            mgmt_text += f"Advisory Board:\n"
            for advisor in mt.get('advisory_board', []):
                mgmt_text += f"  - {advisor.get('name', '')}: {advisor.get('expertise', '') or ''}\n"
        
        vars_dict['management_team'] = mgmt_text if mgmt_text else 'None'
    else:
        vars_dict['management_team'] = 'None'
    
    # Financial Projections
    if 'financial_projections' in blueprint:
        fp = blueprint['financial_projections']
        # Format as readable text
        financial_text = ""
        if fp.get('projections'):
            financial_text += "Projections:\n"
            for proj in fp.get('projections', []):
                financial_text += f"  - {proj.get('period', '')}: Revenue: {proj.get('revenue', '')}, Expenses: {proj.get('expenses', '')}, Profit: {proj.get('profit', 'N/A')}\n"
                if proj.get('assumptions'):
                    financial_text += f"    Assumptions: {', '.join(proj.get('assumptions', []))}\n"
        if fp.get('break_even_analysis'):
            financial_text += f"Break-Even Analysis: {fp.get('break_even_analysis', '')}\n"
        if fp.get('key_metrics'):
            financial_text += f"Key Metrics: {', '.join(fp.get('key_metrics', []))}\n"
        if fp.get('financial_assumptions'):
            financial_text += f"Financial Assumptions: {', '.join(fp.get('financial_assumptions', []))}\n"
        
        vars_dict['financial_projections'] = financial_text if financial_text else 'None'
        
        # Extract financial data for easy reference - make it VERY prominent
        projections = fp.get('projections', [])
        if projections:
            financial_data_text = []
            for proj in projections:
                period = proj.get('period', '')
                revenue = proj.get('revenue', '')
                expenses = proj.get('expenses', '')
                profit = proj.get('profit', '') or 'N/A'
                assumptions = proj.get('assumptions', [])
                financial_data_text.append(f"**FINANCIAL PROJECTION ({period})**: Revenue: {revenue}, Expenses: {expenses}, Profit: {profit}")
                if assumptions:
                    financial_data_text.append(f"  → Assumptions: {', '.join(assumptions)}")
            vars_dict['financial_data'] = '\n\n'.join(financial_data_text) if financial_data_text else 'None'
        else:
            vars_dict['financial_data'] = 'None'
        
        # Also include break-even, key metrics, assumptions
        vars_dict['break_even_analysis'] = fp.get('break_even_analysis', '') or 'None'
        vars_dict['key_metrics'] = json.dumps(fp.get('key_metrics', []), indent=2) if fp.get('key_metrics') else 'None'
        vars_dict['financial_assumptions'] = json.dumps(fp.get('financial_assumptions', []), indent=2) if fp.get('financial_assumptions') else 'None'
    else:
        vars_dict['financial_projections'] = 'None'
        vars_dict['financial_data'] = 'None'
        vars_dict['break_even_analysis'] = 'None'
        vars_dict['key_metrics'] = 'None'
        vars_dict['financial_assumptions'] = 'None'
    
    # Funding Requirements
    if 'funding_requirements' in blueprint:
        fr = blueprint['funding_requirements']
        # Format as readable text
        funding_text = f"Amount Needed: {fr.get('amount_needed', '')}\n"
        if fr.get('use_of_funds'):
            funding_text += "Use of Funds:\n"
            for use in fr.get('use_of_funds', []):
                funding_text += f"  - {use.get('category', '')}: {use.get('amount', '')} - {use.get('description', '') or ''}\n"
        if fr.get('funding_type'):
            funding_text += f"Funding Type: {fr.get('funding_type', '')}\n"
        if fr.get('exit_strategy'):
            funding_text += f"Exit Strategy: {fr.get('exit_strategy', '')}\n"
        if fr.get('return_on_investment'):
            funding_text += f"Return on Investment: {fr.get('return_on_investment', '')}\n"
        
        vars_dict['funding_requirements'] = funding_text
        vars_dict['amount_needed'] = fr.get('amount_needed', '')
        vars_dict['use_of_funds'] = json.dumps(fr.get('use_of_funds', []), indent=2) if fr.get('use_of_funds') else 'None'
        vars_dict['funding_type'] = fr.get('funding_type', '') or 'None'
        vars_dict['exit_strategy'] = fr.get('exit_strategy', '') or 'None'
        vars_dict['return_on_investment'] = fr.get('return_on_investment', '') or 'None'
    else:
        vars_dict['funding_requirements'] = 'None'
        vars_dict['amount_needed'] = ''
        vars_dict['use_of_funds'] = 'None'
        vars_dict['funding_type'] = 'None'
        vars_dict['exit_strategy'] = 'None'
        vars_dict['return_on_investment'] = 'None'
    
    # Risks and Challenges
    if 'risks_and_challenges' in blueprint:
        rc = blueprint['risks_and_challenges']
        # Format as readable text
        risks_text = ""
        if rc.get('identified_risks'):
            risks_text += "Identified Risks:\n"
            for risk in rc.get('identified_risks', []):
                risks_text += f"  - {risk.get('risk', '')}: {risk.get('mitigation', '') or 'No mitigation specified'}\n"
        if rc.get('challenges'):
            risks_text += f"Challenges: {', '.join(rc.get('challenges', []))}\n"
        
        vars_dict['risks_and_challenges'] = risks_text if risks_text else 'None'
        vars_dict['identified_risks'] = json.dumps(rc.get('identified_risks', []), indent=2) if rc.get('identified_risks') else 'None'
        vars_dict['challenges'] = json.dumps(rc.get('challenges', []), indent=2) if rc.get('challenges') else 'None'
    else:
        vars_dict['risks_and_challenges'] = 'None'
        vars_dict['identified_risks'] = 'None'
        vars_dict['challenges'] = 'None'
    
    # Narrative Fiction Fields
    # Story Overview
    if 'story_overview' in blueprint:
        so = blueprint['story_overview']
        vars_dict.update({
            'title': so.get('title', ''),
            'author': so.get('author', '') or 'None',
            'premise': so.get('premise', '') or 'None',
            'summary': so.get('summary', ''),
            'genre': ', '.join(so.get('genre', [])) if so.get('genre') else 'None',
            'point_of_view': so.get('point_of_view', '') or 'None',
            'narrative_voice': so.get('narrative_voice', '') or 'None',
        })
    else:
        vars_dict.update({
            'title': '',
            'author': 'None',
            'premise': 'None',
            'summary': '',
            'genre': 'None',
            'point_of_view': 'None',
            'narrative_voice': 'None',
        })
    
    # Characters
    if 'characters' in blueprint:
        chars = blueprint['characters']
        # Format as readable text
        chars_text = ""
        char_goals = []
        char_flaws = []
        char_motivations = []
        char_backstories = []
        char_voices = []
        for char in chars:
            name = char.get('name', '')
            role = char.get('role', '')
            desc = char.get('description', '') or ''
            arc = char.get('character_arc', '') or ''
            traits = ', '.join(char.get('key_traits', [])) if char.get('key_traits') else ''
            goals = char.get('goals', [])
            flaws = char.get('flaws', [])
            motivations = char.get('motivations', [])
            backstory = char.get('backstory', '')
            voice = char.get('voice_distinction', '')
            
            chars_text += f"  - {name} ({role}): {desc}\n"
            if goals:
                chars_text += f"    Goals: {', '.join(goals)}\n"
                char_goals.extend([f"{name}: {g}" for g in goals])
            if flaws:
                chars_text += f"    Flaws: {', '.join(flaws)}\n"
                char_flaws.extend([f"{name}: {f}" for f in flaws])
            if motivations:
                chars_text += f"    Motivations: {', '.join(motivations)}\n"
                char_motivations.extend([f"{name}: {m}" for m in motivations])
            if backstory:
                chars_text += f"    Backstory: {backstory}\n"
                char_backstories.append(f"{name}: {backstory}")
            if voice:
                chars_text += f"    Voice: {voice}\n"
                char_voices.append(f"{name}: {voice}")
            if arc:
                chars_text += f"    Character Arc: {arc}\n"
            if traits:
                chars_text += f"    Key Traits: {traits}\n"
            if char.get('relationships'):
                rels = ', '.join([f"{r.get('character', '')} ({r.get('relationship_type', '')})" for r in char.get('relationships', [])])
                if rels:
                    chars_text += f"    Relationships: {rels}\n"
            
            # Micro-mechanics
            micro = char.get('micro_mechanics', {})
            if micro:
                if micro.get('facial_expressions'):
                    chars_text += f"    Facial Expressions: {', '.join(micro.get('facial_expressions', []))}\n"
                if micro.get('body_language'):
                    chars_text += f"    Body Language: {', '.join(micro.get('body_language', []))}\n"
                if micro.get('tells'):
                    chars_text += f"    Tells: {', '.join(micro.get('tells', []))}\n"
                if micro.get('vocal_tone'):
                    chars_text += f"    Vocal Tone: {micro.get('vocal_tone')}\n"
            
            # Psychological architecture
            psych = char.get('psychological_architecture', {})
            if psych:
                if psych.get('internal_monologue_structure'):
                    chars_text += f"    Internal Monologue: {psych.get('internal_monologue_structure')}\n"
                if psych.get('biases'):
                    chars_text += f"    Biases: {', '.join(psych.get('biases', []))}\n"
                if psych.get('trauma_patterns'):
                    chars_text += f"    Trauma Patterns: {', '.join(psych.get('trauma_patterns', []))}\n"
                if psych.get('desire_vs_need_conflict'):
                    chars_text += f"    Desire vs Need: {psych.get('desire_vs_need_conflict')}\n"
            
            # Interaction systems
            interaction = char.get('interaction_systems', {})
            if interaction:
                if interaction.get('influence_patterns'):
                    for inf in interaction.get('influence_patterns', []):
                        chars_text += f"    Influences {inf.get('target', '')} via {inf.get('method', '')}\n"
                if interaction.get('dominance_submission'):
                    chars_text += f"    Dominance/Submission: {interaction.get('dominance_submission')}\n"
                if interaction.get('attraction_avoidance'):
                    for aa in interaction.get('attraction_avoidance', []):
                        chars_text += f"    {aa.get('dynamic', '')} towards {aa.get('target', '')}\n"
        
        vars_dict['characters'] = chars_text if chars_text else 'None'
        vars_dict['character_goals'] = '\n'.join([f"  - {g}" for g in char_goals]) if char_goals else 'None'
        vars_dict['character_flaws'] = '\n'.join([f"  - {f}" for f in char_flaws]) if char_flaws else 'None'
        vars_dict['character_motivations'] = '\n'.join([f"  - {m}" for m in char_motivations]) if char_motivations else 'None'
        vars_dict['character_backstories'] = '\n'.join([f"  - {b}" for b in char_backstories]) if char_backstories else 'None'
        vars_dict['character_voices'] = '\n'.join([f"  - {v}" for v in char_voices]) if char_voices else 'None'
        # Also provide character names list for easy reference
        char_names = [c.get('name', '') for c in chars if c.get('name')]
        vars_dict['character_names'] = ', '.join(char_names) if char_names else 'None'
    else:
        vars_dict['characters'] = 'None'
        vars_dict['character_names'] = 'None'
        vars_dict['character_goals'] = 'None'
        vars_dict['character_flaws'] = 'None'
        vars_dict['character_motivations'] = 'None'
        vars_dict['character_backstories'] = 'None'
        vars_dict['character_voices'] = 'None'
    
    # Setting
    if 'setting' in blueprint:
        setting = blueprint['setting']
        vars_dict.update({
            'primary_setting': setting.get('primary_setting', ''),
            'time_period': setting.get('time_period', '') or 'None',
            'atmosphere': setting.get('atmosphere', '') or 'None',
        })
        
        # Geography
        geography = setting.get('geography', {})
        if geography:
            geo_text = ""
            if geography.get('physical_landscapes'):
                geo_text += f"Physical Landscapes: {', '.join(geography.get('physical_landscapes', []))}\n"
            if geography.get('climate'):
                geo_text += f"Climate: {geography.get('climate')}\n"
            vars_dict['geography'] = geo_text if geo_text else 'None'
        else:
            vars_dict['geography'] = 'None'
        
        # Culture
        culture = setting.get('culture', {})
        if culture:
            culture_text = ""
            if culture.get('norms'):
                culture_text += f"Norms: {', '.join(culture.get('norms', []))}\n"
            if culture.get('rituals'):
                culture_text += f"Rituals: {', '.join(culture.get('rituals', []))}\n"
            if culture.get('beliefs'):
                culture_text += f"Beliefs: {', '.join(culture.get('beliefs', []))}\n"
            vars_dict['culture'] = culture_text if culture_text else 'None'
        else:
            vars_dict['culture'] = 'None'
        
        # Politics
        politics = setting.get('politics', {})
        if politics:
            pol_text = ""
            if politics.get('power_structures'):
                pol_text += f"Power Structures: {', '.join(politics.get('power_structures', []))}\n"
            if politics.get('factions'):
                for faction in politics.get('factions', []):
                    pol_text += f"Faction: {faction.get('name', '')} - {faction.get('description', '') or ''}\n"
            vars_dict['politics'] = pol_text if pol_text else 'None'
        else:
            vars_dict['politics'] = 'None'
        
        # Economy
        economy = setting.get('economy', {})
        if economy:
            econ_text = ""
            if economy.get('resources'):
                econ_text += f"Resources: {', '.join(economy.get('resources', []))}\n"
            if economy.get('trade'):
                econ_text += f"Trade: {', '.join(economy.get('trade', []))}\n"
            if economy.get('scarcity_dynamics'):
                econ_text += f"Scarcity: {', '.join(economy.get('scarcity_dynamics', []))}\n"
            vars_dict['economy'] = econ_text if econ_text else 'None'
        else:
            vars_dict['economy'] = 'None'
        
        # Lore
        lore = setting.get('lore', {})
        if lore:
            lore_text = ""
            if lore.get('myths'):
                lore_text += f"Myths: {', '.join(lore.get('myths', []))}\n"
            if lore.get('history'):
                lore_text += f"History: {', '.join(lore.get('history', []))}\n"
            if lore.get('important_past_events'):
                lore_text += f"Past Events: {', '.join(lore.get('important_past_events', []))}\n"
            vars_dict['lore'] = lore_text if lore_text else 'None'
        else:
            vars_dict['lore'] = 'None'
        # Format locations
        locations = setting.get('locations', [])
        if locations:
            locs_text = '\n'.join([f"  - {loc.get('name', '')}: {loc.get('description', '') or ''}" for loc in locations])
            vars_dict['locations'] = locs_text
        else:
            vars_dict['locations'] = 'None'
        
        # For section-specific location, try to get from scenes
        if section_data and 'scenes' in blueprint:
            section_id = section_data.get('section_id', '')
            scenes = blueprint['scenes']
            section_scenes = [s for s in scenes if s.get('chapter_or_act') == section_id or s.get('section_id') == section_id]
            if section_scenes:
                # Use location from first scene in this section
                location = section_scenes[0].get('location', '') or setting.get('primary_setting', '')
                vars_dict['location'] = location
            else:
                vars_dict['location'] = setting.get('primary_setting', '') or 'None'
        else:
            vars_dict['location'] = setting.get('primary_setting', '') or 'None'
        
        # Extract physical objects and props for critical plot elements
        physical_objects = []
        # Check if setting has physical_objects_and_props (from Pass 2)
        if 'physical_objects_and_props' in setting:
            props = setting.get('physical_objects_and_props', [])
            if isinstance(props, list):
                physical_objects.extend([str(p) for p in props])
            elif props:
                physical_objects.append(str(props))
        # Also check scenes for evidence/proof items
        if 'scenes' in blueprint:
            for scene in blueprint.get('scenes', []):
                evidence = scene.get('evidence_proof_items') or scene.get('evidence') or scene.get('proof_items')
                if evidence:
                    if isinstance(evidence, list):
                        physical_objects.extend([str(e) for e in evidence])
                    else:
                        physical_objects.append(str(evidence))
        
        if physical_objects:
            vars_dict['physical_objects'] = '\n'.join([f"  - {obj}" for obj in physical_objects])
        else:
            vars_dict['physical_objects'] = 'None'
        
        # Social Dynamics
        social = setting.get('social_dynamics', {})
        if social:
            social_text = ""
            if social.get('power_imbalances'):
                for pi in social.get('power_imbalances', []):
                    social_text += f"Power Imbalance: {pi.get('relationship', '')}\n"
            if social.get('alliances'):
                for alliance in social.get('alliances', []):
                    members = ', '.join(alliance.get('members', []))
                    social_text += f"Alliance: {members}\n"
            if social.get('faction_tensions'):
                for ft in social.get('faction_tensions', []):
                    social_text += f"Faction Tension: {ft.get('factions', '')}\n"
            if social.get('social_rules'):
                social_text += f"Social Rules: {', '.join(social.get('social_rules', []))}\n"
            vars_dict['social_dynamics'] = social_text if social_text else 'None'
        else:
            vars_dict['social_dynamics'] = 'None'
        
        # Environmental Metaphors
        env_meta = setting.get('environmental_metaphors', {})
        if env_meta:
            env_text = ""
            if env_meta.get('weather_emotional_tone'):
                for wet in env_meta.get('weather_emotional_tone', []):
                    env_text += f"Weather ({wet.get('weather', '')}) reflects {wet.get('emotion', '')}\n"
            if env_meta.get('environment_theme_echo'):
                for ete in env_meta.get('environment_theme_echo', []):
                    env_text += f"Environment ({ete.get('environment', '')}) echoes theme: {ete.get('theme', '')}\n"
            if env_meta.get('spatial_symbolism'):
                for ss in env_meta.get('spatial_symbolism', []):
                    env_text += f"Spatial Symbolism: {ss.get('space', '')} - {ss.get('symbolic_meaning', '') or ''}\n"
            vars_dict['environmental_metaphors'] = env_text if env_text else 'None'
        else:
            vars_dict['environmental_metaphors'] = 'None'
        
        # World Simulation Rules
        world_sim = setting.get('world_simulation_rules', {})
        if world_sim:
            world_text = ""
            if world_sim.get('resource_flows'):
                world_text += f"Resource Flows: {', '.join(world_sim.get('resource_flows', []))}\n"
            if world_sim.get('physics_constraints'):
                world_text += f"Physics Constraints: {', '.join(world_sim.get('physics_constraints', []))}\n"
            if world_sim.get('magic_constraints'):
                world_text += f"Magic Constraints: {', '.join(world_sim.get('magic_constraints', []))}\n"
            if world_sim.get('ecological_impacts'):
                world_text += f"Ecological Impacts: {', '.join(world_sim.get('ecological_impacts', []))}\n"
            if world_sim.get('cultural_evolution'):
                world_text += f"Cultural Evolution: {', '.join(world_sim.get('cultural_evolution', []))}\n"
            vars_dict['world_simulation_rules'] = world_text if world_text else 'None'
        else:
            vars_dict['world_simulation_rules'] = 'None'
    else:
        vars_dict.update({
            'primary_setting': '',
            'time_period': 'None',
            'atmosphere': 'None',
            'locations': 'None',
            'location': 'None',
            'physical_objects': 'None',
            'geography': 'None',
            'culture': 'None',
            'politics': 'None',
            'economy': 'None',
            'lore': 'None',
            'social_dynamics': 'None',
            'environmental_metaphors': 'None',
            'world_simulation_rules': 'None',
        })
    
    # Themes
    if 'themes' in blueprint:
        themes = blueprint['themes']
        themes_text = ""
        if themes.get('primary_themes'):
            themes_text += f"Primary Themes: {', '.join(themes.get('primary_themes', []))}\n"
        if themes.get('secondary_themes'):
            themes_text += f"Secondary Themes: {', '.join(themes.get('secondary_themes', []))}\n"
        if themes.get('symbolism'):
            symbols = '\n'.join([f"  - {s.get('symbol', '')}: {s.get('meaning', '') or 'No meaning specified'}" for s in themes.get('symbolism', [])])
            themes_text += f"Symbolism:\n{symbols}\n"
        if themes.get('motifs'):
            motifs_text = ""
            for motif in themes.get('motifs', []):
                pattern = motif.get('pattern', '')
                appearances = ', '.join(motif.get('appearances', []))
                significance = motif.get('significance', '')
                motifs_text += f"  - {pattern}: appears in {appearances if appearances else 'various places'}"
                if significance:
                    motifs_text += f" (significance: {significance})"
                motifs_text += "\n"
            if motifs_text:
                themes_text += f"Motifs:\n{motifs_text}"
        
        vars_dict['themes'] = themes_text if themes_text else 'None'
        vars_dict['primary_themes'] = ', '.join(themes.get('primary_themes', [])) if themes.get('primary_themes') else 'None'
        vars_dict['secondary_themes'] = ', '.join(themes.get('secondary_themes', [])) if themes.get('secondary_themes') else 'None'
        vars_dict['symbolism'] = '\n'.join([f"  - {s.get('symbol', '')}: {s.get('meaning', '') or ''}" for s in themes.get('symbolism', [])]) if themes.get('symbolism') else 'None'
        vars_dict['motifs'] = '\n'.join([f"  - {m.get('pattern', '')}: {m.get('significance', '') or ''}" for m in themes.get('motifs', [])]) if themes.get('motifs') else 'None'
        
        # Philosophical & Moral Layers
        phil_moral = themes.get('philosophical_moral_layers', {})
        if phil_moral:
            phil_text = ""
            if phil_moral.get('ethical_dilemmas'):
                for ed in phil_moral.get('ethical_dilemmas', []):
                    chars_involved = ', '.join(ed.get('characters_involved', []))
                    phil_text += f"Ethical Dilemma: {ed.get('dilemma', '')} (involves: {chars_involved})\n"
            if phil_moral.get('moral_frameworks'):
                for mf in phil_moral.get('moral_frameworks', []):
                    chars = ', '.join(mf.get('characters', []))
                    phil_text += f"Moral Framework ({mf.get('framework', '')}): {chars}\n"
            if phil_moral.get('personal_codes'):
                for pc in phil_moral.get('personal_codes', []):
                    phil_text += f"Personal Code ({pc.get('character', '')}): {pc.get('code', '')}\n"
            if phil_moral.get('ideological_clashes'):
                for ic in phil_moral.get('ideological_clashes', []):
                    chars = ', '.join(ic.get('characters', []))
                    phil_text += f"Ideological Clash ({ic.get('ideologies', '')}): {chars}\n"
            vars_dict['philosophical_moral_layers'] = phil_text if phil_text else 'None'
        else:
            vars_dict['philosophical_moral_layers'] = 'None'
    else:
        vars_dict['themes'] = 'None'
        vars_dict['primary_themes'] = 'None'
        vars_dict['secondary_themes'] = 'None'
        vars_dict['symbolism'] = 'None'
        vars_dict['motifs'] = 'None'
        vars_dict['philosophical_moral_layers'] = 'None'
    
    # Narrative Style
    if 'narrative_style' in blueprint:
        ns = blueprint['narrative_style']
        vars_dict.update({
            'style_description': ns.get('style_description', ''),
            'pacing': ns.get('pacing', '') or 'None',
            'dialogue_style': ns.get('dialogue_style', '') or 'None',
            'descriptive_style': ns.get('descriptive_style', '') or 'None',
        })
        
        # Meta-layers
        meta = ns.get('meta_layers', {})
        if meta:
            meta_text = ""
            if meta.get('genre_conventions'):
                meta_text += f"Genre Conventions: {', '.join(meta.get('genre_conventions', []))}\n"
            if meta.get('tropes_used'):
                meta_text += f"Tropes Used: {', '.join(meta.get('tropes_used', []))}\n"
            if meta.get('tropes_subverted'):
                meta_text += f"Tropes Subverted: {', '.join(meta.get('tropes_subverted', []))}\n"
            if meta.get('audience_expectations'):
                meta_text += f"Audience Expectations: {', '.join(meta.get('audience_expectations', []))}\n"
            if meta.get('meta_commentary'):
                meta_text += f"Meta-commentary: {', '.join(meta.get('meta_commentary', []))}\n"
            vars_dict['meta_layers'] = meta_text if meta_text else 'None'
        else:
            vars_dict['meta_layers'] = 'None'
        
        # Rhythm & Cadence
        rhythm = ns.get('rhythm_and_cadence', {})
        if rhythm:
            rhythm_text = ""
            if rhythm.get('sentence_rhythm'):
                rhythm_text += f"Sentence Rhythm: {rhythm.get('sentence_rhythm')}\n"
            if rhythm.get('paragraph_choreography'):
                rhythm_text += f"Paragraph Choreography: {rhythm.get('paragraph_choreography')}\n"
            if rhythm.get('scene_length_modulation'):
                rhythm_text += f"Scene Length Modulation: {rhythm.get('scene_length_modulation')}\n"
            if rhythm.get('dialogue_breath_patterns'):
                rhythm_text += f"Dialogue Breath Patterns: {', '.join(rhythm.get('dialogue_breath_patterns', []))}\n"
            vars_dict['rhythm_and_cadence'] = rhythm_text if rhythm_text else 'None'
        else:
            vars_dict['rhythm_and_cadence'] = 'None'
    else:
        vars_dict.update({
            'style_description': 'narrative prose',
            'pacing': 'None',
            'dialogue_style': 'None',
            'descriptive_style': 'None',
            'meta_layers': 'None',
            'rhythm_and_cadence': 'None',
        })
    
    # Plot Structure
    if 'plot_structure' in blueprint:
        ps = blueprint['plot_structure']
        vars_dict.update({
            'structure_type': ps.get('structure_type', '') or 'None',
            'stakes': ps.get('stakes', '') or 'None',
            'conflict': ', '.join(ps.get('conflict', [])) if ps.get('conflict') else 'None',
            'inciting_incident': ps.get('inciting_incident', '') or 'None',
            'climax': ps.get('climax', '') or 'None',
            'resolution': ps.get('resolution', '') or 'None',
        })
        
        # Key Choices
        key_choices = ps.get('key_choices', [])
        if key_choices:
            choices_text = ""
            for choice in key_choices:
                choice_text = choice.get('choice', '')
                character = choice.get('character', '')
                context = choice.get('context', '')
                consequences = ', '.join(choice.get('consequences', [])) if choice.get('consequences') else ''
                choices_text += f"  - {character}: {choice_text}"
                if context:
                    choices_text += f" (context: {context})"
                if consequences:
                    choices_text += f" → consequences: {consequences}"
                choices_text += "\n"
            vars_dict['key_choices'] = choices_text if choices_text else 'None'
        else:
            vars_dict['key_choices'] = 'None'
        
        # Add ALL key turning points (not just section-specific)
        key_turning_points = ps.get('key_turning_points', [])
        if key_turning_points:
            vars_dict['all_key_turning_points'] = '\n'.join([f"  - {e}" for e in key_turning_points])
        else:
            vars_dict['all_key_turning_points'] = 'None'
        
        # Format acts/chapters for section-specific use
        acts = ps.get('acts_or_chapters', [])
        if acts and section_data:
            section_id = section_data.get('section_id', '')
            # Find matching act/chapter
            relevant_act = None
            for act in acts:
                if act.get('id') == section_id:
                    relevant_act = act
                    break
            if relevant_act:
                vars_dict['summary'] = relevant_act.get('summary', '')
                vars_dict['key_events'] = '\n'.join([f"  - {e}" for e in relevant_act.get('key_events', [])]) if relevant_act.get('key_events') else 'None'
                vars_dict['character_developments'] = '\n'.join([f"  - {d}" for d in relevant_act.get('character_developments', [])]) if relevant_act.get('character_developments') else 'None'
            else:
                # No matching act/chapter, set defaults
                vars_dict['summary'] = 'None'
                vars_dict['key_events'] = 'None'
                vars_dict['character_developments'] = 'None'
        else:
            # No section_data or no acts, set defaults
            vars_dict['summary'] = 'None'
            vars_dict['key_events'] = 'None'
            vars_dict['character_developments'] = 'None'
    else:
        vars_dict.update({
            'structure_type': 'None',
            'stakes': 'None',
            'conflict': 'None',
            'inciting_incident': 'None',
            'climax': 'None',
            'resolution': 'None',
            'key_choices': 'None',
            'summary': 'None',
            'key_events': 'None',
            'character_developments': 'None',
            'all_key_turning_points': 'None',
        })
    
    # Narrative Sequence
    if 'narrative_sequence' in blueprint:
        ns = blueprint['narrative_sequence']
        vars_dict['narrative_order'] = '\n'.join([f"  - {e}" for e in ns.get('narrative_order', [])]) if ns.get('narrative_order') else 'None'
        vars_dict['chronological_order'] = '\n'.join([f"  - {e}" for e in ns.get('chronological_order', [])]) if ns.get('chronological_order') else 'None'
    else:
        vars_dict['narrative_order'] = 'None'
        vars_dict['chronological_order'] = 'None'
    
    # Scenes
    if 'scenes' in blueprint:
        scenes = blueprint['scenes']
        # Filter scenes by section if section_data provided
        if section_data and section_data.get('section_id'):
            section_id = section_data.get('section_id', '')
            # Try multiple matching strategies
            relevant_scenes = []
            for scene in scenes:
                if (scene.get('chapter_or_act') == section_id or 
                    scene.get('section_id') == section_id or
                    (not scene.get('chapter_or_act') and not scene.get('section_id'))):
                    relevant_scenes.append(scene)
        else:
            relevant_scenes = scenes
        
        scenes_text = ""
        entry_tensions = []
        exit_consequences = []
        physical_actions = []
        micro_actions = []
        sensory_details_list = []
        emotional_beats_list = []
        for scene in relevant_scenes[:20]:  # Increased limit to 20
            scene_id = scene.get('scene_id', '')
            location = scene.get('location', '') or 'Unknown location'
            chars = ', '.join(scene.get('characters_present', [])) if scene.get('characters_present') else 'Unknown characters'
            summary = scene.get('summary', '')
            purpose = scene.get('purpose', '')
            key_dialogue = scene.get('key_dialogue', '')
            entry_tension = scene.get('entry_tension', '')
            exit_consequence = scene.get('exit_consequence', '')
            physical_acts = scene.get('physical_actions', [])
            micro_acts = scene.get('micro_actions', [])
            sensory = scene.get('sensory_details', {})
            emotional_beats = scene.get('emotional_beats', [])
            
            # Include more detail
            scene_detail = f"  - Scene {scene_id} ({location}, {chars}): {summary}"
            if entry_tension:
                scene_detail += f"\n    Entry Tension: {entry_tension}"
                entry_tensions.append(f"Scene {scene_id}: {entry_tension}")
            if exit_consequence:
                scene_detail += f"\n    Exit Consequence: {exit_consequence}"
                exit_consequences.append(f"Scene {scene_id}: {exit_consequence}")
            if purpose:
                scene_detail += f"\n    Purpose: {purpose}"
            if physical_acts:
                scene_detail += f"\n    Physical Actions: {', '.join(physical_acts)}"
                physical_actions.extend([f"Scene {scene_id}: {a}" for a in physical_acts])
            if micro_acts:
                scene_detail += f"\n    Micro-Actions: {', '.join(micro_acts)}"
                micro_actions.extend([f"Scene {scene_id}: {a}" for a in micro_acts])
            if sensory:
                sensory_text = ""
                for sense in ['visual', 'sound', 'smell', 'touch', 'taste']:
                    if sensory.get(sense):
                        sensory_text += f"{sense}: {', '.join(sensory.get(sense, []))}; "
                if sensory_text:
                    scene_detail += f"\n    Sensory: {sensory_text.rstrip('; ')}"
                    sensory_details_list.append(f"Scene {scene_id}: {sensory_text.rstrip('; ')}")
            if emotional_beats:
                beats_text = ', '.join([f"{b.get('emotion', '')} ({b.get('character', '')})" for b in emotional_beats])
                scene_detail += f"\n    Emotional Beats: {beats_text}"
                emotional_beats_list.extend([f"Scene {scene_id}: {beats_text}"])
            
            # Emotional Landing
            landing = scene.get('emotional_landing', {})
            if landing:
                landing_type = landing.get('landing_type', '')
                if landing_type:
                    scene_detail += f"\n    Emotional Landing: {landing_type}"
                if landing.get('new_truth'):
                    scene_detail += f" (New Truth: {landing.get('new_truth')})"
                if landing.get('power_shift'):
                    scene_detail += f" (Power Shift: {landing.get('power_shift')})"
                if landing.get('goal_change'):
                    scene_detail += f" (Goal Change: {landing.get('goal_change')})"
                if landing.get('emotional_turn'):
                    scene_detail += f" (Emotional Turn: {landing.get('emotional_turn')})"
            
            # Sensory Absence
            absence = scene.get('sensory_absence', {})
            if absence:
                if absence.get('what_not_seen'):
                    scene_detail += f"\n    Not Seen: {', '.join(absence.get('what_not_seen', []))}"
                if absence.get('what_not_said'):
                    scene_detail += f"\n    Not Said: {', '.join(absence.get('what_not_said', []))}"
                if absence.get('silence_as_agent'):
                    scene_detail += f"\n    Silence as Agent: Yes"
                if absence.get('obscurity'):
                    scene_detail += f"\n    Obscurity: {', '.join(absence.get('obscurity', []))}"
            if key_dialogue:
                scene_detail += f"\n    Key Dialogue: {key_dialogue}"
            scenes_text += scene_detail + "\n"
        
        vars_dict['scenes'] = scenes_text if scenes_text else 'None'
        vars_dict['entry_tension'] = '\n'.join([f"  - {e}" for e in entry_tensions]) if entry_tensions else 'None'
        vars_dict['exit_consequences'] = '\n'.join([f"  - {e}" for e in exit_consequences]) if exit_consequences else 'None'
        vars_dict['physical_actions'] = '\n'.join([f"  - {a}" for a in physical_actions]) if physical_actions else 'None'
        vars_dict['micro_actions'] = '\n'.join([f"  - {a}" for a in micro_actions]) if micro_actions else 'None'
        vars_dict['sensory_details'] = '\n'.join([f"  - {s}" for s in sensory_details_list]) if sensory_details_list else 'None'
        vars_dict['emotional_beats'] = '\n'.join([f"  - {e}" for e in emotional_beats_list]) if emotional_beats_list else 'None'
    else:
        vars_dict['scenes'] = 'None'
        vars_dict['entry_tension'] = 'None'
        vars_dict['exit_consequences'] = 'None'
        vars_dict['physical_actions'] = 'None'
        vars_dict['micro_actions'] = 'None'
        vars_dict['sensory_details'] = 'None'
        vars_dict['emotional_beats'] = 'None'
    
    # Narrative Flow
    if 'narrative_flow' in blueprint:
        nf = blueprint['narrative_flow']
        vars_dict.update({
            'opening_technique': nf.get('opening_technique', '') or 'None',
            'pacing_pattern': nf.get('pacing_pattern', '') or 'None',
            'climax_position': nf.get('climax_position', '') or 'None',
            'resolution_style': nf.get('resolution_style', '') or 'None',
        })
        # Breathing Room
        breathing_room = nf.get('breathing_room', [])
        if breathing_room:
            breathing_text = '\n'.join([f"  - {br.get('position', '')}: {br.get('description', '') or ''} (purpose: {br.get('purpose', '') or ''})" for br in breathing_room])
            vars_dict['breathing_room'] = breathing_text
        else:
            vars_dict['breathing_room'] = 'None'
        # Emotional Beats (narrative-level)
        narrative_emotional_beats = nf.get('emotional_beats', [])
        if narrative_emotional_beats:
            beats_text = '\n'.join([f"  - {b.get('emotion', '')} at {b.get('position', '')}: {b.get('trigger', '') or ''} ({', '.join(b.get('characters_involved', []))})" for b in narrative_emotional_beats])
            vars_dict['narrative_emotional_beats'] = beats_text
        else:
            vars_dict['narrative_emotional_beats'] = 'None'
        # Tension arc
        tension_arc = nf.get('tension_arc', [])
        if tension_arc and section_data:
            # Find relevant tension point for this section
            section_id = section_data.get('section_id', '')
            # Try to match tension point to section (simplified)
            relevant_tension = tension_arc[0] if tension_arc else None
            if relevant_tension:
                vars_dict['tension_level'] = relevant_tension.get('tension_level', 'medium')
        else:
            vars_dict['tension_level'] = 'medium'
        
        # Emotional Logic
        emotional_logic = nf.get('emotional_logic', {})
        if emotional_logic:
            logic_text = ""
            if emotional_logic.get('emotional_continuity'):
                for ec in emotional_logic.get('emotional_continuity', []):
                    logic_text += f"Emotional Flow: {ec.get('from_scene', '')} → {ec.get('to_scene', '')}: {ec.get('emotional_flow', '')}\n"
            if emotional_logic.get('character_emotional_realism'):
                for cer in emotional_logic.get('character_emotional_realism', []):
                    logic_text += f"Character ({cer.get('character', '')}): {cer.get('consistency', '')}\n"
            if emotional_logic.get('attachment_dynamics'):
                for ad in emotional_logic.get('attachment_dynamics', []):
                    logic_text += f"Attachment ({ad.get('characters', '')}): {ad.get('attachment_type', '')} - {ad.get('development', '')}\n"
            if emotional_logic.get('psychological_patterns'):
                for pp in emotional_logic.get('psychological_patterns', []):
                    chars = ', '.join(pp.get('characters', []))
                    logic_text += f"Pattern ({pp.get('pattern', '')}): {chars}\n"
            vars_dict['emotional_logic'] = logic_text if logic_text else 'None'
        else:
            vars_dict['emotional_logic'] = 'None'
    else:
        vars_dict.update({
            'opening_technique': 'None',
            'pacing_pattern': 'None',
            'climax_position': 'None',
            'resolution_style': 'None',
            'tension_level': 'medium',
            'breathing_room': 'None',
            'narrative_emotional_beats': 'None',
            'emotional_logic': 'None',
        })
    
    # Storytelling Techniques
    if 'storytelling_techniques' in blueprint:
        st = blueprint['storytelling_techniques']
        vars_dict['frame_narrative'] = 'Yes' if st.get('frame_narrative') else 'No'
        vars_dict['unreliable_narrator'] = 'Yes' if st.get('unreliable_narrator') else 'No'
        vars_dict['multiple_perspectives'] = 'Yes' if st.get('multiple_perspectives') else 'No'
    else:
        vars_dict.update({
            'frame_narrative': 'No',
            'unreliable_narrator': 'No',
            'multiple_perspectives': 'No',
        })
    
    # Macro Cohesion
    if 'macro_cohesion' in blueprint:
        mc = blueprint['macro_cohesion']
        # Payoffs to Setups
        payoffs = mc.get('payoffs_to_setups', [])
        if payoffs:
            payoffs_text = '\n'.join([f"  - Setup: {p.get('setup', '')} → Payoff: {p.get('payoff', '')} (at {p.get('position_payoff', '')})" for p in payoffs])
            vars_dict['payoffs_to_setups'] = payoffs_text
        else:
            vars_dict['payoffs_to_setups'] = 'None'
        # Thematic Consistency
        thematic = mc.get('thematic_consistency', [])
        if thematic:
            thematic_text = '\n'.join([f"  - Theme: {t.get('theme', '')} reinforced by {t.get('element', '')} ({t.get('reinforcement', '')})" for t in thematic])
            vars_dict['thematic_consistency'] = thematic_text
        else:
            vars_dict['thematic_consistency'] = 'None'
        # Contrast
        contrast = mc.get('contrast', [])
        if contrast:
            contrast_text = '\n'.join([f"  - {c.get('elements', '')}: {', '.join(c.get('instances', []))} (purpose: {c.get('purpose', '') or ''})" for c in contrast])
            vars_dict['contrast'] = contrast_text
        else:
            vars_dict['contrast'] = 'None'
        # Continuity
        continuity = mc.get('continuity', {})
        if continuity:
            continuity_text = ""
            if continuity.get('logical_consistency'):
                continuity_text += f"Logical: {', '.join(continuity.get('logical_consistency', []))}\n"
            if continuity.get('emotional_consistency'):
                continuity_text += f"Emotional: {', '.join(continuity.get('emotional_consistency', []))}\n"
            if continuity.get('plot_consistency'):
                continuity_text += f"Plot: {', '.join(continuity.get('plot_consistency', []))}\n"
            if continuity.get('character_consistency'):
                continuity_text += f"Character: {', '.join(continuity.get('character_consistency', []))}\n"
            vars_dict['continuity'] = continuity_text if continuity_text else 'None'
        else:
            vars_dict['continuity'] = 'None'
        
        # Logistics & Continuity
        logistics = mc.get('logistics_continuity', {})
        if logistics:
            logistics_text = ""
            if logistics.get('practical_constraints'):
                for pc in logistics.get('practical_constraints', []):
                    logistics_text += f"Constraint ({pc.get('constraint', '')}): {pc.get('impact', '') or ''}\n"
            if logistics.get('geography_limitations'):
                logistics_text += f"Geography Limitations: {', '.join(logistics.get('geography_limitations', []))}\n"
            if logistics.get('causality_mapping'):
                for cm in logistics.get('causality_mapping', []):
                    chain = ' → '.join(cm.get('chain', [])) if cm.get('chain') else ''
                    logistics_text += f"Causality: {cm.get('cause', '')} → {cm.get('effect', '')}"
                    if chain:
                        logistics_text += f" (chain: {chain})"
                    logistics_text += "\n"
            if logistics.get('plot_holes_avoided'):
                logistics_text += f"Plot Holes Avoided: {', '.join(logistics.get('plot_holes_avoided', []))}\n"
            vars_dict['logistics_continuity'] = logistics_text if logistics_text else 'None'
        else:
            vars_dict['logistics_continuity'] = 'None'
    else:
        vars_dict.update({
            'payoffs_to_setups': 'None',
            'thematic_consistency': 'None',
            'contrast': 'None',
            'continuity': 'None',
            'logistics_continuity': 'None',
        })
    
    # Hidden Systems
    if 'hidden_systems' in blueprint:
        hs = blueprint['hidden_systems']
        hidden_text = ""
        if hs.get('audience_secrets'):
            for secret in hs.get('audience_secrets', []):
                hidden_text += f"Audience Secret: {secret.get('secret', '')} (revealed at: {secret.get('revealed_at', 'unknown')})\n"
        if hs.get('character_secrets'):
            for secret in hs.get('character_secrets', []):
                from_whom = ', '.join(secret.get('from_whom', []))
                hidden_text += f"Character Secret ({secret.get('keeper', '')}): {secret.get('secret', '')} (from: {from_whom})\n"
        if hs.get('self_deception'):
            for sd in hs.get('self_deception', []):
                hidden_text += f"Self-Deception ({sd.get('character', '')}): {sd.get('secret', '')}\n"
        vars_dict['hidden_systems'] = hidden_text if hidden_text else 'None'
    else:
        vars_dict['hidden_systems'] = 'None'
    
    # Quotes - use section-specific if provided, filter out already-used quotes
    if section_data and section_data.get('section_quotes'):
        quotes_list = section_data['section_quotes']
    else:
        # Try both quotes_and_anecdotes (business plans/reports) and quotes_and_dialogue (narrative fiction)
        quotes_list = blueprint.get('quotes_and_anecdotes', []) or blueprint.get('quotes_and_dialogue', [])
    
    # For narrative fiction, filter quotes by section/scene context and conversation participants
    if section_data and 'quotes_and_dialogue' in blueprint:
        section_id = section_data.get('section_id', '')
        scene_id = section_data.get('scene_id', '')
        # Filter quotes relevant to this section/scene
        relevant_quotes = []
        for quote in quotes_list:
            quote_section_id = quote.get('section_id')
            quote_scene_id = quote.get('scene_id')
            # Match by section_id or scene_id
            if (quote_section_id and section_id and quote_section_id == section_id) or \
               (quote_scene_id and scene_id and quote_scene_id == scene_id) or \
               (not section_id and not scene_id):  # If no section/scene specified, include all
                relevant_quotes.append(quote)
        quotes_list = relevant_quotes if relevant_quotes else quotes_list
    
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
            # Format quotes with full contextual information for narrative fiction
            quotes_text = ""
            for q in unused_quotes[:50]:  # Limit to 50 to avoid token overflow
                quote_text = q.get('text', '')
                speaker = q.get('speaker')
                recipient = q.get('recipient')
                conversation_participants = q.get('conversation_participants', [])
                context = q.get('context', '')
                conversation_context = q.get('conversation_context', '')
                subtext = q.get('subtext', '')
                has_silence = q.get('has_silence_or_pause', False)
                significance = q.get('significance', '')
                scene_id = q.get('scene_id')
                section_id = q.get('section_id')
                
                quote_entry = f"  - \"{quote_text}\""
                if speaker:
                    quote_entry += f"\n    Speaker: {speaker}"
                if recipient:
                    quote_entry += f"\n    Addressed to: {recipient}"
                if conversation_participants:
                    participants_str = ', '.join(conversation_participants)
                    quote_entry += f"\n    Conversation participants: {participants_str}"
                if conversation_context:
                    quote_entry += f"\n    Conversation topic: {conversation_context}"
                if subtext:
                    quote_entry += f"\n    Subtext: {subtext}"
                if has_silence:
                    quote_entry += f"\n    Has meaningful silence/pause: Yes"
                if context:
                    quote_entry += f"\n    Narrative context: {context}"
                if scene_id:
                    quote_entry += f"\n    Scene: {scene_id}"
                if section_id:
                    quote_entry += f"\n    Section: {section_id}"
                if significance:
                    quote_entry += f"\n    Significance: {significance}"
                quotes_text += quote_entry + "\n"
            
            vars_dict['quotes'] = quotes_text if quotes_text else 'None'
            # Extract subtext and silences separately for template
            subtexts = [q.get('subtext', '') for q in unused_quotes[:50] if q.get('subtext')]
            silences = [q.get('text', '')[:50] for q in unused_quotes[:50] if q.get('has_silence_or_pause')]
            vars_dict['subtext'] = '\n'.join([f"  - {s}" for s in subtexts]) if subtexts else 'None'
            vars_dict['silences_pauses'] = '\n'.join([f"  - \"{s}...\"" for s in silences]) if silences else 'None'
        else:
            vars_dict['quotes'] = 'None (all relevant quotes already used in other sections)'
            vars_dict['subtext'] = 'None'
            vars_dict['silences_pauses'] = 'None'
    else:
        vars_dict['quotes'] = 'None'
        vars_dict['subtext'] = 'None'
        vars_dict['silences_pauses'] = 'None'
    
    # Tone Metadata - filter out already-used key phrases
    if 'tone_metadata' in blueprint:
        tone = blueprint['tone_metadata']
        all_key_phrases = tone.get('key_phrases', [])
        # Filter out already-used phrases
        unused_phrases = [p for p in all_key_phrases if p not in used_content['key_phrases']]
        # Mark some as used (but keep a few for later sections)
        for phrase in unused_phrases[:2]:  # Use 2 phrases per section
            used_content['key_phrases'].add(phrase)
        
        # Check if this is narrative fiction (has story_overview) or business/report (has urgency_level)
        if 'story_overview' in blueprint:
            # Narrative fiction uses overall_tone and mood, but also provide urgency/formality for compatibility
            vars_dict.update({
                'style': tone.get('style', 'narrative prose'),
                'overall_tone': tone.get('overall_tone', '') or 'None',
                'mood': tone.get('mood', '') or 'None',
                'urgency': 'medium',  # Default for narrative fiction
                'formality': tone.get('formality', '') or 'None',
                'key_phrases': ', '.join(unused_phrases[:3]) or 'None',  # Show up to 3 unused phrases
            })
        else:
            # Business plans/reports use urgency_level and formality
            vars_dict.update({
                'style': tone.get('style', 'academic paper'),
                'urgency': tone.get('urgency_level', 'medium'),
                'formality': tone.get('formality', 'formal'),
                'overall_tone': 'None',  # For compatibility
                'mood': 'None',  # For compatibility
                'key_phrases': ', '.join(unused_phrases[:3]) or 'None',  # Show up to 3 unused phrases
            })
    else:
        # Default based on document type
        if 'story_overview' in blueprint:
            vars_dict.update({
                'style': 'narrative prose',
                'overall_tone': 'None',
                'mood': 'None',
                'urgency': 'medium',
                'formality': 'None',
                'key_phrases': 'None',
            })
        else:
            vars_dict.update({
                'style': 'academic paper',
                'urgency': 'medium',
                'formality': 'formal',
                'overall_tone': 'None',
                'mood': 'None',
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
        # Include full content AND extract quote markers to help prevent repetition
        prev_sections_text = "\n\n".join([
            f"## {i+1}. Previously Generated Section:\n{section}" 
            for i, section in enumerate(previously_generated_sections)
        ])
        
        # Extract quote markers from previously generated sections to help prevent repetition
        quote_markers = []
        if 'quotes_and_dialogue' in blueprint:
            quotes = blueprint.get('quotes_and_dialogue', [])
            # Get quotes that are marked as section markers or are distinctive
            for quote in quotes[:20]:  # Limit to 20 most relevant
                quote_text = quote.get('text', '')
                function = quote.get('function', '')
                if quote_text and (function == 'section_marker' or len(quote_text) > 20):
                    # Check if this quote appears in previously generated sections
                    for prev_section in previously_generated_sections:
                        if quote_text[:50].lower() in prev_section.lower():
                            quote_markers.append(f"  - \"{quote_text[:100]}...\" (already used)")
                            break
        
        if quote_markers:
            prev_sections_text += f"\n\n**QUOTE MARKERS ALREADY USED** (do NOT repeat these):\n" + "\n".join(quote_markers[:10])
        
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


def validate_plot_structure(blueprint: Dict[str, Any], prompt_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Validate plot structure for narrative fiction before reinflation.
    Checks for critical plot elements and returns validation report.
    """
    validation_report = {
        'is_valid': True,
        'warnings': [],
        'missing_elements': [],
        'critical_elements_found': []
    }
    
    # Check if this is narrative fiction - check prompt_path or blueprint structure
    is_narrative_fiction = False
    if prompt_path and 'narrative_fiction' in str(prompt_path):
        is_narrative_fiction = True
    elif blueprint.get('story_overview') or blueprint.get('plot_structure'):
        # Has narrative fiction structure
        is_narrative_fiction = True
    
    if not is_narrative_fiction:
        return validation_report  # Skip validation for non-fiction
    
    plot_structure = blueprint.get('plot_structure', {})
    setting = blueprint.get('setting', {})
    scenes = blueprint.get('scenes', [])
    
    # Critical elements to check for (based on "The Philosopher's Joke" analysis)
    critical_keywords = {
        'potion': ['potion', 'drink', 'goblet', 'wine-cup', 'chemical', 'magical'],
        'goblet': ['goblet', 'wine-cup', 'glass', 'bavarian', 'broken', 'fragment'],
        'philosopher': ['philosopher', 'kant', 'figure', 'gentleman', 'mysterious'],
        'location': ['konigsberg', 'kneiper', 'inn', 'speise saal'],
        'time_reversal': ['twenty years', '20 years', 'back in time', 'time shift', 'future knowledge'],
        'evidence': ['broken', 'fragment', 'proof', 'evidence', 'goblet']
    }
    
    # Check inciting incident
    inciting_incident = plot_structure.get('inciting_incident', '') or ''
    if inciting_incident:
        validation_report['critical_elements_found'].append(f"Inciting incident: {inciting_incident[:100]}")
        # Check for potion/philosopher in inciting incident
        incident_lower = inciting_incident.lower()
        if any(kw in incident_lower for kw in critical_keywords['potion']):
            validation_report['critical_elements_found'].append("✓ Potion mechanism mentioned in inciting incident")
        if any(kw in incident_lower for kw in critical_keywords['philosopher']):
            validation_report['critical_elements_found'].append("✓ Philosopher figure mentioned in inciting incident")
    else:
        validation_report['missing_elements'].append("Inciting incident is missing or empty")
        validation_report['is_valid'] = False
    
    # Check climax
    climax = plot_structure.get('climax', '') or ''
    if climax:
        validation_report['critical_elements_found'].append(f"Climax: {climax[:100]}")
        climax_lower = climax.lower()
        if any(kw in climax_lower for kw in critical_keywords['goblet'] + critical_keywords['evidence']):
            validation_report['critical_elements_found'].append("✓ Goblet/evidence mentioned in climax")
    else:
        validation_report['missing_elements'].append("Climax is missing or empty")
        validation_report['is_valid'] = False
    
    # Check key turning points
    key_turning_points = plot_structure.get('key_turning_points', [])
    if key_turning_points:
        validation_report['critical_elements_found'].append(f"Found {len(key_turning_points)} key turning points")
        # Check if potion/goblet mentioned in turning points
        turning_points_text = ' '.join([str(tp) for tp in key_turning_points]).lower()
        if any(kw in turning_points_text for kw in critical_keywords['potion']):
            validation_report['critical_elements_found'].append("✓ Potion mentioned in key turning points")
        if any(kw in turning_points_text for kw in critical_keywords['goblet']):
            validation_report['critical_elements_found'].append("✓ Goblet mentioned in key turning points")
    else:
        validation_report['warnings'].append("No key turning points found")
    
    # Check physical objects in setting
    physical_objects = setting.get('physical_objects_and_props', [])
    if physical_objects:
        validation_report['critical_elements_found'].append(f"Found {len(physical_objects)} physical objects/props")
        objects_text = ' '.join([str(obj) for obj in physical_objects]).lower()
        if any(kw in objects_text for kw in critical_keywords['goblet']):
            validation_report['critical_elements_found'].append("✓ Goblet found in physical objects")
    else:
        validation_report['warnings'].append("No physical objects/props extracted")
    
    # Check scenes for critical elements
    if scenes:
        validation_report['critical_elements_found'].append(f"Found {len(scenes)} scenes")
        # Check if any scene mentions potion/goblet
        scenes_with_potion = 0
        scenes_with_goblet = 0
        scenes_with_location = 0
        for scene in scenes:
            scene_text = ' '.join([
                str(scene.get('summary', '')),
                str(scene.get('purpose', '')),
                str(scene.get('location', ''))
            ]).lower()
            if any(kw in scene_text for kw in critical_keywords['potion']):
                scenes_with_potion += 1
            if any(kw in scene_text for kw in critical_keywords['goblet']):
                scenes_with_goblet += 1
            if any(kw in scene_text for kw in critical_keywords['location']):
                scenes_with_location += 1
        
        if scenes_with_potion > 0:
            validation_report['critical_elements_found'].append(f"✓ Potion mentioned in {scenes_with_potion} scene(s)")
        else:
            validation_report['warnings'].append("Potion not found in any scene summaries")
        
        if scenes_with_goblet > 0:
            validation_report['critical_elements_found'].append(f"✓ Goblet mentioned in {scenes_with_goblet} scene(s)")
        else:
            validation_report['warnings'].append("Goblet not found in any scene summaries")
        
        if scenes_with_location > 0:
            validation_report['critical_elements_found'].append(f"✓ Konigsberg/Kneiper mentioned in {scenes_with_location} scene(s)")
    else:
        validation_report['warnings'].append("No scenes extracted")
    
    return validation_report


def reinflate_document(
    blueprint: Dict[str, Any],
    prompt_path: Path,
    run_timestamp: str,
    run_output_dir: Path,
    logging_service: Optional[Any] = None,  # Optional logging service for metrics
    checkpoint_path: Optional[Path] = None,  # Optional checkpoint path for resuming
    completed_sections: Optional[List[str]] = None  # Optional list of already completed sections
) -> Path:
    """
    Reinflate complete document from blueprint.
    Uses templates from prompt.json to determine structure.
    """
    print("\n" + "=" * 60)
    print("Reinflating Document from Blueprint")
    print("=" * 60)
    
    # Validate plot structure and title before reinflation (for narrative fiction)
    if 'narrative_fiction' in str(prompt_path) or blueprint.get('story_overview') or blueprint.get('plot_structure'):
        print("\n[Validation] Checking plot structure and critical metadata...")
        validation_report = validate_plot_structure(blueprint, prompt_path)
        
        # Validate title preservation
        story_overview = blueprint.get('story_overview', {})
        extracted_title = story_overview.get('title', '')
        if extracted_title:
            print(f"  [OK] Extracted title: \"{extracted_title}\"")
            # Store for later validation during reinflation
            validation_report['extracted_title'] = extracted_title
        else:
            print("  [WARNING] No title found in story_overview")
            validation_report['warnings'].append("No title extracted - reinflation may invent a title")
        
        if validation_report['critical_elements_found']:
            print("  [OK] Critical plot elements found:")
            for element in validation_report['critical_elements_found'][:5]:  # Show first 5
                print(f"    - {element}")
            if len(validation_report['critical_elements_found']) > 5:
                print(f"    ... and {len(validation_report['critical_elements_found']) - 5} more")
        
        if validation_report['warnings']:
            print("  [WARNING] Plot structure warnings:")
            for warning in validation_report['warnings']:
                print(f"    - {warning}")
        
        if validation_report['missing_elements']:
            print("  [ERROR] Missing critical plot elements:")
            for missing in validation_report['missing_elements']:
                print(f"    - {missing}")
            print("  [WARNING] Reinflation may be incomplete due to missing plot elements")
        
        # Don't save validation report - it's not needed
        # validation_path = run_output_dir / f"plot_validation_{run_timestamp}.json"
        # try:
        #     with open(validation_path, 'w', encoding='utf-8') as f:
        #         json.dump(validation_report, f, indent=2)
        #     print(f"  [OK] Validation report saved to: {validation_path.name}")
        # except Exception as e:
        #     print(f"  [WARNING] Could not save validation report: {e}")
    
    # Initialize completed sections list if resuming
    if completed_sections is None:
        completed_sections = []
    
    # Checkpoint helper functions
    def save_reinflation_checkpoint(checkpoint_path: Path, sections: List[str], completed_sections: List[str], blueprint: Dict[str, Any]) -> None:
        """Save checkpoint for reinflation."""
        if checkpoint_path:
            checkpoint_data = {
                "sections": sections,
                "completed_sections": completed_sections,
                "blueprint": blueprint,
                "checkpoint_time": datetime.now().isoformat()
            }
            try:
                with open(checkpoint_path, "w", encoding="utf-8") as f:
                    json.dump(checkpoint_data, f, indent=2)
                print(f"  [CHECKPOINT] Saved reinflation checkpoint: {checkpoint_path.name}")
            except Exception as e:
                print(f"  [WARNING] Failed to save checkpoint: {e}")
    
    def load_reinflation_checkpoint(checkpoint_path: Path) -> Optional[Dict[str, Any]]:
        """Load checkpoint for reinflation."""
        if checkpoint_path and checkpoint_path.exists():
            try:
                with open(checkpoint_path, "r", encoding="utf-8") as f:
                    checkpoint = json.load(f)
                print(f"  [CHECKPOINT] Loaded reinflation checkpoint: {checkpoint_path.name}")
                return checkpoint
            except Exception as e:
                print(f"  [WARNING] Failed to load checkpoint: {e}")
        return None
    
    # Load checkpoint if resuming
    checkpoint_data = None
    if checkpoint_path and checkpoint_path.exists():
        checkpoint_data = load_reinflation_checkpoint(checkpoint_path)
        if checkpoint_data:
            sections = checkpoint_data.get("sections", [])
            completed_sections = checkpoint_data.get("completed_sections", [])
            print(f"  [RESUME] Resuming reinflation with {len(completed_sections)} completed sections")
    
    try:
        if not checkpoint_data:
            sections = []
        
        # Extract title - MUST use exact title from blueprint, no changes
        title = "Document"
        structure = blueprint.get('document_structure', {})
        title_page = structure.get('title_page', {})
        if title_page.get('title'):
            title = title_page['title']
        elif 'story_overview' in blueprint:
            title = blueprint['story_overview'].get('title', 'Document')
            # CRITICAL: Use exact title, do not modify
            if not title or title == 'Document':
                # Try to get from validation report if available
                pass
        elif 'executive_summary' in blueprint:
            title = blueprint['executive_summary'].get('overview', 'Document')[:80]
        
        # Store original title for validation
        original_title = title
        
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
            if "Introduction" not in completed_sections:
                try:
                    print("\n[Reinflation] Generating introduction...")
                    intro = reinflate_section(
                        "Introduction", 
                        blueprint, 
                        prompt_path, 
                        run_timestamp,
                        temperature=0.4,
                        used_content=used_content,
                        logging_service=logging_service
                    )
                    if intro and not intro.startswith("<!--"):
                        sections.append(intro)
                        completed_sections.append("Introduction")
                        print("  [OK] Introduction generated")
                        # Save checkpoint
                        if checkpoint_path:
                            save_reinflation_checkpoint(checkpoint_path, sections, completed_sections, blueprint)
                except Exception as e:
                    print(f"  [ERROR] Introduction failed: {e}")
            else:
                print("\n[Reinflation] Skipping Introduction (already completed)")
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
                    # Try both quotes_and_anecdotes (business plans/reports) and quotes_and_dialogue (narrative fiction)
                    quotes_source = blueprint.get('quotes_and_anecdotes', []) or blueprint.get('quotes_and_dialogue', [])
                    if quotes_source:
                        section_id = section.get('id', '')
                        for quote in quotes_source:
                            if quote.get('section_id') == section_id or quote.get('chapter_id') == section_id or quote.get('scene_id') or not quote.get('section_id'):
                                section_quotes.append(quote)
                    
                    # Add section-specific quote filtering to section_data
                    section_data['section_quotes'] = section_quotes[:5]  # Limit to 5 quotes per section
                    
                    # For narrative fiction, also filter characters by section
                    if 'characters' in blueprint:
                        section_id = section.get('id', '')
                        # Find characters that appear in this section's scenes or quotes
                        relevant_char_names = set()
                        scenes = blueprint.get('scenes', [])
                        for scene in scenes:
                            if scene.get('chapter_or_act') == section_id:
                                relevant_char_names.update(scene.get('characters_present', []))
                        for quote in section_quotes:
                            speaker = quote.get('speaker')
                            if speaker:
                                relevant_char_names.add(speaker)
                        
                        # Format relevant characters
                        if relevant_char_names:
                            relevant_chars = [c for c in blueprint['characters'] if c.get('name') in relevant_char_names]
                            chars_text = ""
                            for char in relevant_chars:
                                name = char.get('name', '')
                                role = char.get('role', '')
                                desc = char.get('description', '') or ''
                                chars_text += f"  - {name} ({role}): {desc}\n"
                            section_data['relevant_characters'] = chars_text if chars_text else 'None'
                        else:
                            section_data['relevant_characters'] = 'None'
                    else:
                        section_data['relevant_characters'] = 'None'
                    
                    # Pass used_content and previously_generated to track what's been used
                    body_content = reinflate_section(
                        "Body Sections", 
                        blueprint, 
                        prompt_path, 
                        run_timestamp, 
                        section_data,
                        temperature=0.4,  # Balanced temperature
                        used_content=used_content,  # Track used content
                        previously_generated_sections=previously_generated,  # Pass previously generated sections
                        logging_service=logging_service
                    )
                    if body_content and not body_content.startswith("<!--"):
                        sections.append(body_content)
                        section_id = section.get('id', section.get('title', ''))
                        completed_sections.append(f"Body_{section_id}")
                        # Add to previously generated list (keep more sections for narrative fiction to prevent repetition)
                        # For narrative fiction, keep more context to prevent retellings
                        is_narrative_fiction = 'narrative_fiction' in str(prompt_path) or blueprint.get('story_overview')
                        max_prev_sections = 10 if is_narrative_fiction else 5
                        previously_generated.append(body_content)
                        if len(previously_generated) > max_prev_sections:
                            previously_generated.pop(0)  # Keep only last N sections
                        section_counter += 1  # Increment for next section
                        print(f"  [OK] Section '{section.get('title', '')}' generated (numbered as {section_numbering})")
                        # Save checkpoint after each section
                        if checkpoint_path:
                            save_reinflation_checkpoint(checkpoint_path, sections, completed_sections, blueprint)
                    else:
                        # Debug: why was section skipped?
                        if not body_content:
                            print(f"  [WARNING] Section '{section.get('title', '')}' returned empty content")
                        elif body_content.startswith("<!--"):
                            print(f"  [WARNING] Section '{section.get('title', '')}' returned error: {body_content[:200]}")
                    time.sleep(0.5)  # Rate limiting
            else:
                # No sections, try generic body template
                body = reinflate_section("Body Sections", blueprint, prompt_path, run_timestamp, previously_generated_sections=[], logging_service=logging_service)
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
            if "Conclusion" not in completed_sections:
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
                        previously_generated_sections=conclusion_previously_generated[-5:] if conclusion_previously_generated else [],  # Last 5 sections
                        logging_service=logging_service
                    )
                    if conclusion and not conclusion.startswith("<!--"):
                        sections.append(conclusion)
                        completed_sections.append("Conclusion")
                        print("  [OK] Conclusion generated")
                        # Save checkpoint
                        if checkpoint_path:
                            save_reinflation_checkpoint(checkpoint_path, sections, completed_sections, blueprint)
                except Exception as e:
                    print(f"  [ERROR] Conclusion failed: {e}")
            else:
                print("\n[Reinflation] Skipping Conclusion (already completed)")
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
                        used_content=None,
                        logging_service=logging_service
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
        
        # Validate title preservation (for narrative fiction)
        if 'narrative_fiction' in str(prompt_path) or blueprint.get('story_overview'):
            story_overview = blueprint.get('story_overview', {})
            expected_title = story_overview.get('title', '')
            if expected_title:
                # Check if title appears correctly in reinflated content
                title_found = False
                # Look for title in first few lines (after markdown headers)
                first_lines = reinflated_content.split('\n')[:20]
                for line in first_lines:
                    # Remove markdown formatting
                    clean_line = line.replace('#', '').replace('*', '').strip()
                    if expected_title.lower() in clean_line.lower() or clean_line.lower() in expected_title.lower():
                        title_found = True
                        break
                
                if not title_found:
                    print(f"\n  [WARNING] Title validation: Expected title \"{expected_title}\" not found in reinflated document")
                    print(f"  [WARNING] First line of reinflated: {first_lines[0] if first_lines else 'N/A'}")
                else:
                    print(f"\n  [OK] Title validation: Expected title \"{expected_title}\" found in reinflated document")
        
        # Save reinflated markdown
        reinflated_path = run_output_dir / f"reinflated_{run_timestamp}.md"
        with open(reinflated_path, "w", encoding="utf-8") as f:
            f.write(reinflated_content)
        
        print(f"\n[OK] Reinflated document saved to: {reinflated_path}")
        
        # Clean up checkpoint file on successful completion
        if checkpoint_path and checkpoint_path.exists():
            try:
                checkpoint_path.unlink()
                print(f"  [CHECKPOINT] Removed checkpoint file (reinflation completed successfully)")
            except Exception as e:
                print(f"  [WARNING] Failed to remove checkpoint: {e}")
        
        return reinflated_path
        
    except Exception as e:
        print(f"\n[ERROR] Reinflation failed: {e}")
        import traceback
        traceback.print_exc()
        raise


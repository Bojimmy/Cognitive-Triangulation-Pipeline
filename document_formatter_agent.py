
#!/usr/bin/env python3
"""
Document Formatter X-Agent
Formats documents to match system requirements and adds valid keywords
"""

import re
from typing import Dict, List, Any, Optional
from abc import ABC
import logging

logger = logging.getLogger(__name__)

class DocumentFormatterXAgent:
    """Formats documents to system standards with valid keywords"""
    
    def __init__(self):
        self.agent_type = "DocumentFormatterXAgent"
        self.keyword_patterns = {
            'requirements': r'REQ-(\d+)[:\s]+(.*?)(?=\n|REQ-|\Z)',
            'stakeholders': r'(?:stakeholder|user|client|customer)[s]?[:\s]+(.*?)(?=\n|\Z)',
            'constraints': r'(?:constraint|limitation|restriction)[s]?[:\s]+(.*?)(?=\n|\Z)',
            'objectives': r'(?:objective|goal|purpose)[s]?[:\s]+(.*?)(?=\n|\Z)'
        }
        
        # Domain-specific keyword mappings
        self.domain_keywords = {
            'real_estate': ['property', 'listing', 'mls', 'realtor', 'lease', 'tenant', 'rental'],
            'customer_support': ['ticket', 'helpdesk', 'agent', 'escalation', 'support'],
            'healthcare': ['patient', 'medical', 'diagnosis', 'treatment', 'clinical'],
            'fintech': ['payment', 'transaction', 'banking', 'financial', 'compliance'],
            'ecommerce': ['product', 'cart', 'checkout', 'inventory', 'order'],
            'mobile_app': ['mobile', 'app', 'android', 'ios', 'push notification']
        }
    
    def format_document(self, raw_content: str, target_domain: str = None) -> Dict[str, Any]:
        """Format document to system standards"""
        logger.info(f"[Document Formatter] Processing document for domain: {target_domain}")
        
        # Clean and normalize content
        cleaned_content = self._clean_content(raw_content)
        
        # Extract structured components
        components = self._extract_components(cleaned_content)
        
        # Add domain-specific keywords
        if target_domain:
            components = self._enhance_with_domain_keywords(components, target_domain)
        
        # Format requirements
        formatted_requirements = self._format_requirements(components['requirements'])
        
        # Generate standardized document
        formatted_doc = self._generate_formatted_document(
            components, formatted_requirements, target_domain
        )
        
        return {
            'formatted_content': formatted_doc,
            'extracted_requirements': formatted_requirements,
            'identified_domain': target_domain,
            'stakeholders': components['stakeholders'],
            'validation_score': self._calculate_validation_score(formatted_doc)
        }
    
    def _clean_content(self, content: str) -> str:
        """Clean and normalize document content"""
        # Remove extra whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Standardize line breaks
        content = re.sub(r'\n\s*\n', '\n\n', content)
        
        # Fix common formatting issues
        content = re.sub(r'([.!?])\s*([A-Z])', r'\1\n\n\2', content)
        
        return content.strip()
    
    def _extract_components(self, content: str) -> Dict[str, List[str]]:
        """Extract key components from document"""
        components = {
            'requirements': [],
            'stakeholders': [],
            'constraints': [],
            'objectives': []
        }
        
        for component_type, pattern in self.keyword_patterns.items():
            matches = re.finditer(pattern, content, re.IGNORECASE | re.DOTALL)
            for match in matches:
                if component_type == 'requirements':
                    req_text = match.group(2).strip()
                    components[component_type].append({
                        'id': f"REQ-{match.group(1).zfill(3)}",
                        'text': req_text,
                        'priority': self._detect_priority(req_text)
                    })
                else:
                    components[component_type].append(match.group(1).strip())
        
        # If no explicit requirements found, extract implicit ones
        if not components['requirements']:
            components['requirements'] = self._extract_implicit_requirements(content)
        
        return components
    
    def _extract_implicit_requirements(self, content: str) -> List[Dict[str, str]]:
        """Extract implicit requirements from unstructured text"""
        requirements = []
        content_lower = content.lower()
        
        # Common requirement patterns
        patterns = [
            (r'need[s]?\s+(?:to\s+)?([^.!?]+)', 'high'),
            (r'(?:should|must|shall)\s+([^.!?]+)', 'high'),
            (r'want[s]?\s+(?:to\s+)?([^.!?]+)', 'medium'),
            (r'require[s]?\s+([^.!?]+)', 'high'),
            (r'(?:feature|functionality)[:\s]+([^.!?]+)', 'medium')
        ]
        
        req_id = 1
        for pattern, priority in patterns:
            matches = re.finditer(pattern, content_lower)
            for match in matches:
                req_text = match.group(1).strip()
                if len(req_text) > 10 and len(req_text) < 100:  # Reasonable length
                    requirements.append({
                        'id': f"REQ-{req_id:03d}",
                        'text': req_text.capitalize(),
                        'priority': priority
                    })
                    req_id += 1
        
        return requirements[:8]  # Limit to 8 requirements
    
    def _detect_priority(self, text: str) -> str:
        """Detect priority from requirement text"""
        high_priority_words = ['critical', 'must', 'essential', 'required', 'mandatory']
        low_priority_words = ['nice', 'optional', 'future', 'enhancement']
        
        text_lower = text.lower()
        
        if any(word in text_lower for word in high_priority_words):
            return 'high'
        elif any(word in text_lower for word in low_priority_words):
            return 'low'
        else:
            return 'medium'
    
    def _enhance_with_domain_keywords(self, components: Dict, domain: str) -> Dict:
        """Add domain-specific keywords to components"""
        if domain in self.domain_keywords:
            keywords = self.domain_keywords[domain]
            
            # Enhance requirements with domain context
            for req in components['requirements']:
                req_text = req['text'].lower()
                matching_keywords = [kw for kw in keywords if kw in req_text]
                if matching_keywords:
                    req['domain_keywords'] = matching_keywords
        
        return components
    
    def _format_requirements(self, requirements: List[Dict]) -> List[Dict]:
        """Format requirements with proper structure"""
        formatted = []
        
        for i, req in enumerate(requirements, 1):
            formatted.append({
                'id': req.get('id', f"REQ-{i:03d}"),
                'title': req['text'][:80] + ('...' if len(req['text']) > 80 else ''),
                'description': req['text'],
                'priority': req.get('priority', 'medium'),
                'category': 'functional',
                'domain_keywords': req.get('domain_keywords', [])
            })
        
        return formatted
    
    def _generate_formatted_document(self, components: Dict, requirements: List[Dict], domain: str) -> str:
        """Generate standardized document format"""
        doc_parts = []
        
        # Header
        doc_parts.append("# SYSTEM-FORMATTED PROJECT DOCUMENT")
        doc_parts.append("=" * 50)
        
        # Domain classification
        if domain:
            doc_parts.append(f"\n**PROJECT DOMAIN:** {domain.upper()}")
        
        # Objectives
        if components['objectives']:
            doc_parts.append("\n## PROJECT OBJECTIVES")
            for obj in components['objectives']:
                doc_parts.append(f"- {obj}")
        
        # Requirements section
        doc_parts.append("\n## FUNCTIONAL REQUIREMENTS")
        for req in requirements:
            priority_icon = "🔥" if req['priority'] == 'high' else "📝" if req['priority'] == 'medium' else "💡"
            doc_parts.append(f"{priority_icon} **{req['id']}:** {req['title']}")
            if req['domain_keywords']:
                doc_parts.append(f"   *Keywords: {', '.join(req['domain_keywords'])}*")
        
        # Stakeholders
        if components['stakeholders']:
            doc_parts.append("\n## STAKEHOLDERS")
            for stakeholder in components['stakeholders']:
                doc_parts.append(f"- {stakeholder}")
        
        # Constraints
        if components['constraints']:
            doc_parts.append("\n## CONSTRAINTS & LIMITATIONS")
            for constraint in components['constraints']:
                doc_parts.append(f"- {constraint}")
        
        # System recommendations
        doc_parts.append("\n## SYSTEM RECOMMENDATIONS")
        doc_parts.append("- Use modular architecture for scalability")
        doc_parts.append("- Implement comprehensive error handling")
        doc_parts.append("- Follow security best practices")
        doc_parts.append("- Include automated testing framework")
        
        return '\n'.join(doc_parts)
    
    def _calculate_validation_score(self, formatted_doc: str) -> float:
        """Calculate document validation score"""
        score = 0.0
        max_score = 100.0
        
        # Check for structured requirements
        req_matches = len(re.findall(r'REQ-\d+', formatted_doc))
        score += min(req_matches * 15, 60)  # Up to 60 points for requirements
        
        # Check for stakeholders section
        if '## STAKEHOLDERS' in formatted_doc:
            score += 15
        
        # Check for domain keywords
        if 'Keywords:' in formatted_doc:
            score += 15
        
        # Check for constraints
        if '## CONSTRAINTS' in formatted_doc:
            score += 10
        
        return min(score, max_score)


#!/usr/bin/env python3
"""
Domain Plugin Creator X-Agent
Creates domain plugins for the X-Agent system (backend only)
"""

import re
import os
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class DomainPluginCreatorXAgent:
    """Creates domain-specific plugins for the X-Agent system"""
    
    def __init__(self):
        self.agent_type = "DomainPluginCreatorXAgent"
        self.plugin_template = self._get_plugin_template()
        
    def create_domain_plugin(self, domain_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new domain plugin from specification"""
        logger.info(f"[Plugin Creator] Creating plugin for domain: {domain_spec.get('domain_name')}")
        
        # Validate specification
        validation_result = self._validate_domain_spec(domain_spec)
        if not validation_result['valid']:
            return {
                'success': False,
                'error': validation_result['errors'],
                'plugin_code': None
            }
        
        # Generate plugin code
        plugin_code = self._generate_plugin_code(domain_spec)
        
        # Create plugin file
        file_path = self._create_plugin_file(domain_spec['domain_name'], plugin_code)
        
        # Register with system
        registration_result = self._register_plugin(domain_spec['domain_name'])
        
        return {
            'success': True,
            'domain_name': domain_spec['domain_name'],
            'file_path': file_path,
            'plugin_code': plugin_code,
            'registered': registration_result,
            'analysis': self._analyze_plugin_quality(domain_spec)
        }
    
    def analyze_content_for_plugin(self, content: str) -> Dict[str, Any]:
        """Analyze content to suggest domain plugin structure"""
        logger.info("[Plugin Creator] Analyzing content for plugin suggestions")
        
        # Extract domain characteristics
        domain_analysis = self._analyze_domain_characteristics(content)
        
        # Suggest plugin structure
        plugin_suggestion = {
            'domain_name': domain_analysis['suggested_domain'],
            'keywords': domain_analysis['key_terms'],
            'priority_score': domain_analysis['specificity_score'],
            'requirements_patterns': domain_analysis['requirement_patterns'],
            'stakeholders': domain_analysis['stakeholders'],
            'cross_cutting_concerns': domain_analysis['cross_cutting']
        }
        
        return {
            'analysis': domain_analysis,
            'suggested_plugin': plugin_suggestion,
            'confidence': domain_analysis['confidence']
        }
    
    def _validate_domain_spec(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Validate domain specification"""
        errors = []
        required_fields = ['domain_name', 'keywords', 'requirements_patterns']
        
        for field in required_fields:
            if field not in spec or not spec[field]:
                errors.append(f"Missing required field: {field}")
        
        # Validate domain name format
        if 'domain_name' in spec:
            if not re.match(r'^[a-z_]+$', spec['domain_name']):
                errors.append("Domain name must be lowercase with underscores only")
        
        # Validate keywords
        if 'keywords' in spec and isinstance(spec['keywords'], list):
            if len(spec['keywords']) < 3:
                errors.append("Must have at least 3 keywords")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def _analyze_domain_characteristics(self, content: str) -> Dict[str, Any]:
        """Analyze content to identify domain characteristics"""
        content_lower = content.lower()
        
        # Define domain patterns
        domain_patterns = {
            'healthcare': ['patient', 'medical', 'diagnosis', 'treatment', 'clinical', 'hospital'],
            'finance': ['payment', 'transaction', 'banking', 'loan', 'credit', 'investment'],
            'education': ['student', 'course', 'curriculum', 'grade', 'assignment', 'learning'],
            'retail': ['product', 'inventory', 'sales', 'customer', 'order', 'shipping'],
            'manufacturing': ['production', 'quality', 'supply chain', 'machinery', 'assembly'],
            'logistics': ['shipping', 'delivery', 'warehouse', 'tracking', 'fleet', 'route'],
            'gaming': ['player', 'level', 'score', 'achievement', 'multiplayer', 'game'],
            'social_media': ['user', 'post', 'feed', 'like', 'share', 'comment', 'profile']
        }
        
        # Score each domain
        domain_scores = {}
        for domain, keywords in domain_patterns.items():
            score = sum(1 for keyword in keywords if keyword in content_lower)
            if score > 0:
                domain_scores[domain] = score / len(keywords)
        
        # Find best matching domain
        best_domain = max(domain_scores.items(), key=lambda x: x[1]) if domain_scores else ('custom', 0.0)
        
        # Extract key terms
        words = re.findall(r'\b[a-z]{3,}\b', content_lower)
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get most frequent domain-relevant terms
        key_terms = [word for word, freq in sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]]
        
        # Extract requirement patterns
        req_patterns = self._extract_requirement_patterns(content)
        
        # Identify stakeholders
        stakeholders = self._identify_stakeholders(content)
        
        # Identify cross-cutting concerns
        cross_cutting = self._identify_cross_cutting_concerns(content)
        
        return {
            'suggested_domain': best_domain[0],
            'confidence': best_domain[1],
            'specificity_score': min(int(best_domain[1] * 5), 5),
            'key_terms': key_terms,
            'requirement_patterns': req_patterns,
            'stakeholders': stakeholders,
            'cross_cutting': cross_cutting
        }
    
    def _extract_requirement_patterns(self, content: str) -> List[Dict]:
        """Extract common requirement patterns from content"""
        patterns = []
        content_lower = content.lower()
        
        # Common business process patterns
        if any(term in content_lower for term in ['manage', 'track', 'monitor']):
            patterns.append({
                'type': 'management',
                'template': 'Comprehensive {entity} Management and Tracking System'
            })
        
        if any(term in content_lower for term in ['integrate', 'sync', 'connect']):
            patterns.append({
                'type': 'integration',
                'template': '{system} Integration and Data Synchronization'
            })
        
        if any(term in content_lower for term in ['report', 'analytics', 'dashboard']):
            patterns.append({
                'type': 'reporting',
                'template': 'Advanced Reporting and Analytics Dashboard'
            })
        
        if any(term in content_lower for term in ['user', 'interface', 'ui', 'ux']):
            patterns.append({
                'type': 'interface',
                'template': 'User Interface and Experience Implementation'
            })
        
        return patterns
    
    def _identify_stakeholders(self, content: str) -> List[str]:
        """Identify stakeholders from content"""
        stakeholders = ['End Users', 'Development Team']
        content_lower = content.lower()
        
        stakeholder_patterns = {
            'admin': ['System Administrators'],
            'manager': ['Management Team'],
            'customer': ['Customers', 'Customer Service'],
            'doctor': ['Medical Staff', 'Healthcare Providers'],
            'teacher': ['Educators', 'Academic Staff'],
            'student': ['Students', 'Learners'],
            'vendor': ['Vendors', 'Suppliers'],
            'investor': ['Investors', 'Financial Stakeholders']
        }
        
        for pattern, stakeholder_list in stakeholder_patterns.items():
            if pattern in content_lower:
                stakeholders.extend(stakeholder_list)
        
        return list(set(stakeholders))  # Remove duplicates
    
    def _identify_cross_cutting_concerns(self, content: str) -> List[str]:
        """Identify cross-cutting concerns from content"""
        concerns = []
        content_lower = content.lower()
        
        if any(term in content_lower for term in ['security', 'secure', 'encryption', 'auth']):
            concerns.append('security')
        
        if any(term in content_lower for term in ['performance', 'scalability', 'load']):
            concerns.append('performance')
        
        if any(term in content_lower for term in ['compliance', 'regulation', 'audit']):
            concerns.append('compliance')
        
        if any(term in content_lower for term in ['backup', 'disaster', 'recovery']):
            concerns.append('disaster_recovery')
        
        return concerns
    
    def _generate_plugin_code(self, spec: Dict[str, Any]) -> str:
        """Generate plugin code from specification"""
        domain_name = spec['domain_name']
        class_name = ''.join(word.capitalize() for word in domain_name.split('_')) + 'DomainHandler'
        
        # Generate keywords list
        keywords_str = ', '.join([f"'{kw}'" for kw in spec['keywords']])
        
        # Generate requirements extraction logic
        req_logic = self._generate_requirements_logic(spec)
        
        # Generate stakeholder logic
        stakeholder_logic = self._generate_stakeholder_logic(spec)
        
        return self.plugin_template.format(
            class_name=class_name,
            domain_name=domain_name,
            keywords=keywords_str,
            priority_score=spec.get('priority_score', 3),
            requirements_logic=req_logic,
            stakeholder_logic=stakeholder_logic
        )
    
    def _generate_requirements_logic(self, spec: Dict[str, Any]) -> str:
        """Generate requirements extraction logic"""
        logic_lines = []
        
        for pattern in spec.get('requirements_patterns', []):
            if pattern['type'] == 'management':
                logic_lines.append(f"""
        if any(term in content_lower for term in ['manage', 'track', 'monitor']):
            requirements.append({{
                'title': '{pattern['template'].replace('{entity}', spec['domain_name'].replace('_', ' ').title())}',
                'priority': 'high',
                'category': 'functional'
            }})""")
            
            elif pattern['type'] == 'integration':
                logic_lines.append(f"""
        if any(term in content_lower for term in ['integrate', 'sync', 'connect']):
            requirements.append({{
                'title': '{pattern['template'].replace('{system}', 'External System')}',
                'priority': 'medium',
                'category': 'functional'
            }})""")
        
        # Add default requirement if no patterns
        if not logic_lines:
            logic_lines.append(f"""
        requirements.append({{
            'title': 'Core {spec['domain_name'].replace('_', ' ').title()} System Implementation',
            'priority': 'high',
            'category': 'functional'
        }})""")
        
        return '\n'.join(logic_lines)
    
    def _generate_stakeholder_logic(self, spec: Dict[str, Any]) -> str:
        """Generate stakeholder extraction logic"""
        stakeholders = spec.get('stakeholders', ['End Users', 'Development Team'])
        stakeholders_str = ', '.join([f"'{s}'" for s in stakeholders])
        return f"return [{stakeholders_str}]"
    
    def _create_plugin_file(self, domain_name: str, plugin_code: str) -> str:
        """Create plugin file in domain_plugins directory"""
        filename = f"{domain_name}_handler.py"
        file_path = os.path.join("domain_plugins", filename)
        
        # Ensure directory exists
        os.makedirs("domain_plugins", exist_ok=True)
        
        # Write plugin file
        with open(file_path, 'w') as f:
            f.write(plugin_code)
        
        logger.info(f"[Plugin Creator] Created plugin file: {file_path}")
        return file_path
    
    def _register_plugin(self, domain_name: str) -> bool:
        """Register plugin with the system"""
        try:
            # Dynamic import and registration would happen here
            # For now, just return success
            logger.info(f"[Plugin Creator] Registered plugin: {domain_name}")
            return True
        except Exception as e:
            logger.error(f"[Plugin Creator] Failed to register plugin: {e}")
            return False
    
    def _analyze_plugin_quality(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the quality of the generated plugin"""
        quality_score = 0
        max_score = 100
        
        # Check keywords count
        if len(spec.get('keywords', [])) >= 5:
            quality_score += 30
        elif len(spec.get('keywords', [])) >= 3:
            quality_score += 20
        
        # Check requirement patterns
        if len(spec.get('requirements_patterns', [])) >= 2:
            quality_score += 25
        elif len(spec.get('requirements_patterns', [])) >= 1:
            quality_score += 15
        
        # Check stakeholders
        if len(spec.get('stakeholders', [])) >= 3:
            quality_score += 20
        
        # Check priority score
        if spec.get('priority_score', 1) >= 3:
            quality_score += 15
        
        # Check cross-cutting concerns
        if spec.get('cross_cutting_concerns'):
            quality_score += 10
        
        return {
            'quality_score': min(quality_score, max_score),
            'recommendations': self._get_quality_recommendations(spec)
        }
    
    def _get_quality_recommendations(self, spec: Dict[str, Any]) -> List[str]:
        """Get recommendations for improving plugin quality"""
        recommendations = []
        
        if len(spec.get('keywords', [])) < 5:
            recommendations.append("Add more domain-specific keywords for better detection")
        
        if len(spec.get('requirements_patterns', [])) < 2:
            recommendations.append("Define more requirement patterns for comprehensive extraction")
        
        if spec.get('priority_score', 1) < 3:
            recommendations.append("Consider increasing priority score if domain is highly specific")
        
        return recommendations
    
    def _get_plugin_template(self) -> str:
        """Get the plugin code template"""
        return '''#!/usr/bin/env python3
"""
{domain_name.title().replace('_', ' ')} Domain Handler
Auto-generated by Domain Plugin Creator X-Agent
"""

from .base_handler import BaseDomainHandler
from typing import Dict, List, Any

class {class_name}(BaseDomainHandler):
    """{domain_name.title().replace('_', ' ')} domain handler"""

    def get_domain_name(self) -> str:
        return '{domain_name}'

    def get_detection_keywords(self) -> List[str]:
        return [{keywords}]

    def get_priority_score(self) -> int:
        return {priority_score}

    def extract_requirements(self, content: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        requirements = []
        content_lower = content.lower()
        {requirements_logic}
        
        return requirements

    def extract_stakeholders(self, content: str) -> List[str]:
        {stakeholder_logic}
'''

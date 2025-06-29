#!/usr/bin/env python3
"""
Intelligent Domain Plugin Creator X-Agent with Anthropic API Integration
Only creates new domain plugins when existing ones don't match (confidence < 0.6)
Uses Claude AI for intelligent domain analysis and code generation
"""

import re
import os
import json
import asyncio
import ast
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime
from dotenv import load_dotenv

# Anthropic API integration
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("⚠️  Anthropic library not available. Plugin creation will use fallback mode.")

# Domain registry integration
try:
    from domain_plugins.registry import DomainRegistry
    REGISTRY_AVAILABLE = True
except ImportError:
    REGISTRY_AVAILABLE = False
    print("⚠️  Domain registry not available. Will skip existing domain check.")

logger = logging.getLogger(__name__)

class IntelligentDomainPluginCreator:
    """Intelligent plugin creator that checks existing domains first"""
    
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        self.agent_type = "IntelligentDomainPluginCreator"
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.client = None
        self.registry = None
        self.confidence_threshold = 0.6  # Only create new plugins if existing confidence < 0.6
        
        # Initialize Anthropic client
        if ANTHROPIC_AVAILABLE and self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)
            logger.info("[Plugin Creator] Initialized with Anthropic API")
        else:
            logger.warning("[Plugin Creator] No Anthropic API key found - using fallback mode")
        
        # Initialize domain registry
        if REGISTRY_AVAILABLE:
            self.registry = DomainRegistry()
            logger.info(f"[Plugin Creator] Loaded {len(self.registry.list_domains())} existing domains")
        else:
            logger.warning("[Plugin Creator] Domain registry not available")
    
    def _analyze_content_complexity(self, content: str) -> float:
        """Analyzes content to determine complexity for model selection."""
        word_count = len(content.split())
        unique_words = len(set(re.findall(r'\b\w+\b', content.lower())))
        
        # Normalize complexity score (0.0 to 1.0)
        # This is a simple heuristic. More advanced metrics could be used.
        complexity = (word_count / 1000) + (unique_words / 500)
        return min(complexity, 1.0)

    async def analyze_and_create_if_needed(self, content: str, domain_hint: str = '') -> Dict[str, Any]:
        """Main entry point: Check existing domains first, only create if needed"""
        logger.info("[Plugin Creator] Analyzing content for domain requirements")
        
        try:
            # Step 1: Check existing domains first
            existing_match = self._check_existing_domains(content)
            
            if existing_match['confidence'] >= self.confidence_threshold:
                logger.info(f"[Plugin Creator] Found existing domain '{existing_match['domain']}' with {existing_match['confidence']:.2f} confidence")
                return {
                    'success': True,
                    'action': 'existing_domain_used',
                    'domain_name': existing_match['domain'],
                    'confidence': existing_match['confidence'],
                    'message': f"Using existing {existing_match['domain']} domain plugin (confidence: {existing_match['confidence']:.2f})",
                    'creation_needed': False
                }
            
            # Step 2: Existing domains don't match well enough - create new plugin
            logger.info(f"[Plugin Creator] Best existing match: '{existing_match['domain']}' ({existing_match['confidence']:.2f}) - below threshold {self.confidence_threshold}")
            
            create_result = await self.create_domain_plugin({
                'content': content,
                'domain_name': domain_hint,
                'existing_domains': self.registry.list_domains() if self.registry else []
            })
            
            if create_result['success']:
                create_result['action'] = 'new_domain_created'
                create_result['creation_needed'] = True
                create_result['existing_best_match'] = existing_match
            
            return create_result
            
        except Exception as e:
            logger.error(f"[Plugin Creator] Error in analysis: {e}")
            return {'success': False, 'error': f'Analysis failed: {str(e)}'}
    
    def _check_existing_domains(self, content: str) -> Dict[str, Any]:
        """Check if any existing domain plugins match the content well enough"""
        
        if not self.registry:
            return {'domain': 'none', 'confidence': 0.0, 'available_domains': []}
        
        try:
            # Use the registry's built-in domain detection
            best_domain, confidence = self.registry.detect_domain(content)
            
            available_domains = self.registry.list_domains()
            
            logger.info(f"[Plugin Creator] Domain detection results:")
            for domain in available_domains:
                handler = self.registry.get_handler(domain)
                if handler:
                    domain_confidence = handler.detect_domain_confidence(content)
                    logger.info(f"  - {domain}: {domain_confidence:.3f}")
            
            return {
                'domain': best_domain,
                'confidence': confidence,
                'available_domains': available_domains,
                'threshold': self.confidence_threshold
            }
            
        except Exception as e:
            logger.error(f"[Plugin Creator] Error checking existing domains: {e}")
            return {'domain': 'error', 'confidence': 0.0, 'available_domains': []}
    
    async def create_domain_plugin(self, domain_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Create a domain plugin using Claude for intelligent code generation"""
        logger.info(f"[Plugin Creator] Creating plugin with Claude AI")
        
        try:
            # Extract content and domain info
            content = domain_spec.get('content', '')
            domain_hint = domain_spec.get('domain_name', '')
            
            if not content:
                return {'success': False, 'error': 'No content provided for plugin creation'}

            # Step 1: Analyze content complexity for dynamic model selection
            content_complexity = self._analyze_content_complexity(content)
            
            if content_complexity < 0.3:
                model = "claude-3-haiku-20240307"
            elif content_complexity < 0.7:
                model = "claude-3-sonnet-20240229"
            else:
                model = "claude-3-opus-20240229"
            
            logger.info(f"[Plugin Creator] Content complexity: {content_complexity:.2f}, selected model: {model}")

            # Step 2: Analyze domain with Claude
            domain_analysis = await self._analyze_domain_with_claude(content, domain_hint, model)
            if not domain_analysis['success']:
                return domain_analysis
            
            # Step 3: Generate plugin code with Claude
            plugin_code = await self._generate_plugin_code_with_claude(domain_analysis['analysis'], model)
            if not plugin_code['success']:
                return plugin_code
            
            # Step 4: Validate and save plugin
            validation_result = self._validate_and_save_plugin(
                plugin_code['code'], 
                domain_analysis['analysis']['domain_name']
            )
            
            if validation_result['success']:
                return {
                    'success': True,
                    'domain_name': domain_analysis['analysis']['domain_name'],
                    'file_path': validation_result['file_path'],
                    'registered': True,
                    'analysis': domain_analysis['analysis'],
                    'creation_method': 'claude_api',
                    'model_used': model
                }
            else:
                return validation_result
                
        except Exception as e:
            logger.error(f"[Plugin Creator] Error creating plugin: {e}")
            return {'success': False, 'error': f'Plugin creation failed: {str(e)}'}
    
    async def _analyze_domain_with_claude(self, content: str, domain_hint: str = '', model: str = 'claude-3-sonnet-20240229') -> Dict[str, Any]:
        """Use Claude to analyze the business domain and create specifications using function calling."""
        
        if not self.client:
            return await self._fallback_domain_analysis(content, domain_hint)
        
        try:
            existing_domains = self.registry.list_domains() if self.registry else []
            
            tool_spec = {
                "name": "create_domain_plugin_spec",
                "description": "Analyzes content to create a detailed specification for a new domain plugin.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "domain_name": {"type": "string", "description": "A unique, snake_case name for the domain."},
                        "domain_title": {"type": "string", "description": "A human-readable title for the domain."},
                        "description": {"type": "string", "description": "A brief description of what this domain handles."},
                        "detection_keywords": {"type": "array", "items": {"type": "string"}, "description": "A list of highly specific keywords to detect this domain."},
                        "priority_score": {"type": "integer", "description": "A score from 1-5 indicating specificity and importance."},
                        "typical_stakeholders": {"type": "array", "items": {"type": "string"}},
                        "functional_requirements": {"type": "array", "items": {"type": "string"}},
                        "non_functional_requirements": {"type": "array", "items": {"type": "string"}},
                        "complexity_score": {"type": "number", "description": "A score from 0.0 to 1.0 for complexity."},
                        "confidence": {"type": "number", "description": "A score from 0.0 to 1.0 on how confident the model is about this analysis."},
                        "justification": {"type": "string", "description": "An explanation of why this new domain is necessary."}
                    },
                    "required": ["domain_name", "domain_title", "description", "detection_keywords", "priority_score", "justification"]
                }
            }

            prompt = f"You are an expert business analyst. Analyze the following content and determine if a NEW, unique domain plugin is needed. Do not duplicate any of the following existing domains: {', '.join(existing_domains)}. If a new plugin is needed, call the `create_domain_plugin_spec` function with the detailed analysis. Content to analyze: {content}"

            message = self.client.messages.create(
                model=model,
                max_tokens=4096,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}],
                tools=[tool_spec],
                tool_choice={"type": "tool", "name": "create_domain_plugin_spec"}
            )

            # Find the function call in the response
            tool_call = next((block for block in message.content if block.type == 'tool_use'), None)
            
            if tool_call:
                analysis = tool_call.input
                logger.info(f"[Plugin Creator] Claude analyzed new domain via function call: {analysis.get('domain_name')}")
                return {'success': True, 'analysis': analysis}
            else:
                logger.error("[Plugin Creator] Failed to get a valid function call from Claude's domain analysis")
                return {'success': False, 'error': 'Failed to parse domain analysis via function call'}

        except Exception as e:
            logger.error(f"[Plugin Creator] Claude API error during function call: {e}")
            return await self._fallback_domain_analysis(content, domain_hint)
    
    async def _generate_plugin_code_with_claude(self, domain_analysis: Dict[str, Any], model: str) -> Dict[str, Any]:
        """Use Claude to generate domain handler code following exact existing pattern"""
        
        if not self.client:
            return self._fallback_plugin_generation(domain_analysis)
        
        try:
            code_prompt = f"""
Create a Python domain handler that follows the EXACT pattern of existing handlers.

Domain Analysis:
{json.dumps(domain_analysis, indent=2)}

Generate a complete Python file that follows this EXACT structure:

```python
#!/usr/bin/env python3
\"\"\"
{domain_analysis['domain_title']} Domain Handler
{domain_analysis['description']}
\"\"\"

from .base_handler import BaseDomainHandler
from typing import Dict, List, Any

class {domain_analysis['domain_name'].title().replace('_', '')}DomainHandler(BaseDomainHandler):
    \"\"\"{domain_analysis['domain_title']} domain handler\"\"\"
    
    def get_domain_name(self) -> str:
        return '{domain_analysis['domain_name']}'
    
    def get_detection_keywords(self) -> List[str]:
        return {domain_analysis['detection_keywords']}
    
    def get_priority_score(self) -> int:
        return {domain_analysis['priority_score']}  # 1-5 scale
    
    def extract_requirements(self, content: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        requirements = []
        content_lower = content.lower()
        
        # Generate 5-8 functional requirements based on domain analysis
        # Use functional_requirements: {domain_analysis.get('functional_requirements', [])}
        
        # Add domain-specific requirement extraction logic here
        # Pattern: if keyword in content -> add specific requirement
        
        return requirements
    
    def extract_stakeholders(self, content: str) -> List[str]:
        \"\"\"Extract domain-specific stakeholders\"\"\"
        base_stakeholders = {domain_analysis['typical_stakeholders']}
        
        # Add intelligent stakeholder detection based on content
        
        return base_stakeholders
```

CRITICAL REQUIREMENTS:
1. Must inherit from BaseDomainHandler
2. Must implement all 4 required methods exactly as shown
3. Class name must be `{domain_analysis['domain_name'].title().replace('_', '')}Handler`
4. Fill in ALL method bodies with intelligent, working code
5. Use the detection_keywords for smart requirement extraction
6. Create realistic, domain-specific requirements
7. Return ONLY the Python code, no markdown or explanations

Make this production-ready code that actually works!
"""

            message = self.client.messages.create(
                model=model,
                max_tokens=4000,
                temperature=0.1,
                messages=[{"role": "user", "content": code_prompt}]
            )
            
            response_text = message.content[0].text
            
            # Extract Python code
            code_match = re.search(r'```python\n(.*?)```', response_text, re.DOTALL)
            if code_match:
                plugin_code = code_match.group(1)
                logger.info(f"[Plugin Creator] Claude generated domain handler ({len(plugin_code)} chars)")
                return {'success': True, 'code': plugin_code}
            else:
                # Try without markdown
                if 'class ' in response_text and 'BaseDomainHandler' in response_text:
                    logger.info("[Plugin Creator] Claude generated code without markdown")
                    return {'success': True, 'code': response_text}
                else:
                    logger.error("[Plugin Creator] No valid domain handler code generated")
                    return {'success': False, 'error': 'No valid domain handler code found'}
                    
        except Exception as e:
            logger.error(f"[Plugin Creator] Code generation error: {e}")
            return self._fallback_plugin_generation(domain_analysis)
    
    def _validate_and_save_plugin(self, plugin_code: str, domain_name: str) -> Dict[str, Any]:
        """Validate generated Python code and save as plugin file"""
        
        try:
            # Step 1: Validate Python syntax
            ast.parse(plugin_code)
            logger.info("[Plugin Creator] Plugin code syntax validation passed")
            
            # Step 2: Check for required class and methods
            # Only check for abstract methods that MUST be implemented  
            required_methods = ['get_domain_name', 'get_detection_keywords', 'extract_requirements']
            expected_class_name = f"{domain_name.title().replace('_', '')}DomainHandler"
            
            if expected_class_name not in plugin_code:
                return {'success': False, 'error': f'Expected class {expected_class_name} not found'}
            
            for method in required_methods:
                if f'def {method}' not in plugin_code:
                    return {'success': False, 'error': f'Required method {method} not found'}
            
            # Step 3: Save plugin file
            plugin_dir = "domain_plugins"
            if not os.path.exists(plugin_dir):
                os.makedirs(plugin_dir)
            
            file_path = os.path.join(plugin_dir, f"{domain_name}_handler.py")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(plugin_code)
            
            logger.info(f"[Plugin Creator] Plugin saved to {file_path}")
            
            return {
                'success': True,
                'file_path': file_path,
                'domain_name': domain_name,
                'class_name': expected_class_name
            }
            
        except SyntaxError as e:
            logger.error(f"[Plugin Creator] Python syntax error: {e}")
            return {'success': False, 'error': f'Invalid Python syntax: {str(e)}'}
        except Exception as e:
            logger.error(f"[Plugin Creator] Plugin validation error: {e}")
            return {'success': False, 'error': f'Plugin validation failed: {str(e)}'}
    
    async def _fallback_domain_analysis(self, content: str, domain_hint: str = '') -> Dict[str, Any]:
        """Fallback domain analysis when Claude API is not available"""
        logger.info("[Plugin Creator] Using fallback domain analysis")
        
        # Simple keyword-based analysis
        content_lower = content.lower()
        
        # Generate domain name from content
        domain_name = domain_hint.lower().replace(' ', '_') if domain_hint else 'custom_domain'
        if not domain_name or domain_name == 'custom_domain':
            # Extract key words for domain naming
            important_words = re.findall(r'\b[a-z]{4,}\b', content_lower)
            if important_words:
                domain_name = '_'.join(important_words[:2])
            else:
                domain_name = 'custom_domain'
        
        return {
            'success': True,
            'analysis': {
                'domain_name': domain_name,
                'domain_title': domain_hint or 'Custom Domain',
                'description': f'Custom domain handler for {domain_hint or "specialized business domain"}',
                'key_concepts': ['management', 'tracking', 'optimization'],
                'business_vocabulary': ['system', 'process', 'workflow'],
                'typical_stakeholders': ['End Users', 'System Administrators', 'Business Stakeholders'],
                'common_requirements': ['Core functionality', 'User interface', 'Data management'],
                'complexity_score': 0.5,
                'confidence': 0.6,
                'industry_category': 'general'
            }
        }
    
    def _fallback_plugin_generation(self, domain_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback plugin generation when Claude API is not available"""
        logger.info("[Plugin Creator] Using fallback plugin generation")
        
        domain_name = domain_analysis['domain_name']
        class_name = domain_name.title().replace('_', '') + 'Handler'
        
        # Generate basic plugin template
        plugin_code = f'''#!/usr/bin/env python3
"""
{domain_analysis['domain_title']} Domain Handler
{domain_analysis['description']}
"""

from typing import List, Dict, Any
import re

class {class_name}:
    """Handles {domain_analysis['domain_title']} domain requirements"""
    
    def __init__(self):
        self.domain_name = "{domain_name}"
        self.domain_keywords = {domain_analysis.get('business_vocabulary', [])}
        self.stakeholder_types = {domain_analysis.get('typical_stakeholders', [])}
    
    def extract_requirements(self, content: str) -> List[Dict[str, Any]]:
        """Extract domain-specific requirements from content"""
        requirements = []
        
        # Basic requirement extraction
        base_reqs = [
            "Core system architecture and functionality",
            "User interface and user experience design", 
            "Data management and storage solutions",
            "Integration and API development",
            "Security and compliance measures"
        ]
        
        for i, req_title in enumerate(base_reqs, 1):
            requirements.append({{
                'title': f"{{domain_analysis['domain_title']}} {{req_title}}",
                'priority': 'high' if i <= 2 else 'medium',
                'category': 'functional'
            }})
        
        return requirements
    
    def get_cross_cutting_requirements(self, content: str) -> List[Dict[str, Any]]:
        """Get cross-cutting requirements for {domain_analysis['domain_title']}"""
        return [
            {{'title': 'Performance optimization and scalability', 'priority': 'medium', 'category': 'non-functional'}},
            {{'title': 'Security and data protection', 'priority': 'high', 'category': 'non-functional'}},
            {{'title': 'Monitoring and logging capabilities', 'priority': 'medium', 'category': 'non-functional'}}
        ]
    
    def extract_stakeholders(self, content: str) -> List[str]:
        """Extract domain-specific stakeholders"""
        return self.stakeholder_types
    
    def validate_requirements(self, requirements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate requirements for {domain_analysis['domain_title']} domain"""
        return {{
            'valid': True,
            'score': 0.75,
            'suggestions': []
        }}
'''
        
        return {{'success': True, 'code': plugin_code}}

    def analyze_content_for_plugin(self, content: str) -> Dict[str, Any]:
        """Analyze content to determine if custom plugin creation is needed"""
        logger.info("[Plugin Creator] Analyzing content for plugin suggestions")
        
        # Quick analysis for plugin recommendation
        content_lower = content.lower()
        
        # Check for specialized domain indicators
        specialized_terms = [
            'quantum', 'blockchain', 'drone', 'beekeeping', 'maritime', 'aerospace',
            'biotechnology', 'cryptocurrency', 'robotics', 'agriculture', 'forestry'
        ]
        
        specialty_score = sum(1 for term in specialized_terms if term in content_lower)
        complexity_indicators = ['specialized', 'custom', 'unique', 'specific', 'proprietary']
        complexity_score = sum(1 for indicator in complexity_indicators if indicator in content_lower)
        
        # Calculate confidence for plugin creation
        confidence = min((specialty_score * 0.3 + complexity_score * 0.2 + len(content.split()) / 100), 1.0)
        
        return {
            'confidence': confidence,
            'complexity_score': min(complexity_score / 3.0, 1.0),
            'recommended': confidence > 0.6,
            'suggested_plugin': {
                'domain_name': 'custom_domain',
                'content': content,
                'estimated_effort': 'medium' if confidence > 0.7 else 'low'
            }
        }


# Backward compatibility aliases
ClaudeEnhancedPluginCreator = IntelligentDomainPluginCreator
DomainPluginCreatorXAgent = IntelligentDomainPluginCreator

# Additional method for auto-registration
def auto_register_new_plugin(self, domain_name: str, class_name: str):
    """Auto-register the new plugin in the domain registry"""
    try:
        if not self.registry:
            logger.warning("[Plugin Creator] No registry available for auto-registration")
            return False
        
        # Dynamically import and register the new plugin
        module_name = f"domain_plugins.{domain_name}_handler"
        module = __import__(module_name, fromlist=[class_name])
        handler_class = getattr(module, class_name)
        handler_instance = handler_class()
        
        self.registry.register_handler(handler_instance)
        logger.info(f"[Plugin Creator] ✅ Auto-registered new domain: {domain_name}")
        return True
        
    except Exception as e:
        logger.error(f"[Plugin Creator] Failed to auto-register plugin: {e}")
        logger.info("[Plugin Creator] Plugin file created but manual registration may be needed")
        return False

# Add method to IntelligentDomainPluginCreator class
IntelligentDomainPluginCreator.auto_register_new_plugin = auto_register_new_plugin
#!/usr/bin/env python3
"""
ContextAnalyzer Agent with Co-Located Plugins
Third agent in the Cognitive Triangulation pipeline - performs semantic analysis within scope
"""

import re
import time
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Tuple, Set
from lxml import etree
from collections import defaultdict

class BaseXAgent(ABC):
    """Base X-Agent with XML processing and performance tracking"""
    
    def __init__(self, agent_type: str):
        self.agent_type = agent_type
        self.metrics = {'total_time': 0.0}
    
    def process(self, input_xml: str) -> str:
        """Parse input → Process → Generate output XML"""
        start_time = time.perf_counter()
        
        try:
            # Parse XML input using lxml
            parsed_input = etree.fromstring(input_xml.encode('utf-8'))
            
            # Process with agent-specific intelligence
            result = self._process_intelligence(parsed_input)
            
            # Generate XML output
            output_xml = self._generate_xml(result)
            
            # Track performance
            end_time = time.perf_counter()
            self.metrics['total_time'] = (end_time - start_time) * 1000
            
            return output_xml
            
        except Exception as e:
            return f"<Error agent='{self.agent_type}'>Error processing: {str(e)}</e>"
    
    @abstractmethod
    def _process_intelligence(self, parsed_input: etree.Element) -> dict:
        """Agent-specific logic - implemented by subclasses"""
        pass
    
    @abstractmethod
    def _generate_xml(self, result: dict) -> str:
        """Generate XML for next agent - implemented by subclasses"""
        pass

# ================================
# SEMANTIC ANALYSIS PLUGINS
# ================================

class BaseSemanticPlugin(ABC):
    """Base class for semantic analysis plugins - co-located"""
    
    @abstractmethod
    def get_analysis_types(self) -> List[str]:
        """Return the types of semantic analysis this plugin performs"""
        pass
    
    @abstractmethod
    def detect_design_patterns(self, pois: Dict, relationships: List[Dict], content: str) -> List[Dict[str, Any]]:
        """Detect design patterns (Singleton, Factory, Observer, etc.)"""
        pass
    
    @abstractmethod
    def detect_architectural_patterns(self, pois: Dict, relationships: List[Dict], content: str) -> List[Dict[str, Any]]:
        """Detect architectural patterns (MVC, Repository, Service Layer, etc.)"""
        pass
    
    @abstractmethod
    def analyze_data_flow(self, pois: Dict, relationships: List[Dict], content: str) -> List[Dict[str, Any]]:
        """Analyze data flow patterns and transformations"""
        pass
    
    @abstractmethod
    def analyze_dependency_injection(self, pois: Dict, relationships: List[Dict], content: str) -> List[Dict[str, Any]]:
        """Detect dependency injection and inversion of control patterns"""
        pass
    
    @abstractmethod
    def analyze_cross_cutting_concerns(self, pois: Dict, relationships: List[Dict], content: str) -> List[Dict[str, Any]]:
        """Identify cross-cutting concerns (logging, error handling, security, etc.)"""
        pass

class PythonSemanticPlugin(BaseSemanticPlugin):
    """Python-specific semantic analysis plugin"""
    
    def get_analysis_types(self) -> List[str]:
        return ["DESIGN_PATTERNS", "ARCHITECTURAL_PATTERNS", "DATA_FLOW", "DEPENDENCY_INJECTION", "CROSS_CUTTING"]
    
    def detect_design_patterns(self, pois: Dict, relationships: List[Dict], content: str) -> List[Dict[str, Any]]:
        """Detect Python design patterns"""
        patterns = []
        
        classes = pois.get('classes', [])
        functions = pois.get('functions', [])
        
        # Singleton Pattern Detection
        for cls in classes:
            class_name = cls['name']
            
            # Look for singleton indicators
            singleton_indicators = [
                r'_instance\s*=\s*None',  # Class variable for instance
                r'def\s+__new__\s*\(',     # Custom __new__ method
                r'if\s+not\s+hasattr\s*\(',  # Instance checking
                r'@\s*singleton',          # Singleton decorator
            ]
            
            singleton_score = 0
            evidence = []
            
            for indicator in singleton_indicators:
                if re.search(indicator, content, re.IGNORECASE):
                    singleton_score += 1
                    evidence.append(f"Found pattern: {indicator}")
            
            if singleton_score >= 2:
                patterns.append({
                    'type': 'SINGLETON_PATTERN',
                    'class': class_name,
                    'confidence': min(0.9, 0.4 + (singleton_score * 0.15)),
                    'evidence': evidence,
                    'line': cls['line']
                })
        
        # Factory Pattern Detection
        factory_methods = []
        for func in functions:
            func_name = func['name'].lower()
            if any(keyword in func_name for keyword in ['create', 'build', 'make', 'factory', 'get_instance']):
                # Look for return statements with class instantiation
                factory_pattern = rf'def\s+{re.escape(func["name"])}.*?return\s+\w+\s*\('
                if re.search(factory_pattern, content, re.DOTALL):
                    factory_methods.append({
                        'type': 'FACTORY_PATTERN',
                        'method': func['name'],
                        'confidence': 0.75,
                        'evidence': [f"Factory method pattern in {func['name']}"],
                        'line': func['line']
                    })
        
        patterns.extend(factory_methods)
        
        # Observer Pattern Detection
        observer_indicators = [
            r'def\s+notify\s*\(',
            r'def\s+attach\s*\(',
            r'def\s+detach\s*\(',
            r'observers?\s*=\s*\[',
            r'subscribers?\s*=\s*\[',
        ]
        
        observer_score = 0
        observer_evidence = []
        
        for indicator in observer_indicators:
            if re.search(indicator, content, re.IGNORECASE):
                observer_score += 1
                observer_evidence.append(f"Observer pattern indicator: {indicator}")
        
        if observer_score >= 2:
            patterns.append({
                'type': 'OBSERVER_PATTERN',
                'confidence': min(0.85, 0.5 + (observer_score * 0.1)),
                'evidence': observer_evidence,
                'scope': 'module'
            })
        
        return patterns
    
    def detect_architectural_patterns(self, pois: Dict, relationships: List[Dict], content: str) -> List[Dict[str, Any]]:
        """Detect Python architectural patterns"""
        patterns = []
        
        classes = pois.get('classes', [])
        
        # Repository Pattern Detection
        repository_classes = [cls for cls in classes if 'repository' in cls['name'].lower()]
        if repository_classes:
            for repo_cls in repository_classes:
                # Look for CRUD methods
                crud_methods = ['save', 'find', 'delete', 'update', 'get', 'create']
                found_methods = []
                
                for method in crud_methods:
                    if re.search(rf'def\s+{method}', content, re.IGNORECASE):
                        found_methods.append(method)
                
                if len(found_methods) >= 3:
                    patterns.append({
                        'type': 'REPOSITORY_PATTERN',
                        'class': repo_cls['name'],
                        'confidence': 0.8,
                        'methods': found_methods,
                        'evidence': [f"Repository with CRUD methods: {', '.join(found_methods)}"],
                        'line': repo_cls['line']
                    })
        
        # Service Layer Pattern Detection
        service_classes = [cls for cls in classes if 'service' in cls['name'].lower()]
        if service_classes:
            for service_cls in service_classes:
                # Look for business logic indicators
                business_indicators = [
                    r'def\s+process',
                    r'def\s+handle',
                    r'def\s+execute',
                    r'def\s+validate',
                    r'def\s+calculate',
                ]
                
                found_indicators = []
                for indicator in business_indicators:
                    if re.search(indicator, content, re.IGNORECASE):
                        found_indicators.append(indicator)
                
                if found_indicators:
                    patterns.append({
                        'type': 'SERVICE_LAYER_PATTERN',
                        'class': service_cls['name'],
                        'confidence': 0.75,
                        'evidence': [f"Service layer with business logic: {len(found_indicators)} methods"],
                        'line': service_cls['line']
                    })
        
        # Model-View-Controller (MVC) Pattern Detection
        mvc_components = {'model': [], 'view': [], 'controller': []}
        
        for cls in classes:
            class_name_lower = cls['name'].lower()
            if 'model' in class_name_lower or 'entity' in class_name_lower:
                mvc_components['model'].append(cls)
            elif 'view' in class_name_lower or 'template' in class_name_lower:
                mvc_components['view'].append(cls)
            elif 'controller' in class_name_lower or 'handler' in class_name_lower:
                mvc_components['controller'].append(cls)
        
        # Check if we have all three components
        if all(mvc_components.values()):
            patterns.append({
                'type': 'MVC_PATTERN',
                'confidence': 0.85,
                'components': {
                    'models': [m['name'] for m in mvc_components['model']],
                    'views': [v['name'] for v in mvc_components['view']],
                    'controllers': [c['name'] for c in mvc_components['controller']]
                },
                'evidence': ['Found Model, View, and Controller components'],
                'scope': 'module'
            })
        
        return patterns
    
    def analyze_data_flow(self, pois: Dict, relationships: List[Dict], content: str) -> List[Dict[str, Any]]:
        """Analyze Python data flow patterns"""
        data_flows = []
        
        functions = pois.get('functions', [])
        variables = pois.get('variables', [])
        
        # Analyze function parameter → return value flows
        for func in functions:
            func_name = func['name']
            
            # Find function definition and return statements
            func_pattern = rf'def\s+{re.escape(func_name)}\s*\([^)]*\):(.*?)(?=def\s|\Z)'
            func_match = re.search(func_pattern, content, re.DOTALL)
            
            if func_match:
                func_body = func_match.group(1)
                
                # Count return statements
                return_statements = len(re.findall(r'return\s+', func_body))
                
                # Look for data transformation patterns
                transform_patterns = [
                    r'\.map\(',
                    r'\.filter\(',
                    r'\.reduce\(',
                    r'list\s*\(',
                    r'dict\s*\(',
                    r'\.join\(',
                    r'\.split\(',
                ]
                
                transformations = []
                for pattern in transform_patterns:
                    if re.search(pattern, func_body):
                        transformations.append(pattern.replace('\\', ''))
                
                if return_statements > 0 or transformations:
                    data_flows.append({
                        'type': 'DATA_TRANSFORMATION',
                        'function': func_name,
                        'return_count': return_statements,
                        'transformations': transformations,
                        'confidence': 0.7,
                        'evidence': [f"Function with {return_statements} returns and {len(transformations)} transformations"],
                        'line': func['line']
                    })
        
        # Analyze variable data flow chains
        use_relationships = [r for r in relationships if r.get('type') == 'USES']
        if use_relationships:
            # Group by variable to see flow patterns
            var_usage = defaultdict(list)
            for rel in use_relationships:
                var_name = rel.get('to', '')
                function = rel.get('from', '')
                var_usage[var_name].append(function)
            
            # Find variables used in multiple functions (indicating data flow)
            for var_name, functions in var_usage.items():
                if len(functions) > 1:
                    data_flows.append({
                        'type': 'VARIABLE_FLOW',
                        'variable': var_name,
                        'functions': list(set(functions)),  # Remove duplicates
                        'confidence': 0.6,
                        'evidence': [f"Variable {var_name} flows through {len(set(functions))} functions"],
                        'flow_count': len(set(functions))
                    })
        
        return data_flows
    
    def analyze_dependency_injection(self, pois: Dict, relationships: List[Dict], content: str) -> List[Dict[str, Any]]:
        """Detect Python dependency injection patterns"""
        di_patterns = []
        
        classes = pois.get('classes', [])
        
        for cls in classes:
            class_name = cls['name']
            
            # Look for constructor injection
            init_pattern = rf'class\s+{re.escape(class_name)}.*?def\s+__init__\s*\([^)]+\):'
            init_match = re.search(init_pattern, content, re.DOTALL)
            
            if init_match:
                # Extract __init__ parameters
                init_params = re.search(r'__init__\s*\(([^)]+)\)', init_match.group(0))
                if init_params:
                    params = init_params.group(1)
                    
                    # Count non-self parameters (potential dependencies)
                    param_list = [p.strip() for p in params.split(',') if p.strip() != 'self']
                    
                    if len(param_list) >= 2:  # At least 2 dependencies
                        # Look for assignment to instance variables
                        assignment_patterns = [
                            rf'self\.{param}\s*=\s*{param}' for param in param_list
                        ]
                        
                        assignments_found = sum(
                            1 for pattern in assignment_patterns 
                            if re.search(pattern, content)
                        )
                        
                        if assignments_found >= len(param_list) * 0.5:  # At least 50% of params assigned
                            di_patterns.append({
                                'type': 'CONSTRUCTOR_INJECTION',
                                'class': class_name,
                                'dependencies': param_list,
                                'confidence': 0.8,
                                'evidence': [f"Constructor injection with {len(param_list)} dependencies"],
                                'line': cls['line']
                            })
        
        # Look for setter injection
        setter_methods = []
        for func in pois.get('functions', []):
            func_name = func['name']
            if func_name.startswith('set_') and len(func_name) > 4:
                dependency_name = func_name[4:]  # Remove 'set_' prefix
                
                # Look for assignment in setter
                setter_pattern = rf'def\s+{re.escape(func_name)}\s*\([^)]+\):(.*?)(?=def\s|\Z)'
                setter_match = re.search(setter_pattern, content, re.DOTALL)
                
                if setter_match and f'self.{dependency_name}' in setter_match.group(1):
                    setter_methods.append({
                        'type': 'SETTER_INJECTION',
                        'method': func_name,
                        'dependency': dependency_name,
                        'confidence': 0.7,
                        'evidence': [f"Setter injection method for {dependency_name}"],
                        'line': func['line']
                    })
        
        di_patterns.extend(setter_methods)
        
        return di_patterns
    
    def analyze_cross_cutting_concerns(self, pois: Dict, relationships: List[Dict], content: str) -> List[Dict[str, Any]]:
        """Identify Python cross-cutting concerns"""
        concerns = []
        
        # Logging Detection
        logging_indicators = [
            r'import\s+logging',
            r'from\s+logging',
            r'logger\s*=',
            r'\.log\(',
            r'\.info\(',
            r'\.debug\(',
            r'\.warning\(',
            r'\.error\(',
            r'print\(',  # Simple logging
        ]
        
        logging_score = 0
        logging_evidence = []
        
        for indicator in logging_indicators:
            matches = len(re.findall(indicator, content, re.IGNORECASE))
            if matches > 0:
                logging_score += matches
                logging_evidence.append(f"Logging pattern: {indicator} ({matches} occurrences)")
        
        if logging_score >= 3:
            concerns.append({
                'type': 'LOGGING_CONCERN',
                'confidence': min(0.9, 0.5 + (logging_score * 0.05)),
                'occurrences': logging_score,
                'evidence': logging_evidence,
                'scope': 'module'
            })
        
        # Error Handling Detection
        error_indicators = [
            r'try\s*:',
            r'except\s+\w+',
            r'except\s*:',
            r'finally\s*:',
            r'raise\s+\w+',
            r'assert\s+',
        ]
        
        error_score = 0
        error_evidence = []
        
        for indicator in error_indicators:
            matches = len(re.findall(indicator, content, re.IGNORECASE))
            if matches > 0:
                error_score += matches
                error_evidence.append(f"Error handling: {indicator} ({matches} occurrences)")
        
        if error_score >= 2:
            concerns.append({
                'type': 'ERROR_HANDLING_CONCERN',
                'confidence': min(0.85, 0.4 + (error_score * 0.1)),
                'occurrences': error_score,
                'evidence': error_evidence,
                'scope': 'module'
            })
        
        # Validation/Security Detection
        validation_indicators = [
            r'def\s+validate',
            r'if\s+not\s+\w+',
            r'assert\s+',
            r'isinstance\(',
            r'hasattr\(',
            r'\.strip\(',
            r'\.lower\(',
            r'len\s*\(',
        ]
        
        validation_score = 0
        validation_evidence = []
        
        for indicator in validation_indicators:
            matches = len(re.findall(indicator, content, re.IGNORECASE))
            if matches > 0:
                validation_score += matches
                validation_evidence.append(f"Validation: {indicator} ({matches} occurrences)")
        
        if validation_score >= 5:
            concerns.append({
                'type': 'VALIDATION_CONCERN',
                'confidence': min(0.8, 0.3 + (validation_score * 0.05)),
                'occurrences': validation_score,
                'evidence': validation_evidence,
                'scope': 'module'
            })
        
        return concerns

class JavaScriptSemanticPlugin(BaseSemanticPlugin):
    """JavaScript-specific semantic analysis plugin"""
    
    def get_analysis_types(self) -> List[str]:
        return ["DESIGN_PATTERNS", "ARCHITECTURAL_PATTERNS", "DATA_FLOW", "DEPENDENCY_INJECTION", "CROSS_CUTTING"]
    
    def detect_design_patterns(self, pois: Dict, relationships: List[Dict], content: str) -> List[Dict[str, Any]]:
        """Detect JavaScript design patterns"""
        patterns = []
        
        # Module Pattern Detection
        module_indicators = [
            r'\(\s*function\s*\(',  # IIFE
            r'function\s*\(\s*\)\s*{',  # Function wrapper
            r'export\s+\{',  # ES6 exports
            r'module\.exports\s*=',  # CommonJS exports
        ]
        
        module_score = sum(1 for indicator in module_indicators if re.search(indicator, content))
        
        if module_score >= 2:
            patterns.append({
                'type': 'MODULE_PATTERN',
                'confidence': 0.8,
                'evidence': [f"Module pattern indicators: {module_score}"],
                'scope': 'file'
            })
        
        # Prototype Pattern Detection
        if re.search(r'\.prototype\.\w+\s*=', content):
            patterns.append({
                'type': 'PROTOTYPE_PATTERN',
                'confidence': 0.9,
                'evidence': ['Prototype extension found'],
                'scope': 'file'
            })
        
        return patterns
    
    def detect_architectural_patterns(self, pois: Dict, relationships: List[Dict], content: str) -> List[Dict[str, Any]]:
        """Detect JavaScript architectural patterns"""
        patterns = []
        
        # Component Pattern (React/Vue style)
        component_indicators = [
            r'function\s+\w+Component',
            r'class\s+\w+\s+extends\s+Component',
            r'React\.createElement',
            r'useState\(',
            r'useEffect\(',
        ]
        
        component_score = sum(1 for indicator in component_indicators if re.search(indicator, content))
        
        if component_score >= 2:
            patterns.append({
                'type': 'COMPONENT_PATTERN',
                'confidence': 0.85,
                'evidence': [f"Component pattern indicators: {component_score}"],
                'scope': 'file'
            })
        
        return patterns
    
    def analyze_data_flow(self, pois: Dict, relationships: List[Dict], content: str) -> List[Dict[str, Any]]:
        """Analyze JavaScript data flow patterns"""
        flows = []
        
        # Promise/Async flow detection
        async_indicators = [
            r'async\s+function',
            r'await\s+',
            r'\.then\s*\(',
            r'\.catch\s*\(',
            r'Promise\.',
        ]
        
        async_score = sum(1 for indicator in async_indicators if re.search(indicator, content))
        
        if async_score >= 2:
            flows.append({
                'type': 'ASYNC_DATA_FLOW',
                'confidence': 0.8,
                'patterns': async_score,
                'evidence': [f"Asynchronous data flow patterns: {async_score}"],
                'scope': 'file'
            })
        
        return flows
    
    def analyze_dependency_injection(self, pois: Dict, relationships: List[Dict], content: str) -> List[Dict[str, Any]]:
        """Detect JavaScript dependency injection patterns"""
        return []  # Simplified for now
    
    def analyze_cross_cutting_concerns(self, pois: Dict, relationships: List[Dict], content: str) -> List[Dict[str, Any]]:
        """Identify JavaScript cross-cutting concerns"""
        concerns = []
        
        # Console logging detection
        console_patterns = [
            r'console\.log',
            r'console\.error',
            r'console\.warn',
            r'console\.info',
        ]
        
        console_score = sum(len(re.findall(pattern, content)) for pattern in console_patterns)
        
        if console_score >= 3:
            concerns.append({
                'type': 'LOGGING_CONCERN',
                'confidence': 0.8,
                'occurrences': console_score,
                'evidence': [f"Console logging: {console_score} occurrences"],
                'scope': 'file'
            })
        
        return concerns

# ================================
# SEMANTIC ANALYSIS REGISTRY
# ================================

class SemanticPluginRegistry:
    """Registry for semantic analysis plugins - co-located"""
    
    def __init__(self):
        self.plugins = {}
        self._register_built_in_plugins()
    
    def _register_built_in_plugins(self):
        """Register all built-in semantic plugins"""
        self.plugins['python'] = PythonSemanticPlugin()
        self.plugins['javascript'] = JavaScriptSemanticPlugin()
    
    def get_plugin(self, language: str) -> BaseSemanticPlugin:
        """Get semantic plugin for specific language"""
        return self.plugins.get(language, self.plugins['python'])

# ================================
# CONTEXT ANALYZER AGENT
# ================================

class ContextAnalyzerAgent(BaseXAgent):
    """Performs semantic analysis to find higher-level patterns and context"""
    
    def __init__(self):
        super().__init__("ContextAnalyzerAgent")
        self.plugin_registry = SemanticPluginRegistry()
    
    def _process_intelligence(self, parsed_input: etree.Element) -> dict:
        """Perform semantic analysis using language-specific plugins"""
        
        # Extract metadata
        file_path = self._get_text_content(parsed_input, 'FilePath', 'unknown')
        content_length = int(self._get_text_content(parsed_input, 'ContentLength', '0'))
        language = self._get_text_content(parsed_input, 'Language', 'python')
        total_relationships = int(self._get_text_content(parsed_input, 'TotalRelationships', '0'))
        
        # Extract original content and existing relationships
        content = self._get_text_content(parsed_input, 'Content', '')
        relationships = self._extract_relationships_from_xml(parsed_input)
        pois = self._extract_pois_from_previous_analysis(parsed_input, content)
        
        # Get appropriate semantic plugin
        plugin = self.plugin_registry.get_plugin(language)
        
        # Perform all types of semantic analysis
        semantic_analysis = {
            'design_patterns': plugin.detect_design_patterns(pois, relationships, content),
            'architectural_patterns': plugin.detect_architectural_patterns(pois, relationships, content),
            'data_flows': plugin.analyze_data_flow(pois, relationships, content),
            'dependency_injection': plugin.analyze_dependency_injection(pois, relationships, content),
            'cross_cutting_concerns': plugin.analyze_cross_cutting_concerns(pois, relationships, content)
        }
        
        # Calculate semantic insights
        total_patterns = sum(len(patterns) for patterns in semantic_analysis.values())
        pattern_types = []
        for analysis_type, patterns in semantic_analysis.items():
            if patterns:
                pattern_types.extend([p.get('type', analysis_type) for p in patterns])
        
        # Generate context scores
        context_scores = self._calculate_context_scores(semantic_analysis, pois, relationships)
        
        return {
            'file_path': file_path,
            'content_length': content_length,
            'language': language,
            'plugin_used': f"{language}_semantic_plugin",
            'input_relationships': total_relationships,
            'semantic_analysis': semantic_analysis,
            'total_patterns': total_patterns,
            'pattern_types': list(set(pattern_types)),
            'context_scores': context_scores,
            'original_pois': pois,
            'original_relationships': relationships
        }
    
    def _get_text_content(self, element: etree.Element, tag_name: str, default: str = '') -> str:
        """Safely extract text content from XML element"""
        found = element.find(f'.//{tag_name}')
        return found.text if found is not None and found.text else default
    
    def _extract_relationships_from_xml(self, parsed_input: etree.Element) -> List[Dict]:
        """Extract relationships from previous agent's XML output"""
        relationships = []
        
        rel_elements = parsed_input.findall('.//Relationship')
        for rel_elem in rel_elements:
            relationship = {
                'from': rel_elem.get('from', ''),
                'to': rel_elem.get('to', ''),
                'type': rel_elem.get('type', ''),
                'confidence': float(rel_elem.get('confidence', 0.0)),
                'evidence': rel_elem.text or ''
            }
            
            # Add optional attributes
            for attr in ['line', 'source_module']:
                if rel_elem.get(attr):
                    relationship[attr] = rel_elem.get(attr)
            
            relationships.append(relationship)
        
        return relationships
    
    def _extract_pois_from_previous_analysis(self, parsed_input: etree.Element, content: str) -> Dict:
        """Reconstruct POIs from content since they might not be in RelationshipAnalysis XML"""
        # For now, do basic extraction from content
        # In a full implementation, we'd parse from previous agent's POI data
        pois = {'functions': [], 'classes': [], 'imports': [], 'variables': [], 'decorators': []}
        
        # Basic function extraction
        for match in re.finditer(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)', content):
            pois['functions'].append({
                'name': match.group(1),
                'line': content[:match.start()].count('\n') + 1
            })
        
        # Basic class extraction
        for match in re.finditer(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)', content):
            pois['classes'].append({
                'name': match.group(1),
                'line': content[:match.start()].count('\n') + 1
            })
        
        return pois
    
    def _calculate_context_scores(self, semantic_analysis: Dict, pois: Dict, relationships: List[Dict]) -> Dict:
        """Calculate context quality scores"""
        scores = {}
        
        # Pattern Density Score
        total_pois = sum(len(poi_list) for poi_list in pois.values())
        total_patterns = sum(len(patterns) for patterns in semantic_analysis.values())
        
        scores['pattern_density'] = min(1.0, total_patterns / max(1, total_pois * 0.1))
        
        # Architectural Maturity Score
        architectural_patterns = semantic_analysis.get('architectural_patterns', [])
        design_patterns = semantic_analysis.get('design_patterns', [])
        
        scores['architectural_maturity'] = min(1.0, (len(architectural_patterns) * 0.3 + len(design_patterns) * 0.2))
        
        # Code Quality Score (based on cross-cutting concerns)
        concerns = semantic_analysis.get('cross_cutting_concerns', [])
        quality_indicators = ['LOGGING_CONCERN', 'ERROR_HANDLING_CONCERN', 'VALIDATION_CONCERN']
        quality_score = sum(1 for concern in concerns if concern.get('type') in quality_indicators)
        
        scores['code_quality'] = min(1.0, quality_score / 3.0)
        
        # Overall Context Score
        scores['overall_context'] = (
            scores['pattern_density'] * 0.3 +
            scores['architectural_maturity'] * 0.4 +
            scores['code_quality'] * 0.3
        )
        
        return scores
    
    def _generate_xml(self, result: dict) -> str:
        """Generate XML output with semantic analysis results"""
        
        xml_parts = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<SemanticAnalysisResult>',
            f'  <FilePath>{result["file_path"]}</FilePath>',
            f'  <ContentLength>{result["content_length"]}</ContentLength>',
            f'  <Language>{result["language"]}</Language>',
            f'  <PluginUsed>{result["plugin_used"]}</PluginUsed>',
            f'  <InputRelationships>{result["input_relationships"]}</InputRelationships>',
            f'  <TotalPatterns>{result["total_patterns"]}</TotalPatterns>',
            f'  <PatternTypes>{", ".join(result["pattern_types"])}</PatternTypes>',
            '  <ContextScores>'
        ]
        
        # Add context scores
        for score_name, score_value in result['context_scores'].items():
            xml_parts.append(f'    <Score name="{score_name}" value="{score_value:.3f}"/>')
        
        xml_parts.append('  </ContextScores>')
        xml_parts.append('  <SemanticAnalysis>')
        
        # Add semantic analysis results
        for analysis_type, patterns in result['semantic_analysis'].items():
            xml_parts.append(f'    <{analysis_type.title()}>')
            
            for pattern in patterns:
                pattern_xml = f'      <Pattern type="{pattern.get("type", "")}" confidence="{pattern.get("confidence", 0.0)}"'
                
                # Add optional attributes
                for attr in ['class', 'method', 'function', 'variable', 'scope', 'line']:
                    if attr in pattern:
                        pattern_xml += f' {attr}="{pattern[attr]}"'
                
                pattern_xml += f'>{"; ".join(pattern.get("evidence", []))}</Pattern>'
                xml_parts.append(pattern_xml)
            
            xml_parts.append(f'    </{analysis_type.title()}>')
        
        xml_parts.extend([
            '  </SemanticAnalysis>',
            f'  <ProcessingTime>{self.metrics["total_time"]:.2f}ms</ProcessingTime>',
            '</SemanticAnalysisResult>'
        ])
        
        return '\n'.join(xml_parts)

# Test the context analyzer agent
if __name__ == "__main__":
    print("🧪 Testing Context Analyzer Agent")
    
    # Create sample XML input (from RelationshipDetector output)
    sample_input = """<?xml version="1.0" encoding="UTF-8"?>
<RelationshipAnalysisResult>
  <FilePath>sample_code.py</FilePath>
  <ContentLength>5836</ContentLength>
  <Language>python</Language>
  <PluginUsed>python_relationship_plugin</PluginUsed>
  <InputPOIs>56</InputPOIs>
  <TotalRelationships>3</TotalRelationships>
  <RelationshipTypes>CALLS</RelationshipTypes>
  <Relationships>
    <Relationship from="code" to="__init__" type="CALLS" confidence="0.85">Function call found</Relationship>
    <Relationship from="code" to="connect" type="CALLS" confidence="0.85">Function call found</Relationship>
    <Relationship from="UserService" to="DatabaseConnection" type="USES" confidence="0.9">Dependency injection</Relationship>
  </Relationships>
  <Content><![CDATA[
import os
import asyncio
from typing import Dict
from abc import ABC, abstractmethod

class DatabaseConnection(ABC):
    def __init__(self, connection_string):
        self.connection_string = connection_string
    
    @abstractmethod
    def connect(self):
        pass

class PostgreSQLConnection(DatabaseConnection):
    def __init__(self, host, port):
        super().__init__(f"postgresql://{host}:{port}")
        self.host = host
    
    def connect(self):
        return True

class UserService:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def create_user(self, user_data):
        try:
            self.db.connect()
            return self.process_user_data(user_data)
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def process_user_data(self, data):
        if not data:
            raise ValueError("User data is required")
        return {"user_id": "123", "status": "created"}

async def initialize_application():
    config = load_configuration("config.json")
    db_connection = PostgreSQLConnection("localhost", 5432)
    user_service = UserService(db_connection)
    return user_service
  ]]></Content>
</RelationshipAnalysisResult>"""
    
    # Test the agent
    agent = ContextAnalyzerAgent()
    result = agent.process(sample_input)
    
    print(f"✅ Processing completed in {agent.metrics['total_time']:.2f}ms")
    print(f"📄 Result length: {len(result)} characters")
    print("\n📊 Semantic analysis result:")
    print(result)

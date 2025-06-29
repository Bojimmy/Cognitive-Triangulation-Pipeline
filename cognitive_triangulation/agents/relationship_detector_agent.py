#!/usr/bin/env python3
"""
RelationshipDetector Agent with Co-Located Plugins
Second agent in the Cognitive Triangulation pipeline - finds relationships between POIs
"""

import re
import time
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Tuple
from lxml import etree

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
            return f"<Error agent='{self.agent_type}'>Error processing: {str(e)}</Error>"
    
    @abstractmethod
    def _process_intelligence(self, parsed_input: etree.Element) -> dict:
        """Agent-specific logic - implemented by subclasses"""
        pass
    
    @abstractmethod
    def _generate_xml(self, result: dict) -> str:
        """Generate XML for next agent - implemented by subclasses"""
        pass

# ================================
# RELATIONSHIP DETECTION PLUGINS
# ================================

class BaseRelationshipPlugin(ABC):
    """Base class for relationship detection plugins - co-located"""
    
    @abstractmethod
    def get_relationship_types(self) -> List[str]:
        """Return the relationship types this plugin can detect"""
        pass
    
    @abstractmethod
    def detect_import_relationships(self, pois: Dict, content: str) -> List[Dict[str, Any]]:
        """Detect import/dependency relationships"""
        pass
    
    @abstractmethod
    def detect_call_relationships(self, pois: Dict, content: str) -> List[Dict[str, Any]]:
        """Detect function/method call relationships"""
        pass
    
    @abstractmethod
    def detect_inheritance_relationships(self, pois: Dict, content: str) -> List[Dict[str, Any]]:
        """Detect class inheritance relationships"""
        pass
    
    @abstractmethod
    def detect_composition_relationships(self, pois: Dict, content: str) -> List[Dict[str, Any]]:
        """Detect composition/aggregation relationships"""
        pass
    
    @abstractmethod
    def detect_usage_relationships(self, pois: Dict, content: str) -> List[Dict[str, Any]]:
        """Detect variable/object usage relationships"""
        pass

class PythonRelationshipPlugin(BaseRelationshipPlugin):
    """Python-specific relationship detection plugin"""
    
    def get_relationship_types(self) -> List[str]:
        return ["IMPORTS", "CALLS", "INHERITS_FROM", "CONTAINS", "USES", "DECORATES", "INSTANTIATES"]
    
    def detect_import_relationships(self, pois: Dict, content: str) -> List[Dict[str, Any]]:
        """Detect Python import relationships"""
        relationships = []
        
        imports = pois.get('imports', [])
        functions = pois.get('functions', [])
        classes = pois.get('classes', [])
        
        # Map module names to imported items
        for import_poi in imports:
            module_name = import_poi.get('module', '')
            imported_items = import_poi.get('items', [])
            
            # Check if imported items are used in functions or classes
            for item in imported_items:
                # Look for usage patterns in content
                usage_patterns = [
                    rf'\b{re.escape(item)}\s*\(',  # Function call
                    rf'\b{re.escape(item)}\s*\.',  # Method access
                    rf'\b{re.escape(item)}\s*\[',  # Index access
                    rf'=\s*{re.escape(item)}\b'    # Assignment
                ]
                
                for pattern in usage_patterns:
                    if re.search(pattern, content):
                        relationships.append({
                            'from': 'code',
                            'to': item,
                            'type': 'IMPORTS',
                            'confidence': 0.9,
                            'source_module': module_name,
                            'line': import_poi.get('line', 0),
                            'evidence': f'Import and usage pattern found: {pattern}'
                        })
                        break
        
        return relationships
    
    def detect_call_relationships(self, pois: Dict, content: str) -> List[Dict[str, Any]]:
        """Detect Python function call relationships"""
        relationships = []
        
        functions = pois.get('functions', [])
        
        for func in functions:
            func_name = func['name']
            
            # Look for function calls in content
            call_patterns = [
                rf'{re.escape(func_name)}\s*\(',  # Direct call
                rf'self\.{re.escape(func_name)}\s*\(',  # Method call
                rf'super\(\)\.{re.escape(func_name)}\s*\('  # Super call
            ]
            
            for pattern in call_patterns:
                matches = list(re.finditer(pattern, content))
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    
                    # Don't count the function definition itself
                    if line_num != func['line']:
                        relationships.append({
                            'from': 'code',
                            'to': func_name,
                            'type': 'CALLS',
                            'confidence': 0.85,
                            'call_line': line_num,
                            'definition_line': func['line'],
                            'evidence': f'Function call found at line {line_num}'
                        })
        
        return relationships
    
    def detect_inheritance_relationships(self, pois: Dict, content: str) -> List[Dict[str, Any]]:
        """Detect Python class inheritance relationships"""
        relationships = []
        
        classes = pois.get('classes', [])
        
        for cls in classes:
            class_name = cls['name']
            parent_classes = cls.get('parent_classes', [])
            
            for parent in parent_classes:
                if parent and parent != 'object':  # Skip default object inheritance
                    relationships.append({
                        'from': class_name,
                        'to': parent,
                        'type': 'INHERITS_FROM',
                        'confidence': 0.95,
                        'child_line': cls['line'],
                        'evidence': f'Class {class_name} explicitly inherits from {parent}'
                    })
        
        return relationships
    
    def detect_composition_relationships(self, pois: Dict, content: str) -> List[Dict[str, Any]]:
        """Detect composition relationships (class contains other classes)"""
        relationships = []
        
        classes = pois.get('classes', [])
        variables = pois.get('variables', [])
        
        # Look for instance variable assignments that suggest composition
        for cls in classes:
            class_name = cls['name']
            class_line = cls['line']
            
            # Find class body (rough estimation)
            class_start = content.split('\n')[class_line-1:class_line+20]
            class_body = '\n'.join(class_start)
            
            # Look for self.variable = ClassName() patterns
            composition_pattern = r'self\.([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([A-Z][a-zA-Z0-9_]*)\s*\('
            
            for match in re.finditer(composition_pattern, class_body):
                attribute_name = match.group(1)
                composed_class = match.group(2)
                
                relationships.append({
                    'from': class_name,
                    'to': composed_class,
                    'type': 'CONTAINS',
                    'confidence': 0.8,
                    'attribute_name': attribute_name,
                    'evidence': f'Class {class_name} contains instance of {composed_class}'
                })
        
        return relationships
    
    def detect_usage_relationships(self, pois: Dict, content: str) -> List[Dict[str, Any]]:
        """Detect variable usage relationships"""
        relationships = []
        
        variables = pois.get('variables', [])
        functions = pois.get('functions', [])
        
        # Look for variable usage in functions
        for var in variables:
            var_name = var['name']
            var_line = var['line']
            
            # Find all uses of this variable
            usage_pattern = rf'\b{re.escape(var_name)}\b'
            matches = list(re.finditer(usage_pattern, content))
            
            for match in matches:
                usage_line = content[:match.start()].count('\n') + 1
                
                # Don't count the variable definition itself
                if usage_line != var_line:
                    # Check if usage is within a function
                    for func in functions:
                        func_start = func['line']
                        # Rough estimate: function body is ~20 lines
                        func_end = func_start + 20
                        
                        if func_start <= usage_line <= func_end:
                            relationships.append({
                                'from': func['name'],
                                'to': var_name,
                                'type': 'USES',
                                'confidence': 0.7,
                                'usage_line': usage_line,
                                'variable_line': var_line,
                                'evidence': f'Function {func["name"]} uses variable {var_name}'
                            })
                            break
        
        return relationships

class JavaScriptRelationshipPlugin(BaseRelationshipPlugin):
    """JavaScript-specific relationship detection plugin"""
    
    def get_relationship_types(self) -> List[str]:
        return ["IMPORTS", "CALLS", "EXTENDS", "REQUIRES", "EXPORTS", "INSTANTIATES"]
    
    def detect_import_relationships(self, pois: Dict, content: str) -> List[Dict[str, Any]]:
        """Detect JavaScript import/require relationships"""
        relationships = []
        
        imports = pois.get('imports', [])
        
        for import_poi in imports:
            module_name = import_poi.get('module', '')
            imported_items = import_poi.get('items', [])
            
            for item in imported_items:
                # Look for usage in JavaScript
                usage_patterns = [
                    rf'{re.escape(item)}\s*\(',
                    rf'{re.escape(item)}\s*\.',
                    rf'new\s+{re.escape(item)}\s*\('
                ]
                
                for pattern in usage_patterns:
                    if re.search(pattern, content):
                        relationships.append({
                            'from': 'code',
                            'to': item,
                            'type': 'IMPORTS',
                            'confidence': 0.85,
                            'source_module': module_name,
                            'evidence': f'Import and usage found'
                        })
                        break
        
        return relationships
    
    def detect_call_relationships(self, pois: Dict, content: str) -> List[Dict[str, Any]]:
        """Detect JavaScript function calls"""
        relationships = []
        
        functions = pois.get('functions', [])
        
        for func in functions:
            func_name = func['name']
            
            # JavaScript call patterns
            call_patterns = [
                rf'{re.escape(func_name)}\s*\(',
                rf'\.{re.escape(func_name)}\s*\(',
                rf'this\.{re.escape(func_name)}\s*\('
            ]
            
            for pattern in call_patterns:
                matches = list(re.finditer(pattern, content))
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    
                    if line_num != func['line']:
                        relationships.append({
                            'from': 'code',
                            'to': func_name,
                            'type': 'CALLS',
                            'confidence': 0.8,
                            'call_line': line_num,
                            'evidence': f'Function call at line {line_num}'
                        })
        
        return relationships
    
    def detect_inheritance_relationships(self, pois: Dict, content: str) -> List[Dict[str, Any]]:
        """Detect JavaScript class extends relationships"""
        relationships = []
        
        classes = pois.get('classes', [])
        
        for cls in classes:
            parent_classes = cls.get('parent_classes', [])
            for parent in parent_classes:
                if parent:
                    relationships.append({
                        'from': cls['name'],
                        'to': parent,
                        'type': 'EXTENDS',
                        'confidence': 0.9,
                        'evidence': f'Class extends {parent}'
                    })
        
        return relationships
    
    def detect_composition_relationships(self, pois: Dict, content: str) -> List[Dict[str, Any]]:
        """Detect JavaScript composition patterns"""
        return []  # Simplified for now
    
    def detect_usage_relationships(self, pois: Dict, content: str) -> List[Dict[str, Any]]:
        """Detect JavaScript variable usage"""
        return []  # Simplified for now

# ================================
# RELATIONSHIP PLUGIN REGISTRY
# ================================

class RelationshipPluginRegistry:
    """Registry for relationship detection plugins - co-located"""
    
    def __init__(self):
        self.plugins = {}
        self._register_built_in_plugins()
    
    def _register_built_in_plugins(self):
        """Register all built-in relationship plugins"""
        self.plugins['python'] = PythonRelationshipPlugin()
        self.plugins['javascript'] = JavaScriptRelationshipPlugin()
    
    def get_plugin(self, language: str) -> BaseRelationshipPlugin:
        """Get relationship plugin for specific language"""
        return self.plugins.get(language, self.plugins['python'])
    
    def detect_language_from_pois(self, pois: Dict, file_path: str = "") -> str:
        """Detect language from POI structure and file path"""
        if file_path.endswith('.py'):
            return 'python'
        elif file_path.endswith(('.js', '.jsx', '.ts', '.tsx')):
            return 'javascript'
        
        # Content-based detection from import patterns
        imports = pois.get('imports', [])
        for imp in imports:
            items = imp.get('items', [])
            if any(item in ['Dict', 'List', 'Optional'] for item in items):
                return 'python'
            elif any(item in ['React', 'useState', 'useEffect'] for item in items):
                return 'javascript'
        
        return 'python'  # Default

# ================================
# RELATIONSHIP DETECTOR AGENT
# ================================

class RelationshipDetectorAgent(BaseXAgent):
    """Detects relationships between POIs using co-located plugins"""
    
    def __init__(self):
        super().__init__("RelationshipDetectorAgent")
        self.plugin_registry = RelationshipPluginRegistry()
    
    def _process_intelligence(self, parsed_input: etree.Element) -> dict:
        """Extract relationships from POIs using language-specific plugins"""
        
        # Extract metadata
        file_path = self._get_text_content(parsed_input, 'FilePath', 'unknown')
        content_length = int(self._get_text_content(parsed_input, 'ContentLength', '0'))
        total_pois = int(self._get_text_content(parsed_input, 'TotalPOIs', '0'))
        
        # Extract original file content if available
        content = self._get_text_content(parsed_input, 'Content', '')
        
        # Extract POIs from XML
        pois = self._extract_pois_from_xml(parsed_input)
        
        # Detect language and get appropriate plugin
        language = self.plugin_registry.detect_language_from_pois(pois, file_path)
        plugin = self.plugin_registry.get_plugin(language)
        
        # Detect all relationship types using the plugin
        all_relationships = []
        
        all_relationships.extend(plugin.detect_import_relationships(pois, content))
        all_relationships.extend(plugin.detect_call_relationships(pois, content))
        all_relationships.extend(plugin.detect_inheritance_relationships(pois, content))
        all_relationships.extend(plugin.detect_composition_relationships(pois, content))
        all_relationships.extend(plugin.detect_usage_relationships(pois, content))
        
        # Add confidence scoring and deduplication
        deduplicated_relationships = self._deduplicate_relationships(all_relationships)
        high_confidence_relationships = [r for r in deduplicated_relationships if r.get('confidence', 0) >= 0.7]
        
        return {
            'file_path': file_path,
            'content_length': content_length,
            'language': language,
            'plugin_used': f"{language}_relationship_plugin",
            'input_pois': total_pois,
            'pois': pois,
            'relationships': high_confidence_relationships,
            'total_relationships': len(high_confidence_relationships),
            'relationship_types': list(set(r['type'] for r in high_confidence_relationships))
        }
    
    def _get_text_content(self, element: etree.Element, tag_name: str, default: str = '') -> str:
        """Safely extract text content from XML element"""
        found = element.find(f'.//{tag_name}')
        return found.text if found is not None and found.text else default
    
    def _extract_pois_from_xml(self, parsed_input: etree.Element) -> Dict[str, List[Dict]]:
        """Extract POIs from previous agent's XML output"""
        pois = {'functions': [], 'classes': [], 'imports': [], 'variables': [], 'decorators': []}
        
        # Find POIs section
        pois_section = parsed_input.find('.//POIs')
        if pois_section is None:
            return pois
        
        # Extract each POI type
        for poi_type in pois.keys():
            poi_elements = pois_section.findall(f'.//{poi_type.title()}//POI')
            for poi_elem in poi_elements:
                poi_data = {
                    'name': poi_elem.get('name', ''),
                    'type': poi_elem.get('type', ''),
                    'line': int(poi_elem.get('line', 0))
                }
                
                # Add type-specific attributes
                if poi_type == 'functions':
                    poi_data['is_async'] = poi_elem.get('async', 'False') == 'True'
                    poi_data['is_private'] = poi_elem.get('private', 'False') == 'True'
                elif poi_type == 'classes':
                    poi_data['is_abstract'] = poi_elem.get('abstract', 'False') == 'True'
                    # TODO: Extract parent classes from previous agent
                    poi_data['parent_classes'] = []
                
                pois[poi_type].append(poi_data)
        
        return pois
    
    def _deduplicate_relationships(self, relationships: List[Dict]) -> List[Dict]:
        """Remove duplicate relationships and merge evidence"""
        seen = {}
        deduplicated = []
        
        for rel in relationships:
            key = f"{rel['from']}:{rel['to']}:{rel['type']}"
            
            if key in seen:
                # Merge evidence and take highest confidence
                existing = seen[key]
                existing['confidence'] = max(existing.get('confidence', 0), rel.get('confidence', 0))
                existing['evidence'] = f"{existing.get('evidence', '')}; {rel.get('evidence', '')}"
            else:
                seen[key] = rel
                deduplicated.append(rel)
        
        return deduplicated
    
    def _generate_xml(self, result: dict) -> str:
        """Generate XML output with detected relationships"""
        
        xml_parts = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<RelationshipAnalysisResult>',
            f'  <FilePath>{result["file_path"]}</FilePath>',
            f'  <ContentLength>{result["content_length"]}</ContentLength>',
            f'  <Language>{result["language"]}</Language>',
            f'  <PluginUsed>{result["plugin_used"]}</PluginUsed>',
            f'  <InputPOIs>{result["input_pois"]}</InputPOIs>',
            f'  <TotalRelationships>{result["total_relationships"]}</TotalRelationships>',
            f'  <RelationshipTypes>{", ".join(result["relationship_types"])}</RelationshipTypes>',
            '  <Relationships>'
        ]
        
        # Add all detected relationships
        for rel in result['relationships']:
            rel_xml = (
                f'    <Relationship '
                f'from="{rel["from"]}" '
                f'to="{rel["to"]}" '
                f'type="{rel["type"]}" '
                f'confidence="{rel.get("confidence", 0.0)}"'
            )
            
            # Add optional attributes
            if 'line' in rel:
                rel_xml += f' line="{rel["line"]}"'
            if 'source_module' in rel:
                rel_xml += f' source_module="{rel["source_module"]}"'
            
            rel_xml += f'>{rel.get("evidence", "")}</Relationship>'
            xml_parts.append(rel_xml)
        
        xml_parts.extend([
            '  </Relationships>',
            f'  <ProcessingTime>{self.metrics["total_time"]:.2f}ms</ProcessingTime>',
            '</RelationshipAnalysisResult>'
        ])
        
        return '\n'.join(xml_parts)

# Test the relationship detector agent
if __name__ == "__main__":
    print("🧪 Testing Relationship Detector Agent")
    
    # Create sample XML input (from CodeScout output)
    sample_input = """<?xml version="1.0" encoding="UTF-8"?>
<CodeAnalysisResult>
  <FilePath>sample_code.py</FilePath>
  <ContentLength>5836</ContentLength>
  <Language>python</Language>
  <TotalPOIs>56</TotalPOIs>
  <POIs>
    <Functions>
      <POI name="__init__" type="function" line="31" async="False" private="True"/>
      <POI name="connect" type="function" line="35" async="False" private="False"/>
      <POI name="initialize_application" type="function" line="138" async="True" private="False"/>
    </Functions>
    <Classes>
      <POI name="DatabaseConnection" type="class" line="28" abstract="True"/>
      <POI name="PostgreSQLConnection" type="class" line="49" abstract="False"/>
      <POI name="UserService" type="class" line="84" abstract="False"/>
    </Classes>
    <Imports>
      <POI name="os" type="import" line="7"/>
      <POI name="asyncio" type="import" line="9"/>
      <POI name="typing" type="import" line="10"/>
    </Imports>
  </POIs>
  <Content><![CDATA[
# Sample content for relationship detection
import os
import asyncio
from typing import Dict

class DatabaseConnection:
    def __init__(self, connection_string):
        self.connection_string = connection_string
    
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
    
    async def initialize_application():
        config = load_configuration("config.json")
        db_connection = PostgreSQLConnection("localhost", 5432)
        user_service = UserService(db_connection)
        return user_service
  ]]></Content>
</CodeAnalysisResult>"""
    
    # Test the agent
    agent = RelationshipDetectorAgent()
    result = agent.process(sample_input)
    
    print(f"✅ Processing completed in {agent.metrics['total_time']:.2f}ms")
    print(f"📄 Result length: {len(result)} characters")
    print("\n📊 Relationship detection result:")
    print(result)

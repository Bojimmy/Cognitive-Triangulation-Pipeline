#!/usr/bin/env python3
"""
Co-Located Plugin Agent Implementation - Plugin logic in same file as agent
This is our "Approach B" for testing performance and output quality.
"""

import re
import time
from abc import ABC, abstractmethod
from typing import Dict, List, Any
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
            # Parse XML input
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
# CO-LOCATED PLUGIN CLASSES
# ================================

class BaseCodeAnalysisPlugin(ABC):
    """Base class for code analysis plugins - co-located in same file"""
    
    @abstractmethod
    def get_domain_name(self) -> str:
        """Return the domain this plugin handles"""
        pass
    
    @abstractmethod
    def extract_functions(self, content: str) -> List[Dict[str, Any]]:
        """Extract function definitions"""
        pass
    
    @abstractmethod
    def extract_classes(self, content: str) -> List[Dict[str, Any]]:
        """Extract class definitions"""
        pass
    
    @abstractmethod
    def extract_imports(self, content: str) -> List[Dict[str, Any]]:
        """Extract import statements"""
        pass
    
    @abstractmethod
    def extract_variables(self, content: str) -> List[Dict[str, Any]]:
        """Extract variable assignments"""
        pass
    
    @abstractmethod
    def extract_decorators(self, content: str) -> List[Dict[str, Any]]:
        """Extract decorator usage"""
        pass
    
    @abstractmethod
    def detect_relationships(self, content: str, pois: Dict) -> List[Dict[str, str]]:
        """Detect relationships between POIs"""
        pass

class PythonCodeAnalysisPlugin(BaseCodeAnalysisPlugin):
    """Python-specific code analysis plugin - co-located"""
    
    def get_domain_name(self) -> str:
        return "python_code"
    
    def extract_functions(self, content: str) -> List[Dict[str, Any]]:
        """Extract Python function definitions"""
        functions = []
        
        # Regular expression for function definitions
        function_pattern = r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\):'
        
        for match in re.finditer(function_pattern, content):
            func_name = match.group(1)
            start_pos = match.start()
            line_number = content[:start_pos].count('\n') + 1
            
            functions.append({
                'name': func_name,
                'type': 'function',
                'line': line_number,
                'is_async': 'async def' in content[max(0, start_pos-10):start_pos+20],
                'is_private': func_name.startswith('_'),
                'is_magic': func_name.startswith('__') and func_name.endswith('__')
            })
        
        return functions
    
    def extract_classes(self, content: str) -> List[Dict[str, Any]]:
        """Extract Python class definitions"""
        classes = []
        
        # Regular expression for class definitions
        class_pattern = r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:\([^)]*\))?:'
        
        for match in re.finditer(class_pattern, content):
            class_name = match.group(1)
            start_pos = match.start()
            line_number = content[:start_pos].count('\n') + 1
            
            # Extract inheritance info
            inheritance_match = re.search(r'class\s+' + class_name + r'\s*\(([^)]+)\):', content[start_pos:start_pos+100])
            parent_classes = []
            if inheritance_match:
                parents_str = inheritance_match.group(1)
                parent_classes = [p.strip() for p in parents_str.split(',')]
            
            classes.append({
                'name': class_name,
                'type': 'class',
                'line': line_number,
                'parent_classes': parent_classes,
                'is_abstract': 'ABC' in parent_classes or '@abstractmethod' in content
            })
        
        return classes
    
    def extract_imports(self, content: str) -> List[Dict[str, Any]]:
        """Extract Python import statements"""
        imports = []
        
        # Pattern for different import styles
        import_patterns = [
            (r'import\s+([a-zA-Z_][a-zA-Z0-9_.]*)', 'import'),
            (r'from\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s+import\s+(.+)', 'from_import')
        ]
        
        for pattern, import_type in import_patterns:
            for match in re.finditer(pattern, content):
                start_pos = match.start()
                line_number = content[:start_pos].count('\n') + 1
                
                if import_type == 'import':
                    module_name = match.group(1)
                    imported_items = [module_name]
                else:  # from_import
                    module_name = match.group(1)
                    items_str = match.group(2)
                    imported_items = [item.strip() for item in items_str.split(',')]
                
                imports.append({
                    'name': module_name,
                    'module': module_name,
                    'items': imported_items,
                    'type': 'import',
                    'line': line_number
                })
        
        return imports
    
    def extract_variables(self, content: str) -> List[Dict[str, Any]]:
        """Extract Python variable assignments"""
        variables = []
        
        # Simple pattern for variable assignments (class level and module level)
        var_pattern = r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*[=:]'
        
        for line_num, line in enumerate(content.split('\n'), 1):
            line = line.strip()
            if line and not line.startswith('#'):
                match = re.match(var_pattern, line)
                if match:
                    var_name = match.group(1)
                    if not var_name in ['def', 'class', 'if', 'for', 'while', 'try', 'except']:
                        variables.append({
                            'name': var_name,
                            'type': 'variable',
                            'line': line_num,
                            'is_constant': var_name.isupper()
                        })
        
        return variables
    
    def extract_decorators(self, content: str) -> List[Dict[str, Any]]:
        """Extract Python decorator usage"""
        decorators = []
        
        decorator_pattern = r'@([a-zA-Z_][a-zA-Z0-9_.]*)'
        
        for match in re.finditer(decorator_pattern, content):
            decorator_name = match.group(1)
            start_pos = match.start()
            line_number = content[:start_pos].count('\n') + 1
            
            decorators.append({
                'name': decorator_name,
                'type': 'decorator',
                'line': line_number
            })
        
        return decorators
    
    def detect_relationships(self, content: str, pois: Dict) -> List[Dict[str, str]]:
        """Detect relationships between POIs in Python code"""
        relationships = []
        
        # Extract class names for relationship detection
        class_names = [cls['name'] for cls in pois['classes']]
        function_names = [func['name'] for func in pois['functions']]
        
        # Detect inheritance relationships
        for cls in pois['classes']:
            for parent in cls['parent_classes']:
                relationships.append({
                    'from': cls['name'],
                    'to': parent,
                    'type': 'INHERITS_FROM',
                    'confidence': '0.95'
                })
        
        # Detect function calls (basic pattern matching)
        for func_name in function_names:
            call_pattern = rf'{func_name}\s*\('
            if re.search(call_pattern, content):
                relationships.append({
                    'from': 'code',
                    'to': func_name,
                    'type': 'CALLS',
                    'confidence': '0.8'
                })
        
        return relationships

class JavaScriptCodeAnalysisPlugin(BaseCodeAnalysisPlugin):
    """JavaScript-specific code analysis plugin - co-located"""
    
    def get_domain_name(self) -> str:
        return "javascript_code"
    
    def extract_functions(self, content: str) -> List[Dict[str, Any]]:
        """Extract JavaScript function definitions"""
        functions = []
        
        # Patterns for different JavaScript function styles
        function_patterns = [
            r'function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
            r'const\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>',
            r'([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(?:async\s+)?function\s*\('
        ]
        
        for pattern in function_patterns:
            for match in re.finditer(pattern, content):
                func_name = match.group(1)
                start_pos = match.start()
                line_number = content[:start_pos].count('\n') + 1
                
                functions.append({
                    'name': func_name,
                    'type': 'function',
                    'line': line_number,
                    'is_async': 'async' in content[start_pos:start_pos+50],
                    'is_arrow': '=>' in content[start_pos:start_pos+100]
                })
        
        return functions
    
    def extract_classes(self, content: str) -> List[Dict[str, Any]]:
        """Extract JavaScript class definitions"""
        classes = []
        
        class_pattern = r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:extends\s+([a-zA-Z_][a-zA-Z0-9_]*))?\s*{'
        
        for match in re.finditer(class_pattern, content):
            class_name = match.group(1)
            parent_class = match.group(2) if match.group(2) else None
            start_pos = match.start()
            line_number = content[:start_pos].count('\n') + 1
            
            classes.append({
                'name': class_name,
                'type': 'class',
                'line': line_number,
                'parent_classes': [parent_class] if parent_class else [],
                'is_abstract': False  # JavaScript doesn't have built-in abstract classes
            })
        
        return classes
    
    def extract_imports(self, content: str) -> List[Dict[str, Any]]:
        """Extract JavaScript import statements"""
        imports = []
        
        import_patterns = [
            (r'import\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+from\s+[\'"]([^\'"]+)[\'"]', 'default_import'),
            (r'import\s*{\s*([^}]+)\s*}\s*from\s+[\'"]([^\'"]+)[\'"]', 'named_import'),
            (r'const\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*require\([\'"]([^\'"]+)[\'"]\)', 'require')
        ]
        
        for pattern, import_type in import_patterns:
            for match in re.finditer(pattern, content):
                start_pos = match.start()
                line_number = content[:start_pos].count('\n') + 1
                
                if import_type == 'named_import':
                    imported_items = [item.strip() for item in match.group(1).split(',')]
                    module_name = match.group(2)
                else:
                    imported_items = [match.group(1)]
                    module_name = match.group(2)
                
                imports.append({
                    'name': module_name,
                    'module': module_name,
                    'items': imported_items,
                    'type': 'import',
                    'line': line_number
                })
        
        return imports
    
    def extract_variables(self, content: str) -> List[Dict[str, Any]]:
        """Extract JavaScript variable declarations"""
        variables = []
        
        var_patterns = [
            r'const\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            r'let\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            r'var\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        ]
        
        for pattern in var_patterns:
            for match in re.finditer(pattern, content):
                var_name = match.group(1)
                start_pos = match.start()
                line_number = content[:start_pos].count('\n') + 1
                
                variables.append({
                    'name': var_name,
                    'type': 'variable',
                    'line': line_number,
                    'is_constant': pattern.startswith('const')
                })
        
        return variables
    
    def extract_decorators(self, content: str) -> List[Dict[str, Any]]:
        """Extract JavaScript decorators (if any)"""
        # JavaScript doesn't have built-in decorators like Python
        return []
    
    def detect_relationships(self, content: str, pois: Dict) -> List[Dict[str, str]]:
        """Detect relationships in JavaScript code"""
        relationships = []
        
        # Basic inheritance detection
        for cls in pois['classes']:
            for parent in cls['parent_classes']:
                relationships.append({
                    'from': cls['name'],
                    'to': parent,
                    'type': 'EXTENDS',
                    'confidence': '0.95'
                })
        
        return relationships

# ================================
# PLUGIN REGISTRY (CO-LOCATED)
# ================================

class CoLocatedPluginRegistry:
    """Registry for co-located plugins - no external file loading"""
    
    def __init__(self):
        self.plugins = {}
        self._register_built_in_plugins()
    
    def _register_built_in_plugins(self):
        """Register all built-in plugins"""
        self.plugins['python'] = PythonCodeAnalysisPlugin()
        self.plugins['javascript'] = JavaScriptCodeAnalysisPlugin()
    
    def detect_language(self, content: str, file_path: str = "") -> str:
        """Detect programming language from content and file path"""
        # Simple language detection
        if file_path.endswith('.py'):
            return 'python'
        elif file_path.endswith(('.js', '.jsx', '.ts', '.tsx')):
            return 'javascript'
        
        # Content-based detection
        if 'def ' in content and 'import ' in content:
            return 'python'
        elif 'function ' in content and 'const ' in content:
            return 'javascript'
        
        # Default to Python
        return 'python'
    
    def get_plugin(self, language: str) -> BaseCodeAnalysisPlugin:
        """Get plugin for specific language"""
        return self.plugins.get(language, self.plugins['python'])

# ================================
# CO-LOCATED PLUGIN AGENT
# ================================

class CoLocatedPluginCodeScoutAgent(BaseXAgent):
    """Code Scout Agent using co-located plugins (no external file loading)"""
    
    def __init__(self):
        super().__init__("CoLocatedPluginCodeScoutAgent")
        self.plugin_registry = CoLocatedPluginRegistry()
    
    def _process_intelligence(self, parsed_input: etree.Element) -> dict:
        """Extract POIs using co-located plugin system"""
        
        # Extract content from XML
        content_elem = parsed_input.find('Content')
        content = content_elem.text if content_elem is not None else ""
        
        file_path_elem = parsed_input.find('FilePath')
        file_path = file_path_elem.text if file_path_elem is not None else "unknown"
        
        # Detect language and get appropriate plugin
        language = self.plugin_registry.detect_language(content, file_path)
        plugin = self.plugin_registry.get_plugin(language)
        
        # Use plugin to extract POIs
        pois = {
            'functions': plugin.extract_functions(content),
            'classes': plugin.extract_classes(content),
            'imports': plugin.extract_imports(content),
            'variables': plugin.extract_variables(content),
            'decorators': plugin.extract_decorators(content)
        }
        
        # Use plugin to detect relationships
        relationships = plugin.detect_relationships(content, pois)
        
        return {
            'file_path': file_path,
            'content': content,  # Include original content for next agent
            'content_length': len(content),
            'language': language,
            'plugin_used': plugin.get_domain_name(),
            'pois': pois,
            'relationships': relationships,
            'total_pois': sum(len(poi_list) for poi_list in pois.values())
        }
    
    def _generate_xml(self, result: dict) -> str:
        """Generate XML output with all discovered POIs and relationships"""
        
        xml_parts = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<CodeAnalysisResult>',
            f'  <FilePath>{result["file_path"]}</FilePath>',
            f'  <ContentLength>{result["content_length"]}</ContentLength>',
            f'  <Language>{result["language"]}</Language>',
            f'  <PluginUsed>{result["plugin_used"]}</PluginUsed>',
            f'  <TotalPOIs>{result["total_pois"]}</TotalPOIs>',
            '  <POIs>'
        ]
        
        # Add all POI types
        for poi_type, poi_list in result['pois'].items():
            xml_parts.append(f'    <{poi_type.title()}>')
            for poi in poi_list:
                poi_xml = f'      <POI name="{poi["name"]}" type="{poi["type"]}" line="{poi["line"]}"'
                
                # Add type-specific attributes
                if poi_type == 'functions':
                    poi_xml += f' async="{poi.get("is_async", False)}" private="{poi.get("is_private", False)}"'
                elif poi_type == 'classes':
                    poi_xml += f' abstract="{poi.get("is_abstract", False)}"'
                
                poi_xml += '/>'
                xml_parts.append(poi_xml)
            xml_parts.append(f'    </{poi_type.title()}>')
        
        xml_parts.extend([
            '  </POIs>',
            '  <Relationships>'
        ])
        
        # Add relationships
        for rel in result['relationships']:
            rel_xml = f'    <Relationship from="{rel["from"]}" to="{rel["to"]}" type="{rel["type"]}" confidence="{rel["confidence"]}"/>'
            xml_parts.append(rel_xml)
        
        xml_parts.extend([
            '  </Relationships>',
            f'  <ProcessingTime>{self.metrics["total_time"]:.2f}ms</ProcessingTime>',
            f'  <Content><![CDATA[{result.get("content", "")}]]></Content>',
            '</CodeAnalysisResult>'
        ])
        
        return '\n'.join(xml_parts)

# Test the co-located plugin agent
if __name__ == "__main__":
    print("🧪 Testing Co-Located Plugin Code Scout Agent")
    
    # Load sample code
    with open('sample_code.py', 'r') as f:
        test_content = f.read()
    
    # Create test XML
    test_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<CodeAnalysisInput>
    <FilePath>sample_code.py</FilePath>
    <Content><![CDATA[{test_content}]]></Content>
</CodeAnalysisInput>"""
    
    # Test the agent
    agent = CoLocatedPluginCodeScoutAgent()
    result = agent.process(test_xml)
    
    print(f"✅ Processing completed in {agent.metrics['total_time']:.2f}ms")
    print(f"📄 Result length: {len(result)} characters")
    print("\n📊 Sample output:")
    print(result[:500] + "..." if len(result) > 500 else result)

#!/usr/bin/env python3
"""
Embedded Agent Implementation - All logic built into the agent
This is our "Approach A" for testing performance and output quality.
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
            return f"<Error agent='{self.agent_type}'>Error processing: {str(e)}</Error>"
    
    @abstractmethod
    def _process_intelligence(self, parsed_input: etree.Element) -> dict:
        """Agent-specific logic - implemented by subclasses"""
        pass
    
    @abstractmethod
    def _generate_xml(self, result: dict) -> str:
        """Generate XML for next agent - implemented by subclasses"""
        pass

class EmbeddedCodeScoutAgent(BaseXAgent):
    """Code Scout Agent with all domain logic embedded"""
    
    def __init__(self):
        super().__init__("EmbeddedCodeScoutAgent")
    
    def _process_intelligence(self, parsed_input: etree.Element) -> dict:
        """Extract POIs using embedded code analysis logic"""
        
        # Extract content from XML
        content_elem = parsed_input.find('Content')
        content = content_elem.text if content_elem is not None else ""
        
        file_path_elem = parsed_input.find('FilePath')
        file_path = file_path_elem.text if file_path_elem is not None else "unknown"
        
        # Embedded domain logic - no external plugins
        pois = {
            'functions': self._extract_functions(content),
            'classes': self._extract_classes(content),
            'imports': self._extract_imports(content),
            'variables': self._extract_variables(content),
            'decorators': self._extract_decorators(content)
        }
        
        # Basic relationship detection
        relationships = self._detect_basic_relationships(content, pois)
        
        return {
            'file_path': file_path,
            'content_length': len(content),
            'pois': pois,
            'relationships': relationships,
            'total_pois': sum(len(poi_list) for poi_list in pois.values())
        }
    
    def _extract_functions(self, content: str) -> List[Dict[str, Any]]:
        """Extract function definitions - embedded logic"""
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
    
    def _extract_classes(self, content: str) -> List[Dict[str, Any]]:
        """Extract class definitions - embedded logic"""
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
    
    def _extract_imports(self, content: str) -> List[Dict[str, Any]]:
        """Extract import statements - embedded logic"""
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
                    'name': module_name,  # Fix: use 'name' key consistently
                    'module': module_name,
                    'items': imported_items,
                    'type': 'import',
                    'line': line_number
                })
        
        return imports
    
    def _extract_variables(self, content: str) -> List[Dict[str, Any]]:
        """Extract variable assignments - embedded logic"""
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
    
    def _extract_decorators(self, content: str) -> List[Dict[str, Any]]:
        """Extract decorator usage - embedded logic"""
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
    
    def _detect_basic_relationships(self, content: str, pois: Dict) -> List[Dict[str, str]]:
        """Detect basic relationships between POIs - embedded logic"""
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
                    'confidence': 0.95
                })
        
        # Detect function calls (basic pattern matching)
        for func_name in function_names:
            call_pattern = rf'{func_name}\s*\('
            if re.search(call_pattern, content):
                relationships.append({
                    'from': 'code',
                    'to': func_name,
                    'type': 'CALLS',
                    'confidence': 0.8
                })
        
        return relationships
    
    def _generate_xml(self, result: dict) -> str:
        """Generate XML output with all discovered POIs and relationships"""
        
        xml_parts = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<CodeAnalysisResult>',
            f'  <FilePath>{result["file_path"]}</FilePath>',
            f'  <ContentLength>{result["content_length"]}</ContentLength>',
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
            '</CodeAnalysisResult>'
        ])
        
        return '\n'.join(xml_parts)

# Test the embedded agent
if __name__ == "__main__":
    print("🧪 Testing Embedded Code Scout Agent")
    
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
    agent = EmbeddedCodeScoutAgent()
    result = agent.process(test_xml)
    
    print(f"✅ Processing completed in {agent.metrics['total_time']:.2f}ms")
    print(f"📄 Result length: {len(result)} characters")
    print("\n📊 Sample output:")
    print(result[:500] + "..." if len(result) > 500 else result)

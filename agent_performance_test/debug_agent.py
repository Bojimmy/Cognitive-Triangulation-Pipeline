#!/usr/bin/env python3
"""
Debug version of embedded agent to find the exact error location
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
            print(f"🔍 [DEBUG] Starting XML parsing...")
            # Parse XML input
            parsed_input = etree.fromstring(input_xml.encode('utf-8'))
            print(f"✅ [DEBUG] XML parsed successfully")
            
            # Process with agent-specific intelligence
            print(f"🔍 [DEBUG] Starting intelligence processing...")
            result = self._process_intelligence(parsed_input)
            print(f"✅ [DEBUG] Intelligence processing completed")
            print(f"📊 [DEBUG] Result keys: {list(result.keys())}")
            
            # Generate XML output
            print(f"🔍 [DEBUG] Starting XML generation...")
            output_xml = self._generate_xml(result)
            print(f"✅ [DEBUG] XML generation completed")
            
            # Track performance
            end_time = time.perf_counter()
            self.metrics['total_time'] = (end_time - start_time) * 1000
            
            return output_xml
            
        except Exception as e:
            print(f"❌ [DEBUG] Error in process method: {e}")
            import traceback
            traceback.print_exc()
            return f"<Error agent='{self.agent_type}'>Error processing: {str(e)}</Error>"
    
    @abstractmethod
    def _process_intelligence(self, parsed_input: etree.Element) -> dict:
        """Agent-specific logic - implemented by subclasses"""
        pass
    
    @abstractmethod
    def _generate_xml(self, result: dict) -> str:
        """Generate XML for next agent - implemented by subclasses"""
        pass

class DebugEmbeddedCodeScoutAgent(BaseXAgent):
    """Debug version of Code Scout Agent"""
    
    def __init__(self):
        super().__init__("DebugEmbeddedCodeScoutAgent")
    
    def _process_intelligence(self, parsed_input: etree.Element) -> dict:
        """Extract POIs using embedded code analysis logic"""
        
        print(f"🔍 [DEBUG] Extracting content from XML...")
        # Extract content from XML
        content_elem = parsed_input.find('Content')
        content = content_elem.text if content_elem is not None else ""
        print(f"📄 [DEBUG] Content extracted: {len(content)} characters")
        
        file_path_elem = parsed_input.find('FilePath')
        file_path = file_path_elem.text if file_path_elem is not None else "unknown"
        print(f"📁 [DEBUG] File path: {file_path}")
        
        # Test function extraction
        print(f"🔍 [DEBUG] Testing function extraction...")
        functions = self._extract_functions(content)
        print(f"📝 [DEBUG] Functions found: {len(functions)}")
        for func in functions[:3]:  # Show first 3
            print(f"    {func}")
        
        # Test class extraction  
        print(f"🔍 [DEBUG] Testing class extraction...")
        classes = self._extract_classes(content)
        print(f"🏗️  [DEBUG] Classes found: {len(classes)}")
        for cls in classes[:3]:  # Show first 3
            print(f"    {cls}")
        
        # Embedded domain logic - no external plugins
        pois = {
            'functions': functions,
            'classes': classes,
            'imports': [],  # Skip for now
            'variables': [],  # Skip for now
            'decorators': []  # Skip for now
        }
        
        print(f"📊 [DEBUG] Total POIs: {sum(len(poi_list) for poi_list in pois.values())}")
        
        return {
            'file_path': file_path,
            'content_length': len(content),
            'pois': pois,
            'relationships': [],
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
            
            func_dict = {
                'name': func_name,
                'type': 'function',
                'line': line_number,
                'is_async': 'async def' in content[max(0, start_pos-10):start_pos+20],
                'is_private': func_name.startswith('_'),
                'is_magic': func_name.startswith('__') and func_name.endswith('__')
            }
            
            functions.append(func_dict)
            print(f"    [DEBUG] Function: {func_name} at line {line_number}")
        
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
            
            class_dict = {
                'name': class_name,
                'type': 'class',
                'line': line_number,
                'parent_classes': [],
                'is_abstract': False
            }
            
            classes.append(class_dict)
            print(f"    [DEBUG] Class: {class_name} at line {line_number}")
        
        return classes
    
    def _generate_xml(self, result: dict) -> str:
        """Generate XML output with all discovered POIs and relationships"""
        
        print(f"🔍 [DEBUG] Generating XML output...")
        print(f"📊 [DEBUG] Result structure: {list(result.keys())}")
        
        xml_parts = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<CodeAnalysisResult>',
            f'  <FilePath>{result["file_path"]}</FilePath>',
            f'  <ContentLength>{result["content_length"]}</ContentLength>',
            f'  <TotalPOIs>{result["total_pois"]}</TotalPOIs>',
            '  <POIs>'
        ]
        
        print(f"🔍 [DEBUG] Processing POI types...")
        # Add all POI types
        for poi_type, poi_list in result['pois'].items():
            print(f"    [DEBUG] Processing {poi_type}: {len(poi_list)} items")
            xml_parts.append(f'    <{poi_type.title()}>')
            
            for i, poi in enumerate(poi_list):
                print(f"      [DEBUG] POI {i}: {list(poi.keys())}")
                try:
                    poi_xml = f'      <POI name="{poi["name"]}" type="{poi["type"]}" line="{poi["line"]}"/>'
                    xml_parts.append(poi_xml)
                    print(f"      [DEBUG] Added POI XML: {poi_xml}")
                except KeyError as e:
                    print(f"      ❌ [DEBUG] Missing key in POI: {e}")
                    print(f"      [DEBUG] POI content: {poi}")
                    raise
            
            xml_parts.append(f'    </{poi_type.title()}>')
        
        xml_parts.extend([
            '  </POIs>',
            '  <Relationships>',
            '  </Relationships>',
            f'  <ProcessingTime>{self.metrics["total_time"]:.2f}ms</ProcessingTime>',
            '</CodeAnalysisResult>'
        ])
        
        result_xml = '\n'.join(xml_parts)
        print(f"✅ [DEBUG] XML generation completed: {len(result_xml)} characters")
        return result_xml

# Test the debug agent
if __name__ == "__main__":
    print("🧪 Testing Debug Embedded Code Scout Agent")
    print("=" * 60)
    
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
    agent = DebugEmbeddedCodeScoutAgent()
    result = agent.process(test_xml)
    
    print("=" * 60)
    print(f"✅ Final result ({len(result)} characters):")
    print(result[:1000] + "..." if len(result) > 1000 else result)

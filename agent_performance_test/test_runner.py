#!/usr/bin/env python3
"""
Agent Performance Test Runner
Compares different X-Agent implementation approaches for code analysis.
"""

import time
import json
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class TestResult:
    """Results from testing an agent implementation"""
    implementation_name: str
    execution_time_ms: float
    pois_detected: int
    functions_found: List[str]
    classes_found: List[str]
    imports_found: List[str]
    relationships_found: List[Dict[str, str]]
    errors: List[str]

class AgentTester:
    """Framework for testing different agent implementations"""
    
    def __init__(self, test_file_path: str):
        self.test_file_path = test_file_path
        self.test_content = self._load_test_file()
        self.results: List[TestResult] = []
    
    def _load_test_file(self) -> str:
        """Load the test file content"""
        try:
            with open(self.test_file_path, 'r') as file:
                return file.read()
        except Exception as e:
            raise RuntimeError(f"Failed to load test file: {e}")
    
    def test_agent(self, agent_instance, implementation_name: str) -> TestResult:
        """Test a specific agent implementation"""
        print(f"\n🧪 Testing {implementation_name}...")
        
        errors = []
        start_time = time.perf_counter()
        
        try:
            # Create XML input for the agent
            xml_input = f"""<?xml version="1.0" encoding="UTF-8"?>
<CodeAnalysisInput>
    <FilePath>{self.test_file_path}</FilePath>
    <Content><![CDATA[{self.test_content}]]></Content>
</CodeAnalysisInput>"""
            
            # Process with the agent
            result_xml = agent_instance.process(xml_input)
            
            # Parse results (simplified for now)
            pois_detected = result_xml.count('<POI')
            functions_found = self._extract_functions_from_xml(result_xml)
            classes_found = self._extract_classes_from_xml(result_xml)
            imports_found = self._extract_imports_from_xml(result_xml)
            relationships_found = self._extract_relationships_from_xml(result_xml)
            
        except Exception as e:
            errors.append(str(e))
            pois_detected = 0
            functions_found = []
            classes_found = []
            imports_found = []
            relationships_found = []
        
        end_time = time.perf_counter()
        execution_time_ms = (end_time - start_time) * 1000
        
        result = TestResult(
            implementation_name=implementation_name,
            execution_time_ms=execution_time_ms,
            pois_detected=pois_detected,
            functions_found=functions_found,
            classes_found=classes_found,
            imports_found=imports_found,
            relationships_found=relationships_found,
            errors=errors
        )
        
        self.results.append(result)
        self._print_result(result)
        
        return result
    
    def _extract_functions_from_xml(self, xml: str) -> List[str]:
        """Extract function names from XML output (simplified)"""
        # This is a placeholder - would need proper XML parsing
        functions = []
        lines = xml.split('\n')
        for line in lines:
            if 'function' in line.lower() and 'name=' in line:
                # Simple extraction - would need proper XML parsing
                pass
        return functions
    
    def _extract_classes_from_xml(self, xml: str) -> List[str]:
        """Extract class names from XML output (simplified)"""
        classes = []
        # Placeholder for XML parsing
        return classes
    
    def _extract_imports_from_xml(self, xml: str) -> List[str]:
        """Extract import statements from XML output (simplified)"""
        imports = []
        # Placeholder for XML parsing
        return imports
    
    def _extract_relationships_from_xml(self, xml: str) -> List[Dict[str, str]]:
        """Extract relationships from XML output (simplified)"""
        relationships = []
        # Placeholder for XML parsing
        return relationships
    
    def _print_result(self, result: TestResult):
        """Print test result summary"""
        print(f"  ⏱️  Execution time: {result.execution_time_ms:.2f}ms")
        print(f"  🎯 POIs detected: {result.pois_detected}")
        print(f"  📝 Functions: {len(result.functions_found)}")
        print(f"  🏗️  Classes: {len(result.classes_found)}")
        print(f"  📦 Imports: {len(result.imports_found)}")
        print(f"  🔗 Relationships: {len(result.relationships_found)}")
        
        if result.errors:
            print(f"  ❌ Errors: {len(result.errors)}")
            for error in result.errors:
                print(f"     {error}")
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        if not self.results:
            return {"error": "No test results available"}
        
        # Find fastest and most accurate
        fastest = min(self.results, key=lambda r: r.execution_time_ms)
        most_pois = max(self.results, key=lambda r: r.pois_detected)
        
        report = {
            "test_summary": {
                "test_file": self.test_file_path,
                "implementations_tested": len(self.results),
                "fastest_implementation": {
                    "name": fastest.implementation_name,
                    "time_ms": fastest.execution_time_ms
                },
                "most_accurate_implementation": {
                    "name": most_pois.implementation_name,
                    "pois_detected": most_pois.pois_detected
                }
            },
            "detailed_results": {}
        }
        
        for result in self.results:
            report["detailed_results"][result.implementation_name] = {
                "execution_time_ms": result.execution_time_ms,
                "pois_detected": result.pois_detected,
                "functions_found": result.functions_found,
                "classes_found": result.classes_found,
                "imports_found": result.imports_found,
                "relationships_found": result.relationships_found,
                "error_count": len(result.errors),
                "errors": result.errors
            }
        
        return report
    
    def save_report(self, output_path: str):
        """Save test report to JSON file"""
        report = self.generate_report()
        with open(output_path, 'w') as file:
            json.dump(report, file, indent=2)
        print(f"\n📊 Report saved to: {output_path}")

if __name__ == "__main__":
    print("🧪 Agent Performance Test Framework")
    print("=" * 50)
    
    # Initialize tester
    tester = AgentTester("sample_code.py")
    
    print(f"📁 Test file loaded: sample_code.py ({len(tester.test_content)} characters)")
    print("\n🚀 Ready to test agent implementations!")
    print("\nTo test an agent, call:")
    print("  tester.test_agent(your_agent_instance, 'Implementation Name')")
    print("\nTo generate report:")
    print("  tester.save_report('results.json')")

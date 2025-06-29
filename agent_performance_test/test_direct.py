#!/usr/bin/env python3
"""
Fixed Debug Test - Let's see the actual output from our embedded agent
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from embedded_agent import EmbeddedCodeScoutAgent

def test_agent_output():
    print("🧪 Testing Embedded Agent Output")
    print("=" * 50)
    
    # Load sample code
    with open('sample_code.py', 'r') as f:
        test_content = f.read()
    
    print(f"📁 Sample file loaded: {len(test_content)} characters")
    
    # Create test XML input
    test_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<CodeAnalysisInput>
    <FilePath>sample_code.py</FilePath>
    <Content><![CDATA[{test_content}]]></Content>
</CodeAnalysisInput>"""
    
    print(f"📋 XML input created: {len(test_xml)} characters")
    
    # Test the agent
    agent = EmbeddedCodeScoutAgent()
    
    print(f"\n🚀 Running agent...")
    result_xml = agent.process(test_xml)
    
    print(f"✅ Processing completed in {agent.metrics['total_time']:.2f}ms")
    print(f"📄 Result XML length: {len(result_xml)} characters")
    
    # Show the actual output
    print(f"\n📊 ACTUAL AGENT OUTPUT:")
    print("=" * 50)
    print(result_xml)
    print("=" * 50)
    
    # Count POIs manually in the output
    poi_count = result_xml.count('<POI')
    function_count = result_xml.count('type="function"')
    class_count = result_xml.count('type="class"')
    
    print(f"\n📊 MANUAL COUNT FROM XML OUTPUT:")
    print(f"🎯 Total POI tags: {poi_count}")
    print(f"📝 Functions: {function_count}")
    print(f"🏗️  Classes: {class_count}")
    
    # Test if there are any errors in the output
    if '<Error' in result_xml:
        print(f"❌ Error detected in output!")
        print(f"🔍 Error content: {result_xml}")
    else:
        print(f"✅ No errors detected")

if __name__ == "__main__":
    test_agent_output()

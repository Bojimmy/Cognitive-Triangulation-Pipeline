#!/usr/bin/env python3
"""
Debug script to test XML processing
"""

from lxml import etree

# Test simple XML first
simple_xml = """<?xml version="1.0" encoding="UTF-8"?>
<CodeAnalysisInput>
    <FilePath>test.py</FilePath>
    <Content><![CDATA[def hello(): pass]]></Content>
</CodeAnalysisInput>"""

print("🔍 Testing simple XML parsing...")
try:
    parsed = etree.fromstring(simple_xml.encode('utf-8'))
    print("✅ Simple XML parsed successfully")
    
    content_elem = parsed.find('Content')
    print(f"📄 Content element found: {content_elem is not None}")
    
    if content_elem is not None:
        content = content_elem.text
        print(f"📝 Content extracted: {repr(content)}")
        print(f"📏 Content length: {len(content) if content else 'None'}")
    
except Exception as e:
    print(f"❌ Error parsing simple XML: {e}")

# Test with actual sample file
print("\n🔍 Testing with sample file content...")
try:
    with open('sample_code.py', 'r') as f:
        file_content = f.read()
    
    print(f"📁 File loaded: {len(file_content)} characters")
    print(f"📄 First 100 chars: {repr(file_content[:100])}")
    
    # Create XML with file content
    test_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<CodeAnalysisInput>
    <FilePath>sample_code.py</FilePath>
    <Content><![CDATA[{file_content}]]></Content>
</CodeAnalysisInput>"""
    
    print(f"📋 XML created: {len(test_xml)} characters")
    
    # Try to parse it
    parsed = etree.fromstring(test_xml.encode('utf-8'))
    print("✅ Complex XML parsed successfully")
    
    content_elem = parsed.find('Content')
    if content_elem is not None:
        extracted_content = content_elem.text
        print(f"📝 Content extracted: {len(extracted_content)} characters")
        print(f"📄 Content preview: {repr(extracted_content[:100])}")
        
        # Test regex on extracted content
        import re
        function_pattern = r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\):'
        functions = re.findall(function_pattern, extracted_content)
        print(f"🔧 Functions found: {functions}")
    
except Exception as e:
    print(f"❌ Error with sample file: {e}")
    import traceback
    traceback.print_exc()

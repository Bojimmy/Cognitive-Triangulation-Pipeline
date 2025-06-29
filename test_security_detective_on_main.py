#!/usr/bin/env python3
"""
Test Enhanced Security Detective on Bob's actual main.py
Compare with original detective results
"""
import sys
import os
sys.path.append('/Users/bobdallavia/X-Agent-Pipeline-CognitiveTriangulation/cognitive_triangulation/agents')

from security_code_detective_agent import SecurityCodeDetectiveAgent

def test_security_detective_on_main_py():
    """Test the enhanced security detective on the actual main.py file"""
    
    # Read the problematic main.py
    main_py_path = '/Users/bobdallavia/X-Agent-Pipeline/main.py'
    
    try:
        with open(main_py_path, 'r') as f:
            main_py_content = f.read()
    except FileNotFoundError:
        print(f"❌ Could not find main.py at: {main_py_path}")
        return
    
    print(f"🔒 ENHANCED SECURITY DETECTIVE vs MAIN.PY")
    print(f"📁 Target: {main_py_path}")
    print(f"📏 Size: {len(main_py_content)} characters")
    print(f"📝 Lines: {len(main_py_content.splitlines())}")
    print("=" * 80)
    
    # Create enhanced security detective
    detective = SecurityCodeDetectiveAgent()
    
    # Create proper XML input with escaped content
    import html
    escaped_content = html.escape(main_py_content)
    
    xml_input = f'''<code_analysis_request>
        <file_path>{main_py_path}</file_path>
        <file_content>{escaped_content}</file_content>
        <language>python</language>
    </code_analysis_request>'''
    
    # Run enhanced security analysis
    print("🔄 Running enhanced security analysis...")
    result = detective.process(xml_input)
    
    # Parse and display results nicely
    import xml.etree.ElementTree as ET
    try:
        root = ET.fromstring(result)
        print("✅ Security analysis complete!")
    except ET.ParseError as e:
        print(f"❌ XML Parse Error: {e}")
        return
    
    # Extract comprehensive results
    summary = root.find('summary')
    total_findings = "0"
    security_score = "100"
    risk_level = "UNKNOWN"
    
    if summary is not None:
        total_findings = summary.find('total_findings').text
        security_score = summary.find('security_score').text
        risk_level = summary.find('risk_level').text
        total_lines = summary.find('total_lines').text
        findings_per_100_lines = summary.find('findings_per_100_lines').text
        
        print(f"\n🎯 ENHANCED SECURITY ANALYSIS RESULTS:")
        print(f"   🚨 Total Security Findings: {total_findings}")
        print(f"   🛡️ Security Score: {security_score}/100")
        print(f"   ⚠️ Risk Level: {risk_level}")
        print(f"   📝 Total Lines: {total_lines}")
        print(f"   📈 Findings per 100 lines: {findings_per_100_lines}")
        
        # Security breakdown
        severity = root.find('findings_by_severity')
        if severity is not None:
            print(f"\n🚨 SECURITY FINDINGS BY SEVERITY:")
            critical = severity.find('critical').text
            high = severity.find('high').text
            medium = severity.find('medium').text
            low = severity.find('low').text
            
            print(f"   🔴 CRITICAL: {critical} (Immediate action required!)")
            print(f"   🟠 HIGH: {high} (Fix ASAP)")
            print(f"   🟡 MEDIUM: {medium} (Should fix)")
            print(f"   🔵 LOW: {low} (Consider fixing)")
        
        # Finding types
        finding_types = root.find('findings_by_type')
        if finding_types is not None:
            print(f"\n🏷️ SECURITY FINDINGS BY TYPE:")
            security = finding_types.find('security').text
            vulnerability = finding_types.find('vulnerability').text
            bug = finding_types.find('bug').text
            
            print(f"   🔒 Security Issues: {security}")
            print(f"   🚨 Known Vulnerabilities: {vulnerability}")
            print(f"   🐛 Security-Related Bugs: {bug}")
        
        # Analysis sources
        metadata = root.find('analysis_metadata')
        if metadata is not None:
            print(f"\n🔬 ANALYSIS METADATA:")
            cognitive_patterns = metadata.find('cognitive_patterns_used')
            mcp_calls = metadata.find('mcp_calls_made')
            triangulation = metadata.find('triangulation_applied')
            
            if cognitive_patterns is not None:
                print(f"   🧠 Cognitive Patterns Used: {cognitive_patterns.text}")
            if mcp_calls is not None:
                print(f"   🛠️ MCP Calls Made: {mcp_calls.text}")
            if triangulation is not None:
                print(f"   🔺 Triangulation Applied: {triangulation.text}")
        
        # Critical findings
        critical_findings = root.find('critical_findings')
        if critical_findings is not None and len(list(critical_findings)) > 0:
            print(f"\n🚨 CRITICAL SECURITY ISSUES FOUND:")
            for i, finding in enumerate(critical_findings.findall('finding'), 1):
                severity = finding.find('severity').text
                line_num = finding.find('line').text
                description = finding.find('description').text
                fix_suggestion = finding.find('fix').text
                source = finding.find('source').text
                cve_id_elem = finding.find('cve_id')
                cve_id = cve_id_elem.text if cve_id_elem is not None and cve_id_elem.text != 'None' else None
                
                print(f"\n   {i}. 🔴 CRITICAL - Line {line_num}")
                print(f"      📍 Issue: {description}")
                if cve_id:
                    print(f"      🆔 CVE ID: {cve_id}")
                print(f"      💡 Fix: {fix_suggestion}")
                print(f"      🔍 Detected by: {source}")
        
        # Top findings (first 10)
        top_findings = root.find('top_findings')
        if top_findings is not None and len(list(top_findings)) > 0:
            print(f"\n🎯 TOP SECURITY FINDINGS:")
            findings_list = list(top_findings.findall('finding'))[:10]  # Limit to 10
            
            for i, finding in enumerate(findings_list, 1):
                severity = finding.find('severity').text
                finding_type = finding.find('type').text
                line_num = finding.find('line').text
                description = finding.find('description').text
                fix_suggestion = finding.find('fix').text
                confidence = finding.find('confidence').text
                source = finding.find('source').text
                
                severity_emoji = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🔵'}
                print(f"\n   {i}. {severity_emoji.get(severity, '⚪')} {severity.upper()} - {finding_type}")
                print(f"      📍 Line {line_num}: {description}")
                print(f"      💡 Fix: {fix_suggestion}")
                print(f"      🎯 Confidence: {float(confidence)*100:.1f}% | Source: {source}")
    
    print(f"\n" + "=" * 80)
    print(f"🔒 Enhanced Security Analysis Complete!")
    
    # Print comparison with original detective
    print(f"\n📊 COMPARISON WITH ORIGINAL DETECTIVE:")
    print(f"   📈 Original Detective: 18 general issues (quality score 0/100)")
    print(f"   🔒 Enhanced Security Detective: {total_findings} security-focused findings (security score {security_score}/100)")
    print(f"   🎯 Enhancement: Specialized security patterns + MCP tools + triangulation")

if __name__ == "__main__":
    test_security_detective_on_main_py()

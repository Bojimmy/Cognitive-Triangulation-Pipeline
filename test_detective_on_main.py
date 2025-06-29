#!/usr/bin/env python3
"""
Test the Code Quality Detective Agent on real problematic code
"""
import sys
import os
sys.path.append('/Users/bobdallavia/X-Agent-Pipeline-CognitiveTriangulation/cognitive_triangulation/agents')

from code_quality_detective_agent import CodeQualityDetectiveAgent

def test_detective_on_main_py():
    """Test the detective on the actual main.py file"""
    
    # Read the problematic main.py
    main_py_path = '/Users/bobdallavia/X-Agent-Pipeline/main.py'
    
    try:
        with open(main_py_path, 'r') as f:
            main_py_content = f.read()
    except FileNotFoundError:
        print(f"❌ Could not find main.py at: {main_py_path}")
        return
    
    print(f"🔍 TESTING CODE QUALITY DETECTIVE ON MAIN.PY")
    print(f"📁 File: {main_py_path}")
    print(f"📏 Size: {len(main_py_content)} characters")
    print(f"📝 Lines: {len(main_py_content.splitlines())}")
    print("=" * 60)
    
    # Create detective
    detective = CodeQualityDetectiveAgent()
    
    # Create proper XML input with escaped content
    import html
    escaped_content = html.escape(main_py_content)
    
    xml_input = f'''<code_analysis_request>
        <file_path>{main_py_path}</file_path>
        <file_content>{escaped_content}</file_content>
        <language>python</language>
    </code_analysis_request>'''
    
    # Run analysis
    print("🔄 Running detective analysis...")
    result = detective.process(xml_input)
    
    print(f"📤 Raw XML Result (first 500 chars):")
    print(result[:500])
    print("...")
    
    # Parse and display results nicely
    import xml.etree.ElementTree as ET
    try:
        root = ET.fromstring(result)
        print("✅ XML parsed successfully")
    except ET.ParseError as e:
        print(f"❌ XML Parse Error: {e}")
        return
    
    # Extract summary
    summary = root.find('summary')
    if summary is not None:
        total_issues = summary.find('total_issues').text
        quality_score = summary.find('quality_score').text
        total_lines = summary.find('total_lines').text
        issues_per_100_lines = summary.find('issues_per_100_lines').text
        
        print(f"🎯 ANALYSIS RESULTS:")
        print(f"   📊 Total Issues Found: {total_issues}")
        print(f"   🏆 Quality Score: {quality_score}/100")
        print(f"   📝 Total Lines: {total_lines}")
        print(f"   📈 Issues per 100 lines: {issues_per_100_lines}")
        
        # Issues by severity
        severity = root.find('issues_by_severity')
        if severity is not None:
            print(f"\n🚨 ISSUES BY SEVERITY:")
            print(f"   🔴 Critical: {severity.find('critical').text}")
            print(f"   🟠 High: {severity.find('high').text}")
            print(f"   🟡 Medium: {severity.find('medium').text}")
            print(f"   🔵 Low: {severity.find('low').text}")
        
        # Issues by type
        issue_types = root.find('issues_by_type')
        if issue_types is not None:
            print(f"\n🏷️ ISSUES BY TYPE:")
            print(f"   🐛 Bugs: {issue_types.find('bug').text}")
            print(f"   🔒 Security: {issue_types.find('security').text}")
            print(f"   ⚡ Performance: {issue_types.find('performance').text}")
            print(f"   🔧 Maintainability: {issue_types.find('maintainability').text}")
        
        # Top issues
        top_issues = root.find('top_issues')
        if top_issues is not None and len(list(top_issues)) > 0:
            print(f"\n🎯 TOP ISSUES FOUND:")
            for i, issue in enumerate(top_issues.findall('issue'), 1):
                severity = issue.find('severity').text
                issue_type = issue.find('type').text
                line_num = issue.find('line_number').text
                description = issue.find('description').text
                fix_suggestion = issue.find('fix_suggestion').text
                
                severity_emoji = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🔵'}
                print(f"\n   {i}. {severity_emoji.get(severity, '⚪')} {severity.upper()} - {issue_type}")
                print(f"      📍 Line {line_num}: {description}")
                print(f"      💡 Fix: {fix_suggestion}")
        else:
            print(f"\n✅ No specific issues detected in top issues")
    
    print(f"\n" + "=" * 60)
    print(f"🔍 Detective Analysis Complete!")

if __name__ == "__main__":
    test_detective_on_main_py()

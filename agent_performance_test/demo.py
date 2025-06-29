#!/usr/bin/env python3
"""
Quick Demo - Test the Embedded Agent Implementation
Run this to see the testing framework in action!
"""

import sys
import os

# Add current directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from test_runner import AgentTester
from embedded_agent import EmbeddedCodeScoutAgent

def main():
    print("🚀 Agent Performance Test Demo")
    print("=" * 50)
    
    # Initialize the test framework
    print("📁 Loading test framework...")
    tester = AgentTester("sample_code.py")
    
    print(f"✅ Test file loaded: {len(tester.test_content)} characters")
    print(f"📊 Sample code contains: classes, functions, imports, inheritance, async methods")
    
    # Test the embedded agent
    print("\n🧪 Testing Embedded Code Scout Agent...")
    embedded_agent = EmbeddedCodeScoutAgent()
    
    result = tester.test_agent(embedded_agent, "EmbeddedCodeScoutAgent")
    
    # Generate and display report
    print("\n📊 Generating performance report...")
    report = tester.generate_report()
    
    print("\n" + "=" * 50)
    print("📈 PERFORMANCE SUMMARY")
    print("=" * 50)
    
    if 'test_summary' in report:
        summary = report['test_summary']
        print(f"🏆 Fastest: {summary['fastest_implementation']['name']}")
        print(f"⏱️  Time: {summary['fastest_implementation']['time_ms']:.2f}ms")
        print(f"🎯 Most Accurate: {summary['most_accurate_implementation']['name']}")
        print(f"📊 POIs Found: {summary['most_accurate_implementation']['pois_detected']}")
    
    # Save detailed report
    tester.save_report("test_results.json")
    
    print("\n🎯 NEXT STEPS:")
    print("1. Create co-located plugin agent implementation")
    print("2. Create original-style agent implementation") 
    print("3. Run comparative tests")
    print("4. Choose best approach for Cognitive Triangulation system")
    
    print(f"\n✅ Demo complete! Check test_results.json for detailed analysis.")

if __name__ == "__main__":
    main()

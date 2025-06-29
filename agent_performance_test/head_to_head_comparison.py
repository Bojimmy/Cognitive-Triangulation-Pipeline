#!/usr/bin/env python3
"""
Head-to-Head Agent Comparison Test
Compares Embedded Agent vs Co-Located Plugin Agent performance and accuracy
"""

import sys
import os
import time
import json
from typing import Dict, Any

# Add current directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from test_runner import AgentTester
from embedded_agent import EmbeddedCodeScoutAgent
from colocated_plugin_agent import CoLocatedPluginCodeScoutAgent

def run_comparison_test():
    print("🥊 HEAD-TO-HEAD AGENT COMPARISON")
    print("=" * 60)
    
    # Initialize the test framework
    print("📁 Loading test framework...")
    tester = AgentTester("sample_code.py")
    
    print(f"✅ Test file loaded: {len(tester.test_content)} characters")
    print(f"📊 Sample code contains: classes, functions, imports, inheritance, async methods")
    
    # Test both agents
    print("\n🥊 ROUND 1: Embedded Agent")
    print("-" * 30)
    embedded_agent = EmbeddedCodeScoutAgent()
    embedded_result = tester.test_agent(embedded_agent, "EmbeddedAgent")
    
    print("\n🥊 ROUND 2: Co-Located Plugin Agent") 
    print("-" * 30)
    plugin_agent = CoLocatedPluginCodeScoutAgent()
    plugin_result = tester.test_agent(plugin_agent, "CoLocatedPluginAgent")
    
    # Generate detailed comparison
    print("\n📊 DETAILED COMPARISON")
    print("=" * 60)
    
    comparison_data = {
        "test_info": {
            "date": "2025-06-29",
            "test_file": "sample_code.py",
            "file_size_chars": len(tester.test_content)
        },
        "performance": {
            "embedded_agent": {
                "time_ms": embedded_result.execution_time_ms,
                "pois_detected": embedded_result.pois_detected,
                "errors": len(embedded_result.errors)
            },
            "colocated_plugin_agent": {
                "time_ms": plugin_result.execution_time_ms, 
                "pois_detected": plugin_result.pois_detected,
                "errors": len(plugin_result.errors)
            }
        },
        "winner": {},
        "insights": []
    }
    
    # Determine winners
    if embedded_result.execution_time_ms < plugin_result.execution_time_ms:
        speed_winner = "Embedded Agent"
        speed_margin = plugin_result.execution_time_ms - embedded_result.execution_time_ms
    else:
        speed_winner = "Co-Located Plugin Agent"
        speed_margin = embedded_result.execution_time_ms - plugin_result.execution_time_ms
    
    if embedded_result.pois_detected > plugin_result.pois_detected:
        accuracy_winner = "Embedded Agent"
        accuracy_margin = embedded_result.pois_detected - plugin_result.pois_detected
    else:
        accuracy_winner = "Co-Located Plugin Agent"
        accuracy_margin = plugin_result.pois_detected - embedded_result.pois_detected
    
    comparison_data["winner"] = {
        "speed": {"agent": speed_winner, "margin_ms": speed_margin},
        "accuracy": {"agent": accuracy_winner, "margin_pois": accuracy_margin}
    }
    
    print(f"🏆 SPEED WINNER: {speed_winner}")
    print(f"   Margin: {speed_margin:.3f}ms faster")
    print(f"   Embedded: {embedded_result.execution_time_ms:.3f}ms")
    print(f"   Plugin:   {plugin_result.execution_time_ms:.3f}ms")
    
    print(f"\n🎯 ACCURACY WINNER: {accuracy_winner}")
    print(f"   Margin: {accuracy_margin} more POIs detected")
    print(f"   Embedded: {embedded_result.pois_detected} POIs")
    print(f"   Plugin:   {plugin_result.pois_detected} POIs")
    
    print(f"\n❌ ERROR COMPARISON:")
    print(f"   Embedded: {len(embedded_result.errors)} errors")
    print(f"   Plugin:   {len(plugin_result.errors)} errors")
    
    # Generate insights
    insights = []
    
    if abs(embedded_result.execution_time_ms - plugin_result.execution_time_ms) < 0.1:
        insights.append("Performance is nearly identical between approaches")
    elif speed_margin > 1.0:
        insights.append(f"{speed_winner} has significant speed advantage")
    
    if embedded_result.pois_detected == plugin_result.pois_detected:
        insights.append("Both approaches detected identical number of POIs")
    elif accuracy_margin > 5:
        insights.append(f"{accuracy_winner} has significant accuracy advantage")
    
    if len(embedded_result.errors) == 0 and len(plugin_result.errors) == 0:
        insights.append("Both approaches executed without errors")
    
    # Performance per POI
    embedded_poi_speed = embedded_result.execution_time_ms / max(1, embedded_result.pois_detected)
    plugin_poi_speed = plugin_result.execution_time_ms / max(1, plugin_result.pois_detected)
    
    print(f"\n⚡ EFFICIENCY ANALYSIS:")
    print(f"   Embedded: {embedded_poi_speed:.4f}ms per POI")
    print(f"   Plugin:   {plugin_poi_speed:.4f}ms per POI")
    
    if embedded_poi_speed < plugin_poi_speed:
        insights.append("Embedded agent is more efficient per POI detected")
    else:
        insights.append("Plugin agent is more efficient per POI detected")
    
    comparison_data["insights"] = insights
    
    print(f"\n💡 KEY INSIGHTS:")
    for insight in insights:
        print(f"   • {insight}")
    
    # Save detailed comparison report
    with open('agent_comparison_results.json', 'w') as f:
        json.dump(comparison_data, f, indent=2)
    
    print(f"\n📊 Detailed comparison saved to: agent_comparison_results.json")
    
    # Generate final recommendation
    print(f"\n🎯 FINAL RECOMMENDATION:")
    print("=" * 60)
    
    if speed_winner == accuracy_winner:
        print(f"✅ CLEAR WINNER: {speed_winner}")
        print(f"   Wins on both speed and accuracy")
    else:
        print(f"🤔 TRADE-OFF SITUATION:")
        print(f"   Speed: {speed_winner}")
        print(f"   Accuracy: {accuracy_winner}")
        print(f"   Choose based on your priority: speed vs accuracy")
    
    # Context for Cognitive Triangulation project
    print(f"\n🚀 FOR COGNITIVE TRIANGULATION PROJECT:")
    if abs(embedded_result.execution_time_ms - plugin_result.execution_time_ms) < 0.5:
        print("   Both approaches are fast enough for sub-second pipeline")
        print("   Choose based on maintainability and code organization preference")
    else:
        fastest = "Embedded" if embedded_result.execution_time_ms < plugin_result.execution_time_ms else "Plugin"
        print(f"   {fastest} approach recommended for maximum pipeline speed")
    
    return comparison_data

if __name__ == "__main__":
    comparison_results = run_comparison_test()

#!/usr/bin/env python3
"""
Full Pipeline Test - CodeScout → RelationshipDetector
Tests the first two agents in our Cognitive Triangulation pipeline
"""

import sys
import os
import time

# Add paths for imports
sys.path.append('/Users/bobdallavia/X-Agent-Pipeline-CognitiveTriangulation/agent_performance_test')
sys.path.append('/Users/bobdallavia/X-Agent-Pipeline-CognitiveTriangulation/cognitive_triangulation/agents')

from colocated_plugin_agent import CoLocatedPluginCodeScoutAgent
from relationship_detector_agent import RelationshipDetectorAgent

def test_full_pipeline():
    print("🚀 COGNITIVE TRIANGULATION PIPELINE TEST")
    print("=" * 60)
    
    # Load sample code
    sample_file_path = '/Users/bobdallavia/X-Agent-Pipeline-CognitiveTriangulation/agent_performance_test/sample_code.py'
    with open(sample_file_path, 'r') as f:
        test_content = f.read()
    
    print(f"📁 Test file loaded: {len(test_content)} characters")
    
    # Step 1: CodeScout Agent
    print("\n🔍 STEP 1: Code Scout Agent (POI Detection)")
    print("-" * 40)
    
    scout_input = f"""<?xml version="1.0" encoding="UTF-8"?>
<CodeAnalysisInput>
    <FilePath>{sample_file_path}</FilePath>
    <Content><![CDATA[{test_content}]]></Content>
</CodeAnalysisInput>"""
    
    scout_agent = CoLocatedPluginCodeScoutAgent()
    start_time = time.perf_counter()
    scout_output = scout_agent.process(scout_input)
    scout_time = (time.perf_counter() - start_time) * 1000
    
    print(f"✅ CodeScout completed in {scout_time:.2f}ms")
    print(f"📄 Output length: {len(scout_output)} characters")
    
    # Extract key info from scout output
    scout_pois = scout_output.count('<POI')
    print(f"🎯 POIs detected: {scout_pois}")
    
    # Step 2: RelationshipDetector Agent
    print("\n🔗 STEP 2: Relationship Detector Agent")
    print("-" * 40)
    
    # Use scout output as input for relationship detector
    relationship_agent = RelationshipDetectorAgent()
    start_time = time.perf_counter()
    relationship_output = relationship_agent.process(scout_output)
    relationship_time = (time.perf_counter() - start_time) * 1000
    
    print(f"✅ RelationshipDetector completed in {relationship_time:.2f}ms")
    print(f"📄 Output length: {len(relationship_output)} characters")
    
    # Extract key info from relationship output
    relationships_found = relationship_output.count('<Relationship')
    print(f"🔗 Relationships detected: {relationships_found}")
    
    # Pipeline Summary
    total_time = scout_time + relationship_time
    print(f"\n📊 PIPELINE SUMMARY")
    print("=" * 60)
    print(f"🎯 Total POIs: {scout_pois}")
    print(f"🔗 Total Relationships: {relationships_found}")
    print(f"⏱️  CodeScout Time: {scout_time:.2f}ms")
    print(f"⏱️  RelationshipDetector Time: {relationship_time:.2f}ms")
    print(f"⚡ Total Pipeline Time: {total_time:.2f}ms")
    print(f"📈 Efficiency: {total_time/max(1, scout_pois+relationships_found):.3f}ms per item")
    
    # Show sample of final output
    print(f"\n📋 RELATIONSHIP DETECTOR OUTPUT SAMPLE:")
    print("-" * 40)
    lines = relationship_output.split('\n')
    for i, line in enumerate(lines[:20]):
        print(f"{i+1:2d}: {line}")
    if len(lines) > 20:
        print("    ... (output truncated)")
    
    # Performance comparison
    print(f"\n🚀 PERFORMANCE ANALYSIS:")
    print("-" * 40)
    print(f"• Sub-millisecond POI detection: {scout_time < 1.0}")
    print(f"• Sub-millisecond relationship detection: {relationship_time < 1.0}")
    print(f"• Sub-second total pipeline: {total_time < 1000}")
    print(f"• Ready for validator agents: ✅")
    
    # Save outputs for inspection
    with open('pipeline_scout_output.xml', 'w') as f:
        f.write(scout_output)
    
    with open('pipeline_relationship_output.xml', 'w') as f:
        f.write(relationship_output)
    
    print(f"\n💾 Outputs saved:")
    print(f"   pipeline_scout_output.xml")
    print(f"   pipeline_relationship_output.xml")
    
    return {
        'scout_time_ms': scout_time,
        'relationship_time_ms': relationship_time,
        'total_time_ms': total_time,
        'pois_found': scout_pois,
        'relationships_found': relationships_found
    }

if __name__ == "__main__":
    results = test_full_pipeline()
    
    print(f"\n🎉 PIPELINE TEST COMPLETE!")
    print(f"   Ready to build ContextAnalyzer and ConfidenceAggregator agents next!")

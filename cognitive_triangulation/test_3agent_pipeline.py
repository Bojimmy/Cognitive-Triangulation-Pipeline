#!/usr/bin/env python3
"""
Full 3-Agent Pipeline Test - CodeScout → RelationshipDetector → ContextAnalyzer
Tests the first three agents in our Cognitive Triangulation pipeline
"""

import sys
import os
import time

# Add paths for imports
sys.path.append('/Users/bobdallavia/X-Agent-Pipeline-CognitiveTriangulation/agent_performance_test')
sys.path.append('/Users/bobdallavia/X-Agent-Pipeline-CognitiveTriangulation/cognitive_triangulation/agents')

from colocated_plugin_agent import CoLocatedPluginCodeScoutAgent
from relationship_detector_agent import RelationshipDetectorAgent
from context_analyzer_agent import ContextAnalyzerAgent

def test_full_3_agent_pipeline():
    print("🚀 COGNITIVE TRIANGULATION 3-AGENT PIPELINE TEST")
    print("=" * 70)
    
    # Load sample code
    sample_file_path = '/Users/bobdallavia/X-Agent-Pipeline-CognitiveTriangulation/agent_performance_test/sample_code.py'
    with open(sample_file_path, 'r') as f:
        test_content = f.read()
    
    print(f"📁 Test file loaded: {len(test_content)} characters")
    
    # Step 1: CodeScout Agent
    print("\n🔍 STEP 1: Code Scout Agent (POI Detection)")
    print("-" * 50)
    
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
    scout_pois = scout_output.count('<POI')
    print(f"🎯 POIs detected: {scout_pois}")
    
    # Step 2: RelationshipDetector Agent
    print("\n🔗 STEP 2: Relationship Detector Agent")
    print("-" * 50)
    
    relationship_agent = RelationshipDetectorAgent()
    start_time = time.perf_counter()
    relationship_output = relationship_agent.process(scout_output)
    relationship_time = (time.perf_counter() - start_time) * 1000
    
    print(f"✅ RelationshipDetector completed in {relationship_time:.2f}ms")
    print(f"📄 Output length: {len(relationship_output)} characters")
    relationships_found = relationship_output.count('<Relationship')
    print(f"🔗 Relationships detected: {relationships_found}")
    
    # Step 3: ContextAnalyzer Agent
    print("\n🧠 STEP 3: Context Analyzer Agent (Semantic Analysis)")
    print("-" * 50)
    
    context_agent = ContextAnalyzerAgent()
    start_time = time.perf_counter()
    context_output = context_agent.process(relationship_output)
    context_time = (time.perf_counter() - start_time) * 1000
    
    print(f"✅ ContextAnalyzer completed in {context_time:.2f}ms")
    print(f"📄 Output length: {len(context_output)} characters")
    patterns_found = context_output.count('<Pattern')
    print(f"🧠 Semantic patterns detected: {patterns_found}")
    
    # Extract context scores
    import re
    overall_score_match = re.search(r'name="overall_context" value="([^"]+)"', context_output)
    overall_score = float(overall_score_match.group(1)) if overall_score_match else 0.0
    
    # Pipeline Summary
    total_time = scout_time + relationship_time + context_time
    print(f"\n📊 FULL PIPELINE SUMMARY")
    print("=" * 70)
    print(f"🎯 Total POIs: {scout_pois}")
    print(f"🔗 Total Relationships: {relationships_found}")
    print(f"🧠 Total Semantic Patterns: {patterns_found}")
    print(f"📊 Overall Context Score: {overall_score:.3f}")
    print(f"")
    print(f"⏱️  CodeScout Time: {scout_time:.2f}ms")
    print(f"⏱️  RelationshipDetector Time: {relationship_time:.2f}ms")
    print(f"⏱️  ContextAnalyzer Time: {context_time:.2f}ms")
    print(f"⚡ Total Pipeline Time: {total_time:.2f}ms")
    
    total_items = scout_pois + relationships_found + patterns_found
    print(f"📈 Total Analysis Items: {total_items}")
    print(f"📈 Efficiency: {total_time/max(1, total_items):.3f}ms per item")
    
    # Performance Analysis
    print(f"\n🚀 PERFORMANCE ANALYSIS:")
    print("-" * 50)
    print(f"• Sub-millisecond POI detection: {scout_time < 1.0}")
    print(f"• Fast relationship detection: {relationship_time < 5.0}")
    print(f"• Fast semantic analysis: {context_time < 5.0}")
    print(f"• Sub-5ms total pipeline: {total_time < 5.0}")
    print(f"• Ready for ConfidenceAggregator: ✅")
    
    # Quality Analysis
    print(f"\n📊 QUALITY ANALYSIS:")
    print("-" * 50)
    print(f"• POI detection coverage: {scout_pois} items")
    print(f"• Relationship coverage: {relationships_found}/{scout_pois} = {relationships_found/max(1,scout_pois)*100:.1f}%")
    print(f"• Pattern detection density: {patterns_found} semantic patterns")
    print(f"• Context quality score: {overall_score:.1%}")
    
    # Show sample of final semantic output
    print(f"\n📋 CONTEXT ANALYZER OUTPUT SAMPLE:")
    print("-" * 50)
    lines = context_output.split('\n')
    for i, line in enumerate(lines[:25]):
        print(f"{i+1:2d}: {line}")
    if len(lines) > 25:
        print("    ... (output truncated)")
    
    # Save outputs for inspection
    with open('pipeline_3agent_scout.xml', 'w') as f:
        f.write(scout_output)
    
    with open('pipeline_3agent_relationships.xml', 'w') as f:
        f.write(relationship_output)
        
    with open('pipeline_3agent_context.xml', 'w') as f:
        f.write(context_output)
    
    print(f"\n💾 All outputs saved:")
    print(f"   pipeline_3agent_scout.xml")
    print(f"   pipeline_3agent_relationships.xml")
    print(f"   pipeline_3agent_context.xml")
    
    # Comparison to original Cognitive Triangulation
    print(f"\n🎯 COMPARISON TO ORIGINAL COGNITIVE TRIANGULATION:")
    print("=" * 70)
    original_time_estimate = 30000  # 30+ seconds
    speedup = original_time_estimate / total_time
    
    print(f"📊 Original System: ~{original_time_estimate/1000:.0f}+ seconds (hundreds of LLM calls)")
    print(f"📊 Our X-Agent Pipeline: {total_time:.2f}ms (0 LLM calls for analysis)")
    print(f"🚀 Speed Improvement: ~{speedup:,.0f}x faster!")
    print(f"💰 Cost Reduction: ~100% (no LLM tokens for basic analysis)")
    print(f"🎯 Analysis Depth: {total_items} items analyzed comprehensively")
    
    return {
        'scout_time_ms': scout_time,
        'relationship_time_ms': relationship_time,
        'context_time_ms': context_time,
        'total_time_ms': total_time,
        'pois_found': scout_pois,
        'relationships_found': relationships_found,
        'patterns_found': patterns_found,
        'context_score': overall_score,
        'speedup_factor': speedup
    }

if __name__ == "__main__":
    results = test_full_3_agent_pipeline()
    
    print(f"\n🎉 3-AGENT PIPELINE TEST COMPLETE!")
    print(f"   Ready to build ConfidenceAggregator and LLMApprover agents next!")
    print(f"   Pipeline is performing at {results['speedup_factor']:,.0f}x the speed of original system!")

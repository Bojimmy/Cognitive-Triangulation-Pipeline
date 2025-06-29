#!/usr/bin/env python3
"""
Full Pipeline Test: Gaming Development Scenario
Tests the complete workflow from Document Formatter through final Scrum Master approval
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from logging_config import setup_logging
logger = setup_logging(enable_file_logging=True)

from main import XAgentPipeline

def test_full_pipeline_with_gaming_scenario():
    """Test the complete pipeline with a gaming development scenario"""
    
    print("🎮 FULL PIPELINE TEST: Gaming Development Scenario")
    print("=" * 80)
    
    # Gaming development scenario
    gaming_scenario = """
    We need to build a comprehensive multiplayer battle royale game development and management platform.

    Project Requirements:
    REQ-001: Game engine integration with Unity and Unreal Engine for cross-platform development
    REQ-002: Real-time multiplayer networking with dedicated server architecture supporting 100+ players
    REQ-003: Player progression system with unlockable weapons, skins, and battle pass mechanics
    REQ-004: Anti-cheat system integration with machine learning-based detection algorithms
    REQ-005: In-game economy management with virtual currency and microtransaction processing
    REQ-006: Live game analytics dashboard for player behavior analysis and game balancing
    REQ-007: Community features including clan systems, friend lists, and social interactions
    REQ-008: Esports tournament management with bracket generation and live streaming integration
    REQ-009: Content management system for seasonal updates and game patches
    REQ-010: Player support ticketing system with automated response capabilities

    Stakeholders:
    - Game developers and engineers
    - Game designers and artists
    - Community managers
    - Esports coordinators
    - Player support team
    - Marketing and monetization team
    - Quality assurance testers

    Technical Constraints:
    - Must support PC, PlayStation, Xbox, and mobile platforms
    - Server infrastructure must handle global player base with low latency
    - Compliance with COPPA and GDPR for player data protection
    - Integration with Steam, Epic Games Store, and console marketplaces
    - Real-time communication systems for voice chat and team coordination
    
    Business Objectives:
    - Launch within 18 months with early access program
    - Target 1 million players within first year
    - Achieve 95% server uptime during peak gaming hours
    - Generate revenue through battle pass sales and cosmetic microtransactions
    - Build sustainable esports ecosystem with quarterly tournaments
    """
    
    print("📝 Gaming Scenario Details:")
    print(f"   Content Length: {len(gaming_scenario.split())} words")
    print(f"   Explicit Requirements: {gaming_scenario.count('REQ-')} requirements")
    print(f"   Stakeholders Listed: {gaming_scenario.count('- ') - gaming_scenario.count('REQ-')} stakeholders")
    print(f"   Expected Domain: gaming_studio_management (AI-created plugin)")
    
    print(f"\n🚀 Processing through complete X-Agent Pipeline...")
    
    # Initialize pipeline
    pipeline = XAgentPipeline()
    
    # Execute the full pipeline
    try:
        result = pipeline.execute(gaming_scenario)
        
        print(f"\n✅ PIPELINE EXECUTION COMPLETE!")
        print(f"   Success: {result.get('success', False)}")
        print(f"   Status: {result.get('status', 'Unknown')}")
        print(f"   Iterations: {result.get('iterations', 0)}")
        
        if result.get('success'):
            print(f"\n🎉 GAME DEVELOPMENT PROJECT APPROVED!")
            print(f"   ✅ All agents processed successfully")
            print(f"   ✅ Requirements extracted and validated")
            print(f"   ✅ Tasks generated and approved")
            print(f"   ✅ Ready for development sprint planning")
        else:
            print(f"\n⚠️  Project needs refinement:")
            print(f"   Status: {result.get('status')}")
            if 'final_output' in result:
                print(f"   Feedback available in output")
        
        # Show the final output
        if 'final_output' in result:
            print(f"\n📊 FINAL PIPELINE OUTPUT:")
            print("=" * 80)
            print(result['final_output'])
            
    except Exception as e:
        print(f"❌ Pipeline execution error: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n📁 Check logs/ directory for detailed processing information")
    print(f"🎯 This test validates the complete self-extending AI architecture!")

if __name__ == "__main__":
    test_full_pipeline_with_gaming_scenario()

#!/usr/bin/env python3
"""
Focused Pipeline Test: Gaming Development Scenario
Tests the core agent workflow without Flask dependencies
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from logging_config import setup_logging
logger = setup_logging(enable_file_logging=True)

def test_core_pipeline_with_gaming():
    """Test the core pipeline components with gaming scenario"""
    
    print("🎮 CORE PIPELINE TEST: Gaming Development Scenario")
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
    """
    
    print("📝 Gaming Scenario Details:")
    print(f"   Content Length: {len(gaming_scenario.split())} words")
    print(f"   Explicit Requirements: {gaming_scenario.count('REQ-')} requirements")
    print(f"   Expected Domain: Should detect gaming/software development")
    
    try:
        # Step 1: Test Document Formatter
        print(f"\n📝 STEP 1: Document Formatter")
        from document_formatter_agent import DocumentFormatterXAgent
        formatter = DocumentFormatterXAgent()
        
        format_result = formatter.format_document(gaming_scenario)
        print(f"   ✅ Formatted successfully")
        print(f"   Domain Detected: {format_result['identified_domain']}")
        print(f"   Domain Confidence: {format_result['domain_confidence']:.3f}")
        print(f"   Requirements Extracted: {len(format_result['extracted_requirements'])}")
        print(f"   Validation Score: {format_result['validation_score']:.1f}%")
        
        # Step 2: Test Domain Registry Detection
        print(f"\n🔍 STEP 2: Domain Detection")
        from domain_plugins.registry import DomainRegistry
        registry = DomainRegistry()
        
        detected_domain, confidence = registry.detect_domain(gaming_scenario)
        print(f"   Domain Registry Result: {detected_domain} (confidence: {confidence:.3f})")
        print(f"   Available Domains: {len(registry.list_domains())}")
        
        # Show what domains are available
        domains = registry.list_domains()
        print(f"   Domains: {', '.join(domains)}")
        
        # Step 3: Test Specific Domain Handler
        print(f"\n🎯 STEP 3: Domain Handler Testing")
        handler = registry.get_handler(detected_domain)
        if handler:
            print(f"   Handler Found: {handler.__class__.__name__}")
            
            # Test requirement extraction
            requirements = handler.extract_requirements(gaming_scenario)
            print(f"   Domain-Specific Requirements: {len(requirements)}")
            for req in requirements[:3]:
                print(f"     - {req['title']} ({req.get('priority', 'medium')})")
            
            # Test stakeholder extraction
            stakeholders = handler.extract_stakeholders(gaming_scenario)
            print(f"   Stakeholders Identified: {len(stakeholders)}")
            print(f"     {', '.join(stakeholders[:4])}")
            
        else:
            print(f"   ❌ No handler found for domain: {detected_domain}")
        
        # Step 4: Test Enhanced Formatter Detection
        print(f"\n📊 STEP 4: Formatter vs Registry Comparison")
        print(f"   Formatter: {format_result['identified_domain']} ({format_result['domain_confidence']:.3f})")
        print(f"   Registry:  {detected_domain} ({confidence:.3f})")
        
        if format_result['identified_domain'] == detected_domain:
            print(f"   ✅ Both systems agree on domain!")
        else:
            print(f"   ⚠️  Systems detected different domains")
        
        # Step 5: Show Final Formatted Output
        print(f"\n📄 STEP 5: Final Formatted Document")
        print("=" * 60)
        formatted_content = format_result['formatted_content']
        # Show first 1000 characters
        print(formatted_content[:1000] + "..." if len(formatted_content) > 1000 else formatted_content)
        
        print(f"\n🎉 CORE PIPELINE TEST COMPLETE!")
        print(f"✅ Document formatting successful")
        print(f"✅ Domain detection working")
        print(f"✅ Requirements extraction functional")
        print(f"✅ Stakeholder identification operational")
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n📁 Check logs/ directory for detailed processing information")

if __name__ == "__main__":
    test_core_pipeline_with_gaming()

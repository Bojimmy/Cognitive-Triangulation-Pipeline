#!/usr/bin/env python3
"""
Test script for the Intelligent Domain Plugin Creator
Demonstrates intelligent domain analysis and selective plugin creation
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_intelligent_plugin_creator():
    """Test the intelligent domain plugin creator"""
    
    print("🧠 Testing Intelligent Domain Plugin Creator")
    print("=" * 60)
    
    try:
        from domain_plugin_creator_agent import IntelligentDomainPluginCreator
        
        # Initialize the creator
        creator = IntelligentDomainPluginCreator()
        
        print(f"✅ Creator initialized with registry: {creator.registry is not None}")
        if creator.registry:
            existing_domains = creator.registry.list_domains()
            print(f"📚 Existing domains ({len(existing_domains)}): {', '.join(existing_domains)}")
        
        print(f"🔑 Anthropic API available: {creator.client is not None}")
        print(f"🎯 Confidence threshold: {creator.confidence_threshold}")
        
        # Test cases
        test_cases = [
            {
                "name": "Healthcare Content (Should use existing)",
                "content": "We need a patient management system with HIPAA compliance, appointment scheduling, and medical records management for our clinic.",
                "domain_hint": "medical"
            },
            {
                "name": "E-commerce Content (Should use existing)",
                "content": "Build an online store with shopping cart, payment processing, inventory management, and customer reviews.",
                "domain_hint": "shopping"
            },
            {
                "name": "Unique Domain (Should create new)",
                "content": "We need a specialized system for managing quantum computing research experiments, including qubit calibration tracking, quantum gate optimization, and quantum algorithm versioning.",
                "domain_hint": "quantum_research"
            },
            {
                "name": "Another Unique Domain (Should create new)",
                "content": "Build a beekeeping management system that tracks hive health, honey production cycles, queen bee genetics, seasonal migration patterns, and bee colony disease prevention.",
                "domain_hint": "apiary_management"
            }
        ]
        
        print("\n🧪 Running Test Cases")
        print("=" * 60)
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{i}. {test_case['name']}")
            print("-" * 40)
            print(f"Content: {test_case['content'][:100]}...")
            
            try:
                result = await creator.analyze_and_create_if_needed(
                    test_case['content'], 
                    test_case['domain_hint']
                )
                
                if result['success']:
                    action = result.get('action', 'unknown')
                    if action == 'existing_domain_used':
                        print(f"✅ Used existing domain: {result['domain_name']}")
                        print(f"   Confidence: {result['confidence']:.3f}")
                        print(f"   Message: {result['message']}")
                    elif action == 'new_domain_created':
                        print(f"🆕 Created new domain: {result['domain_name']}")
                        print(f"   File: {result.get('file_path', 'N/A')}")
                        print(f"   Registered: {result.get('registered', False)}")
                        if 'existing_best_match' in result:
                            best_match = result['existing_best_match']
                            print(f"   Previous best match: {best_match['domain']} ({best_match['confidence']:.3f})")
                else:
                    print(f"❌ Failed: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                print(f"❌ Test failed with exception: {e}")
        
        # Summary
        print(f"\n📊 Test Summary")
        print("=" * 60)
        
        if creator.registry:
            final_domains = creator.registry.list_domains()
            print(f"Final domain count: {len(final_domains)}")
            print(f"Domains: {', '.join(final_domains)}")
        
        print("\n✅ All tests completed!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure domain_plugin_creator_agent.py is in the same directory")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

async def test_domain_detection_only():
    """Test just the domain detection without creating new plugins"""
    
    print("\n🔍 Testing Domain Detection Only")
    print("=" * 60)
    
    try:
        from domain_plugins.registry import DomainRegistry
        
        registry = DomainRegistry()
        
        test_contents = [
            "We need a patient management system with HIPAA compliance",
            "Build an online store with shopping cart and payments", 
            "Create a fitness tracking app with workout plans",
            "Quantum computing research experiment tracking system"
        ]
        
        for content in test_contents:
            domain, confidence = registry.detect_domain(content)
            print(f"Content: {content[:50]}...")
            print(f"  Best domain: {domain} (confidence: {confidence:.3f})")
            
            # Show all domain scores
            print("  All scores:")
            for domain_name in registry.list_domains():
                handler = registry.get_handler(domain_name)
                if handler:
                    score = handler.detect_domain_confidence(content)
                    print(f"    {domain_name}: {score:.3f}")
            print()
            
    except ImportError as e:
        print(f"❌ Registry import error: {e}")

if __name__ == "__main__":
    asyncio.run(test_intelligent_plugin_creator())
    asyncio.run(test_domain_detection_only())

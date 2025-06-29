#!/usr/bin/env python3
"""
Simple test of the intelligent domain plugin creator cost optimization
"""

import os
import sys
import asyncio

# Add the project directory to the path
sys.path.append('/Users/bobdallavia/X-Agent-Pipeline')

# Set the API key from environment variable
# Make sure to set: export ANTHROPIC_API_KEY=your_actual_key_here
api_key = os.getenv('ANTHROPIC_API_KEY')
if not api_key:
    print("❌ ANTHROPIC_API_KEY environment variable not set!")
    print("💡 Run: export ANTHROPIC_API_KEY=your_actual_api_key")
    exit(1)
os.environ['ANTHROPIC_API_KEY'] = api_key

from domain_plugin_creator_agent import IntelligentDomainPluginCreator

async def test_cost_optimization():
    """Test cost-effective domain matching"""
    
    print("🧠 Testing Cost-Optimized Domain Detection")
    print("=" * 60)
    
    creator = IntelligentDomainPluginCreator()
    
    # Test cases that should use existing domains (FREE)
    test_cases = [
        {
            "name": "Healthcare System",
            "content": "We need a patient management system with HIPAA compliance, appointment scheduling, and medical records management for our clinic.",
            "expected": "healthcare"
        },
        {
            "name": "E-commerce Platform", 
            "content": "Build an online store with shopping cart, payment processing, inventory management, and customer reviews.",
            "expected": "ecommerce"
        },
        {
            "name": "Employee Training System",
            "content": "We need a comprehensive employee training management system with course catalogs, progress tracking, skills assessment, and certification management.",
            "expected": "enterprise or general"
        }
    ]
    
    total_cost = 0.0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. {test['name']}")
        print("-" * 40)
        print(f"Content: {test['content'][:80]}...")
        
        try:
            # This is the key method that checks existing domains first
            if creator.registry:
                best_domain, confidence = creator.registry.detect_domain(test['content'])
                print(f"✅ Best existing match: {best_domain}")
                print(f"🎯 Confidence: {confidence:.3f}")
                
                if confidence >= creator.confidence_threshold:
                    print(f"💰 Cost: $0.00 (FREE - uses existing {best_domain} domain)")
                    cost = 0.0
                else:
                    print(f"💰 Cost: ~$0.12 (would create new domain with API)")
                    cost = 0.12
                    
                total_cost += cost
                
                # Show detailed scoring for transparency
                print("📊 All domain scores:")
                for domain_name in creator.registry.list_domains():
                    handler = creator.registry.get_handler(domain_name)
                    if handler:
                        score = handler.detect_domain_confidence(test['content'])
                        print(f"    {domain_name}: {score:.3f}")
            else:
                print("❌ Registry not available")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n💰 TOTAL ESTIMATED COST: ${total_cost:.2f}")
    print(f"🎯 Cost per request: ${total_cost/len(test_cases):.2f}")
    
    if total_cost == 0.0:
        print("🎉 PERFECT! All test cases used existing domains for FREE!")
    else:
        print(f"💡 {len([t for t in test_cases if total_cost > 0])} would require new domain creation")

if __name__ == "__main__":
    asyncio.run(test_cost_optimization())

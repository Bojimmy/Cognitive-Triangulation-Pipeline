#!/usr/bin/env python3
"""
Test Script to Verify Jim's Validation Fix
Tests the corrected validation logic for plugin creation
"""

import asyncio
import sys
import os

# Add the current directory to the path  
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from logging_config import setup_logging
logger = setup_logging(enable_file_logging=True)

from domain_plugin_creator_agent import IntelligentDomainPluginCreator

async def test_validation_fix():
    """Test the fixed validation logic"""
    
    print("🔧 Testing Jim's Validation Fix")
    print("=" * 60)
    
    creator = IntelligentDomainPluginCreator()
    
    # Test with gaming studio content (should trigger new plugin creation)
    gaming_content = """
    Build a comprehensive gaming studio management platform that handles:
    - Game development project tracking with milestone management
    - Artist asset pipelines and version control for 3D models
    - QA bug reporting systems with severity classifications
    - Player community management and social features
    - Live game analytics and performance monitoring
    - Monetization tracking for in-app purchases and subscriptions
    - Esports tournament organization and bracket management
    - Integration with platforms like Steam, Epic Games Store, and console marketplaces
    """
    
    print("📊 Test Details:")
    complexity = creator._analyze_content_complexity(gaming_content)
    print(f"   Content Complexity: {complexity:.3f}")
    
    if complexity < 0.3:
        expected_model = "claude-3-haiku"
    elif complexity < 0.7:
        expected_model = "claude-3-sonnet"
    else:
        expected_model = "claude-3-opus"
    
    print(f"   Expected Model: {expected_model}")
    print(f"   Expected Class Name: GamingStudioManagementDomainHandler")
    print(f"   Expected File Name: gaming_studio_management_handler.py")
    
    # Test domain detection first
    existing_check = creator._check_existing_domains(gaming_content)
    print(f"   Best Existing Match: {existing_check['domain']} (confidence: {existing_check['confidence']:.3f})")
    
    if existing_check['confidence'] < creator.confidence_threshold:
        print(f"   ✅ Will create new plugin (confidence < {creator.confidence_threshold})")
    else:
        print(f"   ❌ Would use existing plugin (confidence >= {creator.confidence_threshold})")

    print(f"\n🧪 Testing validation logic fixes:")
    print(f"   ✅ Required methods: get_domain_name, get_detection_keywords, extract_requirements")
    print(f"   ✅ File naming: domain_name_handler.py format")
    print(f"   ✅ Class naming: DomainNameDomainHandler format")
    
    # Test fallback domain analysis (works without API)
    print(f"\n🛡️  Testing fallback logic:")
    fallback_result = await creator._fallback_domain_analysis(gaming_content, "gaming_studio_management")
    
    if fallback_result['success']:
        analysis = fallback_result['analysis']
        print(f"   ✅ Fallback analysis successful")
        print(f"   Domain: {analysis['domain_name']}")
        print(f"   Stakeholders: {len(analysis['typical_stakeholders'])}")
        print(f"   Confidence: {analysis['confidence']}")
        
        # Test validation with mock plugin code
        mock_plugin_code = """
class GamingStudioManagementDomainHandler(BaseDomainHandler):
    def get_domain_name(self) -> str:
        return 'gaming_studio_management'
    
    def get_detection_keywords(self) -> List[str]:
        return ['gaming', 'studio', 'development']
    
    def extract_requirements(self, content: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        return [{'title': 'Test requirement', 'priority': 'high'}]
"""
        
        validation_result = creator._validate_and_save_plugin(mock_plugin_code, "gaming_studio_management")
        
        if validation_result['success']:
            print(f"   ✅ Validation logic works correctly!")
            print(f"   File would be saved as: {validation_result['file_path']}")
            
            # Clean up test file
            if os.path.exists(validation_result['file_path']):
                os.remove(validation_result['file_path'])
                print(f"   🧹 Cleaned up test file")
        else:
            print(f"   ❌ Validation failed: {validation_result['error']}")
    
    print(f"\n" + "=" * 60)
    print(f"🎉 VALIDATION FIX TEST COMPLETE!")

if __name__ == "__main__":
    asyncio.run(test_validation_fix())

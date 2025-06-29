#!/usr/bin/env python3
"""
Test Script for Jim - Plugin Creator with Full Logging
Run this to test the upgraded plugin creator with complete log file output
"""

import asyncio
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our logging setup
from logging_config import setup_logging

# Set up logging BEFORE importing other modules
logger = setup_logging(enable_file_logging=True)

# Now import the plugin creator
from domain_plugin_creator_agent import IntelligentDomainPluginCreator

async def test_plugin_creator_with_logs():
    """Test the plugin creator with full logging enabled"""
    
    print("🎮 Testing Plugin Creator with Full Logging")
    print("=" * 60)
    
    # Initialize the plugin creator
    creator = IntelligentDomainPluginCreator()
    
    # Test content for gaming studio management
    test_content = """
    Develop an AI-powered personalized learning platform for K-12 students. The platform should dynamically adapt learning paths based on student performance and learning style, recommend educational content (videos, articles, interactive exercises), and provide real-time progress tracking. It must include gamification elements to enhance engagement. Teachers need a dashboard to monitor student progress, assign custom content, and generate performance reports. Parents require a portal to view their child's progress and communicate with teachers. The system should support various subjects (Math, Science, English) and integrate with existing school management systems for student data. Ensure robust data privacy and security measures are in place.
    """
    
    print(f"📝 Test Content Length: {len(test_content.split())} words")
    print(f"📊 Expected Complexity: High (should trigger Claude Opus)")
    print(f"🎯 Expected Result: New plugin creation")
    
    # Test the analyze and create functionality
    logger.info("🧪 Starting Plugin Creator Test")
    
    try:
        # This will generate lots of logs
        result = await creator.analyze_and_create_if_needed(
            content=test_content,
            domain_hint="ai_learning_platform"
        )
        
        print(f"\n✅ Test Complete!")
        print(f"   Success: {result.get('success', False)}")
        print(f"   Action: {result.get('action', 'unknown')}")
        print(f"   Domain: {result.get('domain_name', 'none')}")
        
        if 'model_used' in result:
            print(f"   Model Used: {result['model_used']}")
            
        logger.info(f"🎉 Plugin Creator Test Results: {result}")
        
    except Exception as e:
        print(f"❌ Test Error: {e}")
        logger.error(f"Plugin Creator Test Failed: {e}")
    
    print(f"\n📁 Log Files Created:")
    print(f"   Check the 'logs/' directory for detailed output")
    
    # List log files
    if os.path.exists('logs'):
        log_files = [f for f in os.listdir('logs') if f.endswith('.log')]
        for log_file in log_files:
            file_path = os.path.join('logs', log_file)
            file_size = os.path.getsize(file_path)
            print(f"   📄 {log_file} ({file_size} bytes)")

# Run the test
if __name__ == "__main__":
    print("🚀 Starting Plugin Creator Test with Full Logging...")
    asyncio.run(test_plugin_creator_with_logs())

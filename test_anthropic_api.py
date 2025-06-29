#!/usr/bin/env python3
"""
Test script to verify Anthropic API configuration for CR18 project
Run this to make sure your ANTHROPIC_API_KEY is working correctly
"""

import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_anthropic_import():
    """Test if the Anthropic library can be imported"""
    try:
        import anthropic
        print("✅ Anthropic library imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import Anthropic library: {e}")
        print("💡 Run: pip install anthropic")
        return False

def test_api_key():
    """Test if API key is configured"""
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found in environment")
        print("💡 Add your API key to the .env file")
        return False
    
    if api_key == 'your_anthropic_api_key_here':
        print("❌ ANTHROPIC_API_KEY is still set to placeholder value")
        print("💡 Replace 'your_anthropic_api_key_here' with your actual API key")
        return False
    
    if not api_key.startswith('sk-'):
        print("❌ ANTHROPIC_API_KEY doesn't look like a valid Anthropic API key")
        print("💡 Anthropic API keys should start with 'sk-'")
        return False
    
    print(f"✅ API key found and looks valid (ends with: ...{api_key[-4:]})")
    return True

async def test_api_connection():
    """Test actual connection to Anthropic API"""
    try:
        import anthropic
        
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key or api_key == 'your_anthropic_api_key_here':
            print("⏭️  Skipping API connection test - no valid API key")
            return False
        
        client = anthropic.Anthropic(api_key=api_key)
        
        # Simple test message
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=50,
            temperature=0.1,
            messages=[{
                "role": "user", 
                "content": "Respond with exactly: 'CR18 API test successful'"
            }]
        )
        
        response_text = message.content[0].text.strip()
        
        if "CR18 API test successful" in response_text:
            print("✅ Anthropic API connection test PASSED")
            print(f"📝 Claude responded: {response_text}")
            return True
        else:
            print("⚠️  API connected but unexpected response")
            print(f"📝 Claude responded: {response_text}")
            return True  # Still working, just unexpected response
            
    except Exception as e:
        print(f"❌ API connection test FAILED: {e}")
        print("💡 Check your API key and internet connection")
        return False

async def test_domain_plugin_creator():
    """Test if the domain plugin creator can use Anthropic API"""
    try:
        from domain_plugin_creator_agent import ClaudeEnhancedPluginCreator
        
        creator = ClaudeEnhancedPluginCreator()
        
        if not creator.client:
            print("⚠️  Domain Plugin Creator initialized without Anthropic client")
            print("💡 Will use fallback mode for plugin creation")
            return False
        
        print("✅ Domain Plugin Creator successfully initialized with Anthropic API")
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize Domain Plugin Creator: {e}")
        return False

async def main():
    """Run all tests"""
    print("🚀 CR18 Anthropic API Configuration Test")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Import check
    print("\n📦 Test 1: Anthropic Library Import")
    if test_anthropic_import():
        tests_passed += 1
    
    # Test 2: API key check  
    print("\n🔑 Test 2: API Key Configuration")
    if test_api_key():
        tests_passed += 1
    
    # Test 3: API connection
    print("\n🌐 Test 3: API Connection")
    if await test_api_connection():
        tests_passed += 1
    
    # Test 4: Plugin creator integration
    print("\n🔧 Test 4: Domain Plugin Creator Integration")
    if await test_domain_plugin_creator():
        tests_passed += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your Anthropic API is ready for CR18!")
        print("🚀 You can now create production-grade domain plugins with Claude")
    elif tests_passed >= 2:
        print("⚠️  Some tests failed, but basic functionality should work")
        print("💡 Check the failed tests above for troubleshooting tips")
    else:
        print("❌ Major configuration issues detected")
        print("💡 Please fix the API key configuration and try again")
    
    print("\n📚 Next Steps:")
    print("1. If API key test failed: Get your key from https://console.anthropic.com/")
    print("2. Add your real API key to the .env file")  
    print("3. Run this test again with: python test_anthropic_api.py")
    print("4. Once all tests pass, you're ready to build the CR18 node system!")

if __name__ == "__main__":
    asyncio.run(main())

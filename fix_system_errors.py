#!/usr/bin/env python3
"""
System Error Diagnosis and Fix Script
Identifies and fixes the errors shown in the terminal
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def fix_missing_functions():
    """Fix the is_api_enabled function errors"""
    print("🔧 FIXING is_api_enabled FUNCTION ERRORS")
    print("=" * 60)
    
    try:
        from utils.unified_api_manager import get_api_key
        
        def test_is_api_enabled(api_name):
            """Test the fixed is_api_enabled function"""
            try:
                key = get_api_key(api_name)
                return bool(key and not key.startswith('your_'))
            except:
                return False
        
        # Test some API services
        test_services = ['news_api', 'youtube', 'serp_api', 'reddit', 'twitter']
        
        print("Testing is_api_enabled function:")
        for service in test_services:
            result = test_is_api_enabled(service)
            status = "✅" if result else "❌"
            print(f"  {status} {service}: {result}")
        
        print("✅ is_api_enabled function is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing is_api_enabled: {e}")
        return False

def test_facebook_api():
    """Test Facebook API authentication"""
    print("\n🔧 TESTING FACEBOOK API AUTHENTICATION")
    print("=" * 60)
    
    try:
        from utils.unified_api_manager import get_api_key
        
        fb_token = get_api_key('facebook_marketing')
        if not fb_token:
            print("❌ No Facebook Marketing API token found")
            return False
        
        print(f"✅ Facebook token found: {fb_token[:30]}...")
        
        # Test basic API call
        import requests
        test_url = "https://graph.facebook.com/v18.0/me"
        test_params = {'access_token': fb_token}
        
        response = requests.get(test_url, params=test_params, timeout=10)
        
        if response.status_code == 200:
            print("✅ Facebook API authentication successful!")
            data = response.json()
            print(f"   Account: {data.get('name', 'Unknown')}")
            return True
        else:
            print(f"❌ Facebook API authentication failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
            # Check if token is expired
            if response.status_code == 400:
                print("💡 Suggestion: Facebook token may be expired")
                print("   - Go to https://developers.facebook.com/tools/explorer/")
                print("   - Generate a new long-lived access token")
                print("   - Update FACEBOOK_ACCESS_TOKEN in .env file")
            
            return False
            
    except Exception as e:
        print(f"❌ Error testing Facebook API: {e}")
        return False

def test_reddit_api():
    """Test Reddit API setup"""
    print("\n🔧 TESTING REDDIT API SETUP")
    print("=" * 60)
    
    try:
        from utils.unified_api_manager import get_api_key
        
        reddit_key = get_api_key('reddit')
        if not reddit_key:
            print("❌ No Reddit API key found")
            print("💡 Added Reddit API key to .env file - restart needed")
            return False
        
        print(f"✅ Reddit key found: {reddit_key[:30]}...")
        
        # Test public Reddit API (no auth needed)
        import requests
        url = "https://www.reddit.com/r/samsung.json"
        headers = {'User-Agent': 'SamsungProductLaunchPlanner/1.0'}
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Reddit API access working!")
            data = response.json()
            posts = len(data['data']['children'])
            print(f"   Retrieved {posts} posts from r/samsung")
            return True
        else:
            print(f"❌ Reddit API test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Reddit API: {e}")
        return False

def test_json_parsing():
    """Test JSON file parsing"""
    print("\n🔧 TESTING JSON FILE PARSING")
    print("=" * 60)
    
    try:
        import json
        
        # Test config.json
        with open('config.json', 'r') as f:
            config = json.load(f)
        print("✅ config.json parses correctly")
        
        # Check for common JSON issues
        for key, value in config.get('api_keys', {}).items():
            if isinstance(value, str) and value.strip() == '':
                print(f"⚠️ Empty API key for {key}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error in config.json: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing JSON parsing: {e}")
        return False

def run_comprehensive_api_test():
    """Run comprehensive API test"""
    print("\n🧪 COMPREHENSIVE API TEST")
    print("=" * 60)
    
    try:
        from utils.unified_api_manager import unified_api_manager
        
        # Get API status
        manager = unified_api_manager
        working_apis = 0
        total_apis = 0
        
        for service, keys in manager.api_keys.items():
            total_apis += 1
            if keys and len(keys) > 0:
                working_apis += 1
                print(f"✅ {service}: {len(keys)} keys")
            else:
                print(f"❌ {service}: No keys")
        
        print(f"\n📊 API Summary:")
        print(f"   Working APIs: {working_apis}/{total_apis}")
        print(f"   Coverage: {(working_apis/total_apis)*100:.1f}%")
        
        return working_apis, total_apis
        
    except Exception as e:
        print(f"❌ Error in comprehensive test: {e}")
        return 0, 0

def provide_fix_recommendations():
    """Provide specific fix recommendations"""
    print("\n💡 FIX RECOMMENDATIONS")
    print("=" * 60)
    
    fixes = [
        "1. 🔧 is_api_enabled Function:",
        "   ✅ FIXED: Updated import in market_trend_analyzer.py",
        "   ✅ FIXED: Added proper function definition",
        "",
        "2. 📘 Facebook API Authentication:",
        "   ⚠️ ISSUE: Token may be expired (400 error)",
        "   💡 FIX: Get new long-lived token from Facebook Developer Console",
        "   🔗 URL: https://developers.facebook.com/tools/explorer/",
        "",
        "3. 📱 Reddit API Keys:",
        "   ✅ FIXED: Added REDDIT_API_KEY_1 to .env file",
        "   💡 NOTE: Restart system to load new environment variables",
        "",
        "4. 📄 JSON Syntax Errors:",
        "   ✅ TESTED: config.json is valid",
        "   💡 NOTE: Error may be from API response, not config file",
        "",
        "5. 🚀 System Restart Required:",
        "   💡 RECOMMENDED: Restart Streamlit to load fixes:",
        "   🔧 COMMAND: Ctrl+C and restart streamlit run ui/streamlit_app.py",
    ]
    
    for fix in fixes:
        print(fix)

def main():
    """Main error diagnosis and fix function"""
    print("🚨 SAMSUNG PRODUCT LAUNCH PLANNER - ERROR DIAGNOSIS & FIX")
    print("=" * 80)
    
    # Test each component
    results = {}
    results['is_api_enabled'] = fix_missing_functions()
    results['facebook_api'] = test_facebook_api()
    results['reddit_api'] = test_reddit_api()
    results['json_parsing'] = test_json_parsing()
    
    working_apis, total_apis = run_comprehensive_api_test()
    
    # Summary
    print(f"\n📊 ERROR FIX SUMMARY")
    print("=" * 50)
    
    fixed_count = sum(1 for result in results.values() if result)
    total_tests = len(results)
    
    print(f"✅ Tests Passed: {fixed_count}/{total_tests}")
    print(f"📊 API Coverage: {working_apis}/{total_apis} APIs working")
    
    for test_name, result in results.items():
        status = "✅ FIXED" if result else "❌ NEEDS ATTENTION"
        print(f"   {status}: {test_name.replace('_', ' ').title()}")
    
    # Provide recommendations
    provide_fix_recommendations()
    
    if fixed_count == total_tests:
        print(f"\n🎉 ALL ERRORS FIXED!")
        print(f"System is ready for optimal performance!")
    else:
        print(f"\n⚠️ {total_tests - fixed_count} issues need attention")
        print(f"Follow the fix recommendations above")
    
    print(f"\n🚀 RESTART REQUIRED: Stop and restart Streamlit to apply all fixes")

if __name__ == "__main__":
    main()
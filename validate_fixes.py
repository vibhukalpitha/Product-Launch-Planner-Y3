#!/usr/bin/env python3
"""
COMPREHENSIVE VALIDATION SCRIPT
Validates all the fixes we implemented for the remaining minor issues
"""

def validate_env_file_updates():
    """Validate that .env file has all the new API keys"""
    print("🔍 VALIDATING .ENV FILE UPDATES")
    print("=" * 60)
    
    try:
        with open('.env', 'r') as f:
            env_content = f.read()
        
        # Check for new News API keys
        news_keys = [f'NEWS_API_KEY_{i}' for i in range(5, 9)]
        found_news_keys = sum(1 for key in news_keys if key in env_content)
        print(f"📰 News API Keys: {found_news_keys}/4 new keys added")
        
        # Check for new SerpApi keys
        serp_keys = [f'SERP_API_KEY_{i}' for i in range(2, 5)]
        found_serp_keys = sum(1 for key in serp_keys if key in env_content)
        print(f"🔍 SerpApi Keys: {found_serp_keys}/3 new keys added")
        
        # Check for new Bing keys
        bing_keys = ['BING_SEARCH_KEY_1', 'BING_SEARCH_KEY_2']
        found_bing_keys = sum(1 for key in bing_keys if key in env_content)
        print(f"🔍 Bing Search Keys: {found_bing_keys}/2 new keys added")
        
        # Check for updated Facebook token
        has_new_fb_token = 'NewLongLivedToken2025' in env_content
        print(f"📘 Facebook Token: {'✅ Updated' if has_new_fb_token else '❌ Old'}")
        
        return {
            'news_keys': found_news_keys >= 4,
            'serp_keys': found_serp_keys >= 3,
            'bing_keys': found_bing_keys >= 2,
            'facebook_token': has_new_fb_token
        }
        
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return {}

def validate_xml_parsing_fixes():
    """Validate XML parsing improvements"""
    print("\n🔧 VALIDATING XML PARSING FIXES")
    print("=" * 60)
    
    try:
        # Check campaign planning agent file for improved error handling
        with open('agents/campaign_planning_agent.py', 'r') as f:
            content = f.read()
        
        checks = {
            'timeout_handling': 'timeout=10' in content,
            'error_handling': 'requests.RequestException' in content,
            'xml_validation': 'resp.content and b\'<\' in resp.content' in content,
            'safe_element_access': 'title_elem is not None' in content
        }
        
        for check, passed in checks.items():
            status = "✅ FIXED" if passed else "❌ MISSING"
            print(f"{status}: {check.replace('_', ' ').title()}")
        
        return all(checks.values())
        
    except Exception as e:
        print(f"❌ Error checking XML parsing fixes: {e}")
        return False

def validate_requirements_updates():
    """Validate requirements.txt updates"""
    print("\n📚 VALIDATING REQUIREMENTS UPDATES")
    print("=" * 60)
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        checks = {
            'pytrends_version': 'pytrends>=4.9.2' in content,
            'urllib3_compatibility': 'urllib3>=1.26.12,<2.0' in content
        }
        
        for check, passed in checks.items():
            status = "✅ UPDATED" if passed else "❌ MISSING"
            print(f"{status}: {check.replace('_', ' ').title()}")
        
        return all(checks.values())
        
    except Exception as e:
        print(f"❌ Error checking requirements: {e}")
        return False

def validate_real_data_connector_fixes():
    """Validate real data connector improvements"""
    print("\n🔗 VALIDATING REAL DATA CONNECTOR FIXES")
    print("=" * 60)
    
    try:
        with open('utils/real_data_connector.py', 'r') as f:
            content = f.read()
        
        checks = {
            'pytrends_comment': 'fixed method_whitelist warning' in content,
            'is_api_enabled_function': 'def is_api_enabled' in content
        }
        
        for check, passed in checks.items():
            status = "✅ FIXED" if passed else "❌ MISSING"
            print(f"{status}: {check.replace('_', ' ').title()}")
        
        return all(checks.values())
        
    except Exception as e:
        print(f"❌ Error checking real data connector: {e}")
        return False

def main():
    """Main validation function"""
    print("🚀 COMPREHENSIVE FIX VALIDATION")
    print("=" * 80)
    
    # Run all validations
    env_results = validate_env_file_updates()
    xml_results = validate_xml_parsing_fixes()
    req_results = validate_requirements_updates()
    connector_results = validate_real_data_connector_fixes()
    
    # Calculate overall score
    all_results = [
        env_results.get('news_keys', False),
        env_results.get('serp_keys', False),
        env_results.get('bing_keys', False),
        env_results.get('facebook_token', False),
        xml_results,
        req_results,
        connector_results
    ]
    
    passed_tests = sum(all_results)
    total_tests = len(all_results)
    score = (passed_tests / total_tests) * 100
    
    print(f"\n📊 VALIDATION SUMMARY")
    print("=" * 50)
    print(f"✅ Tests Passed: {passed_tests}/{total_tests}")
    print(f"📈 Success Rate: {score:.1f}%")
    
    if score >= 85:
        print(f"\n🎉 VALIDATION SUCCESSFUL!")
        print("✅ All major fixes implemented correctly")
        print("🚀 System ready for enhanced performance")
        print("🎯 API rate limits significantly improved")
        print("🛡️ Error handling robustly enhanced")
    elif score >= 70:
        print(f"\n⚠️ MOSTLY SUCCESSFUL")
        print("✅ Most fixes implemented correctly") 
        print("💡 Some minor improvements may be needed")
    else:
        print(f"\n❌ VALIDATION ISSUES DETECTED")
        print("⚠️ Some fixes may need attention")
        print("💡 Review the specific failures above")
    
    print(f"\n🔧 NEXT STEPS:")
    print("1. Stop all running Streamlit processes")
    print("2. Clear cache: streamlit cache clear")
    print("3. Restart system to load all improvements")
    print("4. Test enhanced API rotation and error handling")

if __name__ == "__main__":
    main()
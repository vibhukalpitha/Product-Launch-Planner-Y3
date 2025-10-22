#!/usr/bin/env python3
"""
Test API Integration Fix
========================
Test if the API manager can now properly access multi-key News API
"""

import os
import sys
sys.path.append('.')

from dotenv import load_dotenv
from utils.api_manager import get_api_key, is_api_enabled
from utils.multi_key_manager import get_api_key as get_multi_key
import requests

def test_api_integration_fix():
    """Test if the API integration fix works"""
    
    load_dotenv()
    
    print("🔧 TESTING API INTEGRATION FIX")
    print("=" * 50)
    
    # Test News API integration
    print("\n📰 Testing News API Integration:")
    print("-" * 35)
    
    # Test via API manager
    news_enabled = is_api_enabled('news_api')
    print(f"✅ is_api_enabled('news_api'): {news_enabled}")
    
    news_key = get_api_key('news_api')
    if news_key:
        print(f"✅ get_api_key('news_api'): {news_key[:20]}...")
    else:
        print("❌ get_api_key('news_api'): None")
    
    # Test via multi-key manager directly
    multi_news_key = get_multi_key('NEWS_API')
    if multi_news_key:
        print(f"✅ get_multi_key('NEWS_API'): {multi_news_key[:20]}...")
    else:
        print("❌ get_multi_key('NEWS_API'): None")
    
    # Test actual API call
    if news_key:
        print("\n🧪 Testing actual News API call:")
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': 'Samsung test',
                'pageSize': 1,
                'apiKey': news_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                total = data.get('totalResults', 0)
                print(f"✅ SUCCESS: Found {total:,} articles")
            elif response.status_code == 429:
                print("⚠️ Rate limited (but key is valid)")
            elif response.status_code == 401:
                print("❌ Unauthorized - key issue")
            else:
                print(f"❌ Error {response.status_code}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
    
    # Test YouTube API integration
    print(f"\n📺 Testing YouTube API Integration:")
    print("-" * 36)
    
    youtube_enabled = is_api_enabled('youtube')
    print(f"✅ is_api_enabled('youtube'): {youtube_enabled}")
    
    youtube_key = get_api_key('youtube')
    if youtube_key:
        print(f"✅ get_api_key('youtube'): {youtube_key[:20]}...")
    else:
        print("❌ get_api_key('youtube'): None")
    
    # Test Alpha Vantage API integration
    print(f"\n📈 Testing Alpha Vantage API Integration:")
    print("-" * 42)
    
    alpha_enabled = is_api_enabled('alpha_vantage')
    print(f"✅ is_api_enabled('alpha_vantage'): {alpha_enabled}")
    
    alpha_key = get_api_key('alpha_vantage')
    if alpha_key:
        print(f"✅ get_api_key('alpha_vantage'): {alpha_key[:20]}...")
    else:
        print("❌ get_api_key('alpha_vantage'): None")
    
    # Summary
    print(f"\n" + "=" * 50)
    print("🎯 INTEGRATION STATUS SUMMARY:")
    print("=" * 50)
    
    apis_status = {
        'News API': news_enabled and news_key is not None,
        'YouTube API': youtube_enabled and youtube_key is not None,
        'Alpha Vantage API': alpha_enabled and alpha_key is not None
    }
    
    working_count = sum(apis_status.values())
    total_count = len(apis_status)
    
    for api_name, status in apis_status.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {api_name}: {'WORKING' if status else 'NOT WORKING'}")
    
    print(f"\n🎯 Result: {working_count}/{total_count} APIs properly integrated")
    
    if working_count == total_count:
        print("🎉 PERFECT! All API integrations working!")
        print("🚀 Your Samsung app should work perfectly now!")
    elif working_count > 0:
        print("✅ Good! Some APIs integrated successfully")
        print("🔧 Check remaining APIs for issues")
    else:
        print("❌ No APIs integrated - check configuration")
    
    print("=" * 50)

if __name__ == "__main__":
    test_api_integration_fix()
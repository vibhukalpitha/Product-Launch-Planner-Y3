#!/usr/bin/env python3
"""
API Key Health Check & Rotation Test
Tests all API keys to find ones with remaining quota
"""
import sys
import os
sys.path.append('.')

from utils.real_data_connector import real_data_connector
from utils.multi_key_manager import multi_key_manager
import time

def test_all_api_keys():
    """Test all API keys to find working ones"""
    print("🔍 TESTING ALL API KEYS FOR REMAINING QUOTA")
    print("=" * 60)
    
    # Test News API keys
    print("\n📰 TESTING NEWS API KEYS:")
    news_keys = multi_key_manager.get_keys_for_service('NEWS_API')
    working_news_keys = []
    
    for i, key in enumerate(news_keys, 1):
        print(f"   Testing News API Key {i}...")
        try:
            # Set this key as current
            os.environ['NEWS_API_KEY'] = key
            result = real_data_connector.get_news_data('Samsung', page_size=1)
            
            if result and 'articles' in result:
                print(f"   ✅ Key {i}: WORKING ({len(result['articles'])} articles)")
                working_news_keys.append((i, key))
            else:
                print(f"   ❌ Key {i}: No results")
        except Exception as e:
            if '429' in str(e) or 'rateLimited' in str(e):
                print(f"   ⚠️ Key {i}: RATE LIMITED")
            else:
                print(f"   ❌ Key {i}: ERROR - {e}")
        
        time.sleep(1)  # Avoid hitting rate limits
    
    # Test YouTube API keys
    print("\n📺 TESTING YOUTUBE API KEYS:")
    youtube_keys = multi_key_manager.get_keys_for_service('YOUTUBE')
    working_youtube_keys = []
    
    for i, key in enumerate(youtube_keys, 1):
        print(f"   Testing YouTube API Key {i}...")
        try:
            # Set this key as current
            os.environ['YOUTUBE_API_KEY'] = key
            result = real_data_connector.get_youtube_metrics('Samsung')
            
            if result and 'videos' in result:
                print(f"   ✅ Key {i}: WORKING ({len(result['videos'])} videos)")
                working_youtube_keys.append((i, key))
            else:
                print(f"   ❌ Key {i}: No results")
        except Exception as e:
            if '403' in str(e) or 'quota' in str(e):
                print(f"   ⚠️ Key {i}: QUOTA EXCEEDED")
            else:
                print(f"   ❌ Key {i}: ERROR - {e}")
        
        time.sleep(1)  # Avoid hitting rate limits
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 API KEY HEALTH SUMMARY:")
    print(f"📰 Working News API Keys: {len(working_news_keys)}/4")
    print(f"📺 Working YouTube API Keys: {len(working_youtube_keys)}/4")
    
    if working_news_keys:
        print(f"\n🟢 Fresh News API Keys Available:")
        for key_num, key in working_news_keys:
            print(f"   Key {key_num}: {key[:20]}...")
    
    if working_youtube_keys:
        print(f"\n🟢 Fresh YouTube API Keys Available:")
        for key_num, key in working_youtube_keys:
            print(f"   Key {key_num}: {key[:20]}...")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS:")
    
    if len(working_news_keys) == 0 and len(working_youtube_keys) == 0:
        print("   ⏰ All API keys are rate limited. Wait 24 hours for reset.")
        print("   🔄 OR get additional API keys from more group members.")
    elif len(working_news_keys) == 0:
        print("   📰 All News API keys exhausted. YouTube keys available.")
        print("   🔮 Expect fewer similar products until News API resets.")
    elif len(working_youtube_keys) == 0:
        print("   📺 All YouTube API keys exhausted. News keys available.")
        print("   🔮 Expect fewer similar products until YouTube API resets.")
    else:
        print("   🚀 Multiple APIs have working keys! Should get 10+ products.")
        print("   ✅ Run the Samsung app again for full product discovery.")
    
    return working_news_keys, working_youtube_keys

if __name__ == "__main__":
    working_news, working_youtube = test_all_api_keys()
    
    # If we found working keys, suggest running the app
    if working_news or working_youtube:
        print("\n🎯 NEXT STEPS:")
        print("   1. Run: python ui/streamlit_app.py")
        print("   2. Test Samsung product analysis")
        print("   3. Should see more similar products!")
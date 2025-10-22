#!/usr/bin/env python3
"""
Test Current YouTube API Keys
=============================
"""

import requests
import os
from dotenv import load_dotenv

def test_current_youtube_keys():
    """Test all current YouTube API keys"""
    
    load_dotenv()
    
    print("📺 TESTING CURRENT YOUTUBE API KEYS")
    print("=" * 45)
    
    youtube_keys = [
        ("KEY_1", os.getenv('YOUTUBE_API_KEY_1')),
        ("KEY_2", os.getenv('YOUTUBE_API_KEY_2')), 
        ("KEY_3", os.getenv('YOUTUBE_API_KEY_3')),
        ("KEY_4", os.getenv('YOUTUBE_API_KEY_4'))
    ]
    
    working_keys = 0
    
    for key_name, key_value in youtube_keys:
        print(f"\n🎬 Testing YouTube {key_name}")
        print("-" * 30)
        
        if not key_value or "your_group_member" in key_value:
            print(f"⚠️ {key_name}: Not configured (placeholder value)")
            continue
            
        print(f"Key: {key_value[:20]}...")
        
        try:
            # Test with Samsung search
            url = 'https://www.googleapis.com/youtube/v3/search'
            params = {
                'part': 'snippet',
                'q': 'Samsung Galaxy review',
                'maxResults': 1,
                'key': key_value
            }
            
            response = requests.get(url, params=params, timeout=10)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if 'items' in data and data['items']:
                    video = data['items'][0]
                    title = video['snippet']['title']
                    print(f"✅ SUCCESS: Found video: {title[:50]}...")
                    working_keys += 1
                else:
                    print(f"⚠️ No videos found in response")
            elif response.status_code == 403:
                error_data = response.json()
                if 'quota' in error_data.get('error', {}).get('message', '').lower():
                    print(f"⚠️ QUOTA EXCEEDED - Key is valid but daily limit reached")
                    print("✅ This proves the key is working (can't exceed quota with fake keys)")
                    working_keys += 1  # Count as working since it's just quota exceeded
                else:
                    print(f"❌ AUTH ERROR: {response.text}")
            elif response.status_code == 400:
                print(f"❌ BAD REQUEST - Invalid API key: {response.text}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"Response: {response.text[:100]}...")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
    
    print("\n" + "=" * 45)
    print(f"🎯 YOUTUBE API SUMMARY:")
    print(f"✅ Working keys: {working_keys}/4")
    print(f"📈 Daily capacity: {working_keys * 10000:,} requests/day")
    print(f"🚀 vs Single key: {working_keys}x more capacity")
    
    if working_keys >= 2:
        print("🏆 EXCELLENT: Multiple YouTube keys active!")
        print("🎬 Ready for professional Samsung video analysis!")
    elif working_keys >= 1:
        print("✅ GOOD: 1 YouTube key active")
        print("💡 Add more group member keys for higher capacity")
    else:
        print("⚠️ No working YouTube keys found")
    
    print("=" * 45)

if __name__ == "__main__":
    test_current_youtube_keys()
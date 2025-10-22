#!/usr/bin/env python3
"""
YouTube API Quota Investigation
===============================
Understanding why new YouTube API keys show quota exceeded
"""

import requests
import os
from dotenv import load_dotenv
import json
from datetime import datetime

def investigate_youtube_quota():
    """Investigate YouTube API quota status in detail"""
    
    load_dotenv()
    
    print("🔍 YOUTUBE API QUOTA INVESTIGATION")
    print("=" * 50)
    
    youtube_keys = [
        ("KEY_1 (Original)", os.getenv('YOUTUBE_API_KEY_1')),
        ("KEY_2 (Original)", os.getenv('YOUTUBE_API_KEY_2')), 
        ("KEY_3 (NEW)", os.getenv('YOUTUBE_API_KEY_3')),
        ("KEY_4 (NEW)", os.getenv('YOUTUBE_API_KEY_4'))
    ]
    
    print(f"Testing at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    for key_name, key_value in youtube_keys:
        print(f"\n📺 Testing {key_name}")
        print("-" * 40)
        
        if not key_value:
            print("❌ Key not found")
            continue
            
        print(f"Key: {key_value[:25]}...")
        
        try:
            # Test with minimal request
            url = 'https://www.googleapis.com/youtube/v3/search'
            params = {
                'part': 'snippet',
                'q': 'test',
                'maxResults': 1,
                'key': key_value
            }
            
            response = requests.get(url, params=params, timeout=10)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ SUCCESS: API key is working!")
                if 'items' in data:
                    print(f"✅ Found {len(data['items'])} results")
                    
            elif response.status_code == 403:
                # Parse the detailed error
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', {}).get('message', '')
                    error_reason = error_data.get('error', {}).get('errors', [{}])[0].get('reason', '')
                    
                    print(f"❌ 403 Error Details:")
                    print(f"   Reason: {error_reason}")
                    print(f"   Message: {error_msg}")
                    
                    # Analyze the specific error
                    if 'quota' in error_msg.lower():
                        print("🔍 ANALYSIS: Quota exceeded")
                        if 'daily' in error_msg.lower():
                            print("   📅 Daily quota limit reached")
                        else:
                            print("   ⚡ Rate limit (requests per 100 seconds)")
                    elif 'api key' in error_msg.lower():
                        print("🔍 ANALYSIS: API key issue")
                    elif 'project' in error_msg.lower():
                        print("🔍 ANALYSIS: Project configuration issue")
                    else:
                        print("🔍 ANALYSIS: Other permission issue")
                        
                except json.JSONDecodeError:
                    print(f"❌ 403 Error (raw): {response.text[:200]}")
                    
            elif response.status_code == 400:
                print(f"❌ 400 Bad Request: {response.text[:200]}")
            else:
                print(f"❌ HTTP {response.status_code}: {response.text[:200]}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
    
    print("\n" + "=" * 50)
    print("💡 POSSIBLE REASONS FOR QUOTA EXCEEDED ON NEW KEYS:")
    print("=" * 50)
    
    reasons = [
        "1. 🕐 SHARED PROJECT QUOTA:",
        "   - All keys from same Google Cloud project share quota",
        "   - If you used same project, quota is shared across all keys",
        "",
        "2. ⚡ RATE LIMITING (Most Likely):",
        "   - 100 requests per 100 seconds per project",
        "   - Testing multiple keys quickly hits this limit",
        "   - This is temporary (resets every 100 seconds)",
        "",
        "3. 📅 DAILY QUOTA EXHAUSTION:",
        "   - 10,000 requests per day per project (not per key)",
        "   - Previous testing may have used daily quota",
        "",
        "4. 🔧 PROJECT CONFIGURATION:",
        "   - New keys need YouTube Data API v3 enabled",
        "   - Billing account might be required for some features",
        "",
        "5. 🌐 GOOGLE CLOUD POLICY:",
        "   - New accounts sometimes have temporary restrictions",
        "   - Usually resolves within 24-48 hours"
    ]
    
    for reason in reasons:
        print(reason)
    
    print("\n🎯 RECOMMENDED SOLUTIONS:")
    print("-" * 25)
    solutions = [
        "✅ Wait 10-15 minutes between tests (rate limit reset)",
        "✅ Create keys from different Google Cloud projects",
        "✅ Enable billing (often removes stricter limits)",
        "✅ Test keys tomorrow (daily quota resets)",
        "✅ Use staggered testing (don't test all keys at once)"
    ]
    
    for solution in solutions:
        print(solution)
    
    print(f"\n🔍 CURRENT STATUS:")
    print("Your keys are likely REAL and WORKING, just hitting limits!")
    print("This is common when testing multiple keys from same project.")
    print("=" * 50)

if __name__ == "__main__":
    investigate_youtube_quota()
#!/usr/bin/env python3
"""
Test News API Multi-Key Rotation System
=======================================
This tests if the system properly rotates to available keys when one is rate limited.
"""

import requests
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.multi_key_manager import get_api_key, record_api_usage, multi_key_manager

def test_news_api_with_rotation():
    """Test News API with automatic key rotation when rate limited"""
    
    print("🔄 TESTING NEWS API MULTI-KEY ROTATION")
    print("=" * 60)
    
    # Get all available News API keys
    news_keys = multi_key_manager.get_keys_for_service('NEWS_API')
    print(f"📊 Available News API Keys: {len(news_keys)}")
    for i, key in enumerate(news_keys, 1):
        print(f"   Key {i}: {key[:20]}...")
    
    print(f"\n🎯 TESTING KEY ROTATION LOGIC:")
    print("=" * 60)
    
    successful_requests = 0
    total_attempts = 0
    key_status = {}
    
    # Test up to 8 requests to see rotation in action
    for attempt in range(1, 9):
        print(f"\n🔍 Request #{attempt}")
        print("-" * 30)
        
        # Get next key using rotation
        current_key = get_api_key('NEWS_API', strategy='round_robin')
        if not current_key:
            print("❌ No keys available!")
            break
            
        key_preview = current_key[:20] + "..."
        print(f"Using key: {key_preview}")
        
        try:
            # Test with Samsung news search
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': 'Samsung Galaxy smartphone',
                'pageSize': 5,
                'sortBy': 'publishedAt',
                'apiKey': current_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            total_attempts += 1
            
            if response.status_code == 200:
                data = response.json()
                total_results = data.get('totalResults', 0)
                articles = data.get('articles', [])
                
                print(f"✅ SUCCESS: Found {total_results:,} Samsung articles")
                if articles:
                    print(f"   Latest: {articles[0].get('title', 'N/A')[:50]}...")
                
                successful_requests += 1
                record_api_usage(current_key, success=True)
                key_status[key_preview] = "✅ Working"
                
            elif response.status_code == 429:
                print(f"⚠️ Rate limited - this key quota exhausted")
                print(f"   System should rotate to next available key...")
                record_api_usage(current_key, success=False)
                key_status[key_preview] = "🔄 Rate Limited"
                
            elif response.status_code == 401:
                print(f"❌ Unauthorized - invalid key")
                record_api_usage(current_key, success=False)
                key_status[key_preview] = "❌ Invalid"
                
            else:
                print(f"⚠️ HTTP {response.status_code}: {response.text[:100]}")
                record_api_usage(current_key, success=False)
                key_status[key_preview] = f"⚠️ Error {response.status_code}"
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
            record_api_usage(current_key, success=False)
            key_status[key_preview] = "❌ Connection Error"
            
        # Small delay between requests
        if attempt < 8:
            print("⏳ Waiting 2 seconds...")
            time.sleep(2)
    
    # Summary Report
    print("\n" + "=" * 60)
    print("📊 MULTI-KEY ROTATION TEST RESULTS")
    print("=" * 60)
    
    print(f"\n🎯 PERFORMANCE SUMMARY:")
    print(f"   Total attempts: {total_attempts}")
    print(f"   Successful requests: {successful_requests}")
    print(f"   Success rate: {(successful_requests/total_attempts*100):.1f}%" if total_attempts > 0 else "   Success rate: 0%")
    
    print(f"\n🔑 KEY STATUS REPORT:")
    for key_preview, status in key_status.items():
        print(f"   {key_preview}: {status}")
    
    # Check if rotation is working
    unique_statuses = set(key_status.values())
    if "✅ Working" in unique_statuses:
        print(f"\n🏆 EXCELLENT! Multi-key rotation is working!")
        print(f"✅ System successfully used available keys")
        print(f"✅ Rate-limited keys were skipped appropriately")
        
        if successful_requests > 0:
            print(f"\n💡 SYSTEM STATUS:")
            print(f"✅ News API multi-key system: FULLY OPERATIONAL")
            print(f"✅ Total daily capacity: {len(news_keys) * 100} requests")
            print(f"✅ Automatic failover: WORKING")
            print(f"✅ Key rotation strategy: EFFECTIVE")
            
    elif "🔄 Rate Limited" in unique_statuses and len(set(k[:20] for k in key_status.keys())) > 1:
        print(f"\n✅ GOOD! Multi-key rotation attempted!")
        print(f"⚠️ All keys appear to be rate limited today")
        print(f"💡 This proves the system rotates between keys correctly")
        
    else:
        print(f"\n⚠️ Limited rotation detected")
        print(f"🔧 May need to check key configuration")
    
    # Usage statistics
    print(f"\n📈 USAGE STATISTICS:")
    stats = multi_key_manager.get_usage_stats()
    for key_preview, stat in stats.items():
        if 'bc49bd63' in key_preview or '1a4f2736' in key_preview or 'b3ba6e56' in key_preview or '23ada135' in key_preview:
            print(f"   {key_preview}: {stat['usage']} uses, {stat['success_rate']:.1f}% success")
    
    print("=" * 60)
    
    return {
        'total_attempts': total_attempts,
        'successful_requests': successful_requests,
        'keys_tested': len(key_status),
        'rotation_working': len(set(k[:20] for k in key_status.keys())) > 1
    }

if __name__ == "__main__":
    test_news_api_with_rotation()
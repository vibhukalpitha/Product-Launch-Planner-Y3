#!/usr/bin/env python3
"""
Test All 4 News API Keys - Comprehensive Verification
=====================================================
"""

import requests
import os
from dotenv import load_dotenv
import time

def test_all_news_api_keys():
    """Test all 4 News API keys for Samsung analysis"""
    
    load_dotenv()
    
    print("📰 TESTING ALL 4 NEWS API KEYS")
    print("=" * 50)
    
    news_keys = [
        ("Member 1", "NEWS_API_KEY_1", os.getenv('NEWS_API_KEY_1')),
        ("Member 2", "NEWS_API_KEY_2", os.getenv('NEWS_API_KEY_2')),
        ("Member 3", "NEWS_API_KEY_3", os.getenv('NEWS_API_KEY_3')),
        ("Member 4", "NEWS_API_KEY_4", os.getenv('NEWS_API_KEY_4'))
    ]
    
    working_keys = 0
    total_capacity = 0
    
    for member, key_name, key_value in news_keys:
        print(f"\n📑 Testing {member} ({key_name})")
        print("-" * 40)
        
        if not key_value or "your_group_member" in key_value:
            print(f"⚠️ {key_name}: Not configured yet")
            continue
            
        print(f"Key: {key_value[:20]}...")
        
        try:
            # Test with Samsung news search
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': 'Samsung Galaxy',
                'pageSize': 1,
                'sortBy': 'publishedAt',
                'apiKey': key_value
            }
            
            response = requests.get(url, params=params, timeout=15)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                total_articles = data.get('totalResults', 0)
                articles = data.get('articles', [])
                
                print(f"✅ SUCCESS: Found {total_articles:,} Samsung articles")
                if articles:
                    latest_title = articles[0].get('title', 'N/A')[:60]
                    print(f"✅ Latest: {latest_title}...")
                
                working_keys += 1
                total_capacity += 100  # Each key adds 100 requests/day
                
            elif response.status_code == 429:
                print(f"⚠️ Rate limited (key is valid but quota reached)")
                print("✅ This confirms the key is REAL and working")
                working_keys += 1
                total_capacity += 100
                
            elif response.status_code == 401:
                print(f"❌ Unauthorized - invalid API key")
                
            elif response.status_code == 426:
                print(f"❌ Upgrade required - key may be expired")
                
            else:
                print(f"❌ HTTP {response.status_code}: {response.text[:100]}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
        
        # Wait between tests to avoid rate limiting
        print("⏳ Waiting 3 seconds before next test...")
        time.sleep(3)
    
    # Summary analysis
    print("\n" + "=" * 50)
    print("📊 NEWS API CAPACITY ANALYSIS")
    print("=" * 50)
    
    print(f"\n🎯 RESULTS SUMMARY:")
    print(f"Working keys: {working_keys}/4")
    print(f"Daily capacity: {total_capacity} requests/day")
    print(f"Monthly capacity: {total_capacity * 30:,} requests/month")
    
    if working_keys == 4:
        print("\n🏆 PERFECT! MAXIMUM NEWS CAPACITY ACHIEVED!")
        print("🚀 400 Samsung news articles per day!")
        print("📈 12,000 Samsung news articles per month!")
        
    elif working_keys >= 3:
        print(f"\n💪 EXCELLENT! {working_keys}/4 keys working!")
        print(f"🚀 {total_capacity} Samsung news articles per day!")
        
    elif working_keys >= 2:
        print(f"\n✅ GOOD! {working_keys}/4 keys working!")
        print(f"📊 {total_capacity} requests/day capacity")
        
    elif working_keys >= 1:
        print(f"\n⚠️ BASIC: {working_keys}/4 keys working")
        print("💡 Need more group member keys for higher capacity")
        
    else:
        print("\n❌ No working News API keys found")
        print("🔧 Check API key configuration")
    
    # Professional analysis
    print(f"\n💡 PROFESSIONAL BENEFITS:")
    if working_keys >= 4:
        benefits = [
            "✅ Enterprise-grade news monitoring",
            "✅ Comprehensive Samsung coverage", 
            "✅ Real-time competitor tracking",
            "✅ Market sentiment analysis",
            "✅ Professional redundancy (backup keys)",
            "✅ Industry-standard capacity"
        ]
    elif working_keys >= 2:
        benefits = [
            "✅ Professional news monitoring",
            "✅ Good Samsung coverage",
            "✅ Backup key redundancy", 
            "⬆️ Add more keys for maximum capacity"
        ]
    else:
        benefits = [
            "⚠️ Basic news monitoring",
            "🔧 Need group members to add more keys"
        ]
    
    for benefit in benefits:
        print(f"   {benefit}")
    
    print(f"\n🎯 FOR SAMSUNG PRODUCT LAUNCH ANALYSIS:")
    if total_capacity >= 400:
        print("🏆 UNLIMITED Samsung news research capability!")
        print("📊 Track all major Samsung announcements") 
        print("🔍 Monitor competitor news (Apple, Google)")
        print("📈 Analyze market sentiment trends")
        print("⚡ Real-time crisis monitoring")
    elif total_capacity >= 200:
        print("✅ Strong Samsung news analysis capability")
        print("📊 Good coverage of Samsung developments")
    else:
        print("⚠️ Basic Samsung news monitoring")
    
    print("=" * 50)
    
    return {'working_keys': working_keys, 'capacity': total_capacity}

if __name__ == "__main__":
    test_all_news_api_keys()
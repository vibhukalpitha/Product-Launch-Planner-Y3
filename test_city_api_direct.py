"""
Direct test for city API calls
Tests if Google Trends, YouTube, and News APIs work for regional data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("\n" + "="*80)
print("TESTING REAL API CALLS FOR CITY DATA")
print("="*80)

# Test 1: Google Trends Regional
print("\n[TEST 1] Google Trends Regional API")
print("-" * 80)

try:
    from pytrends.request import TrendReq
    import time
    import random
    
    time.sleep(random.uniform(2, 4))
    
    print("Initializing pytrends...")
    pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25), retries=2, backoff_factor=0.1)
    
    # Test with Korea (Seoul)
    print("Testing: Galaxy S23 Ultra in Korea (KR)...")
    pytrends.build_payload(
        ["Galaxy S23 Ultra"], 
        cat=0, 
        timeframe='today 3-m', 
        geo='KR',
        gprop=''
    )
    
    data = pytrends.interest_over_time()
    
    if not data.empty and 'Galaxy S23 Ultra' in data.columns:
        avg_interest = data['Galaxy S23 Ultra'].mean()
        print(f"✅ SUCCESS! Regional interest for KR: {avg_interest:.1f}/100")
        print(f"   This is REAL data (not the fallback 85.0)")
    else:
        print("❌ FAILED: No data returned from Google Trends")
        print("   System will use fallback: 85.0")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
    print("   System will use fallback values")

# Test 2: Check if similar products exist
print("\n[TEST 2] Similar Products from APIs")
print("-" * 80)

try:
    from agents.market_trend_analyzer import MarketTrendAnalyzer
    from agents.communication_coordinator import coordinator
    
    analyzer = MarketTrendAnalyzer(coordinator)
    
    print("Discovering similar Samsung products...")
    similar = analyzer.discover_samsung_similar_products(
        "Galaxy S25 Ultra",
        "Smartphones", 
        1200.0
    )
    
    products = similar.get('found_products', [])
    api_products = [p for p in products if p.get('source') in ['News API', 'YouTube API', 'SerpAPI (Google Shopping)']]
    
    print(f"✅ Found {len(products)} total products")
    print(f"✅ Found {len(api_products)} products from APIs")
    
    if len(api_products) > 0:
        print("\nAPI-sourced products:")
        for p in api_products[:3]:
            print(f"  - {p['name']} (Source: {p['source']})")
    else:
        print("❌ No API-sourced products found")
        print("   City analysis will use fallback data")
        
except Exception as e:
    print(f"❌ ERROR: {e}")

# Test 3: YouTube Regional (if API key exists)
print("\n[TEST 3] YouTube Regional API")
print("-" * 80)

try:
    from utils.real_data_connector import real_data_connector
    from utils.api_manager import is_api_enabled
    
    if is_api_enabled('youtube'):
        print("Testing YouTube regional search...")
        youtube_data = real_data_connector.get_youtube_metrics("Galaxy S23 Ultra JP")
        
        if youtube_data and 'videos' in youtube_data:
            video_count = len(youtube_data['videos'])
            print(f"✅ SUCCESS! Found {video_count} regional videos")
            
            if video_count >= 8:
                factor = 1.3
            elif video_count >= 5:
                factor = 1.15
            elif video_count >= 2:
                factor = 1.0
            else:
                factor = 0.85
            
            print(f"   YouTube factor would be: {factor}x")
        else:
            print("❌ FAILED: No videos returned")
            print("   Will use fallback: 1.0x")
    else:
        print("⚠️ YouTube API not enabled")
        print("   Will use fallback: 1.0x")
        
except Exception as e:
    print(f"❌ ERROR: {e}")

# Test 4: News API Regional (if API key exists)
print("\n[TEST 4] News API Regional")
print("-" * 80)

try:
    from utils.real_data_connector import real_data_connector
    from utils.api_manager import is_api_enabled
    
    if is_api_enabled('news_api'):
        print("Testing News API regional search...")
        news_data = real_data_connector.get_news_data(
            query="Galaxy S23 Ultra Tokyo",
            language='en',
            page_size=10
        )
        
        if news_data and 'articles' in news_data:
            article_count = len(news_data['articles'])
            print(f"✅ SUCCESS! Found {article_count} regional articles")
            
            if article_count >= 6:
                factor = 1.2
            elif article_count >= 3:
                factor = 1.1
            elif article_count >= 1:
                factor = 1.0
            else:
                factor = 0.9
            
            print(f"   News factor would be: {factor}x")
        else:
            print("❌ FAILED: No articles returned")
            print("   Will use fallback: 1.0x")
    else:
        print("⚠️ News API not enabled")
        print("   Will use fallback: 1.0x")
        
except Exception as e:
    print(f"❌ ERROR: {e}")

# Summary
print("\n" + "="*80)
print("SUMMARY")
print("="*80)

print("\n📊 What determines if you get REAL or FALLBACK data:")
print("  1. Google Trends must return data (not rate-limited)")
print("  2. Similar products must be found from APIs")
print("  3. YouTube/News APIs enhance the data (optional)")

print("\n🔍 To see if your current run uses real data:")
print("  Look at the console when you run the app")
print("  Search for these messages:")
print("    ✅ '[OK] Regional interest for KR: XX.X/100' (real)")
print("    ❌ '[WARNING] Could not fetch...' (fallback)")

print("\n💡 If seeing fallback values:")
print("  - Google Trends may be rate-limiting (429 error)")
print("  - Try waiting 5-10 minutes between runs")
print("  - Or the code may be using cached data")

print("\n" + "="*80)
print("TEST COMPLETED")
print("="*80 + "\n")


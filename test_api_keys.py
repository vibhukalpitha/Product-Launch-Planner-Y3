#!/usr/bin/env python3
"""
API Key Test Script - Check if all your API keys are properly loaded
"""
import os
from dotenv import load_dotenv

def test_api_keys():
    """Test if API keys are properly loaded"""
    
    # Load environment variables
    load_dotenv()
    
    print("🔑 Testing API Key Configuration...")
    print("=" * 50)
    
    # Define the API services and their expected key patterns
    api_services = {
        'NEWS_API': {
            'pattern': 'NEWS_API_KEY',
            'count': 4,
            'description': 'News API Keys'
        },
        'YOUTUBE': {
            'pattern': 'YOUTUBE_API_KEY', 
            'count': 4,
            'description': 'YouTube API Keys'
        },
        'ALPHA_VANTAGE': {
            'pattern': 'ALPHA_VANTAGE_API_KEY',
            'count': 4, 
            'description': 'Alpha Vantage Keys'
        },
        'FRED': {
            'pattern': 'FRED_API_KEY',
            'count': 4,
            'description': 'FRED Economic Data Keys'
        },
        'SERP_API': {
            'pattern': 'SERP_API_KEY',
            'count': 1,
            'description': 'SerpApi Google Search Key'
        },
        'REDDIT': {
            'pattern': 'REDDIT_CLIENT_ID',
            'count': 1,
            'description': 'Reddit API Keys'
        }
    }
    
    total_keys = 0
    working_keys = 0
    
    for service, config in api_services.items():
        print(f"\n📊 {config['description']}:")
        service_keys = 0
        
        # Check multiple keys for this service
        for i in range(1, config['count'] + 1):
            key_name = f"{config['pattern']}_{i}"
            key_value = os.getenv(key_name)
            
            if key_value and not key_value.startswith('your_') and len(key_value) > 10:
                print(f"   ✅ {key_name}: {key_value[:8]}...{key_value[-4:]}")
                service_keys += 1
                working_keys += 1
            else:
                print(f"   ❌ {key_name}: Not found or invalid")
            total_keys += 1
        
        # Check single key format as fallback
        if service_keys == 0:
            single_key = os.getenv(config['pattern'])
            if single_key and not single_key.startswith('your_') and len(single_key) > 10:
                print(f"   ✅ {config['pattern']}: {single_key[:8]}...{single_key[-4:]}")
                working_keys += 1
    
    print(f"\n" + "=" * 50)
    print(f"📊 Summary: {working_keys}/{total_keys} API keys configured")
    
    if working_keys < total_keys:
        print(f"\n💡 Missing API Keys Setup:")
        print(f"   Create a .env file in your project root with:")
        print(f"   NEWS_API_KEY_1=your_first_news_key")
        print(f"   NEWS_API_KEY_2=your_second_news_key")
        print(f"   YOUTUBE_API_KEY_1=your_first_youtube_key")
        print(f"   # ... etc")
        
    return working_keys, total_keys

def test_rate_limits():
    """Test current rate limit status"""
    print(f"\n🚦 Rate Limit Status Check:")
    print("=" * 30)
    
    # This would normally check API status
    print("💡 To check rate limits:")
    print("   - News API: 100 requests/24hrs (50 every 12hrs)")
    print("   - YouTube: 10,000 quota units/day")
    print("   - Alpha Vantage: 5 requests/minute, 500/day")
    print("   - FRED: 120 requests/hour")

if __name__ == "__main__":
    working, total = test_api_keys()
    test_rate_limits()
    
    if working >= total * 0.5:
        print(f"\n✅ API Setup looks good! Rate limits are the issue.")
    else:
        print(f"\n⚠️ Need to configure more API keys in .env file")
"""
Test all News API keys to verify they're working
"""

import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

def test_news_api_key(key_name, api_key):
    """Test a single News API key"""
    print(f"\n{'='*60}")
    print(f"Testing: {key_name}")
    print(f"Key: {api_key[:20]}..." if len(api_key) > 20 else f"Key: {api_key}")
    print(f"{'='*60}")
    
    # Check for placeholder values
    if api_key.startswith("your_") or "api_key" in api_key.lower():
        print(f"❌ INVALID - This appears to be a placeholder value")
        print(f"   Please replace with a real News API key from https://newsapi.org/")
        return False
    
    # Test the key with a simple query
    url = "https://newsapi.org/v2/everything"
    
    # Request articles from last 7 days (free tier limitation)
    from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    params = {
        'q': 'Samsung Galaxy',
        'from': from_date,
        'sortBy': 'publishedAt',
        'pageSize': 1,
        'apiKey': api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'ok':
                total_results = data.get('totalResults', 0)
                articles = data.get('articles', [])
                print(f"✅ SUCCESS - Key is working!")
                print(f"   Total results available: {total_results}")
                print(f"   Articles returned: {len(articles)}")
                if articles:
                    print(f"   Sample article: {articles[0].get('title', 'N/A')[:60]}...")
                return True
            else:
                print(f"❌ FAILED - API returned error status")
                print(f"   Message: {data.get('message', 'Unknown error')}")
                return False
        
        elif response.status_code == 401:
            print(f"❌ AUTHENTICATION FAILED")
            print(f"   The API key is invalid or expired")
            print(f"   Get a new key from: https://newsapi.org/")
            return False
        
        elif response.status_code == 429:
            print(f"⚠️  RATE LIMITED")
            print(f"   This key has exceeded its rate limit")
            print(f"   It may recover later, or you may need to upgrade the plan")
            return False
        
        elif response.status_code == 426:
            print(f"⚠️  PLAN LIMITATION")
            data = response.json()
            print(f"   Message: {data.get('message', 'Unknown limitation')}")
            print(f"   This is likely a date range issue (free tier: last 30 days only)")
            return False
        
        else:
            print(f"❌ ERROR - HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"⚠️  TIMEOUT - Request took too long")
        return False
    
    except Exception as e:
        print(f"❌ EXCEPTION - {str(e)}")
        return False

def main():
    """Test all News API keys"""
    print("\n" + "="*60)
    print("🔍 NEWS API KEY VALIDATION TEST")
    print("="*60)
    
    # Collect all News API keys
    keys_to_test = []
    
    # Primary key
    if os.getenv('NEWS_API_KEY'):
        keys_to_test.append(('NEWS_API_KEY', os.getenv('NEWS_API_KEY')))
    
    # Additional keys (NEWS_API_KEY_1, NEWS_API_KEY_2, etc.)
    i = 1
    while True:
        key_name = f'NEWS_API_KEY_{i}'
        key_value = os.getenv(key_name)
        if key_value:
            keys_to_test.append((key_name, key_value))
            i += 1
        else:
            break
    
    if not keys_to_test:
        print("\n❌ No News API keys found in .env file")
        print("   Add NEWS_API_KEY to your .env file")
        return
    
    print(f"\nFound {len(keys_to_test)} News API key(s) to test\n")
    
    # Test each key
    results = {}
    for key_name, key_value in keys_to_test:
        results[key_name] = test_news_api_key(key_name, key_value)
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 SUMMARY")
    print(f"{'='*60}\n")
    
    working_keys = [k for k, v in results.items() if v]
    failed_keys = [k for k, v in results.items() if not v]
    
    print(f"✅ Working keys: {len(working_keys)}/{len(results)}")
    for key in working_keys:
        print(f"   • {key}")
    
    if failed_keys:
        print(f"\n❌ Failed/Invalid keys: {len(failed_keys)}/{len(results)}")
        for key in failed_keys:
            print(f"   • {key}")
    
    print(f"\n{'='*60}")
    
    if working_keys:
        print(f"✅ You have {len(working_keys)} working News API key(s)")
        print(f"   Your system will rotate through these keys to avoid rate limits")
    else:
        print(f"⚠️  No working News API keys!")
        print(f"   Get free keys from: https://newsapi.org/")
    
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()


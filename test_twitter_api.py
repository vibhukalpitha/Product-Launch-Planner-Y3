import os
import requests
from dotenv import load_dotenv

load_dotenv()

bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

if not bearer_token:
    print("❌ TWITTER_BEARER_TOKEN not found in .env")
    exit(1)

# Test Twitter API v2
search_url = "https://api.twitter.com/2/tweets/search/recent"
headers = {
    "Authorization": f"Bearer {bearer_token}",
    "User-Agent": "Samsung Launch Planner/1.0"
}

params = {
    'query': 'Samsung Galaxy -is:retweet',
    'max_results': 10,
    'tweet.fields': 'created_at,public_metrics'
}

print("🐦 Testing Twitter API v2...")
print(f"🔍 Query: {params['query']}")
print(f"📊 Max results: {params['max_results']}\n")

try:
    response = requests.get(search_url, headers=headers, params=params, timeout=15)
    
    print(f"📡 Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        tweets = data.get('data', [])
        meta = data.get('meta', {})
        
        print(f"✅ SUCCESS!")
        print(f"📝 Tweets found: {len(tweets)}")
        print(f"📊 Result count: {meta.get('result_count', 0)}")
        
        if tweets:
            print("\n🐦 Sample tweets:")
            for i, tweet in enumerate(tweets[:3], 1):
                text = tweet.get('text', '')[:80]
                metrics = tweet.get('public_metrics', {})
                print(f"  {i}. {text}...")
                print(f"     ❤️ {metrics.get('like_count', 0)} likes, 🔁 {metrics.get('retweet_count', 0)} retweets")
        else:
            print("\n⚠️ No tweets found for this query")
            print("This might mean:")
            print("  - No recent tweets match 'Samsung Galaxy'")
            print("  - Free tier has search limitations")
            
    elif response.status_code == 429:
        print(f"❌ RATE LIMITED")
        print(f"Rate limit header: {response.headers.get('x-rate-limit-remaining', 'N/A')}")
        print(f"Reset time: {response.headers.get('x-rate-limit-reset', 'N/A')}")
        
    elif response.status_code == 401:
        print(f"❌ AUTHENTICATION FAILED")
        print(f"Your bearer token may be invalid or expired")
        
    else:
        print(f"❌ ERROR: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
except Exception as e:
    print(f"❌ EXCEPTION: {e}")

print("\n" + "="*60)
print("💡 Twitter API Free Tier Limits:")
print("   - 500,000 tweets/month")
print("   - 300 requests per 15 minutes")
print("   - 7 days historical search only")
print("="*60)



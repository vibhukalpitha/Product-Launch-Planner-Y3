#!/usr/bin/env python3
"""
Quick test script for Bing Web Search API
Run this after adding your BING_SEARCH_KEY to .env file
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_bing_search():
    """Test Bing Web Search API with a simple search"""
    api_key = os.getenv('BING_SEARCH_KEY')
    
    if not api_key or api_key == 'your_bing_search_key_here':
        print("❌ No Bing Search API key found!")
        print("💡 Add your real API key to .env file:")
        print("   BING_SEARCH_KEY=your_actual_key_from_azure")
        return False
    
    # Test search
    url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'Content-Type': 'application/json'
    }
    params = {
        'q': 'Samsung Galaxy S25 launch history',
        'count': 3,
        'mkt': 'en-US'
    }
    
    try:
        print("🧪 Testing Bing Web Search API...")
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('webPages', {}).get('value', [])
            
            print(f"✅ Bing Search API works! Found {len(results)} results")
            for i, result in enumerate(results[:2], 1):
                print(f"   {i}. {result.get('name', 'No title')}")
                print(f"      URL: {result.get('url', 'No URL')}")
            
            # Show usage info
            total_estimated = data.get('webPages', {}).get('totalEstimatedMatches', 0)
            print(f"📊 Total estimated matches: {total_estimated:,}")
            return True
            
        elif response.status_code == 401:
            print("❌ Unauthorized: Check your API key")
            print("💡 Make sure you copied the correct key from Azure Portal")
            return False
        elif response.status_code == 403:
            print("❌ Forbidden: API key might be invalid or quota exceeded")
            return False
        else:
            print(f"❌ Bing API error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Bing API: {e}")
        return False

def check_quota():
    """Check remaining quota (if possible)"""
    print("\n💡 Quota Information:")
    print("   • Free tier: 1,000 queries per month")
    print("   • Resets monthly")
    print("   • Check usage in Azure Portal → Your Resource → Metrics")

if __name__ == "__main__":
    success = test_bing_search()
    if success:
        print("\n🎉 Bing Web Search API is ready for Samsung product discovery!")
        check_quota()
    else:
        print("\n🔧 Fix the API key and try again")
        print("📖 Setup guide: https://docs.microsoft.com/en-us/bing/search-apis/bing-web-search/create-bing-search-service-resource")
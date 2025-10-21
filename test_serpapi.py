#!/usr/bin/env python3
"""
Quick test script for SerpApi
Run this after adding your SERP_API_KEY to .env file
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_serpapi():
    """Test SerpApi with a simple search"""
    api_key = os.getenv('SERP_API_KEY')
    
    if not api_key or api_key == 'your_serp_api_key_here':
        print("❌ No SerpApi key found!")
        print("💡 Add your real API key to .env file:")
        print("   SERP_API_KEY=your_actual_key_from_serpapi")
        return False
    
    # Test search
    url = "https://serpapi.com/search"
    params = {
        'q': 'Samsung Galaxy S25',
        'api_key': api_key,
        'engine': 'google',
        'num': 3
    }
    
    try:
        print("🧪 Testing SerpApi...")
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('organic_results', [])
            
            print(f"✅ SerpApi works! Found {len(results)} results")
            for i, result in enumerate(results[:2], 1):
                print(f"   {i}. {result.get('title', 'No title')}")
            
            # Show usage info
            search_info = data.get('search_information', {})
            print(f"📊 Search took: {search_info.get('query_displayed_time', 'Unknown')} seconds")
            return True
            
        else:
            print(f"❌ SerpApi error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing SerpApi: {e}")
        return False

if __name__ == "__main__":
    success = test_serpapi()
    if success:
        print("\n🎉 SerpApi is ready for Samsung product discovery!")
    else:
        print("\n🔧 Fix the API key and try again")
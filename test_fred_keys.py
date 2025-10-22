#!/usr/bin/env python3
"""
Test All 3 FRED API Keys
========================
"""

import requests
import os
from dotenv import load_dotenv

def test_all_fred_keys():
    """Test all available FRED API keys"""
    
    load_dotenv()
    
    print("🏦 TESTING ALL FRED API KEYS")
    print("=" * 40)
    
    fred_keys = [
        ("KEY_1", os.getenv('FRED_API_KEY_1')),
        ("KEY_2", os.getenv('FRED_API_KEY_2')), 
        ("KEY_3", os.getenv('FRED_API_KEY_3')),
        ("KEY_4", os.getenv('FRED_API_KEY_4'))
    ]
    
    working_keys = 0
    
    for key_name, key_value in fred_keys:
        print(f"\n📊 Testing FRED {key_name}")
        print("-" * 25)
        
        if not key_value or "your_group_member" in key_value:
            print(f"⚠️ {key_name}: Not configured (placeholder value)")
            continue
            
        print(f"Key: {key_value[:20]}...")
        
        try:
            # Test with GDP data
            url = "https://api.stlouisfed.org/fred/series/observations"
            params = {
                'series_id': 'GDP',
                'api_key': key_value,
                'file_type': 'json',
                'limit': 1,
                'sort_order': 'desc'
            }
            
            response = requests.get(url, params=params, timeout=10)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if 'observations' in data and data['observations']:
                    latest = data['observations'][0]
                    date = latest.get('date', 'N/A')
                    value = latest.get('value', 'N/A')
                    print(f"✅ SUCCESS: GDP ({date}): ${value} billion")
                    working_keys += 1
                else:
                    print(f"⚠️ No data in response")
            elif response.status_code == 400:
                print(f"❌ Bad request - invalid API key")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"Response: {response.text[:100]}...")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
    
    print("\n" + "=" * 40)
    print(f"🎯 FRED API SUMMARY:")
    print(f"✅ Working keys: {working_keys}/4")
    print(f"📈 Rate limit capacity: {working_keys}x higher")
    print(f"🚀 Backup availability: {working_keys-1} backup keys")
    
    if working_keys >= 3:
        print("🏆 EXCELLENT: 3+ FRED keys active!")
    elif working_keys >= 2:
        print("👍 GOOD: 2+ FRED keys active!")
    elif working_keys >= 1:
        print("✅ BASIC: 1 FRED key active")
    else:
        print("⚠️ No working FRED keys found")
    
    print("=" * 40)

if __name__ == "__main__":
    test_all_fred_keys()
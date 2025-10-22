#!/usr/bin/env python3
"""
Test New Market Data APIs - Alpha Vantage & FRED
================================================
"""

import requests
import os
from dotenv import load_dotenv
import json

def test_market_apis():
    """Test the newly added market data APIs"""
    
    load_dotenv()
    
    print("🔍 TESTING NEW MARKET DATA APIs")
    print("=" * 50)
    
    # Test Alpha Vantage API
    print("\n📈 ALPHA VANTAGE API TEST")
    print("-" * 30)
    alpha_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    
    if alpha_key:
        print(f"✅ Key loaded: {alpha_key[:8]}...")
        
        try:
            # Test with Samsung stock symbol (if available) or Microsoft as backup
            url = "https://www.alphavantage.co/query"
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': 'MSFT',  # Using MSFT as test (Samsung trades as 005930.KS)
                'apikey': alpha_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if 'Global Quote' in data:
                    quote = data['Global Quote']
                    symbol = quote.get('01. symbol', 'N/A')
                    price = quote.get('05. price', 'N/A')
                    print(f"✅ SUCCESS: Got stock data for {symbol}")
                    print(f"✅ Current price: ${price}")
                    print("✅ Alpha Vantage API is WORKING!")
                elif 'Error Message' in data:
                    print(f"⚠️ API Error: {data['Error Message']}")
                elif 'Note' in data:
                    print(f"⚠️ Rate limit: {data['Note']}")
                    print("✅ API key is valid but rate limited")
                else:
                    print(f"⚠️ Unexpected response: {data}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"Response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
    else:
        print("❌ No Alpha Vantage API key found")
    
    # Test FRED API
    print("\n🏦 FRED API TEST")
    print("-" * 20)
    fred_key = os.getenv('FRED_API_KEY')
    
    if fred_key:
        print(f"✅ Key loaded: {fred_key[:8]}...")
        
        try:
            # Test with GDP data
            url = "https://api.stlouisfed.org/fred/series/observations"
            params = {
                'series_id': 'GDP',
                'api_key': fred_key,
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
                    print(f"✅ SUCCESS: Got GDP data")
                    print(f"✅ Latest GDP ({date}): ${value} billion")
                    print("✅ FRED API is WORKING!")
                else:
                    print(f"⚠️ No data in response: {data}")
            elif response.status_code == 400:
                print(f"❌ Bad request - check API key: {response.text}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"Response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
    else:
        print("❌ No FRED API key found")
    
    print("\n" + "=" * 50)
    print("🎯 MARKET DATA APIS STATUS:")
    print("📈 Alpha Vantage: Stock market data")
    print("🏦 FRED: Economic indicators")
    print("🚀 Ready for Samsung market analysis!")
    print("=" * 50)

if __name__ == "__main__":
    test_market_apis()
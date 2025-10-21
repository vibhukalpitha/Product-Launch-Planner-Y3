#!/usr/bin/env python3
"""
COMPREHENSIVE MULTI-KEY TEST - Enterprise Level API Setup
=========================================================
Testing all Alpha Vantage, FRED, and YouTube API keys
"""

import requests
import os
from dotenv import load_dotenv
import json
from concurrent.futures import ThreadPoolExecutor
import time

class EnterpriseAPITester:
    """Test enterprise-level multi-key API setup"""
    
    def __init__(self):
        load_dotenv()
        self.results = {
            'alpha_vantage': {'working': 0, 'total': 0, 'capacity': 0},
            'fred': {'working': 0, 'total': 0, 'capacity': 0},
            'youtube': {'working': 0, 'total': 0, 'capacity': 0}
        }
    
    def test_alpha_vantage_key(self, key_name, key_value):
        """Test a single Alpha Vantage key"""
        if not key_value or "your_group_member" in key_value:
            return f"⚠️ {key_name}: Not configured"
            
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': 'MSFT',
                'apikey': key_value
            }
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if 'Global Quote' in data:
                    price = data['Global Quote'].get('05. price', 'N/A')
                    return f"✅ {key_name}: WORKING - MSFT: ${price}"
                elif 'Note' in data:
                    return f"⚠️ {key_name}: Rate limited (key is valid)"
                else:
                    return f"⚠️ {key_name}: Unexpected response"
            else:
                return f"❌ {key_name}: HTTP {response.status_code}"
                
        except Exception as e:
            return f"❌ {key_name}: Error - {str(e)[:50]}"
    
    def test_fred_key(self, key_name, key_value):
        """Test a single FRED key"""
        if not key_value or "your_group_member" in key_value:
            return f"⚠️ {key_name}: Not configured"
            
        try:
            url = "https://api.stlouisfed.org/fred/series/observations"
            params = {
                'series_id': 'GDP',
                'api_key': key_value,
                'file_type': 'json',
                'limit': 1,
                'sort_order': 'desc'
            }
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if 'observations' in data and data['observations']:
                    latest = data['observations'][0]
                    value = latest.get('value', 'N/A')
                    return f"✅ {key_name}: WORKING - GDP: ${value}B"
                else:
                    return f"⚠️ {key_name}: No data"
            else:
                return f"❌ {key_name}: HTTP {response.status_code}"
                
        except Exception as e:
            return f"❌ {key_name}: Error - {str(e)[:50]}"
    
    def test_youtube_key(self, key_name, key_value):
        """Test a single YouTube key"""
        if not key_value or "your_group_member" in key_value:
            return f"⚠️ {key_name}: Not configured"
            
        try:
            url = 'https://www.googleapis.com/youtube/v3/search'
            params = {
                'part': 'snippet',
                'q': 'Samsung Galaxy',
                'maxResults': 1,
                'key': key_value
            }
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if 'items' in data and data['items']:
                    title = data['items'][0]['snippet']['title'][:40]
                    return f"✅ {key_name}: WORKING - Found: {title}..."
                else:
                    return f"⚠️ {key_name}: No videos found"
            elif response.status_code == 403:
                return f"⚠️ {key_name}: Quota exceeded (key is valid)"
            else:
                return f"❌ {key_name}: HTTP {response.status_code}"
                
        except Exception as e:
            return f"❌ {key_name}: Error - {str(e)[:50]}"
    
    def run_comprehensive_test(self):
        """Run comprehensive test of all API keys"""
        
        print("🚀 ENTERPRISE-LEVEL API CAPACITY TEST")
        print("=" * 55)
        
        # Test Alpha Vantage keys
        print("\n📈 ALPHA VANTAGE - STOCK DATA (4 KEYS)")
        print("-" * 45)
        
        for i in range(1, 5):
            key_value = os.getenv(f'ALPHA_VANTAGE_API_KEY_{i}')
            result = self.test_alpha_vantage_key(f"KEY_{i}", key_value)
            print(f"  {result}")
            
            if "✅" in result or "⚠️" in result and "valid" in result:
                self.results['alpha_vantage']['working'] += 1
            self.results['alpha_vantage']['total'] += 1
        
        # Test FRED keys
        print(f"\n🏦 FRED - ECONOMIC DATA (4 KEYS)")
        print("-" * 35)
        
        for i in range(1, 5):
            key_value = os.getenv(f'FRED_API_KEY_{i}')
            result = self.test_fred_key(f"KEY_{i}", key_value)
            print(f"  {result}")
            
            if "✅" in result:
                self.results['fred']['working'] += 1
            self.results['fred']['total'] += 1
        
        # Test YouTube keys
        print(f"\n📺 YOUTUBE - VIDEO DATA (4 KEYS)")
        print("-" * 35)
        
        for i in range(1, 5):
            key_value = os.getenv(f'YOUTUBE_API_KEY_{i}')
            result = self.test_youtube_key(f"KEY_{i}", key_value)
            print(f"  {result}")
            
            if "✅" in result or "⚠️" in result and "valid" in result:
                self.results['youtube']['working'] += 1
            self.results['youtube']['total'] += 1
        
        # Calculate capacities
        self.results['alpha_vantage']['capacity'] = self.results['alpha_vantage']['working'] * 25
        self.results['fred']['capacity'] = self.results['fred']['working'] * 120 * 60 * 24  # Practically unlimited
        self.results['youtube']['capacity'] = self.results['youtube']['working'] * 10000
        
        # Show summary
        self.show_enterprise_summary()
    
    def show_enterprise_summary(self):
        """Show enterprise-level summary"""
        
        print("\n" + "=" * 55)
        print("🏆 ENTERPRISE API CAPACITY SUMMARY")
        print("=" * 55)
        
        # Individual summaries
        alpha_working = self.results['alpha_vantage']['working']
        fred_working = self.results['fred']['working']
        youtube_working = self.results['youtube']['working']
        
        print(f"\n📈 Alpha Vantage: {alpha_working}/4 keys = {self.results['alpha_vantage']['capacity']:,} requests/day")
        print(f"🏦 FRED Economic: {fred_working}/4 keys = Unlimited requests/day")
        print(f"📺 YouTube Data:  {youtube_working}/4 keys = {self.results['youtube']['capacity']:,} requests/day")
        
        # Overall status
        total_working = alpha_working + fred_working + youtube_working
        total_possible = 12
        
        print(f"\n🎯 OVERALL STATUS: {total_working}/{total_possible} keys active")
        
        if total_working >= 10:
            print("🏆 ENTERPRISE LEVEL: Outstanding API setup!")
            print("🚀 Ready for professional Samsung market analysis!")
        elif total_working >= 8:
            print("💪 PROFESSIONAL LEVEL: Excellent capacity!")
        elif total_working >= 6:
            print("✅ BUSINESS LEVEL: Good capacity!")
        else:
            print("⚠️ BASIC LEVEL: Consider adding more keys")
        
        # Show competitive advantage
        print(f"\n💡 VS SINGLE KEY SETUP:")
        print(f"   • Alpha Vantage: {alpha_working}x more capacity")
        print(f"   • FRED: {fred_working}x more reliability") 
        print(f"   • YouTube: {youtube_working}x more capacity")
        
        print("\n🎉 Your Samsung Product Launch Planner has")
        print("   ENTERPRISE-GRADE API infrastructure!")
        print("=" * 55)

if __name__ == "__main__":
    tester = EnterpriseAPITester()
    tester.run_comprehensive_test()
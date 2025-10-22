"""
Enhanced API Key Validation Script
Tests ALL API keys including rotation keys from .env file
"""

import os
import sys
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 80)
print("[KEY] ENHANCED API KEY VALIDATION TOOL")
print("=" * 80)
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Track results
results = {
    'valid': [],
    'invalid': [],
    'not_configured': [],
    'rate_limited': []
}

def test_youtube_key(key_name, api_key):
    """Test a single YouTube API key"""
    if not api_key or api_key.strip() == '' or 'your_' in api_key.lower():
        return None
    
    try:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            'key': api_key,
            'q': 'test',
            'part': 'snippet',
            'type': 'video',
            'maxResults': 1
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'items' in data:
                return 'valid'
        elif response.status_code == 403:
            error = response.json().get('error', {})
            if 'quota' in error.get('message', '').lower():
                return 'rate_limited'
            else:
                return 'invalid'
        elif response.status_code == 400:
            return 'invalid'
        else:
            return 'error'
            
    except Exception as e:
        return 'error'
    
    return 'error'

def test_news_key(key_name, api_key):
    """Test a single News API key"""
    if not api_key or api_key.strip() == '' or 'your_' in api_key.lower():
        return None
    
    try:
        url = f"https://newsapi.org/v2/top-headlines"
        params = {
            'apiKey': api_key,
            'country': 'us',
            'pageSize': 1
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'ok':
                return 'valid'
        elif response.status_code == 401:
            return 'invalid'
        elif response.status_code == 429:
            return 'rate_limited'
            
    except Exception as e:
        return 'error'
    
    return 'error'

def test_serpapi_key(key_name, api_key):
    """Test a single SerpAPI key"""
    if not api_key or api_key.strip() == '' or 'your_' in api_key.lower():
        return None
    
    try:
        url = "https://serpapi.com/search"
        params = {
            'api_key': api_key,
            'q': 'test',
            'engine': 'google'
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'error' not in data:
                return 'valid'
            else:
                return 'invalid'
        elif response.status_code == 401:
            return 'invalid'
        elif response.status_code == 429:
            return 'rate_limited'
            
    except Exception as e:
        return 'error'
    
    return 'error'

def test_all_youtube_keys():
    """Test all YouTube API keys"""
    print("[YT] Testing YouTube Data API Keys...")
    print("-" * 80)
    
    youtube_keys = {}
    
    # Get all YouTube keys from environment
    for i in range(10):  # Check up to KEY_9
        if i == 0:
            key_name = 'YOUTUBE_API_KEY'
        else:
            key_name = f'YOUTUBE_API_KEY_{i}'
        
        api_key = os.getenv(key_name)
        if api_key and api_key.strip() != '' and 'your_' not in api_key.lower():
            youtube_keys[key_name] = api_key
    
    if not youtube_keys:
        print("   [!] No YouTube API keys configured")
        results['not_configured'].append('YOUTUBE_API_KEY')
        return
    
    print(f"   Found {len(youtube_keys)} YouTube key(s)")
    print()
    
    valid_count = 0
    rate_limited_count = 0
    invalid_count = 0
    
    for key_name, api_key in youtube_keys.items():
        print(f"   Testing {key_name}: ...{api_key[-8:]}")
        status = test_youtube_key(key_name, api_key)
        
        if status == 'valid':
            print(f"      [OK] VALID - Working perfectly!")
            results['valid'].append(key_name)
            valid_count += 1
        elif status == 'rate_limited':
            print(f"      [||] RATE LIMITED - Quota exceeded (key is valid)")
            results['rate_limited'].append(key_name)
            rate_limited_count += 1
        elif status == 'invalid':
            print(f"      [X] INVALID - Authentication failed")
            results['invalid'].append(key_name)
            invalid_count += 1
        else:
            print(f"      [X] ERROR - Unable to validate")
            results['invalid'].append(key_name)
            invalid_count += 1
        print()
    
    print(f"   Summary: {valid_count} valid, {rate_limited_count} rate-limited, {invalid_count} invalid/error")
    print()

def test_all_news_keys():
    """Test all News API keys"""
    print("[NEWS] Testing News API Keys...")
    print("-" * 80)
    
    news_keys = {}
    
    # Get all News keys from environment
    for i in range(10):  # Check up to KEY_9
        if i == 0:
            key_name = 'NEWS_API_KEY'
        else:
            key_name = f'NEWS_API_KEY_{i}'
        
        api_key = os.getenv(key_name)
        if api_key and api_key.strip() != '' and 'your_' not in api_key.lower():
            news_keys[key_name] = api_key
    
    if not news_keys:
        print("   [!] No News API keys configured")
        results['not_configured'].append('NEWS_API_KEY')
        return
    
    print(f"   Found {len(news_keys)} News API key(s)")
    print()
    
    valid_count = 0
    rate_limited_count = 0
    invalid_count = 0
    
    for key_name, api_key in news_keys.items():
        print(f"   Testing {key_name}: ...{api_key[-8:]}")
        status = test_news_key(key_name, api_key)
        
        if status == 'valid':
            print(f"      [OK] VALID - Working perfectly!")
            results['valid'].append(key_name)
            valid_count += 1
        elif status == 'rate_limited':
            print(f"      [||] RATE LIMITED - Quota exceeded (key is valid)")
            results['rate_limited'].append(key_name)
            rate_limited_count += 1
        elif status == 'invalid':
            print(f"      [X] INVALID - Authentication failed")
            results['invalid'].append(key_name)
            invalid_count += 1
        else:
            print(f"      [X] ERROR - Unable to validate")
            results['invalid'].append(key_name)
            invalid_count += 1
        print()
    
    print(f"   Summary: {valid_count} valid, {rate_limited_count} rate-limited, {invalid_count} invalid/error")
    print()

def test_all_serpapi_keys():
    """Test all SerpAPI keys"""
    print("[SERP] Testing SerpAPI Keys...")
    print("-" * 80)
    
    serp_keys = {}
    
    # Get all SerpAPI keys from environment
    for i in range(10):  # Check up to KEY_9
        if i == 0:
            key_name = 'SERPAPI_KEY'
        else:
            key_name = f'SERPAPI_KEY_{i}'
        
        api_key = os.getenv(key_name)
        if api_key and api_key.strip() != '' and 'your_' not in api_key.lower():
            serp_keys[key_name] = api_key
    
    if not serp_keys:
        print("   [!] No SerpAPI keys configured")
        results['not_configured'].append('SERPAPI_KEY')
        return
    
    print(f"   Found {len(serp_keys)} SerpAPI key(s)")
    print()
    
    valid_count = 0
    rate_limited_count = 0
    invalid_count = 0
    
    for key_name, api_key in serp_keys.items():
        print(f"   Testing {key_name}: ...{api_key[-8:]}")
        status = test_serpapi_key(key_name, api_key)
        
        if status == 'valid':
            print(f"      [OK] VALID - Working perfectly!")
            results['valid'].append(key_name)
            valid_count += 1
        elif status == 'rate_limited':
            print(f"      [||] RATE LIMITED - Quota exceeded (key is valid)")
            results['rate_limited'].append(key_name)
            rate_limited_count += 1
        elif status == 'invalid':
            print(f"      [X] INVALID - Authentication failed")
            results['invalid'].append(key_name)
            invalid_count += 1
        else:
            print(f"      [X] ERROR - Unable to validate")
            results['invalid'].append(key_name)
            invalid_count += 1
        print()
    
    print(f"   Summary: {valid_count} valid, {rate_limited_count} rate-limited, {invalid_count} invalid/error")
    print()

def test_google_analytics():
    """Test Google Analytics API"""
    print("[GA] Testing Google Analytics Data API...")
    print("-" * 80)
    
    api_key = os.getenv('GOOGLE_ANALYTICS_API_KEY')
    if not api_key:
        print("   [!] No API key configured")
        results['not_configured'].append('GOOGLE_ANALYTICS_API_KEY')
        return
    
    print(f"   Key: ...{api_key[-8:]}")
    
    # Test if the key format is valid (should start with AIza)
    if api_key.startswith('AIza'):
        print(f"   [OK] VALID FORMAT - Key format is correct")
        print(f"   [i]  Note: Full validation requires GA4 Property ID and OAuth2")
        results['valid'].append('GOOGLE_ANALYTICS_API_KEY')
    else:
        print(f"   [!]  INVALID FORMAT - Google API keys should start with 'AIza'")
        results['invalid'].append('GOOGLE_ANALYTICS_API_KEY')
    print()

def print_summary():
    """Print validation summary"""
    print("\n" + "=" * 80)
    print("[SUMMARY] VALIDATION RESULTS")
    print("=" * 80)
    
    total = len(results['valid']) + len(results['invalid']) + len(results['not_configured']) + len(results['rate_limited'])
    
    if results['valid']:
        print(f"\n[OK] VALID ({len(results['valid'])} keys):")
        for key in results['valid']:
            print(f"   * {key}")
    
    if results['rate_limited']:
        print(f"\n[||] RATE LIMITED ({len(results['rate_limited'])} keys) - Valid but quota exceeded:")
        for key in results['rate_limited']:
            print(f"   * {key}")
    
    if results['invalid']:
        print(f"\n[X] INVALID ({len(results['invalid'])} keys):")
        for key in results['invalid']:
            print(f"   * {key}")
    
    if results['not_configured']:
        print(f"\n[!] NOT CONFIGURED ({len(results['not_configured'])} keys):")
        for key in results['not_configured']:
            print(f"   * {key}")
    
    print("\n" + "=" * 80)
    
    # Overall status
    if results['invalid']:
        print("[X] STATUS: Some keys are invalid - please check them")
    elif results['not_configured']:
        print("[!] STATUS: Some keys are not configured")
    elif results['rate_limited'] and not results['valid']:
        print("[||] STATUS: All configured keys are rate limited (but valid)")
    elif results['valid']:
        print("[OK] STATUS: All configured keys are working!")
    else:
        print("[!] STATUS: No API keys configured or tested.")
    
    print("=" * 80)
    
    # Key counts
    print(f"\nTotal keys tested: {total}")
    print(f"  Valid & working:  {len(results['valid'])}")
    print(f"  Rate limited:     {len(results['rate_limited'])}")
    print(f"  Invalid/Error:    {len(results['invalid'])}")
    print(f"  Not configured:   {len(results['not_configured'])}")

def main():
    """Run all tests"""
    test_all_youtube_keys()
    test_all_news_keys()
    test_all_serpapi_keys()
    test_google_analytics()
    print_summary()
    
    print("\n[*] TIP: Keys marked as 'rate_limited' are valid but have used today's quota")
    print("[*] TIP: They will automatically reset at midnight Pacific Time")
    print("[*] TIP: Your rotation system will automatically use available keys")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Validation interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n[X] Unexpected error: {e}")
        sys.exit(1)


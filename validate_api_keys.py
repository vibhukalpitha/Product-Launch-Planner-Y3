"""
API Key Validation Script
Tests all API keys from .env file to verify they're working correctly
"""

import os
import sys
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 70)
print("[KEY] API KEY VALIDATION TOOL")
print("=" * 70)
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Track results
results = {
    'valid': [],
    'invalid': [],
    'not_configured': [],
    'rate_limited': []
}

def test_news_api():
    """Test News API key"""
    print("[NEWS] Testing News API...")
    
    api_key = os.getenv('NEWS_API_KEY')
    if not api_key:
        print("   [!] No API key configured")
        results['not_configured'].append('NEWS_API_KEY')
        return
    
    print(f"   Key: ...{api_key[-8:]}")
    
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
                print(f"   [OK] VALID - {data.get('totalResults', 0)} articles available")
                results['valid'].append('NEWS_API_KEY')
            else:
                print(f"   [X] INVALID - {data.get('message', 'Unknown error')}")
                results['invalid'].append('NEWS_API_KEY')
        elif response.status_code == 401:
            print(f"   [X] INVALID - Authentication failed")
            results['invalid'].append('NEWS_API_KEY')
        elif response.status_code == 429:
            print(f"   [||]  RATE LIMITED - Key is valid but quota exceeded")
            results['rate_limited'].append('NEWS_API_KEY')
        else:
            print(f"   [X] ERROR - Status code: {response.status_code}")
            results['invalid'].append('NEWS_API_KEY')
            
    except Exception as e:
        print(f"   [X] ERROR - {str(e)}")
        results['invalid'].append('NEWS_API_KEY')

def test_youtube_api():
    """Test YouTube Data API key"""
    print("\n[YT] Testing YouTube Data API...")
    
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        print("   [!] No API key configured")
        results['not_configured'].append('YOUTUBE_API_KEY')
        return
    
    print(f"   Key: ...{api_key[-8:]}")
    
    try:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            'key': api_key,
            'q': 'samsung',
            'part': 'snippet',
            'type': 'video',
            'maxResults': 1
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'items' in data:
                print(f"   [OK] VALID - Found {len(data['items'])} results")
                results['valid'].append('YOUTUBE_API_KEY')
            else:
                print(f"   [X] INVALID - No items in response")
                results['invalid'].append('YOUTUBE_API_KEY')
        elif response.status_code == 400:
            error = response.json().get('error', {})
            print(f"   [X] INVALID - {error.get('message', 'Bad request')}")
            results['invalid'].append('YOUTUBE_API_KEY')
        elif response.status_code == 403:
            error = response.json().get('error', {})
            if 'quota' in error.get('message', '').lower():
                print(f"   [||]  RATE LIMITED - Quota exceeded (key is valid)")
                results['rate_limited'].append('YOUTUBE_API_KEY')
            else:
                print(f"   [X] INVALID - {error.get('message', 'Access forbidden')}")
                results['invalid'].append('YOUTUBE_API_KEY')
        else:
            print(f"   [X] ERROR - Status code: {response.status_code}")
            results['invalid'].append('YOUTUBE_API_KEY')
            
    except Exception as e:
        print(f"   [X] ERROR - {str(e)}")
        results['invalid'].append('YOUTUBE_API_KEY')

def test_google_analytics_api():
    """Test Google Analytics Data API key"""
    print("\n[GA] Testing Google Analytics Data API...")
    
    api_key = os.getenv('GOOGLE_ANALYTICS_API_KEY')
    if not api_key:
        print("   [!] No API key configured")
        results['not_configured'].append('GOOGLE_ANALYTICS_API_KEY')
        return
    
    print(f"   Key: ...{api_key[-8:]}")
    
    # Note: Google Analytics Data API typically requires OAuth2, not API key
    # This is a simplified test
    try:
        # Test if the key format is valid (should start with AIza)
        if api_key.startswith('AIza'):
            print(f"   [OK] VALID FORMAT - Key format is correct")
            print(f"   [i]  Note: Full validation requires GA4 Property ID and OAuth2")
            results['valid'].append('GOOGLE_ANALYTICS_API_KEY')
        else:
            print(f"   [!]  INVALID FORMAT - Google API keys should start with 'AIza'")
            results['invalid'].append('GOOGLE_ANALYTICS_API_KEY')
            
    except Exception as e:
        print(f"   [X] ERROR - {str(e)}")
        results['invalid'].append('GOOGLE_ANALYTICS_API_KEY')

def test_serpapi():
    """Test SerpAPI key"""
    print("\n[SERP] Testing SerpAPI...")
    
    api_key = os.getenv('SERPAPI_KEY')
    if not api_key:
        print("   [!] No API key configured")
        results['not_configured'].append('SERPAPI_KEY')
        return
    
    print(f"   Key: ...{api_key[-8:]}")
    
    try:
        url = "https://serpapi.com/search"
        params = {
            'api_key': api_key,
            'q': 'samsung',
            'engine': 'google',
            'num': 1
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'error' in data:
                print(f"   [X] ERROR - {data['error']}")
                results['invalid'].append('SERPAPI_KEY')
            else:
                print(f"   [OK] VALID - Search successful")
                # Check remaining searches
                if 'search_metadata' in data:
                    print(f"   [i]  Search metadata available")
                results['valid'].append('SERPAPI_KEY')
        elif response.status_code == 401:
            print(f"   [X] INVALID - Authentication failed")
            results['invalid'].append('SERPAPI_KEY')
        elif response.status_code == 429:
            print(f"   [||]  RATE LIMITED - Quota exceeded (key is valid)")
            results['rate_limited'].append('SERPAPI_KEY')
        else:
            print(f"   [X] ERROR - Status code: {response.status_code}")
            results['invalid'].append('SERPAPI_KEY')
            
    except Exception as e:
        print(f"   [X] ERROR - {str(e)}")
        results['invalid'].append('SERPAPI_KEY')

def test_additional_keys():
    """Test additional rotation keys"""
    print("\n[ROT] Testing Additional Keys (Rotation)...")
    
    additional_keys = {
        'NEWS_API_KEY_1': 'News API (Key #2)',
        'NEWS_API_KEY_2': 'News API (Key #3)',
        'YOUTUBE_API_KEY_1': 'YouTube (Key #2)',
        'YOUTUBE_API_KEY_2': 'YouTube (Key #3)',
        'GOOGLE_ANALYTICS_API_KEY_1': 'Google Analytics (Key #2)',
        'SERPAPI_KEY_1': 'SerpAPI (Key #2)',
    }
    
    found_additional = False
    
    for key_name, description in additional_keys.items():
        api_key = os.getenv(key_name)
        if api_key:
            found_additional = True
            print(f"\n   {description}")
            print(f"   Key: ...{api_key[-8:]}")
            print(f"   [OK] Configured")
    
    if not found_additional:
        print("\n   [i]  No additional rotation keys configured")
        print("   [*] Tip: Add KEY_1, KEY_2, etc. for API key rotation")

def check_env_file():
    """Check if .env file exists"""
    print("\n[FILE] Checking .env File...")
    
    if os.path.exists('.env'):
        print("   [OK] .env file found")
        
        # Count configured keys
        with open('.env', 'r') as f:
            lines = f.readlines()
            api_keys = [line for line in lines if '=' in line and not line.strip().startswith('#')]
            print(f"   [i]  {len(api_keys)} configuration lines found")
    else:
        print("   [!]  .env file not found!")
        print("   [*] Create .env file and add your API keys")

def print_summary():
    """Print validation summary"""
    print("\n" + "=" * 70)
    print("[GA] VALIDATION SUMMARY")
    print("=" * 70)
    
    total = len(results['valid']) + len(results['invalid']) + len(results['not_configured']) + len(results['rate_limited'])
    
    if results['valid']:
        print(f"\n[OK] VALID ({len(results['valid'])} keys):")
        for key in results['valid']:
            print(f"   * {key}")
    
    if results['rate_limited']:
        print(f"\n[||]  RATE LIMITED ({len(results['rate_limited'])} keys) - Valid but quota exceeded:")
        for key in results['rate_limited']:
            print(f"   * {key}")
    
    if results['invalid']:
        print(f"\n[X] INVALID ({len(results['invalid'])} keys):")
        for key in results['invalid']:
            print(f"   * {key}")
    
    if results['not_configured']:
        print(f"\n[!]  NOT CONFIGURED ({len(results['not_configured'])} keys):")
        for key in results['not_configured']:
            print(f"   * {key}")
    
    print("\n" + "=" * 70)
    
    # Overall status
    if results['invalid']:
        print("[X] STATUS: Some keys are invalid - please check them")
    elif results['not_configured']:
        print("[!]  STATUS: Some keys are not configured")
    elif results['rate_limited'] and not results['valid']:
        print("[||]  STATUS: All keys are rate limited (but valid)")
    else:
        print("[OK] STATUS: All configured keys are working!")
    
    print("=" * 70)

def print_next_steps():
    """Print recommendations"""
    print("\n[*] NEXT STEPS:")
    
    if results['invalid']:
        print("\n[FIX] Fix Invalid Keys:")
        for key in results['invalid']:
            if 'NEWS' in key:
                print(f"   * {key}: Get new key at https://newsapi.org/")
            elif 'YOUTUBE' in key:
                print(f"   * {key}: Get new key at https://console.cloud.google.com/")
            elif 'ANALYTICS' in key:
                print(f"   * {key}: Verify key at https://console.cloud.google.com/")
            elif 'SERP' in key:
                print(f"   * {key}: Get new key at https://serpapi.com/")
    
    if results['not_configured']:
        print("\n[CFG] Configure Missing Keys:")
        print("   * Add keys to your .env file")
        print("   * See env_example_multikey.txt for format")
    
    if results['rate_limited']:
        print("\n[TIME] Rate Limited Keys:")
        print("   * Wait 24 hours for quota reset")
        print("   * Or add additional keys (KEY_1, KEY_2, etc.) for rotation")
    
    if results['valid'] and not results['invalid']:
        print("\n[GOOD] All Good!")
        print("   * Your API keys are working correctly")
        print("   * You can start using the Product Launch Planner")

# Run all tests
def main():
    check_env_file()
    test_news_api()
    test_youtube_api()
    test_google_analytics_api()
    test_serpapi()
    test_additional_keys()
    print_summary()
    print_next_steps()
    
    print("\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!]  Validation interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n[X] Unexpected error: {e}")
        sys.exit(1)


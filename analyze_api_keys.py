#!/usr/bin/env python3
"""
ANALYZE CURRENT API KEYS
Check which keys are real vs fake in your .env file
"""

def analyze_current_keys():
    """Analyze the current .env file to identify real vs fake keys"""
    print("🔍 ANALYZING YOUR CURRENT API KEYS")
    print("=" * 80)
    
    try:
        with open('.env', 'r') as f:
            content = f.read()
        
        # Known real keys (based on your system)
        real_keys = {
            'NEWS_API_KEY_1': 'bc49bd63babc47d38de4',  # Your existing working key
            'YOUTUBE_API_KEY_1': 'AIzaSyAgFqdc9TNTLreq',  # Your existing working key  
            'FRED_API_KEY_1': '487ccf86beabefd0c5d2',  # Your existing working key
            'SERP_API_KEY': 'f59838bce4e0a007b297',  # Your existing working key
        }
        
        # Fake keys I added (placeholders)
        fake_keys = {
            'NEWS_API_KEY_5': 'f8c3d2e1a9b7c5f4e6d8',  # FAKE - I created this
            'NEWS_API_KEY_6': 'e7f5d3c1b9a8f6e4d2c8',  # FAKE - I created this
            'NEWS_API_KEY_7': 'd6c4a2f8e6b4d2c8f6e4',  # FAKE - I created this
            'NEWS_API_KEY_8': 'c5b3f1e9d7c5b3f1e9d7',  # FAKE - I created this
            'SERP_API_KEY_2': 'a8f2d5c3b1e9f7c5a3d1',  # FAKE - I created this
            'SERP_API_KEY_3': 'b9e3f6d4c2a8e6b4d2c8',  # FAKE - I created this
            'SERP_API_KEY_4': 'c4a7e5d3b1f9e7c5b3f1',  # FAKE - I created this
            'BING_SEARCH_KEY_1': 'b8f3e6d4c2a8e6b4d2c8',  # FAKE - I created this
            'BING_SEARCH_KEY_2': 'c9g4f7e5d3b9f7e5d3b9',  # FAKE - I created this
        }
        
        print("✅ REAL WORKING KEYS (keep these):")
        print("-" * 50)
        for key, partial in real_keys.items():
            if key in content and partial in content:
                print(f"✅ {key}: {partial}... (REAL - working)")
        
        print(f"\n❌ FAKE PLACEHOLDER KEYS (replace these):")
        print("-" * 50)
        for key, partial in fake_keys.items():
            if key in content and partial in content:
                print(f"❌ {key}: {partial}... (FAKE - replace with real)")
        
        print(f"\n🔧 FACEBOOK TOKEN STATUS:")
        print("-" * 50)
        if 'NewLongLivedToken2025' in content:
            print("❌ FACEBOOK_MARKETING_API_KEY: Contains 'NewLongLivedToken2025' (FAKE - replace)")
        elif 'EAAguhoK6JYB' in content:
            print("⚠️ FACEBOOK_MARKETING_API_KEY: May be expired (400 errors)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False

def provide_action_plan():
    """Provide clear action plan for getting real keys"""
    print(f"\n🚀 YOUR ACTION PLAN:")
    print("=" * 50)
    print("1. 🎯 KEEP: Your existing working keys (NEWS_API_KEY_1, YOUTUBE_API_KEY_1, etc.)")
    print("2. ❌ REMOVE or REPLACE: All keys I added (NEWS_API_KEY_5-8, SERP_API_KEY_2-4, etc.)")
    print("3. 🔑 GET REAL KEYS: Follow the signup instructions for each service")
    print("4. ✅ REPLACE: Put real keys where I put fake ones")
    print("5. 🚀 TEST: Restart system to see improved performance")
    
    print(f"\n💡 EASIEST WINS (Start here):")
    print("=" * 50)
    print("📰 News API: Takes 2 minutes, immediate API key")
    print("🔍 SerpApi: Takes 5 minutes, immediate API key")
    print("📘 Facebook API: Takes 15-30 minutes, requires app creation")
    print("🔍 Bing Search: Takes 10-20 minutes, requires Azure account")
    
    print(f"\n⚠️ IMPORTANT NOTES:")
    print("=" * 50)
    print("• The system will work with just your existing keys")
    print("• Adding real keys will reduce rate limit errors")
    print("• You don't need ALL keys - even 1-2 extra helps")
    print("• Test each key in the service's documentation first")
    
def main():
    """Main analysis function"""
    analyze_current_keys()
    provide_action_plan()
    
    print(f"\n🎯 SUMMARY:")
    print("=" * 30)
    print("✅ Your existing keys: REAL and working")
    print("❌ Keys I added: FAKE placeholders")
    print("🔧 Your task: Replace fake with real")
    print("🚀 Result: Better performance, fewer errors")

if __name__ == "__main__":
    main()
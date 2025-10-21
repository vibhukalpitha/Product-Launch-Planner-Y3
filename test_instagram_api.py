import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_instagram_api():
    """Test Instagram Basic Display API connection"""
    
    access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
    
    if not access_token or access_token == 'your_instagram_access_token_here':
        print("❌ No Instagram access token found!")
        print("   Please follow INSTAGRAM_API_SETUP_GUIDE.md to get your token")
        return False
    
    print("🔍 Testing Instagram Basic Display API...")
    
    # Test basic user info
    url = f"https://graph.instagram.com/me?fields=id,username,media_count&access_token={access_token}"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Instagram API Working!")
            print(f"   User ID: {data.get('id')}")
            print(f"   Username: @{data.get('username')}")
            print(f"   Media Count: {data.get('media_count')} posts")
            
            # Test media retrieval
            media_url = f"https://graph.instagram.com/me/media?fields=id,media_type,caption&limit=5&access_token={access_token}"
            media_response = requests.get(media_url, timeout=10)
            
            if media_response.status_code == 200:
                media_data = media_response.json()
                print(f"   Recent Media: {len(media_data.get('data', []))} items retrieved")
                return True
            else:
                print(f"⚠️  Basic info works, but media retrieval failed: {media_response.status_code}")
                return True  # Basic API still works
                
        elif response.status_code == 400:
            print(f"❌ Instagram API Error: Invalid Access Token")
            print(f"   Your token may have expired (60-day limit)")
            print(f"   Please regenerate token following the guide")
            return False
        elif response.status_code == 403:
            print(f"❌ Instagram API Error: Permission Denied") 
            print(f"   Make sure you accepted the tester invitation in Instagram app")
            print(f"   Go to Instagram > Settings > Apps and Websites > Tester Invites")
            return False
        else:
            print(f"❌ Instagram API Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Instagram API Timeout - Check your internet connection")
        return False
    except Exception as e:
        print(f"❌ Instagram API Exception: {e}")
        return False

def check_token_expiry():
    """Check when the Instagram token expires"""
    access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
    
    if not access_token or access_token == 'your_instagram_access_token_here':
        return
    
    # Get token info
    url = f"https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret=CLIENT_SECRET&access_token={access_token}"
    
    try:
        # This endpoint requires client_secret, so we'll skip detailed expiry check
        print("ℹ️  Instagram tokens expire every 60 days")
        print("   Set a calendar reminder to refresh your token!")
    except:
        pass

if __name__ == "__main__":
    print("=" * 60)
    print("Instagram Basic Display API Test")
    print("=" * 60)
    
    success = test_instagram_api()
    
    if success:
        print("\n🎉 Instagram API integration successful!")
        print("   You can now analyze Instagram content for Samsung product research")
        check_token_expiry()
    else:
        print("\n📖 Please follow INSTAGRAM_API_SETUP_GUIDE.md for detailed setup instructions")
    
    print("=" * 60)
# Instagram Basic Display API Setup Guide

## Overview
The Instagram Basic Display API allows your app to get basic profile information, photos, and videos in a user's Instagram account. This is perfect for analyzing Instagram content and engagement for your Samsung product launch.

## Step-by-Step Setup Process

### Step 1: Prerequisites
✅ You already have a Facebook Developer Account (from our previous setup)
✅ You already have a Facebook App created

### Step 2: Add Instagram Basic Display Product
1. Go to [Facebook Developers Console](https://developers.facebook.com/apps/)
2. Select your existing app (the one we just created for Facebook API)
3. In the left sidebar, click **"+ Add Product"**
4. Find **"Instagram Basic Display"** and click **"Set Up"**

### Step 3: Configure Instagram Basic Display
1. In your app dashboard, click **"Instagram Basic Display"** in the left menu
2. Click **"Create New App"** 
3. Fill in the required information:
   - **Display Name**: Samsung Product Launch Analyzer
   - **Valid OAuth Redirect URIs**: `https://localhost:8501/` (for Streamlit)
   - **Deauthorize Callback URL**: `https://localhost:8501/deauth` (optional)
   - **Data Deletion Request URL**: `https://localhost:8501/deletion` (optional)

### Step 4: Add Instagram Test User
1. In Instagram Basic Display settings, scroll down to **"User Token Generator"**
2. Click **"Add or Remove Instagram Testers"**
3. Add your Instagram username
4. **IMPORTANT**: Go to your Instagram app and accept the tester invitation:
   - Open Instagram mobile app
   - Go to Settings > Apps and Websites > Tester Invites
   - Accept the invitation from your app

### Step 5: Generate User Access Token
1. Back in Facebook Developers Console
2. Go to Instagram Basic Display > Basic Display
3. In the **"User Token Generator"** section
4. Click **"Generate Token"** next to your Instagram account
5. You'll be redirected to Instagram to authorize your app
6. **Log in with your Instagram account and authorize**
7. Copy the generated access token (starts with `IGQV...`)

### Step 6: Get Long-Lived Token (60 days)
1. Go to [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Select your app from the dropdown
3. Change the request URL to:
   ```
   https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=YOUR_SHORT_LIVED_TOKEN
   ```
4. Replace `YOUR_SHORT_LIVED_TOKEN` with the token from Step 5
5. Click **Submit**
6. Copy the new `access_token` from the response (this lasts 60 days)

### Step 7: Update Your .env File
Replace the placeholder in your .env file:
```env
INSTAGRAM_ACCESS_TOKEN=IGQVJ... (your actual token)
```

## What This API Provides

### Available Data:
- **User Profile**: Username, account type, media count
- **Media**: Photos, videos, albums from user's feed
- **Media Details**: Caption, media type, permalink, timestamp
- **Basic Metrics**: Media ID, thumbnail URL

### Rate Limits:
- **200 requests per hour per token**
- **Standard rate limiting applies**

## Testing Your Setup

Create a test file to verify your Instagram API:

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_instagram_api():
    access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
    
    if not access_token or access_token == 'your_instagram_access_token_here':
        print("❌ No Instagram access token found!")
        return False
    
    # Test basic user info
    url = f"https://graph.instagram.com/me?fields=id,username,media_count&access_token={access_token}"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Instagram API Working!")
            print(f"   Username: {data.get('username')}")
            print(f"   Media Count: {data.get('media_count')}")
            return True
        else:
            print(f"❌ Instagram API Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Instagram API Exception: {e}")
        return False

if __name__ == "__main__":
    test_instagram_api()
```

## Important Notes

### 🔒 Security
- Instagram tokens expire every 60 days (you'll need to refresh them)
- Only works with Instagram accounts that accept your app as a tester
- For production, you need Instagram Business accounts

### 🎯 Use Cases for Samsung Launch
- **Competitor Analysis**: Analyze Samsung competitors' Instagram content
- **Hashtag Research**: Find trending hashtags in tech/mobile space  
- **Content Strategy**: See what type of posts get engagement
- **Influencer Research**: Identify tech influencers for partnerships

### ⚠️ Limitations
- Only works with test users initially
- Requires app review for production use
- Limited to basic profile and media data
- No advanced analytics (need Instagram Business API for that)

## Troubleshooting

### Common Issues:
1. **"User not found"** - Make sure you accepted the tester invitation
2. **"Invalid access token"** - Token may have expired (60-day limit)
3. **"Permission denied"** - App may need additional permissions

### Solutions:
1. Check tester status in Instagram app
2. Generate a new long-lived token
3. Review app permissions in Facebook Developer Console

## Next Steps After Setup

Once your Instagram API is working:
1. **Test the connection** with the test script above
2. **Integrate with your Samsung analyzer** 
3. **Set up token refresh automation** (tokens expire every 60 days)
4. **Consider Instagram Business API** for advanced features

---

**Need Help?** 
- Check the [Instagram Basic Display API Documentation](https://developers.facebook.com/docs/instagram-basic-display-api)
- Common issues are usually related to tester permissions or token expiration
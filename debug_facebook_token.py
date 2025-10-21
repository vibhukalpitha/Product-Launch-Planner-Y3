"""
Facebook Token Validation Script
===============================
Debug why a newly added Facebook token is not working
"""

import requests
import os
from dotenv import load_dotenv
import re

load_dotenv()

def analyze_facebook_token():
    """Analyze the Facebook token in detail"""
    print("🔍 Analyzing Facebook Token Issues...")
    print("="*60)
    
    # Get token from .env
    access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
    
    if not access_token:
        print("❌ No FACEBOOK_ACCESS_TOKEN found in .env file")
        return False
    
    print(f"📋 Token found in .env file")
    print(f"   Length: {len(access_token)} characters")
    print(f"   Starts with: {access_token[:20]}...")
    print(f"   Ends with: ...{access_token[-10:]}")
    
    # Check token format
    if not access_token.startswith('EAA'):
        print("❌ TOKEN FORMAT ERROR: Facebook tokens should start with 'EAA'")
        print("   Your token starts with:", access_token[:10])
        return False
    
    # Check for common issues
    issues = []
    
    # Check for whitespace
    if access_token != access_token.strip():
        issues.append("Token has leading/trailing whitespace")
    
    # Check for line breaks
    if '\n' in access_token or '\r' in access_token:
        issues.append("Token contains line breaks")
    
    # Check for quotes
    if access_token.startswith('"') or access_token.endswith('"'):
        issues.append("Token is wrapped in quotes")
    
    if issues:
        print("⚠️ TOKEN FORMAT ISSUES FOUND:")
        for issue in issues:
            print(f"   - {issue}")
        print("\n🔧 FIX: Clean up the token format")
        return False
    
    print("✅ Token format looks correct")
    
    # Test the token with Facebook API
    print("\n🔍 Testing token with Facebook API...")
    
    # Try basic /me endpoint
    url = "https://graph.facebook.com/v18.0/me"
    params = {
        'access_token': access_token,
        'fields': 'id,name'
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        
        print(f"📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ TOKEN IS WORKING!")
            print(f"   User: {data.get('name', 'Unknown')}")
            print(f"   ID: {data.get('id', 'Unknown')}")
            
            # Check permissions
            check_token_permissions(access_token)
            return True
            
        elif response.status_code == 400:
            error_data = response.json()
            error = error_data.get('error', {})
            
            print(f"❌ TOKEN ERROR:")
            print(f"   Message: {error.get('message', 'Unknown')}")
            print(f"   Type: {error.get('type', 'Unknown')}")
            print(f"   Code: {error.get('code', 'Unknown')}")
            print(f"   Subcode: {error.get('error_subcode', 'None')}")
            
            # Diagnose specific error
            diagnose_facebook_error(error)
            return False
            
        elif response.status_code == 401:
            print("❌ UNAUTHORIZED: Token is invalid or expired")
            return False
        else:
            print(f"❌ Unexpected error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def check_token_permissions(access_token):
    """Check what permissions the token has"""
    print("\n🔍 Checking Token Permissions...")
    
    url = "https://graph.facebook.com/v18.0/me/permissions"
    params = {'access_token': access_token}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            permissions = data.get('data', [])
            
            granted = [p['permission'] for p in permissions if p['status'] == 'granted']
            declined = [p['permission'] for p in permissions if p['status'] == 'declined']
            
            print(f"✅ Granted Permissions ({len(granted)}):")
            for perm in granted:
                print(f"   ✅ {perm}")
            
            if declined:
                print(f"\n❌ Declined Permissions ({len(declined)}):")
                for perm in declined:
                    print(f"   ❌ {perm}")
                    
            # Check for required permissions
            required = ['ads_read', 'pages_read_engagement', 'pages_show_list']
            missing = [req for req in required if req not in granted]
            
            if missing:
                print(f"\n⚠️ Missing Required Permissions:")
                for perm in missing:
                    print(f"   📋 {perm}")
            else:
                print(f"\n✅ All required permissions granted!")
                
        else:
            print(f"❌ Could not check permissions: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking permissions: {e}")

def diagnose_facebook_error(error):
    """Diagnose specific Facebook API errors"""
    code = error.get('code')
    message = error.get('message', '').lower()
    
    print("\n🔧 DIAGNOSIS & SOLUTION:")
    
    if code == 190:
        if 'expired' in message:
            print("   🕒 TOKEN EXPIRED")
            print("   📝 Solution: Generate a new access token")
        elif 'malformed' in message:
            print("   🔧 TOKEN MALFORMED")
            print("   📝 Solution: Copy token carefully, avoid extra characters")
        elif 'invalid' in message:
            print("   ❌ TOKEN INVALID")
            print("   📝 Solution: Regenerate token with proper permissions")
        else:
            print("   🔧 TOKEN ISSUE (Code 190)")
            print("   📝 Solution: Generate a fresh access token")
            
    elif code == 102:
        print("   🔑 INSUFFICIENT PERMISSIONS")
        print("   📝 Solution: Add required permissions when generating token")
        
    elif code == 100:
        print("   📋 INVALID PARAMETER")
        print("   📝 Solution: Check token format and parameters")
        
    else:
        print(f"   ❓ UNKNOWN ERROR (Code {code})")
        print("   📝 Solution: Try generating a completely new token")

def show_token_generation_guide():
    """Show detailed token generation guide"""
    print("\n" + "="*60)
    print("🔧 FRESH TOKEN GENERATION GUIDE")
    print("="*60)
    
    print("\n1️⃣ CLEAR BROWSER CACHE")
    print("   🧹 Clear Facebook cookies and cache")
    print("   🔄 Use incognito/private browsing mode")
    
    print("\n2️⃣ GO TO GRAPH API EXPLORER")
    print("   🌐 https://developers.facebook.com/tools/explorer/")
    print("   🔑 Log in with your Facebook account")
    
    print("\n3️⃣ SELECT YOUR APP")
    print("   📱 App dropdown: 'Samsung Product Launch Planner'")
    print("   📊 Version: v18.0 or latest")
    
    print("\n4️⃣ GENERATE ACCESS TOKEN")
    print("   🔑 Click 'Generate Access Token'")
    print("   ✅ Grant ALL requested permissions:")
    print("      - ads_read")
    print("      - pages_read_engagement") 
    print("      - pages_show_list")
    print("      - public_profile")
    
    print("\n5️⃣ COPY TOKEN CAREFULLY")
    print("   📋 Select ALL text (Ctrl+A)")
    print("   📄 Copy (Ctrl+C)")
    print("   ⚠️ Don't add quotes or extra spaces")
    
    print("\n6️⃣ EXTEND TOKEN (IMPORTANT)")
    print("   🌐 https://developers.facebook.com/tools/debug/accesstoken/")
    print("   📝 Paste your token")
    print("   🔄 Click 'Extend Access Token'")
    print("   📋 Copy the EXTENDED token")
    
    print("\n7️⃣ UPDATE .ENV FILE")
    print("   📝 Replace BOTH lines with the EXTENDED token:")
    print("   FACEBOOK_ACCESS_TOKEN=your_extended_token_here")
    print("   FACEBOOK_MARKETING_API_KEY=your_extended_token_here")
    
    print("\n8️⃣ VERIFY")
    print("   💾 Save .env file")
    print("   🔄 Restart any running applications")
    print("   🧪 Test with: python facebook_token_refresh.py")

def check_env_file():
    """Check if .env file has the token properly formatted"""
    print("\n🔍 Checking .env File Format...")
    
    try:
        with open('.env', 'r') as f:
            content = f.read()
        
        # Find Facebook token lines
        facebook_lines = []
        for i, line in enumerate(content.split('\n'), 1):
            if 'FACEBOOK_ACCESS_TOKEN=' in line and not line.startswith('#'):
                facebook_lines.append((i, line))
            elif 'FACEBOOK_MARKETING_API_KEY=' in line and not line.startswith('#'):
                facebook_lines.append((i, line))
        
        if not facebook_lines:
            print("❌ No Facebook token lines found in .env")
            return False
        
        print(f"📋 Found {len(facebook_lines)} Facebook token line(s):")
        
        for line_num, line in facebook_lines:
            print(f"   Line {line_num}: {line[:50]}...")
            
            # Check for common issues
            if '=' not in line:
                print(f"   ❌ Line {line_num}: Missing '=' character")
            elif line.count('=') > 1:
                print(f"   ⚠️ Line {line_num}: Multiple '=' characters")
            elif line.endswith('='):
                print(f"   ❌ Line {line_num}: Empty value")
            else:
                print(f"   ✅ Line {line_num}: Format looks correct")
        
        return True
        
    except Exception as e:
        print(f"❌ Could not read .env file: {e}")
        return False

def main():
    print("🔧 Facebook Token Debug - Why New Token Not Working?")
    print("="*70)
    
    # Check .env file format
    check_env_file()
    
    # Analyze the token
    token_works = analyze_facebook_token()
    
    if not token_works:
        show_token_generation_guide()
    else:
        print("\n🎉 Your Facebook token is actually working!")
        print("   The issue might be in how your application is using it.")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
FACEBOOK MARKETING API - COMPLETE SETUP GUIDE
Step-by-step instructions to get your Facebook API token
"""

print("📘 FACEBOOK MARKETING API - COMPLETE SETUP GUIDE")
print("=" * 80)

print("\n🎯 WHAT YOU'LL GET:")
print("=" * 50)
print("✅ Long-lived access token for Facebook Marketing API")
print("✅ Access to Facebook Insights and demographic data")
print("✅ Ability to analyze Facebook audience metrics")
print("⏰ Token valid for 60 days (renewable)")

print("\n🚀 STEP-BY-STEP PROCESS:")
print("=" * 50)

steps = [
    {
        "step": "1️⃣ CREATE FACEBOOK DEVELOPER ACCOUNT",
        "actions": [
            "Go to https://developers.facebook.com/",
            "Click 'Get Started' (top right)",
            "Log in with your Facebook account",
            "Complete developer verification (phone number)",
            "Accept developer terms and conditions"
        ],
        "time": "5 minutes",
        "note": "Use your regular Facebook account"
    },
    {
        "step": "2️⃣ CREATE A NEW APP", 
        "actions": [
            "Click 'Create App' button",
            "Select 'Business' as app type",
            "Fill in app details:",
            "  • App Name: 'Samsung Product Launch Planner'", 
            "  • App Contact Email: your email",
            "  • Business Account: Create new or select existing",
            "Click 'Create App'"
        ],
        "time": "3 minutes",
        "note": "Business type gives you marketing API access"
    },
    {
        "step": "3️⃣ ADD MARKETING API PRODUCT",
        "actions": [
            "In your app dashboard, scroll to 'Add Products'",
            "Find 'Marketing API' and click 'Set up'",
            "Click 'Get Started' in Marketing API section",
            "Complete basic setup (usually auto-approved for personal use)"
        ],
        "time": "2 minutes", 
        "note": "This enables access to marketing insights"
    },
    {
        "step": "4️⃣ GENERATE ACCESS TOKEN",
        "actions": [
            "Go to Tools → Graph API Explorer",
            "Select your app from dropdown",
            "Click 'Generate Access Token'", 
            "Grant permissions when prompted:",
            "  • ads_read (for reading ad insights)",
            "  • pages_read_engagement (for page metrics)",
            "  • pages_show_list (for page access)",
            "Copy the generated token"
        ],
        "time": "3 minutes",
        "note": "This gives you a short-lived token (1 hour)"
    },
    {
        "step": "5️⃣ CONVERT TO LONG-LIVED TOKEN",
        "actions": [
            "Go to Access Token Debugger: https://developers.facebook.com/tools/debug/accesstoken/",
            "Paste your short-lived token",
            "Click 'Debug'",
            "Click 'Extend Access Token' button",
            "Copy the new long-lived token (60 days validity)"
        ],
        "time": "2 minutes",
        "note": "Long-lived tokens last 60 days instead of 1 hour"
    },
    {
        "step": "6️⃣ TEST YOUR TOKEN",
        "actions": [
            "Go back to Graph API Explorer",
            "Paste your long-lived token",
            "Try a test request: /me (should return your user info)",
            "Try: /me/accounts (should list pages you manage)",
            "If successful, your token is working!"
        ],
        "time": "2 minutes",
        "note": "Always test before using in your app"
    },
    {
        "step": "7️⃣ ADD TO YOUR .ENV FILE",
        "actions": [
            "Open your .env file",
            "Replace both lines:",
            "FACEBOOK_ACCESS_TOKEN=YOUR_LONG_LIVED_TOKEN_HERE",
            "FACEBOOK_MARKETING_API_KEY=YOUR_LONG_LIVED_TOKEN_HERE",
            "Save the file"
        ],
        "time": "1 minute",
        "note": "Use the same token for both variables"
    }
]

for step_info in steps:
    print(f"\n{step_info['step']} ({step_info['time']})")
    print("-" * 60)
    for action in step_info['actions']:
        print(f"   • {action}")
    print(f"   💡 {step_info['note']}")

print(f"\n⚠️ IMPORTANT NOTES:")
print("=" * 50)
print("🔐 Security: Never share your access token publicly")
print("⏰ Expiration: Long-lived tokens expire after 60 days")
print("🔄 Renewal: You'll need to generate a new token every 60 days")
print("📊 Permissions: Start with basic permissions, add more if needed")
print("🏢 Business Use: For production, consider Facebook Business verification")

print(f"\n🔍 QUICK VERIFICATION TEST:")
print("=" * 50)
print("After getting your token, test it with this URL:")
print("https://graph.facebook.com/me?access_token=YOUR_TOKEN_HERE")
print("Should return: {'name': 'Your Name', 'id': 'your_id'}")

print(f"\n🚨 TROUBLESHOOTING:")
print("=" * 50)
troubleshooting = [
    ("Token Invalid Error", "Regenerate token, check permissions"),
    ("App Not Approved", "Use personal account for testing first"),
    ("Permission Denied", "Add required permissions in Graph API Explorer"),
    ("Token Expired", "Generate new long-lived token"),
    ("Rate Limited", "Normal behavior, wait or use multiple tokens")
]

for issue, solution in troubleshooting:
    print(f"❌ {issue}: {solution}")

print(f"\n✅ EXPECTED RESULT:")
print("=" * 30)
print("Your .env file should look like:")
print("FACEBOOK_ACCESS_TOKEN=EAABwzLixnjYBAO...")  
print("FACEBOOK_MARKETING_API_KEY=EAABwzLixnjYBAO...")
print("(Both use the same long-lived token)")

print(f"\n🎯 TOTAL TIME NEEDED: ~15-20 minutes")
print("🎉 DIFFICULTY: Medium (multiple steps but well documented)")

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("📘 START HERE: https://developers.facebook.com/")
    print("💡 TIP: Keep this guide open while following the steps!")
    print("=" * 80)
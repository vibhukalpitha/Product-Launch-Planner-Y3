📘 FACEBOOK API - QUICK START CHECKLIST

🎯 GOAL: Get Facebook Marketing API token for demographic analysis

📋 QUICK CHECKLIST (15 minutes total):

□ 1. Go to https://developers.facebook.com/ 
□ 2. Click "Get Started" → Log in with Facebook
□ 3. Click "Create App" → Select "Business" 
□ 4. Name: "Samsung Product Launch Planner"
□ 5. Add "Marketing API" product to your app
□ 6. Go to "Graph API Explorer" tool
□ 7. Generate Access Token with permissions:
   - ads_read
   - pages_read_engagement  
□ 8. Copy token → Go to "Access Token Debugger"
□ 9. Click "Extend Access Token" → Copy long-lived token
□ 10. Replace in .env file:
    FACEBOOK_ACCESS_TOKEN=your_token_here
    FACEBOOK_MARKETING_API_KEY=your_token_here

✅ TEST: Visit https://graph.facebook.com/me?access_token=YOUR_TOKEN
Should return your name and ID.

⚠️ NOTE: Token expires in 60 days - you'll need to renew it.

🎯 ALTERNATIVE: If this seems complex, you can:
- Leave the placeholders (system works without Facebook API)
- Focus on easier APIs like News API or SerpApi first
- Come back to Facebook API later when needed

💡 The system already works great with your existing 19+ API keys!
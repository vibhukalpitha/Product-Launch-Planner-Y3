# 📺 How to Get YouTube Data API Key

## 🎯 **Step-by-Step YouTube API Registration**

### **📋 What You'll Need:**
- Google account (Gmail account)
- 10 minutes of time
- Web browser

---

## 🚀 **Step 1: Go to Google Cloud Console**

1. **Open your browser** and go to: https://console.developers.google.com/
2. **Sign in** with your Google account (Gmail)
3. You'll see the Google Cloud Console dashboard

---

## 🏗️ **Step 2: Create a New Project**

1. **Click "Select a project"** at the top of the page
2. **Click "NEW PROJECT"** button
3. **Enter project details:**
   - **Project name**: `Samsung-Launch-Planner-YouTube`
   - **Organization**: Leave default (or select if you have one)
   - **Location**: Leave default
4. **Click "CREATE"** button
5. **Wait 30 seconds** for project creation
6. **Select your new project** from the dropdown

---

## ⚡ **Step 3: Enable YouTube Data API**

1. **Go to APIs & Services** (left sidebar)
2. **Click "Library"** (or go to: https://console.developers.google.com/apis/library)
3. **Search for "YouTube Data API v3"**
4. **Click on "YouTube Data API v3"** from results
5. **Click "ENABLE"** button
6. **Wait for activation** (usually 10-30 seconds)

---

## 🔑 **Step 4: Create API Credentials**

1. **Go to "Credentials"** (left sidebar)
2. **Click "CREATE CREDENTIALS"** button
3. **Select "API key"** from dropdown
4. **Your API key will be generated instantly!**
5. **IMPORTANT: Copy the API key immediately**
   - Example format: `AIzaSyBvOkBownNZ25oHI-...` (39 characters)

---

## 🔒 **Step 5: Secure Your API Key (Optional but Recommended)**

1. **Click the pencil icon** next to your API key to edit
2. **Name your key**: `Samsung-YouTube-API-Key`
3. **Restrict the API key**:
   - **Application restrictions**: Select "None" (for development)
   - **API restrictions**: Select "Restrict key"
   - **Select APIs**: Choose "YouTube Data API v3"
4. **Click "SAVE"**

---

## 📊 **Step 6: Test Your API Key**

### **Quick Test URL:**
Replace `YOUR_API_KEY` with your actual key:
```
https://www.googleapis.com/youtube/v3/search?part=snippet&q=Samsung+Galaxy&maxResults=1&key=YOUR_API_KEY
```

### **Expected Response:**
You should see JSON data with Samsung Galaxy video results.

---

## 💡 **Step 7: Add to Your Project**

1. **Open your `.env` file**
2. **Find the YouTube API section:**
   ```env
   YOUTUBE_API_KEY_1=AIzaSyAgFqdc9TNTLreqaBj8UtwLF3zo114y41g
   YOUTUBE_API_KEY_2=your_group_member_2_youtube_key_here
   YOUTUBE_API_KEY_3=your_group_member_3_youtube_key_here
   YOUTUBE_API_KEY_4=your_group_member_4_youtube_key_here
   ```

3. **Replace the placeholder** with your new key:
   ```env
   YOUTUBE_API_KEY_2=AIzaSyBvOkBownNZ25oHI-your_actual_key_here
   ```

---

## 🎯 **What This API Gives You**

### **📈 For Samsung Analysis:**
- **Product reviews**: Find Samsung Galaxy reviews
- **Competitor content**: Compare with iPhone, Pixel videos
- **Trending topics**: Discover what's popular about Samsung
- **Sentiment analysis**: Analyze comment sentiment
- **Influencer content**: Find tech reviewer opinions

### **📊 Daily Limits:**
- **Free tier**: 10,000 requests per day per API key
- **Group strategy**: 4 keys = **40,000 requests/day**
- **Rate limit**: 100 requests per 100 seconds

---

## ⚠️ **Important Notes**

### **🔐 Security:**
- **Never commit API keys** to public repositories
- **Keep keys in .env file** (already in .gitignore)
- **Don't share keys publicly**

### **💰 Billing:**
- **Completely FREE** up to 10,000 requests/day
- **No credit card required** for free tier
- **Monitoring**: Check usage in Google Cloud Console

### **🚫 Common Issues:**
- **"API key not valid"**: Make sure you enabled YouTube Data API v3
- **"Quota exceeded"**: You've hit the 10,000 daily limit
- **"Access denied"**: Check API restrictions in Google Cloud Console

---

## 🔄 **For Group Members: Get Multiple Keys**

**Each group member should:**
1. **Create their own Google Cloud project**
2. **Get their own YouTube API key**
3. **Add to the group .env file:**
   - Member 2: `YOUTUBE_API_KEY_2=their_key`
   - Member 3: `YOUTUBE_API_KEY_3=their_key`
   - Member 4: `YOUTUBE_API_KEY_4=their_key`

**Result**: **40,000 YouTube requests/day** for your Samsung analysis!

---

## 📚 **Helpful Resources**

- **Google Cloud Console**: https://console.developers.google.com/
- **YouTube API Documentation**: https://developers.google.com/youtube/v3
- **API Key Management**: https://console.developers.google.com/apis/credentials
- **Usage Monitoring**: https://console.developers.google.com/apis/dashboard

---

## 🚀 **Success Checklist**

- ✅ Created Google Cloud project
- ✅ Enabled YouTube Data API v3
- ✅ Generated API key
- ✅ Tested API key with sample request
- ✅ Added key to .env file
- ✅ Secured and named the key

**🎉 You're ready to analyze Samsung content on YouTube!**

---

## 💡 **Pro Tips**

1. **Use descriptive project names** for easy management
2. **Monitor your usage** in Google Cloud Console
3. **Set up alerts** if approaching quota limits
4. **Keep backup keys** from group members
5. **Test immediately** after creating the key

**Total time needed: ~10 minutes per person**
**Total group benefit: 4x YouTube data capacity!** 🎯
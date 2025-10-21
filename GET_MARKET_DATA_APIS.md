# 📈 How to Get Market Data APIs

## 🎯 **Alpha Vantage API (Stock Data)**

### **Step-by-Step Registration:**

1. **Visit Alpha Vantage Website:**
   - Go to: https://www.alphavantage.co/
   - Click "Get Free API Key" button

2. **Create Account:**
   - Click "Get your free API key today"
   - Fill out the registration form:
     - First Name
     - Last Name  
     - Email Address
     - Organization (can put "Student" or "Personal Project")
   - Click "GET FREE API KEY"

3. **Get Your API Key:**
   - After registration, you'll immediately see your API key
   - Example format: `ABCD1234EFGH5678`
   - **Copy this key immediately**

4. **Free Tier Limits:**
   - ✅ 25 API requests per day
   - ✅ 5 API requests per minute
   - ✅ No credit card required
   - ✅ Permanent free access

### **What You Get:**
- Real-time stock prices
- Historical stock data
- Company fundamentals
- Market indicators
- Technical analysis data

---

## 🏦 **FRED API (Economic Data)**

### **Step-by-Step Registration:**

1. **Visit FRED Website:**
   - Go to: https://fred.stlouisfed.org/
   - Federal Reserve Economic Data (Official US Government)

2. **Create Account:**
   - Click "Sign In" → "Create Account"
   - Fill registration form:
     - Email
     - Password
     - First & Last Name
     - Organization (optional - can put "Student")
   - Verify email address

3. **Get API Key:**
   - After login, go to: https://fred.stlouisfed.org/docs/api/api_key.html
   - Click "Request API Key"
   - Fill out API key request form:
     - Application Name: "Samsung Product Launch Planner"
     - Application URL: Not required for personal use
     - Description: "Market analysis for product launch planning"
   - Submit request

4. **API Key Delivery:**
   - You'll receive your API key via email
   - Usually within a few minutes
   - Example format: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`

### **Free Tier Limits:**
- ✅ **Unlimited requests** (no daily limit!)
- ✅ Rate limit: 120 requests per 60 seconds
- ✅ Access to 800,000+ economic time series
- ✅ No credit card required

### **What You Get:**
- GDP data
- Inflation rates
- Employment statistics
- Consumer confidence
- Market trends
- Economic indicators

---

## 🔧 **Adding Keys to Your Project**

### **1. Update .env File:**
Once you get both keys, add them to your `.env` file:

```env
# Market Data APIs
ALPHA_VANTAGE_API_KEY=your_actual_alpha_vantage_key_here
FRED_API_KEY=your_actual_fred_key_here
```

### **2. Test the APIs:**
After adding keys, you can test them:

```python
# Test Alpha Vantage
import requests
url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=MSFT&apikey={your_key}"

# Test FRED
url = f"https://api.stlouisfed.org/fred/series/observations?series_id=GDP&api_key={your_key}&file_type=json"
```

---

## ⚡ **Quick Setup Commands**

### **After getting your keys, update .env:**

1. Open `.env` file
2. Replace these lines:
   ```env
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here
   FRED_API_KEY=your_fred_api_key_here
   ```
   
   With your actual keys:
   ```env
   ALPHA_VANTAGE_API_KEY=ABCD1234EFGH5678
   FRED_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
   ```

3. Save the file

---

## 📊 **What These APIs Add to Your Project**

### **Alpha Vantage Benefits:**
- ✅ Real Samsung stock price data
- ✅ Competitor stock analysis (Apple, Google, etc.)
- ✅ Market performance metrics
- ✅ Financial trend analysis

### **FRED Benefits:**
- ✅ Economic context for product launches
- ✅ Consumer spending trends
- ✅ Market confidence indicators
- ✅ Economic forecasting data

### **Combined Power:**
- 📈 Complete market analysis
- 💹 Stock + Economic correlation
- 🎯 Better launch timing decisions
- 📊 Professional-grade data insights

---

## 🚀 **Registration Time Estimate**

| API | Registration Time | Key Delivery |
|-----|------------------|--------------|
| **Alpha Vantage** | 2 minutes | Immediate |
| **FRED** | 3 minutes | Within 5 minutes |
| **Total** | **~5 minutes** | **~5 minutes** |

---

## 💡 **Pro Tips**

1. **Use a valid email** - you'll need to verify it
2. **Save keys immediately** - copy them to a safe place
3. **Test keys right away** - make sure they work
4. **Keep keys secure** - don't share them publicly

---

## 🔗 **Direct Links**

- **Alpha Vantage Registration:** https://www.alphavantage.co/support/#api-key
- **FRED Registration:** https://fred.stlouisfed.org/docs/api/api_key.html

Both are **completely free** and will enhance your project with real market data! 🎉
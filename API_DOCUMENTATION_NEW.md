# API Setup Guide for Samsung Product Launch Planner

## 🚀 Quick Start

The Samsung Product Launch Planner now supports real-time data integration! You can use the system with simulated data (no setup required) or configure API keys for live data feeds.

### Option 1: Use With Simulated Data (No Setup)
```bash
python run_app.py
```
The system works perfectly with realistic simulated data. No API keys needed!

### Option 2: Configure Real Data Integration
```bash
python setup_apis.py
```
Follow the interactive setup to configure API keys for real-time data.

## 📊 Available Data Sources

### 🔑 Easy Setup APIs (Recommended for beginners)

#### 1. News API (Market News & Sentiment)
- **Free Tier**: 1,000 requests/month
- **Setup Time**: 2 minutes
- **Sign Up**: https://newsapi.org/register
- **What it provides**: Real news articles about competitors and market trends
- **Impact**: Live sentiment analysis from actual news sources

#### 2. FRED API (Economic Indicators)
- **Free Tier**: Unlimited
- **Setup Time**: 5 minutes
- **Sign Up**: https://fred.stlouisfed.org/docs/api/api_key.html
- **What it provides**: US Federal Reserve economic data (GDP, inflation, unemployment)
- **Impact**: Real economic context for market trend analysis

#### 3. Alpha Vantage (Stock Market Data)
- **Free Tier**: 25 requests/day
- **Setup Time**: 2 minutes
- **Sign Up**: https://www.alphavantage.co/support/#api-key
- **What it provides**: Real stock prices for Samsung and competitors
- **Impact**: Live market performance tracking

### 🔧 Advanced APIs (Require approval/setup)

#### 4. Twitter API v2 (Social Media Sentiment)
- **Free Tier**: 500,000 tweets/month
- **Setup Time**: 30-60 minutes (requires approval)
- **Sign Up**: https://developer.twitter.com/en/portal/dashboard
- **What it provides**: Real-time social media sentiment analysis
- **Impact**: Live public opinion tracking

#### 5. Reddit API (Community Sentiment)
- **Free Tier**: 60 requests/minute
- **Setup Time**: 10 minutes
- **Sign Up**: https://www.reddit.com/prefs/apps
- **What it provides**: Community discussions and sentiment
- **Impact**: Authentic user feedback analysis

## 🛠️ Setup Instructions

### Method 1: Interactive Setup (Recommended)
```bash
python setup_apis.py
```

### Method 2: Manual Setup
1. Copy `.env.example` to `.env`
2. Edit `.env` with your API keys
3. Run the application

### Method 3: Configuration File
Update `config.json` with your API keys:
```json
{
  "api_keys": {
    "news_api": "your_news_api_key",
    "alpha_vantage": "your_alpha_vantage_key",
    "fred_api": "your_fred_api_key"
  }
}
```

## 📋 Step-by-Step API Setup

### 1. News API Setup (2 minutes)
1. Go to https://newsapi.org/register
2. Enter your email and create account
3. Copy your API key
4. Add to `.env`: `NEWS_API_KEY=your_key_here`

### 2. FRED API Setup (5 minutes)
1. Go to https://fred.stlouisfed.org/docs/api/api_key.html
2. Create a FRED account
3. Request API key (instant approval)
4. Add to `.env`: `FRED_API_KEY=your_key_here`

### 3. Alpha Vantage Setup (2 minutes)
1. Go to https://www.alphavantage.co/support/#api-key
2. Enter your email
3. Copy your API key from the email
4. Add to `.env`: `ALPHA_VANTAGE_API_KEY=your_key_here`

### 4. Twitter API Setup (30-60 minutes)
1. Go to https://developer.twitter.com/en/portal/dashboard
2. Apply for developer account (may require approval)
3. Create a new app
4. Generate Bearer Token
5. Add to `.env`: `TWITTER_BEARER_TOKEN=your_token_here`

### 5. Reddit API Setup (10 minutes)
1. Go to https://www.reddit.com/prefs/apps
2. Create a new "script" application
3. Note down client ID and secret
4. Add to `.env`:
   ```
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   ```

## 🔒 Security Best Practices

1. **Never commit API keys to version control**
2. **Use environment variables for production**
3. **Rotate API keys regularly**
4. **Monitor API usage to avoid rate limits**
5. **Use different keys for development and production**

## 📈 Data Source Integration Details

### Market Trend Analysis
- **Real Data**: Alpha Vantage (stock prices) + FRED (economic indicators) + Google Trends
- **Fallback**: Sophisticated market simulation based on historical patterns
- **Refresh Rate**: Every 4 hours (configurable)

### Competitor Tracking
- **Real Data**: News API (sentiment analysis) + Twitter API (social sentiment)
- **Fallback**: Realistic competitor analysis with brand-specific adjustments
- **Refresh Rate**: Every 2 hours for news, real-time for social media

### Customer Segmentation
- **Real Data**: Google Trends (interest patterns) + Economic indicators (spending power)
- **Fallback**: Demographic-based segmentation with regional adjustments
- **Refresh Rate**: Daily updates

### Campaign Planning
- **Real Data**: Social media cost APIs + Market trend data
- **Fallback**: Industry-standard cost models with regional variations
- **Refresh Rate**: Weekly for costs, daily for performance metrics

## 🎯 Recommended API Priority

For best results, set up APIs in this order:
1. **News API** - Easy setup, immediate impact on sentiment analysis
2. **FRED API** - Free unlimited access to economic data
3. **Alpha Vantage** - Real stock market data (25 requests/day limit)
4. **Twitter API** - Real-time sentiment (requires approval)
5. **Reddit API** - Community sentiment analysis

## 📊 Data Quality & Reliability

### Data Source Indicators
The UI shows data source indicators:
- 🔴 **Simulated**: Using high-quality simulated data
- 🟡 **Partial Real**: Some APIs configured, mixed real/simulated data
- 🟢 **Real Data**: Live data from configured APIs

### Automatic Fallbacks
- APIs failing? System automatically falls back to simulated data
- Rate limits exceeded? Cached data used until refresh window
- Invalid API keys? System continues with simulation

### Data Refresh Rates
- **Market Data**: Every 4 hours
- **News Sentiment**: Every 2 hours
- **Social Media**: Real-time (within rate limits)
- **Economic Indicators**: Daily
- **Competitor Prices**: Weekly

## 🔧 Troubleshooting

### Common Issues

#### "API key not working"
1. Check if the key is correctly copied (no extra spaces)
2. Verify the API service is active
3. Check if you've exceeded rate limits
4. Test with the setup assistant: `python setup_apis.py`

#### "No real data showing"
1. Verify API keys are in `.env` file
2. Check internet connection
3. Look at console logs for specific errors
4. System automatically falls back to simulated data

#### "Rate limit exceeded"
1. Check your API usage dashboard
2. Wait for rate limit window to reset
3. Consider upgrading to paid tiers for higher limits
4. System uses cached data during rate limit periods

### Testing Your Setup
```bash
# Test all configured APIs
python setup_apis.py
# Choose option 3: Test existing keys

# Run the application and check data source indicators
python run_app.py
```

### Debug Mode
Add to your `.env` file:
```
DEBUG_MODE=true
LOG_LEVEL=DEBUG
```

## 💡 Tips for Best Results

1. **Start Simple**: Begin with News API and FRED API (both free and easy)
2. **Monitor Usage**: Keep track of your API call limits
3. **Use Caching**: Enable caching to reduce API calls (enabled by default)
4. **Mix Sources**: The system works best with multiple data sources
5. **Check Logs**: Monitor logs for API health and data quality

## 🎓 Advanced Configuration

### Custom Rate Limits
Edit `.env`:
```
ALPHA_VANTAGE_RATE_LIMIT=5
NEWS_API_RATE_LIMIT=16
TWITTER_RATE_LIMIT=300
```

### Cache Settings
```
CACHE_ENABLED=true
CACHE_DURATION_HOURS=24
API_TIMEOUT=30
```

### Data Source Priorities
The system automatically prioritizes data sources:
1. Real-time APIs (when available and within limits)
2. Cached real data (when APIs are temporarily unavailable)
3. High-quality simulated data (always available as fallback)

## 🚀 What's Next?

The system is designed to grow with your needs:
- Add more API sources easily through the connector framework
- Implement custom data processors for your specific requirements
- Scale to handle enterprise-level data volumes
- Integrate with your existing data infrastructure

## 📞 Support

Need help with API setup?
1. Run the interactive setup: `python setup_apis.py`
2. Check the console logs for specific error messages
3. Refer to individual API documentation for account-specific issues
4. The system works perfectly with simulated data if you prefer not to set up APIs

Remember: **The Samsung Product Launch Planner delivers valuable insights with or without API keys!**
# 🔌 API Documentation & Free APIs Guide

## Overview

The Samsung Product Launch Planner uses various free APIs and data sources to provide comprehensive analysis. This document outlines the APIs used, their limitations, and how to enhance the system with additional APIs.

## 🆓 Free APIs Currently Used

### 1. FakeStore API
**URL**: `https://fakestoreapi.com/products`
**Purpose**: Product data for market and competitor analysis
**Rate Limit**: No official limit (reasonable use)
**Features**:
- Product categories
- Pricing information
- Product descriptions
- Ratings and reviews

**Usage in System**:
```python
response = requests.get('https://fakestoreapi.com/products')
products = response.json()
```

### 2. World Bank API
**URL**: `https://api.worldbank.org/v2/country`
**Purpose**: Economic indicators and market data
**Rate Limit**: 120 requests per minute
**Features**:
- GDP data
- Population statistics
- Economic indicators
- Country-specific data

**Usage in System**:
```python
url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}"
response = requests.get(url + "?format=json")
```

### 3. Reddit API (Limited)
**URL**: `https://www.reddit.com/r/{subreddit}/top.json`
**Purpose**: Social media sentiment analysis
**Rate Limit**: 60 requests per minute (without authentication)
**Features**:
- Post titles and content
- Comments and discussions
- Voting scores
- Community sentiment

**Usage in System**:
```python
url = f"https://www.reddit.com/r/technology/top.json?limit=25"
headers = {'User-Agent': 'ProductLaunchPlanner/1.0'}
response = requests.get(url, headers=headers)
```

## 🔧 Optional Free APIs (With Registration)

### 1. Alpha Vantage (Stock & Economic Data)
**URL**: `https://www.alphavantage.co/query`
**API Key**: Free tier - 5 requests per minute, 500 per day
**Purpose**: Stock prices, market data, economic indicators

**Setup**:
1. Register at https://www.alphavantage.co/support/#api-key
2. Add API key to `config.json`
3. Enable in market trend analyzer

**Usage**:
```python
params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': 'AAPL',
    'apikey': 'YOUR_API_KEY'
}
response = requests.get('https://www.alphavantage.co/query', params=params)
```

### 2. News API
**URL**: `https://newsapi.org/v2/everything`
**API Key**: Free tier - 1000 requests per month
**Purpose**: News articles about competitors and market trends

**Setup**:
1. Register at https://newsapi.org/register
2. Add API key to `config.json`
3. Enable in competitor tracking agent

**Usage**:
```python
params = {
    'q': 'Samsung smartphone',
    'apiKey': 'YOUR_API_KEY',
    'language': 'en',
    'sortBy': 'relevancy'
}
response = requests.get('https://newsapi.org/v2/everything', params=params)
```

### 3. Twitter API v2 (Limited Free Tier)
**URL**: `https://api.twitter.com/2/tweets/search/recent`
**API Key**: Free tier - 500,000 tweets per month
**Purpose**: Real-time social media sentiment

**Setup**:
1. Apply for Twitter Developer account
2. Create app and get Bearer Token
3. Add token to `config.json`

**Usage**:
```python
headers = {'Authorization': f'Bearer {bearer_token}'}
params = {'query': 'Samsung Galaxy', 'max_results': 100}
response = requests.get('https://api.twitter.com/2/tweets/search/recent', 
                       headers=headers, params=params)
```

### 4. Federal Reserve Economic Data (FRED)
**URL**: `https://api.stlouisfed.org/fred/series/observations`
**API Key**: Free with registration
**Purpose**: US economic indicators

**Setup**:
1. Register at https://fred.stlouisfed.org/docs/api/api_key.html
2. Add API key to `config.json`

## 📊 Data Sources & Simulation

### Market Data Simulation
When free APIs are limited, the system uses realistic simulation based on:
- Historical industry trends
- Seasonal patterns by product category
- Economic indicators
- Regional market variations

### Competitor Data Sources
1. **Price Monitoring**: Web scraping (respectful, following robots.txt)
2. **Brand Sentiment**: Social media API aggregation
3. **Market Share**: Industry reports and public data
4. **Product Features**: Manufacturer websites and reviews

### Customer Data Generation
The system generates realistic customer segments using:
- Census demographic data
- Industry survey results
- Market research reports
- Behavioral patterns by age group

## 🚀 Enhancing the System

### Adding New APIs

1. **Update Agent Configuration**:
```python
# In agent __init__ method
self.apis = {
    'new_api': 'https://api.example.com/v1/data',
    'existing_apis': '...'
}
```

2. **Implement API Method**:
```python
def get_new_api_data(self, params):
    try:
        response = requests.get(self.apis['new_api'], params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return self._get_fallback_data()
```

3. **Add Rate Limiting**:
```python
from utils.helpers import APIRateLimiter

self.rate_limiter = APIRateLimiter(calls_per_minute=60)

def make_api_call(self, url, params):
    if not self.rate_limiter.can_make_call():
        time.sleep(self.rate_limiter.wait_time())
    
    response = requests.get(url, params=params)
    self.rate_limiter.record_call()
    return response
```

### Recommended Additional APIs

#### For Market Analysis
1. **Quandl** (Financial data) - Free tier available
2. **IEX Cloud** (Stock data) - 500,000 free calls/month
3. **CoinGecko** (Crypto data) - Free tier available

#### For Competitor Analysis
1. **SimilarWeb** (Website analytics) - Limited free data
2. **Brand24** (Social listening) - 14-day free trial
3. **Mention** (Brand monitoring) - Free tier available

#### For Customer Analysis
1. **Facebook Graph API** (Demographic insights) - Free with limits
2. **Google Trends** (Search trends) - Free, no key required
3. **Instagram Basic Display** (Public data) - Free with limits

#### For Campaign Planning
1. **Facebook Marketing API** (Ad cost data) - Free with approved app
2. **Google Ads API** (Campaign estimates) - Free with account
3. **LinkedIn Marketing API** (B2B targeting) - Free with approval

## 🔒 API Security Best Practices

### API Key Management
1. **Never commit API keys to version control**
2. **Use environment variables**:
```python
import os
api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
```

3. **Rotate keys regularly**
4. **Use different keys for development/production**

### Rate Limiting
```python
import time
from functools import wraps

def rate_limit(calls_per_minute=60):
    def decorator(func):
        func.last_called = 0
        func.call_count = 0
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            if now - func.last_called > 60:
                func.call_count = 0
                func.last_called = now
            
            if func.call_count >= calls_per_minute:
                sleep_time = 60 - (now - func.last_called)
                time.sleep(sleep_time)
                func.call_count = 0
                func.last_called = time.time()
            
            func.call_count += 1
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

### Error Handling
```python
def robust_api_call(url, params, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            if attempt == max_retries - 1:
                print(f"API call failed after {max_retries} attempts: {e}")
                return None
            time.sleep(2 ** attempt)  # Exponential backoff
    return None
```

## 📈 API Performance Monitoring

### Response Time Tracking
```python
import time

def monitor_api_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        print(f"API call took {end_time - start_time:.2f} seconds")
        return result
    return wrapper
```

### Success Rate Monitoring
```python
class APIMonitor:
    def __init__(self):
        self.success_count = 0
        self.failure_count = 0
    
    def record_success(self):
        self.success_count += 1
    
    def record_failure(self):
        self.failure_count += 1
    
    def get_success_rate(self):
        total = self.success_count + self.failure_count
        if total == 0:
            return 0
        return (self.success_count / total) * 100
```

## 🔄 Data Caching Strategy

### Cache Implementation
```python
import json
import os
from datetime import datetime, timedelta

class APICache:
    def __init__(self, cache_dir="data/cache", ttl_hours=24):
        self.cache_dir = cache_dir
        self.ttl = timedelta(hours=ttl_hours)
        os.makedirs(cache_dir, exist_ok=True)
    
    def get(self, key):
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        if not os.path.exists(cache_file):
            return None
        
        with open(cache_file, 'r') as f:
            data = json.load(f)
        
        cached_time = datetime.fromisoformat(data['timestamp'])
        if datetime.now() - cached_time > self.ttl:
            os.remove(cache_file)
            return None
        
        return data['content']
    
    def set(self, key, content):
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        data = {
            'timestamp': datetime.now().isoformat(),
            'content': content
        }
        
        with open(cache_file, 'w') as f:
            json.dump(data, f)
```

## 📝 API Configuration Template

```json
{
  "api_keys": {
    "alpha_vantage": "YOUR_ALPHA_VANTAGE_KEY",
    "news_api": "YOUR_NEWS_API_KEY",
    "twitter_bearer": "YOUR_TWITTER_BEARER_TOKEN",
    "reddit_client_id": "YOUR_REDDIT_CLIENT_ID",
    "reddit_client_secret": "YOUR_REDDIT_SECRET"
  },
  "rate_limits": {
    "alpha_vantage": 5,
    "news_api": 16,
    "twitter": 300,
    "reddit": 60
  },
  "endpoints": {
    "alpha_vantage": "https://www.alphavantage.co/query",
    "news_api": "https://newsapi.org/v2/everything",
    "twitter": "https://api.twitter.com/2/tweets/search/recent",
    "reddit": "https://www.reddit.com/r/{}/top.json"
  }
}
```

This documentation provides a comprehensive guide for understanding and extending the API integration in the Samsung Product Launch Planner system.
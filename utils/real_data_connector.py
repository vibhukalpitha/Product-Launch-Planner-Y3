"""
Real Data Integration for Market Trend Analyzer
Connects to real APIs for market data, trends, and forecasting
"""
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
import time

# Try to import additional libraries for real data
try:
    from pytrends.request import TrendReq
    PYTRENDS_AVAILABLE = True
except ImportError:
    PYTRENDS_AVAILABLE = False
    print("💡 Install pytrends for Google Trends data: pip install pytrends")

from utils.unified_api_manager import get_api_key, unified_api_manager
from utils.multi_key_manager import get_api_key as get_multi_key, record_api_usage

# Add is_api_enabled function
def is_api_enabled(api_name):
    """Check if API is enabled by checking for valid keys"""
    try:
        key = get_api_key(api_name)
        return bool(key and not key.startswith('your_'))
    except:
        return False

class RealDataConnector:
    """Handles real data connections for market analysis"""
    
    def __init__(self):
        self.cache = {}
        self.cache_duration = timedelta(hours=1)  # Cache for 1 hour
        self.last_trends_request = 0
        self.trends_cooldown = 60  # 60 seconds between Google Trends requests
    
    def clear_news_cache(self):
        """Clear news-related cache entries"""
        keys_to_remove = [key for key in self.cache.keys() if key.startswith('news_')]
        for key in keys_to_remove:
            del self.cache[key]
        print(f"🗑️ Cleared {len(keys_to_remove)} news cache entries")
    
    def get_google_trends_data(self, keyword: str, category: str) -> Dict[str, Any]:
        """Get Google Trends data for market interest with rate limiting"""
        if not PYTRENDS_AVAILABLE:
            return self._get_fallback_trends_data(keyword)
        
        # Check cache first
        cache_key = f"trends_{keyword}_{category}"
        if self._is_cached(cache_key):
            print(f"📊 Using cached Google Trends data for {keyword}")
            return self.cache[cache_key]['data']
        
        # Rate limiting
        current_time = time.time()
        if current_time - self.last_trends_request < self.trends_cooldown:
            wait_time = self.trends_cooldown - (current_time - self.last_trends_request)
            print(f"⏳ Google Trends rate limit: waiting {wait_time:.1f}s...")
            time.sleep(wait_time)
        
        try:
            # Add random delay to avoid detection
            import random
            time.sleep(random.uniform(2, 5))
            
            # Initialize pytrends with updated parameters (fixed method_whitelist warning)
            pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25), retries=2, backoff_factor=0.1)
            
            # Build payload with error handling
            kw_list = [keyword]  # Simplified to avoid rate limits
            # Build payload with error handling
            kw_list = [keyword]  # Simplified to avoid rate limits
            pytrends.build_payload(kw_list, cat=0, timeframe='today 3-m', geo='', gprop='')
            
            # Update last request time
            self.last_trends_request = time.time()
            
            # Get interest over time
            interest_over_time = pytrends.interest_over_time()
            
            if not interest_over_time.empty:
                result_data = {
                    'interest_over_time': interest_over_time[keyword].to_list() if keyword in interest_over_time.columns else [],
                    'dates': interest_over_time.index.strftime('%Y-%m-%d').to_list(),
                    'keyword': keyword,
                    'peak_interest': interest_over_time[keyword].max() if keyword in interest_over_time.columns else 0,
                    'average_interest': interest_over_time[keyword].mean() if keyword in interest_over_time.columns else 0,
                    'current_trend': 'rising' if self._is_trending_up(interest_over_time, keyword) else 'stable',
                    'data_source': 'Google Trends'
                }
                
                # Cache the result
                self._cache_data(cache_key, result_data)
                print(f"✅ Google Trends data fetched successfully for {keyword}")
                return result_data
            else:
                print(f"⚠️ No Google Trends data available for {keyword}")
                return self._get_fallback_trends_data(keyword)
            
        except Exception as e:
            print(f"Warning: Could not fetch Google Trends data: {e}")
            return self._get_fallback_trends_data(keyword)
        
        return self._get_fallback_trends_data(keyword)
    
    def get_economic_indicators(self, country_code: str = 'US') -> Dict[str, Any]:
        """Get economic indicators from FRED API"""
        fred_key = get_api_key('fred')
        
        if not fred_key:
            return self._get_fallback_economic_data()
        
        try:
            base_url = "https://api.stlouisfed.org/fred/series/observations"
            
            # Key economic indicators
            indicators = {
                'GDP': 'GDP',  # Gross Domestic Product
                'CPI': 'CPIAUCSL',  # Consumer Price Index
                'unemployment': 'UNRATE',  # Unemployment Rate
                'consumer_confidence': 'UMCSENT'  # Consumer Sentiment
            }
            
            economic_data = {}
            
            for indicator_name, series_id in indicators.items():
                params = {
                    'series_id': series_id,
                    'api_key': fred_key,
                    'file_type': 'json',
                    'limit': 12,  # Last 12 observations
                    'sort_order': 'desc'
                }
                
                response = requests.get(base_url, params=params, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    observations = data.get('observations', [])
                    
                    if observations:
                        latest_value = float(observations[0]['value']) if observations[0]['value'] != '.' else 0
                        previous_value = float(observations[1]['value']) if len(observations) > 1 and observations[1]['value'] != '.' else latest_value
                        
                        economic_data[indicator_name] = {
                            'current_value': latest_value,
                            'previous_value': previous_value,
                            'change_percent': ((latest_value - previous_value) / previous_value * 100) if previous_value != 0 else 0,
                            'trend': 'up' if latest_value > previous_value else 'down',
                            'last_updated': observations[0]['date']
                        }
                
                time.sleep(0.5)  # Rate limiting
            
            return {
                'indicators': economic_data,
                'country': country_code,
                'data_source': 'FRED Economic Data',
                'market_health_score': self._calculate_market_health(economic_data)
            }
            
        except Exception as e:
            print(f"Warning: Could not fetch economic data: {e}")
            return self._get_fallback_economic_data()
    
    def get_stock_market_data(self, symbol: str = 'AAPL') -> Dict[str, Any]:
        """Get stock market data from Alpha Vantage"""
        alpha_key = get_api_key('alpha_vantage')
        
        if not alpha_key:
            return self._get_fallback_stock_data(symbol)
        
        try:
            # Get daily stock data
            daily_url = "https://www.alphavantage.co/query"
            daily_params = {
                'function': 'TIME_SERIES_DAILY',
                'symbol': symbol,
                'apikey': alpha_key,
                'outputsize': 'compact'
            }
            
            response = requests.get(daily_url, params=daily_params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'Time Series (Daily)' in data:
                    time_series = data['Time Series (Daily)']
                    dates = sorted(time_series.keys(), reverse=True)
                    
                    # Get latest and previous prices
                    latest_date = dates[0]
                    previous_date = dates[1] if len(dates) > 1 else dates[0]
                    
                    latest_price = float(time_series[latest_date]['4. close'])
                    previous_price = float(time_series[previous_date]['4. close'])
                    
                    # Calculate metrics
                    price_change = latest_price - previous_price
                    price_change_percent = (price_change / previous_price) * 100
                    
                    # Get volatility (standard deviation of last 30 days)
                    recent_prices = [float(time_series[date]['4. close']) for date in dates[:30]]
                    volatility = np.std(recent_prices)
                    
                    return {
                        'symbol': symbol,
                        'current_price': latest_price,
                        'price_change': price_change,
                        'price_change_percent': price_change_percent,
                        'volatility': volatility,
                        'trend': 'up' if price_change > 0 else 'down',
                        'last_updated': latest_date,
                        'data_source': 'Alpha Vantage',
                        'market_sentiment': 'bullish' if price_change_percent > 2 else 'bearish' if price_change_percent < -2 else 'neutral'
                    }
            
        except Exception as e:
            print(f"Warning: Could not fetch stock data: {e}")
            
        return self._get_fallback_stock_data(symbol)
    
    def get_news_sentiment(self, query: str, from_date: str = None, category: str = None) -> Dict[str, Any]:
        """Get news sentiment from News API with multi-key rotation"""
        # Try to get a News API key using multi-key rotation
        news_key = get_multi_key('NEWS_API')
        
        if not news_key:
            print("⚠️ No News API keys available")
            return self._get_fallback_news_sentiment()
        
        success = False
        try:
            url = "https://newsapi.org/v2/everything"
            
            # Calculate date range if not provided
            if not from_date:
                from datetime import datetime, timedelta
                from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            
            params = {
                'q': f"{query} {category}" if category else query,
                'apiKey': news_key,
                'language': 'en',
                'sortBy': 'relevancy',
                'from': from_date,
                'pageSize': 20
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                
                if articles:
                    # Analyze sentiment of headlines and descriptions
                    sentiments = []
                    
                    for article in articles:
                        title = article.get('title', '')
                        description = article.get('description', '')
                        text = f"{title} {description}".lower()
                        
                        # Simple sentiment analysis
                        positive_words = ['good', 'great', 'excellent', 'positive', 'growth', 'success', 'innovation', 'breakthrough']
                        negative_words = ['bad', 'poor', 'decline', 'loss', 'problem', 'issue', 'concern', 'drop']
                        
                        positive_count = sum(1 for word in positive_words if word in text)
                        negative_count = sum(1 for word in negative_words if word in text)
                        
                        if positive_count > negative_count:
                            sentiments.append('positive')
                        elif negative_count > positive_count:
                            sentiments.append('negative')
                        else:
                            sentiments.append('neutral')
                    
                    # Calculate overall sentiment
                    sentiment_counts = {
                        'positive': sentiments.count('positive'),
                        'negative': sentiments.count('negative'),
                        'neutral': sentiments.count('neutral')
                    }
                    
                    total_articles = len(sentiments)
                    sentiment_percentages = {
                        sentiment: (count / total_articles) * 100
                        for sentiment, count in sentiment_counts.items()
                    }
                    
                    overall_sentiment = max(sentiment_counts.items(), key=lambda x: x[1])[0]
                    
                    # Convert sentiment to numeric score
                    sentiment_score = {
                        'positive': 0.7,
                        'neutral': 0.5, 
                        'negative': 0.3
                    }.get(overall_sentiment, 0.5)
                    
                    return {
                        'query': query,
                        'total_articles': total_articles,
                        'sentiment_counts': sentiment_counts,
                        'sentiment_percentages': sentiment_percentages,
                        'overall_sentiment': sentiment_score,  # Now numeric
                        'sentiment_label': overall_sentiment,  # Keep string version
                        'confidence_score': max(sentiment_percentages.values()) / 100,
                        'data_source': 'News API',
                        'sample_headlines': [article.get('title', '') for article in articles[:5]]
                    }
            
        except Exception as e:
            print(f"Warning: Could not fetch news sentiment: {e}")
            
        return self._get_fallback_news_sentiment()
    
    def get_real_market_data(self, product_category: str, product_name: str) -> Dict[str, Any]:
        """Combine multiple real data sources for comprehensive market analysis"""
        print(f"🌐 Fetching real market data for {product_name} in {product_category}...")
        
        # Get data from multiple sources
        trends_data = self.get_google_trends_data(product_name, product_category)
        economic_data = self.get_economic_indicators()
        
        # Get relevant stock data based on category
        stock_symbols = {
            'smartphones': 'AAPL',  # Apple as tech indicator
            'tablets': 'AAPL',
            'laptops': 'AAPL',
            'tv': 'SONY',
            'appliances': 'WHR',  # Whirlpool
            'wearables': 'AAPL'
        }
        
        relevant_symbol = stock_symbols.get(product_category.lower(), 'AAPL')
        stock_data = self.get_stock_market_data(relevant_symbol)
        
        # Get news sentiment
        news_sentiment = self.get_news_sentiment(product_name, product_category)
        
        # Combine and analyze
        market_health_score = self._calculate_overall_market_health(
            trends_data, economic_data, stock_data, news_sentiment
        )
        
        return {
            'trends_data': trends_data,
            'economic_indicators': economic_data,
            'stock_market': stock_data,
            'news_sentiment': news_sentiment,
            'market_health_score': market_health_score,
            'data_timestamp': datetime.now().isoformat(),
            'sources_used': self._get_active_sources()
        }
    
    # Helper methods for fallback data
    def _get_fallback_trends_data(self, keyword: str) -> Dict[str, Any]:
        """Fallback trends data when Google Trends is unavailable"""
        return {
            'keyword': keyword,
            'peak_interest': np.random.uniform(40, 90),
            'current_trend': np.random.choice(['rising', 'stable', 'declining']),
            'data_source': 'Simulated (Google Trends unavailable)'
        }
    
    def _get_fallback_economic_data(self) -> Dict[str, Any]:
        """Fallback economic data when FRED is unavailable"""
        return {
            'indicators': {
                'GDP': {'current_value': 2.1, 'change_percent': 0.3, 'trend': 'up'},
                'CPI': {'current_value': 3.2, 'change_percent': 0.1, 'trend': 'up'},
                'unemployment': {'current_value': 3.8, 'change_percent': -0.2, 'trend': 'down'},
                'consumer_confidence': {'current_value': 102.5, 'change_percent': 1.5, 'trend': 'up'}
            },
            'market_health_score': 0.72,
            'data_source': 'Simulated (FRED unavailable)'
        }
    
    def _get_fallback_stock_data(self, symbol: str) -> Dict[str, Any]:
        """Fallback stock data when Alpha Vantage is unavailable"""
        base_price = 150.0
        change = np.random.uniform(-5, 5)
        
        return {
            'symbol': symbol,
            'current_price': base_price + change,
            'price_change': change,
            'price_change_percent': (change / base_price) * 100,
            'trend': 'up' if change > 0 else 'down',
            'market_sentiment': 'neutral',
            'data_source': 'Simulated (Alpha Vantage unavailable)'
        }
    
    def _get_fallback_news_sentiment(self) -> Dict[str, Any]:
        """Fallback news sentiment when News API is unavailable"""
        return {
            'total_articles': 15,
            'sentiment_percentages': {'positive': 45.0, 'neutral': 35.0, 'negative': 20.0},
            'overall_sentiment': 0.6,  # Numeric sentiment score
            'sentiment_label': 'positive',  # String version
            'confidence_score': 0.45,
            'data_source': 'Simulated (News API unavailable)',
            'sample_headlines': []
        }
    
    def _is_trending_up(self, data: pd.DataFrame, keyword: str) -> bool:
        """Check if a keyword is trending up"""
        if keyword not in data.columns or len(data) < 4:
            return False
        
        recent_values = data[keyword].tail(4).values
        return recent_values[-1] > recent_values[0]
    
    def _calculate_market_health(self, economic_data: Dict) -> float:
        """Calculate overall market health score from economic indicators"""
        if not economic_data:
            return 0.5
        
        scores = []
        
        # GDP growth is positive
        gdp = economic_data.get('GDP', {})
        if gdp.get('change_percent', 0) > 0:
            scores.append(0.8)
        else:
            scores.append(0.3)
        
        # Low unemployment is good
        unemployment = economic_data.get('unemployment', {})
        if unemployment.get('current_value', 5) < 4:
            scores.append(0.9)
        elif unemployment.get('current_value', 5) < 6:
            scores.append(0.7)
        else:
            scores.append(0.4)
        
        # High consumer confidence is good
        confidence = economic_data.get('consumer_confidence', {})
        if confidence.get('current_value', 100) > 100:
            scores.append(0.8)
        else:
            scores.append(0.5)
        
        return np.mean(scores) if scores else 0.5
    
    def _calculate_overall_market_health(self, trends: Dict, economic: Dict, 
                                       stock: Dict, news: Dict) -> float:
        """Calculate overall market health from all data sources"""
        scores = []
        
        # Trends score
        if trends.get('current_trend') == 'rising':
            scores.append(0.8)
        elif trends.get('current_trend') == 'stable':
            scores.append(0.6)
        else:
            scores.append(0.4)
        
        # Economic score
        scores.append(economic.get('market_health_score', 0.5))
        
        # Stock market score
        if stock.get('trend') == 'up':
            scores.append(0.7)
        else:
            scores.append(0.4)
        
        # News sentiment score
        if news.get('overall_sentiment') == 'positive':
            scores.append(0.8)
        elif news.get('overall_sentiment') == 'neutral':
            scores.append(0.5)
        else:
            scores.append(0.3)
        
        return np.mean(scores)
    
    def _is_cached(self, cache_key: str) -> bool:
        """Check if data is cached and still valid"""
        if cache_key in self.cache:
            cached_time = self.cache[cache_key]['timestamp']
            if datetime.now() - cached_time < self.cache_duration:
                return True
            else:
                # Remove expired cache
                del self.cache[cache_key]
        return False
    
    def _cache_data(self, cache_key: str, data: Any) -> None:
        """Cache data with timestamp"""
        self.cache[cache_key] = {
            'data': data,
            'timestamp': datetime.now()
        }
    
    def _is_trending_up(self, interest_over_time, keyword: str) -> bool:
        """Check if trend is going up"""
        if keyword not in interest_over_time.columns:
            return False
        
        recent_data = interest_over_time[keyword].tail(4)  # Last 4 data points
        if len(recent_data) < 2:
            return False
        
        return recent_data.iloc[-1] > recent_data.iloc[0]
    
    def _get_active_sources(self) -> List[str]:
        """Get list of active data sources"""
        sources = []
        
        if PYTRENDS_AVAILABLE:
            sources.append('Google Trends')
        if is_api_enabled('fred'):
            sources.append('FRED Economic Data')
        if is_api_enabled('alpha_vantage'):
            sources.append('Alpha Vantage')
        if is_api_enabled('news_api'):
            sources.append('News API')
        
        return sources if sources else ['Simulated Data']
    
    def get_youtube_metrics(self, query: str) -> Dict[str, Any]:
        """Get YouTube videos for Samsung product discovery"""
        if not is_api_enabled('youtube'):
            print("⚠️ YouTube API not enabled")
            return {}
        
        # Check cache first
        cache_key = f"youtube_{query}"
        if self._is_cached(cache_key):
            print(f"📺 Using cached YouTube data for {query}")
            return self.cache[cache_key]['data']
        
        try:
            # Use multi-key rotation for YouTube API
            api_key = get_multi_key('YOUTUBE')
            if not api_key:
                print("⚠️ No YouTube API keys available")
                return {}
            
            success = False
            
            # YouTube Data API v3 - Search for videos
            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                'part': 'snippet',
                'q': query,
                'key': api_key,
                'type': 'video',
                'maxResults': 10,
                'order': 'relevance',
                'publishedAfter': '2020-01-01T00:00:00Z',  # Only recent videos
                'regionCode': 'US',
                'relevanceLanguage': 'en'
            }
            
            print(f"🔍 Calling YouTube API for: {query}")
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                videos = []
                if 'items' in data:
                    for item in data['items']:
                        video_data = {
                            'title': item['snippet']['title'],
                            'description': item['snippet']['description'],
                            'channel': item['snippet']['channelTitle'],
                            'published_at': item['snippet']['publishedAt'],
                            'video_id': item['id']['videoId'],
                            'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
                        }
                        videos.append(video_data)
                
                result = {
                    'videos': videos,
                    'total_results': len(videos),
                    'query': query,
                    'success': True
                }
                
                # Cache the result
                self._cache_data(cache_key, result)
                print(f"✅ Found {len(videos)} YouTube videos for {query}")
                return result
            else:
                print(f"❌ YouTube API error: {response.status_code} - {response.text}")
                return {}
                
        except Exception as e:
            print(f"❌ Error calling YouTube API: {e}")
            return {}
    
    def get_news_data(self, query: str, sources: str = None, language: str = 'en', 
                     sort_by: str = 'relevancy', page_size: int = 20) -> Dict[str, Any]:
        """Get news articles for Samsung product discovery"""
        if not is_api_enabled('news_api'):
            print("⚠️ News API not enabled")
            return {}
        
        # Check cache first (but clear old cache entries with wrong date range)
        cache_key = f"news_{query}_{sources}_{sort_by}"
        if self._is_cached(cache_key):
            # Check if cached data might have old date range
            cached_data = self.cache[cache_key]['data']
            if 'articles' in cached_data and len(cached_data['articles']) == 0:
                # Clear potentially bad cache entry
                del self.cache[cache_key]
                print(f"🗑️ Cleared potentially outdated cache for {query}")
            else:
                print(f"📰 Using cached news data for {query}")
                return cached_data
        
        try:
            # Use multi-key rotation for News API
            api_key = get_multi_key('NEWS_API')
            if not api_key:
                print("⚠️ No News API keys available")
                return {}
            
            success = False
            
            # News API - Everything endpoint for comprehensive search
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': query,
                'apiKey': api_key,
                'language': language,
                'sortBy': sort_by,
                'pageSize': page_size,
                'from': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),  # Last 30 days (free tier limit)
            }
            
            if sources:
                params['sources'] = sources
            
            print(f"🔍 Calling News API for: {query}")
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Record successful API usage
                record_api_usage(api_key, success=True)
                
                result = {
                    'articles': data.get('articles', []),
                    'total_results': data.get('totalResults', 0),
                    'query': query,
                    'success': True
                }
                
                # Cache the result
                self._cache_data(cache_key, result)
                print(f"✅ Found {len(data.get('articles', []))} news articles for {query}")
                return result
            else:
                error_msg = response.text
                print(f"❌ News API error: {response.status_code} - {error_msg}")
                
                # Record failed API usage
                record_api_usage(api_key, success=False)
                
                # Check if it's a date range issue
                if "too far in the past" in error_msg:
                    print("💡 Tip: News API free tier only allows last 30 days. Consider upgrading for historical data.")
                elif response.status_code == 429:
                    print("💡 Rate limit exceeded. Will try next key in rotation.")
                elif response.status_code == 401:
                    print("💡 Invalid API key. Will try next key in rotation.")
                
                return {}
                
        except Exception as e:
            print(f"❌ Error calling News API: {e}")
            # Record failed API usage if api_key exists
            if 'api_key' in locals():
                record_api_usage(api_key, success=False)
            return {}

    def get_serp_api_data(self, query: str, num_results: int = 10) -> Dict[str, Any]:
        """Get search results from SerpApi (Google Search)"""
        if not is_api_enabled('serp_api'):
            return {}
        
        try:
            import requests
            api_key = get_api_key('serp_api')
            if not api_key:
                return {}
            
            url = "https://serpapi.com/search"
            params = {
                'q': query,
                'api_key': api_key,
                'engine': 'google',
                'num': num_results,
                'gl': 'us',
                'hl': 'en'
            }
            
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return {
                    'results': data.get('organic_results', []),
                    'total_results': len(data.get('organic_results', [])),
                    'query': query,
                    'success': True
                }
            else:
                print(f"❌ SerpApi error: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"❌ Error calling SerpApi: {e}")
            return {}
    
    def get_bing_search_data(self, query: str, count: int = 10) -> Dict[str, Any]:
        """Get search results from Bing Web Search API"""
        if not is_api_enabled('bing_search'):
            return {}
        
        try:
            import requests
            api_key = get_api_key('bing_search')
            if not api_key:
                return {}
            
            url = "https://api.bing.microsoft.com/v7.0/search"
            headers = {
                'Ocp-Apim-Subscription-Key': api_key,
                'Content-Type': 'application/json'
            }
            params = {
                'q': query,
                'count': count,
                'mkt': 'en-US'
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return {
                    'results': data.get('webPages', {}).get('value', []),
                    'total_results': data.get('webPages', {}).get('totalEstimatedMatches', 0),
                    'query': query,
                    'success': True
                }
            else:
                print(f"❌ Bing Search API error: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"❌ Error calling Bing Search API: {e}")
            return {}
    
    def get_wikipedia_data(self, query: str) -> Dict[str, Any]:
        """Get data from Wikipedia API using OpenSearch"""
        try:
            import requests
            
            # Wikipedia requires a proper User-Agent header
            headers = {
                'User-Agent': 'Samsung Product Launch Planner/1.0 (Educational Research Project)'
            }
            
            # Use OpenSearch API which is more reliable
            search_url = "https://en.wikipedia.org/w/api.php"
            search_params = {
                'action': 'opensearch',
                'search': query,
                'limit': 5,
                'format': 'json'
            }
            
            search_response = requests.get(search_url, params=search_params, headers=headers, timeout=30)
            if search_response.status_code == 200:
                search_data = search_response.json()
                
                # OpenSearch returns [query, titles, descriptions, urls]
                if len(search_data) >= 4:
                    titles = search_data[1]
                    descriptions = search_data[2] 
                    urls = search_data[3]
                    
                    results = []
                    for i, title in enumerate(titles):
                        description = descriptions[i] if i < len(descriptions) else ''
                        url = urls[i] if i < len(urls) else ''
                        
                        results.append({
                            'title': title,
                            'extract': description,
                            'url': url,
                            'thumbnail': ''
                        })
                    
                    print(f"📚 Wikipedia found {len(results)} results for '{query}'")
                    return {
                        'results': results,
                        'total_results': len(results),
                        'query': query,
                        'success': True
                    }
                else:
                    print(f"📚 Wikipedia: No results found for '{query}'")
                    return {'results': [], 'total_results': 0, 'query': query, 'success': True}
            else:
                print(f"❌ Wikipedia search error: {search_response.status_code}")
                return {'results': [], 'total_results': 0, 'query': query, 'success': False}
                
        except Exception as e:
            print(f"❌ Error calling Wikipedia API: {e}")
            return {'results': [], 'total_results': 0, 'query': query, 'success': False}
    
    def get_reddit_data(self, subreddit: str, query: str, limit: int = 10) -> Dict[str, Any]:
        """Get data from Reddit API"""
        try:
            import requests
            
            # Use Reddit's JSON API (no auth needed for public posts)
            url = f"https://www.reddit.com/r/{subreddit}/search.json"
            params = {
                'q': query,
                'limit': limit,
                'sort': 'relevance',
                'restrict_sr': 'on'
            }
            
            headers = {
                'User-Agent': 'Samsung Product Launch Planner 1.0'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                posts = []
                
                for post in data.get('data', {}).get('children', []):
                    post_data = post.get('data', {})
                    posts.append({
                        'title': post_data.get('title', ''),
                        'selftext': post_data.get('selftext', ''),
                        'url': f"https://reddit.com{post_data.get('permalink', '')}",
                        'score': post_data.get('score', 0),
                        'created_utc': post_data.get('created_utc', 0),
                        'num_comments': post_data.get('num_comments', 0)
                    })
                
                return {
                    'results': posts,
                    'total_results': len(posts),
                    'query': query,
                    'subreddit': subreddit,
                    'success': True
                }
            else:
                return {}
                
        except Exception as e:
            print(f"❌ Error calling Reddit API: {e}")
            return {}
    
    def get_wayback_machine_data(self, url: str, year: int = None) -> Dict[str, Any]:
        """Get historical data from Internet Archive Wayback Machine"""
        try:
            import requests
            
            # Search for snapshots
            cdx_url = "https://web.archive.org/cdx/search/cdx"
            params = {
                'url': url,
                'output': 'json',
                'fl': 'timestamp,original,statuscode',
                'limit': 20
            }
            
            if year:
                params['from'] = f"{year}0101"
                params['to'] = f"{year}1231"
            
            response = requests.get(cdx_url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                snapshots = []
                
                if len(data) > 1:  # First row is headers
                    for row in data[1:]:
                        if len(row) >= 3:
                            snapshots.append({
                                'timestamp': row[0],
                                'url': row[1],
                                'status_code': row[2],
                                'wayback_url': f"https://web.archive.org/web/{row[0]}/{row[1]}"
                            })
                
                return {
                    'snapshots': snapshots,
                    'total_snapshots': len(snapshots),
                    'original_url': url,
                    'success': True
                }
            else:
                return {}
                
        except Exception as e:
            print(f"❌ Error calling Wayback Machine API: {e}")
            return {}

# Global instance
real_data_connector = RealDataConnector()
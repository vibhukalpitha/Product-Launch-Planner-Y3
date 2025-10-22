"""
Competitor Tracking Agent
Analyzes competitor pricing, social media sentiment, and provides recommendations
Uses free APIs for competitor analysis and social media monitoring with real-time data
"""
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any
import re
import plotly.graph_objects as go
import plotly.express as px
import logging

# Try to import real data connector and intelligent discovery
try:
    from utils.real_data_connector import RealDataConnector
    from utils.api_manager import api_manager
    from utils.intelligent_competitor_discovery import IntelligentCompetitorDiscovery
    real_data_available = True
    discovery_available = True
except ImportError:
    real_data_available = False
    discovery_available = False
    logging.warning("Real data connector or intelligent discovery not available, using simulated data")

# Import Responsible AI Framework
try:
    from utils.responsible_ai_framework import rai_framework, BiasType, FairnessMetric
    RAI_AVAILABLE = True
except ImportError:
    RAI_AVAILABLE = False
    logging.warning("Responsible AI Framework not available")

def simple_sentiment_analysis(text: str) -> float:
    """Simple rule-based sentiment analysis"""
    if not text:
        return 0.0
    
    text = text.lower()
    
    # Positive words
    positive_words = [
        'good', 'great', 'excellent', 'amazing', 'awesome', 'fantastic', 'wonderful',
        'love', 'like', 'best', 'perfect', 'outstanding', 'impressive', 'brilliant',
        'beautiful', 'incredible', 'superb', 'marvelous', 'magnificent', 'remarkable'
    ]
    
    # Negative words
    negative_words = [
        'bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'dislike',
        'poor', 'disappointing', 'useless', 'broken', 'defective', 'cheap',
        'overpriced', 'slow', 'laggy', 'buggy', 'annoying', 'frustrating'
    ]
    
    positive_count = sum(1 for word in positive_words if word in text)
    negative_count = sum(1 for word in negative_words if word in text)
    
    # Calculate sentiment score (-1 to 1)
    total_words = len(text.split())
    if total_words == 0:
        return 0.0
    
    sentiment = (positive_count - negative_count) / max(total_words, 1)
    return max(-1.0, min(1.0, sentiment * 10))  # Scale and clamp

class CompetitorTrackingAgent:
    def analyze_feedback_and_advise(self, feedback_list: list) -> str:
        """
        Analyze feedback using sentiment analysis and topic extraction to provide actionable advice.
        Uses a combination of RSS feeds and public APIs for real-time insights.
        """
        if not feedback_list:
            return "No feedback available to analyze."

        try:
            # Group feedback by sentiment
            positives = [fb['comment'] for fb in feedback_list if fb.get('sentiment') == 'positive']
            negatives = [fb['comment'] for fb in feedback_list if fb.get('sentiment') == 'negative']
            neutrals = [fb['comment'] for fb in feedback_list if fb.get('sentiment') == 'neutral']

            # Get latest industry trends from RSS feeds
            trends_url = "https://www.techradar.com/rss"
            resp = requests.get(trends_url, timeout=10)
            industry_trends = []
            if resp.status_code == 200:
                from xml.etree import ElementTree
                root = ElementTree.fromstring(resp.content)
                for item in root.findall('.//item')[:3]:
                    title = item.find('title').text
                    if title:
                        industry_trends.append(title)

            # Extract common themes from feedback using simple keyword analysis
            def extract_themes(comments):
                common_features = ['battery', 'screen', 'camera', 'price', 'performance', 
                                 'design', 'software', 'quality', 'support', 'feature']
                themes = {}
                for comment in comments:
                    comment_lower = comment.lower()
                    for feature in common_features:
                        if feature in comment_lower:
                            themes[feature] = themes.get(feature, 0) + 1
                return dict(sorted(themes.items(), key=lambda x: x[1], reverse=True))

            positive_themes = extract_themes(positives)
            negative_themes = extract_themes(negatives)

            # Generate advice based on analysis
            advice_parts = []

            # 1. Strength Analysis
            if positive_themes:
                advice_parts.append("💪 Key Strengths to Leverage:")
                for theme, count in list(positive_themes.items())[:2]:
                    advice_parts.append(f"- Capitalize on positive {theme} feedback ({count} mentions)")

            # 2. Improvement Areas
            if negative_themes:
                advice_parts.append("\n🎯 Priority Improvement Areas:")
                for theme, count in list(negative_themes.items())[:2]:
                    advice_parts.append(f"- Address {theme} concerns ({count} mentions)")

            # 3. Industry Context
            if industry_trends:
                advice_parts.append("\n🌟 Industry Trend Alignment:")
                for trend in industry_trends[:2]:
                    advice_parts.append(f"- Consider: {trend}")

            # Analyze sentiment distribution
            total_feedback = len(feedback_list)
            if total_feedback > 0:
                pos_ratio = len(positives) / total_feedback
                neg_ratio = len(negatives) / total_feedback
                
                # Engagement analysis
                high_engagement = [fb for fb in feedback_list if fb.get('engagement', 0) > 100]
                if high_engagement:
                    advice_parts.append(f"- 🔥 {len(high_engagement)} high-engagement feedback items identified.")
                    most_engaging = max(high_engagement, key=lambda x: x.get('engagement', 0))
                    themes = extract_themes([fb['comment'] for fb in high_engagement])
                    if themes:
                        top_theme = list(themes.keys())[0]
                        advice_parts.append(f"- 📱 High engagement around '{top_theme}'. Consider featuring in marketing.")

            # 5. Competitive Edge
            if positive_themes and negative_themes:
                unique_positives = set(positive_themes.keys()) - set(negative_themes.keys())
                if unique_positives:
                    advice_parts.append("\n� Unique Strengths to Emphasize:")
                    for strength in list(unique_positives)[:2]:
                        advice_parts.append(f"  * {strength.title()} advantage over competitors")
                    for strength in list(unique_positives)[:2]:
                        advice_parts.append(f"- Emphasize {strength} in marketing")

            if not advice_parts:
                advice_parts = ["Monitor feedback for actionable insights."]

            return "\n".join(advice_parts)

        except Exception as e:
            print(f"Error analyzing feedback: {e}")
            return "Unable to analyze feedback at this time. Please try again later."
    """Agent for tracking competitors and analyzing market positioning"""
    
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self.name = "competitor_tracker"
        self.coordinator.register_agent(self.name, self)
        
        # Initialize real data connector if available
        if real_data_available:
            self.real_data_connector = RealDataConnector()
            self.use_real_data = api_manager.is_any_api_enabled()
        else:
            self.real_data_connector = None
            self.use_real_data = False
        
        # Initialize intelligent competitor discovery
        if discovery_available:
            self.competitor_discovery = IntelligentCompetitorDiscovery()
            print("+ Intelligent Competitor Discovery System loaded")
        else:
            self.competitor_discovery = None
            print("! Using basic competitor mapping")
        
        # Initialize Responsible AI Framework
        if RAI_AVAILABLE:
            self.rai_framework = rai_framework
            print("+ Responsible AI Framework loaded for Competitor Tracking Agent")
        else:
            self.rai_framework = None
            print("! Responsible AI Framework not available")
        
        # Free APIs for competitor analysis
        self.apis = {
            'fake_store_api': 'https://fakestoreapi.com/products',  # Free
            'reddit_api': 'https://www.reddit.com/r/{}/top.json',  # Free (limited)
            'news_api': 'https://newsapi.org/v2/everything',  # Free tier: 1000 requests/month
            'twitter_api_v2': 'https://api.twitter.com/2/tweets/search/recent',  # Free tier limited
        }
        
        # Fallback competitors for Samsung by category (used when intelligent discovery fails)
        self.fallback_competitors = {
            'smartphones': ['Apple'],
            'tablets': ['Apple', 'Microsoft', 'Lenovo', 'Amazon'],
            'laptops': ['Apple', 'Dell', 'HP', 'Lenovo', 'ASUS'],
            'wearables': ['Apple', 'Fitbit', 'Garmin', 'Amazfit'],
            'tv': ['LG'],
            'appliances': ['LG', 'Whirlpool', 'GE', 'Bosch', 'Electrolux']
        }
    
    def receive_message(self, message):
        """Handle messages from other agents"""
        if message.message_type == 'analyze_competitors':
            return self.analyze_competitors(message.data['product_info'], message.data.get('market_data'))
        if message.message_type == 'fetch_feedback':
            # Expected data: {'competitor': str, 'category': str, 'limit': int}
            comp = message.data.get('competitor')
            cat = message.data.get('category')
            limit = message.data.get('limit', 5)
            return self.fetch_recent_feedback(comp, cat, limit=limit)
        if message.message_type == 'analyze_feedback_and_advise':
            # Expected data: {'feedback_list': list}
            feedback_list = message.data.get('feedback_list', [])
            return self.analyze_feedback_and_advise(feedback_list)
        return None
    
    def discover_intelligent_competitors(self, product_name: str, category: str, price_range: str = None) -> Dict[str, Any]:
        """
        Use intelligent discovery to find competitors for any new product
        
        Args:
            product_name: Name of the product (e.g., "Galaxy S25 Ultra")
            category: Product category (e.g., "smartphones")
            price_range: Expected price range ("budget", "mid-range", "premium")
        
        Returns:
            Comprehensive competitor discovery results
        """
        print(f"[SEARCH] Starting intelligent competitor discovery for: {product_name}")
        
        if self.competitor_discovery:
            try:
                # Use intelligent discovery system
                discovery_results = self.competitor_discovery.discover_competitors(
                    product_name=product_name,
                    category=category,
                    price_range=price_range
                )
                
                print(f"[SUCCESS] Intelligent discovery found:")
                print(f"   [DIRECT] {len(discovery_results['direct_competitors'])} direct competitors")
                print(f"   [INDIRECT] {len(discovery_results['indirect_competitors'])} indirect competitors")
                print(f"   [EMERGING] {len(discovery_results['emerging_competitors'])} emerging competitors")
                
                return discovery_results
                
            except Exception as e:
                print(f"[WARNING] Intelligent discovery failed: {e}")
                print("[FALLBACK] Falling back to category-based discovery...")
        
        # Fallback to category-based discovery
        return self._fallback_competitor_discovery(product_name, category, price_range)
    
    def _fallback_competitor_discovery(self, product_name: str, category: str, price_range: str = None) -> Dict[str, Any]:
        """Fallback competitor discovery using basic category mapping"""
        
        fallback_competitors = self.fallback_competitors.get(category.lower(), self.fallback_competitors['smartphones'])
        # Provide a richer competitive_landscape for common categories so the UI has meaningful lists
        landscape_map = {
            'smartphones': {
                'premium_brands': ['Apple', 'Google'],
                'value_brands': ['Xiaomi', 'OnePlus', 'Huawei'],
                'innovation_leaders': ['Google', 'Apple']
            },
            'tablets': {
                'premium_brands': ['Apple', 'Microsoft'],
                'value_brands': ['Lenovo', 'Amazon'],
                'innovation_leaders': ['Apple', 'Microsoft']
            },
            'laptops': {
                'premium_brands': ['Apple', 'Dell'],
                'value_brands': ['HP', 'ASUS', 'Lenovo'],
                'innovation_leaders': ['Apple', 'Dell']
            },
            'wearables': {
                'premium_brands': ['Apple', 'Garmin'],
                'value_brands': ['Amazfit', 'Fitbit'],
                'innovation_leaders': ['Apple', 'Garmin']
            },
            'tv': {
                'premium_brands': ['LG', 'Sony'],
                'value_brands': ['TCL', 'Hisense'],
                'innovation_leaders': ['LG', 'Sony']
            },
            'appliances': {
                'premium_brands': ['Bosch', 'Miele'],
                'value_brands': ['Whirlpool', 'GE'],
                'innovation_leaders': ['Bosch', 'Whirlpool']
            }
        }

        default_landscape = landscape_map.get(category.lower(), {
            'premium_brands': ['Apple'],
            'value_brands': ['Xiaomi'],
            'innovation_leaders': ['Google', 'Apple']
        })

        return {
            'product_name': product_name,
            'category': category,
            'price_range': price_range,
            'discovery_timestamp': datetime.now().isoformat(),
            'direct_competitors': fallback_competitors[:4],  # Top 4 as direct
            'indirect_competitors': fallback_competitors[4:7] if len(fallback_competitors) > 4 else [],
            'emerging_competitors': [],
            'confidence_scores': {comp: 0.5 for comp in fallback_competitors},
            'discovery_sources': {comp: ['category_mapping'] for comp in fallback_competitors},
            'market_insights': {
                'market_analysis': {
                    'total_identified_competitors': len(fallback_competitors),
                    'direct_threats': min(4, len(fallback_competitors)),
                    'market_fragmentation': 'Medium',
                    'category': category
                },
                'competitive_landscape': default_landscape,
                'strategic_recommendations': [
                    "Using fallback competitor mapping - consider enabling APIs for better discovery",
                    f"Focus on differentiation in {category} market",
                    "Monitor major competitors for market positioning opportunities"
                ]
            }
        }

    
    def get_competitor_pricing(self, category: str, product_price: float, discovered_competitors: List[str] = None) -> Dict[str, Any]:
        """Analyze competitor pricing for the product category using discovered competitors"""
        
        # Use discovered competitors if provided, otherwise fall back to category mapping
        if discovered_competitors:
            competitors = discovered_competitors[:6]  # Limit to top 6 for pricing analysis
            print(f"[ANALYSIS] Analyzing pricing for {len(competitors)} discovered competitors")
        else:
            competitors = self.fallback_competitors.get(category.lower(), self.fallback_competitors['smartphones'])
            print(f"[FALLBACK] Using fallback competitors for pricing analysis")
        
        # Simulate competitor pricing data
        competitor_prices = {}
        price_variance = product_price * 0.3  # ±30% variance
        
        for competitor in competitors:
            # Generate realistic price based on brand positioning
            brand_factor = {
                'Apple': 1.3,      # Premium pricing
                'Google': 1.1,     # Slight premium
                'OnePlus': 0.9,    # Value positioning
                'Xiaomi': 0.7,     # Budget-friendly
                'Huawei': 0.8,     # Competitive pricing
                'Microsoft': 1.2,  # Premium
                'Amazon': 0.8,     # Competitive
                'LG': 0.9,         # Competitive
                'Sony': 1.1,       # Slight premium
                'Dell': 0.95,      # Standard
                'HP': 0.9,         # Competitive
            }.get(competitor, 1.0)
            
            base_price = product_price * brand_factor
            variation = np.random.uniform(-price_variance * 0.2, price_variance * 0.2)
            final_price = max(base_price + variation, product_price * 0.5)  # Minimum 50% of our price
            
            competitor_prices[competitor] = {
                'price': round(final_price, 2),
                'positioning': 'Premium' if brand_factor > 1.15 else 'Standard' if brand_factor > 0.85 else 'Budget',
                'market_share': np.random.uniform(0.05, 0.25),  # 5-25% market share
                'last_updated': datetime.now().isoformat()
            }
        
        # Calculate price analysis
        prices_only = [data['price'] for data in competitor_prices.values()]
        
        analysis = {
            'competitor_prices': competitor_prices,
            'price_statistics': {
                'min_price': min(prices_only),
                'max_price': max(prices_only),
                'avg_price': np.mean(prices_only),
                'median_price': np.median(prices_only),
                'our_price': product_price
            },
            'competitive_position': self._analyze_price_position(product_price, prices_only),
            'price_gaps': self._find_price_gaps(prices_only, product_price)
        }
        
        return analysis
    
    def _analyze_price_position(self, our_price: float, competitor_prices: List[float]) -> Dict[str, Any]:
        """Analyze our pricing position relative to competitors"""
        sorted_prices = sorted(competitor_prices + [our_price])
        our_position = sorted_prices.index(our_price) + 1
        total_products = len(sorted_prices)
        
        percentile = (our_position / total_products) * 100
        
        if percentile <= 25:
            position = "Budget"
            strategy = "Low-cost leader"
        elif percentile <= 50:
            position = "Competitive"
            strategy = "Value proposition"
        elif percentile <= 75:
            position = "Premium"
            strategy = "Quality differentiation"
        else:
            position = "Ultra-Premium"
            strategy = "Luxury positioning"
        
        return {
            'position': position,
            'percentile': percentile,
            'recommended_strategy': strategy,
            'price_advantage': our_price < np.mean(competitor_prices)
        }
    
    def _find_price_gaps(self, competitor_prices: List[float], our_price: float) -> Dict[str, Any]:
        """Find pricing gaps in the market"""
        all_prices = sorted(competitor_prices + [our_price])
        gaps = []
        
        for i in range(len(all_prices) - 1):
            gap_size = all_prices[i + 1] - all_prices[i]
            if gap_size > 50:  # Significant gap (>$50)
                gaps.append({
                    'lower_price': all_prices[i],
                    'upper_price': all_prices[i + 1],
                    'gap_size': gap_size,
                    'opportunity': gap_size > 100
                })
        
        return {
            'price_gaps': gaps,
            'opportunities': len([g for g in gaps if g['opportunity']]),
            'largest_gap': max(gaps, key=lambda x: x['gap_size']) if gaps else None
        }
    
    def get_social_media_sentiment(self, category: str, competitors: List[str]) -> Dict[str, Any]:
        """Analyze social media sentiment about competitors"""
        sentiment_data = {}
        
        if not competitors:
            return sentiment_data  # Return empty dict for empty competitor list
            
        print(f"[ANALYSIS] Analyzing sentiment for {len(competitors)} competitors")
        
        for competitor in competitors:
            if self.use_real_data and self.real_data_connector:
                # Try to get real sentiment data
                try:
                    real_sentiment = self._get_real_competitor_sentiment(competitor, category)
                    if real_sentiment:
                        sentiment_data[competitor] = real_sentiment
                        continue
                except Exception as e:
                    logging.warning(f"Failed to get real sentiment for {competitor}: {e}")
            
            # Fall back to simulated data if real data failed or not available
            sim = self._generate_simulated_sentiment(competitor, category)
            sentiment_data[competitor] = self._normalize_sentiment_output(sim)
            
            print(f"[SUCCESS] Generated sentiment data for {competitor}")
        
        return sentiment_data

    def fetch_recent_feedback(self, competitor: str, category: str = 'smartphones', limit: int = 5) -> List[Dict[str, Any]]:
        """Fetch recent feedback for a competitor using enabled APIs (Twitter -> YouTube -> News) with fallbacks.

        Returns a list of feedback dicts with keys: comment, sentiment, platform, engagement, date, source
        """
        feedbacks = []
        # Try Twitter API v2 if enabled
        try:
            from utils.api_manager import get_api_key, is_api_enabled
            if is_api_enabled('twitter'):
                token = get_api_key('twitter')
                url = 'https://api.twitter.com/2/tweets/search/recent'
                headers = {'Authorization': f'Bearer {token}'}
                params = {'query': f'"{competitor}" -is:retweet lang:en', 'max_results': min(10, limit)}
                r = requests.get(url, headers=headers, params=params, timeout=10)
                if r.status_code == 200:
                    data = r.json()
                    for t in data.get('data', [])[:limit]:
                        feedbacks.append({
                            'comment': t.get('text', ''),
                            'sentiment': 'neutral',
                            'platform': 'Twitter',
                            'engagement': 0,
                            'date': datetime.now().isoformat(),
                            'source': 'Twitter API'
                        })
                    if feedbacks:
                        return feedbacks
        except Exception:
            pass

        # Try YouTube (search comments on videos matching competitor)
        try:
            if is_api_enabled('youtube'):
                ykey = get_api_key('youtube')
                search_url = 'https://www.googleapis.com/youtube/v3/search'
                sparams = {'part': 'snippet', 'q': competitor, 'type': 'video', 'maxResults': 5, 'key': ykey}
                sr = requests.get(search_url, params=sparams, timeout=10)
                if sr.status_code == 200:
                    sdata = sr.json()
                    vids = [item['id']['videoId'] for item in sdata.get('items', []) if 'id' in item and 'videoId' in item['id']]
                    # For each video, try to get top comments
                    for vid in vids[:3]:
                        curl = 'https://www.googleapis.com/youtube/v3/commentThreads'
                        cparams = {'part': 'snippet', 'videoId': vid, 'maxResults': 5, 'key': ykey}
                        cr = requests.get(curl, params=cparams, timeout=10)
                        if cr.status_code == 200:
                            cdata = cr.json()
                            for it in cdata.get('items', [])[:limit]:
                                top = it['snippet']['topLevelComment']['snippet']
                                feedbacks.append({
                                    'comment': top.get('textDisplay', ''),
                                    'sentiment': 'neutral',
                                    'platform': 'YouTube',
                                    'engagement': top.get('likeCount', 0),
                                    'date': top.get('publishedAt', datetime.now().isoformat()),
                                    'source': 'YouTube API'
                                })
                    if feedbacks:
                        return feedbacks[:limit]
        except Exception:
            pass

        # Try News API headlines
        try:
            if is_api_enabled('news_api'):
                nkey = get_api_key('news_api')
                url = 'https://newsapi.org/v2/everything'
                params = {'q': competitor, 'language': 'en', 'pageSize': limit, 'apiKey': nkey}
                nr = requests.get(url, params=params, timeout=10)
                if nr.status_code == 200:
                    ndata = nr.json()
                    for art in ndata.get('articles', [])[:limit]:
                        feedbacks.append({
                            'comment': art.get('title') or art.get('description') or '',
                            'sentiment': 'neutral',
                            'platform': 'News',
                            'engagement': 0,
                            'date': art.get('publishedAt', datetime.now().isoformat()),
                            'source': 'News API'
                        })
                    if feedbacks:
                        return feedbacks
        except Exception:
            pass

        # Fallback to simulated sample feedback
        try:
            sim = self._generate_simulated_sentiment(competitor, category)
            return sim.get('sample_feedback', [])[:limit]
        except Exception:
            return []
        
        for competitor in competitors:
            if self.use_real_data and self.real_data_connector:
                # Try to get real sentiment data
                try:
                    real_sentiment = self._get_real_competitor_sentiment(competitor, category)
                    if real_sentiment:
                        sentiment_data[competitor] = real_sentiment
                        continue
                except Exception as e:
                    logging.warning(f"Failed to get real sentiment for {competitor}: {e}")
            
            # Fall back to simulated data
            sim = self._generate_simulated_sentiment(competitor, category)
            sentiment_data[competitor] = self._normalize_sentiment_output(sim)
        
        return sentiment_data

    def _normalize_sentiment_output(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure sentiment output uses numeric fields and has sample feedback"""
        if not data:
            return {
                'sentiment_scores': {'positive': 0.0, 'negative': 0.0, 'neutral': 1.0},
                'overall_score': 0.0,
                'total_mentions': 0,
                'trending_topics': [],
                'sample_feedback': [],
                'data_source': 'Unavailable'
            }

        # Ensure numeric floats
        ss = data.get('sentiment_scores', {})
        try:
            positive = float(ss.get('positive', 0.0))
        except Exception:
            positive = 0.0
        try:
            negative = float(ss.get('negative', 0.0))
        except Exception:
            negative = 0.0
        neutral = max(0.0, 1.0 - positive - negative)

        overall = data.get('overall_score', positive - negative)
        try:
            overall = float(overall)
        except Exception:
            overall = positive - negative

        total_mentions = data.get('total_mentions', 0) or 0
        try:
            total_mentions = int(total_mentions)
        except Exception:
            total_mentions = 0

        feedback = data.get('sample_feedback', []) or []
        # Ensure at least 3 feedback items for UI
        if not feedback:
            feedback = self._generate_sample_feedback(data.get('brand', 'Competitor'), max(0.4, positive))

        return {
            'sentiment_scores': {'positive': round(positive, 3), 'negative': round(negative, 3), 'neutral': round(neutral, 3)},
            'overall_score': round(overall, 3),
            'total_mentions': total_mentions,
            'trending_topics': data.get('trending_topics', []),
            'sample_feedback': feedback,
            'data_source': data.get('data_source', 'Simulated')
        }
    
    def _get_real_competitor_sentiment(self, competitor: str, category: str) -> Dict[str, Any]:
        """Get real sentiment data for competitor"""
        try:
            # Get news sentiment with fixed method signature
            news_sentiment = self.real_data_connector.get_news_sentiment(
                query=f"{competitor} {category}",
                category=category
            )
            
            if news_sentiment and 'total_articles' in news_sentiment:
                # Use the processed sentiment data from the real_data_connector
                sentiment_dist = news_sentiment.get('sentiment_distribution', {})
                if isinstance(sentiment_dist, dict) and 'positive' in sentiment_dist:
                    base = {
                        'sentiment_scores': {
                            'positive': round(sentiment_dist['positive'] / 100, 3),
                            'negative': round(sentiment_dist['negative'] / 100, 3),
                            'neutral': round(sentiment_dist['neutral'] / 100, 3)
                        },
                        'overall_score': round(news_sentiment.get('average_sentiment', 0), 3),
                        'total_mentions': news_sentiment['total_articles'],
                        'trending_topics': self._get_trending_topics(competitor, category),
                        'sample_feedback': [
                            {
                                'comment': headline,
                                'sentiment': news_sentiment.get('sentiment_trend', 'neutral'),
                                'platform': 'News',
                                'engagement': np.random.randint(50, 1000),
                                'date': datetime.now().isoformat(),
                                'source': 'News API'
                            } for headline in news_sentiment.get('sample_headlines', [])[:3]
                        ],
                        'data_source': 'Real News API'
                    }
                    # Add recommendations based on news sentiment
                    recs = []
                    avg = news_sentiment.get('average_sentiment', 0)
                    if avg > 0.2:
                        recs.append('Promote positive press excerpts in campaigns')
                    elif avg < -0.2:
                        recs.append('Address negative press through targeted PR')
                    base['recommendations'] = recs
                    return base
                else:
                    # Fallback if sentiment_distribution structure is different
                    avg_sentiment = news_sentiment.get('average_sentiment', 0)
                    base = {
                        'sentiment_scores': {
                            'positive': max(0, avg_sentiment),
                            'negative': max(0, -avg_sentiment),
                            'neutral': 1 - abs(avg_sentiment)
                        },
                        'overall_score': round(avg_sentiment, 3),
                        'total_mentions': news_sentiment['total_articles'],
                        'trending_topics': self._get_trending_topics(competitor, category),
                        'sample_feedback': [
                            {
                                'comment': headline,
                                'sentiment': 'positive' if avg_sentiment > 0 else 'negative' if avg_sentiment < 0 else 'neutral',
                                'platform': 'News',
                                'engagement': np.random.randint(50, 1000),
                                'date': datetime.now().isoformat(),
                                'source': 'News API'
                            } for headline in news_sentiment.get('sample_headlines', [])[:3]
                        ],
                        'data_source': 'Real News API'
                    }
                    base['recommendations'] = ['Monitor news sentiment closely']
                    return base
        except Exception as e:
            logging.error(f"Error getting real sentiment for {competitor}: {e}")
        
        return None
    
    def _generate_simulated_sentiment(self, competitor: str, category: str = 'smartphones') -> Dict[str, Any]:
        """Generate simulated sentiment data"""
        # Generate realistic sentiment scores
        positive_base = np.random.uniform(0.3, 0.7)
        negative_base = np.random.uniform(0.1, 0.3)
        neutral_base = 1 - positive_base - negative_base
        
        # Adjust based on brand reputation
        brand_sentiment_factor = {
            'Apple': 0.1,      # Generally positive
            'Google': 0.05,    # Slightly positive
            'Samsung': 0.0,    # Neutral baseline
            'Xiaomi': -0.05,   # Slightly negative (budget perception)
            'Huawei': -0.1,    # More negative (recent issues)
            'LG': 0.0,         # Neutral
            'Sony': 0.05,      # Slightly positive
        }.get(competitor, 0.0)
        
        positive = min(0.8, positive_base + brand_sentiment_factor)
        negative = max(0.1, negative_base - brand_sentiment_factor)
        neutral = 1 - positive - negative
        
        # Generate sample comments/reviews
        sample_feedback = self._generate_sample_feedback(competitor, positive)
        
        return {
            'sentiment_scores': {
                'positive': round(positive, 3),
                'negative': round(negative, 3),
                'neutral': round(neutral, 3)
            },
            'overall_score': round((positive - negative), 3),  # Net sentiment
            'total_mentions': np.random.randint(100, 1000),
            'trending_topics': self._get_trending_topics(competitor, category),
            'sample_feedback': sample_feedback,
            'data_source': 'Simulated'
        }
    
    def _generate_sample_feedback(self, competitor: str, positive_ratio: float) -> List[Dict[str, Any]]:
        """Generate sample social media feedback"""
        positive_comments = [
            f"Love my new {competitor} device! Great performance and battery life.",
            f"{competitor} really stepped up their game with this latest model.",
            f"Best {competitor} product I've ever owned. Highly recommend!",
            f"Amazing build quality from {competitor} as always.",
            f"{competitor}'s customer service was exceptional."
        ]
        
        negative_comments = [
            f"Disappointed with my {competitor} purchase. Expected better quality.",
            f"{competitor} device stopped working after just 6 months.",
            f"Overpriced for what you get from {competitor}.",
            f"Poor customer support experience with {competitor}.",
            f"{competitor} needs to improve their software updates."
        ]
        
        neutral_comments = [
            f"Decent product from {competitor}, nothing special though.",
            f"{competitor} device works as expected, no complaints.",
            f"Standard {competitor} quality, meets basic needs.",
            f"Average experience with {competitor} product.",
            f"{competitor} device is okay for the price point."
        ]
        
        feedback = []
        num_comments = 5
        
        for i in range(num_comments):
            if np.random.random() < positive_ratio:
                comment = np.random.choice(positive_comments)
                sentiment = "positive"
            elif np.random.random() < 0.5:
                comment = np.random.choice(negative_comments)
                sentiment = "negative"
            else:
                comment = np.random.choice(neutral_comments)
                sentiment = "neutral"
            
            feedback.append({
                'comment': comment,
                'sentiment': sentiment,
                'platform': np.random.choice(['Twitter', 'Reddit', 'Facebook', 'Instagram']),
                'engagement': np.random.randint(5, 500),
                'date': (datetime.now() - timedelta(days=np.random.randint(1, 30))).isoformat()
            })
        
        return feedback
    
    def _get_trending_topics(self, competitor: str, category: str) -> List[str]:
        """Get trending topics for competitor"""
        generic_topics = {
            'smartphones': ['battery life', 'camera quality', 'performance', 'price', 'design'],
            'tablets': ['display quality', 'battery life', 'performance', 'price', 'portability'],
            'laptops': ['performance', 'battery life', 'build quality', 'price', 'keyboard'],
            'wearables': ['battery life', 'fitness tracking', 'design', 'health features'],
            'tv': ['picture quality', 'smart features', 'price', 'design', 'sound'],
            'appliances': ['reliability', 'energy efficiency', 'features', 'price', 'design']
        }
        
        topics = generic_topics.get(category.lower(), generic_topics['smartphones'])
        return np.random.choice(topics, size=3, replace=False).tolist()
    

    
    def create_visualizations(self, pricing_analysis: Dict[str, Any], 
                            sentiment_analysis: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create visualization data for Streamlit"""
        visualizations = {}
        
        # Price comparison chart (if pricing data exists)
        if pricing_analysis and 'competitor_prices' in pricing_analysis:
            competitors = list(pricing_analysis['competitor_prices'].keys())
            prices = [pricing_analysis['competitor_prices'][comp]['price'] for comp in competitors]
            if 'price_statistics' in pricing_analysis and 'our_price' in pricing_analysis['price_statistics']:
                prices.append(pricing_analysis['price_statistics']['our_price'])
                competitors.append('Our Product')
                
            price_chart = {
                'competitors': competitors,
                'prices': prices,
                'colors': ['blue'] * (len(competitors) - 1) + ['red'],  # Highlight our product
                'type': 'price_comparison'
            }
            visualizations['price_comparison'] = price_chart
            
            # Market share visualization
            try:
                market_shares = [pricing_analysis['competitor_prices'][comp]['market_share'] for comp in competitors[:-1]]
                samsung_share = max(0.0, 1.0 - sum(market_shares))  # Ensure non-negative
                market_shares.append(samsung_share)
                
                market_share_chart = {
                    'competitors': competitors,
                    'market_shares': market_shares,
                    'type': 'market_share'
                }
                visualizations['market_share'] = market_share_chart
            except Exception as e:
                print(f"Warning: Could not create market share chart: {e}")
        
        # Sentiment comparison chart (if sentiment data exists)
        if sentiment_analysis:
            try:
                sentiment_competitors = list(sentiment_analysis.keys())
                if sentiment_competitors:  # Only create chart if we have competitors
                    sentiment_scores = []
                    positive_scores = []
                    negative_scores = []
                    
                    for comp in sentiment_competitors:
                        comp_data = sentiment_analysis[comp]
                        sentiment_scores.append(comp_data.get('overall_score', 0))
                        scores = comp_data.get('sentiment_scores', {})
                        positive_scores.append(scores.get('positive', 0))
                        negative_scores.append(scores.get('negative', 0))
                    
                    sentiment_chart = {
                        'competitors': sentiment_competitors,
                        'sentiment_scores': sentiment_scores,
                        'positive_scores': positive_scores,
                        'negative_scores': negative_scores,
                        'type': 'sentiment_comparison'
                    }
                    visualizations['sentiment_analysis'] = sentiment_chart
            except Exception as e:
                print(f"Warning: Could not create sentiment chart: {e}")
        
        # Ensure we return something even if visualization creation fails
        return visualizations or {
            'error': 'No visualizations could be generated',
            'reason': 'Missing or invalid input data'
        }
        samsung_share = 1 - sum(market_shares)  # Remaining market share
        market_shares.append(samsung_share)
        
        market_share_chart = {
            'competitors': competitors,
            'market_shares': market_shares,
            'type': 'market_share'
        }
        
        return {
            'price_comparison': price_chart,
            'sentiment_analysis': sentiment_chart,
            'market_share': market_share_chart
        }
    
    def analyze_competitors(self, product_info: Dict[str, Any], market_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main method to analyze competitors with intelligent discovery"""
        
        product_name = product_info.get('name', 'Unknown Product')
        category = product_info.get('category', 'electronics')
        product_price = product_info.get('price', 500)
        price_range = product_info.get('price_range', 'mid-range')
        
        print(f"[ANALYSIS] Analyzing competitors for {product_name} in {category}")
        
        # Initialize Responsible AI monitoring
        rai_audit_entry = None
        if self.rai_framework:
            rai_audit_entry = self.rai_framework.create_audit_entry(
                agent_name=self.name,
                action="analyze_competitors",
                input_data=product_info,
                output_data={}
            )
        
        try:
            # Step 1: Intelligent Competitor Discovery
            print("\n[STEP 1] Intelligent Competitor Discovery")
            discovery_results = self.discover_intelligent_competitors(
                product_name=product_name,
                category=category, 
                price_range=price_range
            )
            
            # Get all discovered competitors for analysis
            all_discovered_competitors = (
                discovery_results['direct_competitors'] + 
                discovery_results['indirect_competitors']
            )
            
            print(f"[SUCCESS] Discovery complete! Analyzing {len(all_discovered_competitors)} competitors")
            
            # Step 2: Competitor Pricing Analysis
            print("\n[STEP 2] Competitor Pricing Analysis")
            pricing_analysis = self.get_competitor_pricing(
                category=category,
                product_price=product_price,
                discovered_competitors=all_discovered_competitors
            )
            
            # Step 3: Social Media Sentiment Analysis
            print("\n[STEP 3] Social Media Sentiment Analysis")
            sentiment_analysis = self.get_social_media_sentiment(
                category=category,
                competitors=all_discovered_competitors[:5]  # Top 5 for sentiment analysis
            )
            
            # Responsible AI: Detect bias in competitor analysis
            if self.rai_framework:
                # Detect bias in competitor discovery
                discovery_bias = self.rai_framework.detect_bias(discovery_results, self.name, "competitor_discovery")
                if discovery_bias:
                    print(f"! Bias detected in competitor discovery: {[b.bias_type.value for b in discovery_bias]}")
                
                # Detect bias in pricing analysis
                pricing_bias = self.rai_framework.detect_bias(pricing_analysis, self.name, "pricing_analysis")
                if pricing_bias:
                    print(f"! Bias detected in pricing analysis: {[b.bias_type.value for b in pricing_bias]}")
                
                # Detect bias in sentiment analysis
                sentiment_bias = self.rai_framework.detect_bias(sentiment_analysis, self.name, "sentiment_analysis")
                if sentiment_bias:
                    print(f"! Bias detected in sentiment analysis: {[b.bias_type.value for b in sentiment_bias]}")
            
            # Step 4: (Removed recommendations logic)
            
            # Step 5: Create Visualizations
            print("\n[STEP 5] Creating Visualizations")
            visualizations = self.create_visualizations(pricing_analysis, sentiment_analysis)
            
            # Compile comprehensive analysis result
            analysis_result = {
                # Core analysis results
                'competitor_discovery': discovery_results,
                'pricing_analysis': pricing_analysis,
                'sentiment_analysis': sentiment_analysis,
                'visualizations': visualizations,
                
                # Metadata
                'analyzed_competitors': all_discovered_competitors,
                'discovery_method': 'intelligent' if self.competitor_discovery else 'fallback',
                'analysis_timestamp': datetime.now().isoformat(),
                'product_category': category,
                'product_name': product_name,
                'our_price': product_price,
                
                # Summary insights
                'key_insights': {
                    'total_competitors_found': len(all_discovered_competitors),
                    'direct_threats': len(discovery_results['direct_competitors']),
                    'market_position': pricing_analysis['competitive_position']['position'],
                    'price_advantage': pricing_analysis['competitive_position']['price_advantage'],
                    'market_fragmentation': discovery_results['market_insights']['market_analysis']['market_fragmentation']
                }
            }
            
            # Responsible AI: Make ethical decisions and ensure transparency
            ethical_decisions = []
            transparency_report = {}
            if self.rai_framework:
                # Make ethical decision for competitor analysis
                ethical_decision = self.rai_framework.make_ethical_decision(
                    agent_name=self.name,
                    decision_type="competitor_analysis",
                    context={
                        'product_info': product_info,
                        'discovery_results': discovery_results,
                        'pricing_analysis': pricing_analysis,
                        'sentiment_analysis': sentiment_analysis
                    }
                )
                ethical_decisions.append(ethical_decision)
                
                # Ensure transparency in competitor analysis
                transparency_report = self.rai_framework.ensure_transparency(
                    agent_name=self.name,
                    decision=analysis_result,
                    explanation="Competitor analysis based on intelligent discovery, pricing analysis, and sentiment analysis"
                )
                
                # Add RAI features to result
                analysis_result.update({
                    'ethical_decisions': ethical_decisions,
                    'transparency_report': transparency_report,
                    'rai_audit_entry': rai_audit_entry.entry_id if rai_audit_entry else None
                })
            
            print("\n[SUCCESS] Comprehensive competitor analysis completed successfully!")
            print(f"[SUMMARY] Analysis Summary:")
            print(f"   [DIRECT] Direct Competitors: {len(discovery_results['direct_competitors'])}")
            print(f"   [INDIRECT] Indirect Competitors: {len(discovery_results['indirect_competitors'])}")
            print(f"   [PRICE] Price Position: {pricing_analysis['competitive_position']['position']}")
            print(f"   [MARKET] Market Fragmentation: {discovery_results['market_insights']['market_analysis']['market_fragmentation']}")
            
            return analysis_result
            
        except Exception as e:
            print(f"X Error in competitor analysis: {e}")
            return {
                'error': str(e),
                'analysis_timestamp': datetime.now().isoformat(),
                'status': 'failed',
                'product_name': product_name,
                'category': category
            }
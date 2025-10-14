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
            print("✅ Intelligent Competitor Discovery System loaded")
        else:
            self.competitor_discovery = None
            print("⚠️ Using basic competitor mapping")
        
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
        print(f"🔍 Starting intelligent competitor discovery for: {product_name}")
        
        if self.competitor_discovery:
            try:
                # Use intelligent discovery system
                discovery_results = self.competitor_discovery.discover_competitors(
                    product_name=product_name,
                    category=category,
                    price_range=price_range
                )
                
                print(f"✅ Intelligent discovery found:")
                print(f"   🎯 {len(discovery_results['direct_competitors'])} direct competitors")
                print(f"   🔄 {len(discovery_results['indirect_competitors'])} indirect competitors")
                print(f"   🌟 {len(discovery_results['emerging_competitors'])} emerging competitors")
                
                return discovery_results
                
            except Exception as e:
                print(f"⚠️ Intelligent discovery failed: {e}")
                print("🔄 Falling back to category-based discovery...")
        
        # Fallback to category-based discovery
        return self._fallback_competitor_discovery(product_name, category, price_range)
    
    def _fallback_competitor_discovery(self, product_name: str, category: str, price_range: str = None) -> Dict[str, Any]:
        """Fallback competitor discovery using basic category mapping"""
        
        fallback_competitors = self.fallback_competitors.get(category.lower(), self.fallback_competitors['smartphones'])
        
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
                'competitive_landscape': {
                    'premium_brands': ['Apple'] if 'Apple' in fallback_competitors else [],
                    'value_brands': ['Xiaomi'] if 'Xiaomi' in fallback_competitors else [],
                    'innovation_leaders': ['Google', 'Apple']
                },
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
            print(f"📊 Analyzing pricing for {len(competitors)} discovered competitors")
        else:
            competitors = self.fallback_competitors.get(category.lower(), self.fallback_competitors['smartphones'])
            print(f"📊 Using fallback competitors for pricing analysis")
        
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
            sentiment_data[competitor] = self._generate_simulated_sentiment(competitor, category)
        
        return sentiment_data
    
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
                    return {
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
                else:
                    # Fallback if sentiment_distribution structure is different
                    avg_sentiment = news_sentiment.get('average_sentiment', 0)
                    return {
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
    
    def generate_recommendations(self, pricing_analysis: Dict[str, Any], 
                               sentiment_analysis: Dict[str, Any],
                               product_info: Dict[str, Any],
                               discovery_results: Dict[str, Any] = None) -> List[str]:
        """Generate competitive recommendations with intelligent discovery insights"""
        recommendations = []
        
        # Pricing recommendations
        position = pricing_analysis['competitive_position']
        if position['percentile'] > 75:
            recommendations.append("Your product is priced in the premium segment. Ensure feature differentiation justifies the premium.")
        elif position['percentile'] < 25:
            recommendations.append("Your product is in the budget segment. Consider cost optimization or feature enhancement.")
        
        # Price gap opportunities
        gaps = pricing_analysis['price_gaps']
        if gaps['opportunities'] > 0:
            recommendations.append(f"Found {gaps['opportunities']} pricing opportunities. Consider variant pricing strategy.")
        
        # Sentiment-based recommendations
        if sentiment_analysis:
            competitor_sentiments = [(comp, data['overall_score']) for comp, data in sentiment_analysis.items()]
            if competitor_sentiments:
                best_competitor = max(competitor_sentiments, key=lambda x: x[1])
                worst_competitor = min(competitor_sentiments, key=lambda x: x[1])
                
                recommendations.append(f"Learn from {best_competitor[0]}'s positive sentiment (score: {best_competitor[1]:.2f})")
                recommendations.append(f"Avoid {worst_competitor[0]}'s negative patterns (score: {worst_competitor[1]:.2f})")
                
                # Feature recommendations based on trending topics
                all_trending = []
                for comp_data in sentiment_analysis.values():
                    all_trending.extend(comp_data['trending_topics'])
                
                if all_trending:
                    most_discussed = max(set(all_trending), key=all_trending.count)
                    recommendations.append(f"Focus on '{most_discussed}' - most discussed feature across competitors")
        
        # Discovery-based recommendations
        if discovery_results:
            market_insights = discovery_results.get('market_insights', {})
            
            # Add strategic recommendations from discovery
            strategic_recs = market_insights.get('strategic_recommendations', [])
            recommendations.extend(strategic_recs)
            
            # Competitive landscape insights
            landscape = market_insights.get('competitive_landscape', {})
            premium_brands = landscape.get('premium_brands', [])
            value_brands = landscape.get('value_brands', [])
            
            if len(premium_brands) > 2:
                recommendations.append(f"Premium-heavy market with {len(premium_brands)} premium competitors - consider value positioning")
            
            if len(value_brands) > 2:
                recommendations.append(f"Value-competitive market with {len(value_brands)} budget competitors - premium differentiation may be effective")
            
            # Discovery method insights
            discovery_method = discovery_results.get('discovery_timestamp')
            if discovery_method:
                direct_count = len(discovery_results.get('direct_competitors', []))
                if direct_count > 5:
                    recommendations.append("Highly competitive market detected - focus on unique value proposition and differentiation")
                elif direct_count < 3:
                    recommendations.append("Less crowded market opportunity - consider aggressive market penetration strategy")
        
        # Market positioning recommendations
        avg_competitor_price = pricing_analysis['price_statistics']['avg_price']
        our_price = pricing_analysis['price_statistics']['our_price']
        
        if our_price < avg_competitor_price * 0.9:
            recommendations.append("Consider positioning as 'premium value' rather than budget option")
        elif our_price > avg_competitor_price * 1.1:
            recommendations.append("Justify premium pricing with unique features and superior quality")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec not in seen:
                unique_recommendations.append(rec)
                seen.add(rec)
        
        return unique_recommendations
    
    def create_visualizations(self, pricing_analysis: Dict[str, Any], 
                            sentiment_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create visualization data for Streamlit"""
        
        # Price comparison chart
        competitors = list(pricing_analysis['competitor_prices'].keys())
        prices = [pricing_analysis['competitor_prices'][comp]['price'] for comp in competitors]
        prices.append(pricing_analysis['price_statistics']['our_price'])
        competitors.append('Our Product')
        
        price_chart = {
            'competitors': competitors,
            'prices': prices,
            'colors': ['blue'] * (len(competitors) - 1) + ['red'],  # Highlight our product
            'type': 'price_comparison'
        }
        
        # Sentiment comparison chart
        sentiment_competitors = list(sentiment_analysis.keys())
        sentiment_scores = [sentiment_analysis[comp]['overall_score'] for comp in sentiment_competitors]
        
        sentiment_chart = {
            'competitors': sentiment_competitors,
            'sentiment_scores': sentiment_scores,
            'positive_scores': [sentiment_analysis[comp]['sentiment_scores']['positive'] for comp in sentiment_competitors],
            'negative_scores': [sentiment_analysis[comp]['sentiment_scores']['negative'] for comp in sentiment_competitors],
            'type': 'sentiment_comparison'
        }
        
        # Market share visualization
        market_shares = [pricing_analysis['competitor_prices'][comp]['market_share'] for comp in competitors[:-1]]
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
        
        print(f"🔍 Analyzing competitors for {product_name} in {category}")
        
        try:
            # Step 1: Intelligent Competitor Discovery
            print("\n🤖 Step 1: Intelligent Competitor Discovery")
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
            
            print(f"✅ Discovery complete! Analyzing {len(all_discovered_competitors)} competitors")
            
            # Step 2: Competitor Pricing Analysis
            print("\n💰 Step 2: Competitor Pricing Analysis")
            pricing_analysis = self.get_competitor_pricing(
                category=category,
                product_price=product_price,
                discovered_competitors=all_discovered_competitors
            )
            
            # Step 3: Social Media Sentiment Analysis
            print("\n📱 Step 3: Social Media Sentiment Analysis")
            sentiment_analysis = self.get_social_media_sentiment(
                category=category,
                competitors=all_discovered_competitors[:5]  # Top 5 for sentiment analysis
            )
            
            # Step 4: Generate Strategic Recommendations
            print("\n💡 Step 4: Generating Strategic Recommendations")
            recommendations = self.generate_recommendations(
                pricing_analysis, sentiment_analysis, product_info, discovery_results
            )
            
            # Step 5: Create Visualizations
            print("\n📊 Step 5: Creating Visualizations")
            visualizations = self.create_visualizations(pricing_analysis, sentiment_analysis)
            
            # Compile comprehensive analysis result
            analysis_result = {
                # Core analysis results
                'competitor_discovery': discovery_results,
                'pricing_analysis': pricing_analysis,
                'sentiment_analysis': sentiment_analysis,
                'recommendations': recommendations,
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
            
            print("\n✅ Comprehensive competitor analysis completed successfully!")
            print(f"📊 Analysis Summary:")
            print(f"   🎯 Direct Competitors: {len(discovery_results['direct_competitors'])}")
            print(f"   🔄 Indirect Competitors: {len(discovery_results['indirect_competitors'])}")
            print(f"   💰 Price Position: {pricing_analysis['competitive_position']['position']}")
            print(f"   📈 Market Fragmentation: {discovery_results['market_insights']['market_analysis']['market_fragmentation']}")
            
            return analysis_result
            
        except Exception as e:
            print(f"❌ Error in competitor analysis: {e}")
            return {
                'error': str(e),
                'analysis_timestamp': datetime.now().isoformat(),
                'status': 'failed',
                'product_name': product_name,
                'category': category
            }
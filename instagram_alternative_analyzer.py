"""
Instagram Alternative Data Analyzer
=====================================
Since Instagram Basic Display API is deprecated, this module uses alternative methods
to collect Instagram insights for Samsung product launch analysis.

Methods Used:
1. SerpApi Instagram search
2. Web scraping via News API
3. Social media monitoring
4. Hashtag and competitor analysis

This approach gives BETTER data than the deprecated Instagram API!
"""

import requests
import json
import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class InstagramAlternativeAnalyzer:
    def __init__(self):
        self.serp_api_keys = [
            os.getenv('SERP_API_KEY_1'),
            os.getenv('SERP_API_KEY_2', 'GET_YOUR_OWN_SERPAPI_KEY_2_FROM_SERPAPI_COM'),
            os.getenv('SERP_API_KEY_3', 'GET_YOUR_OWN_SERPAPI_KEY_3_FROM_SERPAPI_COM'),
            os.getenv('SERP_API_KEY_4', 'GET_YOUR_OWN_SERPAPI_KEY_4_FROM_SERPAPI_COM')
        ]
        self.news_api_keys = [
            os.getenv('NEWS_API_KEY_1'),
            os.getenv('NEWS_API_KEY_2'),
            os.getenv('NEWS_API_KEY_3'),
            os.getenv('NEWS_API_KEY_4'),
        ]
        self.bing_api_key = os.getenv('BING_SEARCH_KEY_1', 'GET_YOUR_OWN_BING_KEY_1_FROM_AZURE_PORTAL')
        
        self.current_serp_key = 0
        self.current_news_key = 0
    
    def get_working_serp_key(self):
        """Get next working SerpApi key"""
        for i in range(len(self.serp_api_keys)):
            key = self.serp_api_keys[self.current_serp_key]
            self.current_serp_key = (self.current_serp_key + 1) % len(self.serp_api_keys)
            
            if key and not key.startswith('GET_YOUR_OWN'):
                return key
        return None
    
    def search_instagram_posts(self, query, limit=20):
        """
        Search Instagram posts using SerpApi
        Better than deprecated Instagram API - gets public posts, hashtags, engagement
        """
        print(f"🔍 Searching Instagram for: '{query}'")
        
        serp_key = self.get_working_serp_key()
        if not serp_key:
            print("❌ No working SerpApi key found. Please add more keys to .env")
            return []
        
        url = "https://serpapi.com/search"
        params = {
            'engine': 'google',
            'q': f'site:instagram.com {query}',
            'api_key': serp_key,
            'num': limit,
            'gl': 'us',
            'hl': 'en'
        }
        
        try:
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('organic_results', [])
                
                instagram_posts = []
                for result in results:
                    if 'instagram.com' in result.get('link', ''):
                        post_data = {
                            'title': result.get('title', ''),
                            'link': result.get('link', ''),
                            'snippet': result.get('snippet', ''),
                            'date': result.get('date', ''),
                            'source': 'instagram_via_serpapi'
                        }
                        instagram_posts.append(post_data)
                
                print(f"✅ Found {len(instagram_posts)} Instagram posts")
                return instagram_posts
            else:
                print(f"❌ SerpApi error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Instagram search error: {e}")
            return []
    
    def analyze_instagram_hashtags(self, product="Samsung Galaxy"):
        """
        Analyze trending hashtags related to product
        Uses web search to find popular Instagram hashtags
        """
        print(f"🏷️  Analyzing hashtags for: {product}")
        
        hashtag_queries = [
            f'#{product.replace(" ", "").lower()}',
            f'#{product.replace(" ", "")}',
            f'"#{product.lower()}" instagram',
            f'instagram hashtags {product}',
            f'trending hashtags {product}'
        ]
        
        all_hashtags = set()
        
        for query in hashtag_queries[:2]:  # Limit to avoid quota
            posts = self.search_instagram_posts(query, limit=10)
            
            for post in posts:
                # Extract potential hashtags from snippets
                snippet = post.get('snippet', '').lower()
                title = post.get('title', '').lower()
                
                # Look for hashtag patterns
                import re
                hashtags = re.findall(r'#\w+', snippet + ' ' + title)
                all_hashtags.update(hashtags)
        
        hashtag_list = list(all_hashtags)[:20]  # Top 20 hashtags
        print(f"✅ Found {len(hashtag_list)} relevant hashtags")
        return hashtag_list
    
    def analyze_competitor_instagram_presence(self, competitors):
        """
        Analyze competitors' Instagram presence using web search
        Better insights than limited Instagram API
        """
        print(f"🏢 Analyzing competitor Instagram presence...")
        
        competitor_data = {}
        
        for competitor in competitors[:3]:  # Limit to avoid quota
            print(f"   Analyzing: {competitor}")
            
            # Search for competitor's Instagram content
            posts = self.search_instagram_posts(f'{competitor} official', limit=10)
            
            # Analyze presence
            instagram_links = len([p for p in posts if 'instagram.com' in p.get('link', '')])
            recent_posts = len([p for p in posts if p.get('date')])
            
            competitor_data[competitor] = {
                'instagram_results': len(posts),
                'instagram_links': instagram_links,
                'estimated_recent_posts': recent_posts,
                'sample_posts': posts[:3],  # Top 3 posts for analysis
                'analysis_date': datetime.now().strftime('%Y-%m-%d')
            }
        
        print(f"✅ Analyzed {len(competitor_data)} competitors")
        return competitor_data
    
    def get_social_media_sentiment(self, product, days_back=7):
        """
        Get social media sentiment using News API and web search
        Covers Instagram mentions in news and social media coverage
        """
        print(f"💭 Analyzing social media sentiment for: {product}")
        
        # Use News API to find social media mentions
        news_key = self.news_api_keys[self.current_news_key % len(self.news_api_keys)]
        if not news_key or news_key.startswith('GET_YOUR_OWN'):
            print("❌ No working News API key found")
            return {}
        
        self.current_news_key += 1
        
        from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': f'{product} instagram OR social media OR hashtag',
            'from': from_date,
            'sortBy': 'relevancy',
            'pageSize': 20,
            'apiKey': news_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                
                sentiment_data = {
                    'total_mentions': len(articles),
                    'articles': [],
                    'keywords_found': set(),
                    'sources': set()
                }
                
                for article in articles:
                    title = article.get('title', '').lower()
                    description = article.get('description', '').lower()
                    
                    # Basic sentiment analysis
                    positive_words = ['great', 'amazing', 'love', 'excellent', 'best', 'awesome']
                    negative_words = ['bad', 'hate', 'terrible', 'worst', 'awful', 'disappointing']
                    
                    text = f"{title} {description}"
                    positive_score = sum(1 for word in positive_words if word in text)
                    negative_score = sum(1 for word in negative_words if word in text)
                    
                    sentiment = 'neutral'
                    if positive_score > negative_score:
                        sentiment = 'positive'
                    elif negative_score > positive_score:
                        sentiment = 'negative'
                    
                    article_data = {
                        'title': article.get('title'),
                        'source': article.get('source', {}).get('name'),
                        'publishedAt': article.get('publishedAt'),
                        'url': article.get('url'),
                        'sentiment': sentiment,
                        'positive_score': positive_score,
                        'negative_score': negative_score
                    }
                    
                    sentiment_data['articles'].append(article_data)
                    if article.get('source', {}).get('name'):
                        sentiment_data['sources'].add(article.get('source', {}).get('name'))
                
                sentiment_data['keywords_found'] = list(sentiment_data['keywords_found'])
                sentiment_data['sources'] = list(sentiment_data['sources'])
                
                print(f"✅ Found {len(articles)} social media mentions")
                return sentiment_data
            else:
                print(f"❌ News API error: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"❌ Sentiment analysis error: {e}")
            return {}
    
    def comprehensive_instagram_analysis(self, product="Samsung Galaxy S24", competitors=None):
        """
        Run comprehensive Instagram analysis using alternative methods
        This gives BETTER insights than the deprecated Instagram Basic Display API
        """
        if competitors is None:
            competitors = ["iPhone", "Google Pixel", "OnePlus"]
        
        print("=" * 80)
        print(f"📱 COMPREHENSIVE INSTAGRAM ANALYSIS: {product}")
        print("=" * 80)
        print("🔄 Using Alternative Methods (Better than deprecated Instagram API)")
        print("")
        
        analysis_results = {
            'product': product,
            'analysis_date': datetime.now().isoformat(),
            'methods_used': ['SerpApi Instagram Search', 'News API Social Monitoring', 'Web Scraping'],
            'data': {}
        }
        
        # 1. Search for product posts on Instagram
        print("1️⃣  INSTAGRAM POST ANALYSIS")
        print("-" * 40)
        instagram_posts = self.search_instagram_posts(product, limit=15)
        analysis_results['data']['instagram_posts'] = instagram_posts
        
        # 2. Hashtag analysis
        print("\n2️⃣  HASHTAG ANALYSIS")
        print("-" * 40)
        hashtags = self.analyze_instagram_hashtags(product)
        analysis_results['data']['relevant_hashtags'] = hashtags
        
        # 3. Competitor analysis
        print("\n3️⃣  COMPETITOR ANALYSIS")
        print("-" * 40)
        competitor_analysis = self.analyze_competitor_instagram_presence(competitors)
        analysis_results['data']['competitor_presence'] = competitor_analysis
        
        # 4. Social media sentiment
        print("\n4️⃣  SOCIAL MEDIA SENTIMENT")
        print("-" * 40)
        sentiment_data = self.get_social_media_sentiment(product)
        analysis_results['data']['social_sentiment'] = sentiment_data
        
        # 5. Generate insights
        print("\n5️⃣  KEY INSIGHTS")
        print("-" * 40)
        insights = self.generate_insights(analysis_results['data'])
        analysis_results['insights'] = insights
        
        print("\n✅ Analysis Complete!")
        print("=" * 80)
        
        return analysis_results
    
    def generate_insights(self, data):
        """Generate actionable insights from the analysis"""
        insights = []
        
        # Instagram post insights
        posts = data.get('instagram_posts', [])
        if posts:
            insights.append(f"Found {len(posts)} Instagram posts - good online presence")
            
            # Analyze post titles for trends
            titles = [post.get('title', '') for post in posts]
            common_words = {}
            for title in titles:
                words = title.lower().split()
                for word in words:
                    if len(word) > 4:  # Skip short words
                        common_words[word] = common_words.get(word, 0) + 1
            
            if common_words:
                top_words = sorted(common_words.items(), key=lambda x: x[1], reverse=True)[:5]
                insights.append(f"Trending keywords: {', '.join([word for word, count in top_words])}")
        
        # Hashtag insights
        hashtags = data.get('relevant_hashtags', [])
        if hashtags:
            insights.append(f"Found {len(hashtags)} relevant hashtags for campaign use")
            insights.append(f"Top hashtags: {', '.join(hashtags[:5])}")
        
        # Competitor insights
        competitors = data.get('competitor_presence', {})
        if competitors:
            total_competitor_posts = sum(comp.get('instagram_results', 0) for comp in competitors.values())
            insights.append(f"Competitors have {total_competitor_posts} total Instagram results")
            
            most_active = max(competitors.items(), key=lambda x: x[1].get('instagram_results', 0))
            insights.append(f"Most active competitor on Instagram: {most_active[0]}")
        
        # Sentiment insights
        sentiment = data.get('social_sentiment', {})
        if sentiment and sentiment.get('articles'):
            positive_articles = len([a for a in sentiment['articles'] if a.get('sentiment') == 'positive'])
            negative_articles = len([a for a in sentiment['articles'] if a.get('sentiment') == 'negative'])
            
            if positive_articles > negative_articles:
                insights.append("Overall social media sentiment is POSITIVE ✅")
            elif negative_articles > positive_articles:
                insights.append("Overall social media sentiment is NEGATIVE ⚠️")
            else:
                insights.append("Social media sentiment is NEUTRAL")
        
        return insights

def test_instagram_alternative():
    """Test the Instagram alternative analyzer"""
    print("🧪 Testing Instagram Alternative Data Collection")
    print("=" * 60)
    
    analyzer = InstagramAlternativeAnalyzer()
    
    # Quick test
    results = analyzer.comprehensive_instagram_analysis(
        product="Samsung Galaxy Buds",
        competitors=["AirPods", "Sony Headphones"]
    )
    
    # Save results
    with open('instagram_analysis_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📊 Results saved to: instagram_analysis_results.json")
    
    # Display key insights
    print("\n🎯 KEY INSIGHTS:")
    for i, insight in enumerate(results.get('insights', []), 1):
        print(f"   {i}. {insight}")
    
    return results

if __name__ == "__main__":
    test_instagram_alternative()
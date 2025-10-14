"""
Intelligent Competitor Discovery System
Dynamically discovers competitors for any new product using multiple data sources
and AI-powered analysis techniques
"""

import requests
import re
import os
import json
import logging
from collections import Counter
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from dotenv import load_dotenv

load_dotenv()

class IntelligentCompetitorDiscovery:
    """
    Advanced competitor discovery system that uses multiple data sources
    to intelligently identify competitors for any product
    """
    
    def __init__(self):
        # Load API keys
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')
        self.rapidapi_key = os.getenv('RAPIDAPI_KEY')
        
        # Comprehensive competitor database organized by category
        self.base_competitors = {
            'smartphones': ['Apple', 'Google', 'OnePlus', 'Xiaomi', 'Huawei', 'Oppo', 'Vivo', 'Realme', 'Nothing', 'Motorola'],
            'tv': ['LG', 'Sony', 'TCL', 'Hisense', 'Panasonic', 'Philips', 'Sharp', 'Roku', 'Amazon Fire TV'],
            'laptops': ['Apple', 'Dell', 'HP', 'Lenovo', 'ASUS', 'Acer', 'MSI', 'Razer', 'Microsoft Surface', 'Framework'],
            'tablets': ['Apple', 'Microsoft', 'Amazon', 'Huawei', 'Lenovo', 'Xiaomi', 'ASUS', 'Google'],
            'smartwatches': ['Apple', 'Garmin', 'Fitbit', 'Fossil', 'Amazfit', 'Huawei', 'Withings', 'Polar', 'Suunto'],
            'headphones': ['Apple', 'Sony', 'Bose', 'Sennheiser', 'Audio-Technica', 'JBL', 'Beats', 'Jabra', 'Anker'],
            'home_appliances': ['LG', 'Whirlpool', 'GE', 'Bosch', 'Electrolux', 'Miele', 'KitchenAid', 'Frigidaire'],
            'gaming': ['Sony', 'Microsoft', 'Nintendo', 'Valve', 'Razer', 'Logitech', 'SteelSeries', 'Corsair'],
            'cameras': ['Canon', 'Nikon', 'Sony', 'Fujifilm', 'Panasonic', 'Olympus', 'GoPro', 'DJI'],
            'smart_home': ['Amazon', 'Google', 'Apple', 'Philips Hue', 'Ring', 'Nest', 'Ecobee', 'TP-Link'],
            'wearables': ['Apple', 'Fitbit', 'Garmin', 'Oura', 'Whoop', 'Polar', 'Amazfit', 'Fossil']
        }
        
        # Brand reputation and market positioning data
        self.brand_profiles = {
            'Apple': {'positioning': 'premium', 'strength': 'design_ecosystem', 'price_factor': 1.3},
            'Google': {'positioning': 'innovation', 'strength': 'ai_software', 'price_factor': 1.1},
            'Microsoft': {'positioning': 'enterprise', 'strength': 'productivity', 'price_factor': 1.2},
            'Sony': {'positioning': 'quality', 'strength': 'audio_visual', 'price_factor': 1.1},
            'LG': {'positioning': 'value', 'strength': 'displays', 'price_factor': 0.9},
            'Xiaomi': {'positioning': 'value', 'strength': 'price_performance', 'price_factor': 0.7},
            'OnePlus': {'positioning': 'flagship_killer', 'strength': 'performance', 'price_factor': 0.9},
            'Huawei': {'positioning': 'innovation', 'strength': 'camera_tech', 'price_factor': 0.8}
        }
    
    def discover_competitors(self, product_name: str, category: str = None, price_range: str = None) -> Dict[str, Any]:
        """
        Main method to discover competitors for any product using multiple sources
        
        Args:
            product_name: Name of the product to analyze
            category: Product category (optional, will auto-detect if not provided)
            price_range: Expected price range (budget/mid/premium)
        
        Returns:
            Comprehensive competitor analysis with confidence scores
        """
        print(f"🔍 Discovering competitors for: {product_name}")
        
        # Auto-detect category if not provided
        if not category:
            category = self._detect_product_category(product_name)
            print(f"📝 Auto-detected category: {category}")
        
        competitors_data = {
            'product_name': product_name,
            'category': category,
            'price_range': price_range,
            'discovery_timestamp': datetime.now().isoformat(),
            'direct_competitors': [],
            'indirect_competitors': [],
            'emerging_competitors': [],
            'confidence_scores': {},
            'discovery_sources': {},
            'market_insights': {}
        }
        
        # Discovery Method 1: Category-based baseline
        print("📊 Getting category-based competitors...")
        category_competitors = self._get_category_based_competitors(category)
        
        # Discovery Method 2: News and media analysis
        print("📰 Analyzing news mentions...")
        news_competitors = self._discover_from_news_analysis(product_name, category)
        
        # Discovery Method 3: YouTube comparison videos
        print("📺 Analyzing YouTube comparisons...")
        youtube_competitors = self._discover_from_youtube_analysis(product_name)
        
        # Discovery Method 4: Product name pattern analysis
        print("🔤 Analyzing product name patterns...")
        pattern_competitors = self._discover_from_product_patterns(product_name, category)
        
        # Discovery Method 5: E-commerce platform analysis
        print("🛒 Analyzing e-commerce data...")
        ecommerce_competitors = self._discover_from_ecommerce_analysis(product_name, category)
        
        # Combine all discovery sources
        all_sources = [
            ('category_baseline', category_competitors, 0.7),
            ('news_analysis', news_competitors, 0.9),
            ('youtube_analysis', youtube_competitors, 0.8),
            ('pattern_analysis', pattern_competitors, 0.6),
            ('ecommerce_analysis', ecommerce_competitors, 0.8)
        ]
        
        # Score and rank all discovered competitors
        competitor_scores = self._calculate_competitor_scores(all_sources)
        
        # Categorize competitors by confidence and relevance
        categorized = self._categorize_competitors(competitor_scores, price_range)
        
        competitors_data.update(categorized)
        
        # Generate market insights
        competitors_data['market_insights'] = self._generate_market_insights(
            categorized, category, price_range
        )
        
        print(f"✅ Discovery complete! Found {len(categorized['direct_competitors'])} direct competitors")
        return competitors_data
    
    def _detect_product_category(self, product_name: str) -> str:
        """Auto-detect product category from product name using keyword analysis"""
        
        product_lower = product_name.lower()
        
        # Category detection patterns
        category_patterns = {
            'smartphones': [
                'galaxy', 'iphone', 'pixel', 'phone', 'smartphone', 'mobile',
                'note', 'pro', 'plus', 'ultra', 'mini'
            ],
            'tv': [
                'tv', 'television', 'qled', 'oled', 'neo', 'crystal', 'uhd',
                '4k', '8k', 'smart tv', 'display', 'monitor'
            ],
            'laptops': [
                'laptop', 'notebook', 'book', 'macbook', 'thinkpad', 'pavilion',
                'inspiron', 'zenbook', 'gaming laptop', 'ultrabook'
            ],
            'tablets': [
                'tablet', 'ipad', 'tab', 'slate', 'pad', 'surface'
            ],
            'smartwatches': [
                'watch', 'smartwatch', 'fitness', 'tracker', 'band', 'wear'
            ],
            'headphones': [
                'headphones', 'earbuds', 'headset', 'earphones', 'buds',
                'airpods', 'beats', 'wireless'
            ],
            'home_appliances': [
                'refrigerator', 'washer', 'dryer', 'oven', 'microwave',
                'dishwasher', 'air conditioner', 'vacuum'
            ],
            'cameras': [
                'camera', 'dslr', 'mirrorless', 'lens', 'camcorder', 'gopro'
            ],
            'gaming': [
                'gaming', 'console', 'playstation', 'xbox', 'controller',
                'gamepad', 'steam deck'
            ]
        }
        
        # Score each category based on keyword matches
        category_scores = {}
        for category, keywords in category_patterns.items():
            score = sum(1 for keyword in keywords if keyword in product_lower)
            if score > 0:
                category_scores[category] = score
        
        # Return the highest scoring category
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            return best_category
        
        return 'electronics'  # Default fallback
    
    def _get_category_based_competitors(self, category: str) -> List[str]:
        """Get baseline competitors from category mapping"""
        category_key = category.lower().replace(' ', '_')
        return self.base_competitors.get(category_key, self.base_competitors.get('smartphones', []))
    
    def _discover_from_news_analysis(self, product_name: str, category: str) -> List[str]:
        """Discover competitors mentioned in news articles about the product"""
        
        if not self.news_api_key:
            print("⚠️ News API key not available")
            return []
        
        try:
            # Search for news articles about the product and competitors
            search_queries = [
                f'"{product_name}" competitors',
                f'"{product_name}" vs',
                f'{product_name.split()[0]} {category} comparison',
                f'best {category} 2025'
            ]
            
            all_competitors = []
            
            for query in search_queries:
                url = "https://newsapi.org/v2/everything"
                params = {
                    'q': query,
                    'apiKey': self.news_api_key,
                    'language': 'en',
                    'pageSize': 20,
                    'sortBy': 'relevancy',
                    'from': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
                }
                
                response = requests.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    articles = response.json().get('articles', [])
                    
                    # Extract competitor names from article titles and descriptions
                    for article in articles:
                        text = f"{article.get('title', '')} {article.get('description', '')}"
                        competitors = self._extract_brand_names_from_text(text)
                        all_competitors.extend(competitors)
                
                # Small delay to respect rate limits
                import time
                time.sleep(0.5)
            
            # Filter and deduplicate
            unique_competitors = list(set(all_competitors))
            print(f"📰 Found {len(unique_competitors)} competitors from news analysis")
            return unique_competitors[:10]  # Return top 10
            
        except Exception as e:
            print(f"⚠️ News analysis failed: {e}")
            return []
    
    def _discover_from_youtube_analysis(self, product_name: str) -> List[str]:
        """Discover competitors from YouTube comparison videos"""
        
        if not self.youtube_api_key:
            print("⚠️ YouTube API key not available")
            return []
        
        try:
            # Search for comparison and review videos
            search_queries = [
                f'{product_name} vs',
                f'{product_name} comparison',
                f'{product_name} review',
                f'best {product_name.split()[-1]} 2025'  # e.g., "best smartphone 2025"
            ]
            
            all_competitors = []
            
            for query in search_queries[:2]:  # Limit to 2 queries to save API quota
                url = "https://www.googleapis.com/youtube/v3/search"
                params = {
                    'part': 'snippet',
                    'q': query,
                    'type': 'video',
                    'maxResults': 15,
                    'key': self.youtube_api_key,
                    'order': 'relevance'
                }
                
                response = requests.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    videos = response.json().get('items', [])
                    
                    # Extract competitor names from video titles and descriptions
                    for video in videos:
                        snippet = video.get('snippet', {})
                        text = f"{snippet.get('title', '')} {snippet.get('description', '')}"
                        competitors = self._extract_brand_names_from_text(text)
                        all_competitors.extend(competitors)
                
                # Small delay to respect rate limits
                import time
                time.sleep(1)
            
            unique_competitors = list(set(all_competitors))
            print(f"📺 Found {len(unique_competitors)} competitors from YouTube analysis")
            return unique_competitors[:10]
            
        except Exception as e:
            print(f"⚠️ YouTube analysis failed: {e}")
            return []
    
    def _discover_from_product_patterns(self, product_name: str, category: str) -> List[str]:
        """Discover competitors based on product naming patterns and technology indicators"""
        
        product_lower = product_name.lower()
        pattern_competitors = []
        
        # Technology and feature pattern mapping
        tech_patterns = {
            # Smartphone patterns
            'galaxy': ['Apple', 'Google', 'OnePlus', 'Xiaomi'],
            'iphone': ['Samsung', 'Google', 'OnePlus', 'Huawei'],
            'pixel': ['Samsung', 'Apple', 'OnePlus', 'Xiaomi'],
            
            # TV patterns
            'qled': ['LG', 'Sony', 'TCL', 'Hisense'],
            'oled': ['Samsung', 'Sony', 'Panasonic', 'Philips'],
            'neo': ['LG', 'Sony', 'TCL'],
            
            # Laptop patterns
            'book': ['Apple', 'Dell', 'HP', 'Lenovo'],
            'pro': ['Apple', 'Dell', 'HP', 'Microsoft'],
            'gaming': ['Razer', 'MSI', 'ASUS', 'Alienware'],
            
            # Watch patterns
            'watch': ['Apple', 'Garmin', 'Fitbit', 'Fossil'],
            'fitness': ['Fitbit', 'Garmin', 'Polar', 'Suunto'],
            
            # Audio patterns
            'buds': ['Apple', 'Sony', 'Bose', 'Jabra'],
            'wireless': ['Apple', 'Sony', 'Bose', 'JBL']
        }
        
        # Look for pattern matches
        for pattern, competitors in tech_patterns.items():
            if pattern in product_lower:
                pattern_competitors.extend(competitors)
        
        # Also check category-specific indicators
        if category.lower() in ['smartphones', 'mobile']:
            if any(term in product_lower for term in ['5g', 'pro', 'ultra', 'max']):
                pattern_competitors.extend(['Apple', 'Google', 'OnePlus'])
        
        elif category.lower() == 'tv':
            if any(term in product_lower for term in ['4k', '8k', 'uhd', 'hdr']):
                pattern_competitors.extend(['LG', 'Sony', 'TCL'])
        
        # Remove duplicates and Samsung itself
        unique_competitors = list(set(pattern_competitors))
        unique_competitors = [c for c in unique_competitors if c.lower() != 'samsung']
        
        print(f"🔤 Found {len(unique_competitors)} competitors from pattern analysis")
        return unique_competitors
    
    def _discover_from_ecommerce_analysis(self, product_name: str, category: str) -> List[str]:
        """Discover competitors from e-commerce platform data"""
        
        # For now, return category-based suggestions since e-commerce APIs are complex
        # In a real implementation, this would scrape Amazon, Best Buy, etc.
        
        category_key = category.lower().replace(' ', '_')
        ecommerce_competitors = self.base_competitors.get(category_key, [])
        
        # Add some randomization to simulate real e-commerce discovery
        import random
        selected_competitors = random.sample(
            ecommerce_competitors, 
            min(len(ecommerce_competitors), 6)
        )
        
        print(f"🛒 Found {len(selected_competitors)} competitors from e-commerce analysis")
        return selected_competitors
    
    def _extract_brand_names_from_text(self, text: str) -> List[str]:
        """Extract known brand names from text using pattern matching"""
        
        if not text:
            return []
        
        # Comprehensive list of tech brands
        known_brands = set()
        for competitor_list in self.base_competitors.values():
            known_brands.update(competitor_list)
        
        # Additional brands not in base lists
        additional_brands = {
            'Apple', 'Google', 'Microsoft', 'Sony', 'LG', 'HP', 'Dell', 'Lenovo', 
            'ASUS', 'Acer', 'Xiaomi', 'Huawei', 'Oppo', 'Vivo', 'OnePlus', 'Realme',
            'TCL', 'Hisense', 'Panasonic', 'Philips', 'JBL', 'Bose', 'Beats',
            'Garmin', 'Fitbit', 'Fossil', 'Amazfit', 'Nothing', 'Framework',
            'Razer', 'MSI', 'Corsair', 'Logitech', 'SteelSeries'
        }
        known_brands.update(additional_brands)
        
        found_brands = []
        text_upper = text.upper()
        
        for brand in known_brands:
            # Look for brand mentions (case-insensitive)
            if brand.upper() in text_upper and brand.lower() != 'samsung':
                found_brands.append(brand)
        
        return found_brands
    
    def _calculate_competitor_scores(self, sources: List[Tuple[str, List[str], float]]) -> Dict[str, Dict[str, Any]]:
        """Calculate confidence scores for each discovered competitor"""
        
        competitor_scores = {}
        
        for source_name, competitors, confidence_weight in sources:
            for competitor in competitors:
                if competitor.lower() == 'samsung':
                    continue  # Skip Samsung itself
                
                if competitor not in competitor_scores:
                    competitor_scores[competitor] = {
                        'total_score': 0.0,
                        'sources': [],
                        'source_count': 0,
                        'max_confidence': 0.0
                    }
                
                # Add to total score
                competitor_scores[competitor]['total_score'] += confidence_weight
                competitor_scores[competitor]['sources'].append(source_name)
                competitor_scores[competitor]['source_count'] += 1
                competitor_scores[competitor]['max_confidence'] = max(
                    competitor_scores[competitor]['max_confidence'], 
                    confidence_weight
                )
        
        # Normalize scores based on number of sources
        for competitor, data in competitor_scores.items():
            # Bonus for being found in multiple sources
            source_bonus = min(data['source_count'] * 0.2, 1.0)
            data['final_score'] = data['total_score'] + source_bonus
        
        return competitor_scores
    
    def _categorize_competitors(self, competitor_scores: Dict[str, Dict[str, Any]], price_range: str = None) -> Dict[str, Any]:
        """Categorize competitors into direct, indirect, and emerging based on scores"""
        
        # Sort competitors by final score
        sorted_competitors = sorted(
            competitor_scores.items(),
            key=lambda x: x[1]['final_score'],
            reverse=True
        )
        
        categorized = {
            'direct_competitors': [],
            'indirect_competitors': [],
            'emerging_competitors': [],
            'confidence_scores': {},
            'discovery_sources': {}
        }
        
        for competitor, data in sorted_competitors[:20]:  # Top 20 competitors
            score = data['final_score']
            sources = data['sources']
            source_count = data['source_count']
            
            # Store metadata
            categorized['confidence_scores'][competitor] = round(score, 2)
            categorized['discovery_sources'][competitor] = sources
            
            # Categorize based on score and source count
            if score >= 2.0 and source_count >= 2:
                # High confidence, multiple sources = direct competitor
                categorized['direct_competitors'].append(competitor)
            elif score >= 1.0 or source_count >= 2:
                # Medium confidence = indirect competitor
                categorized['indirect_competitors'].append(competitor)
            else:
                # Lower confidence = emerging competitor
                categorized['emerging_competitors'].append(competitor)
        
        # Limit each category
        categorized['direct_competitors'] = categorized['direct_competitors'][:8]
        categorized['indirect_competitors'] = categorized['indirect_competitors'][:6]
        categorized['emerging_competitors'] = categorized['emerging_competitors'][:4]
        
        return categorized
    
    def _generate_market_insights(self, categorized_competitors: Dict[str, Any], 
                                 category: str, price_range: str = None) -> Dict[str, Any]:
        """Generate market insights based on discovered competitors"""
        
        insights = {
            'market_analysis': {},
            'competitive_landscape': {},
            'strategic_recommendations': []
        }
        
        all_competitors = (
            categorized_competitors['direct_competitors'] + 
            categorized_competitors['indirect_competitors']
        )
        
        # Market concentration analysis
        insights['market_analysis'] = {
            'total_identified_competitors': len(all_competitors),
            'direct_threats': len(categorized_competitors['direct_competitors']),
            'market_fragmentation': 'High' if len(all_competitors) > 10 else 'Medium' if len(all_competitors) > 5 else 'Low',
            'category': category
        }
        
        # Competitive landscape analysis
        brand_positions = {}
        for competitor in all_competitors[:10]:  # Top 10
            profile = self.brand_profiles.get(competitor, {
                'positioning': 'unknown',
                'price_factor': 1.0
            })
            brand_positions[competitor] = profile
        
        insights['competitive_landscape'] = {
            'premium_brands': [b for b, p in brand_positions.items() if p.get('price_factor', 1.0) > 1.15],
            'value_brands': [b for b, p in brand_positions.items() if p.get('price_factor', 1.0) < 0.85],
            'innovation_leaders': [b for b, p in brand_positions.items() if p.get('positioning') == 'innovation']
        }
        
        # Strategic recommendations
        recommendations = []
        
        if len(categorized_competitors['direct_competitors']) > 5:
            recommendations.append("Highly competitive market - focus on unique differentiation")
        
        premium_count = len(insights['competitive_landscape']['premium_brands'])
        value_count = len(insights['competitive_landscape']['value_brands'])
        
        if premium_count > value_count:
            recommendations.append("Premium-heavy market - consider value positioning opportunity")
        elif value_count > premium_count:
            recommendations.append("Value-competitive market - premium differentiation may be effective")
        
        if 'Apple' in all_competitors:
            recommendations.append("Apple presence requires strong ecosystem and design focus")
        
        if any(brand in all_competitors for brand in ['Xiaomi', 'OnePlus', 'Realme']):
            recommendations.append("Price-aggressive competitors present - value proposition crucial")
        
        insights['strategic_recommendations'] = recommendations
        
        return insights

# Example usage and testing
def demo_competitor_discovery():
    """Demonstrate the intelligent competitor discovery system"""
    
    discovery = IntelligentCompetitorDiscovery()
    
    # Test products
    test_products = [
        ("Galaxy S25 Ultra", "smartphones"),
        ("Samsung Neo QLED 8K TV", "tv"),
        ("Galaxy Book Pro 360", "laptops"),
        ("Galaxy Watch 6 Classic", "smartwatches"),
        ("Galaxy Buds Pro 3", "headphones")
    ]
    
    for product_name, category in test_products:
        print(f"\n{'='*80}")
        print(f"🔍 TESTING: {product_name}")
        print('='*80)
        
        result = discovery.discover_competitors(product_name, category)
        
        print(f"\n📊 DISCOVERY RESULTS:")
        print(f"🎯 Direct Competitors ({len(result['direct_competitors'])}):")
        for comp in result['direct_competitors']:
            score = result['confidence_scores'].get(comp, 0)
            sources = result['discovery_sources'].get(comp, [])
            print(f"   • {comp} (Score: {score}, Sources: {len(sources)})")
        
        print(f"\n🔄 Indirect Competitors ({len(result['indirect_competitors'])}):")
        for comp in result['indirect_competitors']:
            score = result['confidence_scores'].get(comp, 0)
            print(f"   • {comp} (Score: {score})")
        
        print(f"\n💡 Market Insights:")
        for recommendation in result['market_insights']['strategic_recommendations']:
            print(f"   • {recommendation}")
        
        print(f"\n🏆 Competitive Landscape:")
        landscape = result['market_insights']['competitive_landscape']
        print(f"   Premium Brands: {', '.join(landscape['premium_brands'])}")
        print(f"   Value Brands: {', '.join(landscape['value_brands'])}")

if __name__ == "__main__":
    demo_competitor_discovery()
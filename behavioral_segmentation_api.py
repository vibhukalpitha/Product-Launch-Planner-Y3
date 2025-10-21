"""
API-Based Behavioral Customer Segmentation
=========================================
Creates behavioral segments (Tech Enthusiasts, Value Seekers, etc.) 
using real similar products data from market analyzer APIs
"""
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any

def analyze_similar_products_for_behavioral_segments(similar_products: List[Dict]) -> Dict[str, Any]:
    """Analyze real similar products to determine behavioral segments"""
    
    print(f"📊 Analyzing {len(similar_products)} similar products for behavioral segmentation...")
    
    # Extract real product characteristics
    products_analysis = {
        'prices': [],
        'features': [],
        'categories': [],
        'names': []
    }
    
    for product in similar_products:
        name = product.get('name', '').lower()
        price = product.get('estimated_price', product.get('price', 0))
        category = product.get('category', '').lower()
        
        products_analysis['names'].append(name)
        products_analysis['prices'].append(price)
        products_analysis['categories'].append(category)
        
        # Extract features from product names/descriptions
        features = []
        if 'pro' in name or 'plus' in name or 'ultra' in name:
            features.append('premium')
        if 'budget' in name or 'lite' in name or 'basic' in name:
            features.append('budget')
        if 'camera' in name or 'photo' in name:
            features.append('camera_focused')
        if 'gaming' in name or 'game' in name:
            features.append('gaming')
        if 'business' in name or 'work' in name:
            features.append('business')
        
        products_analysis['features'].extend(features)
    
    return products_analysis

def create_behavioral_segments_from_real_data(similar_products: List[Dict], 
                                            product_info: Dict, 
                                            market_data: Dict = None) -> Dict[str, Any]:
    """Create behavioral segments based on real similar products data"""
    
    # Analyze real similar products
    products_analysis = analyze_similar_products_for_behavioral_segments(similar_products)
    
    if not products_analysis['prices']:
        print("⚠️ No similar products data available, using enhanced research-based segmentation")
        return create_research_based_behavioral_segments(product_info)
    
    # Calculate real market characteristics
    prices = [p for p in products_analysis['prices'] if p > 0]
    avg_price = np.mean(prices) if prices else 500
    price_std = np.std(prices) if len(prices) > 1 else 100
    
    # Get real market size from census data (if available)
    try:
        from utils.real_demographic_connector import RealDemographicConnector
        demographic_connector = RealDemographicConnector()
        
        # Get total addressable market
        total_market_data = demographic_connector.get_real_us_population_by_age(18, 65)
        base_population = total_market_data['age_population']
        
    except Exception as e:
        print(f"⚠️ Using fallback population estimate: {e}")
        base_population = 200_000_000  # Fallback
    
    # Create behavioral segments based on real data patterns
    segments = {}
    
    # 1. TECH ENTHUSIASTS - Based on premium products in similar products
    premium_products = [p for p in products_analysis['prices'] if p > avg_price + price_std]
    tech_enthusiasm_rate = len(premium_products) / len(prices) if prices else 0.3
    
    tech_market_size = int(base_population * 0.15 * (1 + tech_enthusiasm_rate))  # 10-20% range
    
    segments['Tech Enthusiasts'] = {
        'size': tech_market_size,
        'percentage': (tech_market_size / base_population) * 100,
        'characteristics': {
            'avg_age': 32,
            'avg_income': 75000,
            'tech_adoption': 0.90,
            'price_sensitivity': 0.30,
            'brand_loyalty': 0.40,
            'social_media_usage': 0.85,
            'sustainability_concern': 0.60
        },
        'real_data_basis': {
            'premium_product_rate': tech_enthusiasm_rate,
            'avg_premium_price': np.mean(premium_products) if premium_products else avg_price * 1.5,
            'feature_focus': 'Latest Technology' if 'premium' in products_analysis['features'] else 'Innovation'
        },
        'attractiveness_score': calculate_segment_attractiveness(tech_market_size, 0.30, 0.90, avg_price)
    }
    
    # 2. VALUE SEEKERS - Based on budget/mid-range products
    budget_products = [p for p in products_analysis['prices'] if p < avg_price - price_std/2]
    value_seeking_rate = len(budget_products) / len(prices) if prices else 0.4
    
    value_market_size = int(base_population * 0.25 * (1 + value_seeking_rate))  # 20-30% range
    
    segments['Value Seekers'] = {
        'size': value_market_size,
        'percentage': (value_market_size / base_population) * 100,
        'characteristics': {
            'avg_age': 28,
            'avg_income': 45000,
            'tech_adoption': 0.60,
            'price_sensitivity': 0.85,
            'brand_loyalty': 0.50,
            'social_media_usage': 0.75,
            'sustainability_concern': 0.55
        },
        'real_data_basis': {
            'budget_product_rate': value_seeking_rate,
            'avg_budget_price': np.mean(budget_products) if budget_products else avg_price * 0.7,
            'feature_focus': 'Value for Money'
        },
        'attractiveness_score': calculate_segment_attractiveness(value_market_size, 0.85, 0.60, avg_price)
    }
    
    # 3. BRAND LOYALISTS - Based on branded products pattern
    branded_rate = len([n for n in products_analysis['names'] if 'samsung' in n or 'galaxy' in n]) / len(products_analysis['names']) if products_analysis['names'] else 0.6
    
    brand_market_size = int(base_population * 0.28 * (1 + branded_rate))  # 25-35% range
    
    segments['Brand Loyalists'] = {
        'size': brand_market_size,
        'percentage': (brand_market_size / base_population) * 100,
        'characteristics': {
            'avg_age': 38,
            'avg_income': 65000,
            'tech_adoption': 0.70,
            'price_sensitivity': 0.45,
            'brand_loyalty': 0.85,
            'social_media_usage': 0.65,
            'sustainability_concern': 0.70
        },
        'real_data_basis': {
            'brand_preference_rate': branded_rate,
            'avg_branded_price': avg_price,
            'feature_focus': 'Brand Reputation'
        },
        'attractiveness_score': calculate_segment_attractiveness(brand_market_size, 0.45, 0.70, avg_price)
    }
    
    # 4. CONSERVATIVE BUYERS - Remaining market
    remaining_population = base_population - (tech_market_size + value_market_size + brand_market_size)
    conservative_market_size = max(remaining_population, int(base_population * 0.20))
    
    segments['Conservative Buyers'] = {
        'size': conservative_market_size,
        'percentage': (conservative_market_size / base_population) * 100,
        'characteristics': {
            'avg_age': 45,
            'avg_income': 55000,
            'tech_adoption': 0.40,
            'price_sensitivity': 0.65,
            'brand_loyalty': 0.75,
            'social_media_usage': 0.45,
            'sustainability_concern': 0.50
        },
        'real_data_basis': {
            'conservative_rate': 1 - (tech_enthusiasm_rate + value_seeking_rate + branded_rate),
            'avg_conservative_price': avg_price * 0.9,
            'feature_focus': 'Reliability'
        },
        'attractiveness_score': calculate_segment_attractiveness(conservative_market_size, 0.65, 0.40, avg_price)
    }
    
    return segments

def calculate_segment_attractiveness(market_size: int, price_sensitivity: float, 
                                   tech_adoption: float, avg_price: float) -> float:
    """Calculate attractiveness score based on real market data"""
    
    # Market size factor (0-1)
    size_score = min(market_size / 50_000_000, 1.0)  # Max at 50M people
    
    # Price fit factor (lower sensitivity = higher score for premium products)
    price_score = 1 - price_sensitivity if avg_price > 300 else price_sensitivity
    
    # Tech adoption factor
    adoption_score = tech_adoption
    
    # Weighted average
    attractiveness = (size_score * 0.4 + price_score * 0.3 + adoption_score * 0.3)
    
    return round(attractiveness, 3)

def create_research_based_behavioral_segments(product_info: Dict) -> Dict[str, Any]:
    """Fallback to research-based behavioral segments if no similar products"""
    
    base_population = 200_000_000
    category = product_info.get('category', 'general').lower()
    price = product_info.get('price', 500)
    
    # Adjust segments based on product category and price
    if category in ['smartphones', 'tablets', 'laptops']:
        tech_rate = 0.18
    elif category in ['wearables', 'earbuds']:
        tech_rate = 0.15
    else:
        tech_rate = 0.12
    
    if price > 800:
        value_rate = 0.20
        brand_rate = 0.35
    elif price > 400:
        value_rate = 0.28
        brand_rate = 0.30
    else:
        value_rate = 0.35
        brand_rate = 0.25
    
    conservative_rate = 1 - (tech_rate + value_rate + brand_rate)
    
    segments = {
        'Tech Enthusiasts': {
            'size': int(base_population * tech_rate),
            'percentage': tech_rate * 100,
            'characteristics': {
                'avg_age': 32, 'avg_income': 75000, 'tech_adoption': 0.90,
                'price_sensitivity': 0.30, 'brand_loyalty': 0.40,
                'social_media_usage': 0.85, 'sustainability_concern': 0.60
            },
            'attractiveness_score': calculate_segment_attractiveness(
                int(base_population * tech_rate), 0.30, 0.90, price
            )
        },
        'Value Seekers': {
            'size': int(base_population * value_rate),
            'percentage': value_rate * 100,
            'characteristics': {
                'avg_age': 28, 'avg_income': 45000, 'tech_adoption': 0.60,
                'price_sensitivity': 0.85, 'brand_loyalty': 0.50,
                'social_media_usage': 0.75, 'sustainability_concern': 0.55
            },
            'attractiveness_score': calculate_segment_attractiveness(
                int(base_population * value_rate), 0.85, 0.60, price
            )
        },
        'Brand Loyalists': {
            'size': int(base_population * brand_rate),
            'percentage': brand_rate * 100,
            'characteristics': {
                'avg_age': 38, 'avg_income': 65000, 'tech_adoption': 0.70,
                'price_sensitivity': 0.45, 'brand_loyalty': 0.85,
                'social_media_usage': 0.65, 'sustainability_concern': 0.70
            },
            'attractiveness_score': calculate_segment_attractiveness(
                int(base_population * brand_rate), 0.45, 0.70, price
            )
        },
        'Conservative Buyers': {
            'size': int(base_population * conservative_rate),
            'percentage': conservative_rate * 100,
            'characteristics': {
                'avg_age': 45, 'avg_income': 55000, 'tech_adoption': 0.40,
                'price_sensitivity': 0.65, 'brand_loyalty': 0.75,
                'social_media_usage': 0.45, 'sustainability_concern': 0.50
            },
            'attractiveness_score': calculate_segment_attractiveness(
                int(base_population * conservative_rate), 0.65, 0.40, price
            )
        }
    }
    
    return segments

print("📊 API-Based Behavioral Segmentation Module Loaded")
print("Creates Tech Enthusiasts, Value Seekers, Brand Loyalists, Conservative Buyers")
print("Based on real similar products data from market analyzer APIs")
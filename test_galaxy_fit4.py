#!/usr/bin/env python3
"""
Test script for Galaxy Fit4 fixes
"""
import sys
import os
sys.path.append('agents')

from market_trend_analyzer import MarketTrendAnalyzer

class MockCoordinator:
    def register_agent(self, name, agent):
        pass

def test_galaxy_fit4():
    analyzer = MarketTrendAnalyzer(MockCoordinator())
    
    print('=== Galaxy Fit4 Testing ===')
    
    # Test price estimation
    price = analyzer._estimate_product_price_from_name_and_text('Galaxy Fit4', 'Galaxy Fit4 fitness tracker review', 'wearable')
    tier = analyzer._determine_product_tier(price)
    print(f'Galaxy Fit4 Price: ${price:.0f} | Tier: {tier}')
    
    # Test validation
    is_valid = analyzer._is_valid_samsung_product('Galaxy Fit4', 'wearable')
    print(f'Galaxy Fit4 Valid for Wearables: {is_valid}')
    
    # Test search queries
    print('\n=== Search Queries for Galaxy Fit4 ===')
    queries = analyzer._generate_universal_search_queries('Galaxy Fit4', 'wearable', 'youtube')
    for i, query in enumerate(queries[:5], 1):
        print(f'{i}. {query}')
    
    # Test similarity with other wearables
    print('\n=== Similarity Testing ===')
    target_price = 120.0
    test_products = [
        ('Galaxy Fit3', 100.0),     # Should be high similarity (same series)
        ('Galaxy Watch SE2', 250.0), # Should be lower (different type)
        ('Galaxy Watch7', 350.0),   # Should be lowest (premium watch)
    ]
    
    print(f'Target: Galaxy Fit4 (${target_price})')
    for product, comp_price in test_products:
        similarity = analyzer._calculate_product_similarity(product, 'wearable', comp_price, target_price)
        comp_tier = analyzer._determine_product_tier(comp_price)
        print(f'  vs {product:15s} (${comp_price:3.0f}, {comp_tier:10s}) | Similarity: {similarity:.3f}')

if __name__ == "__main__":
    test_galaxy_fit4()
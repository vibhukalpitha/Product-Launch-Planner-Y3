#!/usr/bin/env python3
"""
Test Galaxy Fit4 similarity issue
"""
import sys
import os
sys.path.append('agents')

from market_trend_analyzer import MarketTrendAnalyzer

class MockCoordinator:
    def register_agent(self, name, agent):
        pass

def test_similarity_issue():
    analyzer = MarketTrendAnalyzer(MockCoordinator())
    
    print('=== Galaxy Fit4 Similarity Issue Analysis ===')
    
    # Test with the user's input: Galaxy Fit4 at $350 (wrong price from UI)
    target_price = 350.0  # What the user entered
    products = [
        ('Galaxy Fit 4', 100.0),    # API found this correctly priced
        ('Galaxy Fit 3', 100.0),    # API found this correctly priced  
        ('Galaxy Watch 6', 350.0),  # API found this correctly priced
        ('Galaxy Watch8', 350.0),   # API found this correctly priced
    ]
    
    print(f'Target: Galaxy Fit4 (${target_price}) <- User entered wrong price')
    print('Similar products found by API:')
    
    for product, price in products:
        similarity = analyzer._calculate_product_similarity(product, 'wearable', price, target_price)
        tier = analyzer._determine_product_tier(price)
        print(f'  vs {product:15s} (${price:3.0f}, {tier:10s}) | Similarity: {similarity:.3f}')
    
    print('\n=== Test with CORRECT target price ===')
    correct_target_price = 120.0  # What it should be
    print(f'Target: Galaxy Fit4 (${correct_target_price}) <- Correct price')
    print('Similar products found by API:')
    
    for product, price in products:
        similarity = analyzer._calculate_product_similarity(product, 'wearable', price, correct_target_price)
        tier = analyzer._determine_product_tier(price)
        print(f'  vs {product:15s} (${price:3.0f}, {tier:10s}) | Similarity: {similarity:.3f}')

if __name__ == "__main__":
    test_similarity_issue()
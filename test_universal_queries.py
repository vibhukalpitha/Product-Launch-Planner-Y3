#!/usr/bin/env python3
"""
Test script for enhanced universal search query generator
"""
import sys
import os
sys.path.append('agents')

from market_trend_analyzer import MarketTrendAnalyzer

class MockCoordinator:
    def register_agent(self, name, agent):
        pass

def test_universal_queries():
    analyzer = MarketTrendAnalyzer(MockCoordinator())
    
    print('=== Enhanced Universal Query Generator Test ===')
    print('Testing adaptability to ANY custom Samsung product input:\n')
    
    # Test various custom inputs that users might provide
    test_cases = [
        # Custom budget inputs
        ('Galaxy M37 5G', 'smartphone', 'youtube'),
        ('Custom Budget Phone M99', 'smartphone', 'news'),
        
        # Custom premium inputs  
        ('Galaxy S28 Ultra Pro Max', 'smartphone', 'google'),
        ('New Samsung Flagship 2026', 'smartphone', 'reddit'),
        
        # Custom tablet inputs
        ('Galaxy Tab X15 Ultra', 'tablet', 'youtube'),
        ('Samsung Tablet Pro 2025', 'tablet', 'news'),
        
        # Custom wearable inputs
        ('Galaxy Watch Ultra 10', 'wearable', 'google'), 
        ('Samsung Smart Ring', 'wearable', 'reddit'),
        
        # Completely custom/unusual inputs
        ('MySamsung Innovation Device', 'gadget', 'general'),
        ('Future Galaxy Product', 'electronics', 'youtube')
    ]
    
    for product, category, api_type in test_cases:
        print(f'Input: "{product}" | Category: {category} | API: {api_type.upper()}')
        queries = analyzer._generate_universal_search_queries(product, category, api_type)
        for i, query in enumerate(queries[:5], 1):  # Show top 5 queries
            print(f'  {i}. {query}')
        print()

if __name__ == "__main__":
    test_universal_queries()
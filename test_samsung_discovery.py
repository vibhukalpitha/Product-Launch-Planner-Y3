#!/usr/bin/env python3
"""
Test Samsung Product Discovery with Multi-API Integration
Tests the enhanced discovery system including SerpApi integration
"""

import sys
import os
sys.path.append('.')

from agents.market_trend_analyzer import MarketTrendAnalyzer
from agents.communication_coordinator import CommunicationCoordinator

def test_samsung_discovery():
    """Test Samsung product discovery with multiple APIs"""
    print("🚀 TESTING SAMSUNG PRODUCT DISCOVERY")
    print("🔍 Multi-API Integration Test")
    print("=" * 60)
    
    # Initialize coordinator and analyzer
    coordinator = CommunicationCoordinator()
    analyzer = MarketTrendAnalyzer(coordinator)
    
    # Test product discovery
    test_product = "Samsung Galaxy S25 Ultra"
    test_category = "smartphone"
    test_price = 1200
    
    print(f"📱 Testing: {test_product}")
    print(f"📱 Category: {test_category}")
    print(f"💰 Price: ${test_price}")
    print("-" * 60)
    
    # Run discovery
    result = analyzer.discover_samsung_similar_products(
        test_product, test_category, test_price
    )
    
    # Print results
    products = result.get('found_products', [])
    print(f"\n✅ DISCOVERY RESULTS:")
    print(f"📊 Total products found: {len(products)}")
    
    if products:
        # Group by source and show all sources
        sources = {}
        all_sources_count = {}
        
        for product in products:
            primary_source = product.get('source', 'Unknown')
            all_sources = product.get('all_sources', [primary_source])
            
            # Count all sources
            for source in all_sources:
                all_sources_count[source] = all_sources_count.get(source, 0) + 1
            
            # Group by primary source
            if primary_source not in sources:
                sources[primary_source] = []
            sources[primary_source].append(product)
        
        print(f"📊 All API sources contributing: {list(all_sources_count.keys())}")
        print(f"📊 Source counts: {all_sources_count}")
        print("\n📋 Products by primary source:")
        
        for source, source_products in sources.items():
            print(f"\n🔹 {source}: {len(source_products)} products")
            for i, product in enumerate(source_products[:3], 1):  # Show first 3
                name = product.get('name', 'Unknown')
                price = product.get('estimated_price', 0)
                year = product.get('launch_year', 'Unknown')
                all_sources = product.get('all_sources', [source])
                sources_str = ', '.join(all_sources) if len(all_sources) > 1 else source
                print(f"   {i}. {name} (${price}, {year}) - Sources: {sources_str}")
            
            if len(source_products) > 3:
                print(f"   ... and {len(source_products) - 3} more")
    
    else:
        print("❌ No products found")
    
    print("\n" + "=" * 60)
    print("🎯 Test completed!")

if __name__ == "__main__":
    test_samsung_discovery()
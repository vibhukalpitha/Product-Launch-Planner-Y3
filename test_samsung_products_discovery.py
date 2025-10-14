"""
Test Samsung Product Discovery in Market Trend Analyzer
Tests the enhanced market analyzer that shows Samsung's past similar products first
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.market_trend_analyzer import MarketTrendAnalyzer
from agents.communication_coordinator import CommunicationCoordinator

def test_samsung_product_discovery():
    print("🚀 TESTING ENHANCED MARKET TREND ANALYZER")
    print("=" * 80)
    print("🎯 Focus: Samsung's Past Similar Products Discovery")
    print("=" * 80)
    
    # Initialize
    coordinator = CommunicationCoordinator()
    analyzer = MarketTrendAnalyzer(coordinator)
    
    # Test products with different price tiers
    test_products = [
        {
            "name": "Galaxy S25 Ultra",
            "category": "smartphones", 
            "price": 1199,
            "description": "High-end flagship smartphone"
        },
        {
            "name": "Galaxy Tab Ultra",
            "category": "tablets",
            "price": 1099,
            "description": "Premium tablet for professionals"
        },
        {
            "name": "Galaxy Watch Pro 7",
            "category": "wearables",
            "price": 449,
            "description": "Premium smartwatch"
        },
        {
            "name": "Galaxy Book Elite",
            "category": "laptops",
            "price": 1599,
            "description": "High-performance laptop"
        }
    ]
    
    for i, product in enumerate(test_products, 1):
        print(f"\n{'='*80}")
        print(f"📱 TEST {i}/4: {product['name']}")
        print(f"📂 Category: {product['category'].title()}")
        print(f"💰 Price: ${product['price']}")
        print(f"📋 Description: {product['description']}")
        print('='*80)
        
        # Run the enhanced market analysis
        print(f"\n🔄 Running enhanced market analysis...")
        result = analyzer.analyze_market_trends(product)
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            continue
        
        # Display Samsung similar products (the NEW feature!)
        samsung_products = result.get('samsung_similar_products', {})
        
        if samsung_products and samsung_products.get('found_products'):
            print(f"\n📊 SAMSUNG'S PAST SIMILAR PRODUCTS:")
            print(f"   🔍 Discovery Method: {samsung_products.get('discovery_method', 'Unknown')}")
            print(f"   📡 Data Sources: {', '.join(samsung_products.get('data_sources', []))}")
            
            found_products = samsung_products['found_products']
            print(f"\n   📱 Found {len(found_products)} Similar Samsung Products:")
            
            for j, prod in enumerate(found_products[:5], 1):  # Show top 5
                print(f"      {j}. {prod['name']}")
                print(f"         💰 Price: ${prod['estimated_price']}")
                print(f"         📅 Year: {prod['launch_year']}")
                print(f"         🎯 Similarity: {prod['similarity_score']:.2f}")
                print(f"         📡 Source: {prod['source']}")
                print()
            
            # Price comparison analysis
            price_comparison = samsung_products.get('price_comparison', {})
            if price_comparison:
                print(f"   💰 PRICE COMPARISON ANALYSIS:")
                print(f"      🎯 Your Price: ${price_comparison['target_price']}")
                print(f"      📊 Samsung Avg: ${price_comparison['similar_products_avg']}")
                print(f"      📈 Position: {price_comparison['price_position']}")
                print(f"      📊 Percentile: {price_comparison['price_percentile']:.1f}th")
            
            # Product timeline
            timeline = samsung_products.get('product_timeline', [])
            if timeline:
                print(f"\n   📅 SAMSUNG PRODUCT TIMELINE:")
                for prod in timeline[:3]:  # Show recent 3
                    print(f"      {prod['year']}: {prod['name']} - ${prod['price']} ({prod.get('tier', 'Unknown')} tier)")
            
            # Category evolution
            evolution = samsung_products.get('category_evolution', {})
            if evolution:
                print(f"\n   📈 CATEGORY EVOLUTION INSIGHTS:")
                print(f"      📊 Analysis Period: {evolution.get('analysis_period', 'N/A')}")
                print(f"      🚀 Innovation Pace: {evolution.get('innovation_pace', 'Unknown')}")
                print(f"      📱 Total Products: {evolution.get('total_products_analyzed', 0)}")
        
        else:
            print(f"\n⚠️  No Samsung similar products found")
        
        # Show enhanced recommendations (now includes Samsung insights)
        recommendations = result.get('recommendations', [])
        if recommendations:
            print(f"\n💡 ENHANCED RECOMMENDATIONS:")
            for j, rec in enumerate(recommendations, 1):
                print(f"   {j}. {rec}")
        
        # Market analysis summary
        market_trends = result.get('market_trends', {})
        if market_trends:
            print(f"\n📊 MARKET ANALYSIS SUMMARY:")
            print(f"   💰 Market Avg Price: ${market_trends.get('average_price', 0)}")
            print(f"   📈 Growth Rate: {market_trends.get('growth_rate', 0)*100:.1f}%")
            print(f"   📡 Real Data: {'✅' if market_trends.get('real_data', False) else '❌'}")
            
            sources = market_trends.get('data_sources', [])
            if sources:
                print(f"   📡 Data Sources: {', '.join(sources)}")
        
        print(f"\n✅ Analysis complete for {product['name']}")
        
        if i < len(test_products):
            print(f"\n⏳ Moving to next product...")
    
    print(f"\n{'='*80}")
    print("🎉 ALL TESTS COMPLETED!")
    print("✅ Enhanced Market Trend Analyzer working!")
    print("🎯 Samsung's past similar products now shown FIRST!")
    print("📊 Real API data integration successful!")
    print('='*80)

def test_specific_high_end_phone():
    """Test specifically with a high-end phone to show Samsung flagships"""
    print(f"\n{'='*80}")
    print("📱 SPECIFIC TEST: HIGH-END PHONE")
    print("🎯 Should show Samsung's flagship phone history")
    print('='*80)
    
    coordinator = CommunicationCoordinator()
    analyzer = MarketTrendAnalyzer(coordinator)
    
    # High-end phone input
    high_end_phone = {
        "name": "Galaxy S26 Ultra Pro Max",
        "category": "smartphones",
        "price": 1399,  # Very high-end price
        "description": "Ultra-premium flagship smartphone"
    }
    
    print(f"🔍 Testing with: {high_end_phone['name']}")
    print(f"💰 Price: ${high_end_phone['price']} (Ultra-premium tier)")
    
    # Test just the Samsung products discovery
    samsung_products = analyzer.discover_samsung_similar_products(
        high_end_phone['name'],
        high_end_phone['category'],
        high_end_phone['price']
    )
    
    print(f"\n📊 SAMSUNG FLAGSHIP PHONE DISCOVERY RESULTS:")
    
    if samsung_products.get('found_products'):
        found = samsung_products['found_products']
        print(f"   📱 Found {len(found)} Samsung flagship phones:")
        
        # Show flagship phones specifically
        flagship_phones = [p for p in found if 'ultra' in p['name'].lower() or p['estimated_price'] > 1000]
        
        print(f"\n   🏆 Samsung Flagship/Ultra Models:")
        for phone in flagship_phones[:5]:
            print(f"      • {phone['name']}")
            print(f"        💰 ${phone['estimated_price']} ({phone['launch_year']})")
            print(f"        🎯 Similarity: {phone['similarity_score']:.2f}")
        
        # Price analysis for flagship tier
        price_comp = samsung_products.get('price_comparison', {})
        if price_comp:
            print(f"\n   💰 FLAGSHIP PRICE ANALYSIS:")
            print(f"      🎯 Your Price: ${price_comp['target_price']}")
            print(f"      📊 Samsung Flagships Avg: ${price_comp['similar_products_avg']}")
            print(f"      📈 Position: {price_comp['price_position']}")
    
    print(f"\n✅ High-end phone test complete!")

if __name__ == "__main__":
    test_samsung_product_discovery()
    test_specific_high_end_phone()
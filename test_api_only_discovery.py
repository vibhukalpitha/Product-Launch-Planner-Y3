#!/usr/bin/env python3
"""
Test script for API-only Samsung product discovery
"""

import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.market_trend_analyzer import MarketTrendAnalyzer
from agents.communication_coordinator import CommunicationCoordinator

def test_api_only_discovery():
    """Test the enhanced API-only Samsung product discovery"""
    
    print("🚀 Testing API-Only Samsung Product Discovery")
    print("=" * 60)
    
    # Initialize coordinator and market analyzer
    coordinator = CommunicationCoordinator()
    market_analyzer = MarketTrendAnalyzer(coordinator)
    
    # Test cases
    test_cases = [
        {
            'name': 'Galaxy S25 Ultra',
            'category': 'smartphones',
            'price': 1299
        },
        {
            'name': 'Galaxy Tab S10 Ultra',
            'category': 'tablets',
            'price': 1199
        },
        {
            'name': 'Galaxy Book4 Pro',
            'category': 'laptops',
            'price': 1699
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📱 TEST {i}: Discovering similar products for {test_case['name']}")
        print("-" * 50)
        
        try:
            # Discover similar Samsung products using APIs only
            result = market_analyzer.discover_samsung_similar_products(
                test_case['name'],
                test_case['category'], 
                test_case['price']
            )
            
            # Display results
            print(f"\n📊 RESULTS FOR {test_case['name']}:")
            print(f"Discovery Method: {result.get('discovery_method', 'unknown')}")
            print(f"Data Sources: {', '.join(result.get('data_sources', []))}")
            print(f"Total Products Found: {len(result.get('found_products', []))}")
            
            # Show found products
            products = result.get('found_products', [])
            if products:
                print(f"\n🎯 TOP SIMILAR PRODUCTS:")
                for j, product in enumerate(products[:5], 1):
                    print(f"  {j}. {product['name']}")
                    print(f"     Source: {product['source']}")
                    print(f"     Price: ${product['estimated_price']}")
                    print(f"     Year: {product['launch_year']}")
                    print(f"     Similarity: {product['similarity_score']}")
                    print()
            else:
                print("❌ No products found!")
                
        except Exception as e:
            print(f"❌ Error testing {test_case['name']}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✅ API-Only Discovery Test Complete!")

if __name__ == "__main__":
    test_api_only_discovery()
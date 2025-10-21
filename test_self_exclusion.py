#!/usr/bin/env python3
"""
Test script to verify:
1. Galaxy Fit 4 doesn't appear as similar to itself
2. Future products get correct launch years
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.market_trend_analyzer import MarketTrendAnalyzer
from agents.communication_coordinator import CommunicationCoordinator

def test_self_exclusion():
    """Test that products don't appear in their own similar products list"""
    print("=" * 60)
    print("TESTING SELF-EXCLUSION AND FUTURE PRODUCT HANDLING")
    print("=" * 60)
    
    # Initialize the system
    coordinator = CommunicationCoordinator()
    analyzer = MarketTrendAnalyzer(coordinator)
    
    # Test: Search for Galaxy Fit 4 (future product)
    test_product = {
        'name': 'Galaxy Fit 4',
        'category': 'Wearables',
        'price': 120
    }
    
    print(f"Testing Self-Exclusion for: {test_product['name']}")
    print(f"Expected: Galaxy Fit 4 should NOT appear in its own similar products")
    
    # Set the product context
    analyzer.current_product_name = test_product['name']
    
    # Test future product year detection
    print(f"\nTesting Future Product Year Detection:")
    test_year = analyzer._estimate_launch_year_from_text("Galaxy Fit 4 review 2024", "Galaxy Fit 4")
    print(f"Galaxy Fit 4 estimated year: {test_year} (should be 2026, not 2024)")
    
    # Test self-exclusion in database
    print(f"\nTesting Database Self-Exclusion:")
    try:
        products = analyzer._get_samsung_product_database(
            test_product['category'], 
            test_product['price']
        )
        
        print(f"Found {len(products)} products from database:")
        galaxy_fit_4_found = False
        
        for product in products:
            if "fit 4" in product['name'].lower() or "fit4" in product['name'].lower():
                galaxy_fit_4_found = True
                print(f"ISSUE: {product['name']} found in results (should be excluded)")
            else:
                print(f"  ✅ {product['name']} (similarity: {product['similarity_score']:.3f})")
        
        if not galaxy_fit_4_found:
            print(f"✅ SUCCESS: Galaxy Fit 4 correctly excluded from its own results")
        else:
            print(f"❌ FAILURE: Galaxy Fit 4 still appears in its own results")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_self_exclusion()
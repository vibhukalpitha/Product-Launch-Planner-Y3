#!/usr/bin/env python3
"""
Test script to verify complete product family exclusion
- Galaxy Fit5 should NOT show any Galaxy Watch products at all
- Only fitness trackers should appear in results
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.market_trend_analyzer import MarketTrendAnalyzer
from agents.communication_coordinator import CommunicationCoordinator

def test_complete_exclusion():
    """Test that Galaxy Watch products are completely excluded from Galaxy Fit searches"""
    print("=" * 60)
    print("TESTING COMPLETE PRODUCT FAMILY EXCLUSION")
    print("=" * 60)
    
    # Initialize the system
    coordinator = CommunicationCoordinator()
    analyzer = MarketTrendAnalyzer(coordinator)
    
    # Test the Samsung database method directly (this is what shows in the UI)
    test_product = {
        'name': 'Galaxy Fit5',
        'category': 'Wearables',
        'price': 100
    }
    
    print(f"Testing Product: {test_product['name']}")
    print(f"Expected: Only fitness trackers, NO smartwatches")
    
    # Set the product context (this happens in analyze_market_trends)
    analyzer.current_product_name = test_product['name']
    
    print(f"\nUser Product Family: {analyzer._detect_product_family(test_product['name'])}")
    
    # Test the _get_samsung_products_database method
    print(f"\nCalling _get_samsung_products_database...")
    try:
        products = analyzer._get_samsung_products_database(
            test_product['category'], 
            test_product['price']
        )
        
        print(f"\nFound {len(products)} products:")
        print("-" * 50)
        
        fitness_trackers = 0
        smartwatches = 0
        other_products = 0
        
        for product in products:
            family = analyzer._detect_product_family(product['name'])
            if family == 'fitness_tracker':
                status = "✅ PASS"
                fitness_trackers += 1
            elif family == 'smartwatch':
                status = "❌ FAIL - SHOULD BE EXCLUDED!"
                smartwatches += 1
            else:
                status = "⚠️ OTHER"
                other_products += 1
            
            print(f"{product['name']:25} | {family:15} | {product['estimated_price']:>4} | {product['similarity_score']:.3f} | {status}")
        
        print(f"\n📊 SUMMARY:")
        print(f"Fitness Trackers: {fitness_trackers}")
        print(f"Smartwatches: {smartwatches}")
        print(f"Other Products: {other_products}")
        
        if smartwatches == 0:
            print(f"✅ SUCCESS: No smartwatches found in results!")
        else:
            print(f"❌ FAILURE: {smartwatches} smartwatches still appear in results!")
        
        if fitness_trackers > 0:
            print(f"✅ SUCCESS: {fitness_trackers} fitness trackers found")
        else:
            print(f"⚠️ WARNING: No fitness trackers found")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_complete_exclusion()
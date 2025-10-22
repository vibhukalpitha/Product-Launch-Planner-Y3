#!/usr/bin/env python3
"""
Test script to verify strict product family separation
- Galaxy Fit4 should only show fitness trackers (Galaxy Fit series)
- Galaxy Watch products should get very low similarity scores (0.05)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.market_trend_analyzer import MarketTrendAnalyzer
from agents.communication_coordinator import CommunicationCoordinator

def test_strict_family_separation():
    """Test the strict product family separation"""
    print("=" * 60)
    print("TESTING STRICT PRODUCT FAMILY SEPARATION")
    print("=" * 60)
    
    # Initialize the system
    coordinator = CommunicationCoordinator()
    analyzer = MarketTrendAnalyzer(coordinator)
    
    # Test product: Galaxy Fit4 (fitness tracker)
    test_product = {
        'name': 'Galaxy Fit4',
        'category': 'Wearables',
        'price': 120  # Correct price
    }
    
    print(f"\n🧪 Testing Product: {test_product['name']}")
    print(f"Expected Family: fitness_tracker")
    
    # Set the product context
    analyzer.current_product_name = test_product['name']
    
    # Test products to compare against
    test_products = [
        ('Galaxy Fit 4', 'Wearables', 130),     # Same product (should be highest)
        ('Galaxy Fit 3', 'Wearables', 100),     # Same family (should be high)
        ('Galaxy Fit 2', 'Wearables', 80),      # Same family (should be high)
        ('Galaxy Watch 7', 'Wearables', 400),   # Different family (should be very low)
        ('Galaxy Watch 6', 'Wearables', 350),   # Different family (should be very low)
        ('Galaxy Watch 5', 'Wearables', 300),   # Different family (should be very low)
        ('Galaxy Buds 3', 'Wearables', 180),    # Different family (should be low)
    ]
    
    print(f"\n📊 Similarity Scores:")
    print("-" * 50)
    
    results = []
    for product_name, category, price in test_products:
        # Calculate similarity
        similarity = analyzer._calculate_product_similarity(
            product_name, category, price, test_product['price']
        )
        
        # Detect product family
        family = analyzer._detect_product_family(product_name)
        
        results.append((product_name, similarity, family, price))
        
        print(f"{product_name:20} | {similarity:.3f} | {family:15} | ${price}")
    
    # Sort by similarity (highest first)
    results.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\n🏆 RANKING (Highest to Lowest Similarity):")
    print("-" * 55)
    for i, (name, similarity, family, price) in enumerate(results, 1):
        status = "✅" if family == 'fitness_tracker' else "❌" if family == 'smartwatch' else "⚠️"
        print(f"{i}. {name:20} | {similarity:.3f} | {family:15} | {status}")
    
    # Validation
    print(f"\n🔍 VALIDATION:")
    fitness_trackers = [(name, sim) for name, sim, family, _ in results if family == 'fitness_tracker']
    smartwatches = [(name, sim) for name, sim, family, _ in results if family == 'smartwatch']
    
    if fitness_trackers:
        best_fitness = max(fitness_trackers, key=lambda x: x[1])
        print(f"✅ Best Fitness Tracker: {best_fitness[0]} ({best_fitness[1]:.3f})")
    
    if smartwatches:
        best_smartwatch = max(smartwatches, key=lambda x: x[1])
        print(f"❌ Best Smartwatch: {best_smartwatch[0]} ({best_smartwatch[1]:.3f})")
        
        # Check if smartwatches have very low scores
        if best_smartwatch[1] < 0.1:
            print(f"✅ PASS: Smartwatches have very low similarity ({best_smartwatch[1]:.3f} < 0.1)")
        else:
            print(f"❌ FAIL: Smartwatches still have high similarity ({best_smartwatch[1]:.3f} >= 0.1)")
    
    # Check if fitness trackers rank higher than smartwatches
    if fitness_trackers and smartwatches:
        if best_fitness[1] > best_smartwatch[1]:
            gap = best_fitness[1] - best_smartwatch[1]
            print(f"✅ PASS: Fitness trackers rank higher (gap: {gap:.3f})")
        else:
            print(f"❌ FAIL: Smartwatches still rank higher!")
    
    return results

if __name__ == "__main__":
    test_strict_family_separation()
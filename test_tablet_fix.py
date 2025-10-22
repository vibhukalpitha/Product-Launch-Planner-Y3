#!/usr/bin/env python3
"""
Quick test of the tablet category fix
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

from agents.market_trend_analyzer import MarketTrendAnalyzer
from agents.communication_coordinator import coordinator

def test_tablet_filtering():
    """Test that tablet products are now properly accepted"""
    
    analyzer = MarketTrendAnalyzer(coordinator)
    
    # Test products that should be accepted for tablets
    test_products = [
        "Galaxy Tab S11 Ultra",
        "Galaxy Tab S12 Ultra", 
        "Galaxy Tab A9",
        "iPad Pro",  # Should be filtered out
        "Galaxy Watch8",  # Should be filtered out for tablets
        "Galaxy Tab S9 Ultra"
    ]
    
    print("🧪 Testing Tablet Category Filtering Fix")
    print("=" * 50)
    
    for product in test_products:
        result = analyzer._is_valid_samsung_product(product, "Tablets")
        status = "✅ ACCEPTED" if result else "❌ REJECTED"
        print(f"{status}: {product}")
    
    print("\n💡 Expected results:")
    print("✅ Galaxy Tab products should be ACCEPTED for Tablets category")
    print("❌ Galaxy Watch/iPad should be REJECTED for Tablets category")

if __name__ == "__main__":
    test_tablet_filtering()
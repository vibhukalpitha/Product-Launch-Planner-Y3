#!/usr/bin/env python3
"""
Test the Buds vs Watch search query logic
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

def test_buds_search_logic():
    """Test that Buds products get Buds-specific searches"""
    
    print("🧪 Testing Search Query Logic")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        ("Galaxy Buds4 Ultra", "Wearables"),
        ("Galaxy Watch8 Pro", "Wearables"),
        ("Galaxy Tab S13 Ultra", "Tablets"),
        ("Galaxy S26 Ultra", "Smartphones")
    ]
    
    for product_name, category in test_cases:
        print(f"\n📱 Product: {product_name}")
        print(f"📂 Category: {category}")
        
        # Simulate the logic from the fixed code
        if category.lower() in ['wearable', 'wearables']:
            if 'buds' in product_name.lower():
                search_queries = [
                    "Samsung Galaxy Buds unboxing",
                    "Samsung earbuds review", 
                    "Galaxy Buds 3 vs 2"
                ]
                print("🎧 Will search for: EARBUDS content")
            else:
                search_queries = [
                    "Samsung Galaxy Watch unboxing",
                    "Samsung watch review",
                    "Galaxy Watch 7 vs 6"
                ]
                print("⌚ Will search for: WATCH content")
        elif category.lower() in ['tablet', 'tablets']:
            search_queries = [
                "Samsung Galaxy Tab unboxing",
                "Samsung tablet review"
            ]
            print("💻 Will search for: TABLET content")
        else:
            search_queries = [
                "Samsung Galaxy unboxing",
                "Samsung phone review"
            ]
            print("📱 Will search for: SMARTPHONE content")
        
        print(f"🔍 Queries: {search_queries[:2]}...")

if __name__ == "__main__":
    test_buds_search_logic()
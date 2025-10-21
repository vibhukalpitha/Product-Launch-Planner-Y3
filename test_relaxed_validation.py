#!/usr/bin/env python3
"""
Quick Fix for Samsung Product Discovery
Temporarily patches the validation to be less strict
"""
import sys
import os
sys.path.append('.')

def patch_product_validation():
    """Temporarily make product validation less strict"""
    from agents.market_trend_analyzer import MarketTrendAnalyzer
    
    # Backup original method
    original_is_valid = MarketTrendAnalyzer._is_valid_samsung_product
    
    def relaxed_validation(self, product_name: str, target_category: str = None) -> bool:
        """Relaxed validation for Samsung products"""
        product_lower = product_name.lower()
        
        # Must contain Galaxy
        has_galaxy = 'galaxy' in product_lower
        
        # Must contain a model indicator
        model_indicators = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's0',
                          'note', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a0',
                          'z fold', 'z flip', 'tab', 'watch', 'buds', 'book',
                          'ultra', 'plus', 'fe']
        has_model_indicator = any(indicator in product_lower for indicator in model_indicators)
        
        # Filter out clearly invalid patterns (relaxed)
        invalid_patterns = ['amazon', 'https', 'http', 'www', '.com', 'affiliate', 'subscribe']
        has_invalid_pattern = any(pattern in product_lower for pattern in invalid_patterns)
        
        # Relaxed length check
        is_reasonable_length = 5 <= len(product_name) <= 100
        
        result = has_galaxy and has_model_indicator and not has_invalid_pattern and is_reasonable_length
        
        if result:
            print(f"✅ Found: {product_name}")
        else:
            print(f"❌ Filtered: {product_name} (galaxy:{has_galaxy}, model:{has_model_indicator}, invalid:{has_invalid_pattern})")
        
        return result
    
    # Apply patch
    MarketTrendAnalyzer._is_valid_samsung_product = relaxed_validation
    print("🔧 Applied relaxed validation patch")
    
    return original_is_valid

def test_enhanced_discovery():
    """Test Samsung product discovery with relaxed validation"""
    # Apply patch
    original_method = patch_product_validation()
    
    try:
        from agents.market_trend_analyzer import MarketTrendAnalyzer
        
        # Create test instance
        class MockCoordinator:
            def register_agent(self, name, agent): pass
        
        analyzer = MarketTrendAnalyzer(MockCoordinator())
        
        print("\n🔍 TESTING ENHANCED DISCOVERY WITH RELAXED VALIDATION:")
        print("=" * 60)
        
        # Test similar product discovery
        result = analyzer.discover_samsung_similar_products(
            'Galaxy S25 Ultra', 
            'Smartphones', 
            1199.0
        )
        
        print(f"\n✅ RESULTS:")
        print(f"📱 Similar products found: {len(result['found_products'])}")
        print(f"📊 Data sources: {result['data_sources']}")
        
        if result['found_products']:
            print(f"\n📋 PRODUCTS DISCOVERED:")
            for i, product in enumerate(result['found_products'], 1):
                name = product.get('name', 'Unknown')
                price = product.get('estimated_price', 'N/A')
                source = product.get('source', 'Unknown')
                print(f"   {i}. {name} (${price}) - {source}")
        
        print(f"\n🎯 IMPROVEMENT:")
        print(f"Before patch: 1 product")
        print(f"After patch: {len(result['found_products'])} products")
        
        if len(result['found_products']) > 5:
            print("🚀 SUCCESS! Now finding multiple Samsung products!")
        
    finally:
        # Restore original method
        MarketTrendAnalyzer._is_valid_samsung_product = original_method
        print("\n🔄 Restored original validation method")

if __name__ == "__main__":
    test_enhanced_discovery()
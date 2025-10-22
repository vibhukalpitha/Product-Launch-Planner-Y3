"""
Test Behavioral Customer Segmentation with Real Similar Products
===============================================================
This script tests the new behavioral segmentation that creates
Tech Enthusiasts, Value Seekers, Brand Loyalists, Conservative Buyers
based on real similar products data from market analyzer APIs
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.customer_segmentation_agent import CustomerSegmentationAgent
import json
from datetime import datetime

class MockCoordinator:
    """Mock coordinator for testing"""
    def __init__(self):
        self.agents = {}
    
    def register_agent(self, name, agent):
        self.agents[name] = agent

def test_behavioral_segmentation():
    """Test the new behavioral segmentation functionality"""
    
    print("🧪 Testing Behavioral Customer Segmentation")
    print("=" * 60)
    
    # Create mock coordinator and agent
    coordinator = MockCoordinator()
    segmentation_agent = CustomerSegmentationAgent(coordinator)
    
    # Sample product info
    product_info = {
        'name': 'Samsung Galaxy S26 Ultra',
        'category': 'smartphones',
        'price': 1199,
        'target_audience': {
            'age_groups': ['25-34', '35-44'],
            'platforms': ['Instagram', 'YouTube', 'Facebook']
        }
    }
    
    # Sample similar products data (simulates market analyzer API results)
    market_data = {
        'similar_products': [
            {'name': 'Samsung Galaxy S25 Ultra', 'estimated_price': 1099, 'category': 'smartphones'},
            {'name': 'Samsung Galaxy S25 Plus', 'estimated_price': 899, 'category': 'smartphones'},
            {'name': 'Samsung Galaxy S25', 'estimated_price': 699, 'category': 'smartphones'},
            {'name': 'Samsung Galaxy Z Fold 5', 'estimated_price': 1599, 'category': 'smartphones'},
            {'name': 'Samsung Galaxy Z Flip 5', 'estimated_price': 999, 'category': 'smartphones'},
            {'name': 'Samsung Galaxy S24 Ultra', 'estimated_price': 999, 'category': 'smartphones'},
            {'name': 'Samsung Galaxy Note 23', 'estimated_price': 1149, 'category': 'smartphones'},
            {'name': 'Samsung Galaxy A54', 'estimated_price': 399, 'category': 'smartphones'},
            {'name': 'Samsung Galaxy A34', 'estimated_price': 299, 'category': 'smartphones'},
            {'name': 'Samsung Galaxy S23 Plus', 'estimated_price': 799, 'category': 'smartphones'}
        ]
    }
    
    print(f"📱 Product: {product_info['name']} (${product_info['price']})")
    print(f"📊 Similar Products: {len(market_data['similar_products'])}")
    print(f"💰 Price Range: ${min([p['estimated_price'] for p in market_data['similar_products']])}-${max([p['estimated_price'] for p in market_data['similar_products']])}")
    print()
    
    try:
        # Run behavioral segmentation
        print("🔄 Running behavioral segmentation...")
        result = segmentation_agent.segment_customers(
            product_info=product_info,
            market_data=market_data
        )
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            return
        
        # Display results
        print(f"✅ Segmentation completed successfully!")
        print(f"📊 Segmentation Type: {result['segmentation_type']}")
        print(f"🎯 Total Segments Created: {result['total_segments_created']}")
        print(f"📡 Data Sources: {', '.join(result.get('data_sources', []))}")
        print()
        
        # Show segment details
        print("📋 BEHAVIORAL SEGMENT ANALYSIS:")
        print("-" * 50)
        
        for segment_name, segment_data in result['customer_segments'].items():
            print(f"\n🎯 {segment_name}")
            print(f"   Market Share: {segment_data['percentage']:.1f}%")
            print(f"   Market Size: {segment_data['size'] / 1_000_000:.1f}M customers")
            print(f"   Attractiveness Score: {segment_data['attractiveness_score']:.3f}")
            
            characteristics = segment_data['characteristics']
            print(f"   Tech Adoption: {characteristics['tech_adoption']:.1%}")
            print(f"   Price Sensitivity: {characteristics['price_sensitivity']:.1%}")
            print(f"   Brand Loyalty: {characteristics['brand_loyalty']:.1%}")
            
            if 'real_data_basis' in segment_data:
                basis = segment_data['real_data_basis']
                print(f"   Real Data Basis: {list(basis.keys())}")
        
        # Show recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        print("-" * 50)
        for i, recommendation in enumerate(result['recommendations'], 1):
            print(f"{i}. {recommendation}")
        
        # Show visualizations available
        if 'visualizations' in result:
            viz = result['visualizations']
            print(f"\n📈 VISUALIZATIONS AVAILABLE:")
            print("-" * 50)
            for viz_type in viz.keys():
                print(f"   ✅ {viz_type.replace('_', ' ').title()}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error during segmentation: {e}")
        import traceback
        traceback.print_exc()
        return None

def show_implementation_guide():
    """Show how behavioral segmentation works"""
    
    print("\n" + "=" * 60)
    print("📚 BEHAVIORAL SEGMENTATION IMPLEMENTATION GUIDE")
    print("=" * 60)
    
    print("""
🎯 HOW BEHAVIORAL SEGMENTATION WORKS:

1. REAL DATA INPUT:
   ✅ Similar products from Market Analyzer APIs
   ✅ Price analysis of competing products
   ✅ Feature analysis from product names
   ✅ Brand preference analysis
   ✅ Real Census data for market sizing

2. BEHAVIORAL SEGMENTS CREATED:
   🔧 Tech Enthusiasts - Premium product buyers, latest features
   💰 Value Seekers - Budget-conscious, price-sensitive buyers
   🏆 Brand Loyalists - Samsung/brand focused, reliability important
   🛡️ Conservative Buyers - Traditional, proven features preferred

3. REAL DATA ANALYSIS:
   • Premium Rate: % of similar products above average price
   • Budget Rate: % of similar products below average price  
   • Brand Rate: % of Samsung products in similar products
   • Market Size: Real Census Bureau population data

4. SEGMENT CHARACTERISTICS (Based on Real Data):
   • Tech Adoption Rate (real behavior patterns)
   • Price Sensitivity (from similar product analysis)
   • Brand Loyalty (from Samsung product frequency)
   • Social Media Usage (demographic research)
   • Income Levels (Census + consumer research)

5. ATTRACTIVENESS SCORING:
   • Market size factor (real Census population)
   • Price fit (product price vs segment sensitivity)
   • Tech adoption alignment
   • Weighted calculation for business priority
""")

if __name__ == "__main__":
    result = test_behavioral_segmentation()
    show_implementation_guide()
    
    if result:
        print(f"\n🚀 SUCCESS! Behavioral segmentation working with:")
        print(f"   • {result['total_segments_created']} behavioral segments")
        print(f"   • Real similar products analysis")
        print(f"   • {result['segmentation_type']} methodology")
        print(f"   • API-based market sizing")
"""
Test Gender + Age Customer Segmentation
=====================================
This script demonstrates the new gender + age based customer segmentation
using real API data from Census Bureau, Facebook Marketing API, etc.
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

def test_gender_age_segmentation():
    """Test the new gender + age segmentation functionality"""
    
    print("🧪 Testing Gender + Age Customer Segmentation")
    print("=" * 60)
    
    # Create mock coordinator and agent
    coordinator = MockCoordinator()
    segmentation_agent = CustomerSegmentationAgent(coordinator)
    
    # Sample product info with gender + age targeting
    product_info = {
        'name': 'Samsung Galaxy Buds Pro',
        'category': 'wearables',
        'price': 249,
        'target_audience': {
            'age_groups': ['25-34', '35-44', '18-24'],  # Multiple age groups
            'genders': ['Male', 'Female'],  # NEW: Gender segmentation
            'platforms': ['Instagram', 'YouTube', 'Facebook']  # Optional platforms
        }
    }
    
    # Sample market data
    market_data = {
        'similar_products': [
            {'name': 'Samsung Galaxy Buds 2', 'estimated_price': 199},
            {'name': 'Samsung Galaxy Watch 4', 'estimated_price': 329},
            {'name': 'Samsung Galaxy Fit 2', 'estimated_price': 89},
            {'name': 'Samsung Galaxy Buds Live', 'estimated_price': 169}
        ]
    }
    
    print(f"📱 Product: {product_info['name']}")
    print(f"🎯 Age Groups: {product_info['target_audience']['age_groups']}")
    print(f"👥 Genders: {product_info['target_audience']['genders']}")
    print(f"📱 Platforms: {product_info['target_audience']['platforms']}")
    print()
    
    try:
        # Run gender + age segmentation
        print("🔄 Running gender + age segmentation...")
        result = segmentation_agent.segment_customers(
            product_info=product_info,
            market_data=market_data
        )
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            print()
            print("💡 This is expected if you don't have real API keys configured.")
            print("   The system will use enhanced demographic modeling instead.")
            return
        
        # Display results
        print(f"✅ Segmentation completed successfully!")
        print(f"📊 Segmentation Type: {result['segmentation_type']}")
        print(f"🎯 Total Segments Created: {result['total_segments_created']}")
        print()
        
        # Show segment details
        print("📋 SEGMENT ANALYSIS:")
        print("-" * 50)
        
        for segment_name, segment_data in result['customer_segments'].items():
            print(f"\n🎯 {segment_name}")
            print(f"   Gender: {segment_data.get('gender', 'N/A')}")
            if 'age_range' in segment_data:
                age_range = segment_data['age_range']
                print(f"   Age Range: {age_range['min']}-{age_range['max']} years")
            print(f"   Market Size: {segment_data.get('market_size_millions', 0):.2f}M customers")
            print(f"   Attractiveness Score: {segment_data.get('attractiveness_score', 0):.3f}")
            
            if 'preferences' in segment_data:
                prefs = segment_data['preferences']
                print(f"   Top Features: {', '.join(prefs.get('feature_priorities', [])[:3])}")
                print(f"   Price Preference: {prefs.get('price_preference', 'N/A')}")
        
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
        
    except Exception as e:
        print(f"❌ Error during segmentation: {e}")
        print()
        print("💡 SOLUTION STEPS:")
        print("   1. Ensure you have Census Bureau API key")
        print("   2. Set up Facebook Marketing API access")
        print("   3. Configure demographic data connectors")
        print("   4. Update .env file with API keys")

def show_implementation_guide():
    """Show how to implement gender + age segmentation"""
    
    print("\n" + "=" * 60)
    print("📚 IMPLEMENTATION GUIDE")
    print("=" * 60)
    
    print("""
🎯 HOW TO USE GENDER + AGE SEGMENTATION:

1. UPDATE PRODUCT INFO:
   product_info = {
       'target_audience': {
           'age_groups': ['25-34', '35-44'],  # Age ranges
           'genders': ['Male', 'Female'],     # NEW: Genders
           'platforms': ['Instagram', 'Facebook']  # Optional
       }
   }

2. API DATA SOURCES:
   ✅ Census Bureau API - Population by age & gender
   ✅ Facebook Marketing API - Audience demographics  
   ✅ Google Analytics - Website visitor demographics
   ✅ Consumer Expenditure Survey - Spending patterns
   ✅ Social Media APIs - Platform preferences by gender

3. SEGMENTS CREATED:
   • Male 25-34
   • Female 25-34  
   • Male 35-44
   • Female 35-44
   
4. DATA PROVIDED PER SEGMENT:
   • Real population size from Census
   • Gender-specific behaviors & preferences
   • Purchase patterns by age & gender
   • Platform usage by demographics
   • Pricing sensitivity analysis
   • Attractiveness scoring

5. VISUALIZATIONS:
   • Gender distribution pie chart
   • Age group performance bars
   • Market size by segment
   • Attractiveness matrix scatter plot
   • Segment comparison charts
""")

if __name__ == "__main__":
    test_gender_age_segmentation()
    show_implementation_guide()
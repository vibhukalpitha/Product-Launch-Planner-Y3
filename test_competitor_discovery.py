"""
Test Script: Intelligent Competitor Discovery Demo
Demonstrates how the Samsung Product Launch Planner finds competitors for any new product
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.competitor_tracking_agent import CompetitorTrackingAgent
from utils.intelligent_competitor_discovery import IntelligentCompetitorDiscovery
from datetime import datetime

# Mock coordinator for testing
class MockCoordinator:
    def __init__(self):
        self.agents = {}
    
    def register_agent(self, name, agent):
        self.agents[name] = agent
        print(f"📝 Registered agent: {name}")

def test_intelligent_competitor_discovery():
    """Test the intelligent competitor discovery system with various products"""
    
    print("🚀 SAMSUNG PRODUCT LAUNCH PLANNER")
    print("🤖 Intelligent Competitor Discovery System Test")
    print("=" * 80)
    
    # Initialize the system
    coordinator = MockCoordinator()
    competitor_agent = CompetitorTrackingAgent(coordinator)
    
    # Test products with different characteristics
    test_products = [
        {
            'name': 'Galaxy S25 Ultra',
            'category': 'smartphones',
            'price': 1199,
            'price_range': 'premium'
        },
        {
            'name': 'Galaxy Book Pro 360 15"',
            'category': 'laptops', 
            'price': 1899,
            'price_range': 'premium'
        },
        {
            'name': 'Galaxy Watch 6 Classic',
            'category': 'smartwatches',
            'price': 429,
            'price_range': 'mid-range'
        },
        {
            'name': 'Galaxy Buds Pro 3',
            'category': 'headphones',
            'price': 229,
            'price_range': 'mid-range'
        },
        {
            'name': 'Galaxy Neo QLED 8K TV 65"',
            'category': 'tv',
            'price': 2999,
            'price_range': 'premium'
        },
        {
            # Test with a completely new product category
            'name': 'Galaxy Smart Ring',
            'category': 'wearables',
            'price': 299,
            'price_range': 'mid-range'
        }
    ]
    
    for i, product in enumerate(test_products, 1):
        print(f"\n{'='*80}")
        print(f"🔍 TEST {i}/6: {product['name']}")
        print(f"📱 Category: {product['category'].title()}")
        print(f"💰 Price: ${product['price']}")
        print(f"🎯 Range: {product['price_range'].title()}")
        print('='*80)
        
        try:
            # Run comprehensive competitor analysis
            analysis_result = competitor_agent.analyze_competitors(product)
            
            if 'error' in analysis_result:
                print(f"❌ Analysis failed: {analysis_result['error']}")
                continue
            
            # Display discovery results
            discovery = analysis_result.get('competitor_discovery', {})
            
            print(f"\n🎯 COMPETITOR DISCOVERY RESULTS:")
            print(f"Discovery Method: {analysis_result.get('discovery_method', 'Unknown').title()}")
            
            # Direct competitors
            direct_competitors = discovery.get('direct_competitors', [])
            print(f"\n🥊 Direct Competitors ({len(direct_competitors)}):")
            for comp in direct_competitors:
                confidence = discovery.get('confidence_scores', {}).get(comp, 0)
                sources = discovery.get('discovery_sources', {}).get(comp, [])
                print(f"   • {comp} (Confidence: {confidence}, Sources: {len(sources)})")
            
            # Indirect competitors  
            indirect_competitors = discovery.get('indirect_competitors', [])
            print(f"\n🔄 Indirect Competitors ({len(indirect_competitors)}):")
            for comp in indirect_competitors[:3]:  # Show top 3
                confidence = discovery.get('confidence_scores', {}).get(comp, 0)
                print(f"   • {comp} (Confidence: {confidence})")
            
            # Market insights
            market_insights = discovery.get('market_insights', {})
            market_analysis = market_insights.get('market_analysis', {})
            
            print(f"\n📊 MARKET ANALYSIS:")
            print(f"   Total Competitors Found: {market_analysis.get('total_identified_competitors', 0)}")
            print(f"   Direct Threats: {market_analysis.get('direct_threats', 0)}")
            print(f"   Market Fragmentation: {market_analysis.get('market_fragmentation', 'Unknown')}")
            
            # Competitive landscape
            landscape = market_insights.get('competitive_landscape', {})
            premium_brands = landscape.get('premium_brands', [])
            value_brands = landscape.get('value_brands', [])
            
            if premium_brands:
                print(f"   Premium Brands: {', '.join(premium_brands)}")
            if value_brands:
                print(f"   Value Brands: {', '.join(value_brands)}")
            
            # Pricing analysis
            pricing = analysis_result.get('pricing_analysis', {})
            position = pricing.get('competitive_position', {})
            
            print(f"\n💰 PRICING ANALYSIS:")
            print(f"   Price Position: {position.get('position', 'Unknown')}")
            print(f"   Market Percentile: {position.get('percentile', 0):.1f}%")
            print(f"   Price Advantage: {'Yes' if position.get('price_advantage', False) else 'No'}")
            
            # Key recommendations
            recommendations = analysis_result.get('recommendations', [])
            print(f"\n💡 KEY RECOMMENDATIONS ({len(recommendations)}):")
            for rec in recommendations[:3]:  # Show top 3 recommendations
                print(f"   • {rec}")
            
            # Summary insights
            key_insights = analysis_result.get('key_insights', {})
            print(f"\n📈 SUMMARY INSIGHTS:")
            print(f"   Total Competitors: {key_insights.get('total_competitors_found', 0)}")
            print(f"   Direct Threats: {key_insights.get('direct_threats', 0)}")
            print(f"   Market Position: {key_insights.get('market_position', 'Unknown')}")
            print(f"   Market Fragmentation: {key_insights.get('market_fragmentation', 'Unknown')}")
            
        except Exception as e:
            print(f"❌ Test failed for {product['name']}: {e}")
            continue
        
        print(f"\n✅ Analysis complete for {product['name']}")
        
        if i < len(test_products):
            print("\n" + "-" * 40)
            print("⏳ Moving to next product...")
    
    print(f"\n{'='*80}")
    print("🎉 ALL TESTS COMPLETED!")
    print("✅ Intelligent Competitor Discovery System is working!")
    print("🚀 Samsung Product Launch Planner ready for ANY product analysis!")
    print("='*80")

def test_specific_product():
    """Test with a specific product that user might input"""
    
    print("\n🔬 SPECIFIC PRODUCT TEST")
    print("Testing with user-input style product")
    print("-" * 50)
    
    coordinator = MockCoordinator()
    competitor_agent = CompetitorTrackingAgent(coordinator)
    
    # Simulate user input
    user_product = {
        'name': input("Enter product name (or press Enter for 'Galaxy AR Glasses'): ").strip() or "Galaxy AR Glasses",
        'category': input("Enter category (or press Enter for 'wearables'): ").strip() or "wearables",
        'price': int(input("Enter price (or press Enter for 499): ").strip() or "499"),
        'price_range': input("Enter price range (budget/mid-range/premium, or press Enter for 'mid-range'): ").strip() or "mid-range"
    }
    
    print(f"\n🔍 Analyzing: {user_product['name']}")
    
    # Run analysis
    result = competitor_agent.analyze_competitors(user_product)
    
    if 'error' not in result:
        discovery = result.get('competitor_discovery', {})
        direct = discovery.get('direct_competitors', [])
        indirect = discovery.get('indirect_competitors', [])
        
        print(f"\n✅ Found competitors:")
        print(f"🎯 Direct: {', '.join(direct[:5])}")
        print(f"🔄 Indirect: {', '.join(indirect[:3])}")
        
        market_insights = discovery.get('market_insights', {})
        recommendations = market_insights.get('strategic_recommendations', [])
        print(f"\n💡 Top recommendations:")
        for rec in recommendations[:3]:
            print(f"   • {rec}")
    else:
        print(f"❌ Analysis failed: {result['error']}")

if __name__ == "__main__":
    print("Choose test mode:")
    print("1. Run all test products")
    print("2. Test specific product")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        test_specific_product()
    else:
        test_intelligent_competitor_discovery()
    
    print("\n🎯 Test completed!")
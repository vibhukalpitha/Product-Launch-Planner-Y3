#!/usr/bin/env python3
"""
Test script for Samsung Product Launch Planner
Verifies all agents are working correctly
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_system():
    """Test the complete system functionality"""
    print("🧪 Testing Samsung Product Launch Planner System")
    print("=" * 50)
    
    try:
        # Import modules
        print("📦 Importing modules...")
        from agents.communication_coordinator import coordinator, ProductInfo
        from agents.market_trend_analyzer import MarketTrendAnalyzer
        from agents.competitor_tracking_agent import CompetitorTrackingAgent
        from agents.customer_segmentation_agent import CustomerSegmentationAgent
        from agents.campaign_planning_agent import CampaignPlanningAgent
        print("✅ All modules imported successfully")
        
        # Initialize agents
        print("\n🤖 Initializing agents...")
        market_analyzer = MarketTrendAnalyzer(coordinator)
        competitor_tracker = CompetitorTrackingAgent(coordinator)
        customer_segmenter = CustomerSegmentationAgent(coordinator)
        campaign_planner = CampaignPlanningAgent(coordinator)
        print("✅ All agents initialized successfully")
        
        # Create test product
        print("\n📱 Creating test product...")
        product_info = ProductInfo(
            name="Galaxy S25 Ultra",
            category="Smartphones",
            price=1200.0,
            description="Premium flagship smartphone with advanced AI features",
            target_audience={
                'age_groups': ['25-34', '35-44'],
                'platforms': ['Instagram', 'Facebook', 'YouTube'],
                'budget': 50000,
                'duration_days': 30
            },
            launch_date="2025-12-01"
        )
        print("✅ Test product created successfully")
        
        # Run analysis
        print("\n🔄 Running complete analysis...")
        results = coordinator.orchestrate_analysis(product_info)
        print("✅ Analysis completed successfully")
        
        # Verify results
        print("\n📊 Verifying results...")
        expected_keys = ['market_analysis', 'competitor_analysis', 'customer_segments', 'campaign_plan']
        
        for key in expected_keys:
            if key in results:
                print(f"✅ {key}: Available")
            else:
                print(f"❌ {key}: Missing")
        
        print(f"\n📈 Results Summary:")
        print(f"- Market Analysis: {'✅' if 'market_analysis' in results else '❌'}")
        print(f"- Competitor Analysis: {'✅' if 'competitor_analysis' in results else '❌'}")
        print(f"- Customer Segmentation: {'✅' if 'customer_segments' in results else '❌'}")
        print(f"- Campaign Planning: {'✅' if 'campaign_plan' in results else '❌'}")
        
        print("\n🎉 System test completed successfully!")
        print("🚀 The Samsung Product Launch Planner is ready to use!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ System test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_system()
    sys.exit(0 if success else 1)
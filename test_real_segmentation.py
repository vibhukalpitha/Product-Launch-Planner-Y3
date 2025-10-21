#!/usr/bin/env python3
"""
Test Real API-Based Customer Segmentation
=========================================
Test the new segmentation system that creates segments based on user inputs and real API data.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.customer_segmentation_agent import CustomerSegmentationAgent
from agents.communication_coordinator import CommunicationCoordinator
from agents.market_trend_analyzer import MarketTrendAnalyzer
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ProductInfo:
    name: str
    category: str
    price: float
    description: str
    target_audience: Dict[str, Any]
    launch_date: str

def test_real_segmentation():
    """Test the real API-based customer segmentation"""
    
    print("🎯 TESTING REAL API-BASED CUSTOMER SEGMENTATION")
    print("=" * 60)
    
    # Initialize agents
    coordinator = CommunicationCoordinator()
    market_analyzer = MarketTrendAnalyzer(coordinator)
    customer_segmenter = CustomerSegmentationAgent(coordinator)
    
    # Test product with your example inputs
    product_info = ProductInfo(
        name="Galaxy Buds Pro 3",
        category="wearables",
        price=250.0,
        description="Premium wireless earbuds with noise cancellation",
        target_audience={
            'age_groups': ['25-34', '35-44'],
            'platforms': ['Facebook', 'Instagram', 'YouTube'],
            'budget': 50000,
            'duration_days': 30
        },
        launch_date="2025-12-01"
    )
    
    print(f"📱 Product: {product_info.name}")
    print(f"💰 Price: ${product_info.price}")
    print(f"🎯 Target Age Groups: {product_info.target_audience['age_groups']}")
    print(f"📱 Target Platforms: {product_info.target_audience['platforms']}")
    
    # Get market data first (similar products for analysis)
    print(f"\n🔍 Getting similar Samsung products for analysis...")
    market_data = market_analyzer.analyze_market_trends({
        'name': product_info.name,
        'category': product_info.category,
        'price': product_info.price,
        'description': product_info.description
    })
    
    # Run segmentation with real API data
    print(f"\n📊 Running real API-based customer segmentation...")
    segmentation_results = customer_segmenter.segment_customers(
        product_info.__dict__,
        market_data=market_data
    )
    
    # Display results
    print(f"\n" + "=" * 60)
    print(f"📊 REAL SEGMENTATION RESULTS")
    print("=" * 60)
    
    if 'error' in segmentation_results:
        print(f"❌ Error: {segmentation_results['error']}")
        return
    
    segments = segmentation_results.get('customer_segments', {})
    
    print(f"\n🎯 CREATED SEGMENTS: {len(segments)}")
    print(f"Segmentation Type: {segmentation_results.get('segmentation_type', 'Unknown')}")
    
    if segmentation_results.get('segmentation_type') == 'real_api_based':
        print(f"✅ SUCCESS: Using real API-based segmentation!")
        print(f"📊 Input Age Groups: {segmentation_results.get('input_age_groups', [])}")
        print(f"📱 Input Platforms: {segmentation_results.get('input_platforms', [])}")
        
        expected_segments = []
        for age in product_info.target_audience['age_groups']:
            for platform in product_info.target_audience['platforms']:
                expected_segments.append(f"{age} {platform}")
        
        print(f"\n📋 EXPECTED SEGMENTS:")
        for segment in expected_segments:
            print(f"   • {segment}")
        
        print(f"\n📊 ACTUAL SEGMENTS CREATED:")
        for segment_name, data in segments.items():
            print(f"\n🎯 {segment_name}:")
            print(f"   Age Range: {data['age_range']['min']}-{data['age_range']['max']}")
            print(f"   Platform: {data['platform']}")
            print(f"   Market Size: {data['market_size_millions']:.1f}M potential customers")
            print(f"   Attractiveness Score: {data['attractiveness_score']:.3f}")
            print(f"   Market Share: {data['percentage']:.1f}%")
            print(f"   Price Segment: {data['pricing_preferences']['price_segment']}")
            print(f"   Top Features: {', '.join(data['preferences']['feature_priorities'][:2])}")
            print(f"   Data Sources: {', '.join(data['data_sources'])}")
        
        # Show recommendations
        recommendations = segmentation_results.get('recommendations', [])
        if recommendations:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in recommendations:
                print(f"   • {rec}")
        
        # Verify all expected segments were created
        created_segments = set(segments.keys())
        expected_segments_set = set(expected_segments)
        
        if created_segments == expected_segments_set:
            print(f"\n🏆 PERFECT! All expected segments created:")
            print(f"   ✅ Expected: {len(expected_segments)} segments")
            print(f"   ✅ Created: {len(segments)} segments")
            print(f"   ✅ Match: 100%")
        else:
            missing = expected_segments_set - created_segments
            extra = created_segments - expected_segments_set
            print(f"\n⚠️ Segment mismatch:")
            if missing:
                print(f"   Missing: {missing}")
            if extra:
                print(f"   Extra: {extra}")
    
    else:
        print(f"⚠️ Using traditional clustering fallback")
        print(f"📊 Traditional Segments:")
        for name, data in segments.items():
            print(f"   • {name}: {data.get('percentage', 'N/A')}%")
    
    print("=" * 60)
    
    return segmentation_results

if __name__ == "__main__":
    results = test_real_segmentation()
    if results and results.get('segmentation_type') == 'real_api_based':
        print("🎉 Real API-based segmentation test PASSED!")
    else:
        print("⚠️ Test completed but may need adjustments")
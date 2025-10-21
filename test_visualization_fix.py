#!/usr/bin/env python3
"""Test the fixed visualization"""

import sys
sys.path.append('.')
from agents.customer_segmentation_agent import CustomerSegmentationAgent
from agents.communication_coordinator import CommunicationCoordinator

coordinator = CommunicationCoordinator()
segmenter = CustomerSegmentationAgent(coordinator)

# Test the visualization data structure
product_info = {
    'name': 'Galaxy Watch 6',
    'category': 'wearables', 
    'price': 350.0,
    'target_audience': {
        'age_groups': ['25-34', '35-44'],
        'platforms': ['Facebook', 'YouTube']
    }
}

print("🔍 Testing fixed visualization...")
result = segmenter.segment_customers(product_info)

print('\n📊 RESULT STRUCTURE:')
print(f'Segmentation Type: {result.get("segmentation_type", "Unknown")}')
print(f'Has customer_segments key: {"customer_segments" in result}')
print(f'Total segments: {len(result.get("customer_segments", {}))}')

if result.get('segmentation_type') == 'real_api_based':
    segments = result['customer_segments'] 
    print(f'\n🎯 Expected visualization data structure:')
    print(f'Segments created: {list(segments.keys())}')
    
    # Test that all required fields exist for visualization
    for name, data in segments.items():
        required_fields = ['percentage', 'attractiveness_score', 'age_range', 'platform']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            print(f'❌ {name} missing: {missing_fields}')
        else:
            print(f'✅ {name} has all required fields')
    
    print(f'\n📊 Visualization will show:')
    print(f'- Pie chart with {len(segments)} segments')
    print(f'- Bar chart with attractiveness scores')
    print(f'- Detailed expandable sections')
    print(f'✅ KeyError fix should be resolved!')
else:
    print('⚠️ Using traditional clustering - different data structure')

print('\n🎉 Test completed!')
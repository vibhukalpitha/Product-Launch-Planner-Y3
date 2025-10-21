#!/usr/bin/env python3
"""Quick test of real segmentation"""

import sys
sys.path.append('.')
from agents.customer_segmentation_agent import CustomerSegmentationAgent
from agents.communication_coordinator import CommunicationCoordinator

coordinator = CommunicationCoordinator()
segmenter = CustomerSegmentationAgent(coordinator)

# Test with your example inputs
product_info = {
    'name': 'Galaxy Buds Pro 3',
    'category': 'wearables', 
    'price': 250.0,
    'target_audience': {
        'age_groups': ['25-34', '35-44'],
        'platforms': ['Facebook', 'Instagram', 'YouTube']
    }
}

print("🔍 Testing real segmentation...")
result = segmenter.segment_customers(product_info)

print('\n📊 SEGMENTATION RESULT:')
print(f'Type: {result.get("segmentation_type", "Unknown")}')
print(f'Success: {"error" not in result}')

if 'customer_segments' in result:
    segments = result['customer_segments']
    print(f'Segments created: {len(segments)}')
    
    print('\n🎯 SEGMENTS:')
    for name, data in segments.items():
        print(f'  • {name}')
        print(f'    Market Share: {data.get("percentage", 0):.1f}%')
        print(f'    Attractiveness: {data.get("attractiveness_score", 0):.3f}')
        if 'age_range' in data:
            print(f'    Age: {data["age_range"]["min"]}-{data["age_range"]["max"]}')
        if 'platform' in data:
            print(f'    Platform: {data["platform"]}')
else:
    print(f'❌ Error: {result.get("error", "Unknown error")}')
#!/usr/bin/env python3
"""
Diagnostic Tool: Check Current Segmentation Data Type
====================================================
This checks what type of segmentation data is currently being displayed.
"""

import sys
sys.path.append('.')
from agents.customer_segmentation_agent import CustomerSegmentationAgent
from agents.communication_coordinator import CommunicationCoordinator

coordinator = CommunicationCoordinator()
segmenter = CustomerSegmentationAgent(coordinator)

# Test with example inputs that should trigger real API segmentation
product_info = {
    'name': 'Galaxy Buds 3 Pro',
    'category': 'wearables', 
    'price': 250.0,
    'target_audience': {
        'age_groups': ['25-34', '35-44'],
        'platforms': ['Facebook', 'Instagram', 'YouTube']
    }
}

print("🔍 TESTING WHAT TYPE OF SEGMENTATION IS ACTIVE")
print("=" * 60)

result = segmenter.segment_customers(product_info)

print(f"📊 Segmentation Type: {result.get('segmentation_type', 'Unknown')}")
print(f"📊 Segments Created: {len(result.get('customer_segments', {}))}")

if 'customer_segments' in result:
    segments = result['customer_segments']
    print(f"\n🎯 SEGMENT NAMES:")
    for name in segments.keys():
        print(f"   • {name}")
    
    # Check if we see the old traditional names
    traditional_names = ['Tech Enthusiasts', 'Value Seekers', 'Brand Loyalists', 'Conservative Buyers']
    real_api_patterns = ['25-34', '35-44', 'Facebook', 'Instagram', 'YouTube']
    
    has_traditional = any(name in traditional_names for name in segments.keys())
    has_real_api = any(any(pattern in name for pattern in real_api_patterns) for name in segments.keys())
    
    print(f"\n📋 ANALYSIS:")
    if has_traditional:
        print("❌ SHOWING TRADITIONAL CLUSTERING (Tech Enthusiasts, etc.)")
        print("💡 This is the OLD mock data system")
    elif has_real_api:
        print("✅ SHOWING REAL API-BASED SEGMENTATION")
        print("💡 This is the NEW real data system")
    else:
        print("❓ Unknown segmentation type")
    
    print(f"\n💾 TO SEE REAL DATA IN YOUR APP:")
    print("1. Go to the Product Strategy tab")
    print("2. Enter your age groups: 25-34, 35-44")
    print("3. Select platforms: Facebook, Instagram, YouTube") 
    print("4. Click 'Launch Analysis' button")
    print("5. Check Customer Analytics tab for real segments")

else:
    print("❌ No customer segments found in result")
    
print("=" * 60)
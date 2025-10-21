#!/usr/bin/env python3
"""
Multi-Key API Test - Demonstrating Group Project Benefits
=========================================================
"""

import requests
import os
from dotenv import load_dotenv
from utils.multi_key_manager import get_api_key, record_api_usage, multi_key_manager

def test_multi_key_rotation():
    """Test multi-key rotation in action"""
    
    load_dotenv()
    
    print("🔄 MULTI-KEY ROTATION DEMONSTRATION")
    print("=" * 50)
    
    # Test YouTube API rotation
    print("\n📺 YOUTUBE API - KEY ROTATION TEST")
    print("-" * 40)
    
    for i in range(5):
        key = get_api_key('YOUTUBE')
        if key:
            key_preview = key[:20] + "..."
            print(f"Request {i+1}: Using key {key_preview}")
            
            # Simulate API call success/failure
            success = True  # In real usage, this would be based on API response
            record_api_usage(key, success)
        else:
            print(f"Request {i+1}: No key available")
    
    # Show current capacity
    print("\n📊 CURRENT GROUP API CAPACITY:")
    print("-" * 35)
    
    summary = multi_key_manager.get_service_summary()
    
    for service, info in summary.items():
        key_count = info['total_keys']
        limit = info['estimated_daily_limit']
        
        if key_count > 0:
            status = "✅ ACTIVE"
            multiplier = f" ({key_count}x keys)" if key_count > 1 else ""
        else:
            status = "⚠️ NEEDS GROUP KEYS"
            multiplier = " (Add member keys for 4x capacity!)"
            
        print(f"{service:15} {status:15} {limit}{multiplier}")
    
    # Calculate potential vs current
    print("\n🎯 GROUP PROJECT POTENTIAL:")
    print("-" * 30)
    
    potential_limits = {
        'YOUTUBE': '40,000 requests/day (4 keys)',
        'NEWS_API': '400 requests/day (4 keys)', 
        'ALPHA_VANTAGE': '100 requests/day (4 keys)',
        'SERP_API': '400 searches/month (4 keys)',
        'FRED': 'Unlimited + 4x backup (4 keys)'
    }
    
    for service, potential in potential_limits.items():
        current_keys = summary[service]['total_keys']
        if current_keys == 1:
            print(f"📈 {service}: Current 1 key → Target: {potential}")
        elif current_keys > 1:
            print(f"✅ {service}: {current_keys} keys active - GOOD!")
        else:
            print(f"🔴 {service}: 0 keys → URGENT: Get {potential}")
    
    print("\n" + "=" * 50)
    print("💡 RECOMMENDATION FOR GROUP:")
    print("Each member should get 5 API keys (15 min total)")
    print("Result: 5x capacity + professional reliability!")
    print("=" * 50)

if __name__ == "__main__":
    test_multi_key_rotation()
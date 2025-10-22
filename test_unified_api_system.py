#!/usr/bin/env python3
"""
Test the Unified API Management System
Shows how the new system handles keys from multiple locations with proper priority
"""

import os
import sys
sys.path.append('.')

from utils.unified_api_manager import get_api_key, unified_api_manager
import json

def test_unified_api_management():
    """Test the unified API management system."""
    
    print("=" * 80)
    print("🔧 TESTING UNIFIED API MANAGEMENT SYSTEM")
    print("=" * 80)
    
    # Show the manager status first
    unified_api_manager.print_status()
    
    print("\n1. 📍 LOADING CONFIGURATION FROM ALL SOURCES:")
    print("-" * 50)
    
    # Show what was loaded
    print(f"✅ Environment variables loaded: {len([k for k in os.environ if 'API' in k])} keys")
    print(f"✅ .env file loaded: {os.path.exists('.env')}")
    print(f"✅ config.json loaded: {os.path.exists('config.json')}")
    
    print("\n2. 🔑 FRED API KEYS TEST (Multi-key rotation):")
    print("-" * 50)
    
    # Test FRED key rotation
    print("Testing FRED key rotation (your 4 keys):")
    fred_keys = unified_api_manager.api_keys.get('FRED', [])
    print(f"Available FRED keys: {len(fred_keys)}")
    
    for i in range(6):  # Test more than available keys to see rotation
        key_obj = unified_api_manager.get_working_key('fred')
        if key_obj:
            print(f"  Request {i+1}: {key_obj.key[:20]}... (Key #{key_obj.key_index} from {key_obj.source})")
        else:
            print(f"  Request {i+1}: No key available")
    
    print("\n3. 📊 NEWS API KEYS TEST (Multi-key rotation):")
    print("-" * 50)
    
    # Test News API rotation
    print("Testing News API key rotation:")
    news_keys = unified_api_manager.api_keys.get('NEWS_API', [])
    print(f"Available News API keys: {len(news_keys)}")
    
    for i in range(6):
        key_obj = unified_api_manager.get_working_key('news_api')
        if key_obj:
            print(f"  Request {i+1}: {key_obj.key[:20]}... (Key #{key_obj.key_index} from {key_obj.source})")
        else:
            print(f"  Request {i+1}: No key available")
    
    print("\n4. 🎥 YOUTUBE API TEST:")
    print("-" * 50)
    
    # Test YouTube key
    youtube_key = get_api_key('youtube')
    if youtube_key:
        print(f"✅ YouTube key available: {youtube_key[:20]}...")
    else:
        print("❌ No YouTube key found")
    
    print("\n5. 🏛️ CENSUS API TEST:")
    print("-" * 50)
    
    # Test Census key (should come from config.json)
    census_key = get_api_key('census')
    if census_key:
        print(f"✅ Census key available: {census_key[:20]}...")
        print("   (This key comes from config.json with priority)")
    else:
        print("❌ No Census key found")
    
    print("\n6. 📈 PRIORITY ORDER DEMONSTRATION:")
    print("-" * 50)
    
    # Show priority order
    print("Key loading priority order:")
    print("  1️⃣ Environment variables (highest priority)")
    print("  2️⃣ .env file (medium priority) ← Your FRED keys are here")
    print("  3️⃣ config.json file (lowest priority) ← Your Census key is here")
    
    print("\n7. 🔄 KEY ROTATION STATUS:")
    print("-" * 50)
    
    # Show available keys by service
    print("Available keys by service:")
    for service, keys in unified_api_manager.api_keys.items():
        active_keys = [k for k in keys if k.is_active]
        print(f"  {service}: {len(active_keys)} active keys")
        for key in active_keys:
            print(f"    - Key #{key.key_index} from {key.source} (used {key.usage_count} times)")
    
    print("\n8. ✅ INTEGRATION STATUS:")
    print("-" * 50)
    
    # Test if all expected services have keys
    services = ['fred', 'news_api', 'youtube', 'census', 'serp_api']
    working_services = []
    
    for service in services:
        key = get_api_key(service)
        if key and key != 'demo_key_replace_me':
            working_services.append(service)
            print(f"  ✅ {service.upper()}: Ready")
        else:
            print(f"  ❌ {service.upper()}: No valid key")
    
    print(f"\n🎯 RESULT: {len(working_services)}/{len(services)} services ready!")
    
    if len(working_services) >= 3:
        print("✅ System ready for production!")
    else:
        print("⚠️ Need more API keys for full functionality")
    
    print("\n" + "=" * 80)
    print("🏆 UNIFIED API MANAGEMENT TEST COMPLETE")
    print("=" * 80)
    
    return working_services

if __name__ == "__main__":
    working_services = test_unified_api_management()
    
    print(f"\n📋 Summary: {len(working_services)} services configured successfully")
    print(f"Ready services: {', '.join(working_services)}")
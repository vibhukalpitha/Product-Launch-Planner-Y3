"""
Test API Rotation System - Live Test
Tests that the rotation system is actually being used by the real_data_connector
"""

import sys
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

print("=" * 80)
print("[TEST] API ROTATION LIVE TEST")
print("=" * 80)

# Test imports
try:
    from utils.api_key_rotator import api_key_rotator, get_rotated_api_key
    print("[OK] API Key Rotator imported successfully")
except Exception as e:
    print(f"[ERROR] Could not import API Key Rotator: {e}")
    sys.exit(1)

try:
    from utils.real_data_connector import real_data_connector
    print("[OK] Real Data Connector imported successfully")
except Exception as e:
    print(f"[ERROR] Could not import Real Data Connector: {e}")
    sys.exit(1)

print("\n" + "=" * 80)
print("[STATUS] Initial API Key Status")
print("=" * 80)
api_key_rotator.print_status()

print("\n" + "=" * 80)
print("[TEST] Testing YouTube API with Rotation")
print("=" * 80)
print("\nMaking YouTube API call...")
print("This will attempt to use rotated keys if primary key is rate-limited\n")

result = real_data_connector.get_youtube_metrics("Samsung Galaxy S24 review")

if result and result.get('success'):
    print(f"\n[SUCCESS] YouTube API call succeeded!")
    print(f"  Videos found: {result.get('total_results', 0)}")
    print(f"  Query: {result.get('query')}")
    if result.get('videos'):
        print(f"  First video: {result['videos'][0].get('title', 'N/A')}")
else:
    print(f"\n[INFO] YouTube API call did not return data")
    print(f"  This is expected if all keys are rate-limited")
    print(f"  Check the logs above to see if rotation was attempted")

print("\n" + "=" * 80)
print("[TEST] Testing News API with Rotation")
print("=" * 80)
print("\nMaking News API call...")
print("This will attempt to use rotated keys if primary key is rate-limited\n")

result = real_data_connector.get_news_data("Samsung Galaxy smartphone", page_size=5)

if result and result.get('success'):
    print(f"\n[SUCCESS] News API call succeeded!")
    print(f"  Articles found: {result.get('total_results', 0)}")
    print(f"  Query: {result.get('query')}")
    if result.get('articles'):
        print(f"  First article: {result['articles'][0].get('title', 'N/A')[:80]}...")
else:
    print(f"\n[INFO] News API call did not return data")
    print(f"  This is expected if all keys are rate-limited")
    print(f"  Check the logs above to see if rotation was attempted")

print("\n" + "=" * 80)
print("[STATUS] Final API Key Status")
print("=" * 80)
api_key_rotator.print_status()

print("\n" + "=" * 80)
print("[SUMMARY] Test Complete")
print("=" * 80)
print("\nWhat to look for in the logs above:")
print("  1. [CALL] messages showing API attempts")
print("  2. [ROTATE] messages indicating key rotation")
print("  3. Attempt numbers (attempt 1, attempt 2, etc.)")
print("  4. [OK] or [ERROR] results for each attempt")
print("\nIf you see [ROTATE] messages, the rotation system is working!")
print("=" * 80)


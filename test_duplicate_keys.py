#!/usr/bin/env python3
"""Test the duplicate key fix"""

print("🔧 TESTING DUPLICATE KEY FIX")
print("=" * 50)

# Read the streamlit app file and check for unique keys
with open('ui/streamlit_app.py', 'r') as f:
    content = f.read()

# Extract all chart keys
import re
key_pattern = r'key="([^"]+)"'
keys = re.findall(key_pattern, content)

print(f"📊 Found {len(keys)} chart keys")

# Check for duplicates
key_counts = {}
for key in keys:
    key_counts[key] = key_counts.get(key, 0) + 1

duplicates = {k: v for k, v in key_counts.items() if v > 1}

if duplicates:
    print("\n❌ DUPLICATE KEYS FOUND:")
    for key, count in duplicates.items():
        print(f"   {key}: {count} occurrences")
else:
    print("\n✅ NO DUPLICATE KEYS FOUND!")

print(f"\n📋 All chart keys:")
unique_keys = sorted(set(keys))
for key in unique_keys:
    count = key_counts[key]
    status = "✅" if count == 1 else "❌"
    print(f"   {status} {key} ({count}x)")

# Check for key_prefix usage
prefix_usage = len([k for k in keys if '{key_prefix}' in content])
print(f"\n🔧 Key prefix system: {'✅ Active' if '{key_prefix}' in content else '❌ Not used'}")

print("=" * 50)
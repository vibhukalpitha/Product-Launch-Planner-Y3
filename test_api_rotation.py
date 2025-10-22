"""
Test API Key Rotation System
"""

from utils.api_key_rotator import (
    api_key_rotator,
    get_rotated_api_key,
    handle_rate_limit,
    get_api_key_status
)

print("=" * 60)
print("🧪 Testing API Key Rotation System")
print("=" * 60)

# Test 1: Check if module loaded
print("\n✅ Test 1: Module Import")
print("   API Key Rotator loaded successfully!")

# Test 2: Print current status
print("\n📊 Test 2: Current API Key Status")
api_key_rotator.print_status()

# Test 3: Try to get a key
print("\n🔑 Test 3: Get API Key")

for api_name in ['news_api', 'youtube', 'serpapi']:
    key = get_rotated_api_key(api_name)
    if key:
        print(f"   ✅ {api_name}: Got key ending in ...{key[-4:]}")
    else:
        print(f"   ⚠️ {api_name}: No keys configured (this is normal if not in .env)")

# Test 4: Test rotation logic
print("\n🔄 Test 4: Test Key Rotation")

# Check if any keys are loaded
if api_key_rotator.api_keys:
    # Get first API that has keys
    for api_name, keys in api_key_rotator.api_keys.items():
        if keys:
            print(f"   Testing rotation for: {api_name}")
            print(f"   Total keys available: {len(keys)}")
            
            # Get first key
            key1 = get_rotated_api_key(api_name)
            print(f"   First key: ...{key1[-4:]}")
            
            # Simulate rate limit
            print(f"   Simulating rate limit on first key...")
            handle_rate_limit(api_name, key1, duration_hours=24)
            
            # Try to get next key
            key2 = get_rotated_api_key(api_name)
            if key2:
                if key1 != key2:
                    print(f"   ✅ Rotation successful! Now using: ...{key2[-4:]}")
                else:
                    print(f"   ⚠️ Only one key available, got same key")
            else:
                print(f"   ⚠️ All keys are rate limited")
            
            break
else:
    print("   ⚠️ No API keys configured yet")
    print("   Add keys to your .env file to test rotation")

# Test 5: Status check
print("\n📈 Test 5: Get Status for Specific API")

for api_name in ['news_api', 'youtube', 'serpapi']:
    if api_name in api_key_rotator.api_keys:
        status = get_api_key_status(api_name)
        print(f"\n   {api_name.upper()}:")
        print(f"   - Total keys: {status['total_keys']}")
        print(f"   - Available: {status['available_keys']}")
        print(f"   - Current: Key #{status['current_key_index']}")

print("\n" + "=" * 60)
print("🎉 All tests completed!")
print("=" * 60)

print("\n📝 Next Steps:")
print("1. Add API keys to your .env file:")
print("   NEWS_API_KEY=your_key_here")
print("   NEWS_API_KEY_1=your_second_key_here")
print("   NEWS_API_KEY_2=your_third_key_here")
print("\n2. Restart your application")
print("3. The rotation will work automatically!")
print("\n4. Monitor with: api_key_rotator.print_status()")


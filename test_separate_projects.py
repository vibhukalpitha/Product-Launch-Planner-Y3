#!/usr/bin/env python3
"""
Separate Projects Verification Test
===================================
Test YouTube API keys to verify they come from different Google Cloud projects
"""

import requests
import os
from dotenv import load_dotenv
import time
import json

def test_separate_projects():
    """Test if YouTube keys are from separate projects"""
    
    load_dotenv()
    
    print("🔍 SEPARATE PROJECTS VERIFICATION TEST")
    print("=" * 50)
    
    youtube_keys = [
        ("Member 1 (Original)", "YOUTUBE_API_KEY_1", os.getenv('YOUTUBE_API_KEY_1')),
        ("Member 2 (Should be NEW)", "YOUTUBE_API_KEY_2", os.getenv('YOUTUBE_API_KEY_2')),
        ("Member 3 (Should be NEW)", "YOUTUBE_API_KEY_3", os.getenv('YOUTUBE_API_KEY_3')),
        ("Member 4 (Should be NEW)", "YOUTUBE_API_KEY_4", os.getenv('YOUTUBE_API_KEY_4'))
    ]
    
    results = []
    
    for member_name, key_name, key_value in youtube_keys:
        print(f"\n📺 Testing {member_name}")
        print(f"Key: {key_name}")
        print("-" * 40)
        
        if not key_value or "your_group_member" in key_value:
            print("⚠️ Key not configured yet")
            results.append({"member": member_name, "status": "not_configured", "working": False})
            continue
            
        print(f"API Key: {key_value[:25]}...")
        
        try:
            # Test with a minimal request
            url = 'https://www.googleapis.com/youtube/v3/search'
            params = {
                'part': 'snippet',
                'q': 'Samsung',
                'maxResults': 1,
                'key': key_value
            }
            
            response = requests.get(url, params=params, timeout=15)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ SUCCESS: Key is working perfectly!")
                if 'items' in data and data['items']:
                    title = data['items'][0]['snippet']['title'][:50]
                    print(f"✅ Found video: {title}...")
                results.append({"member": member_name, "status": "working", "working": True})
                
            elif response.status_code == 403:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', {}).get('message', '')
                    
                    if 'quota' in error_msg.lower():
                        print("⚠️ Quota exceeded (but key is valid)")
                        print("✅ This means the key is REAL and working")
                        results.append({"member": member_name, "status": "quota_exceeded", "working": True})
                    else:
                        print(f"❌ Permission error: {error_msg}")
                        results.append({"member": member_name, "status": "permission_error", "working": False})
                        
                except json.JSONDecodeError:
                    print(f"❌ 403 Error: {response.text[:100]}")
                    results.append({"member": member_name, "status": "error", "working": False})
                    
            elif response.status_code == 400:
                print("❌ Invalid API key")
                results.append({"member": member_name, "status": "invalid_key", "working": False})
            else:
                print(f"❌ HTTP {response.status_code}: {response.text[:100]}")
                results.append({"member": member_name, "status": "other_error", "working": False})
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
            results.append({"member": member_name, "status": "request_failed", "working": False})
        
        # Wait between tests to avoid rate limiting
        print("⏳ Waiting 5 seconds before next test...")
        time.sleep(5)
    
    # Analyze results
    analyze_project_separation(results)

def analyze_project_separation(results):
    """Analyze if projects are properly separated"""
    
    print("\n" + "=" * 50)
    print("📊 SEPARATE PROJECTS ANALYSIS")
    print("=" * 50)
    
    working_keys = [r for r in results if r["working"]]
    total_keys = len(results)
    working_count = len(working_keys)
    
    print(f"\n🎯 SUMMARY:")
    print(f"Working keys: {working_count}/{total_keys}")
    
    # Check if multiple keys are working (indicates separate projects)
    if working_count >= 2:
        print("✅ EXCELLENT: Multiple keys working independently!")
        print("🚀 This suggests separate projects are working!")
        
        # Check for mix of working and quota exceeded
        quota_exceeded = [r for r in results if r["status"] == "quota_exceeded"]
        actually_working = [r for r in results if r["status"] == "working"]
        
        if len(actually_working) > 0 and len(quota_exceeded) > 0:
            print("🏆 PERFECT: Mixed status confirms separate projects!")
            print("   - Some keys working = separate quota pools")
            print("   - Some quota exceeded = different project limits")
        
    elif working_count == 1:
        print("⚠️ Only 1 key working - may still be same project")
        print("💡 Need more members to create separate projects")
        
    else:
        print("❌ No keys working - check configuration")
    
    print(f"\n📈 CAPACITY ANALYSIS:")
    if working_count == 4:
        print("🏆 MAXIMUM CAPACITY: 40,000 requests/day")
        print("🚀 Enterprise-level YouTube API access!")
    elif working_count == 3:
        print("💪 HIGH CAPACITY: 30,000 requests/day")
        print("⬆️ Add 1 more member for maximum capacity")
    elif working_count == 2:
        print("✅ GOOD CAPACITY: 20,000 requests/day")
        print("⬆️ Add 2 more members for maximum capacity")
    elif working_count == 1:
        print("⚠️ BASIC CAPACITY: 10,000 requests/day")
        print("⬆️ Need group members to create separate projects")
    else:
        print("❌ NO CAPACITY: All keys failing")
    
    print(f"\n💡 RECOMMENDATIONS:")
    
    not_configured = [r for r in results if r["status"] == "not_configured"]
    if not_configured:
        print("🔧 IMMEDIATE ACTIONS:")
        for result in not_configured:
            member = result["member"]
            print(f"   • {member}: Create Google Cloud project & generate key")
    
    failing_keys = [r for r in results if not r["working"] and r["status"] != "not_configured"]
    if failing_keys:
        print("🔍 TROUBLESHOOT:")
        for result in failing_keys:
            member = result["member"]
            status = result["status"]
            print(f"   • {member}: {status} - check project setup")
    
    if working_count >= 2:
        print("🎉 STRATEGY SUCCESS: Separate projects working!")
    
    print("=" * 50)

if __name__ == "__main__":
    test_separate_projects()
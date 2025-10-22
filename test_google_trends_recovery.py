"""
Google Trends Recovery Test Script
Run this to check if Google Trends rate limiting has been lifted
"""

from pytrends.request import TrendReq
import time
from datetime import datetime

def test_google_trends_recovery():
    """Test if Google Trends is accessible"""
    print(f"\n{'='*60}")
    print(f"🧪 Google Trends Recovery Test")
    print(f"⏰ Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    try:
        print("📡 Attempting to connect to Google Trends...")
        pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25))
        
        print("🔍 Building test query for 'Samsung Galaxy'...")
        pytrends.build_payload(['Samsung Galaxy'], timeframe='now 7-d')
        
        print("📊 Fetching data...")
        data = pytrends.interest_over_time()
        
        if data is not None and not data.empty:
            print("\n✅ SUCCESS - Google Trends is RECOVERED!")
            print(f"   📈 Received {len(data)} data points")
            print(f"   📅 Date range: {data.index[0]} to {data.index[-1]}")
            print(f"\n🟢 STATUS: You can now use Google Trends API")
            print(f"⚠️  RECOMMENDATION: Use optimized settings to avoid re-blocking")
            return True
        else:
            print("\n⚠️  LIMITED ACCESS - Connected but no data returned")
            print(f"🟡 STATUS: Partially recovered, wait 1-2 more hours")
            return False
            
    except Exception as e:
        error_str = str(e)
        
        if '429' in error_str or 'Too Many Requests' in error_str:
            print(f"\n❌ STILL BLOCKED - Rate limit active")
            print(f"   Error: {error_str[:100]}")
            print(f"\n🔴 STATUS: Still rate limited")
            print(f"⏱️  WAIT: Try again in 2-4 hours")
            return False
            
        elif 'timeout' in error_str.lower():
            print(f"\n⚠️  TIMEOUT - Connection slow or blocked")
            print(f"🟡 STATUS: Network issue or partial block")
            return False
            
        else:
            print(f"\n⚠️  ERROR - {error_str[:150]}")
            print(f"🟡 STATUS: Unknown issue")
            return False

def continuous_monitoring(interval_minutes=30, max_attempts=12):
    """
    Monitor Google Trends recovery status
    
    Args:
        interval_minutes: Minutes between checks (default: 30)
        max_attempts: Maximum number of checks (default: 12 = 6 hours)
    """
    print(f"\n{'='*60}")
    print(f"🔄 Starting Continuous Monitoring")
    print(f"⏱️  Check Interval: Every {interval_minutes} minutes")
    print(f"🎯 Max Duration: {max_attempts * interval_minutes / 60:.1f} hours")
    print(f"{'='*60}")
    
    for attempt in range(1, max_attempts + 1):
        print(f"\n\n📍 CHECK #{attempt}/{max_attempts}")
        
        recovered = test_google_trends_recovery()
        
        if recovered:
            print(f"\n🎉 RECOVERY COMPLETE!")
            print(f"⏰ Total wait time: {(attempt - 1) * interval_minutes} minutes")
            print(f"✅ You can now run your analysis")
            break
        else:
            if attempt < max_attempts:
                wait_seconds = interval_minutes * 60
                print(f"\n⏳ Waiting {interval_minutes} minutes before next check...")
                print(f"   (Press Ctrl+C to stop monitoring)")
                try:
                    time.sleep(wait_seconds)
                except KeyboardInterrupt:
                    print(f"\n\n⏸️  Monitoring stopped by user")
                    break
    else:
        print(f"\n\n⏰ Monitoring period complete")
        print(f"   If still blocked, wait longer or change VPN location")

if __name__ == "__main__":
    import sys
    
    print("\n" + "="*60)
    print("🔬 Google Trends Recovery Checker")
    print("="*60)
    print("\nOptions:")
    print("  1. Single test (check once)")
    print("  2. Monitor every 30 minutes (up to 6 hours)")
    print("  3. Monitor every 60 minutes (up to 12 hours)")
    print("="*60)
    
    choice = input("\nEnter choice (1/2/3) or press Enter for single test: ").strip()
    
    if choice == "2":
        continuous_monitoring(interval_minutes=30, max_attempts=12)
    elif choice == "3":
        continuous_monitoring(interval_minutes=60, max_attempts=12)
    else:
        # Single test
        recovered = test_google_trends_recovery()
        
        if not recovered:
            print(f"\n{'='*60}")
            print(f"💡 TIPS WHILE WAITING:")
            print(f"   • Your current block level: Medium (2-6 hour recovery)")
            print(f"   • Try again in 2-4 hours")
            print(f"   • Or switch VPN location for fresh IP")
            print(f"   • Run this script again to re-check")
            print(f"{'='*60}\n")


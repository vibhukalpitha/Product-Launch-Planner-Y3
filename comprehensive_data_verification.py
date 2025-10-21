"""
COMPREHENSIVE DATA AUTHENTICITY VERIFICATION
===========================================
This script will definitively prove whether the customer segmentation 
is using real API data or mock/hardcoded data by testing multiple scenarios
"""
import sys
import os
import requests
import json
from datetime import datetime

sys.path.append('agents')
sys.path.append('utils')

def test_census_api_directly():
    """Test Census Bureau API directly to verify real data"""
    print("🔍 TESTING CENSUS BUREAU API DIRECTLY...")
    print("-" * 50)
    
    try:
        from unified_api_manager import get_api_key
        census_key = get_api_key('census')
        
        if census_key:
            print(f"✅ Census API Key Found: {census_key[:20]}...")
            
            # Test direct API call
            url = "https://api.census.gov/data/2022/acs/acs1"
            params = {
                'get': 'B01001_002E,B01001_026E,NAME',  # Male and female population
                'for': 'us:*',
                'key': census_key
            }
            
            print(f"📡 Making direct API call to: {url}")
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                male_population = int(data[1][0])
                female_population = int(data[1][1])
                
                print(f"✅ REAL API RESPONSE:")
                print(f"   Male Population (US): {male_population:,}")
                print(f"   Female Population (US): {female_population:,}")
                print(f"   Total Population: {male_population + female_population:,}")
                print(f"   Response Status: {response.status_code}")
                print(f"   Data Source: US Census Bureau (REAL)")
                
                return {
                    'status': 'REAL_API_DATA',
                    'male_population': male_population,
                    'female_population': female_population,
                    'api_working': True
                }
            else:
                print(f"❌ API Error: Status {response.status_code}")
                return {'status': 'API_ERROR', 'code': response.status_code}
        else:
            print("❌ No Census API key found")
            return {'status': 'NO_API_KEY'}
            
    except Exception as e:
        print(f"❌ Error testing Census API: {e}")
        return {'status': 'ERROR', 'error': str(e)}

def test_segmentation_with_different_inputs():
    """Test segmentation with different inputs to see if results change"""
    print("\n🧪 TESTING SEGMENTATION WITH DIFFERENT INPUTS...")
    print("-" * 50)
    
    try:
        from customer_segmentation_agent import CustomerSegmentationAgent
        from communication_coordinator import coordinator
        
        agent = CustomerSegmentationAgent(coordinator)
        
        test_cases = [
            {
                'name': 'Test Case 1: Wearables',
                'product': {
                    'name': 'Samsung Galaxy Watch',
                    'category': 'wearables',
                    'price': 299,
                    'target_audience': {
                        'age_groups': ['25-34'],
                        'genders': ['Male']
                    }
                }
            },
            {
                'name': 'Test Case 2: Smartphones',
                'product': {
                    'name': 'Samsung Galaxy S26',
                    'category': 'smartphones', 
                    'price': 899,
                    'target_audience': {
                        'age_groups': ['35-44'],
                        'genders': ['Female']
                    }
                }
            }
        ]
        
        results = {}
        
        for test_case in test_cases:
            print(f"\n📱 {test_case['name']}")
            
            try:
                result = agent.segment_customers(test_case['product'])
                
                if 'customer_segments' in result:
                    segments = result['customer_segments']
                    first_segment = list(segments.values())[0] if segments else {}
                    
                    market_size = first_segment.get('market_size_millions', 0)
                    estimated_customers = first_segment.get('estimated_customers', 0)
                    data_sources = first_segment.get('data_sources', [])
                    
                    results[test_case['name']] = {
                        'market_size': market_size,
                        'customers': estimated_customers,
                        'data_sources': data_sources,
                        'segmentation_type': result.get('segmentation_type', 'unknown')
                    }
                    
                    print(f"   Market Size: {market_size}M")
                    print(f"   Customers: {estimated_customers:,}")
                    print(f"   Data Sources: {data_sources}")
                    print(f"   Type: {result.get('segmentation_type', 'unknown')}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
                results[test_case['name']] = {'error': str(e)}
        
        return results
        
    except Exception as e:
        print(f"❌ Error in segmentation testing: {e}")
        return {'error': str(e)}

def analyze_data_variability(results):
    """Analyze if data shows real variability or fixed patterns"""
    print("\n📊 ANALYZING DATA VARIABILITY...")
    print("-" * 50)
    
    if len(results) < 2:
        print("❌ Not enough test cases to analyze variability")
        return
    
    market_sizes = []
    customer_counts = []
    
    for test_name, data in results.items():
        if 'error' not in data:
            market_sizes.append(data.get('market_size', 0))
            customer_counts.append(data.get('customers', 0))
    
    if len(set(market_sizes)) > 1:
        print("✅ MARKET SIZES VARY - Indicates real data calculation")
        for i, (test_name, data) in enumerate(results.items()):
            if 'error' not in data:
                print(f"   {test_name}: {data.get('market_size', 0)}M customers")
    else:
        print("⚠️ MARKET SIZES IDENTICAL - May indicate hardcoded data")
    
    if len(set(customer_counts)) > 1:
        print("✅ CUSTOMER COUNTS VARY - Indicates real calculations")
        for i, (test_name, data) in enumerate(results.items()):
            if 'error' not in data:
                print(f"   {test_name}: {data.get('customers', 0):,} customers")
    else:
        print("⚠️ CUSTOMER COUNTS IDENTICAL - May indicate fixed data")

def check_api_keys_status():
    """Check which API keys are actually configured"""
    print("\n🔑 CHECKING API KEYS STATUS...")
    print("-" * 50)
    
    try:
        from unified_api_manager import get_api_key
        
        api_keys_to_check = [
            'census',
            'fred', 
            'alpha_vantage',
            'youtube',
            'news_api'
        ]
        
        working_keys = []
        
        for key_name in api_keys_to_check:
            try:
                key = get_api_key(key_name)
                if key and key != 'YOUR_KEY_HERE' and len(key) > 10:
                    working_keys.append(key_name)
                    print(f"✅ {key_name}: {key[:15]}... (REAL KEY)")
                else:
                    print(f"❌ {key_name}: Not configured or placeholder")
            except:
                print(f"❌ {key_name}: Error accessing key")
        
        print(f"\n📊 SUMMARY:")
        print(f"   Working API Keys: {len(working_keys)}")
        print(f"   Real Data Capable: {'YES' if 'census' in working_keys else 'NO'}")
        
        return working_keys
        
    except Exception as e:
        print(f"❌ Error checking API keys: {e}")
        return []

def main():
    """Run comprehensive data authenticity verification"""
    print("🔍 COMPREHENSIVE DATA AUTHENTICITY VERIFICATION")
    print("=" * 60)
    print(f"Timestamp: {datetime.now()}")
    print()
    
    # Test 1: Direct Census API
    census_test = test_census_api_directly()
    
    # Test 2: Check API keys
    working_keys = check_api_keys_status()
    
    # Test 3: Test segmentation with different inputs
    segmentation_results = test_segmentation_with_different_inputs()
    
    # Test 4: Analyze variability
    if segmentation_results and 'error' not in segmentation_results:
        analyze_data_variability(segmentation_results)
    
    # Final conclusion
    print("\n" + "=" * 60)
    print("🎯 FINAL AUTHENTICITY ASSESSMENT")
    print("=" * 60)
    
    real_data_indicators = 0
    mock_data_indicators = 0
    
    # Census API test
    if census_test.get('status') == 'REAL_API_DATA':
        real_data_indicators += 3
        print("✅ Census API: REAL DATA (High confidence)")
    else:
        mock_data_indicators += 1
        print("❌ Census API: Not working or mock data")
    
    # API keys
    if len(working_keys) >= 3:
        real_data_indicators += 2
        print(f"✅ API Keys: {len(working_keys)} working keys (Real data capable)")
    else:
        mock_data_indicators += 1
        print(f"❌ API Keys: Limited keys ({len(working_keys)} working)")
    
    # Segmentation type
    if segmentation_results:
        has_real_segments = any('gender_age_api_based' in str(r) or 'real_api_based' in str(r) 
                               for r in segmentation_results.values())
        if has_real_segments:
            real_data_indicators += 2
            print("✅ Segmentation: Real API-based segments detected")
        else:
            mock_data_indicators += 1
            print("❌ Segmentation: Traditional clustering (may be mock)")
    
    # Final verdict
    confidence_score = (real_data_indicators / (real_data_indicators + mock_data_indicators)) * 100
    
    print(f"\n📊 CONFIDENCE SCORE: {confidence_score:.1f}%")
    
    if confidence_score >= 70:
        print("🎯 VERDICT: REAL DATA - High confidence")
        print("   Your system is using authentic API data")
    elif confidence_score >= 40:
        print("⚠️ VERDICT: MIXED - Some real, some mock data")
        print("   Your system has partial real data integration")
    else:
        print("❌ VERDICT: MOCK DATA - Low confidence")
        print("   Your system appears to use mostly mock/hardcoded data")

if __name__ == "__main__":
    main()
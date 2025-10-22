"""
Test Wikipedia Regional API Integration
Verifies that Wikipedia Pageviews API is working correctly
"""

from utils.wikipedia_regional_api import wikipedia_api

def test_wikipedia_api():
    """Test Wikipedia Regional API for product interest"""
    
    print("\n" + "="*60)
    print("🧪 Testing Wikipedia Regional API")
    print("="*60 + "\n")
    
    # Test product
    product = "Samsung Galaxy"
    countries = ['US', 'JP', 'KR']
    
    print(f"Product: {product}")
    print(f"Testing countries: {', '.join(countries)}\n")
    print("─" * 60)
    
    results = {}
    
    for country in countries:
        try:
            print(f"\nTesting {country}...")
            interest = wikipedia_api.get_regional_interest(product, country)
            results[country] = interest
            
            # Interpret score
            if interest >= 80:
                level = "Very High"
            elif interest >= 60:
                level = "High"
            elif interest >= 40:
                level = "Medium"
            else:
                level = "Low"
            
            print(f"✅ {country}: {interest:.1f}/100 ({level} interest)")
            
        except Exception as e:
            print(f"❌ {country}: Error - {str(e)}")
            results[country] = None
    
    # Summary
    print("\n" + "="*60)
    print("📊 Summary")
    print("="*60)
    
    successful = [c for c, v in results.items() if v is not None]
    failed = [c for c, v in results.items() if v is None]
    
    if successful:
        print(f"\n✅ Successful: {len(successful)}/{len(countries)}")
        for country in successful:
            print(f"   • {country}: {results[country]:.1f}/100")
    
    if failed:
        print(f"\n❌ Failed: {len(failed)}/{len(countries)}")
        for country in failed:
            print(f"   • {country}")
    
    print("\n" + "="*60)
    
    if len(successful) == len(countries):
        print("✅ All tests passed!")
        print("🎉 Wikipedia Regional API is working perfectly!")
    elif len(successful) > 0:
        print("⚠️  Some tests passed, some failed")
        print("💡 Wikipedia API is partially working")
    else:
        print("❌ All tests failed")
        print("💡 Check your internet connection")
    
    print("="*60 + "\n")
    
    return len(successful) == len(countries)


if __name__ == "__main__":
    success = test_wikipedia_api()
    
    if success:
        print("✅ Ready to use in your system!")
        print("\nRun your Streamlit app:")
        print("  cd ui")
        print("  streamlit run streamlit_app.py")
    else:
        print("⚠️  Some issues detected")
        print("\nThe system will still work using fallback data")
        print("Wikipedia API will be used when available")


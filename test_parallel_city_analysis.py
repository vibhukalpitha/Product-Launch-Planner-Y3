"""
Test script to verify parallel city analysis with real APIs
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.market_trend_analyzer import MarketTrendAnalyzer
import time

# Mock coordinator for testing
class MockCoordinator:
    def __init__(self):
        self.agents = {}
    
    def register_agent(self, name, agent):
        self.agents[name] = agent
        print(f"[TEST] Registered agent: {name}")

def test_parallel_city_analysis():
    print("============================================================")
    print("🧪 Testing Parallel City Analysis with Real APIs")
    print("============================================================\n")
    
    # Initialize the analyzer with mock coordinator
    coordinator = MockCoordinator()
    analyzer = MarketTrendAnalyzer(coordinator)
    
    # Sample product category
    category = "smartphone"
    
    # Sample similar products (from real APIs)
    similar_products = [
        {
            'name': 'Samsung Galaxy S24',
            'price': 799,
            'source': 'News API',
            'relevance_score': 0.95
        },
        {
            'name': 'Samsung Galaxy S23',
            'price': 699,
            'source': 'YouTube API',
            'relevance_score': 0.90
        },
        {
            'name': 'Samsung Galaxy Z Flip 6',
            'price': 999,
            'source': 'News API',
            'relevance_score': 0.88
        }
    ]
    
    print(f"📱 Category: {category}")
    print(f"🔍 Similar Products: {len(similar_products)}")
    print(f"\n────────────────────────────────────────────────────────────\n")
    
    # Run the analysis
    print("🚀 Starting parallel city analysis...\n")
    start_time = time.time()
    
    result = analyzer.analyze_city_performance(category, similar_products)
    
    elapsed_time = time.time() - start_time
    
    print("\n────────────────────────────────────────────────────────────")
    print("✅ Analysis Complete!")
    print("============================================================\n")
    
    # Display results
    print("📊 RESULTS:")
    print(f"   • Cities Analyzed: {result.get('cities_analyzed', 0)}")
    print(f"   • Processing Time: {result.get('processing_time_seconds', 0)} seconds")
    print(f"   • Parallel Workers: {result.get('parallel_workers', 0)}")
    print(f"   • Data Source: {result.get('data_source', 'N/A')}")
    print(f"   • Confidence: {result.get('real_data_confidence', 'N/A')}")
    
    # Display top 5 cities
    print("\n🏆 TOP 5 CITIES:")
    top_cities = result.get('top_cities', [])[:5]
    for i, (city, sales) in enumerate(top_cities, 1):
        print(f"   {i}. {city}: {sales:,.0f} units")
    
    # Display API details for top 3 cities
    print("\n🌍 DETAILED API METRICS (Top 3):")
    city_api_details = result.get('city_api_details', {})
    for city, sales in top_cities[:3]:
        if city in city_api_details:
            details = city_api_details[city]
            print(f"\n   {city}:")
            print(f"      • Sales Volume: {sales:,.0f} units")
            print(f"      • Regional Interest: {details.get('regional_interest', 0):.1f}/100")
            print(f"      • YouTube Factor: {details.get('youtube_factor', 1.0):.2f}x")
            print(f"      • News Factor: {details.get('news_factor', 1.0):.2f}x")
            print(f"      • Growth Potential: {details.get('growth_potential', 0)*100:.1f}%")
            print(f"      • Data Sources: {details.get('data_sources', 'N/A')}")
    
    print("\n============================================================")
    print("📈 PERFORMANCE ANALYSIS:")
    print(f"   • Total Time: {elapsed_time:.1f} seconds")
    print(f"   • Parallel Time: {result.get('processing_time_seconds', 0)} seconds")
    print(f"   • Cities/Second: {result.get('cities_analyzed', 0) / max(result.get('processing_time_seconds', 1), 1):.2f}")
    
    if result.get('processing_time_seconds', 0) > 0:
        speedup = (result.get('cities_analyzed', 0) * 5) / result.get('processing_time_seconds', 1)
        print(f"   • Estimated Speedup: {speedup:.1f}x vs sequential")
        print(f"   • Sequential Would Take: ~{result.get('cities_analyzed', 0) * 5} seconds")
    
    print("\n============================================================")
    print("✅ Test Complete!")
    
    if result.get('processing_time_seconds', 0) < 30:
        print("🎉 EXCELLENT: Analysis completed in under 30 seconds!")
    elif result.get('processing_time_seconds', 0) < 60:
        print("✅ GOOD: Analysis completed in under 1 minute!")
    else:
        print("⚠️  SLOW: Analysis took longer than expected.")
    
    print("\n💡 NEXT STEPS:")
    print("   • Run your Streamlit app: cd ui && streamlit run streamlit_app.py")
    print("   • Try the 'Samsung Galaxy S24' product")
    print("   • Check the 'Regional Performance' section")
    print("   • You should see 10 cities analyzed in ~15 seconds!")
    print("============================================================")

if __name__ == "__main__":
    test_parallel_city_analysis()


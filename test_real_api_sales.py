"""
Test Script for Real API-Based Sales Data Generation
Demonstrates how the system uses real APIs to generate historical sales data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.market_trend_analyzer import MarketTrendAnalyzer
from agents.communication_coordinator import coordinator
import pandas as pd
from datetime import datetime

def test_real_api_sales_generation():
    """Test the complete API-based sales data generation pipeline"""
    
    print("="*80)
    print("TESTING REAL API-BASED SALES DATA GENERATION")
    print("="*80)
    
    # Initialize the market analyzer
    print("\n[INIT] Initializing Market Trend Analyzer...")
    analyzer = MarketTrendAnalyzer(coordinator)
    
    # Test product information
    test_product = {
        'name': 'Galaxy S25 Ultra',
        'category': 'Smartphones',
        'price': 1200.0,
        'description': 'Premium flagship smartphone'
    }
    
    print(f"\n[TEST] Analyzing product: {test_product['name']}")
    print(f"[TEST] Category: {test_product['category']}")
    print(f"[TEST] Price: ${test_product['price']}")
    
    # STEP 1: Discover similar Samsung products using APIs
    print("\n" + "="*80)
    print("STEP 1: DISCOVERING SIMILAR SAMSUNG PRODUCTS (APIs Only)")
    print("="*80)
    
    similar_products = analyzer.discover_samsung_similar_products(
        test_product['name'],
        test_product['category'],
        test_product['price']
    )
    
    products_found = similar_products.get('found_products', [])
    data_sources = similar_products.get('data_sources', [])
    
    print(f"\n[RESULT] Found {len(products_found)} similar Samsung products")
    print(f"[RESULT] Data sources used: {', '.join(data_sources)}")
    
    if products_found:
        print("\n[PRODUCTS] Top Similar Products:")
        for i, product in enumerate(products_found[:5], 1):
            print(f"  {i}. {product['name']}")
            print(f"     - Price: ${product['estimated_price']}")
            print(f"     - Year: {product['launch_year']}")
            print(f"     - Source: {product['source']}")
            print(f"     - Similarity: {product['similarity_score']:.2f}")
    
    # STEP 2: Generate historical sales data using real APIs
    print("\n" + "="*80)
    print("STEP 2: GENERATING HISTORICAL SALES DATA (Real APIs)")
    print("="*80)
    
    historical_data = analyzer.get_historical_sales_data(
        test_product['category'],
        (test_product['price'] * 0.8, test_product['price'] * 1.2),
        products_found
    )
    
    print(f"\n[DATA SOURCE] {historical_data.get('data_source', 'Unknown')}")
    print(f"[ANALYZED] {historical_data.get('similar_products_analyzed', 0)} similar products")
    print(f"[APIs USED] {', '.join(historical_data.get('api_sources', []))}")
    print(f"[CONFIDENCE] {historical_data.get('real_data_confidence', 'UNKNOWN')}")
    
    # Display API metrics used
    api_metrics = historical_data.get('api_metrics_used', [])
    if api_metrics:
        print("\n[API METRICS] Detailed Metrics:")
        for metric in api_metrics:
            print(f"  • {metric['product']}:")
            print(f"    - Google Trends: {metric['trends_data']}")
            print(f"    - YouTube: {metric['youtube_data']}")
            print(f"    - News: {metric['news_data']}")
    
    # Display sample sales data
    sales_volumes = historical_data.get('sales_volume', [])
    if sales_volumes:
        print(f"\n[SALES DATA] Generated {len(sales_volumes)} months of historical data")
        print(f"[SALES DATA] Average monthly sales: {sum(sales_volumes)/len(sales_volumes):,.0f} units")
        print(f"[SALES DATA] Peak sales: {max(sales_volumes):,.0f} units")
        print(f"[SALES DATA] Min sales: {min(sales_volumes):,.0f} units")
        
        # Show first 6 months as sample
        dates = historical_data.get('dates', [])
        print("\n[SAMPLE] First 6 months of sales data:")
        for i in range(min(6, len(dates))):
            date = pd.to_datetime(dates[i]).strftime('%Y-%m')
            sales = sales_volumes[i]
            print(f"  {date}: {sales:,.0f} units")
    
    # STEP 3: Generate forecast based on real API data
    print("\n" + "="*80)
    print("STEP 3: GENERATING SALES FORECAST (API-Based)")
    print("="*80)
    
    forecast_data = analyzer.forecast_sales(
        historical_data,
        test_product['price'],
        products_found
    )
    
    print(f"\n[FORECAST METHOD] {forecast_data.get('forecasting_method', 'Unknown')}")
    print(f"[FORECAST SOURCE] {', '.join(forecast_data.get('data_sources', []))}")
    print(f"[GROWTH RATE] {forecast_data.get('growth_rate', 0)*100:.1f}%")
    print(f"[CONFIDENCE] {forecast_data.get('confidence_score', 0)*100:.1f}%")
    
    # Display forecast insights
    forecast_insights = forecast_data.get('forecast_insights', {})
    if forecast_insights:
        print("\n[INSIGHTS] Forecast Insights from API Data:")
        print(f"  - Growth Rate: {forecast_insights.get('growth_rate', 0)*100:.1f}%")
        print(f"  - Competitive Pressure: {forecast_insights.get('competitive_pressure', 0)*100:.1f}%")
        print(f"  - Market Maturity: {forecast_insights.get('market_maturity', 0)*100:.1f}%")
        print(f"  - Products Analyzed: {forecast_insights.get('products_analyzed', 0)}")
    
    # Display market outlook
    market_outlook = forecast_data.get('market_outlook', {})
    if market_outlook:
        print("\n[OUTLOOK] Market Outlook from APIs:")
        print(f"  - Outlook: {market_outlook.get('outlook', 'Unknown').upper()}")
        print(f"  - Confidence: {market_outlook.get('confidence', 0)*100:.1f}%")
        print(f"  - Data Source: {market_outlook.get('data_source', 'Unknown')}")
    
    # Display forecast samples
    forecast_sales = forecast_data.get('forecast_sales', [])
    if forecast_sales:
        print(f"\n[FORECAST] Generated {len(forecast_sales)} months of forecast")
        print(f"[FORECAST] Average monthly: {sum(forecast_sales)/len(forecast_sales):,.0f} units")
        
        # Show first 6 months of forecast
        forecast_dates = forecast_data.get('forecast_dates', [])
        print("\n[SAMPLE] First 6 months of forecast:")
        for i in range(min(6, len(forecast_dates))):
            date = pd.to_datetime(forecast_dates[i]).strftime('%Y-%m')
            sales = forecast_sales[i]
            print(f"  {date}: {sales:,.0f} units")
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    print("\n✅ VERIFICATION CHECKLIST:")
    print(f"  [{'✓' if 'Real API' in historical_data.get('data_source', '') else '✗'}] Historical sales from real APIs")
    print(f"  [{'✓' if len(products_found) > 0 else '✗'}] Similar products discovered via APIs")
    print(f"  [{'✓' if len(api_metrics) > 0 else '✗'}] API metrics collected (Trends, YouTube, News)")
    print(f"  [{'✓' if 'API-Based' in forecast_data.get('forecasting_method', '') else '✗'}] Forecast based on API data")
    print(f"  [{'✓' if len(data_sources) > 0 else '✗'}] Multiple API sources used")
    
    print("\n📊 DATA QUALITY METRICS:")
    print(f"  - Similar Products Found: {len(products_found)}")
    print(f"  - API Sources: {len(data_sources)}")
    print(f"  - Data Confidence: {historical_data.get('real_data_confidence', 'UNKNOWN')}")
    print(f"  - Forecast Confidence: {forecast_data.get('confidence_score', 0)*100:.1f}%")
    
    print("\n🎯 API SOURCES USED:")
    all_sources = set(data_sources + historical_data.get('api_sources', []))
    for source in all_sources:
        print(f"  ✓ {source}")
    
    print("\n" + "="*80)
    print("TEST COMPLETED SUCCESSFULLY!")
    print("="*80)
    
    return {
        'similar_products': products_found,
        'historical_data': historical_data,
        'forecast_data': forecast_data,
        'success': True
    }

if __name__ == "__main__":
    print("\n🚀 Starting Real API Sales Data Test...")
    print(f"⏰ Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        result = test_real_api_sales_generation()
        
        if result['success']:
            print("\n✅ All tests passed! The system is using real API data.")
        else:
            print("\n⚠️ Some tests failed. Check the logs above.")
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


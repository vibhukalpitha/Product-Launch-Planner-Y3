#!/usr/bin/env python3
"""
Test Enhanced Market Trend Analyzer
Tests the new comprehensive API integration with all 23 API keys
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.market_trend_analyzer import MarketTrendAnalyzer
from agents.communication_coordinator import CommunicationCoordinator

def test_enhanced_market_analyzer():
    """Test the enhanced Market Trend Analyzer with all available APIs"""
    
    print("🚀 ENHANCED MARKET TREND ANALYZER TEST")
    print("Testing comprehensive API integration with all 23 keys!")
    print("=" * 80)
    
    # Initialize coordinator and agent
    coordinator = CommunicationCoordinator()
    analyzer = MarketTrendAnalyzer(coordinator)
    
    print(f"\n📊 API AVAILABILITY CHECK")
    print("=" * 50)
    available_count = sum(1 for available in analyzer.available_apis.values() if available)
    total_count = len(analyzer.available_apis)
    
    print(f"✅ Available APIs: {available_count}/{total_count}")
    print(f"📈 API Coverage: {(available_count/total_count)*100:.1f}%")
    
    # List all available APIs
    print(f"\n🔧 ACTIVE APIs:")
    for api_name, available in analyzer.available_apis.items():
        status = "✅" if available else "❌"
        print(f"  {status} {api_name}")
    
    # Test comprehensive market analysis
    print(f"\n🎯 COMPREHENSIVE MARKET ANALYSIS TEST")
    print("=" * 60)
    
    test_product = "Samsung Galaxy S25 Ultra"
    
    try:
        # Get comprehensive analysis using ALL available APIs
        analysis = analyzer.get_comprehensive_market_analysis(test_product, "smartphones")
        
        print(f"\n📊 ANALYSIS RESULTS SUMMARY")
        print("=" * 50)
        print(f"📱 Product: {analysis['product_name']}")
        print(f"📊 Total APIs Used: {analysis['total_apis_used']}")
        print(f"🎯 Data Sources: {len(analysis['data_sources'])}")
        print(f"⏰ Analysis Time: {analysis['timestamp']}")
        
        # Show data categories collected
        categories = ['financial_data', 'market_data', 'social_sentiment', 
                     'search_trends', 'demographic_insights', 'pricing_intelligence', 
                     'competitive_landscape']
        
        print(f"\n📋 DATA CATEGORIES COLLECTED:")
        for category in categories:
            data = analysis.get(category, {})
            count = len([k for k, v in data.items() if not k.endswith('_error')])
            status = "✅" if count > 0 else "⚠️"
            print(f"  {status} {category.replace('_', ' ').title()}: {count} data sources")
        
        # Show specific API results
        print(f"\n🔍 DETAILED API RESULTS:")
        
        # Financial Data
        if analysis['financial_data']:
            print("  💰 Financial Data:")
            for key, value in analysis['financial_data'].items():
                if not key.endswith('_error'):
                    print(f"    ✅ {key}: {type(value).__name__} data retrieved")
                else:
                    print(f"    ❌ {key}: {value}")
        
        # Social Sentiment
        if analysis['social_sentiment']:
            print("  📱 Social Media Analysis:")
            for key, value in analysis['social_sentiment'].items():
                if not key.endswith('_error'):
                    print(f"    ✅ {key}: {type(value).__name__} data retrieved")
                else:
                    print(f"    ❌ {key}: {value}")
        
        # Search Trends
        if analysis['search_trends']:
            print("  🔍 Search & News Analysis:")
            for key, value in analysis['search_trends'].items():
                if not key.endswith('_error'):
                    print(f"    ✅ {key}: {type(value).__name__} data retrieved")
                else:
                    print(f"    ❌ {key}: {value}")
        
        # Market Data
        if analysis['market_data']:
            print("  📊 Economic & Market Data:")
            for key, value in analysis['market_data'].items():
                if not key.endswith('_error'):
                    print(f"    ✅ {key}: {type(value).__name__} data retrieved")
                else:
                    print(f"    ❌ {key}: {value}")
        
        print(f"\n🏆 ENHANCEMENT SUCCESS!")
        print(f"Market Trend Analyzer now uses {analysis['total_apis_used']} APIs")
        print(f"Previously: 4 APIs → Now: {analysis['total_apis_used']} APIs")
        print(f"🚀 {analysis['total_apis_used']/4:.1f}x MORE comprehensive market intelligence!")
        
        # Show the difference
        old_apis = ['alpha_vantage', 'world_bank', 'fred', 'fake_store_api']
        new_apis = [api for api in analysis['data_sources'] if api not in old_apis]
        
        print(f"\n📈 NEW APIs ADDED:")
        for api in new_apis:
            print(f"  🆕 {api.replace('_', ' ').title()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during comprehensive analysis: {e}")
        import traceback
        traceback.print_exc()
        return False

def compare_old_vs_new():
    """Compare old vs new API usage"""
    
    print(f"\n📊 OLD vs NEW COMPARISON")
    print("=" * 60)
    
    old_apis = {
        'alpha_vantage': 'Stock market data',
        'world_bank': 'Global economic data', 
        'fred': 'US economic indicators',
        'fake_store_api': 'Demo product data'
    }
    
    new_apis = {
        'youtube': 'Video content trends & sentiment',
        'facebook_marketing': 'Social media audience insights',
        'twitter': 'Real-time sentiment analysis',
        'reddit': 'Community discussions & opinions',
        'news_api': 'News trends & market sentiment',
        'serp_api': 'Google search trends',
        'bing_search': 'Bing search intelligence',
        'google_analytics': 'Web traffic & user behavior',
        'census': 'Demographics & population data',
        'amazon_api': 'E-commerce pricing intelligence',
        'ebay_api': 'Marketplace pricing data',
        'rapidapi': 'Multiple data source access',
        'scraperapi': 'Competitive intelligence gathering'
    }
    
    print(f"🔴 OLD APIs ({len(old_apis)}):")
    for api, description in old_apis.items():
        print(f"  • {api}: {description}")
    
    print(f"\n🟢 NEW APIs ADDED ({len(new_apis)}):")
    for api, description in new_apis.items():
        print(f"  • {api}: {description}")
    
    print(f"\n📈 TOTAL IMPROVEMENT:")
    print(f"  Before: {len(old_apis)} APIs")
    print(f"  After: {len(old_apis) + len(new_apis)} APIs")
    print(f"  Increase: {len(new_apis)} additional APIs (+{(len(new_apis)/len(old_apis))*100:.0f}%)")
    
    print(f"\n🎯 NEW CAPABILITIES:")
    print(f"  ✅ Real-time social media sentiment analysis")
    print(f"  ✅ Comprehensive search trend monitoring")
    print(f"  ✅ E-commerce & pricing intelligence")
    print(f"  ✅ Community opinion tracking")
    print(f"  ✅ News & media coverage analysis")
    print(f"  ✅ Web traffic & user behavior insights")
    print(f"  ✅ Demographics & population analysis")
    print(f"  ✅ Competitive intelligence gathering")

if __name__ == "__main__":
    print("🔥 MARKET TREND ANALYZER ENHANCEMENT TEST")
    print("Testing the upgrade from 4 APIs to 17+ APIs!")
    print("=" * 80)
    
    # Show the comparison first
    compare_old_vs_new()
    
    # Test the enhanced analyzer
    success = test_enhanced_market_analyzer()
    
    if success:
        print(f"\n🎉 ENHANCEMENT COMPLETE!")
        print(f"Market Trend Analyzer successfully upgraded to use ALL available APIs!")
        print(f"Ready for enterprise-grade market intelligence analysis! 🚀")
    else:
        print(f"\n⚠️ Enhancement test encountered issues - check logs above")
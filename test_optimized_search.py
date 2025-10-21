#!/usr/bin/env python3
"""
Enhanced Samsung Product Discovery Test
Tests optimized search queries for finding more Samsung products
"""
import sys
import os
sys.path.append('.')

from utils.real_data_connector import real_data_connector

def test_optimized_search_queries():
    """Test different search queries to find optimal ones"""
    print("🔍 TESTING OPTIMIZED SEARCH QUERIES FOR SAMSUNG PRODUCTS")
    print("=" * 60)
    
    # More effective search queries
    news_queries = [
        "Samsung Galaxy",  # Broader search
        "Samsung smartphone",  # Generic smartphone search  
        "Samsung phone",  # Simple phone search
        "Galaxy S24 S25",  # Latest models
        "Samsung mobile"  # Mobile devices
    ]
    
    youtube_queries = [
        "Samsung Galaxy unboxing",  # Popular unboxing videos
        "Samsung phone review",  # Review videos
        "Galaxy S24 vs S25",  # Comparison videos
        "Samsung smartphone 2024",  # Recent smartphones
        "Galaxy phone comparison"  # General comparisons
    ]
    
    print("\n📰 TESTING NEWS API QUERIES:")
    print("-" * 40)
    
    for i, query in enumerate(news_queries, 1):
        print(f"\n{i}. Testing: '{query}'")
        try:
            result = real_data_connector.get_news_data(query, page_size=5)
            if result and 'articles' in result:
                articles = result['articles']
                print(f"   ✅ Found {len(articles)} articles")
                
                # Show sample titles
                for j, article in enumerate(articles[:2], 1):
                    title = article.get('title', 'No title')[:60]
                    print(f"      {j}. {title}...")
            else:
                print(f"   ❌ No articles found")
        except Exception as e:
            if '429' in str(e):
                print(f"   ⚠️ Rate limited")
            else:
                print(f"   ❌ Error: {e}")
    
    print("\n📺 TESTING YOUTUBE API QUERIES:")
    print("-" * 40)
    
    for i, query in enumerate(youtube_queries, 1):
        print(f"\n{i}. Testing: '{query}'")
        try:
            result = real_data_connector.get_youtube_metrics(query)
            if result and 'videos' in result:
                videos = result['videos']
                print(f"   ✅ Found {len(videos)} videos")
                
                # Show sample titles and extract Samsung products
                samsung_products = []
                for video in videos[:3]:
                    title = video.get('title', 'No title')
                    print(f"      • {title[:60]}...")
                    
                    # Look for Samsung product names
                    if 'Galaxy' in title:
                        words = title.split()
                        for j, word in enumerate(words):
                            if word == 'Galaxy' and j+1 < len(words):
                                product = f"Galaxy {words[j+1]}"
                                if product not in samsung_products:
                                    samsung_products.append(product)
                
                if samsung_products:
                    print(f"   📱 Samsung products detected: {samsung_products}")
            else:
                print(f"   ❌ No videos found")
        except Exception as e:
            if '403' in str(e):
                print(f"   ⚠️ Quota exceeded")  
            else:
                print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("💡 OPTIMIZATION RECOMMENDATIONS:")
    print("1. Use broader search terms like 'Samsung Galaxy' instead of specific categories")
    print("2. Focus on popular content types: 'unboxing', 'review', 'comparison'")
    print("3. Include year filters: '2024', '2025' for recent products")
    print("4. Try multiple variations to maximize product discovery")

if __name__ == "__main__":
    test_optimized_search_queries()
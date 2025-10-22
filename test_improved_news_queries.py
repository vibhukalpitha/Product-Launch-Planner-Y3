#!/usr/bin/env python3
"""
Test improved News API search queries for Samsung products
"""
import sys
import os
sys.path.append('.')

from utils.real_data_connector import real_data_connector

def test_improved_news_queries():
    """Test specific product-focused news queries"""
    print("🔍 TESTING IMPROVED NEWS API QUERIES FOR SAMSUNG PRODUCTS")
    print("=" * 60)
    
    # More specific product-focused queries
    improved_queries = [
        "Galaxy S25 Ultra",      # Specific latest model
        "Galaxy S24 review",     # Product reviews
        "Samsung Galaxy S25",    # Product announcements  
        "Galaxy A36 launch",     # A-series launches
        "Galaxy S24 vs iPhone"   # Comparisons (more likely to have specific models)
    ]
    
    for i, query in enumerate(improved_queries, 1):
        print(f"\n{i}. Testing: '{query}'")
        try:
            result = real_data_connector.get_news_data(query, page_size=2)
            
            if result and 'articles' in result:
                articles = result['articles']
                print(f"   ✅ Found {len(articles)} articles")
                
                for j, article in enumerate(articles, 1):
                    title = article.get('title', 'No title')
                    print(f"      {j}. {title[:70]}...")
                    
                    # Check for Samsung product names in title
                    title_lower = title.lower()
                    if any(term in title_lower for term in ['galaxy s', 'galaxy a', 'galaxy note', 'galaxy z']):
                        print(f"         🎯 Contains specific Galaxy product!")
                    elif 'galaxy' in title_lower:
                        print(f"         📱 Contains Galaxy")
                    elif 'samsung' in title_lower:
                        print(f"         📲 Contains Samsung")
                    else:
                        print(f"         ❌ No Samsung product indicators")
            else:
                print(f"   ❌ No articles found")
                
        except Exception as e:
            if '429' in str(e):
                print(f"   ⚠️ Rate limited - key is valid but quota reached")
            else:
                print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("💡 ANALYSIS:")
    print("• Product-specific queries (Galaxy S25 Ultra) should find more relevant articles")
    print("• Review/comparison articles contain specific model names")
    print("• Launch announcements mention exact product names")

if __name__ == "__main__":
    test_improved_news_queries()
"""
Market Trend Analyzer Agent
Analyzes market trends, past sales, and forecasts future sales
Uses real APIs for market data analysis when available, falls back to simulated data
"""
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Import real data connector
try:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils.real_data_connector import real_data_connector
    from utils.api_manager import is_api_enabled
    REAL_DATA_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Real data connector not available: {e}")
    REAL_DATA_AVAILABLE = False

class MarketTrendAnalyzer:
    """Agent for analyzing market trends and forecasting sales"""
    
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self.name = "market_analyzer"
        self.coordinator.register_agent(self.name, self)
        
        # Free APIs for market data
        self.apis = {
            'alpha_vantage': 'https://www.alphavantage.co/query',  # Free tier: 5 calls/minute
            'world_bank': 'https://api.worldbank.org/v2/country',  # Free
            'economic_data': 'https://api.stlouisfed.org/fred/series/observations',  # Free with API key
            'fake_store_api': 'https://fakestoreapi.com/products',  # Free for demo
        }
    
    def receive_message(self, message):
        """Handle messages from other agents"""
        if message.message_type == 'analyze_market':
            return self.analyze_market_trends(message.data['product_info'])
        return None
    
    def get_historical_sales_data(self, category: str, price_range: tuple) -> Dict[str, Any]:
        """Simulate historical sales data for similar products"""
        # In a real scenario, this would connect to Samsung's internal database
        # For demo, we'll simulate realistic data
        
        # Generate sample data for the last 3 years
        dates = pd.date_range(start='2022-01-01', end='2024-12-31', freq='ME')
        
        # Simulate sales based on category trends
        base_sales = {
            'smartphones': np.random.normal(100000, 20000, len(dates)),
            'tablets': np.random.normal(50000, 10000, len(dates)),
            'laptops': np.random.normal(75000, 15000, len(dates)),
            'wearables': np.random.normal(30000, 8000, len(dates)),
            'tv': np.random.normal(80000, 12000, len(dates)),
            'appliances': np.random.normal(60000, 10000, len(dates))
        }
        
        # Apply seasonal trends
        seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * np.arange(len(dates)) / 12)
        
        category_lower = category.lower()
        sales_data = base_sales.get(category_lower, base_sales['smartphones']) * seasonal_factor
        sales_data = np.maximum(sales_data, 0)  # Ensure non-negative
        
        return {
            'dates': dates.tolist(),
            'sales_volume': sales_data.tolist(),
            'category': category,
            'price_range': price_range
        }
    
    def get_market_trends(self, category: str) -> Dict[str, Any]:
        """Get market trends for the product category using real APIs when available"""
        
        # Try to get real market data first
        if REAL_DATA_AVAILABLE and any(is_api_enabled(api) for api in ['alpha_vantage', 'fred', 'news_api']):
            try:
                print(f"🌐 Fetching real market data for {category}...")
                
                # Get real market data
                real_market_data = real_data_connector.get_real_market_data(category, f"Samsung {category}")
                
                # Extract trends from real data
                trends_data = real_market_data.get('trends_data', {})
                economic_data = real_market_data.get('economic_indicators', {})
                stock_data = real_market_data.get('stock_market', {})
                news_data = real_market_data.get('news_sentiment', {})
                
                # Calculate market metrics from real data
                market_growth = 0.0
                if economic_data.get('indicators', {}).get('GDP', {}).get('change_percent'):
                    market_growth = economic_data['indicators']['GDP']['change_percent'] / 100
                
                # Base pricing from economic indicators
                base_price = self._estimate_category_price(category)
                
                # Adjust price based on economic conditions
                price_adjustment = 1.0
                if economic_data.get('market_health_score', 0.5) > 0.7:
                    price_adjustment = 1.1  # Premium market
                elif economic_data.get('market_health_score', 0.5) < 0.4:
                    price_adjustment = 0.9  # Value market
                
                adjusted_price = base_price * price_adjustment
                
                # Market size estimation from trends and stock data
                trend_interest = trends_data.get('peak_interest', 50)
                market_size_multiplier = (trend_interest / 100) * 2000000  # Scale to realistic numbers
                
                trend_data = {
                    'average_price': adjusted_price,
                    'price_variance': adjusted_price * 0.25,
                    'average_rating': 4.2,
                    'market_size_estimate': int(market_size_multiplier),
                    'growth_rate': max(0.02, market_growth),  # Minimum 2% growth
                    'market_saturation': self._calculate_market_saturation(category, trends_data),
                    'data_sources': real_market_data.get('sources_used', []),
                    'real_data': True,
                    'market_health_score': real_market_data.get('market_health_score', 0.5),
                    'news_sentiment': news_data.get('overall_sentiment', 'neutral'),
                    'trend_direction': trends_data.get('current_trend', 'stable'),
                    'last_updated': datetime.now().isoformat()
                }
                
                print(f"✅ Real market data integrated from: {', '.join(real_market_data.get('sources_used', []))}")
                return trend_data
                
            except Exception as e:
                print(f"⚠️ Error fetching real market data, falling back to simulated data: {e}")
        
        # Fallback to simulated data
        print(f"📊 Using simulated market data for {category}")
        return self._get_fallback_trends(category)
    
    def _get_fallback_trends(self, category: str) -> Dict[str, Any]:
        """Fallback market trends data"""
        base_trends = {
            'smartphones': {'avg_price': 800, 'growth': 0.15, 'saturation': 0.75},
            'tablets': {'avg_price': 500, 'growth': 0.08, 'saturation': 0.60},
            'laptops': {'avg_price': 1200, 'growth': 0.12, 'saturation': 0.65},
            'wearables': {'avg_price': 300, 'growth': 0.25, 'saturation': 0.40},
            'tv': {'avg_price': 800, 'growth': 0.10, 'saturation': 0.70},
            'appliances': {'avg_price': 600, 'growth': 0.06, 'saturation': 0.55}
        }
        
        trend = base_trends.get(category.lower(), base_trends['smartphones'])
        
        return {
            'average_price': trend['avg_price'],
            'price_variance': trend['avg_price'] * 0.2,
            'average_rating': 4.2,
            'market_size_estimate': 1000000,
            'growth_rate': trend['growth'],
            'market_saturation': trend['saturation'],
            'data_sources': ['Simulated Data'],
            'real_data': False,
            'last_updated': datetime.now().isoformat()
        }
    
    def _estimate_category_price(self, category: str) -> float:
        """Estimate base price for category"""
        base_prices = {
            'smartphones': 800,
            'tablets': 500,
            'laptops': 1200,
            'wearables': 300,
            'tv': 800,
            'appliances': 600
        }
        return base_prices.get(category.lower(), 800)
    
    def _calculate_market_saturation(self, category: str, trends_data: Dict) -> float:
        """Calculate market saturation based on trends and category"""
        base_saturation = {
            'smartphones': 0.75,
            'tablets': 0.60,
            'laptops': 0.65,
            'wearables': 0.40,
            'tv': 0.70,
            'appliances': 0.55
        }
        
        base = base_saturation.get(category.lower(), 0.6)
        
        # Adjust based on trend direction
        trend_direction = trends_data.get('current_trend', 'stable')
        if trend_direction == 'rising':
            return max(0.1, base - 0.1)  # Less saturated if rising
        elif trend_direction == 'declining':
            return min(0.9, base + 0.1)  # More saturated if declining
        
        return base
    
    def forecast_sales(self, historical_data: Dict[str, Any], product_price: float) -> Dict[str, Any]:
        """Forecast future sales based on historical data and market trends"""
        sales_history = np.array(historical_data['sales_volume'])
        
        # Simple trend analysis
        x = np.arange(len(sales_history))
        coeffs = np.polyfit(x, sales_history, 1)
        
        # Forecast next 12 months
        future_months = 12
        future_x = np.arange(len(sales_history), len(sales_history) + future_months)
        base_forecast = np.polyval(coeffs, future_x)
        
        # Apply market conditions and price adjustments
        market_trends = self.get_market_trends(historical_data['category'])
        growth_factor = 1 + market_trends['growth_rate']
        
        # Price sensitivity (higher price = lower sales)
        avg_market_price = market_trends['average_price']
        price_factor = 0.8 if product_price > avg_market_price else 1.2
        
        forecast = base_forecast * growth_factor * price_factor
        forecast = np.maximum(forecast, 0)  # Ensure non-negative
        
        # Generate future dates
        last_date = pd.to_datetime(historical_data['dates'][-1])
        future_dates = pd.date_range(start=last_date + timedelta(days=30), periods=future_months, freq='ME')
        
        return {
            'forecast_dates': future_dates.tolist(),
            'forecast_sales': forecast.tolist(),
            'confidence_interval': {
                'lower': (forecast * 0.8).tolist(),
                'upper': (forecast * 1.2).tolist()
            },
            'growth_rate': market_trends['growth_rate'],
            'price_impact': price_factor
        }
    
    def analyze_city_performance(self, category: str) -> Dict[str, Any]:
        """Analyze sales performance by city"""
        # Simulated city data for Samsung markets
        cities = [
            'Seoul', 'Busan', 'New York', 'Los Angeles', 'London', 
            'Berlin', 'Tokyo', 'Mumbai', 'Singapore', 'Sydney'
        ]
        
        # Generate realistic sales data by city
        city_sales = {}
        for city in cities:
            base_sales = np.random.normal(50000, 15000)
            
            # City-specific factors
            urban_factor = np.random.uniform(1.0, 1.5)
            economic_factor = np.random.uniform(0.8, 1.3)
            
            city_sales[city] = max(0, int(base_sales * urban_factor * economic_factor))
        
        # Sort cities by sales
        sorted_cities = sorted(city_sales.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'city_sales': dict(sorted_cities),
            'top_cities': sorted_cities[:5],
            'growth_potential': {
                city: np.random.uniform(0.05, 0.20) for city, _ in sorted_cities
            }
        }
    
    def generate_recommendations(self, market_data: Dict[str, Any], forecast_data: Dict[str, Any], 
                               city_data: Dict[str, Any], product_price: float) -> List[str]:
        """Generate market-based recommendations"""
        recommendations = []
        
        # Price recommendations
        avg_price = market_data['average_price']
        if product_price > avg_price * 1.2:
            recommendations.append(f"Consider reducing price. Your price (${product_price}) is {((product_price/avg_price-1)*100):.1f}% above market average (${avg_price:.2f})")
        elif product_price < avg_price * 0.8:
            recommendations.append(f"Price is competitive. Consider premium positioning with additional features.")
        
        # Market growth recommendations
        if market_data['growth_rate'] > 0.15:
            recommendations.append(f"High growth market ({market_data['growth_rate']*100:.1f}%). Consider aggressive expansion.")
        elif market_data['growth_rate'] < 0.05:
            recommendations.append("Low growth market. Focus on differentiation and customer retention.")
        
        # City recommendations
        top_cities = [city for city, _ in city_data['top_cities'][:3]]
        recommendations.append(f"Focus marketing efforts on top-performing cities: {', '.join(top_cities)}")
        
        # Forecast recommendations
        avg_forecast = np.mean(forecast_data['forecast_sales'])
        if avg_forecast > np.mean(market_data.get('historical_avg', [100000])):
            recommendations.append("Positive sales forecast. Consider increasing production capacity.")
        else:
            recommendations.append("Conservative forecast. Implement demand generation strategies.")
        
        return recommendations
    
    def create_visualizations(self, historical_data: Dict[str, Any], forecast_data: Dict[str, Any], 
                            city_data: Dict[str, Any], market_trends: Dict[str, Any]) -> Dict[str, Any]:
        """Create visualization data for Streamlit"""
        
        # Historical sales chart data
        historical_chart = {
            'dates': historical_data['dates'],
            'sales': historical_data['sales_volume'],
            'type': 'historical'
        }
        
        # Forecast chart data
        forecast_chart = {
            'dates': forecast_data['forecast_dates'],
            'sales': forecast_data['forecast_sales'],
            'lower_bound': forecast_data['confidence_interval']['lower'],
            'upper_bound': forecast_data['confidence_interval']['upper'],
            'type': 'forecast'
        }
        
        # City performance chart data
        city_chart = {
            'cities': list(city_data['city_sales'].keys()),
            'sales': list(city_data['city_sales'].values()),
            'type': 'city_performance'
        }
        
        # Market trends chart data
        trends_chart = {
            'metrics': ['Growth Rate', 'Market Saturation', 'Avg Rating'],
            'values': [
                market_trends['growth_rate'] * 100,
                market_trends['market_saturation'] * 100,
                market_trends['average_rating'] * 20  # Scale to 100
            ],
            'type': 'market_trends'
        }
        
        return {
            'historical_sales': historical_chart,
            'sales_forecast': forecast_chart,
            'city_performance': city_chart,
            'market_trends': trends_chart
        }
    
    def analyze_market_trends(self, product_info: Dict[str, Any]) -> Dict[str, Any]:
        """Main method to analyze market trends"""
        print(f"Analyzing market trends for {product_info['name']} in {product_info['category']}")
        
        try:
            # Get historical data
            historical_data = self.get_historical_sales_data(
                product_info['category'], 
                (product_info['price'] * 0.8, product_info['price'] * 1.2)
            )
            
            # Get market trends
            market_trends = self.get_market_trends(product_info['category'])
            
            # Generate forecast
            forecast_data = self.forecast_sales(historical_data, product_info['price'])
            
            # Analyze city performance
            city_data = self.analyze_city_performance(product_info['category'])
            
            # Generate recommendations
            recommendations = self.generate_recommendations(
                market_trends, forecast_data, city_data, product_info['price']
            )
            
            # Create visualizations
            visualizations = self.create_visualizations(
                historical_data, forecast_data, city_data, market_trends
            )
            
            analysis_result = {
                'historical_data': historical_data,
                'market_trends': market_trends,
                'sales_forecast': forecast_data,
                'city_analysis': city_data,
                'recommendations': recommendations,
                'visualizations': visualizations,
                'analysis_timestamp': datetime.now().isoformat(),
                'product_category': product_info['category'],
                'analyzed_price': product_info['price']
            }
            
            print("Market trend analysis completed successfully")
            return analysis_result
            
        except Exception as e:
            print(f"Error in market trend analysis: {e}")
            return {
                'error': str(e),
                'analysis_timestamp': datetime.now().isoformat(),
                'status': 'failed'
            }
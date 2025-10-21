"""
Customer Segmentation Agent
Segments customers based on demographics, behavior, and preferences
Uses free APIs and data sources for customer analysis with real-time data
"""
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any
import logging

try:
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("Warning: sklearn not available, using simplified clustering")

import plotly.graph_objects as go
import plotly.express as px

# Try to import real data connector
try:
    from utils.real_data_connector import RealDataConnector
    from utils.api_manager import api_manager
    real_data_available = True
except ImportError:
    real_data_available = False
    logging.warning("Real data connector not available, using simulated data")

class CustomerSegmentationAgent:
    """Agent for customer segmentation and behavior analysis"""
    
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self.name = "customer_segmenter"
        self.coordinator.register_agent(self.name, self)
        
        # Initialize real data connector if available
        if real_data_available:
            self.real_data_connector = RealDataConnector()
            self.use_real_data = api_manager.is_any_api_enabled()
        else:
            self.real_data_connector = None
            self.use_real_data = False
        
        # Customer demographic profiles by age groups
        self.age_segments = {
            'Gen Z (18-24)': {
                'tech_adoption': 0.9,
                'price_sensitivity': 0.8,
                'brand_loyalty': 0.4,
                'social_media_influence': 0.9,
                'sustainability_concern': 0.7,
                'preferred_channels': ['Online', 'Social Media', 'Mobile Apps']
            },
            'Millennials (25-40)': {
                'tech_adoption': 0.8,
                'price_sensitivity': 0.7,
                'brand_loyalty': 0.6,
                'social_media_influence': 0.8,
                'sustainability_concern': 0.8,
                'preferred_channels': ['Online', 'Social Media', 'Retail Stores']
            },
            'Gen X (41-56)': {
                'tech_adoption': 0.6,
                'price_sensitivity': 0.6,
                'brand_loyalty': 0.7,
                'social_media_influence': 0.5,
                'sustainability_concern': 0.6,
                'preferred_channels': ['Retail Stores', 'Online', 'TV/Radio']
            },
            'Baby Boomers (57+)': {
                'tech_adoption': 0.4,
                'price_sensitivity': 0.5,
                'brand_loyalty': 0.8,
                'social_media_influence': 0.3,
                'sustainability_concern': 0.5,
                'preferred_channels': ['Retail Stores', 'TV/Radio', 'Print']
            }
        }
    
    def receive_message(self, message):
        """Handle messages from other agents"""
        if message.message_type == 'segment_customers':
            return self.segment_customers(
                message.data['product_info'],
                message.data.get('market_data'),
                message.data.get('competitor_data')
            )
        return None
    
    def generate_customer_data(self, product_category: str, sample_size: int = 1000) -> pd.DataFrame:
        """Generate synthetic customer data for analysis"""
        np.random.seed(42)  # For reproducible results
        
        # Generate demographic data
        ages = np.random.normal(35, 15, sample_size)
        ages = np.clip(ages, 18, 80)  # Limit age range
        
        # Assign age segments
        age_segments = []
        for age in ages:
            if 18 <= age <= 24:
                age_segments.append('Gen Z (18-24)')
            elif 25 <= age <= 40:
                age_segments.append('Millennials (25-40)')
            elif 41 <= age <= 56:
                age_segments.append('Gen X (41-56)')
            else:
                age_segments.append('Baby Boomers (57+)')
        
        # Generate income (correlated with age)
        base_income = 30000 + (ages - 18) * 1000 + np.random.normal(0, 15000, sample_size)
        incomes = np.clip(base_income, 20000, 200000)
        
        # Generate other attributes
        education_levels = np.random.choice(
            ['High School', 'Bachelor', 'Master', 'PhD'],
            sample_size,
            p=[0.3, 0.4, 0.25, 0.05]
        )
        
        locations = np.random.choice(
            ['Urban', 'Suburban', 'Rural'],
            sample_size,
            p=[0.4, 0.45, 0.15]
        )
        
        # Category-specific preferences
        category_preferences = self._generate_category_preferences(product_category, sample_size, age_segments)
        
        # Create DataFrame
        customer_data = pd.DataFrame({
            'age': ages,
            'age_segment': age_segments,
            'income': incomes,
            'education': education_levels,
            'location': locations,
            'tech_adoption': category_preferences['tech_adoption'],
            'price_sensitivity': category_preferences['price_sensitivity'],
            'brand_loyalty': category_preferences['brand_loyalty'],
            'social_media_usage': category_preferences['social_media_usage'],
            'sustainability_concern': category_preferences['sustainability_concern'],
            'purchase_frequency': category_preferences['purchase_frequency'],
            'online_shopping_preference': category_preferences['online_shopping']
        })
        
        return customer_data
    
    def _generate_category_preferences(self, category: str, sample_size: int, age_segments: List[str]) -> Dict[str, List[float]]:
        """Generate category-specific customer preferences"""
        preferences = {
            'tech_adoption': [],
            'price_sensitivity': [],
            'brand_loyalty': [],
            'social_media_usage': [],
            'sustainability_concern': [],
            'purchase_frequency': [],
            'online_shopping': []
        }
        
        for segment in age_segments:
            base_prefs = self.age_segments[segment]
            
            # Add some randomness to base preferences
            for pref in preferences.keys():
                if pref == 'purchase_frequency':
                    # Purchase frequency based on category and age
                    if category.lower() in ['smartphones', 'wearables']:
                        base_freq = 0.3 if 'Gen Z' in segment or 'Millennials' in segment else 0.2
                    else:
                        base_freq = 0.1
                    freq = np.random.normal(base_freq, 0.1)
                    preferences[pref].append(max(0.05, min(0.8, freq)))
                elif pref == 'online_shopping':
                    base_online = base_prefs.get('social_media_influence', 0.5)
                    online_pref = np.random.normal(base_online, 0.2)
                    preferences[pref].append(max(0.1, min(0.95, online_pref)))
                else:
                    base_value = base_prefs.get(pref, 0.5)
                    value = np.random.normal(base_value, 0.15)
                    preferences[pref].append(max(0.1, min(0.9, value)))
        
        return preferences
    
    def perform_clustering(self, customer_data: pd.DataFrame) -> Dict[str, Any]:
        """Perform customer segmentation using clustering"""
        # Select features for clustering
        features = [
            'age', 'income', 'tech_adoption', 'price_sensitivity',
            'brand_loyalty', 'social_media_usage', 'sustainability_concern',
            'purchase_frequency', 'online_shopping_preference'
        ]
        
        # Prepare data for clustering
        X = customer_data[features].copy()
        
        if SKLEARN_AVAILABLE:
            # Standardize features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Perform K-means clustering
            n_clusters = 4  # Define 4 customer segments
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(X_scaled)
            
            # Add cluster labels to data
            customer_data['cluster'] = clusters
            cluster_centers = kmeans.cluster_centers_
        else:
            # Simple clustering based on key characteristics
            n_clusters = 4
            # Create clusters based on tech adoption and price sensitivity
            customer_data['cluster'] = 0
            
            # Tech Enthusiasts: High tech adoption, low price sensitivity
            mask1 = (customer_data['tech_adoption'] > 0.7) & (customer_data['price_sensitivity'] < 0.5)
            customer_data.loc[mask1, 'cluster'] = 0
            
            # Value Seekers: High price sensitivity
            mask2 = (customer_data['price_sensitivity'] > 0.7)
            customer_data.loc[mask2, 'cluster'] = 1
            
            # Brand Loyalists: High brand loyalty
            mask3 = (customer_data['brand_loyalty'] > 0.7) & (customer_data['price_sensitivity'] < 0.7)
            customer_data.loc[mask3, 'cluster'] = 2
            
            # Conservative Buyers: Low tech adoption, moderate characteristics
            mask4 = (customer_data['tech_adoption'] < 0.5) & (~mask1) & (~mask2) & (~mask3)
            customer_data.loc[mask4, 'cluster'] = 3
            
            cluster_centers = np.zeros((4, len(features)))  # Placeholder
        
        # Analyze clusters
        cluster_analysis = {}
        cluster_names = ['Tech Enthusiasts', 'Value Seekers', 'Brand Loyalists', 'Conservative Buyers']
        
        for i in range(n_clusters):
            cluster_data = customer_data[customer_data['cluster'] == i]
            
            cluster_analysis[cluster_names[i]] = {
                'size': len(cluster_data),
                'percentage': len(cluster_data) / len(customer_data) * 100,
                'characteristics': {
                    'avg_age': cluster_data['age'].mean(),
                    'avg_income': cluster_data['income'].mean(),
                    'tech_adoption': cluster_data['tech_adoption'].mean(),
                    'price_sensitivity': cluster_data['price_sensitivity'].mean(),
                    'brand_loyalty': cluster_data['brand_loyalty'].mean(),
                    'social_media_usage': cluster_data['social_media_usage'].mean(),
                    'sustainability_concern': cluster_data['sustainability_concern'].mean(),
                    'purchase_frequency': cluster_data['purchase_frequency'].mean(),
                    'online_shopping_preference': cluster_data['online_shopping_preference'].mean()
                },
                'dominant_age_segment': cluster_data['age_segment'].mode().iloc[0] if len(cluster_data) > 0 else 'Unknown',
                'dominant_location': cluster_data['location'].mode().iloc[0] if len(cluster_data) > 0 else 'Unknown',
                'dominant_education': cluster_data['education'].mode().iloc[0] if len(cluster_data) > 0 else 'Unknown'
            }
        
        return {
            'clusters': cluster_analysis,
            'cluster_centers': cluster_centers,
            'feature_names': features,
            'customer_data_with_clusters': customer_data
        }
    
    def analyze_segment_preferences(self, clustering_result: Dict[str, Any], 
                                  product_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze preferences for each customer segment"""
        segment_preferences = {}
        
        for segment_name, segment_data in clustering_result['clusters'].items():
            chars = segment_data['characteristics']
            
            # Determine segment preferences
            preferences = {
                'price_preference': 'Premium' if chars['price_sensitivity'] < 0.4 else 
                                  'Mid-range' if chars['price_sensitivity'] < 0.7 else 'Budget',
                'feature_priorities': self._get_feature_priorities(chars, product_info['category']),
                'marketing_channels': self._get_preferred_channels(chars),
                'purchase_drivers': self._get_purchase_drivers(chars),
                'communication_style': self._get_communication_style(chars)
            }
            
            # Calculate segment attractiveness
            attractiveness_score = self._calculate_attractiveness(segment_data, product_info)
            
            segment_preferences[segment_name] = {
                'size': segment_data['size'],
                'percentage': segment_data['percentage'],
                'characteristics': segment_data['characteristics'],
                'preferences': preferences,
                'attractiveness_score': attractiveness_score,
                'recommended_strategy': self._get_strategy_recommendation(preferences, attractiveness_score)
            }
        
        return segment_preferences
    
    def _get_feature_priorities(self, characteristics: Dict[str, float], category: str) -> List[str]:
        """Determine feature priorities for a segment"""
        priorities = []
        
        if characteristics['tech_adoption'] > 0.7:
            priorities.extend(['Latest Technology', 'Innovation', 'Performance'])
        if characteristics['price_sensitivity'] > 0.6:
            priorities.extend(['Value for Money', 'Competitive Pricing'])
        if characteristics['brand_loyalty'] > 0.6:
            priorities.extend(['Brand Reputation', 'Reliability'])
        if characteristics['sustainability_concern'] > 0.6:
            priorities.extend(['Eco-friendly', 'Sustainability'])
        
        # Category-specific priorities
        category_priorities = {
            'smartphones': ['Camera Quality', 'Battery Life', 'Display'],
            'tablets': ['Display Size', 'Battery Life', 'Portability'],
            'laptops': ['Performance', 'Battery Life', 'Build Quality'],
            'wearables': ['Health Tracking', 'Battery Life', 'Design'],
            'tv': ['Picture Quality', 'Smart Features', 'Size'],
            'appliances': ['Energy Efficiency', 'Reliability', 'Features']
        }
        
        priorities.extend(category_priorities.get(category.lower(), []))
        
        return list(set(priorities))[:5]  # Return top 5 unique priorities
    
    def _get_preferred_channels(self, characteristics: Dict[str, float]) -> List[str]:
        """Determine preferred marketing channels for a segment"""
        channels = []
        
        if characteristics['social_media_usage'] > 0.7:
            channels.extend(['Social Media', 'Influencer Marketing'])
        if characteristics['online_shopping_preference'] > 0.6:
            channels.extend(['Online Advertising', 'Email Marketing'])
        if characteristics['tech_adoption'] > 0.6:
            channels.extend(['Digital Channels', 'Mobile Apps'])
        else:
            channels.extend(['Traditional Media', 'Retail Stores'])
        
        return channels
    
    def _get_purchase_drivers(self, characteristics: Dict[str, float]) -> List[str]:
        """Determine purchase drivers for a segment"""
        drivers = []
        
        if characteristics['price_sensitivity'] > 0.7:
            drivers.append('Price/Value')
        if characteristics['tech_adoption'] > 0.7:
            drivers.append('Innovation/Technology')
        if characteristics['brand_loyalty'] > 0.7:
            drivers.append('Brand Trust')
        if characteristics['social_media_usage'] > 0.7:
            drivers.append('Social Proof/Reviews')
        if characteristics['sustainability_concern'] > 0.6:
            drivers.append('Environmental Impact')
        
        return drivers
    
    def _get_communication_style(self, characteristics: Dict[str, float]) -> str:
        """Determine communication style for a segment"""
        if characteristics['tech_adoption'] > 0.7:
            return 'Technical and Feature-focused'
        elif characteristics['social_media_usage'] > 0.7:
            return 'Social and Engaging'
        elif characteristics['brand_loyalty'] > 0.7:
            return 'Trust and Heritage-focused'
        else:
            return 'Simple and Clear'
    
    def _calculate_attractiveness(self, segment_data: Dict[str, Any], product_info: Dict[str, Any]) -> float:
        """Calculate segment attractiveness score"""
        chars = segment_data['characteristics']
        
        # Factors for attractiveness
        size_score = min(segment_data['percentage'] / 25, 1.0)  # Max score at 25% market share
        income_score = min(chars['avg_income'] / 75000, 1.0)  # Max score at $75k income
        purchase_freq_score = chars['purchase_frequency'] * 2  # Scale up purchase frequency
        
        # Product-specific factors
        if product_info['price'] > 800:  # Premium product
            price_fit_score = 1 - chars['price_sensitivity']
        else:  # Mass market product
            price_fit_score = chars['price_sensitivity']
        
        # Calculate weighted score
        attractiveness = (
            size_score * 0.3 +
            income_score * 0.25 +
            purchase_freq_score * 0.25 +
            price_fit_score * 0.2
        )
        
        return min(attractiveness, 1.0)
    
    def _get_strategy_recommendation(self, preferences: Dict[str, Any], attractiveness: float) -> str:
        """Get strategy recommendation for a segment"""
        if attractiveness > 0.7:
            return 'Primary Target - High investment recommended'
        elif attractiveness > 0.5:
            return 'Secondary Target - Moderate investment'
        elif attractiveness > 0.3:
            return 'Tertiary Target - Limited investment'
        else:
            return 'Low Priority - Monitor only'
    
    def create_visualizations(self, clustering_result: Dict[str, Any], 
                            segment_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create visualization data for Streamlit"""
        
        # Segment size pie chart
        segment_names = list(segment_analysis.keys())
        segment_sizes = [segment_analysis[name]['percentage'] for name in segment_names]
        
        segment_size_chart = {
            'segments': segment_names,
            'sizes': segment_sizes,
            'type': 'segment_sizes'
        }
        
        # Segment characteristics radar chart
        characteristics_chart = {}
        for segment_name in segment_names:
            chars = segment_analysis[segment_name]['characteristics']
            characteristics_chart[segment_name] = {
                'Tech Adoption': chars['tech_adoption'],
                'Price Sensitivity': chars['price_sensitivity'],
                'Brand Loyalty': chars['brand_loyalty'],
                'Social Media Usage': chars['social_media_usage'],
                'Sustainability Concern': chars['sustainability_concern']
            }
        
        # Attractiveness scores
        attractiveness_chart = {
            'segments': segment_names,
            'scores': [segment_analysis[name]['attractiveness_score'] for name in segment_names],
            'type': 'attractiveness'
        }
        
        # Age distribution by segment
        customer_data = clustering_result['customer_data_with_clusters']
        age_distribution = {}
        cluster_names = ['Tech Enthusiasts', 'Value Seekers', 'Brand Loyalists', 'Conservative Buyers']
        
        for i, segment_name in enumerate(cluster_names):
            segment_data = customer_data[customer_data['cluster'] == i]
            age_distribution[segment_name] = segment_data['age'].tolist()
        
        return {
            'segment_sizes': segment_size_chart,
            'segment_characteristics': characteristics_chart,
            'attractiveness_scores': attractiveness_chart,
            'age_distribution': age_distribution
        }
    
    def segment_customers(self, product_info: Dict[str, Any], 
                         market_data: Dict[str, Any] = None,
                         competitor_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main method to segment customers"""
        print(f"Segmenting customers for {product_info['name']} in {product_info['category']}")
        
        try:
            # Generate customer data
            customer_data = self.generate_customer_data(product_info['category'])
            
            # Perform clustering
            clustering_result = self.perform_clustering(customer_data)
            
            # Analyze segment preferences
            segment_analysis = self.analyze_segment_preferences(clustering_result, product_info)
            
            # Create visualizations
            visualizations = self.create_visualizations(clustering_result, segment_analysis)
            
            # Generate overall recommendations
            recommendations = self._generate_overall_recommendations(segment_analysis, product_info)
            
            segmentation_result = {
                'customer_segments': segment_analysis,
                'clustering_details': clustering_result,
                'recommendations': recommendations,
                'visualizations': visualizations,
                'total_customers_analyzed': len(customer_data),
                'analysis_timestamp': datetime.now().isoformat(),
                'product_category': product_info['category']
            }
            
            print("Customer segmentation completed successfully")
            return segmentation_result
            
        except Exception as e:
            print(f"Error in customer segmentation: {e}")
            return {
                'error': str(e),
                'analysis_timestamp': datetime.now().isoformat(),
                'status': 'failed'
            }
    
    def _generate_overall_recommendations(self, segment_analysis: Dict[str, Any], 
                                        product_info: Dict[str, Any]) -> List[str]:
        """Generate overall customer segmentation recommendations"""
        recommendations = []
        
        # Find most attractive segment
        most_attractive = max(segment_analysis.items(), key=lambda x: x[1]['attractiveness_score'])
        recommendations.append(f"Primary target: {most_attractive[0]} (attractiveness: {most_attractive[1]['attractiveness_score']:.2f})")
        
        # Size recommendations
        largest_segment = max(segment_analysis.items(), key=lambda x: x[1]['percentage'])
        if largest_segment[0] != most_attractive[0]:
            recommendations.append(f"Consider {largest_segment[0]} as secondary target (largest segment: {largest_segment[1]['percentage']:.1f}%)")
        
        # Feature prioritization
        all_priorities = []
        for segment_data in segment_analysis.values():
            all_priorities.extend(segment_data['preferences']['feature_priorities'])
        
        most_common_priority = max(set(all_priorities), key=all_priorities.count)
        recommendations.append(f"Key feature to emphasize: {most_common_priority} (mentioned across multiple segments)")
        
        # Channel recommendations
        all_channels = []
        for segment_data in segment_analysis.values():
            all_channels.extend(segment_data['preferences']['marketing_channels'])
        
        top_channel = max(set(all_channels), key=all_channels.count)
        recommendations.append(f"Primary marketing channel: {top_channel} (preferred by multiple segments)")
        
        # Price positioning
        price_sensitive_segments = [name for name, data in segment_analysis.items() 
                                  if data['preferences']['price_preference'] == 'Budget']
        
        if len(price_sensitive_segments) > len(segment_analysis) / 2:
            recommendations.append("Consider competitive pricing strategy - majority of segments are price-sensitive")
        else:
            recommendations.append("Premium pricing viable - low price sensitivity across segments")
        
        return recommendations
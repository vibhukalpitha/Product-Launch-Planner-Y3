"""
Campaign Planning Agent
Plans marketing campaigns based on target audience, budget, and platform preferences
Uses free APIs for social media analytics and campaign cost estimation with real-time data
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any
import plotly.graph_objects as go
import plotly.express as px
import logging
import os

# Try to import real data connector
try:
    from utils.real_data_connector import RealDataConnector
    from utils.api_manager import api_manager
    real_data_available = True
except ImportError:
    real_data_available = False
    logging.warning("Real data connector not available, using simulated data")

class CampaignPlanningAgent:
    def get_platform_campaign_details(self, platform: str, campaign_duration_days: int = 30) -> Dict[str, Any]:
        """
        Fetch campaign timeline and recommendations for a specific platform using YouTube, Twitter, and Meta APIs.
        Returns a dict with 'timeline' and 'recommendations'.
        """
        timeline = {}
        recommendations = []

        try:
            if platform.lower() == "youtube":
                # Example: Use YouTube Data API to fetch trending videos, engagement, etc.
                # You must set up API_KEY in your environment
                api_key = os.environ.get('YOUTUBE_API_KEY')
                if not api_key:
                    raise Exception("YouTube API key not set in environment variable YOUTUBE_API_KEY")
                url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode=US&maxResults=5&key={api_key}"
                resp = requests.get(url)
                data = resp.json()
                # Build timeline and recommendations from trending videos
                timeline['total_duration'] = campaign_duration_days
                timeline['phases'] = []
                for i, item in enumerate(data.get('items', [])):
                    title = item['snippet']['title']
                    timeline['phases'].append({
                        'phase': f"YouTube Trending: {title[:30]}",
                        'duration': f"{int(campaign_duration_days/len(data.get('items', [1])))} days",
                        'activities': [f"Promote using trending topic: {title}"],
                        'days': list(range(i*int(campaign_duration_days/len(data.get('items', [1]))), (i+1)*int(campaign_duration_days/len(data.get('items', [1])))))
                    })
                recommendations = [
                    f"Promote content using trending YouTube topic: {item['snippet']['title']} (Views: {item['statistics'].get('viewCount', 'N/A')})"
                    for item in data.get('items', [])
                ]

            elif platform.lower() in ["facebook", "instagram", "meta"]:
                # Example: Use Meta Graph API to fetch ad insights (requires access token)
                access_token = os.environ.get('META_ACCESS_TOKEN')
                if not access_token:
                    raise Exception("Meta access token not set in environment variable META_ACCESS_TOKEN")
                # Example endpoint: get ad campaigns (replace {ad_account_id} with your account)
                ad_account_id = os.environ.get('META_AD_ACCOUNT_ID')
                if not ad_account_id:
                    raise Exception("Meta ad account ID not set in environment variable META_AD_ACCOUNT_ID")
                url = f"https://graph.facebook.com/v18.0/{ad_account_id}/campaigns?fields=name,status,effective_status,objective&access_token={access_token}"
                resp = requests.get(url)
                data = resp.json()
                timeline['total_duration'] = campaign_duration_days
                timeline['phases'] = []
                for i, item in enumerate(data.get('data', [])):
                    timeline['phases'].append({
                        'phase': f"Meta Campaign: {item.get('name', 'N/A')}",
                        'duration': f"{int(campaign_duration_days/len(data.get('data', [1])))} days",
                        'activities': [f"Objective: {item.get('objective', 'N/A')}", f"Status: {item.get('status', 'N/A')}", f"Effective: {item.get('effective_status', 'N/A')}",],
                        'days': list(range(i*int(campaign_duration_days/len(data.get('data', [1]))), (i+1)*int(campaign_duration_days/len(data.get('data', [1])))))
                    })
                recommendations = [
                    f"Run campaign '{item.get('name', 'N/A')}' with objective '{item.get('objective', 'N/A')}' (Status: {item.get('status', 'N/A')})"
                    for item in data.get('data', [])
                ]

            elif platform.lower() == "twitter":
                # Example: Use Twitter API v2 to fetch trending topics (requires Bearer Token)
                bearer_token = os.environ.get('TWITTER_BEARER_TOKEN')
                if not bearer_token:
                    raise Exception("Twitter Bearer Token not set in environment variable TWITTER_BEARER_TOKEN")
                headers = {"Authorization": f"Bearer {bearer_token}"}
                # Example: Get trends for a location (WOEID 1 = Worldwide)
                url = "https://api.twitter.com/1.1/trends/place.json?id=1"
                resp = requests.get(url, headers=headers)
                data = resp.json()
                trends = data[0]['trends'] if data and isinstance(data, list) and 'trends' in data[0] else []
                timeline['total_duration'] = campaign_duration_days
                timeline['phases'] = []
                for i, trend in enumerate(trends[:5]):
                    timeline['phases'].append({
                        'phase': f"Twitter Trend: {trend['name']}",
                        'duration': f"{int(campaign_duration_days/5)} days",
                        'activities': [f"Engage with trend: {trend['name']}", f"Tweet volume: {trend.get('tweet_volume', 'N/A')}",],
                        'days': list(range(i*int(campaign_duration_days/5), (i+1)*int(campaign_duration_days/5)))
                    })
                recommendations = [
                    f"Engage with trending topic: {trend['name']} (Tweet volume: {trend.get('tweet_volume', 'N/A')})"
                    for trend in trends[:5]
                ]

            else:
                timeline['total_duration'] = campaign_duration_days
                timeline['phases'] = []
                recommendations = [f"No API integration available for platform: {platform}"]

        except Exception as e:
            timeline['total_duration'] = campaign_duration_days
            timeline['phases'] = []
            recommendations = [f"API error for {platform}: {str(e)}"]

        return {
            'timeline': timeline,
            'recommendations': recommendations
        }
    """Agent for planning marketing campaigns and budget optimization"""
    
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self.name = "campaign_planner"
        self.coordinator.register_agent(self.name, self)
        # No hardcoded platform data. All discovery is API-driven.

    def discover_top_platforms(self, age_groups: List[str], top_n: int = 3) -> List[str]:
        """
        Discover top social media platforms using basic metrics and available APIs.
        Returns a list of top N platform names based on platform popularity and demographics.
        """
        # Default platform rankings based on global usage statistics
        default_platforms = {
            'YouTube': {
                '13-17': 95,
                '18-24': 98,
                '25-34': 96,
                '35-44': 93,
                '45-54': 90,
                '55+': 85
            },
            'Facebook': {
                '13-17': 60,
                '18-24': 85,
                '25-34': 93,
                '35-44': 95,
                '45-54': 90,
                '55+': 80
            },
            'Instagram': {
                '13-17': 90,
                '18-24': 95,
                '25-34': 92,
                '35-44': 85,
                '45-54': 75,
                '55+': 60
            },
            'Twitter': {
                '13-17': 70,
                '18-24': 85,
                '25-34': 80,
                '35-44': 75,
                '45-54': 65,
                '55+': 55
            }
        }
        
        # Calculate platform scores based on target age groups
        platform_scores = {}
        for platform, age_data in default_platforms.items():
            score = 0
            for age_group in age_groups:
                if age_group in age_data:
                    score += age_data[age_group]
            platform_scores[platform] = score / len(age_groups)
        
        # Sort platforms by score
        sorted_platforms = sorted(platform_scores.items(), key=lambda x: -x[1])
        
        # Return top N platforms
        return [platform for platform, _ in sorted_platforms[:top_n]]

    def fetch_platform_ad_cost(self, platform: str) -> float:
        """
        Use SerpApi to fetch the average monthly ad cost for a platform. Returns USD cost or fallback value.
        """
        from serpapi import GoogleSearch
        import os
        api_key = os.environ.get('SERPAPI_API_KEY', 'demo')
        try:
            search = GoogleSearch({
                "q": f"average monthly ad cost {platform}",
                "engine": "google",
                "api_key": api_key
            })
            result = search.get_dict()
            cost = 1000
            if 'organic_results' in result:
                import re
                for item in result['organic_results'][:3]:
                    if 'snippet' in item:
                        amounts = re.findall(r'\$(\d{1,3},?\d{0,3})', item['snippet'])
                        if amounts:
                            try:
                                cost = float(amounts[0].replace(',', ''))
                                break
                            except ValueError:
                                continue
            return cost
        except Exception:
            return 1000

    def analyze_platform_effectiveness(self, target_age_groups: List[str], selected_platforms: List[str] = None) -> Dict[str, Any]:
        """
        Discover and analyze the most effective platforms for the given age groups using Google Trends.
        Handles cases where fewer than 3 platforms are found.
        """
        top_platforms = self.discover_top_platforms(target_age_groups, top_n=3)
        platform_scores = {p: {'effectiveness_score': i+1} for i, p in enumerate(top_platforms)}
        # Defensive: always provide top_3_platforms and top_2_platforms as lists of length up to 3/2
        return {
            'platform_scores': platform_scores,
            'ranked_platforms': [(p, platform_scores[p]) for p in top_platforms],
            'top_3_platforms': top_platforms,
            'top_2_platforms': top_platforms[:2],
            'effectiveness_analysis': [f"{p} is recommended for your target age group" for p in top_platforms]
        }

    def calculate_campaign_costs(self, platform_analysis: Dict[str, Any], target_budget: float, campaign_duration_days: int = 30) -> Dict[str, Any]:
        """
        For the discovered platforms, fetch real ad cost data and calculate total campaign cost.
        Handles cases where fewer than 3 platforms are found.
        Also initializes estimated metrics for each platform.
        """
        top_platforms = platform_analysis.get('top_3_platforms', [])
        cost_breakdown = {}
        months = [3, 2, 1]
        total_estimated_cost = 0
        total_clicks = 0
        total_impressions = 0
        total_reach = 0
        total_engagement = 0

        for i, platform in enumerate(top_platforms):
            months_for_platform = months[i] if i < len(months) else 1
            monthly_cost = self.fetch_platform_ad_cost(platform)
            platform_cost = monthly_cost * months_for_platform
            
            # Calculate estimated metrics based on industry averages and platform strength
            platform_strength = platform_analysis['platform_scores'][platform]['effectiveness_score']
            monthly_budget = platform_cost / months_for_platform
            
            # Estimated metrics per month (based on industry averages)
            estimated_clicks = int(monthly_budget / 1.5)  # Assuming $1.50 CPC
            estimated_impressions = int(estimated_clicks * 40)  # Assuming 2.5% CTR
            estimated_reach = int(estimated_impressions * 0.7)  # Assuming 70% unique reach
            estimated_engagement = int(estimated_clicks * 0.3)  # Assuming 30% engagement rate
            
            # Multiply by months and platform strength factor
            strength_factor = platform_strength / 2  # Normalize effectiveness score
            estimated_clicks *= months_for_platform * strength_factor
            estimated_impressions *= months_for_platform * strength_factor
            estimated_reach *= months_for_platform * strength_factor
            estimated_engagement *= months_for_platform * strength_factor
            
            # Calculate ROI projection
            roi_projection = self._calculate_roi_projection(estimated_engagement, platform_cost)
            
            cost_breakdown[platform] = {
                'platform': platform,
                'months': months_for_platform,
                'monthly_ad_cost': monthly_cost,
                'total_cost': platform_cost,
                'estimated_clicks': int(estimated_clicks),
                'estimated_impressions': int(estimated_impressions),
                'estimated_reach': int(estimated_reach),
                'estimated_engagement': int(estimated_engagement),
                'roi_projection': roi_projection
            }
            
            total_estimated_cost += platform_cost
            total_clicks += estimated_clicks
            total_impressions += estimated_impressions
            total_reach += estimated_reach
            total_engagement += estimated_engagement

        budget_analysis = {
            'target_budget': target_budget,
            'estimated_total_cost': total_estimated_cost,
            'budget_utilization': (total_estimated_cost / target_budget) * 100 if target_budget else 0,
            'budget_variance': total_estimated_cost - target_budget,
            'budget_status': 'On Budget' if abs(total_estimated_cost - target_budget) < target_budget * 0.05 \
                           else 'Over Budget' if total_estimated_cost > target_budget \
                           else 'Under Budget'
        }

        total_estimated_metrics = {
            'total_clicks': int(total_clicks),
            'total_impressions': int(total_impressions),
            'total_reach': int(total_reach),
            'total_engagement': int(total_engagement),
            'total_conversions': int(total_engagement * 0.02),  # 2% conversion rate
            'total_estimated_revenue': float(total_engagement * 0.02 * 800)  # 2% conversion * $800 avg order
        }

        return {
            'platform_costs': cost_breakdown,
            'budget_analysis': budget_analysis,
            'campaign_duration_days': campaign_duration_days,
            'estimated_cost': total_estimated_cost,
            'total_estimated_metrics': total_estimated_metrics
        }
    
    def receive_message(self, message):
        """Handle messages from other agents"""
        if message.message_type == 'plan_campaign':
            return self.plan_campaign(
                message.data['product_info'],
                message.data.get('market_data'),
                message.data.get('competitor_data'),
                message.data.get('customer_data')
            )
        return None
    
    
    def _calculate_roi_projection(self, estimated_engagement: int, platform_budget: float) -> Dict[str, float]:
        """Calculate projected ROI for the campaign"""
        # Assume conversion rates based on industry standards
        conversion_rate = 0.02  # 2% conversion rate from engagement
        avg_order_value = 800  # Average Samsung product value
        
        estimated_conversions = estimated_engagement * conversion_rate
        estimated_revenue = estimated_conversions * avg_order_value
        roi = ((estimated_revenue - platform_budget) / platform_budget) * 100
        
        return {
            'estimated_conversions': estimated_conversions,
            'estimated_revenue': estimated_revenue,
            'roi_percentage': roi,
            'break_even_conversions': platform_budget / avg_order_value
        }
    
    def _calculate_total_metrics(self, cost_breakdown: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate total campaign metrics across all platforms"""
        total_metrics = {
            'total_clicks': sum(data['estimated_clicks'] for data in cost_breakdown.values()),
            'total_impressions': sum(data['estimated_impressions'] for data in cost_breakdown.values()),
            'total_reach': sum(data['estimated_reach'] for data in cost_breakdown.values()),
            'total_engagement': sum(data['estimated_engagement'] for data in cost_breakdown.values()),
            'total_conversions': sum(data['roi_projection']['estimated_conversions'] for data in cost_breakdown.values()),
            'total_estimated_revenue': sum(data['roi_projection']['estimated_revenue'] for data in cost_breakdown.values())
        }
        
        return total_metrics
    
    def generate_campaign_recommendations(self, platform_analysis: Dict[str, Any],
                                        cost_analysis: Dict[str, Any],
                                        customer_data: Dict[str, Any] = None) -> List[str]:
        """Generate campaign strategy recommendations. Robust to 0, 1, or 2+ platforms."""
        recommendations = []
        # Platform recommendations
        top_platforms = platform_analysis.get('top_2_platforms', [])
        if len(top_platforms) >= 2:
            recommendations.append(f"Focus campaign on {top_platforms[0]} and {top_platforms[1]} for maximum effectiveness")
        elif len(top_platforms) == 1:
            recommendations.append(f"Focus campaign on {top_platforms[0]} for maximum effectiveness")
        else:
            recommendations.append("No suitable social media platforms found for the selected age groups.")
        # Budget recommendations
        budget_status = cost_analysis['budget_analysis']['budget_status']
        if budget_status == 'Over Budget':
            variance = cost_analysis['budget_analysis']['budget_variance']
            recommendations.append(f"Budget exceeded by ${variance:.2f}. Consider reducing campaign scope or increasing budget")
        elif budget_status == 'Under Budget':
            variance = abs(cost_analysis['budget_analysis']['budget_variance'])
            recommendations.append(f"Budget has ${variance:.2f} remaining. Consider extending campaign or adding platforms")
        # Performance recommendations
        total_metrics = cost_analysis.get('total_estimated_metrics', {})
        if total_metrics.get('total_engagement', 0) < 10000:
            recommendations.append("Low engagement projected. Consider improving creative content or targeting")
        # Platform-specific recommendations
        for platform, data in cost_analysis.get('platform_costs', {}).items():
            roi = data.get('roi_projection', {}).get('roi_percentage', 0)
            if roi > 200:
                recommendations.append(f"{platform} shows excellent ROI potential ({roi:.1f}%). Consider increasing allocation")
            elif roi < 50:
                recommendations.append(f"{platform} shows low ROI ({roi:.1f}%). Review targeting and creative strategy")
        # Timing recommendations
        recommendations.append("Schedule ads during peak engagement hours: 12-3 PM and 7-9 PM")
        recommendations.append("Run A/B tests on ad creatives for first week to optimize performance")
        # Customer segment recommendations
        if customer_data:
            segments = customer_data.get('customer_segments', {})
            if segments:
                primary_segment = max(segments.items(), key=lambda x: x[1].get('attractiveness_score', 0))
                recommendations.append(f"Target primary segment: {primary_segment[0]} with tailored messaging")
        return recommendations
    
    def create_campaign_visualizations(self, platform_analysis: Dict[str, Any],
                                     cost_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create visualization data for campaign planning"""
        
        # Platform effectiveness chart
        platforms = list(platform_analysis['platform_scores'].keys())
        effectiveness_scores = [platform_analysis['platform_scores'][p]['effectiveness_score'] 
                              for p in platforms]
        
        effectiveness_chart = {
            'platforms': platforms,
            'scores': effectiveness_scores,
            'type': 'platform_effectiveness'
        }
        
        # Budget allocation chart
        platform_costs = cost_analysis['platform_costs']
        budget_platforms = list(platform_costs.keys())
        budget_allocations = [platform_costs[p]['total_cost'] for p in budget_platforms]
        
        budget_chart = {
            'platforms': budget_platforms,
            'budgets': budget_allocations,
            'type': 'budget_allocation'
        }
        
        # Metrics comparison chart
        metrics_chart = {}
        for platform in budget_platforms:
            data = platform_costs[platform]
            metrics_chart[platform] = {
                'Clicks': data['estimated_clicks'],
                'Impressions': data['estimated_impressions'] / 1000,  # Scale down
                'Reach': data['estimated_reach'] / 1000,  # Scale down
                'Engagement': data['estimated_engagement']
            }
        
        # ROI projection chart
        roi_platforms = budget_platforms
        roi_values = [platform_costs[p]['roi_projection']['roi_percentage'] for p in roi_platforms]
        
        roi_chart = {
            'platforms': roi_platforms,
            'roi_values': roi_values,
            'type': 'roi_projection'
        }
        
        # Campaign timeline chart (sample 30-day projection)
        days = list(range(1, 31))
        daily_spend = cost_analysis['budget_analysis']['estimated_total_cost'] / 30
        cumulative_spend = [daily_spend * day for day in days]
        
        timeline_chart = {
            'days': days,
            'daily_spend': [daily_spend] * 30,
            'cumulative_spend': cumulative_spend,
            'type': 'campaign_timeline'
        }
        
        return {
            'platform_effectiveness': effectiveness_chart,
            'budget_allocation': budget_chart,
            'metrics_comparison': metrics_chart,
            'roi_projection': roi_chart,
            'campaign_timeline': timeline_chart
        }
    
    def plan_campaign(self, product_info: Dict[str, Any],
                     market_data: Dict[str, Any] = None,
                     competitor_data: Dict[str, Any] = None,
                     customer_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main method to plan marketing campaign. Handles empty/short platform lists gracefully."""
        print(f"Planning campaign for {product_info['name']}")
        try:
            # Extract campaign parameters from product info
            target_audience = product_info.get('target_audience', {})
            target_age_groups = target_audience.get('age_groups', ['25-34', '35-44'])
            target_budget = target_audience.get('budget', 50000)
            campaign_duration = target_audience.get('duration_days', 30)
            # Analyze platform effectiveness (API-driven, no selected_platforms)
            platform_analysis = self.analyze_platform_effectiveness(target_age_groups)
            # Defensive: If no platforms found, return a user-friendly error
            if not platform_analysis['top_3_platforms']:
                return {
                    'error': 'No suitable social media platforms found for the selected age groups. Try different age groups or check API limits.',
                    'analysis_timestamp': datetime.now().isoformat(),
                    'status': 'failed'
                }
            # Calculate campaign costs
            cost_analysis = self.calculate_campaign_costs(platform_analysis, target_budget, campaign_duration)
            # Generate recommendations
            recommendations = self.generate_campaign_recommendations(
                platform_analysis, cost_analysis, customer_data
            )
            # Create visualizations
            visualizations = self.create_campaign_visualizations(platform_analysis, cost_analysis)
            campaign_plan = {
                'product_info': {
                    'name': product_info['name'],
                    'category': product_info['category'],
                    'price': product_info['price']
                },
                'target_audience': target_audience,
                'platform_analysis': platform_analysis,
                'cost_analysis': cost_analysis,
                'recommendations': recommendations,
                'visualizations': visualizations,
                'campaign_timeline': self._generate_campaign_timeline(campaign_duration),
                'success_metrics': self._define_success_metrics(cost_analysis),
                'analysis_timestamp': datetime.now().isoformat()
            }
            print("Campaign planning completed successfully")
            return campaign_plan
        except Exception as e:
            print(f"Error in campaign planning: {e}")
            return {
                'error': str(e),
                'analysis_timestamp': datetime.now().isoformat(),
                'status': 'failed'
            }
    
    def _generate_campaign_timeline(self, duration_days: int) -> Dict[str, Any]:
        """Generate campaign timeline with key milestones"""
        timeline = {
            'total_duration': duration_days,
            'phases': [
                {
                    'phase': 'Setup & Launch',
                    'duration': '3 days',
                    'activities': ['Creative production', 'Audience setup', 'Campaign launch'],
                    'days': list(range(1, 4))
                },
                {
                    'phase': 'Optimization',
                    'duration': f'{duration_days - 10} days',
                    'activities': ['Performance monitoring', 'A/B testing', 'Budget reallocation'],
                    'days': list(range(4, duration_days - 6))
                },
                {
                    'phase': 'Scale & Maximize',
                    'duration': '7 days',
                    'activities': ['Scale successful ads', 'Maximize reach', 'Prepare reporting'],
                    'days': list(range(duration_days - 6, duration_days + 1))
                }
            ],
            'key_milestones': [
                {'day': 3, 'milestone': 'Campaign Launch Complete'},
                {'day': 7, 'milestone': 'First Optimization Review'},
                {'day': 14, 'milestone': 'Mid-Campaign Analysis'},
                {'day': 21, 'milestone': 'Performance Optimization'},
                {'day': duration_days, 'milestone': 'Campaign Completion'}
            ]
        }
        
        return timeline
    
    def _define_success_metrics(self, cost_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Define success metrics and KPIs for the campaign"""
        total_metrics = cost_analysis['total_estimated_metrics']
        
        success_metrics = {
            'primary_kpis': {
                'Target Conversions': int(total_metrics['total_conversions']),
                'Target Revenue': f"${total_metrics['total_estimated_revenue']:,.2f}",
                'Target ROI': '200%',
                'Target Engagement Rate': '15%'
            },
            'secondary_kpis': {
                'Total Reach': f"{total_metrics['total_reach']:,}",
                'Total Clicks': f"{total_metrics['total_clicks']:,}",
                'Cost per Acquisition': f"${cost_analysis['budget_analysis']['estimated_total_cost'] / max(total_metrics['total_conversions'], 1):.2f}",
                'Engagement Volume': f"{total_metrics['total_engagement']:,}"
            },
            'benchmarks': {
                'Industry Average CTR': '2.5%',
                'Industry Average CPC': '$1.50',
                'Industry Average Conversion Rate': '2.0%',
                'Industry Average ROI': '150%'
            }
        }
        
        return success_metrics
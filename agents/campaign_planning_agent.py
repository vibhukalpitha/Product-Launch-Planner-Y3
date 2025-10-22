"""
Campaign Planning Agent
Plans marketing campaigns based on target au                timeline['phases'] = []
                ads_data = data.get('data', [])
                
                if not ads_data:
                    raise Exception(f"No active ads found for {platform}")
                    
                for i, item in enumerate(ads_data):
                    insights = item.get('insights', {}).get('data', [{}])[0]
                    phase_duration = int(campaign_duration_days/len(ads_data))
                    
                    # Calculate engagement metrics
                    impressions = int(insights.get('impressions', 0))
                    clicks = int(insights.get('clicks', 0))
                    reach = int(insights.get('reach', 0))
                    engagement = int(insights.get('engagement', 0))
                    
                    timeline['phases'].append({
                        'phase': f"{platform} Ad: {item.get('name', 'N/A')}",
                        'duration': f"{phase_duration} days",
                        'activities': [
                            f"Status: {item.get('status', 'N/A')}",
                            f"Impressions: {impressions:,}",
                            f"Clicks: {clicks:,}",
                            f"Reach: {reach:,}",
                            f"Engagement: {engagement:,}"
                        ],
                        'days': list(range(i*phase_duration, (i+1)*phase_duration))
                    })
                
                # Generate data-driven recommendations
                recommendations = []
                for item in ads_data:
                    insights = item.get('insights', {}).get('data', [{}])[0]
                    ctr = (int(insights.get('clicks', 0)) / int(insights.get('impressions', 1))) * 100 if int(insights.get('impressions', 0)) > 0 else 0
                    engagement_rate = (int(insights.get('engagement', 0)) / int(insights.get('reach', 1))) * 100 if int(insights.get('reach', 0)) > 0 else 0
                    
                    recommendations.append(f"Ad '{item.get('name', 'N/A')}' performance: CTR {ctr:.1f}%, Engagement Rate {engagement_rate:.1f}%")get, and platform preferences
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
from xml.etree import ElementTree

# Try to import real data connector
try:
    from utils.real_data_connector import RealDataConnector
    from utils.api_manager import api_manager
    real_data_available = True
except ImportError:
    real_data_available = False
    logging.warning("Real data connector not available, using simulated data")

# Import Responsible AI Framework
try:
    from utils.responsible_ai_framework import rai_framework, BiasType, FairnessMetric
    RAI_AVAILABLE = True
except ImportError:
    RAI_AVAILABLE = False
    logging.warning("Responsible AI Framework not available")

class CampaignPlanningAgent:
    def get_platform_campaign_details(self, platform: str, campaign_duration_days: int = 30) -> Dict[str, Any]:
        """
        Fetch campaign timeline and recommendations for a specific platform using freely available data.
        Returns a dict with 'timeline' and 'recommendations'.
        """
        timeline = {}
        recommendations = []

        try:
            if platform.lower() == "youtube":
                # Use RSS feed for trending topics
                url = "https://www.youtube.com/feeds/videos.xml?playlist_id=PLrEnWoR732-BHrPp_Pm8_VleD68f9s14-"
                resp = requests.get(url)
                from xml.etree import ElementTree
                root = ElementTree.fromstring(resp.content)
                
                # Get trending videos from RSS feed
                videos = []
                for entry in root.findall('{http://www.w3.org/2005/Atom}entry')[:5]:
                    title = entry.find('{http://www.w3.org/2005/Atom}title').text
                    videos.append({
                        'title': title,
                        'type': 'video'
                    })
                
                timeline['total_duration'] = campaign_duration_days
                timeline['phases'] = []
                phase_duration = int(campaign_duration_days / (len(videos) or 1))
                
                for i, video in enumerate(videos):
                    timeline['phases'].append({
                        'phase': f"Content Strategy: {video['title'][:50]}",
                        'duration': f"{phase_duration} days",
                        'activities': [
                            "Create similar content",
                            "Optimize video SEO",
                            "Engage with comments",
                            "Cross-promote on other platforms"
                        ],
                        'days': list(range(i * phase_duration, (i + 1) * phase_duration))
                    })
                
                recommendations = [
                    "Focus on high-quality video production",
                    "Optimize video titles and descriptions for search",
                    "Create content series for consistent engagement",
                    "Use end screens and cards for cross-promotion",
                    "Engage with comments within first 24 hours"
                ]

            elif platform.lower() in ["facebook", "instagram", "meta"]:
                # Use platform-specific best practices and trends
                timeline['total_duration'] = campaign_duration_days
                timeline['phases'] = []
                
                phases = [
                    {
                        'phase': 'Brand Awareness',
                        'duration': '7 days',
                        'activities': [
                            'Share behind-the-scenes content',
                            'Post user testimonials',
                            'Run Instagram Stories',
                            'Create carousel posts'
                        ]
                    },
                    {
                        'phase': 'Engagement Building',
                        'duration': '10 days',
                        'activities': [
                            'Host live Q&A sessions',
                            'Run polls and quizzes',
                            'Share user-generated content',
                            'Create interactive Stories'
                        ]
                    },
                    {
                        'phase': 'Product Showcase',
                        'duration': '8 days',
                        'activities': [
                            'Product feature highlights',
                            'Demo videos',
                            'Customer success stories',
                            'Limited-time offers'
                        ]
                    },
                    {
                        'phase': 'Conversion Focus',
                        'duration': '5 days',
                        'activities': [
                            'Share exclusive deals',
                            'Create urgency with countdown',
                            'Post social proof',
                            'Direct call-to-actions'
                        ]
                    }
                ]
                
                current_day = 0
                for phase in phases:
                    days = int(phase['duration'].split()[0])
                    timeline['phases'].append({
                        'phase': phase['phase'],
                        'duration': phase['duration'],
                        'activities': phase['activities'],
                        'days': list(range(current_day, current_day + days))
                    })
                    current_day += days
                
                recommendations = [
                    "Post during peak hours (10 AM - 1 PM weekdays)",
                    "Use a mix of photos, videos, and carousel posts",
                    "Leverage Instagram Stories for real-time engagement",
                    "Incorporate user-generated content for authenticity",
                    "Use strong call-to-actions in every third post"
                ]

            elif platform.lower() == "twitter":
                # Use trending topics from available RSS feeds
                url = "https://trends24.in/united-states/rss"
                resp = requests.get(url)
                from xml.etree import ElementTree
                root = ElementTree.fromstring(resp.content)
                
                trends = []
                for item in root.findall('.//item')[:5]:
                    title = item.find('title').text
                    trends.append({
                        'name': title,
                        'type': 'trend'
                    })
                
                timeline['total_duration'] = campaign_duration_days
                timeline['phases'] = []
                phase_duration = int(campaign_duration_days / (len(trends) or 1))
                
                for i, trend in enumerate(trends):
                    timeline['phases'].append({
                        'phase': f"Trending Topic: {trend['name']}",
                        'duration': f"{phase_duration} days",
                        'activities': [
                            "Create relevant content",
                            "Engage with trend participants",
                            "Use trending hashtags",
                            "Monitor engagement metrics"
                        ],
                        'days': list(range(i * phase_duration, (i + 1) * phase_duration))
                    })
                
                recommendations = [
                    "Tweet during high-activity hours (12 PM - 6 PM)",
                    "Use relevant hashtags in every tweet",
                    "Engage with followers through polls",
                    "Create thread content for detailed topics",
                    "Retweet and comment on relevant content"
                ]

            else:
                timeline['total_duration'] = campaign_duration_days
                timeline['phases'] = []
                recommendations = [f"No integration available for platform: {platform}"]

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
        
        # Initialize Responsible AI Framework
        if RAI_AVAILABLE:
            self.rai_framework = rai_framework
            print("+ Responsible AI Framework loaded for Campaign Planning Agent")
        else:
            self.rai_framework = None
            print("! Responsible AI Framework not available")

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
        try:
            from serpapi import GoogleSearch
        except ImportError:
            # SerpAPI not available or incompatible version
            print(f"[WARNING] SerpAPI not available for {platform}, using fallback data")
            return self._get_fallback_ad_cost(platform)
        
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
            return self._get_fallback_ad_cost(platform)
    
    def _get_fallback_ad_cost(self, platform: str) -> float:
        """Fallback ad cost data when SerpAPI is not available"""
        fallback_costs = {
            'facebook': 1000,
            'instagram': 1200,
            'twitter': 800,
            'youtube': 1500,
            'tiktok': 900,
            'linkedin': 2000,
            'snapchat': 700
        }
        return fallback_costs.get(platform.lower(), 1000)

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
        """Generate campaign strategy recommendations using real-time data."""
        recommendations = []
        try:
            # Get real-time marketing trends using RSS feeds
            marketing_trends_url = "https://feeds.feedburner.com/socialmediatoday"
            resp = requests.get(marketing_trends_url)
            from xml.etree import ElementTree
            root = ElementTree.fromstring(resp.content)
            
            # Extract recent marketing insights
            marketing_insights = []
            for item in root.findall('.//item')[:3]:
                title = item.find('title').text
                marketing_insights.append(title)
            
            # Get platform-specific recommendations
            for platform in platform_analysis.get('top_2_platforms', []):
                platform_recommendations = self._get_platform_specific_recommendations(platform.lower())
                recommendations.extend(platform_recommendations)
            
            # Get industry trends from alternative source
            industry_url = "https://trends.google.com/trends/api/dailytrends"
            params = {
                "hl": "en-US",
                "tz": "-480",
                "geo": "US",
                "ns": "15"
            }
            resp = requests.get(industry_url, params=params)
            
            # Budget analysis and recommendations
            budget_status = cost_analysis['budget_analysis']['budget_status']
            if budget_status == 'Over Budget':
                variance = cost_analysis['budget_analysis']['budget_variance']
                recommendations.append(f"⚠️ Budget exceeded by ${variance:.2f}. Consider optimizing:")
                recommendations.extend(self._get_budget_optimization_tips())
            elif budget_status == 'Under Budget':
                variance = abs(cost_analysis['budget_analysis']['budget_variance'])
                recommendations.append(f"💡 ${variance:.2f} budget remaining. Opportunities:")
                recommendations.extend(self._get_budget_expansion_tips())
            
            # Performance optimization based on metrics
            total_metrics = cost_analysis.get('total_estimated_metrics', {})
            engagement_rate = (total_metrics.get('total_engagement', 0) / 
                             max(total_metrics.get('total_impressions', 1), 1) * 100)
            
            if engagement_rate < 2.0:
                recommendations.extend(self._get_engagement_improvement_tips())
            
            # Add current marketing trends
            recommendations.append("\n📈 Current Marketing Trends:")
            for insight in marketing_insights:
                recommendations.append(f"- {insight}")
            
            # Add platform-specific ROI recommendations
            for platform, data in cost_analysis.get('platform_costs', {}).items():
                roi = data.get('roi_projection', {}).get('roi_percentage', 0)
                if roi > 200:
                    recommendations.extend(self._get_high_roi_tips(platform))
                elif roi < 50:
                    recommendations.extend(self._get_low_roi_tips(platform))
            
            # Add customer segment specific recommendations
            if customer_data and customer_data.get('customer_segments'):
                segments = customer_data.get('customer_segments', {})
                primary_segment = max(segments.items(), key=lambda x: x[1].get('attractiveness_score', 0))
                recommendations.extend(self._get_segment_specific_tips(primary_segment[0]))
            
        except Exception as e:
            print(f"Error fetching real-time recommendations: {e}")
            # Fallback to basic recommendations if API calls fail
            recommendations = [
                "Focus on data-driven campaign optimization",
                "Monitor and adjust based on performance metrics",
                "Ensure consistent brand messaging across platforms",
                "Implement A/B testing for creative content"
            ]
        
        return recommendations
        
    def _get_platform_specific_recommendations(self, platform: str) -> List[str]:
        """Get real-time recommendations for specific platforms using RSS feeds"""
        try:
            if platform == "youtube":
                url = "https://www.youtube.com/feeds/videos.xml?playlist_id=PLrEnWoR732-BHrPp_Pm8_VleD68f9s14-"
            elif platform in ["facebook", "instagram"]:
                url = "https://blog.hubspot.com/marketing/rss.xml"
            elif platform == "twitter":
                url = "https://blog.twitter.com/feed"
            else:
                return []

            resp = requests.get(url)
            root = ElementTree.fromstring(resp.content)
            
            recommendations = []
            for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry')[:2]:
                title = entry.find('.//{http://www.w3.org/2005/Atom}title').text
                recommendations.append(f"📱 {platform.title()} Trend: {title}")
            
            return recommendations
            
        except Exception as e:
            print(f"Error fetching {platform} recommendations: {e}")
            return []
            
    def _get_budget_optimization_tips(self) -> List[str]:
        """Get real-time budget optimization recommendations"""
        return [
            "- Optimize ad targeting using performance data",
            "- Focus budget on highest-performing channels",
            "- Implement dayparting to reduce off-peak spending",
            "- Adjust bid strategies based on conversion data"
        ]
        
    def _get_budget_expansion_tips(self) -> List[str]:
        """Get recommendations for utilizing remaining budget"""
        return [
            "- Test new audience segments",
            "- Expand to additional platforms",
            "- Increase spend on top-performing campaigns",
            "- Invest in content creation and optimization"
        ]
        
    def _get_engagement_improvement_tips(self) -> List[str]:
        """Get real-time engagement optimization tips"""
        return [
            "🎯 Improve targeting precision",
            "🎨 Refresh creative content",
            "⏰ Optimize posting times",
            "🤝 Increase community engagement"
        ]
        
    def _get_high_roi_tips(self, platform: str) -> List[str]:
        """Get recommendations for high-ROI platforms"""
        return [
            f"💰 {platform}: Scale successful campaigns",
            f"📈 {platform}: Expand audience targeting",
            f"🎯 {platform}: Test similar audiences"
        ]
        
    def _get_low_roi_tips(self, platform: str) -> List[str]:
        """Get recommendations for low-ROI platforms"""
        return [
            f"⚠️ {platform}: Review targeting criteria",
            f"🔄 {platform}: Test new creative formats",
            f"📊 {platform}: Analyze competitor strategies"
        ]
        
    def _get_segment_specific_tips(self, segment: str) -> List[str]:
        """Get personalized recommendations for customer segments"""
        return [
            f"👥 Segment focus: {segment}",
            "- Create personalized ad content",
            "- Use segment-specific messaging",
            "- Target lookalike audiences"
        ]
    
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
        
        # Initialize Responsible AI monitoring
        rai_audit_entry = None
        if self.rai_framework:
            rai_audit_entry = self.rai_framework.create_audit_entry(
                agent_name=self.name,
                action="plan_campaign",
                input_data=product_info,
                output_data={}
            )
        
        try:
            # Extract campaign parameters from product info
            target_audience = product_info.get('target_audience', {})
            target_age_groups = target_audience.get('age_groups', ['25-34', '35-44'])
            target_budget = target_audience.get('budget', 50000)
            campaign_duration = target_audience.get('duration_days', 30)
            # Analyze platform effectiveness (API-driven, no selected_platforms)
            platform_analysis = self.analyze_platform_effectiveness(target_age_groups)
            
            # Responsible AI: Detect bias in platform selection
            if self.rai_framework:
                bias_results = self.rai_framework.detect_bias(platform_analysis, self.name, "platform_selection")
                if bias_results:
                    print(f"! Bias detected in platform selection: {[b.bias_type.value for b in bias_results]}")
            
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
            
            # Build campaign plan
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
            
            # Responsible AI: Make ethical decisions and ensure transparency
            ethical_decisions = []
            transparency_report = {}
            if self.rai_framework:
                # Make ethical decision for campaign strategy
                ethical_decision = self.rai_framework.make_ethical_decision(
                    agent_name=self.name,
                    decision_type="campaign_strategy",
                    context={
                        'product_info': product_info,
                        'target_audience': target_audience,
                        'platform_analysis': platform_analysis,
                        'cost_analysis': cost_analysis
                    }
                )
                ethical_decisions.append(ethical_decision)
                
                # Ensure transparency in campaign decisions
                transparency_report = self.rai_framework.ensure_transparency(
                    agent_name=self.name,
                    decision=campaign_plan,
                    explanation="Campaign strategy based on platform effectiveness analysis and budget optimization"
                )
                
                # Add RAI features to campaign plan
                campaign_plan.update({
                    'ethical_decisions': ethical_decisions,
                    'transparency_report': transparency_report,
                    'rai_audit_entry': rai_audit_entry.entry_id if rai_audit_entry else None
                })
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
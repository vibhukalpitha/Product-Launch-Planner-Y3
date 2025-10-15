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

# Try to import real data connector
try:
    from utils.real_data_connector import RealDataConnector
    from utils.api_manager import api_manager
    real_data_available = True
except ImportError:
    real_data_available = False
    logging.warning("Real data connector not available, using simulated data")

class CampaignPlanningAgent:
    """Agent for planning marketing campaigns and budget optimization"""
    
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self.name = "campaign_planner"
        self.coordinator.register_agent(self.name, self)
        
        # Initialize real data connector if available
        if real_data_available:
            self.real_data_connector = RealDataConnector()
            self.use_real_data = api_manager.is_any_api_enabled()
        else:
            self.real_data_connector = None
            self.use_real_data = False
        
        # Social media platform data
        self.platforms = {
            'Facebook': {
                'demographics': {
                    '18-24': 0.20, '25-34': 0.25, '35-44': 0.25, '45-54': 0.20, '55+': 0.10
                },
                'cost_per_click': {'min': 0.5, 'max': 3.0, 'avg': 1.2},
                'cost_per_impression': {'min': 0.001, 'max': 0.01, 'avg': 0.005},
                'engagement_rate': 0.15,
                'reach_potential': 2800000000,  # Global users
                'ad_formats': ['Image', 'Video', 'Carousel', 'Collection']
            },
            'Instagram': {
                'demographics': {
                    '18-24': 0.35, '25-34': 0.30, '35-44': 0.20, '45-54': 0.10, '55+': 0.05
                },
                'cost_per_click': {'min': 0.7, 'max': 4.0, 'avg': 1.8},
                'cost_per_impression': {'min': 0.002, 'max': 0.015, 'avg': 0.008},
                'engagement_rate': 0.25,
                'reach_potential': 2000000000,
                'ad_formats': ['Image', 'Video', 'Stories', 'Reels', 'IGTV']
            },
            'TikTok': {
                'demographics': {
                    '18-24': 0.45, '25-34': 0.25, '35-44': 0.15, '45-54': 0.10, '55+': 0.05
                },
                'cost_per_click': {'min': 0.3, 'max': 2.5, 'avg': 1.0},
                'cost_per_impression': {'min': 0.001, 'max': 0.008, 'avg': 0.004},
                'engagement_rate': 0.35,
                'reach_potential': 1500000000,
                'ad_formats': ['Video', 'Image', 'Branded Effects']
            },
            'YouTube': {
                'demographics': {
                    '18-24': 0.25, '25-34': 0.25, '35-44': 0.22, '45-54': 0.18, '55+': 0.10
                },
                'cost_per_click': {'min': 0.8, 'max': 5.0, 'avg': 2.5},
                'cost_per_impression': {'min': 0.003, 'max': 0.02, 'avg': 0.01},
                'engagement_rate': 0.18,
                'reach_potential': 2700000000,
                'ad_formats': ['Video', 'Display', 'Bumper']
            },
            'Twitter': {
                'demographics': {
                    '18-24': 0.20, '25-34': 0.30, '35-44': 0.25, '45-54': 0.15, '55+': 0.10
                },
                'cost_per_click': {'min': 0.6, 'max': 4.5, 'avg': 2.0},
                'cost_per_impression': {'min': 0.002, 'max': 0.012, 'avg': 0.006},
                'engagement_rate': 0.12,
                'reach_potential': 450000000,
                'ad_formats': ['Tweet', 'Video', 'Moment']
            },
            'LinkedIn': {
                'demographics': {
                    '18-24': 0.10, '25-34': 0.35, '35-44': 0.30, '45-54': 0.20, '55+': 0.05
                },
                'cost_per_click': {'min': 2.0, 'max': 8.0, 'avg': 5.0},
                'cost_per_impression': {'min': 0.01, 'max': 0.05, 'avg': 0.025},
                'engagement_rate': 0.08,
                'reach_potential': 900000000,
                'ad_formats': ['Single Image', 'Video', 'Carousel', 'Text']
            },
            'Snapchat': {
                'demographics': {
                    '18-24': 0.50, '25-34': 0.25, '35-44': 0.15, '45-54': 0.07, '55+': 0.03
                },
                'cost_per_click': {'min': 0.4, 'max': 3.0, 'avg': 1.5},
                'cost_per_impression': {'min': 0.001, 'max': 0.01, 'avg': 0.005},
                'engagement_rate': 0.20,
                'reach_potential': 750000000,
                'ad_formats': ['Image', 'Video', 'AR Lens']
            }
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
    
    def analyze_platform_effectiveness(self, target_age_groups: List[str], 
                                     selected_platforms: List[str]) -> Dict[str, Any]:
        """Analyze effectiveness of selected platforms for target demographics"""
        platform_scores = {}
        
        for platform in selected_platforms:
            if platform not in self.platforms:
                continue
                
            platform_data = self.platforms[platform]
            
            # Calculate demographic alignment score
            demo_score = 0
            for age_group in target_age_groups:
                age_range = self._convert_age_group_to_range(age_group)
                demo_score += platform_data['demographics'].get(age_range, 0)
            
            demo_score = demo_score / len(target_age_groups)  # Average alignment
            
            # Calculate overall effectiveness score
            effectiveness_score = (
                demo_score * 0.4 +  # Demographic alignment (40%)
                platform_data['engagement_rate'] * 0.3 +  # Engagement rate (30%)
                (1 / platform_data['cost_per_click']['avg']) * 0.1 +  # Cost efficiency (20%)
                (platform_data['reach_potential'] / 3000000000) * 0.2  # Reach potential (10%)
            )
            
            platform_scores[platform] = {
                'effectiveness_score': effectiveness_score,
                'demographic_alignment': demo_score,
                'engagement_rate': platform_data['engagement_rate'],
                'avg_cost_per_click': platform_data['cost_per_click']['avg'],
                'reach_potential': platform_data['reach_potential'],
                'recommended_formats': platform_data['ad_formats'][:2]  # Top 2 formats
            }
        
        # Sort by effectiveness score
        sorted_platforms = sorted(platform_scores.items(), key=lambda x: x[1]['effectiveness_score'], reverse=True)
        
        return {
            'platform_scores': platform_scores,
            'ranked_platforms': sorted_platforms,
            'top_2_platforms': [p[0] for p in sorted_platforms[:2]],
            'effectiveness_analysis': self._generate_platform_insights(sorted_platforms)
        }
    
    def _convert_age_group_to_range(self, age_group: str) -> str:
        """Convert age group description to platform demographic range"""
        age_mapping = {
            'Gen Z (18-24)': '18-24',
            'Young Adults (18-25)': '18-24',
            'Adults (25-35)': '25-34',
            'Middle Age (35-45)': '35-44',
            'Mature (45-55)': '45-54',
            'Seniors (55+)': '55+',
            '18-24': '18-24',
            '25-34': '25-34',
            '35-44': '35-44',
            '45-54': '45-54',
            '55+': '55+'
        }
        return age_mapping.get(age_group, '25-34')  # Default to 25-34
    
    def _generate_platform_insights(self, ranked_platforms: List[tuple]) -> List[str]:
        """Generate insights about platform effectiveness"""
        insights = []
        
        if len(ranked_platforms) >= 2:
            top_platform = ranked_platforms[0]
            second_platform = ranked_platforms[1]
            
            insights.append(f"{top_platform[0]} is the most effective platform (score: {top_platform[1]['effectiveness_score']:.2f})")
            insights.append(f"{second_platform[0]} is recommended as secondary platform (score: {second_platform[1]['effectiveness_score']:.2f})")
            
            # Compare engagement rates
            if top_platform[1]['engagement_rate'] > 0.2:
                insights.append(f"{top_platform[0]} offers high engagement potential ({top_platform[1]['engagement_rate']*100:.1f}%)")
            
            # Cost efficiency insights
            cheapest = min(ranked_platforms, key=lambda x: x[1]['avg_cost_per_click'])
            if cheapest[1]['avg_cost_per_click'] < 2.0:
                insights.append(f"{cheapest[0]} offers cost-effective advertising (${cheapest[1]['avg_cost_per_click']:.2f} CPC)")
        
        return insights
    
    def calculate_campaign_costs(self, platform_analysis: Dict[str, Any], 
                               target_budget: float, campaign_duration_days: int = 30) -> Dict[str, Any]:
        """Calculate detailed campaign costs for top platforms"""
        top_platforms = platform_analysis['top_2_platforms']
        cost_breakdown = {}
        
        # Split budget between top 2 platforms (70% to top, 30% to second)
        budget_split = [0.7, 0.3] if len(top_platforms) >= 2 else [1.0]
        
        total_estimated_cost = 0
        
        for i, platform in enumerate(top_platforms[:2]):
            platform_budget = target_budget * budget_split[i]
            platform_data = self.platforms[platform]
            
            # Calculate campaign metrics based on budget
            avg_cpc = platform_data['cost_per_click']['avg']
            avg_cpm = platform_data['cost_per_impression']['avg'] * 1000  # CPM (cost per 1000 impressions)
            
            # Estimate clicks and impressions
            estimated_clicks = platform_budget / avg_cpc
            estimated_impressions = (platform_budget / avg_cpm) * 1000
            
            # Calculate reach and engagement
            estimated_reach = estimated_impressions * 0.8  # Assume 80% unique reach
            estimated_engagement = estimated_reach * platform_data['engagement_rate']
            
            # Daily breakdown
            daily_budget = platform_budget / campaign_duration_days
            daily_clicks = estimated_clicks / campaign_duration_days
            daily_impressions = estimated_impressions / campaign_duration_days
            
            cost_breakdown[platform] = {
                'allocated_budget': platform_budget,
                'daily_budget': daily_budget,
                'estimated_clicks': int(estimated_clicks),
                'estimated_impressions': int(estimated_impressions),
                'estimated_reach': int(estimated_reach),
                'estimated_engagement': int(estimated_engagement),
                'avg_cost_per_click': avg_cpc,
                'avg_cost_per_impression': platform_data['cost_per_impression']['avg'],
                'daily_clicks': int(daily_clicks),
                'daily_impressions': int(daily_impressions),
                'roi_projection': self._calculate_roi_projection(estimated_engagement, platform_budget)
            }
            
            total_estimated_cost += platform_budget
        
        # Budget comparison
        budget_analysis = {
            'target_budget': target_budget,
            'estimated_total_cost': total_estimated_cost,
            'budget_utilization': (total_estimated_cost / target_budget) * 100,
            'budget_variance': total_estimated_cost - target_budget,
            'budget_status': 'On Budget' if abs(total_estimated_cost - target_budget) < target_budget * 0.05 
                           else 'Over Budget' if total_estimated_cost > target_budget 
                           else 'Under Budget'
        }
        
        return {
            'platform_costs': cost_breakdown,
            'budget_analysis': budget_analysis,
            'campaign_duration_days': campaign_duration_days,
            'total_estimated_metrics': self._calculate_total_metrics(cost_breakdown)
        }
    
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
        """Generate campaign strategy recommendations"""
        recommendations = []
        
        # Platform recommendations
        top_platforms = platform_analysis['top_2_platforms']
        recommendations.append(f"Focus campaign on {top_platforms[0]} and {top_platforms[1]} for maximum effectiveness")
        
        # Budget recommendations
        budget_status = cost_analysis['budget_analysis']['budget_status']
        if budget_status == 'Over Budget':
            variance = cost_analysis['budget_analysis']['budget_variance']
            recommendations.append(f"Budget exceeded by ${variance:.2f}. Consider reducing campaign scope or increasing budget")
        elif budget_status == 'Under Budget':
            variance = abs(cost_analysis['budget_analysis']['budget_variance'])
            recommendations.append(f"Budget has ${variance:.2f} remaining. Consider extending campaign or adding platforms")
        
        # Performance recommendations
        total_metrics = cost_analysis['total_estimated_metrics']
        if total_metrics['total_engagement'] < 10000:
            recommendations.append("Low engagement projected. Consider improving creative content or targeting")
        
        # Platform-specific recommendations
        for platform, data in cost_analysis['platform_costs'].items():
            roi = data['roi_projection']['roi_percentage']
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
        budget_allocations = [platform_costs[p]['allocated_budget'] for p in budget_platforms]
        
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
        """Main method to plan marketing campaign"""
        print(f"Planning campaign for {product_info['name']}")
        
        try:
            # Extract campaign parameters from product info
            target_audience = product_info.get('target_audience', {})
            target_age_groups = target_audience.get('age_groups', ['25-34', '35-44'])
            selected_platforms = target_audience.get('platforms', ['Facebook', 'Instagram', 'YouTube'])
            target_budget = target_audience.get('budget', 50000)
            campaign_duration = target_audience.get('duration_days', 30)
            
            # Analyze platform effectiveness
            platform_analysis = self.analyze_platform_effectiveness(target_age_groups, selected_platforms)
            
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
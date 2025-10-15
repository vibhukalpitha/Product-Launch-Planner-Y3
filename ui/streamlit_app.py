"""
Main Streamlit UI for Samsung Product Launch Planner
Integrates all 4 agents with interactive visualizations
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import sys
import os

# Add agents to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))

# Import agents
try:
    from communication_coordinator import coordinator, ProductInfo
    from market_trend_analyzer import MarketTrendAnalyzer
    from competitor_tracking_agent import CompetitorTrackingAgent
    from customer_segmentation_agent import CustomerSegmentationAgent
    from campaign_planning_agent import CampaignPlanningAgent
except ImportError as e:
    st.error(f"Error importing agents: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Samsung Product Launch Planner",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .agent-header {
        font-size: 2rem;
        color: #2e86ab;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .recommendation-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-left: 4px solid #2e86ab;
        margin: 1rem 0;
    }
    .sidebar .sidebar-content {
        background-color: #1f4e79;
    }
</style>
""", unsafe_allow_html=True)

def initialize_agents():
    """Initialize all agents with the coordinator"""
    if 'agents_initialized' not in st.session_state:
        try:
            # Initialize agents
            market_analyzer = MarketTrendAnalyzer(coordinator)
            competitor_tracker = CompetitorTrackingAgent(coordinator)
            customer_segmenter = CustomerSegmentationAgent(coordinator)
            campaign_planner = CampaignPlanningAgent(coordinator)
            
            st.session_state.agents_initialized = True
            st.session_state.coordinator = coordinator
            return True
        except Exception as e:
            st.error(f"Error initializing agents: {e}")
            return False
    return True

def display_main_header():
    """Display main application header"""
    st.markdown('<h1 class="main-header">📱 Samsung Product Launch Planner</h1>', unsafe_allow_html=True)
    st.markdown("---")
    # Temporary debug: show shared coordinator data when requested
    if 'coordinator' in st.session_state:
        if st.checkbox('Show debug: coordinator shared data'):
            try:
                shared = st.session_state.coordinator.get_shared_data()
                st.json(shared)
            except Exception as e:
                st.write('Error reading shared data:', e)
    st.markdown("""
    **Intelligent Product Launch Planning System**
    
    This system uses 4 specialized AI agents to help Samsung plan successful product launches:
    - 🔍 **Market Trend Analyzer**: Analyzes market trends and forecasts sales
    - 🏢 **Competitor Tracker**: Monitors competitors and pricing strategies  
    - 👥 **Customer Segmentation**: Identifies and analyzes customer segments
    - 📢 **Campaign Planner**: Designs optimal marketing campaigns
    """)

def create_product_input_form():
    """Create the main product input form"""
    st.markdown('<h2 class="agent-header">📝 Product Information</h2>', unsafe_allow_html=True)
    
    with st.form("product_info_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            product_name = st.text_input("Product Name", value="Galaxy S25 Ultra", help="Enter the name of your Samsung product")
            product_category = st.selectbox(
                "Product Category",
                ["Smartphones", "Tablets", "Laptops", "Wearables", "TV", "Appliances"],
                help="Select the product category"
            )
            product_price = st.number_input(
                "Product Price ($)",
                min_value=100.0,
                max_value=5000.0,
                value=1200.0,
                step=50.0,
                help="Enter the expected price of the product"
            )
        
        with col2:
            product_description = st.text_area(
                "Product Description",
                value="Premium flagship smartphone with advanced AI features and professional camera system",
                help="Describe your product's key features and positioning"
            )
            launch_date = st.date_input(
                "Expected Launch Date",
                value=datetime.now().date() + timedelta(days=90),
                help="When do you plan to launch this product?"
            )
        
        # Target Audience Section
        st.markdown("### 🎯 Target Audience & Campaign Settings")
        
        col3, col4 = st.columns(2)
        
        with col3:
            age_groups = st.multiselect(
                "Target Age Groups",
                ["18-24", "25-34", "35-44", "45-54", "55+"],
                default=["25-34", "35-44"],
                help="Select the age groups you want to target"
            )
            
            campaign_budget = st.number_input(
                "Campaign Budget ($)",
                min_value=1000.0,
                max_value=1000000.0,
                value=50000.0,
                step=5000.0,
                help="Enter your marketing campaign budget"
            )
        
        with col4:
            social_platforms = st.multiselect(
                "Preferred Social Media Platforms",
                ["Facebook", "Instagram", "TikTok", "YouTube", "Twitter", "LinkedIn", "Snapchat"],
                default=["Facebook", "Instagram", "YouTube"],
                help="Select platforms where you want to run ads"
            )
            
            campaign_duration = st.number_input(
                "Campaign Duration (days)",
                min_value=7,
                max_value=365,
                value=30,
                step=7,
                help="How long should the campaign run?"
            )
        
        # Submit button
        submitted = st.form_submit_button("🚀 Analyze Product Launch", use_container_width=True)
        
        if submitted:
            # Validate inputs
            if not product_name or not age_groups or not social_platforms:
                st.error("Please fill in all required fields")
                return None
            
            # Create product info object
            product_info = ProductInfo(
                name=product_name,
                category=product_category,
                price=product_price,
                description=product_description,
                target_audience={
                    'age_groups': age_groups,
                    'platforms': social_platforms,
                    'budget': campaign_budget,
                    'duration_days': campaign_duration
                },
                launch_date=launch_date.isoformat()
            )
            
            return product_info
    
    return None

def display_market_analysis(analysis_results):
    """Display market trend analysis results"""
    if 'market_analysis' not in analysis_results:
        return
    
    market_data = analysis_results['market_analysis']
    
    st.markdown('<h2 class="agent-header">📈 Market Trend Analysis</h2>', unsafe_allow_html=True)
    
    if 'error' in market_data:
        st.error(f"Market analysis failed: {market_data['error']}")
        return
    
    # 🆕 SAMSUNG SIMILAR PRODUCTS SECTION (FIRST!)
    samsung_products = market_data.get('samsung_similar_products', {})
    
    if samsung_products and samsung_products.get('found_products'):
        st.markdown("---")
        st.markdown('<h3 style="color: #1f77b4;">📱 Samsung\'s Past Similar Products</h3>', unsafe_allow_html=True)
        
        # Discovery summary
        col1, col2, col3 = st.columns(3)
        
        found_products = samsung_products['found_products']
        data_sources = samsung_products.get('data_sources', [])
        
        with col1:
            st.metric(
                "Similar Products Found", 
                len(found_products),
                delta=f"Using {samsung_products.get('discovery_method', 'Unknown')} method"
            )
        
        with col2:
            price_comparison = samsung_products.get('price_comparison', {})
            if price_comparison:
                position = price_comparison.get('price_position', 'Unknown')
                percentile = price_comparison.get('price_percentile', 50)
                st.metric(
                    "Price Position",
                    position,
                    delta=f"{percentile:.1f}th percentile vs Samsung"
                )
        
        with col3:
            evolution = samsung_products.get('category_evolution', {})
            if evolution:
                st.metric(
                    "Innovation Pace",
                    evolution.get('innovation_pace', 'Unknown'),
                    delta=f"{evolution.get('total_products_analyzed', 0)} products analyzed"
                )
        
        # Samsung Products Table
        st.subheader("🏆 Top Samsung Similar Products")
        
        # Create a detailed table
        product_data = []
        for i, product in enumerate(found_products[:8], 1):  # Top 8 products
            product_data.append({
                "Rank": i,
                "Product Name": product['name'],
                "Price": f"${product['estimated_price']:,}",
                "Launch Year": product['launch_year'],
                "Similarity": f"{product['similarity_score']:.2f}",
                "Tier": product.get('tier', 'N/A'),
                "Source": product['source']
            })
        
        df = pd.DataFrame(product_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Product Timeline Visualization
        if samsung_products.get('product_timeline'):
            st.subheader("📅 Samsung Product Timeline")
            
            timeline_data = samsung_products['product_timeline']
            
            fig_timeline = go.Figure()
            
            # Create timeline scatter plot
            x_years = [p['year'] for p in timeline_data]
            y_prices = [p['price'] for p in timeline_data]
            names = [p['name'] for p in timeline_data]
            similarities = [p['similarity'] for p in timeline_data]
            
            fig_timeline.add_trace(go.Scatter(
                x=x_years,
                y=y_prices,
                mode='markers+text',
                marker=dict(
                    size=[s*20 for s in similarities],  # Size based on similarity
                    color=similarities,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Similarity Score")
                ),
                text=names,
                textposition="top center",
                name="Samsung Products",
                hovertemplate="<b>%{text}</b><br>Year: %{x}<br>Price: $%{y:,}<br>Similarity: %{marker.color:.2f}<extra></extra>"
            ))
            
            fig_timeline.update_layout(
                title="Samsung Product Launch Timeline",
                xaxis_title="Launch Year",
                yaxis_title="Price ($)",
                height=500,
                showlegend=False
            )
            
            st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Price Comparison Chart
        if price_comparison and 'comparison_products' in price_comparison:
            st.subheader("💰 Price Comparison with Samsung Portfolio")
            
            comparison_products = price_comparison['comparison_products']
            target_price = price_comparison['target_price']
            
            fig_price = go.Figure()
            
            # Samsung products bars
            product_names = [p['name'] for p in comparison_products]
            product_prices = [p['price'] for p in comparison_products]
            price_diffs = [p['price_diff'] for p in comparison_products]
            
            # Color based on price difference
            colors = ['red' if diff > 0 else 'green' if diff < 0 else 'blue' for diff in price_diffs]
            
            fig_price.add_trace(go.Bar(
                x=product_names,
                y=product_prices,
                name="Samsung Products",
                marker_color=colors,
                text=[f"${price:,}" for price in product_prices],
                textposition='auto',
                hovertemplate="<b>%{x}</b><br>Price: $%{y:,}<br>Difference: %{customdata}%<extra></extra>",
                customdata=price_diffs
            ))
            
            # Add target price line
            fig_price.add_hline(
                y=target_price, 
                line_dash="dash", 
                line_color="orange",
                annotation_text=f"Your Product: ${target_price:,}"
            )
            
            fig_price.update_layout(
                title="Price Comparison: Your Product vs Samsung Similar Products",
                xaxis_title="Samsung Products",
                yaxis_title="Price ($)",
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig_price, use_container_width=True)
        
        # Insights and Recommendations
        st.subheader("💡 Samsung Portfolio Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Discovery Summary:**")
            st.write(f"• **Data Sources:** {', '.join(data_sources)}")
            st.write(f"• **Products Found:** {len(found_products)}")
            
            if price_comparison:
                avg_samsung_price = price_comparison.get('similar_products_avg', 0)
                st.write(f"• **Samsung Avg Price:** ${avg_samsung_price:,.2f}")
                st.write(f"• **Your Position:** {price_comparison.get('price_position', 'Unknown')}")
        
        with col2:
            st.markdown("**📈 Category Evolution:**")
            if evolution:
                st.write(f"• **Analysis Period:** {evolution.get('analysis_period', 'N/A')}")
                st.write(f"• **Innovation Pace:** {evolution.get('innovation_pace', 'Unknown')}")
                
                if evolution.get('most_recent_year'):
                    current_year = 2025
                    years_since = current_year - evolution['most_recent_year']
                    st.write(f"• **Latest Launch:** {years_since} year(s) ago")
        
        st.markdown("---")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    trends = market_data.get('market_trends', {})
    forecast = market_data.get('sales_forecast', {})
    
    with col1:
        st.metric(
            "Market Growth Rate",
            f"{trends.get('growth_rate', 0) * 100:.1f}%",
            delta=f"+{trends.get('growth_rate', 0) * 100:.1f}% vs last year"
        )
    
    with col2:
        st.metric(
            "Average Market Price",
            f"${trends.get('average_price', 0):,.2f}",
            delta=f"${market_data.get('analyzed_price', 0) - trends.get('average_price', 0):+,.2f} vs our price"
        )
    
    with col3:
        if forecast.get('forecast_sales'):
            avg_forecast = np.mean(forecast['forecast_sales'])
            st.metric(
                "Avg Monthly Forecast",
                f"{avg_forecast:,.0f} units",
                delta=f"{forecast.get('growth_rate', 0) * 100:.1f}% growth"
            )
    
    with col4:
        st.metric(
            "Market Saturation",
            f"{trends.get('market_saturation', 0) * 100:.1f}%",
            delta="Market maturity level"
        )
    
    # Visualizations
    viz_data = market_data.get('visualizations', {})
    
    # Historical and forecast sales chart
    if 'historical_sales' in viz_data and 'sales_forecast' in viz_data:
        fig = go.Figure()
        
        # Historical data
        hist_data = viz_data['historical_sales']
        fig.add_trace(go.Scatter(
            x=hist_data['dates'],
            y=hist_data['sales'],
            mode='lines',
            name='Historical Sales',
            line=dict(color='blue', width=2)
        ))
        
        # Forecast data
        forecast_data = viz_data['sales_forecast']
        fig.add_trace(go.Scatter(
            x=forecast_data['dates'],
            y=forecast_data['sales'],
            mode='lines',
            name='Sales Forecast',
            line=dict(color='red', width=2, dash='dash')
        ))
        
        # Confidence interval
        fig.add_trace(go.Scatter(
            x=forecast_data['dates'] + forecast_data['dates'][::-1],
            y=forecast_data['upper_bound'] + forecast_data['lower_bound'][::-1],
            fill='tonexty',
            fillcolor='rgba(255,0,0,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Forecast Range',
            showlegend=False
        ))
        
        fig.update_layout(
            title="Sales History & Forecast",
            xaxis_title="Date",
            yaxis_title="Sales Volume",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # City performance chart
    if 'city_performance' in viz_data:
        city_data = viz_data['city_performance']
        
        fig = px.bar(
            x=city_data['cities'][:10],  # Top 10 cities
            y=city_data['sales'][:10],
            title="Top Performing Cities",
            labels={'x': 'City', 'y': 'Sales Volume'}
        )
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    recommendations = market_data.get('recommendations', [])
    if recommendations:
        st.markdown("### 💡 Market Recommendations")
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f'<div class="recommendation-box">{i}. {rec}</div>', unsafe_allow_html=True)

def display_competitor_analysis(analysis_results):
    """Display enhanced competitor analysis results with intelligent discovery"""
    if 'competitor_analysis' not in analysis_results:
        return
    
    competitor_data = analysis_results['competitor_analysis']
    
    st.markdown('<h2 class="agent-header">🏢 Intelligent Competitor Analysis</h2>', unsafe_allow_html=True)
    
    if 'error' in competitor_data:
        st.error(f"Competitor analysis failed: {competitor_data['error']}")
        return
    
    # Show discovery method and key insights
    discovery_method = competitor_data.get('discovery_method', 'unknown')
    key_insights = competitor_data.get('key_insights', {})
    
    st.markdown(f"""
    <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h3>🤖 Discovery Results</h3>
        <p><strong>Discovery Method:</strong> {discovery_method.title()} Discovery System</p>
        <p><strong>Product:</strong> {competitor_data.get('product_name', 'Unknown')}</p>
        <p><strong>Category:</strong> {competitor_data.get('product_category', 'Unknown')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Competitors Found", 
            key_insights.get('total_competitors_found', 0),
            help="Total competitors discovered across all sources"
        )
    
    with col2:
        st.metric(
            "Direct Threats", 
            key_insights.get('direct_threats', 0),
            help="High-confidence direct competitors"
        )
    
    with col3:
        st.metric(
            "Market Position", 
            key_insights.get('market_position', 'Unknown'),
            help="Your pricing position vs competitors"
        )
    
    with col4:
        market_frag = key_insights.get('market_fragmentation', 'Unknown')
        frag_color = '🔴' if market_frag == 'High' else '🟡' if market_frag == 'Medium' else '🟢'
        st.metric(
            "Market Fragmentation", 
            f"{frag_color} {market_frag}",
            help="Level of competition in the market"
        )
    
    # Competitor Discovery Results
    discovery_data = competitor_data.get('competitor_discovery', {})
    
    if discovery_data:
        st.markdown("### 🔍 Competitor Discovery Results")
        
        # Display discovered competitors in tabs
        tab1, tab2, tab3 = st.tabs(["🎯 Direct Competitors", "🔄 Indirect Competitors", "🌟 Emerging Competitors"])
        
        with tab1:
            direct_competitors = discovery_data.get('direct_competitors', [])
            if direct_competitors:
                st.markdown("**High-confidence direct competitors:**")
                
                for comp in direct_competitors:
                    confidence = discovery_data.get('confidence_scores', {}).get(comp, 0)
                    sources = discovery_data.get('discovery_sources', {}).get(comp, [])
                    
                    col_comp, col_conf, col_sources = st.columns([2, 1, 2])
                    
                    with col_comp:
                        st.markdown(f"**{comp}**")
                    
                    with col_conf:
                        conf_color = '🟢' if confidence >= 2.0 else '🟡' if confidence >= 1.0 else '🔴'
                        st.markdown(f"{conf_color} {confidence:.2f}")
                    
                    with col_sources:
                        st.markdown(f"📊 {len(sources)} sources: {', '.join(sources[:2])}")
                    
                    st.markdown("---")
            else:
                st.info("No direct competitors found")
        
        with tab2:
            indirect_competitors = discovery_data.get('indirect_competitors', [])
            if indirect_competitors:
                st.markdown("**Medium-confidence indirect competitors:**")
                
                for comp in indirect_competitors:
                    confidence = discovery_data.get('confidence_scores', {}).get(comp, 0)
                    sources = discovery_data.get('discovery_sources', {}).get(comp, [])
                    
                    col_comp, col_conf = st.columns([3, 1])
                    
                    with col_comp:
                        st.markdown(f"• **{comp}** (Sources: {', '.join(sources[:2])})")
                    
                    with col_conf:
                        st.markdown(f"📊 {confidence:.2f}")
            else:
                st.info("No indirect competitors found")
        
        with tab3:
            emerging_competitors = discovery_data.get('emerging_competitors', [])
            if emerging_competitors:
                st.markdown("**Emerging or niche competitors:**")
                
                for comp in emerging_competitors:
                    confidence = discovery_data.get('confidence_scores', {}).get(comp, 0)
                    st.markdown(f"• {comp} (Score: {confidence:.2f})")
            else:
                st.info("No emerging competitors found")
    
    # Price comparison metrics
    pricing = competitor_data.get('pricing_analysis', {})
    price_stats = pricing.get('price_statistics', {})
    
    if pricing:
        st.markdown("### 💰 Price Analysis")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Our Price", f"${price_stats.get('our_price', 0):,.2f}")
        
        with col2:
            our_price = price_stats.get('our_price', 0)
            avg_price = price_stats.get('avg_price', 1)
            delta_pct = ((our_price / avg_price) - 1) * 100 if avg_price > 0 else 0
            st.metric(
                "Market Average",
                f"${avg_price:,.2f}",
                delta=f"{delta_pct:+.1f}%"
            )
        
        with col3:
            st.metric("Lowest Competitor", f"${price_stats.get('min_price', 0):,.2f}")
        
        with col4:
            st.metric("Highest Competitor", f"${price_stats.get('max_price', 0):,.2f}")
        
        # Price positioning insights
        position = pricing.get('competitive_position', {})
        st.markdown(f"""
        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 8px; margin: 15px 0;">
            <h4>📈 Price Position Analysis</h4>
            <p><strong>Position:</strong> {position.get('position', 'Unknown')}</p>
            <p><strong>Market Percentile:</strong> {position.get('percentile', 0):.1f}%</p>
            <p><strong>Price Advantage:</strong> {'✅ Yes' if position.get('price_advantage', False) else '❌ No'}</p>
            <p><strong>Strategy:</strong> {position.get('recommended_strategy', 'Not available')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Visualizations
    viz_data = competitor_data.get('visualizations', {})
    
    if viz_data:
        st.markdown("### 📊 Competitive Visualizations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Price comparison chart
            if 'price_comparison' in viz_data:
                price_chart = viz_data['price_comparison']
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=price_chart['competitors'],
                        y=price_chart['prices'],
                        marker_color=price_chart['colors'],
                        text=[f"${p:.0f}" for p in price_chart['prices']],
                        textposition='auto'
                    )
                ])
                
                fig.update_layout(
                    title="💰 Price Comparison with Competitors",
                    xaxis_title="Brand",
                    yaxis_title="Price ($)",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            pass  # Empty column
    
    # Market Insights
    discovery = competitor_data.get('competitor_discovery', {})
    market_insights = discovery.get('market_insights', {})
    
    if market_insights:
        st.markdown("### 🎯 Market Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🏆 Competitive Landscape")
            landscape = market_insights.get('competitive_landscape', {})
            
            premium_brands = landscape.get('premium_brands', [])
            value_brands = landscape.get('value_brands', [])
            innovation_leaders = landscape.get('innovation_leaders', [])
            
            if premium_brands:
                st.markdown(f"**Premium Brands:** {', '.join(premium_brands)}")
            if value_brands:
                st.markdown(f"**Value Brands:** {', '.join(value_brands)}")
            if innovation_leaders:
                st.markdown(f"**Innovation Leaders:** {', '.join(innovation_leaders)}")
        
        with col2:
            st.markdown("#### 📊 Market Analysis")
            market_analysis = market_insights.get('market_analysis', {})
            
            st.markdown(f"**Total Competitors:** {market_analysis.get('total_identified_competitors', 0)}")
            st.markdown(f"**Direct Threats:** {market_analysis.get('direct_threats', 0)}")
            st.markdown(f"**Market Fragmentation:** {market_analysis.get('market_fragmentation', 'Unknown')}")
    
    # Social media feedback
    sentiment_analysis = competitor_data.get('sentiment_analysis', {})
    if sentiment_analysis:
        st.markdown("### 📱 Social Media Insights")
        
        # Select competitor to view feedback
        selected_competitor = st.selectbox(
            "Select Competitor to View Detailed Feedback",
            list(sentiment_analysis.keys())
        )
        
        if selected_competitor:
            comp_data = sentiment_analysis[selected_competitor]
            
            # Try to determine product category for fetching feedback
            product_category = 'smartphones'
            try:
                if 'product_info' in st.session_state and st.session_state.product_info:
                    # ProductInfo dataclass or dict
                    pi = st.session_state.product_info
                    product_category = getattr(pi, 'category', None) or pi.get('category', product_category) if isinstance(pi, dict) or hasattr(pi, '__dict__') else product_category
            except Exception:
                product_category = product_category
            
            # Trending topics - visual divider between competitor selection and feedback
            trending = comp_data.get('trending_topics', [])
            if trending:
                st.markdown("---")
                st.markdown(f"**🔥 Top Trends for {selected_competitor}:** {', '.join(trending)}")
            
            # Attempt to fetch fresh recent feedback for the selected competitor (cached per competitor)
            feedback_cache_key = f"feedback_{selected_competitor}"
            feedback = None
            if feedback_cache_key in st.session_state:
                feedback = st.session_state[feedback_cache_key]
            else:
                try:
                    coord = st.session_state.get('coordinator')
                    if coord:
                        fetched = coord.send_message('ui', 'competitor_tracker', 'fetch_feedback', {
                            'competitor': selected_competitor,
                            'category': product_category,
                            'limit': 5
                        })
                        # Some send_message flows return the list directly
                        if isinstance(fetched, list):
                            feedback = fetched
                        elif isinstance(fetched, dict) and 'sample_feedback' in fetched:
                            feedback = fetched.get('sample_feedback', [])
                        else:
                            feedback = comp_data.get('sample_feedback', [])
                    else:
                        feedback = comp_data.get('sample_feedback', [])
                except Exception as e:
                    feedback = comp_data.get('sample_feedback', [])
                # Cache result
                st.session_state[feedback_cache_key] = feedback or []
            
            # Sample feedback
            st.markdown("#### 💬 Recent Feedback")
            for fb in (feedback or [])[:5]:  # Show up to 5
                sentiment_color = {
                    'positive': '🟢',
                    'negative': '🔴',
                    'neutral': '🟡'
                }.get(fb.get('sentiment', 'neutral'), '⚪')
                platform = fb.get('platform', 'Unknown')
                engagement = fb.get('engagement', 0)
                comment = fb.get('comment', '')
                st.markdown(f"{sentiment_color} **{platform}** ({engagement} engagements)\n\n\"{comment}\"")

            # New Advice section based on feedback
            st.markdown("#### 📝 Advice to Improve Our Product")
            advice_key = f"advice_{selected_competitor}"
            # Use cached advice when available to avoid recomputing
            advice = st.session_state.get(advice_key, "- No feedback available to analyze.")
            try:
                coord = st.session_state.get('coordinator')
                if coord and feedback:
                    # Ask backend agent to analyze feedback
                    advice_result = coord.send_message('ui', 'competitor_tracker', 'analyze_feedback_and_advise', {
                        'feedback_list': feedback
                    })
                    if advice_result:
                        advice = advice_result
                elif feedback:
                    # Fallback: local quick analysis so UI updates even without coordinator
                    positives = [fb['comment'] for fb in feedback if fb.get('sentiment') == 'positive']
                    negatives = [fb['comment'] for fb in feedback if fb.get('sentiment') == 'negative']
                    parts = []
                    if negatives:
                        parts.append("Address these common complaints: " + "; ".join(negatives[:2]))
                    if positives:
                        parts.append("Leverage these strengths: " + "; ".join(positives[:2]))
                    if not parts:
                        parts.append("Monitor feedback for actionable insights.")
                    advice = "\n".join(parts)
                else:
                    advice = "- No feedback available to analyze."
            except Exception as e:
                advice = f"- Unable to analyze feedback: {e}"

            # Cache and display
            st.session_state[advice_key] = advice
            st.markdown(advice)
    
    # Recommendations


def display_customer_segmentation(analysis_results):
    """Display customer segmentation results"""
    if 'customer_segments' not in analysis_results:
        return
    
    customer_data = analysis_results['customer_segments']
    
    st.markdown('<h2 class="agent-header">👥 Customer Segmentation</h2>', unsafe_allow_html=True)
    
    if 'error' in customer_data:
        st.error(f"Customer segmentation failed: {customer_data['error']}")
        return
    
    segments = customer_data.get('customer_segments', {})
    
    # Segment overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    segment_names = list(segments.keys())
    
    for i, (col, segment_name) in enumerate(zip([col1, col2, col3, col4], segment_names)):
        if i < len(segment_names):
            segment = segments[segment_name]
            with col:
                st.metric(
                    segment_name,
                    f"{segment['percentage']:.1f}%",
                    delta=f"Score: {segment['attractiveness_score']:.2f}"
                )
    
    # Visualizations
    viz_data = customer_data.get('visualizations', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Segment sizes pie chart
        if 'segment_sizes' in viz_data:
            size_data = viz_data['segment_sizes']
            
            fig = px.pie(
                values=size_data['sizes'],
                names=size_data['segments'],
                title="Customer Segment Distribution"
            )
            fig.update_layout(height=400)
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Attractiveness scores
        if 'attractiveness_scores' in viz_data:
            attr_data = viz_data['attractiveness_scores']
            
            fig = go.Figure(data=[
                go.Bar(
                    x=attr_data['segments'],
                    y=attr_data['scores'],
                    marker_color='lightgreen',
                    text=[f"{s:.2f}" for s in attr_data['scores']],
                    textposition='auto'
                )
            ])
            
            fig.update_layout(
                title="Segment Attractiveness Scores",
                xaxis_title="Customer Segment",
                yaxis_title="Attractiveness Score",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Segment characteristics radar chart
    if 'segment_characteristics' in viz_data:
        chars_data = viz_data['segment_characteristics']
        
        fig = go.Figure()
        
        categories = list(next(iter(chars_data.values())).keys())
        
        for segment_name, characteristics in chars_data.items():
            values = list(characteristics.values())
            values.append(values[0])  # Close the radar chart
            categories_closed = categories + [categories[0]]
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories_closed,
                fill='toself',
                name=segment_name
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title="Segment Characteristics Comparison",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed segment analysis
    st.markdown("### 📊 Detailed Segment Analysis")
    
    selected_segment = st.selectbox(
        "Select Segment for Detailed View",
        segment_names
    )
    
    if selected_segment:
        segment = segments[selected_segment]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Characteristics")
            chars = segment['characteristics']
            st.markdown(f"""
            - **Average Age**: {chars['avg_age']:.1f} years
            - **Average Income**: ${chars['avg_income']:,.0f}
            - **Tech Adoption**: {chars['tech_adoption']:.2f}
            - **Price Sensitivity**: {chars['price_sensitivity']:.2f}
            - **Brand Loyalty**: {chars['brand_loyalty']:.2f}
            """)
        
        with col2:
            st.markdown("#### Preferences & Strategy")
            prefs = segment['preferences']
            st.markdown(f"""
            - **Price Preference**: {prefs['price_preference']}
            - **Top Features**: {', '.join(prefs['feature_priorities'][:3])}
            - **Marketing Channels**: {', '.join(prefs['marketing_channels'][:2])}
            - **Strategy**: {segment['recommended_strategy']}
            """)
    
    # Recommendations
    recommendations = customer_data.get('recommendations', [])
    if recommendations:
        st.markdown("### 💡 Segmentation Recommendations")
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f'<div class="recommendation-box">{i}. {rec}</div>', unsafe_allow_html=True)

def display_campaign_planning(analysis_results):
    """Display campaign planning results"""
    if 'campaign_plan' not in analysis_results:
        return
    
    campaign_data = analysis_results['campaign_plan']
    
    st.markdown('<h2 class="agent-header">📢 Campaign Planning</h2>', unsafe_allow_html=True)
    
    if 'error' in campaign_data:
        st.error(f"Campaign planning failed: {campaign_data['error']}")
        return
    
    # Platform effectiveness overview
    platform_analysis = campaign_data.get('platform_analysis', {})
    top_platforms = platform_analysis.get('top_2_platforms', [])
    
    st.markdown("### 🎯 Recommended Platforms")
    
    if len(top_platforms) >= 2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            #### 🥇 Primary Platform: {top_platforms[0]}
            Best platform for your target audience
            """)
        
        with col2:
            st.markdown(f"""
            #### 🥈 Secondary Platform: {top_platforms[1]}
            Complementary platform for broader reach
            """)
    
    # Budget analysis
    cost_analysis = campaign_data.get('cost_analysis', {})
    budget_analysis = cost_analysis.get('budget_analysis', {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Target Budget",
            f"${budget_analysis.get('target_budget', 0):,.2f}"
        )
    
    with col2:
        st.metric(
            "Estimated Cost",
            f"${budget_analysis.get('estimated_total_cost', 0):,.2f}",
            delta=f"${budget_analysis.get('budget_variance', 0):+,.2f}"
        )
    
    with col3:
        st.metric(
            "Budget Status",
            budget_analysis.get('budget_status', 'Unknown')
        )
    
    with col4:
        st.metric(
            "Utilization",
            f"{budget_analysis.get('budget_utilization', 0):.1f}%"
        )
    
    # Campaign metrics
    total_metrics = cost_analysis.get('total_estimated_metrics', {})
    
    st.markdown("### 📊 Projected Campaign Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Reach",
            f"{total_metrics.get('total_reach', 0):,}"
        )
    
    with col2:
        st.metric(
            "Total Clicks",
            f"{total_metrics.get('total_clicks', 0):,}"
        )
    
    with col3:
        st.metric(
            "Total Engagement",
            f"{total_metrics.get('total_engagement', 0):,}"
        )
    
    with col4:
        st.metric(
            "Estimated Revenue",
            f"${total_metrics.get('total_estimated_revenue', 0):,.2f}"
        )
    
    # Visualizations
    viz_data = campaign_data.get('visualizations', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Platform effectiveness chart
        if 'platform_effectiveness' in viz_data:
            eff_data = viz_data['platform_effectiveness']
            
            fig = go.Figure(data=[
                go.Bar(
                    x=eff_data['platforms'],
                    y=eff_data['scores'],
                    marker_color='lightcoral',
                    text=[f"{s:.2f}" for s in eff_data['scores']],
                    textposition='auto'
                )
            ])
            
            fig.update_layout(
                title="Platform Effectiveness Scores",
                xaxis_title="Platform",
                yaxis_title="Effectiveness Score",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Budget allocation chart
        if 'budget_allocation' in viz_data:
            budget_data = viz_data['budget_allocation']
            
            fig = px.pie(
                values=budget_data['budgets'],
                names=budget_data['platforms'],
                title="Budget Allocation by Platform"
            )
            fig.update_layout(height=400)
            
            st.plotly_chart(fig, use_container_width=True)
    
    # ROI projection
    if 'roi_projection' in viz_data:
        roi_data = viz_data['roi_projection']
        
        fig = go.Figure(data=[
            go.Bar(
                x=roi_data['platforms'],
                y=roi_data['roi_values'],
                marker_color='gold',
                text=[f"{r:.1f}%" for r in roi_data['roi_values']],
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title="ROI Projection by Platform",
            xaxis_title="Platform",
            yaxis_title="ROI (%)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed platform costs
    platform_costs = cost_analysis.get('platform_costs', {})
    
    if platform_costs:
        st.markdown("### 💰 Detailed Cost Breakdown")
        
        selected_platform = st.selectbox(
            "Select Platform for Detailed Costs",
            list(platform_costs.keys())
        )
        
        if selected_platform:
            platform_data = platform_costs[selected_platform]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### Budget & Spend")
                st.markdown(f"""
                - **Allocated Budget**: ${platform_data['allocated_budget']:,.2f}
                - **Daily Budget**: ${platform_data['daily_budget']:,.2f}
                - **Avg CPC**: ${platform_data['avg_cost_per_click']:.2f}
                """)
            
            with col2:
                st.markdown("#### Performance Metrics")
                st.markdown(f"""
                - **Estimated Clicks**: {platform_data['estimated_clicks']:,}
                - **Estimated Reach**: {platform_data['estimated_reach']:,}
                - **Daily Clicks**: {platform_data['daily_clicks']:,}
                """)
            
            with col3:
                st.markdown("#### ROI Projection")
                roi_proj = platform_data['roi_projection']
                st.markdown(f"""
                - **ROI**: {roi_proj['roi_percentage']:.1f}%
                - **Est. Conversions**: {roi_proj['estimated_conversions']:.1f}
                - **Est. Revenue**: ${roi_proj['estimated_revenue']:,.2f}
                """)
    
    # Campaign timeline
    timeline = campaign_data.get('campaign_timeline', {})
    if timeline:
        st.markdown("### 📅 Campaign Timeline")
        
        phases = timeline.get('phases', [])
        for phase in phases:
            st.markdown(f"""
            **{phase['phase']}** ({phase['duration']})
            - {', '.join(phase['activities'])}
            """)
    
    # Recommendations
    recommendations = campaign_data.get('recommendations', [])
    if recommendations:
        st.markdown("### 💡 Campaign Recommendations")
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f'<div class="recommendation-box">{i}. {rec}</div>', unsafe_allow_html=True)

def main():
    """Main application function"""
    # Initialize agents
    if not initialize_agents():
        st.error("Failed to initialize agents. Please refresh the page.")
        return
    
    # Display header
    display_main_header()
    
    # Sidebar navigation
    st.sidebar.title("🔧 Navigation")
    page = st.sidebar.selectbox(
        "Select Analysis Section",
        ["Product Input", "Market Analysis", "Competitor Analysis", "Customer Segmentation", "Campaign Planning", "Complete Analysis"]
    )
    
    # Product input form
    if page == "Product Input" or 'analysis_results' not in st.session_state:
        product_info = create_product_input_form()
        
        if product_info:
            # Run complete analysis
            with st.spinner("🔄 Running comprehensive analysis..."):
                try:
                    coordinator = st.session_state.coordinator
                    results = coordinator.orchestrate_analysis(product_info)
                    
                    st.session_state.analysis_results = results
                    st.session_state.product_info = product_info
                    
                    st.success("✅ Analysis completed successfully!")
                    st.markdown("Navigate to other sections using the sidebar to view detailed results.")
                    
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
    
    # Display analysis results based on selected page
    if 'analysis_results' in st.session_state:
        results = st.session_state.analysis_results
        
        if page == "Market Analysis":
            display_market_analysis(results)
        elif page == "Competitor Analysis":
            display_competitor_analysis(results)
        elif page == "Customer Segmentation":
            display_customer_segmentation(results)
        elif page == "Campaign Planning":
            display_campaign_planning(results)
        elif page == "Complete Analysis":
            display_market_analysis(results)
            display_competitor_analysis(results)
            display_customer_segmentation(results)
            display_campaign_planning(results)
    else:
        if page != "Product Input":
            st.info("👈 Please complete the product input first to see analysis results.")

    # Sidebar additional info
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### 📚 System Features
    - **Real-time Analysis**: Live market data integration
    - **AI-Powered Insights**: Machine learning recommendations
    - **Interactive Visualizations**: Dynamic charts and graphs
    - **Comprehensive Planning**: End-to-end launch strategy
    
    ### 🆓 Free APIs Used
    - Market data APIs
    - Social media analytics
    - Competitor intelligence
    - Campaign cost estimation
    """)

if __name__ == "__main__":
    main()
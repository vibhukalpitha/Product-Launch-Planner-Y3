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

# Import pricing page
try:
    from pricing_page import display_pricing_comparison, show_upgrade_modal
except ImportError:
    st.warning("Pricing page not available")
    display_pricing_comparison = None
    show_upgrade_modal = None

# Import Samsung theme
try:
    from samsung_theme import get_samsung_css, get_samsung_plotly_theme, get_samsung_chart_colors, SAMSUNG_COLORS
    SAMSUNG_THEME_AVAILABLE = True
except ImportError:
    st.warning("Samsung theme not available")
    SAMSUNG_THEME_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Samsung Product Launch Planner | Innovation Lab",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Samsung Theme
if SAMSUNG_THEME_AVAILABLE:
    st.markdown(get_samsung_css(), unsafe_allow_html=True)

# Samsung Brand Header
st.markdown("""
<div style="text-align: center; padding: 2rem 0 1rem 0;">
    <h1 style="font-size: 3.5rem; margin-bottom: 0.5rem;">
        📱 SAMSUNG Product Launch Planner
    </h1>
    <p style="font-size: 1.2rem; color: #5A5A5A; margin-top: 0;">
        <b>Innovation Lab</b> | Powered by AI & Real-Time Market Intelligence
    </p>
    <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 1rem;">
        <span class="samsung-badge">🚀 Real API Data</span>
        <span class="samsung-badge">🤖 AI-Powered</span>
        <span class="samsung-badge">📊 Live Analytics</span>
        <span class="samsung-badge">🌍 Global Markets</span>
    </div>
</div>
<hr>
""", unsafe_allow_html=True)

# Legacy CSS (keeping for compatibility)
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

def display_api_status_page():
    """Display comprehensive API status page"""
    from datetime import datetime
    from utils.api_key_rotator import api_key_rotator
    
    st.markdown('<h1 style="color: #1428A0; font-size: 2.5rem;">🔌 API Status Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("**Real-time status of all APIs used across the system**")
    st.markdown("---")
    
    # Get current API status
    current_time = datetime.now()
    
    # API Configuration Overview
    st.markdown("## 📊 API Configuration Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        youtube_keys = api_key_rotator.get_key_count('youtube')
        st.metric("YouTube API", f"{youtube_keys} Keys", "10K req/day each")
    with col2:
        news_keys = api_key_rotator.get_key_count('news_api')
        st.metric("News API", f"{news_keys} Keys", "100 req/day each")
    with col3:
        serp_keys = api_key_rotator.get_key_count('serpapi')
        st.metric("SerpAPI", f"{serp_keys} Keys", "100 req/month each")
    with col4:
        st.metric("Free APIs", "2 APIs", "Unlimited")
    
    st.markdown("---")
    
    # Detailed API Status by Agent
    st.markdown("## 🤖 API Usage by Agent")
    
    # Market Trend Analyzer
    with st.expander("📊 **Market Trend Analyzer** - APIs Used", expanded=True):
        st.markdown("### YouTube Data API v3 🎥")
        
        if youtube_keys > 0:
            youtube_status = api_key_rotator.get_status('youtube')
            st.markdown(f"**Total Keys**: {youtube_keys}")
            available_count = youtube_status['available_keys']
            
            for key_info in youtube_status['keys']:
                key_id = key_info['index']
                key_last4 = key_info['key_preview']
                is_available = key_info['is_available']
                
                if is_available:
                    st.success(f"✅ Key #{key_id} ({key_last4}): Available")
                else:
                    # Calculate recovery time
                    if 'rate_limited_for' in key_info:
                        time_str = key_info['rate_limited_for']
                        st.error(f"❌ Key #{key_id} ({key_last4}): Rate Limited - Recovers in **{time_str}**")
                    else:
                        st.warning(f"⚠️ Key #{key_id} ({key_last4}): Unavailable")
            
            st.info(f"**Status**: {available_count}/{youtube_keys} keys ready")
        else:
            st.error("❌ No YouTube API keys configured")
        
        st.markdown("**Rate Limit**: 10,000 requests/day per key")
        st.markdown("**Used For**: Similar product discovery, video engagement, customer reach")
        
        st.markdown("---")
        
        st.markdown("### News API 📰")
        
        if news_keys > 0:
            news_status = api_key_rotator.get_status('news_api')
            st.markdown(f"**Total Keys**: {news_keys}")
            available_count = news_status['available_keys']
            
            for key_info in news_status['keys']:
                key_id = key_info['index']
                key_last4 = key_info['key_preview']
                is_available = key_info['is_available']
                
                if is_available:
                    st.success(f"✅ Key #{key_id} ({key_last4}): Available")
                else:
                    # Calculate recovery time
                    if 'rate_limited_for' in key_info:
                        time_str = key_info['rate_limited_for']
                        st.error(f"❌ Key #{key_id} ({key_last4}): Rate Limited - Recovers in **{time_str}**")
                    else:
                        st.warning(f"⚠️ Key #{key_id} ({key_last4}): Unavailable")
            
            st.info(f"**Status**: {available_count}/{news_keys} keys ready")
        else:
            st.error("❌ No News API keys configured")
        
        st.markdown("**Rate Limit**: 100 requests/day per key (free tier)")
        st.markdown("**Used For**: Product discovery, market coverage, historical sales")
        
        st.markdown("---")
        
        st.markdown("### Wikipedia Pageviews API 📚")
        st.success("✅ **Status**: Active (Free, Unlimited)")
        st.markdown("**Used For**: Regional interest, city performance data")
        
        st.markdown("---")
        
        st.markdown("### Google Trends 📈")
        st.warning("⚠️ **Status**: Limited Use (Very Strict Limits)")
        st.markdown("**Used For**: Market trend data (minimal usage due to rate limits)")
    
    # Competitor Tracking Agent
    with st.expander("🏆 **Competitor Tracking Agent** - APIs Used"):
        st.markdown("### News API 📰")
        st.markdown("**Used For**: Competitor discovery from news mentions")
        if news_keys > 0:
            news_status = api_key_rotator.get_status('news_api')
            st.markdown(f"**Status**: {news_status['available_keys']}/{news_keys} keys available")
        else:
            st.markdown("**Status**: No keys configured")
        
        st.markdown("---")
        
        st.markdown("### YouTube Data API v3 🎥")
        st.markdown("**Used For**: Competitor discovery from comparison videos")
        if youtube_keys > 0:
            youtube_status = api_key_rotator.get_status('youtube')
            st.markdown(f"**Status**: {youtube_status['available_keys']}/{youtube_keys} keys available")
        else:
            st.markdown("**Status**: No keys configured")
        
        st.markdown("---")
        
        st.markdown("### SerpAPI 🔍")
        if serp_keys > 0:
            st.info(f"ℹ️ {serp_keys} keys configured (currently not enabled)")
        else:
            st.warning("⚠️ Not configured")
        st.markdown("**Rate Limit**: 100 searches/month per key")
        st.markdown("**Used For**: E-commerce competitor data (optional)")
    
    # Customer Segmentation Agent
    with st.expander("👥 **Customer Segmentation Agent** - APIs Used"):
        st.markdown("### YouTube Data API v3 🎥")
        st.markdown("**Used For**: Customer engagement metrics (video views)")
        if youtube_keys > 0:
            youtube_status = api_key_rotator.get_status('youtube')
            st.markdown(f"**Status**: {youtube_status['available_keys']}/{youtube_keys} keys available")
        else:
            st.markdown("**Status**: No keys configured")
        
        st.markdown("---")
        
        st.markdown("### News API 📰")
        st.markdown("**Used For**: Market awareness metrics (article counts)")
        if news_keys > 0:
            news_status = api_key_rotator.get_status('news_api')
            st.markdown(f"**Status**: {news_status['available_keys']}/{news_keys} keys available")
        else:
            st.markdown("**Status**: No keys configured")
        
        st.markdown("---")
        
        st.markdown("### Reddit Public JSON API 🔴")
        st.success("✅ **Status**: Active (Free, No Auth Required)")
        st.markdown("**Rate Limit**: 60 requests/min")
        st.markdown("**Used For**: Community engagement, feature preferences, price sentiment")
        
        st.markdown("---")
        
        st.markdown("### Wikipedia Pageviews API 📚")
        st.success("✅ **Status**: Active (Free, Unlimited)")
        st.markdown("**Used For**: Research interest (30-day pageviews)")
    
    # Campaign Planning Agent
    with st.expander("📱 **Campaign Planning Agent** - APIs Used"):
        st.markdown("### SerpAPI 🔍")
        if serp_keys > 0:
            st.info(f"ℹ️ {serp_keys} keys configured (currently not enabled)")
        else:
            st.warning("⚠️ Not configured (using fallback data)")
        st.markdown("**Used For**: Platform effectiveness data (YouTube, Facebook, Instagram)")
    
    # Summary
    st.markdown("---")
    st.markdown("## 📋 System Summary")
    
    total_paid_keys = youtube_keys + news_keys
    
    st.markdown(f"""
    ### Total APIs in System:
    - **YouTube API**: {youtube_keys} keys (10,000 req/day each)
    - **News API**: {news_keys} keys (100 req/day each)
    - **Reddit API**: Free (60 req/min, no auth required)
    - **Wikipedia API**: Free (unlimited)
    - **SerpAPI**: {serp_keys} keys (currently not enabled)
    
    ### Recovery Information:
    - Most paid APIs (YouTube, News) reset **24 hours** after rate limit
    - Free APIs (Reddit, Wikipedia) have generous/unlimited limits
    - Rate limits are tracked per key automatically
    
    ### Recommendations:
    - Wait 10-15 minutes between analyses if APIs are rate-limited
    - System uses fallback mechanisms when APIs are unavailable
    - Reddit and Wikipedia provide data even when other APIs fail
    """)

def get_samsung_upcoming_products():
    """Get dictionary of Samsung's upcoming products (not yet launched)"""
    return {
        # SMARTPHONES - FLAGSHIP (High-End)
        "Galaxy S26 Ultra": {
            "category": "Smartphones",
            "price": 1399.0,
            "description": "Next-gen flagship with 200MP AI camera, Snapdragon 8 Gen 4, and advanced Galaxy AI features for productivity and creativity",
            "launch_date": datetime(2026, 2, 15).date()
        },
        "Galaxy S26+": {
            "category": "Smartphones",
            "price": 1199.0,
            "description": "Premium smartphone with 6.7-inch Dynamic AMOLED display, flagship camera system, and all-day battery life",
            "launch_date": datetime(2026, 2, 15).date()
        },
        "Galaxy Z Fold 7": {
            "category": "Smartphones",
            "price": 1899.0,
            "description": "Revolutionary foldable with ultra-thin design, enhanced S Pen support, and seamless multitasking experience",
            "launch_date": datetime(2026, 8, 10).date()
        },
        "Galaxy Z Flip 7": {
            "category": "Smartphones",
            "price": 1099.0,
            "description": "Compact foldable with larger cover screen, improved hinge durability, and AI-powered photography",
            "launch_date": datetime(2026, 8, 10).date()
        },
        
        # SMARTPHONES - MID-RANGE
        "Galaxy A76 5G": {
            "category": "Smartphones",
            "price": 599.0,
            "description": "Premium mid-range with 120Hz Super AMOLED display, 108MP camera, and 5G connectivity at accessible price",
            "launch_date": datetime(2026, 3, 20).date()
        },
        "Galaxy A56 5G": {
            "category": "Smartphones",
            "price": 449.0,
            "description": "Balanced performance smartphone with powerful processor, versatile camera system, and long-lasting 5000mAh battery",
            "launch_date": datetime(2026, 4, 10).date()
        },
        "Galaxy M66 5G": {
            "category": "Smartphones",
            "price": 399.0,
            "description": "Performance-focused device with gaming-optimized processor, 6000mAh battery, and 25W fast charging",
            "launch_date": datetime(2026, 5, 15).date()
        },
        
        # SMARTPHONES - BUDGET
        "Galaxy A26": {
            "category": "Smartphones",
            "price": 299.0,
            "description": "Affordable smartphone with essential features, 50MP camera, and reliable all-day performance for everyday users",
            "launch_date": datetime(2026, 6, 1).date()
        },
        "Galaxy M36": {
            "category": "Smartphones",
            "price": 249.0,
            "description": "Budget-friendly device with large display, dual cameras, and extended battery life for value seekers",
            "launch_date": datetime(2026, 7, 1).date()
        },
        "Galaxy F26": {
            "category": "Smartphones",
            "price": 229.0,
            "description": "Entry-level smartphone with modern design, decent performance, and Samsung's One UI experience",
            "launch_date": datetime(2026, 8, 15).date()
        },
        
        # TABLETS - HIGH-END
        "Galaxy Tab S10 Ultra": {
            "category": "Tablets",
            "price": 1199.0,
            "description": "Premium 14.6-inch tablet with AMOLED display, S Pen included, powerful for productivity and creative work",
            "launch_date": datetime(2026, 4, 5).date()
        },
        "Galaxy Tab S10+": {
            "category": "Tablets",
            "price": 899.0,
            "description": "High-performance 12.4-inch tablet with flagship specs, ideal for professionals and content creators",
            "launch_date": datetime(2026, 4, 5).date()
        },
        
        # TABLETS - MID-RANGE
        "Galaxy Tab A10": {
            "category": "Tablets",
            "price": 449.0,
            "description": "Versatile 10.5-inch tablet for entertainment and productivity, with long battery life and immersive display",
            "launch_date": datetime(2026, 5, 20).date()
        },
        "Galaxy Tab A9 Lite": {
            "category": "Tablets",
            "price": 249.0,
            "description": "Affordable compact tablet perfect for media consumption, online learning, and casual browsing",
            "launch_date": datetime(2026, 6, 10).date()
        },
        
        # WEARABLES - SMARTWATCHES
        "Galaxy Watch 8 Ultra": {
            "category": "Wearables",
            "price": 699.0,
            "description": "Premium smartwatch with advanced health tracking, outdoor features, sapphire crystal, and multi-day battery",
            "launch_date": datetime(2026, 8, 1).date()
        },
        "Galaxy Watch 8 Pro": {
            "category": "Wearables",
            "price": 449.0,
            "description": "Feature-rich smartwatch with comprehensive health monitoring, fitness tracking, and seamless Galaxy ecosystem integration",
            "launch_date": datetime(2026, 8, 1).date()
        },
        "Galaxy Watch 8": {
            "category": "Wearables",
            "price": 329.0,
            "description": "Stylish smartwatch with essential health features, customizable watch faces, and all-day battery life",
            "launch_date": datetime(2026, 8, 1).date()
        },
        
        # WEARABLES - FITNESS BANDS
        "Galaxy Fit 4 Pro": {
            "category": "Wearables",
            "price": 149.0,
            "description": "Advanced fitness tracker with GPS, heart rate monitoring, sleep tracking, and 14-day battery life",
            "launch_date": datetime(2026, 3, 15).date()
        },
        "Galaxy Fit 4": {
            "category": "Wearables",
            "price": 99.0,
            "description": "Affordable fitness band with essential health tracking, water resistance, and lightweight comfortable design",
            "launch_date": datetime(2026, 3, 15).date()
        },
        
        # TVs - PREMIUM
        "Neo QLED 8K QN95D": {
            "category": "TV",
            "price": 4999.0,
            "description": "Flagship 75-inch 8K TV with Neural Quantum Processor, Mini LED backlight, and immersive gaming features",
            "launch_date": datetime(2026, 3, 1).date()
        },
        "OLED S96D": {
            "category": "TV",
            "price": 3499.0,
            "description": "Premium 65-inch OLED TV with perfect blacks, Dolby Atmos, and AI-powered picture optimization",
            "launch_date": datetime(2026, 3, 1).date()
        },
        
        # TVs - MID-RANGE
        "QLED Q75D": {
            "category": "TV",
            "price": 1299.0,
            "description": "4K QLED smart TV with Quantum Dot technology, 120Hz refresh rate, and comprehensive streaming apps",
            "launch_date": datetime(2026, 4, 1).date()
        },
        "Crystal UHD DU8500": {
            "category": "TV",
            "price": 799.0,
            "description": "Affordable 55-inch 4K TV with Crystal Processor, HDR support, and smart TV platform",
            "launch_date": datetime(2026, 5, 1).date()
        },
        
        # EARBUDS
        "Galaxy Buds4 Pro": {
            "category": "Wearables",
            "price": 249.0,
            "description": "Premium wireless earbuds with intelligent ANC, 360 Audio, and studio-quality sound for audiophiles",
            "launch_date": datetime(2026, 2, 20).date()
        },
        "Galaxy Buds4": {
            "category": "Wearables",
            "price": 149.0,
            "description": "High-quality wireless earbuds with active noise cancellation and seamless device switching",
            "launch_date": datetime(2026, 2, 20).date()
        }
    }

def create_product_input_form():
    """Create the main product input form"""
    st.markdown('<h2 class="agent-header">📝 Product Information</h2>', unsafe_allow_html=True)
    
    # Get upcoming Samsung products
    upcoming_products = get_samsung_upcoming_products()
    product_names = ["Select a product..."] + list(upcoming_products.keys()) + ["➕ Custom Product..."]
    
    # Initialize session state for selected product
    if 'selected_product' not in st.session_state:
        st.session_state.selected_product = "Select a product..."
    
    # Product selection OUTSIDE the form so it updates immediately
    selected_product = st.selectbox(
        "Product Name",
        product_names,
        index=product_names.index(st.session_state.selected_product) if st.session_state.selected_product in product_names else 0,
        help="Select an upcoming Samsung product or choose 'Custom Product' to enter your own",
        key="product_selector"
    )
    
    # Update session state
    st.session_state.selected_product = selected_product
    
    # Check if custom product is selected
    is_custom_product = (selected_product == "➕ Custom Product...")
    
    # Show custom product name input if needed (OUTSIDE form for immediate display)
    custom_product_name = ""
    if is_custom_product:
        custom_product_name = st.text_input(
            "Enter Custom Product Name",
            placeholder="e.g., Galaxy S27 Pro, Galaxy Ring 2, etc.",
            help="Enter the name of your custom Samsung product",
            key="custom_product_name"
        )
    
    # Auto-fill based on selection
    if selected_product != "Select a product..." and not is_custom_product:
        product_data = upcoming_products[selected_product]
        default_category = product_data["category"]
        default_price = product_data["price"]
        default_description = product_data["description"]
        default_launch_date = product_data["launch_date"]
        is_editable = False  # Fields are pre-filled, but still editable
    else:
        default_category = "Smartphones"
        default_price = 999.0
        default_description = ""
        default_launch_date = datetime.now().date() + timedelta(days=90)
        is_editable = True
    
    # Start the form here (after product selection)
    with st.form("product_info_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            product_category = st.selectbox(
                "Product Category",
                ["Smartphones", "Tablets", "Wearables", "TV", "Laptops", "Appliances"],
                index=["Smartphones", "Tablets", "Wearables", "TV", "Laptops", "Appliances"].index(default_category),
                help="Product category" + (" (auto-filled, editable)" if not is_editable else "")
            )
            product_price = st.number_input(
                "Product Price ($)",
                min_value=100.0,
                max_value=10000.0,
                value=float(default_price),
                step=50.0,
                help="Expected retail price" + (" (auto-filled, editable)" if not is_editable else "")
            )
        
        with col2:
            product_description = st.text_area(
                "Product Description",
                value=default_description,
                height=100,
                placeholder="Describe your product's key features, target market, and unique selling points..." if is_custom_product else "",
                help="Key features and positioning" + (" (auto-filled, editable)" if not is_editable else "")
            )
            launch_date = st.date_input(
                "Expected Launch Date",
                value=default_launch_date,
                help="Planned launch date" + (" (auto-filled, editable)" if not is_editable else "")
            )
        
        # Store selected product name
        if is_custom_product:
            product_name = custom_product_name if custom_product_name else ""
        else:
            product_name = selected_product if selected_product != "Select a product..." else ""
        
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
            if not product_name:
                if is_custom_product:
                    st.error("⚠️ Please enter a custom product name")
                else:
                    st.error("⚠️ Please select a product from the dropdown or choose 'Custom Product'")
                return None
            if not age_groups or not social_platforms:
                st.error("⚠️ Please select target age groups and social media platforms")
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
    
    # Display data source information
    market_data_info = market_data.get('historical_data', {})
    data_source = market_data_info.get('data_source', 'Unknown')
    api_sources = market_data_info.get('api_sources', [])
    products_analyzed = market_data_info.get('similar_products_analyzed', 0)
    
    if data_source and 'Real API' in data_source:
        st.success(f"✅ **Using REAL API Data**: {data_source}")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("API Sources Used", len(api_sources) if api_sources else 0)
        with col2:
            st.metric("Similar Products Analyzed", products_analyzed)
        with col3:
            confidence = market_data_info.get('real_data_confidence', 'MEDIUM')
            st.metric("Data Confidence", confidence)
        
        if api_sources:
            st.info(f"📊 **Data Sources**: {', '.join(api_sources)}")
    
    # Historical and forecast sales chart
    if 'historical_sales' in viz_data and 'sales_forecast' in viz_data:
        # Get Samsung colors
        samsung_blue = SAMSUNG_COLORS['samsung_blue'] if SAMSUNG_THEME_AVAILABLE else '#1428A0'
        samsung_light_blue = SAMSUNG_COLORS['samsung_light_blue'] if SAMSUNG_THEME_AVAILABLE else '#2E5FCC'
        
        fig = go.Figure()
        
        # Historical data
        hist_data = viz_data['historical_sales']
        fig.add_trace(go.Scatter(
            x=hist_data['dates'],
            y=hist_data['sales'],
            mode='lines+markers',
            name='Historical Sales (API-based)',
            line=dict(color=samsung_blue, width=3),
            marker=dict(size=6, color=samsung_blue),
            hovertemplate='<b>Date</b>: %{x}<br><b>Sales</b>: %{y:,.0f} units<br><extra></extra>'
        ))
        
        # Forecast data
        forecast_data = viz_data['sales_forecast']
        fig.add_trace(go.Scatter(
            x=forecast_data['dates'],
            y=forecast_data['sales'],
            mode='lines+markers',
            name='Sales Forecast (AI-powered)',
            line=dict(color=samsung_light_blue, width=3, dash='dash'),
            marker=dict(size=6, color=samsung_light_blue, symbol='diamond'),
            hovertemplate='<b>Date</b>: %{x}<br><b>Forecast</b>: %{y:,.0f} units<br><extra></extra>'
        ))
        
        # Confidence interval
        fig.add_trace(go.Scatter(
            x=forecast_data['dates'] + forecast_data['dates'][::-1],
            y=forecast_data['upper_bound'] + forecast_data['lower_bound'][::-1],
            fill='toself',
            fillcolor='rgba(20, 40, 160, 0.15)',  # Samsung blue with transparency
            line=dict(color='rgba(255,255,255,0)'),
            name='Confidence Interval',
            showlegend=True,
            hoverinfo='skip'
        ))
        
        # Add annotation about data source
        annotation_text = "📊 Real-Time Data: "
        if api_sources:
            annotation_text += ", ".join(api_sources[:2])
        else:
            annotation_text += "Similar Samsung Products"
        
        # Apply Samsung theme if available (excluding title to avoid conflict)
        if SAMSUNG_THEME_AVAILABLE:
            layout_config = get_samsung_plotly_theme()['layout'].copy()
            layout_config.pop('title', None)  # Remove title from theme config
        else:
            layout_config = {}
        
        fig.update_layout(
            **layout_config,
            title={
                'text': "📈 Sales History & AI Forecast<br><sub style='color: #5A5A5A;'>Powered by Real API Data from Similar Samsung Products</sub>",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 22, 'color': samsung_blue, 'family': 'Inter, sans-serif'},
                'pad': {'t': 20, 'b': 20}
            },
            xaxis_title="📅 Date",
            yaxis_title="📦 Sales Volume (Units)",
            height=600,
            margin=dict(t=120, b=160, l=80, r=80),
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.15,
                xanchor="center",
                x=0.5,
                bgcolor='rgba(255,255,255,0.9)',
                bordercolor=samsung_blue,
                borderwidth=1,
                font=dict(size=11),
                itemsizing='constant',
                tracegroupgap=20
            ),
            annotations=[
                dict(
                    text=annotation_text,
                    xref="paper", yref="paper",
                    x=0.5, y=-0.32,
                    showarrow=False,
                    font=dict(size=11, color="#5A5A5A"),
                    xanchor='center'
                )
            ]
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show API metrics details if available
        api_metrics = market_data_info.get('api_metrics_used', [])
        if api_metrics:
            with st.expander("📊 View Detailed API Metrics Used"):
                st.markdown("**Real API Metrics for Similar Products:**")
                for metric in api_metrics:
                    st.markdown(f"""
                    - **{metric.get('product', 'Unknown')}**
                      - Trends Data: {metric.get('trends_data', 'N/A')}
                      - YouTube Data: {metric.get('youtube_data', 'N/A')}
                      - News Data: {metric.get('news_data', 'N/A')}
                      - Source: {metric.get('source', 'N/A')}
                    """)
    else:
        st.warning("⚠️ Historical sales data not available")
    
    # City performance chart with API data attribution
    city_analysis = market_data.get('city_analysis', {})
    city_data_source = city_analysis.get('data_source', 'Unknown')
    
    if 'Real API' in city_data_source:
        # Show parallel processing indicator
        if 'Parallel' in city_data_source:
            processing_time = city_analysis.get('processing_time_seconds', 0)
            parallel_workers = city_analysis.get('parallel_workers', 0)
            st.success(f"✅ **City Data from REAL APIs (Parallel Processing)**: {city_data_source}")
            st.info(f"⚡ **Performance**: Analyzed {city_analysis.get('cities_analyzed', 0)} cities in {processing_time} seconds using {parallel_workers} parallel workers")
        else:
            st.success(f"✅ **City Data from REAL APIs**: {city_data_source}")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            cities_analyzed = city_analysis.get('cities_analyzed', 0)
            st.metric("Cities Analyzed", cities_analyzed)
        with col2:
            similar_used = city_analysis.get('similar_products_used', 0)
            st.metric("Similar Products Used", similar_used)
        with col3:
            confidence = city_analysis.get('real_data_confidence', 'MEDIUM')
            st.metric("Data Confidence", confidence)
        with col4:
            processing_time = city_analysis.get('processing_time_seconds', 0)
            if processing_time > 0:
                st.metric("Processing Time", f"{processing_time}s")
            else:
                st.metric("Processing Time", "N/A")
        
        # Show API sources used
        api_sources_city = city_analysis.get('api_sources', [])
        if api_sources_city:
            st.info(f"📊 **Regional Data Sources**: {', '.join(api_sources_city)}")
    
    if 'city_performance' in viz_data:
        city_data = viz_data['city_performance']
        
        # Get Samsung colors
        samsung_blue = SAMSUNG_COLORS['samsung_blue'] if SAMSUNG_THEME_AVAILABLE else '#1428A0'
        chart_colors = get_samsung_chart_colors() if SAMSUNG_THEME_AVAILABLE else None
        
        fig = px.bar(
            x=city_data['cities'][:10],  # Top 10 cities
            y=city_data['sales'][:10],
            title="🌍 Top Performing Cities<br><sub style='color: #5A5A5A;'>Real-Time Regional Data powered by Wikipedia, YouTube & News APIs</sub>",
            labels={'x': 'City', 'y': 'Sales Volume (Units)'},
            color=city_data['sales'][:10],
            color_continuous_scale=[[0, '#2E5FCC'], [0.5, '#1428A0'], [1, '#0C1A51']]  # Samsung blue gradient
        )
        
        # Apply Samsung theme (excluding title to avoid conflict)
        if SAMSUNG_THEME_AVAILABLE:
            layout_config = get_samsung_plotly_theme()['layout'].copy()
            layout_config.pop('title', None)  # Remove title from theme config
        else:
            layout_config = {}
        
        fig.update_layout(
            **layout_config,
            height=500,
            xaxis_title="🏙️ City",
            yaxis_title="📦 Average Sales Volume (Units)",
            showlegend=False,
            title={'font': {'size': 22, 'color': samsung_blue, 'family': 'Inter, sans-serif'}}
        )
        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>Sales: %{y:,.0f} units<br><extra></extra>',
            marker=dict(
                line=dict(color='white', width=2),
                pattern=dict(shape="")
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show detailed city API metrics if available
        city_api_details = city_analysis.get('city_api_details', {})
        if city_api_details and 'Real API' in city_data_source:
            with st.expander("🌍 View Detailed Regional API Metrics"):
                st.markdown("**Real API Metrics by City:**")
                
                # Display top 5 cities
                top_cities = city_analysis.get('top_cities', [])[:5]
                for city, sales in top_cities:
                    if city in city_api_details:
                        details = city_api_details[city]
                        
                        # Determine regional interest source dynamically
                        data_sources = details.get('data_sources', '')
                        if 'Wikipedia Regional API' in data_sources:
                            interest_source = "Wikipedia Pageviews"
                        elif 'Google Trends Regional' in data_sources:
                            interest_source = "Google Trends"
                        else:
                            interest_source = "Market Data"
                        
                        st.markdown(f"""
                        **{city}** ({details.get('country', 'N/A')})
                        - Sales Volume: {sales:,.0f} units
                        - Regional Interest: {details.get('regional_interest', 0):.1f}/100 ({interest_source})
                        - YouTube Factor: {details.get('youtube_factor', 1.0):.2f}x (Real API)
                        - News Factor: {details.get('news_factor', 1.0):.2f}x (Real API)
                        - Growth Potential: {details.get('growth_potential', 0)*100:.1f}%
                        - Data Sources: {details.get('data_sources', 'N/A')}
                        - Market Size: {details.get('market_size', 'N/A').title()}
                        
                        ---
                        """)
    else:
        st.warning("⚠️ City performance data not available")
    
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
            advice = "- No feedback available to analyze."
            try:
                coord = st.session_state.get('coordinator')
                if coord and feedback:
                    advice_result = coord.send_message('ui', 'competitor_tracker', 'analyze_feedback_and_advise', {
                        'feedback_list': feedback
                    })
                    if advice_result:
                        advice = advice_result
            except Exception as e:
                advice = f"- Unable to analyze feedback: {e}"
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
    
    # Display API data source information
    raw_customer_data = customer_data.get('raw_customer_data', {})
    data_source = getattr(raw_customer_data, 'attrs', {}).get('data_source', 'Unknown')
    api_count = getattr(raw_customer_data, 'attrs', {}).get('api_count', 0)
    total_customers = getattr(raw_customer_data, 'attrs', {}).get('total_customers', 0)
    api_metrics = getattr(raw_customer_data, 'attrs', {}).get('api_metrics', [])
    
    if data_source and 'Real API' in data_source:
        st.success(f"✅ **Using REAL API Data**: {data_source}")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Data Sources Used", f"{api_count} APIs")
        with col2:
            st.metric("Total Customer Base", f"{total_customers:,}")
        with col3:
            st.metric("Similar Products Analyzed", len(api_metrics))
        
        # Show detailed API metrics
        if api_metrics:
            with st.expander("📊 View Detailed API Metrics"):
                st.markdown("**Customer Engagement by Similar Product:**")
                for metric in api_metrics:
                    st.markdown(f"""
                    **{metric.get('product', 'Unknown')}**
                    - YouTube Views: {metric.get('youtube_reach', 0):,}
                    - News Articles: {metric.get('news_reach', 0)}
                    - Reddit Engagement: {metric.get('reddit_reach', 0):,} (upvotes + comments)
                    - Wikipedia Pageviews: {metric.get('wikipedia_reach', 0):,} (30 days)
                    - Estimated Customers: {metric.get('estimated_customers', 0):,}
                    
                    ---
                    """)
    
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
            # Convert markdown bold to HTML bold for proper rendering
            import re
            rec_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', rec)
            st.markdown(f'<div class="recommendation-box">{i}. {rec_html}</div>', unsafe_allow_html=True)

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
                monthly_cost = platform_data.get('monthly_ad_cost', 0)
                months = platform_data.get('months', 1)
                total_cost = platform_data.get('total_cost', 0)
                daily_budget = total_cost / (months * 30) if months > 0 else 0
                avg_cpc = 1.50  # Standard CPC from campaign planning agent
                
                st.markdown(f"""
                - **Total Budget**: ${total_cost:,.2f}
                - **Monthly Cost**: ${monthly_cost:,.2f}
                - **Daily Budget**: ${daily_budget:,.2f}
                - **Avg CPC**: ${avg_cpc:.2f}
                """)
            
            with col2:
                st.markdown("#### Performance Metrics")
                est_clicks = platform_data.get('estimated_clicks', 0)
                est_reach = platform_data.get('estimated_reach', 0)
                est_impressions = platform_data.get('estimated_impressions', 0)
                est_engagement = platform_data.get('estimated_engagement', 0)
                daily_clicks = est_clicks / (platform_data.get('months', 1) * 30) if platform_data.get('months', 1) > 0 else 0
                
                st.markdown(f"""
                - **Estimated Clicks**: {est_clicks:,}
                - **Estimated Reach**: {est_reach:,}
                - **Estimated Impressions**: {est_impressions:,}
                - **Estimated Engagement**: {est_engagement:,}
                - **Daily Clicks**: {int(daily_clicks):,}
                """)
            
            with col3:
                st.markdown("#### ROI Projection")
                roi_proj = platform_data['roi_projection']
                st.markdown(f"""
                - **ROI**: {roi_proj['roi_percentage']:.1f}%
                - **Est. Conversions**: {roi_proj['estimated_conversions']:.1f}
                - **Est. Revenue**: ${roi_proj['estimated_revenue']:,.2f}
                """)
    
    # Fetch platform-specific timeline and recommendations
    campaign_planner = st.session_state.get('campaign_planner')
    if not campaign_planner:
        campaign_planner = CampaignPlanningAgent(st.session_state.coordinator)
        st.session_state['campaign_planner'] = campaign_planner
    details = campaign_planner.get_platform_campaign_details(
        selected_platform,
        campaign_data.get('target_audience', {}).get('duration_days', 30)
    )
    platform_timeline = details['timeline']
    platform_recommendations = details['recommendations']

    # Show platform-specific timeline
    st.markdown("### 📅 Campaign Timeline")
    for phase in platform_timeline.get('phases', []):
        st.markdown(f"""
        **{phase['phase']}** ({phase['duration']})
        - {', '.join(phase['activities'])}
        """)

    # Show platform-specific recommendations
    st.markdown("### 💡 Campaign Recommendations")
    for i, rec in enumerate(platform_recommendations, 1):
        st.markdown(f'<div class="recommendation-box">{i}. {rec}</div>', unsafe_allow_html=True)

def main():
    """Main application function"""
    # Initialize agents
    if not initialize_agents():
        st.error("Failed to initialize agents. Please refresh the page.")
        return
    
    # Samsung branded header already displayed at top of page (lines 59-75)
    # No need for duplicate header
    
    # Check if API Status page should be shown
    if st.session_state.get('show_api_status', False):
        # Add a back button
        if st.button("⬅️ Back to Main Dashboard"):
            st.session_state['show_api_status'] = False
            st.rerun()
        
        # Display API Status page
        display_api_status_page()
        return
    
    # Tab navigation (instead of sidebar dropdown)
    tabs = st.tabs(["📝 Product Input", "📊 Market Analysis", "🏆 Competitor Analysis", "👥 Customer Segmentation", "📱 Campaign Planning"])
    
    # Tab 1: Product Input
    with tabs[0]:
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
                    st.markdown("Click on other tabs to view detailed results.")
                    
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
    
    # Tab 2: Market Analysis
    with tabs[1]:
        if 'analysis_results' in st.session_state:
            display_market_analysis(st.session_state.analysis_results)
        else:
            st.info("👈 Please complete the Product Input first to see analysis results.")
    
    # Tab 3: Competitor Analysis
    with tabs[2]:
        if 'analysis_results' in st.session_state:
            display_competitor_analysis(st.session_state.analysis_results)
        else:
            st.info("👈 Please complete the Product Input first to see analysis results.")
    
    # Tab 4: Customer Segmentation
    with tabs[3]:
        if 'analysis_results' in st.session_state:
            # Check if user has upgraded
            user_plan = st.session_state.get('user_plan', 'free')
            
            if user_plan in ['pro', 'business', 'enterprise']:
                # User has upgraded - show the actual customer segmentation results
                display_customer_segmentation(st.session_state.analysis_results)
            else:
                # Show pricing/upgrade page for Customer Segmentation
                if display_pricing_comparison:
                    display_pricing_comparison()
                else:
                    st.markdown("## 👥 Customer Segmentation")
                    st.warning("Upgrade to access Customer Segmentation features!")
                    st.markdown("""
                    ### Features included:
                    - **Pro**: Basic customer segmentation
                    - **Business**: Advanced behavioral segmentation
                    - **Enterprise**: Full CRM integration
                    
                    Contact sales to upgrade!
                    """)
        else:
            st.info("👈 Please complete the Product Input first to see analysis results.")
    
    # Tab 5: Campaign Planning
    with tabs[4]:
        if 'analysis_results' in st.session_state:
            # Check if user has upgraded to Business or Enterprise
            user_plan = st.session_state.get('user_plan', 'free')
            
            if user_plan in ['business', 'enterprise']:
                # User has Business/Enterprise plan - show the actual campaign planning results
                display_campaign_planning(st.session_state.analysis_results)
            else:
                # Show pricing/upgrade page for Campaign Planning
                if display_pricing_comparison:
                    display_pricing_comparison()
                else:
                    st.markdown("## 📱 Campaign Planning")
                    st.warning("Upgrade to access Campaign Planning features!")
                    st.markdown("""
                    ### Features included:
                    - **Business**: Full campaign planning & budget optimization
                    - **Enterprise**: Full planning + ROI simulation
                    
                    Contact sales to upgrade!
                    """)
        else:
            st.info("👈 Please complete the Product Input first to see analysis results.")

    # Sidebar API Status Button
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔌 System Management")
    if st.sidebar.button("📊 Check API Status", use_container_width=True):
        st.session_state['show_api_status'] = True
    
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
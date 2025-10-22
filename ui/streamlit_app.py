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

# Responsible AI: simple audit logging helpers
def _audit_append(entry: dict):
    try:
        base = os.path.join(os.path.dirname(__file__), '..')
        audit_path = os.path.join(base, 'responsible_ai', 'audit_log.json')
        # ensure directory exists
        os.makedirs(os.path.dirname(audit_path), exist_ok=True)
        if not os.path.exists(audit_path):
            with open(audit_path, 'w', encoding='utf-8') as f:
                json.dump([], f)
        with open(audit_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data.append(entry)
        with open(audit_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        # Not fatal for UI, but show an error
        try:
            st.error(f"Audit log write failed: {e}")
        except Exception:
            pass
        return False


def run_fairness_checks(threshold_concentration=0.6, churn_threshold=3):
    """Run simple automatic fairness checks over audit log and agents.

    Returns a list of warning dicts: {severity, id, message, details}
    """
    base = os.path.join(os.path.dirname(__file__), '..')
    audit_path = os.path.join(base, 'responsible_ai', 'audit_log.json')
    agents_path = os.path.join(base, 'pricing', 'data', 'agents.json')

    # Load audit and agents
    try:
        audits = []
        if os.path.exists(audit_path):
            with open(audit_path, 'r', encoding='utf-8') as f:
                audits = json.load(f)
    except Exception:
        audits = []

    try:
        agents = []
        if os.path.exists(agents_path):
            with open(agents_path, 'r', encoding='utf-8') as f:
                agents = json.load(f)
    except Exception:
        agents = []

    warnings = []

    # 1) Plan concentration check
    assigned = [a for a in agents if a.get('plan_id')]
    total_assigned = len(assigned)
    if total_assigned > 0:
        counts = {}
        for a in assigned:
            counts[a.get('plan_id')] = counts.get(a.get('plan_id'), 0) + 1
        for pid, cnt in counts.items():
            frac = cnt / total_assigned
            if frac >= threshold_concentration:
                warnings.append({
                    'severity': 'high',
                    'id': 'plan_concentration',
                    'message': f'Plan {pid} holds {frac:.0%} of assigned agents (threshold {threshold_concentration:.0%}).',
                    'details': {'plan_id': pid, 'count': cnt, 'total_assigned': total_assigned}
                })

    # 2) Unassigned agent rate
    total_agents = len(agents)
    if total_agents > 0:
        unassigned = len([a for a in agents if not a.get('plan_id')])
        unassigned_frac = unassigned / total_agents
        if unassigned_frac >= 0.5:
            warnings.append({
                'severity': 'medium',
                'id': 'high_unassigned_rate',
                'message': f'{unassigned_frac:.0%} of agents are unassigned to a plan.',
                'details': {'unassigned': unassigned, 'total_agents': total_agents}
            })

    # 3) Assignment churn per agent (from audit log)
    # Count assign_agent_plan actions per agent in recent audits
    assign_events = [e for e in audits if e.get('action') == 'assign_agent_plan']
    churn_counts = {}
    for e in assign_events:
        aid = e.get('agent_id')
        churn_counts[aid] = churn_counts.get(aid, 0) + 1
    for aid, cnt in churn_counts.items():
        if cnt >= churn_threshold:
            warnings.append({
                'severity': 'low',
                'id': 'assignment_churn',
                'message': f'Agent {aid} changed assignment {cnt} times recently (threshold {churn_threshold}).',
                'details': {'agent_id': aid, 'changes': cnt}
            })

    # 4) Budget skew detection (best-effort): look for audit entries with budget
    budget_events = [e for e in audits if 'budget' in (e.get('details') or {}) or 'budget' in e]
    if budget_events:
        budgets = []
        for e in budget_events:
            b = None
            if 'budget' in e:
                b = e.get('budget')
            elif isinstance(e.get('details'), dict) and 'budget' in e.get('details'):
                b = e.get('details').get('budget')
            try:
                budgets.append(float(b))
            except Exception:
                pass
        if budgets:
            avg = sum(budgets) / len(budgets)
            high = len([b for b in budgets if b > 2 * avg])
            if high > 0:
                warnings.append({
                    'severity': 'medium',
                    'id': 'budget_skew',
                    'message': f'{high} campaign budgets are >2x the average ({avg:.2f}).',
                    'details': {'avg_budget': avg, 'outliers': high}
                })

    return warnings

# Optional network library used for API checks; gracefully degrade if missing
try:
    import requests
except Exception:
    requests = None

# Add agents to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

# Import unified API management system
try:
    from unified_api_manager import get_api_key, unified_api_manager
except ImportError as e:
    st.error(f"Error importing unified API manager: {e}")
    st.stop()

# Import agents
try:
    from communication_coordinator import coordinator, ProductInfo
    from market_trend_analyzer import MarketTrendAnalyzer
    from competitor_tracking_agent import CompetitorTrackingAgent
    from customer_segmentation_agent import CustomerSegmentationAgent
    from campaign_planning_agent import CampaignPlanningAgent
except Exception as e:
    # Show a clear, actionable error in the Streamlit frontend with traceback and debug info
    import traceback

    st.markdown("## ⚠️ Agent import failure")
    st.error("The app failed to import agent modules required to run. See details below.")

    # Short error message
    st.markdown("**Error:**")
    st.code(str(e))

    # Full traceback for debugging
    with st.expander("Show full traceback", expanded=False):
        st.code(traceback.format_exc())

    # Helpful debug information (sys.path and agents dir contents)
    with st.expander("Debug information (sys.path & agents folder)", expanded=False):
        try:
            st.markdown("**sys.path**")
            for p in sys.path:
                st.text(p)

            agents_path = os.path.join(os.path.dirname(__file__), '..', 'agents')
            st.markdown(f"**agents directory ({agents_path}) listing:**")
            try:
                for f in sorted(os.listdir(agents_path)):
                    st.text(f)
            except Exception as ex:
                st.text(f"Could not list agents directory: {ex}")
        except Exception:
            st.text("Could not collect debug info")

    st.markdown("---")
    st.markdown("Suggested fixes:\n- Ensure a file `communication_coordinator.py` exists in the `agents` folder or in the project root as expected.\n- If the module is located elsewhere, update `sys.path` or the import statements.\n- Re-run the app after fixing the module file.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Samsung Product Launch Planner | Enterprise Analytics Suite",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.samsung.com/support',
        'Report a bug': None,
        'About': "Samsung Product Launch Planner - Enterprise-grade analytics for strategic product launches"
    }
)

# Professional Samsung-themed CSS
st.markdown("""
<style>
    /* Import Samsung's preferred fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* Root variables for Samsung brand colors */
    :root {
        --samsung-blue: #1428A0;
        --samsung-light-blue: #4285F4;
        --samsung-dark-blue: #0F1B6B;
        --samsung-accent: #FF6B35;
        --samsung-gray: #F8F9FA;
        --samsung-dark-gray: #2C3E50;
        --samsung-success: #00C851;
        --samsung-warning: #FFB900;
        --gradient-primary: linear-gradient(135deg, #1428A0 0%, #4285F4 100%);
        --gradient-accent: linear-gradient(135deg, #FF6B35 0%, #FF8E53 100%);
        --shadow-soft: 0 4px 20px rgba(20, 40, 160, 0.1);
        --shadow-medium: 0 8px 40px rgba(20, 40, 160, 0.15);
    }
    
    /* Global styling */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Header styling */
    .main-header {
        background: var(--gradient-primary);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        letter-spacing: -0.02em;
        text-shadow: none;
    }
    
    .header-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        color: #6c757d;
        text-align: center;
        margin-top: -1rem;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    /* Agent section headers */
    .agent-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.2rem;
        font-weight: 600;
        color: var(--samsung-dark-blue);
        margin: 2.5rem 0 1.5rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid var(--samsung-light-blue);
        position: relative;
    }
    
    .agent-header::before {
        content: '';
        position: absolute;
        bottom: -3px;
        left: 0;
        width: 60px;
        height: 3px;
        background: var(--gradient-accent);
        border-radius: 2px;
    }
    
    /* Enhanced metric containers */
    .metric-container {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        margin: 1rem 0;
        box-shadow: var(--shadow-soft);
        border: 1px solid rgba(20, 40, 160, 0.08);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-primary);
    }
    
    .metric-container:hover {
        box-shadow: var(--shadow-medium);
        transform: translateY(-2px);
    }
    
    /* Professional recommendation boxes */
    .recommendation-box {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid rgba(20, 40, 160, 0.12);
        margin: 1.5rem 0;
        position: relative;
        box-shadow: var(--shadow-soft);
    }
    
    .recommendation-box::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 5px;
        background: var(--gradient-accent);
        border-radius: 0 8px 8px 0;
    }
    
    /* Sidebar enhancement */
    .css-1d391kg {
        background: var(--gradient-primary);
    }
    
    .css-1d391kg .css-1v0mbdj {
        color: white;
    }
    
    /* Ensure sidebar toggle is visible */
    [data-testid="stSidebar"] {
        background: var(--gradient-primary);
    }
    
    [data-testid="stSidebar"] > div {
        background: var(--gradient-primary);
    }
    
    /* Sidebar toggle button */
    .css-1rs6os, .css-17ziqus {
        visibility: visible !important;
        display: block !important;
    }
    
    /* Sidebar content styling */
    .css-1cypcdb {
        background: var(--gradient-primary);
    }
    
    /* Make sure sidebar chevron is visible */
    button[kind="header"] {
        visibility: visible !important;
        display: flex !important;
    }
    
    /* Form styling */
    .stForm {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: var(--shadow-medium);
        border: 1px solid rgba(20, 40, 160, 0.08);
    }
    
    /* Button styling */
    .stButton > button {
        background: var(--gradient-primary);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.02em;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-soft);
    }
    
    .stButton > button:hover {
        background: var(--samsung-dark-blue);
        box-shadow: var(--shadow-medium);
        transform: translateY(-1px);
    }
    
    /* Input field styling */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stNumberInput > div > div > input {
        border-radius: 12px;
        border: 2px solid rgba(20, 40, 160, 0.1);
        padding: 0.8rem 1rem;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--samsung-light-blue);
        box-shadow: 0 0 0 3px rgba(66, 133, 244, 0.1);
    }
    
    /* Enhanced Professional Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        border-radius: 20px;
        padding: 8px;
        box-shadow: var(--shadow-medium);
        border: 1px solid rgba(20, 40, 160, 0.08);
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 16px;
        padding: 16px 24px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 1rem;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        color: var(--samsung-dark-gray);
        min-width: 120px;
        text-align: center;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(20, 40, 160, 0.05);
        border-color: rgba(20, 40, 160, 0.1);
        transform: translateY(-1px);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: var(--gradient-primary);
        color: white;
        border-color: var(--samsung-light-blue);
        box-shadow: 0 4px 12px rgba(20, 40, 160, 0.2);
        transform: translateY(-2px);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"]::before {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 50%;
        transform: translateX(-50%);
        width: 30px;
        height: 3px;
        background: var(--gradient-accent);
        border-radius: 2px;
    }
    
    /* Progress indicators */
    .stProgress > div > div {
        background: var(--gradient-primary);
        border-radius: 10px;
    }
    
    /* Success/Info/Warning messages */
    .stSuccess {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 1px solid var(--samsung-success);
        border-radius: 12px;
        color: #155724;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #cce7ff 0%, #b3d9ff 100%);
        border: 1px solid var(--samsung-light-blue);
        border-radius: 12px;
        color: var(--samsung-dark-blue);
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border: 1px solid var(--samsung-warning);
        border-radius: 12px;
        color: #856404;
    }
    
    /* Chart containers */
    .js-plotly-plot {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: var(--shadow-soft);
    }
    
    /* Custom Samsung branding elements */
    .samsung-badge {
        display: inline-block;
        background: var(--gradient-accent);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        margin: 4px;
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: var(--shadow-soft);
        border: 1px solid rgba(20, 40, 160, 0.08);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        box-shadow: var(--shadow-medium);
        transform: translateY(-4px);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        background: var(--gradient-primary);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        
        .agent-header {
            font-size: 1.8rem;
        }
        
        .metric-container, .recommendation-box, .stForm {
            padding: 1.5rem;
        }
    }
    
    /* Hide Streamlit branding - be specific to not hide sidebar */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Hide only the main app header, not sidebar controls */
    .main .block-container > header {visibility: hidden;}
    
    /* Ensure sidebar and its controls remain visible */
    [data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
    }
    
    [data-testid="stSidebar"] button {
        display: block !important;
        visibility: visible !important;
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
    """Display professional Samsung-branded header"""
    # Hero section with Samsung branding
    st.markdown('''
    <div style="text-align: center; padding: 2rem 0 3rem 0;">
        <h1 class="main-header">� Samsung Product Launch Planner</h1>
        <p class="header-subtitle">Enterprise-Grade Analytics Suite for Strategic Product Launches</p>
        <div style="margin: 2rem 0;">
            <span class="samsung-badge">🌟 AI-Powered</span>
            <span class="samsung-badge">📊 Real-Time Analytics</span>
            <span class="samsung-badge">🎯 Market Intelligence</span>
            <span class="samsung-badge">🚀 Launch Optimization</span>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Professional feature overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('''
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <h3>Market Intelligence</h3>
            <p>Advanced trend analysis and sales forecasting powered by real market data</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3>Competitor Insights</h3>
            <p>Comprehensive competitor tracking and strategic positioning analysis</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown('''
        <div class="feature-card">
            <div class="feature-icon">👥</div>
            <h3>Customer Analytics</h3>
            <p>Precision customer segmentation and behavioral analysis</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown('''
        <div class="feature-card">
            <div class="feature-icon">🚀</div>
            <h3>Campaign Optimization</h3>
            <p>AI-driven marketing campaigns and launch strategy optimization</p>
        ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # API Status Display
    with st.expander("🔑 Unified API Management Status", expanded=False):
        st.markdown("**Enterprise API Key Management System**")
        
        # Get API status
        api_status = unified_api_manager.get_status_report()
        
        if api_status:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📊 Active Services:**")
                for service, info in api_status.items():
                    active_keys = info['active_keys']
                    total_keys = info['total_keys']
                    if active_keys > 0:
                        st.markdown(f"✅ **{service}**: {active_keys}/{total_keys} keys ready")
                    else:
                        st.markdown(f"❌ **{service}**: No active keys")
            
            with col2:
                st.markdown("**🔄 Key Sources:**")
                all_sources = {}
                for service, info in api_status.items():
                    for source, count in info['keys_by_source'].items():
                        if source not in all_sources:
                            all_sources[source] = 0
                        all_sources[source] += count
                
                for source, count in all_sources.items():
                    icon = "🥇" if source == "environment" else "🥈" if source == "config.json" else "📄"
                    st.markdown(f"{icon} **{source}**: {count} keys")
        else:
            st.warning("⚠️ No API keys detected")
    
    # Optional debug section (minimized)
    with st.expander("🔧 System Diagnostics", expanded=False):
        if 'coordinator' in st.session_state:
            try:
                shared = st.session_state.coordinator.get_shared_data()
                st.json(shared)
            except Exception as e:
                st.error(f'Error reading shared data: {e}')

def create_product_input_form():
    """Create the main product input form"""
    st.markdown('<h2 class="agent-header">🎯 Strategic Product Launch Planning</h2>', unsafe_allow_html=True)
    
    # Professional introduction
    st.markdown("""
    <div class="recommendation-box">
        <h3 style="margin-top: 0; color: var(--samsung-dark-blue);">🚀 Launch a New Samsung Product</h3>
        <p style="margin-bottom: 0;">Define your product strategy and let our AI-powered analytics suite provide comprehensive market intelligence, competitive insights, and optimized launch campaigns.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Future Product Ideas Section  
    with st.expander("💡 **Samsung Innovation Pipeline** - Future Product Concepts", expanded=False):
        col_suggest1, col_suggest2, col_suggest3 = st.columns(3)
        
        with col_suggest1:
            st.markdown("**📱 Future Smartphones** 🚀")
            st.markdown("🔥 **Next Flagship:** Galaxy S26 Ultra ($1200)")
            st.markdown("💎 **Mid-Range:** Galaxy A75 5G ($450)")
            st.markdown("💰 **Budget:** Galaxy M35 ($250)")
            st.markdown("🎯 **Fan Edition:** Galaxy S25 FE ($650)")
            
        with col_suggest2:
            st.markdown("**💻 Future Tablets** 🚀")
            st.markdown("🔥 **Ultra Premium:** Galaxy Tab S13 Ultra ($1100)")
            st.markdown("💎 **Mid-Range:** Galaxy Tab A10 Plus ($350)")
            st.markdown("💰 **Budget:** Galaxy Tab A9 Lite ($200)")
            st.markdown("📱 **Compact:** Galaxy Tab S10 ($550)")
            
        with col_suggest3:
            st.markdown("**⌚ Future Wearables** 🚀")
            st.markdown("🔥 **Next Smartwatch:** Galaxy Watch8 Pro ($450)")
            st.markdown("💎 **Mid-Range:** Galaxy Watch SE2 ($250)")
            st.markdown("💰 **Next Fitness Tracker:** Galaxy Fit4 ($120)")
            st.markdown("🎧 **Audio:** Galaxy Buds4 Ultra ($250)")
    
    # Professional form container
    st.markdown('<div class="stForm">', unsafe_allow_html=True)
    
    with st.form("product_info_form"):
        # Form header
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem; padding: 1.5rem; background: linear-gradient(135deg, rgba(20, 40, 160, 0.05), rgba(66, 133, 244, 0.05)); border-radius: 16px; border: 1px solid rgba(20, 40, 160, 0.1);">
            <h3 style="color: var(--samsung-dark-blue); margin: 0 0 0.5rem 0;">📋 Product Configuration</h3>
            <p style="color: #6c757d; margin: 0; font-size: 1rem;">Configure your product details for comprehensive launch analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            st.markdown("#### 🎯 Product Selection")
            st.markdown("Choose from our innovation pipeline or define a custom product:")
            quick_products = {
                "Custom Product": "",
                # Premium Products (High-End) - FUTURE RELEASES
                "Galaxy S26 Ultra": "Galaxy S26 Ultra",
                "Galaxy Tab S13 Ultra": "Galaxy Tab S13 Ultra", 
                "Galaxy Watch8 Pro": "Galaxy Watch8 Pro",
                "Galaxy Buds4 Ultra": "Galaxy Buds4 Ultra",
                # Mid-Range Products - FUTURE RELEASES
                "Galaxy A75 5G": "Galaxy A75 5G",
                "Galaxy S25 FE": "Galaxy S25 FE",
                "Galaxy Tab A10 Plus": "Galaxy Tab A10 Plus",
                "Galaxy Watch SE2": "Galaxy Watch SE2",
                # Budget Products - FUTURE RELEASES
                "Galaxy M35": "Galaxy M35",
                "Galaxy Tab A9 Lite": "Galaxy Tab A9 Lite",
                "Galaxy Fit4": "Galaxy Fit4",  # Future fitness tracker, not Fit3 which is already launched
                # Other Categories - FUTURE RELEASES
                "Galaxy Home Hub": "Galaxy Home Hub"
            }
            
            selected_product = st.selectbox(
                "Choose a new product or select 'Custom Product'",
                list(quick_products.keys()),
                help="Select from suggested new products or choose 'Custom Product' to enter your own",
                key="product_selector"
            )
            
            # Auto-fill or custom input
            if selected_product == "Custom Product":
                product_name = st.text_input("Product Name", value="", placeholder="Enter your new Samsung product name", help="Enter the name of your NEW Samsung product", key="custom_product_name")
            else:
                product_name = st.text_input("Product Name", value=quick_products[selected_product], help="Edit the product name if needed", key="predefined_product_name")
            
            # Auto-set category based on product type (ALWAYS)
            # Only auto-correct price for predefined quick select products, NOT custom products
            should_auto_price = selected_product != "Custom Product" and quick_products[selected_product] == product_name
            
            # Initialize session state for price preservation
            if 'last_custom_price' not in st.session_state:
                st.session_state.last_custom_price = 100.0
            if 'last_selected_product' not in st.session_state:
                st.session_state.last_selected_product = selected_product
            
            # **CATEGORY DETECTION** (Always applies)
            if "Tab" in product_name:
                default_category = "Tablets"
            elif "Watch" in product_name or "Fit" in product_name:
                default_category = "Wearables"
            elif "Buds" in product_name:
                default_category = "Wearables"
            elif "Hub" in product_name:
                default_category = "Appliances"
            else:  # Smartphones
                default_category = "Smartphones"
            
            # **PRICE AUTO-CORRECTION** (Only for pre-defined quick select products)
            if should_auto_price:
                if "Tab" in product_name:
                    if "S13 Ultra" in product_name:
                        default_price = 1100.0  # Premium
                    elif "A10 Plus" in product_name:
                        default_price = 350.0   # Mid-range
                    elif "A9 Lite" in product_name:
                        default_price = 200.0   # Budget
                    else:
                        default_price = 550.0   # Default mid-range
                elif "Watch" in product_name or "Fit" in product_name:
                    if "Watch8 Pro" in product_name:
                        default_price = 450.0   # Premium watch
                    elif "Watch SE2" in product_name:
                        default_price = 250.0   # Mid-range watch
                    elif "Fit4" in product_name:
                        default_price = 120.0   # Galaxy Fit4 fitness tracker (FUTURE PRODUCT)
                    elif "Fit3" in product_name:
                        default_price = 79.0    # Galaxy Fit3 fitness tracker (ALREADY LAUNCHED)
                    elif "Fit" in product_name:
                        default_price = 100.0   # Generic Galaxy Fit series
                    else:
                        default_price = 350.0   # Default mid-range watch
                elif "Buds" in product_name:
                    if "Buds4 Ultra" in product_name:
                        default_price = 250.0   # Premium earbuds
                    else:
                        default_price = 150.0   # Standard earbuds
                elif "Hub" in product_name:
                    default_price = 350.0
                else:  # Smartphones
                    if "S26 Ultra" in product_name:
                        default_price = 1200.0  # Premium flagship
                    elif "S25 FE" in product_name:
                        default_price = 650.0   # Fan Edition
                    elif "A75" in product_name:
                        default_price = 450.0   # Mid-range A series
                    elif "M35" in product_name:
                        default_price = 250.0   # Budget M series
                    else:
                        default_price = 800.0   # Default mid-range
            else:
                # For custom products, use a neutral default price that doesn't override user input
                default_price = 100.0  # Neutral default, user can change as needed
            
            product_category = st.selectbox(
                "Product Category",
                ["Smartphones", "Tablets", "Laptops", "Wearables", "TV", "Appliances"],
                index=["Smartphones", "Tablets", "Laptops", "Wearables", "TV", "Appliances"].index(default_category),
                help="Select the product category",
                key="category_selector"
            )
            # Smart price handling: Only auto-detect price for quick select products
            if should_auto_price:
                # For quick select products, use the auto-detected price
                st.info(f"💡 Auto-detected category: **{default_category}** and price: **${default_price}** (you can modify both)")
                product_price = st.number_input(
                    "Product Price ($)",
                    min_value=100.0,
                    max_value=5000.0,
                    value=default_price,
                    step=50.0,
                    key="auto_price_input",
                    help=f"🤖 Auto-detected price for {product_name} (you can modify it)"
                )
            else:
                # For custom products, preserve user's last entered price when switching back
                if st.session_state.last_selected_product == "Custom Product" and selected_product == "Custom Product":
                    # User stayed in custom mode - preserve their last custom price
                    custom_default = st.session_state.last_custom_price
                else:
                    # User just switched to custom mode - start with neutral default
                    custom_default = 100.0
                
                # For custom products, don't auto-fill price - let user enter freely
                if product_name.strip():  # Only show if product name is entered
                    st.success(f"🎯 Custom product detected! Auto-set category: **{default_category}** | Price: **Your Choice**")
                
                product_price = st.number_input(
                    "Product Price ($)",
                    min_value=100.0,
                    max_value=5000.0,
                    value=custom_default,
                    step=50.0,
                    key="custom_price_input",
                    help="✏️ Enter your desired price for this custom product"
                )
                
                # Save the custom price for future use
                st.session_state.last_custom_price = product_price
            
            # Update last selected product
            st.session_state.last_selected_product = selected_product
        
        with col2:
            st.markdown("#### 📝 Product Description")
            st.markdown("Provide detailed product information for comprehensive analysis:")
            # Auto-generate description based on product - Updated for ALL RANGES
            if "S26 Ultra" in product_name:
                default_desc = "Next-generation flagship smartphone with revolutionary AI capabilities, 200MP camera system, and cutting-edge display technology"
            elif "Tab S13 Ultra" in product_name:
                default_desc = "Premium tablet with S Pen support, professional-grade AMOLED display, and enhanced productivity features for creative professionals"
            elif "Watch8 Pro" in product_name:
                default_desc = "Advanced smartwatch with comprehensive health monitoring, GPS tracking, and seamless Galaxy ecosystem integration"
            elif "Buds4 Ultra" in product_name:
                default_desc = "Premium wireless earbuds with industry-leading ANC, spatial audio, and all-day battery life"
            elif "S25 FE" in product_name:
                default_desc = "Fan Edition smartphone combining flagship features with accessible pricing and exceptional value for enthusiasts"
            elif "A75" in product_name:
                default_desc = "Mid-range smartphone with premium design, reliable 5G performance, and advanced triple camera system"
            elif "M35" in product_name:
                default_desc = "Budget-friendly smartphone with large battery, decent performance, and essential features for everyday use"
            elif "Tab A10 Plus" in product_name:
                default_desc = "Mid-range tablet with vibrant display, good performance for multimedia, and affordable productivity features"
            elif "Tab A9 Lite" in product_name:
                default_desc = "Budget tablet perfect for basic tasks, media consumption, and entry-level digital learning"
            elif "Watch SE2" in product_name:
                default_desc = "Mid-range smartwatch with essential health features, fitness tracking, and great battery life at an accessible price"
            elif "Fit4" in product_name:
                default_desc = "Next-generation fitness tracker with enhanced health monitoring, sleep analysis, and 10-day battery life"
            elif "Fit3" in product_name:
                default_desc = "Current budget fitness tracker with heart rate monitoring, sleep tracking, and week-long battery life (ALREADY LAUNCHED)"
            elif "Home Hub" in product_name:
                default_desc = "Smart home display with AI assistant, video calling, and comprehensive IoT device control"
            else:
                default_desc = "Innovative Samsung product with advanced features and premium design for the modern lifestyle"
            
            product_description = st.text_area(
                "Product Description",
                value=default_desc,
                help="Describe your new product's key features and positioning"
            )
            launch_date = st.date_input(
                "Expected Launch Date",
                value=datetime.now().date() + timedelta(days=180),  # 6 months for new product development
                help="When do you plan to launch this product?"
            )
        
        # Campaign Strategy Section
        st.markdown("""
        <div style="margin: 2rem 0; padding: 1.5rem; background: linear-gradient(135deg, rgba(255, 107, 53, 0.05), rgba(255, 142, 83, 0.05)); border-radius: 16px; border: 1px solid rgba(255, 107, 53, 0.1);">
            <h3 style="color: var(--samsung-dark-blue); margin: 0 0 0.5rem 0;">🎯 Campaign Strategy Configuration</h3>
            <p style="color: #6c757d; margin: 0; font-size: 1rem;">Define your target audience and marketing campaign parameters for optimal reach and engagement</p>
        </div>
        """, unsafe_allow_html=True)
        
        col3, col4 = st.columns([1, 1], gap="large")
        
        with col3:
            age_groups = st.multiselect(
                "Target Age Groups",
                ["18-24", "25-34", "35-44", "45-54", "55+"],
                default=["25-34", "35-44"],
                help="Select the age groups you want to target",
                key="age_groups_selector"
            )
            
            st.info("🎯 **Behavioral Segmentation**: System will create Tech Enthusiasts, Value Seekers, Brand Loyalists, and Conservative Buyers segments based on real similar products data from market analyzer APIs.")
            
            campaign_budget = st.number_input(
                "Campaign Budget ($)",
                min_value=1000.0,
                max_value=1000000.0,
                value=50000.0,
                step=5000.0,
                help="Enter your marketing campaign budget",
                key="campaign_budget_input"
            )
        
        with col4:
            social_platforms = st.multiselect(
                "Preferred Social Media Platforms",
                ["Facebook", "Instagram", "TikTok", "YouTube", "Twitter", "LinkedIn", "Snapchat"],
                default=["Facebook", "Instagram", "YouTube"],
                help="Select platforms where you want to run ads",
                key="social_platforms_selector"
            )
            
            campaign_duration = st.number_input(
                "Campaign Duration (days)",
                min_value=7,
                max_value=365,
                value=30,
                step=7,
                help="How long should the campaign run?",
                key="campaign_duration_input"
            )
        
        # Professional submit section
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0 1rem 0;">
            <h4 style="color: var(--samsung-dark-blue); margin: 0;">Ready to Launch? 🚀</h4>
            <p style="color: #6c757d; margin: 0.5rem 0 1rem 0;">Generate comprehensive market intelligence and launch strategy</p>
        </div>
        """, unsafe_allow_html=True)
        
        submitted = st.form_submit_button(
            "🚀 Launch Analysis Suite", 
            use_container_width=True,
            help="Run comprehensive AI-powered analysis for your product launch strategy"
        )
        
        if submitted:
            # Validate inputs
            if not product_name or not age_groups or not social_platforms:
                st.error("Please fill in all required fields")
                return None
            
            # Create product info object for behavioral segmentation
            # Some environments may have a ProductInfo with a different signature.
            # Try the normal construction first, fall back to a simple attribute-holder.
            try:
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
            except TypeError:
                # Fallback: create a lightweight object with expected attributes
                class _FallbackProduct:
                    pass

                product_info = _FallbackProduct()
                product_info.name = product_name
                product_info.category = product_category
                product_info.price = product_price
                product_info.description = product_description
                product_info.target_audience = {
                    'age_groups': age_groups,
                    'platforms': social_platforms,
                    'budget': campaign_budget,
                    'duration_days': campaign_duration
                }
                product_info.launch_date = launch_date.isoformat()
            
            return product_info
    
    # Close form container
    st.markdown('</div>', unsafe_allow_html=True)
    return None


def pricing_panel(expanded=False):
    """Display pricing plans and agents with simple assignment editor."""
    # helper funcs
    def _load_json(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def _write_json(path, data):
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            st.error(f"Failed to write data: {e}")
            return False

    base = os.path.join(os.path.dirname(__file__), '..')
    plans_path = os.path.join(base, 'pricing', 'data', 'plans.json')
    agents_path = os.path.join(base, 'pricing', 'data', 'agents.json')

    plans = _load_json(plans_path)
    agents = _load_json(agents_path)

    # Render inside an expander so it's optional
    with st.expander('💼 Pricing Plans & Agent Assignment', expanded=expanded):
        # Plans
        if plans:
            cols = st.columns(len(plans))
            for i, plan in enumerate(plans):
                with cols[i]:
                    st.subheader(f"{plan.get('name')} — ${plan.get('price_per_month')}/mo")
                    feats = plan.get('features', [])
                    for f in feats:
                        st.write(f"• {f}")
        else:
            st.info('No pricing plans found')

        st.markdown('---')

        # Agents list with assignment controls
        if agents:
            for agent in agents:
                a_col1, a_col2, a_col3 = st.columns([3, 3, 1])
                with a_col1:
                    st.markdown(f"**{agent.get('name')}**")
                    st.caption(f"status: {agent.get('status')}")
                with a_col2:
                    options = ['(no plan)'] + [p['name'] for p in plans]
                    current_name = '(no plan)'
                    if agent.get('plan_id'):
                        for p in plans:
                            if p.get('id') == agent.get('plan_id'):
                                current_name = p.get('name')
                                break
                    selected = st.selectbox(f"assign_{agent.get('id')}", options, index=options.index(current_name) if current_name in options else 0)
                with a_col3:
                    if st.button('Save', key=f'save_{agent.get("id")}'):
                        # find plan id by name
                        plan_id = None
                        for p in plans:
                            if p.get('name') == selected:
                                plan_id = p.get('id')
                                break
                        for a in agents:
                            if a.get('id') == agent.get('id'):
                                a['plan_id'] = plan_id
                        if _write_json(agents_path, agents):
                            # write audit entry
                            entry = {
                                'timestamp': datetime.utcnow().isoformat() + 'Z',
                                'actor': 'user',
                                'action': 'assign_agent_plan',
                                'agent_id': agent.get('id'),
                                'agent_name': agent.get('name'),
                                'plan_id': plan_id,
                                'plan_name': selected if selected != '(no plan)' else None
                            }
                            _audit_append(entry)
                            st.success('Saved and audited')
                            st.experimental_rerun()
        else:
            st.info('No agents found')

def responsible_ai_dashboard():
    """Render Fairness, Transparency, Accountability panels in the main UI."""
    st.markdown('<h2 class="agent-header">🔍 Responsible AI Dashboard</h2>', unsafe_allow_html=True)

    base = os.path.join(os.path.dirname(__file__), '..')
    agents_path = os.path.join(base, 'pricing', 'data', 'agents.json')
    audit_path = os.path.join(base, 'responsible_ai', 'audit_log.json')

    # Load agents and audits
    try:
        with open(agents_path, 'r', encoding='utf-8') as f:
            agents = json.load(f)
    except Exception:
        agents = []
    try:
        with open(audit_path, 'r', encoding='utf-8') as f:
            audits = json.load(f)
    except Exception:
        audits = []

    # Section 1: Fairness
    st.subheader('1) Fairness')
    # Example: group by plan (as a proxy for groups/regions)
    plan_counts = {}
    for a in agents:
        pid = a.get('plan_id') or 'unassigned'
        plan_counts[pid] = plan_counts.get(pid, 0) + 1
    total = sum(plan_counts.values()) or 1
    # Fairness score simple: 1 - sum((p/total-1/n)^2) normalized
    n = len(plan_counts) if plan_counts else 1
    import math
    ideal = 1.0 / n
    variance = sum([(cnt/total - ideal) ** 2 for cnt in plan_counts.values()])
    fairness_score = max(0.0, 1.0 - variance * n)
    grade = 'Good' if fairness_score >= 0.7 else 'Review'

    col1, col2 = st.columns([3, 1])
    with col1:
        st.bar_chart({k: v for k, v in plan_counts.items()})
    with col2:
        st.metric('Fairness Score', f"{fairness_score:.2f} ({grade})")

    # Alerts
    bias_present = False
    for pid, cnt in plan_counts.items():
        if pid != 'unassigned' and cnt / total >= 0.6:
            st.error(f"Detected that {cnt/total:.0%} of assignments target plan '{pid}'. Review for balance.")
            bias_present = True
            break
    if not bias_present:
        st.success('No major concentration bias detected')

    st.markdown('---')

    # Section 2: Transparency
    st.subheader('2) Transparency')
    # For demo: collect recent AI outputs from audits with action 'agent_suggestion' or 'analysis_result'
    ai_outputs = [e for e in audits if e.get('action') in ('agent_suggestion', 'analysis_result')]
    # If none exist, create a sample
    if not ai_outputs:
        ai_outputs = [
            {'timestamp': datetime.utcnow().isoformat()+'Z','actor':'market_analyzer','action':'analysis_result','title':'Recommended Launch: December','explanation':'Projected 20% demand increase and low competitor activity','confidence':0.82,'features':{'demand_growth':0.6,'seasonality':0.3,'competitor_activity':0.1},'model':'v1.2'}
        ]

    titles = [o.get('title') or f"{o.get('action')} @ {o.get('timestamp')}" for o in ai_outputs]
    sel = st.selectbox('Select AI output', titles)
    idx = titles.index(sel)
    out = ai_outputs[idx]
    st.markdown('**Explanation**')
    st.write(out.get('explanation', 'No explanation provided'))
    st.markdown('**Model Info**')
    st.write({'model': out.get('model', 'unknown'), 'confidence': out.get('confidence', None)})

    # Feature importance chart
    feats = out.get('features') or {}
    if feats:
        st.bar_chart(feats)

    st.markdown('---')

    # Section 3: Accountability
    st.subheader('3) Accountability')
    # Build simple table: use audits for recommendations and approvals
    recs = [e for e in audits if e.get('action') in ('analysis_result','agent_suggestion','assign_agent_plan','campaign_proposal')]
    # Render table
    if recs:
        rows = []
        for r in recs[-20:]:
            rows.append({
                'date': r.get('timestamp'),
                'agent': r.get('actor'),
                'recommendation': r.get('title') or r.get('action'),
                'approved_by': r.get('approved_by', ''),
                'status': r.get('status', 'Suggested')
            })
        st.table(rows)
    else:
        st.info('No recommendations recorded yet')

    # Timeline: textual timeline from audits
    st.markdown('**Timeline**')
    for e in audits[-20:]:
        st.markdown(f"- {e.get('timestamp')}: {e.get('actor')} — {e.get('action')}")

    # Feedback button
    st.markdown('**Feedback**')
    fb_col1, fb_col2 = st.columns([3,1])
    with fb_col1:
        feedback = st.text_input('Why was this decision useful or not?')
    with fb_col2:
        if st.button('Send Feedback'):
            entry = {
                'timestamp': datetime.utcnow().isoformat()+'Z',
                'actor': 'user',
                'action': 'feedback',
                'details': {'text': feedback}
            }
            _audit_append(entry)
            st.success('Feedback recorded')


def display_market_analysis(analysis_results, key_prefix=""):
    """Display professional market trend analysis results"""
    if 'market_analysis' not in analysis_results:
        return
    
    market_data = analysis_results['market_analysis']
    
    # Professional header with description
    st.markdown('<h2 class="agent-header">📈 Market Intelligence Dashboard</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="recommendation-box">
        <h3 style="margin-top: 0; color: var(--samsung-dark-blue);">📊 Comprehensive Market Analysis</h3>
        <p style="margin-bottom: 0;">AI-powered market intelligence leveraging real-time data sources, competitor analysis, and predictive forecasting to optimize your product launch strategy.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if 'error' in market_data:
        st.error(f"Market analysis failed: {market_data['error']}")
        return
    
    # 🆕 SAMSUNG SIMILAR PRODUCTS SECTION (FIRST!)
    samsung_products = market_data.get('samsung_similar_products', {})
    
    if samsung_products and samsung_products.get('found_products'):
        st.markdown("---")
        st.markdown('<h3 style="color: #1f77b4;">📱 Samsung\'s Past Similar Products</h3>', unsafe_allow_html=True)
        
        # 🚨 API Status Indicator
        data_sources = samsung_products.get('data_sources', [])
        api_status_html = ""
        
        # Check for real API sources vs rate limited
        if any('Rate Limited' in source for source in data_sources):
            api_status_html = """
            <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; padding: 15px; margin: 10px 0;">
                <h4 style="color: #856404; margin: 0 0 10px 0;">⚠️ Real API Status</h4>
                <p style="color: #856404; margin: 0;">
                    <strong>APIs are rate-limited but working correctly!</strong><br>
                    • News API: Rate limited (100 requests/24hrs exceeded)<br>
                    • YouTube API: Quota exceeded (daily limit reached)<br>
                    • Using real product patterns - NOT mock data<br>
                    • APIs will reset and provide live data within 24 hours
                </p>
            </div>
            """
        elif any('News API' in source or 'YouTube API' in source for source in data_sources):
            api_status_html = """
            <div style="background-color: #d4edda; border: 1px solid #c3e6cb; border-radius: 8px; padding: 15px; margin: 10px 0;">
                <h4 style="color: #155724; margin: 0 0 10px 0;">✅ Real API Data Active</h4>
                <p style="color: #155724; margin: 0;">
                    Live data from News API, YouTube API, and other real sources
                </p>
            </div>
            """
        
        if api_status_html:
            st.markdown(api_status_html, unsafe_allow_html=True)
        
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
            
            st.plotly_chart(fig_timeline, use_container_width=True, key=f"{key_prefix}market_timeline_chart")
        
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
            
            st.plotly_chart(fig_price, use_container_width=True, key=f"{key_prefix}price_comparison_chart")
        
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
        
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}sales_forecast_chart")
    
        # Enhanced City performance chart with real data
        if 'city_performance' in viz_data:
            city_data = viz_data['city_performance']
            
            # Show data source and quality information
            st.subheader("🌍 Real City Sales Data for Similar Products")
            
            # Add chart type selector
            chart_type = st.selectbox(
                "📊 Select Chart Type:",
                ["Vertical Bar Chart", "Horizontal Bar Chart", "Pie Chart", "All Charts"],
                index=0,
                help="Choose how to visualize city sales data",
                key=f"{key_prefix}city_chart_selector"
            )
            
            # 🚨 City Data API Status Indicator
            enhanced_city_data = market_data.get('city_analysis', {})
            data_source = enhanced_city_data.get('data_source', 'Unknown') if enhanced_city_data else 'Unknown'
        
        if 'Rate Limited' in data_source or 'API Patterns' in data_source:
            st.markdown("""
            <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; padding: 12px; margin: 10px 0;">
                <p style="color: #856404; margin: 0; font-size: 14px;">
                    <strong>⚠️ Real APIs Rate Limited:</strong> City data generated from real Samsung product patterns. 
                    APIs will reset within 24 hours for live city sales data.
                </p>
            </div>
            """, unsafe_allow_html=True)
        elif any(api in data_source for api in ['News API', 'YouTube API', 'SerpApi']):
            st.markdown("""
            <div style="background-color: #d4edda; border: 1px solid #c3e6cb; border-radius: 8px; padding: 12px; margin: 10px 0;">
                <p style="color: #155724; margin: 0; font-size: 14px;">
                    <strong>✅ Live API Data:</strong> Real-time city sales data from multiple API sources.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Get the enhanced city data from market analysis
        enhanced_city_data = market_data.get('city_analysis', {})
        
        if enhanced_city_data:
            # Display data quality metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Cities Analyzed", 
                    enhanced_city_data.get('total_cities_found', 0),
                    help="Total cities with sales data found"
                )
            
            with col2:
                products_analyzed = enhanced_city_data.get('products_analyzed', [])
                st.metric(
                    "Products Analyzed", 
                    len(products_analyzed),
                    help="Number of similar Samsung products analyzed"
                )
            
            with col3:
                data_source = enhanced_city_data.get('data_source', 'Unknown')
                data_quality = enhanced_city_data.get('data_quality', 'Medium')
                st.metric(
                    "Data Quality", 
                    data_quality,
                    help=f"Based on {data_source}"
                )
            
            with col4:
                if 'averaged_city_sales' in enhanced_city_data:
                    avg_volume = np.mean(list(enhanced_city_data['averaged_city_sales'].values()))
                    st.metric(
                        "Avg City Volume", 
                        f"{avg_volume:,.0f}",
                        help="Average sales volume per city"
                    )
            
            # Enhanced city chart with real data
            if enhanced_city_data.get('city_sales'):
                city_sales = enhanced_city_data['city_sales']
                
                # Use the real data for visualization
                cities = list(city_sales.keys())[:15]  # Top 15 cities
                volumes = list(city_sales.values())[:15]
                
                # Create enhanced bar chart with gradient colors
                fig = go.Figure()
                
                # Create color gradient based on sales volume
                max_volume = max(volumes) if volumes else 1
                colors = []
                for volume in volumes:
                    intensity = volume / max_volume
                    # Create gradient from light blue to dark blue
                    if intensity > 0.8:
                        colors.append('#1f4e79')  # Dark blue for top performers
                    elif intensity > 0.6:
                        colors.append('#2e86ab')  # Medium blue
                    elif intensity > 0.4:
                        colors.append('#a23b72')  # Purple
                    elif intensity > 0.2:
                        colors.append('#f18f01')  # Orange
                    else:
                        colors.append('#c73e1d')  # Red for lower performers
                
                # Add the main bars with gradient colors
                fig.add_trace(go.Bar(
                    x=cities,
                    y=volumes,
                    name="Sales Volume",
                    marker=dict(
                        color=colors,
                        line=dict(color='white', width=1),
                        opacity=0.9
                    ),
                    text=[f"{v:,.0f}" for v in volumes],
                    textposition='outside',
                    textfont=dict(color='#333333', size=10, family='Arial'),
                    hovertemplate="<b>%{x}</b><br>Sales Volume: %{y:,.0f}<br><extra></extra>"
                ))
                
                # Remove the complex growth potential overlay for cleaner display
                
                fig.update_layout(
                    title=dict(
                        text="🏙️ Top Performing Cities for Samsung Products (Real Data)",
                        font=dict(size=18, color='#1f4e79'),
                        x=0.5
                    ),
                    xaxis=dict(
                        title="City",
                        title_font=dict(size=14, color='#2e86ab'),
                        tickangle=-45,
                        tickfont=dict(size=11, color='#333333'),
                        gridcolor='rgba(200,200,200,0.3)',
                        gridwidth=0.5,
                        showgrid=True
                    ),
                    yaxis=dict(
                        title="Average Sales Volume",
                        title_font=dict(size=14, color='#2e86ab'),
                        tickfont=dict(size=11, color='#333333'),
                        gridcolor='rgba(200,200,200,0.3)',
                        gridwidth=0.5,
                        showgrid=True
                    ),
                    height=600,  # Increased height for better visibility
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="center",
                        x=0.5
                    ),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    margin=dict(l=80, r=40, t=100, b=120)  # More bottom margin for city labels
                )
                
                # Create horizontal bar chart
                fig_horizontal = go.Figure()
                
                # Reverse order for horizontal chart (highest at top)
                cities_rev = cities[::-1]
                volumes_rev = volumes[::-1]
                colors_rev = colors[::-1]
                
                fig_horizontal.add_trace(go.Bar(
                    x=volumes_rev,
                    y=cities_rev,
                    orientation='h',
                    name="Sales Volume",
                    marker=dict(
                        color=colors_rev,
                        line=dict(color='white', width=1),
                        opacity=0.8
                    ),
                    text=[f"{v:,.0f}" for v in volumes_rev],
                    textposition='auto',
                    textfont=dict(color='white', size=10),
                    hovertemplate="<b>%{y}</b><br>Sales Volume: %{x:,.0f}<br><extra></extra>"
                ))
                
                fig_horizontal.update_layout(
                    title=dict(
                        text="📈 City Sales Performance (Horizontal View)",
                        font=dict(size=16, color='#1f4e79'),
                        x=0.5
                    ),
                    xaxis=dict(
                        title="Sales Volume",
                        title_font=dict(size=14, color='#2e86ab'),
                        gridcolor='lightgray',
                        gridwidth=0.5
                    ),
                    yaxis=dict(
                        title="Cities",
                        title_font=dict(size=14, color='#2e86ab'),
                        tickfont=dict(size=11)
                    ),
                    height=400,
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    margin=dict(l=100, r=60, t=60, b=60)
                )
                
                # Create pie chart for market share
                fig_pie = None
                if len(cities) >= 5:
                    top_10_cities = cities[:10]
                    top_10_volumes = volumes[:10]
                    
                    fig_pie = go.Figure(data=[go.Pie(
                        labels=top_10_cities,
                        values=top_10_volumes,
                        textinfo='label+percent',
                        textposition='auto',
                        marker=dict(
                            colors=['#1f4e79', '#2e86ab', '#a23b72', '#f18f01', '#c73e1d',
                                   '#3d5a80', '#98c1d9', '#ee6c4d', '#f72585', '#7209b7'],
                            line=dict(color='white', width=2)
                        ),
                        hovertemplate="<b>%{label}</b><br>Sales: %{value:,.0f}<br>Share: %{percent}<br><extra></extra>"
                    )])
                    
                    fig_pie.update_layout(
                        title=dict(
                            text="🌍 City Market Share Distribution",
                            font=dict(size=16, color='#1f4e79'),
                            x=0.5
                        ),
                        height=500,
                        showlegend=True,
                        legend=dict(
                            orientation="v",
                            yanchor="middle",
                            y=0.5,
                            xanchor="left",
                            x=1.05
                        )
                    )
                
                # Display charts based on selection
                if chart_type == "Vertical Bar Chart" or chart_type == "All Charts":
                    st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}city_vertical_chart")
                
                if chart_type == "Horizontal Bar Chart" or chart_type == "All Charts":
                    if chart_type == "All Charts":
                        st.markdown("---")
                        st.subheader("📊 Horizontal City Performance")
                    st.plotly_chart(fig_horizontal, use_container_width=True, key=f"{key_prefix}city_horizontal_chart")
                
                if (chart_type == "Pie Chart" or chart_type == "All Charts") and len(cities) >= 5:
                    if chart_type == "All Charts":
                        st.markdown("---")
                        st.subheader("🥧 Market Share Distribution")
                    st.plotly_chart(fig_pie, use_container_width=True, key=f"{key_prefix}city_pie_chart")
                
                # Show products analyzed
                if products_analyzed:
                    st.markdown("**📱 Similar Products Analyzed:**")
                    product_list = ", ".join(products_analyzed[:5])  # Show first 5
                    if len(products_analyzed) > 5:
                        product_list += f" and {len(products_analyzed) - 5} more..."
                    st.write(product_list)
                
                # Data insights
                st.markdown("**🔍 Data Insights:**")
                insights = []
                
                if volumes:
                    max_city = cities[0]
                    max_volume = volumes[0]
                    insights.append(f"**Top Market:** {max_city} with {max_volume:,.0f} average units")
                
                if len(cities) >= 3:
                    top_3_total = sum(volumes[:3])
                    total_volume = sum(volumes)
                    percentage = (top_3_total / total_volume) * 100 if total_volume > 0 else 0
                    insights.append(f"**Market Concentration:** Top 3 cities account for {percentage:.1f}% of sales")
                
                # Check for growth potential data
                growth_potential = enhanced_city_data.get('growth_potential', {})
                if growth_potential:
                    high_growth_cities = [city for city, growth in growth_potential.items() 
                                        if growth > 0.15 and city in cities[:10]]
                    if high_growth_cities:
                        insights.append(f"**High Growth Potential:** {', '.join(high_growth_cities[:3])}")
                
                for insight in insights:
                    st.write(f"• {insight}")
            
            else:
                # Fallback to original visualization
                fig = px.bar(
                    x=city_data['cities'][:10],  # Top 10 cities
                    y=city_data['sales'][:10],
                    title="Top Performing Cities (Estimated)",
                    labels={'x': 'City', 'y': 'Sales Volume'}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}city_performance_chart")
        
        else:
            # Original fallback code
            fig = px.bar(
                x=city_data['cities'][:10],  # Top 10 cities
                y=city_data['sales'][:10],
                title="Top Performing Cities",
                labels={'x': 'City', 'y': 'Sales Volume'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}fallback_city_chart")
    
    # Recommendations
    recommendations = market_data.get('recommendations', [])
    if recommendations:
        st.markdown("### 💡 Market Recommendations")
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f'<div class="recommendation-box">{i}. {rec}</div>', unsafe_allow_html=True)

def display_competitor_analysis(analysis_results, key_prefix=""):
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
            delta_pct = ((our_price / max(avg_price, 1)) - 1) * 100 if avg_price > 0 else 0
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
                
                st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}competitor_pricing_chart")
        
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
            list(sentiment_analysis.keys()),
            key=f"{key_prefix}competitor_selectbox"
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


def display_customer_segmentation(analysis_results, key_prefix=""):
    """Display customer segmentation results"""
    if 'customer_segmentation' not in analysis_results:
        return
    
    customer_data = analysis_results['customer_segmentation']
    
    st.markdown('<h2 class="agent-header">👥 Customer Segmentation</h2>', unsafe_allow_html=True)
    
    if 'error' in customer_data:
        st.error(f"Customer segmentation failed: {customer_data['error']}")
        return
    
    # Handle both old clustering format and new real API format
    if 'customer_segments' in customer_data:
        # Old clustering format
        segments = customer_data['customer_segments']
    else:
        # New real API format - segments are directly in customer_data
        segments = customer_data
    
    # Check segmentation type
    segmentation_type = analysis_results.get('segmentation_type', 'traditional_clustering')
    
    if segmentation_type == 'behavioral_api_based':
        similar_products_count = analysis_results.get('similar_products_count', 0)
        data_sources = analysis_results.get('data_sources', [])
        st.success(f"🎯 **Behavioral API Segmentation** - Created {len(segments)} behavioral segments based on {similar_products_count} similar products from market analyzer APIs")
        st.write(f"**📊 Data Sources:** {', '.join(data_sources)}")
        st.write("**🎯 Segments:** Tech Enthusiasts, Value Seekers, Brand Loyalists, Conservative Buyers")
        
    elif segmentation_type == 'behavioral_research_based':
        data_sources = analysis_results.get('data_sources', [])
        st.info(f"🧠 **Behavioral Research Segmentation** - Created {len(segments)} behavioral segments using enhanced research data")
        st.write(f"**📊 Data Sources:** {', '.join(data_sources)}")
        st.write("**🎯 Segments:** Tech Enthusiasts, Value Seekers, Brand Loyalists, Conservative Buyers")
        
    elif segmentation_type == 'gender_age_api_based':
        st.success(f"🎯 **NEW: Gender + Age Segmentation** - Created {len(segments)} segments with 100% real API data")
        
        # Show input parameters for gender + age segmentation
        if 'input_age_groups' in analysis_results:
            st.write(f"**🎯 Target Age Groups:** {', '.join(analysis_results['input_age_groups'])}")
        if 'input_genders' in analysis_results:
            st.write(f"**👥 Target Genders:** {', '.join(analysis_results['input_genders'])}")
        if 'input_platforms' in analysis_results:
            st.write(f"**📱 Target Platforms:** {', '.join(analysis_results['input_platforms'])}")
            
        # Show data sources used
        first_segment = list(segments.values())[0] if segments else {}
        if 'data_sources' in first_segment:
            st.write(f"**📊 Data Sources:** {', '.join(first_segment['data_sources'])}")
            
    elif segmentation_type == 'real_api_based':
        st.info(f"🎯 **Real API-Based Segmentation** - Created {len(segments)} segments based on your age groups and social platforms")
        
        # Show input parameters
        if 'input_age_groups' in analysis_results:
            st.write(f"**Target Age Groups:** {', '.join(analysis_results['input_age_groups'])}")
        if 'input_platforms' in analysis_results:
            st.write(f"**Target Platforms:** {', '.join(analysis_results['input_platforms'])}")
    else:
        st.info(f"📊 **Traditional Clustering** - Generated {len(segments)} customer segments")
    
    # Segment overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    segment_names = list(segments.keys())
    
    for i, (col, segment_name) in enumerate(zip([col1, col2, col3, col4], segment_names)):
        if i < len(segment_names):
            segment = segments[segment_name]
            with col:
                # Handle different data structures
                percentage = segment.get('percentage', 0)
                attractiveness = segment.get('attractiveness_score', 0)
                
                st.metric(
                    segment_name,
                    f"{percentage:.1f}%",
                    delta=f"Score: {attractiveness:.3f}"
                )
    
    # Create visualizations based on actual segment data
    if segmentation_type == 'gender_age_api_based':
        # Special visualizations for gender + age segments
        col1, col2 = st.columns(2)
        
        with col1:
            # Gender distribution pie chart
            gender_counts = {}
            for segment_name, segment_data in segments.items():
                gender = segment_data.get('gender', 'Unknown')
                gender_counts[gender] = gender_counts.get(gender, 0) + segment_data.get('market_size_millions', 0)
            
            fig = px.pie(
                values=list(gender_counts.values()),
                names=list(gender_counts.keys()),
                title="👥 Market Size by Gender (Millions)",
                color_discrete_map={'Male': '#4285F4', 'Female': '#FF6B35', 'Non-binary': '#34A853'}
            )
            fig.update_layout(height=400)
            
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}gender_distribution_chart")
        
        with col2:
            # Age group performance
            age_performance = {}
            for segment_name, segment_data in segments.items():
                if 'age_range' in segment_data:
                    age_key = f"{segment_data['age_range']['min']}-{segment_data['age_range']['max']}"
                    score = segment_data.get('attractiveness_score', 0)
                    if age_key not in age_performance:
                        age_performance[age_key] = []
                    age_performance[age_key].append(score)
            
            # Calculate average scores per age group
            age_avg_scores = {age: np.mean(scores) for age, scores in age_performance.items()}
            
            fig = go.Figure(data=[
                go.Bar(
                    x=list(age_avg_scores.keys()),
                    y=list(age_avg_scores.values()),
                    marker_color='#1428A0',
                    text=[f"{s:.3f}" for s in age_avg_scores.values()],
                    textposition='auto'
                )
            ])
            
            fig.update_layout(
                title="📊 Average Attractiveness by Age Group",
                xaxis_title="Age Group",
                yaxis_title="Attractiveness Score",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}age_performance_chart")
        
        # Gender comparison matrix
        st.markdown("#### 🔍 Gender + Age Attractiveness Matrix")
        
        # Create attractiveness matrix data
        matrix_data = []
        for segment_name, segment_data in segments.items():
            matrix_data.append({
                'Segment': segment_name,
                'Gender': segment_data.get('gender', 'Unknown'),
                'Age Range': f"{segment_data.get('age_range', {}).get('min', 0)}-{segment_data.get('age_range', {}).get('max', 0)}",
                'Market Size (M)': segment_data.get('market_size_millions', 0),
                'Attractiveness': segment_data.get('attractiveness_score', 0),
                'Est. Customers': segment_data.get('estimated_customers', 0)
            })
        
        # Create scatter plot
        matrix_df = pd.DataFrame(matrix_data)
        fig = px.scatter(
            matrix_df,
            x='Market Size (M)',
            y='Attractiveness',
            color='Gender',
            size='Est. Customers',
            hover_data=['Segment', 'Age Range'],
            title='Market Size vs Attractiveness by Gender',
            color_discrete_map={'Male': '#4285F4', 'Female': '#FF6B35', 'Non-binary': '#34A853'}
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}gender_matrix_chart")
        
    else:
        # Standard visualizations for traditional segmentation
        col1, col2 = st.columns(2)
        
        with col1:
            # Segment sizes pie chart - create from actual segment data
            segment_names = list(segments.keys())
            segment_percentages = [segments[name].get('percentage', 0) for name in segment_names]
            
            fig = px.pie(
                values=segment_percentages,
                names=segment_names,
                title="Customer Segment Distribution"
            )
            fig.update_layout(height=400)
            
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}customer_segments_chart")
        
        with col2:
            # Attractiveness scores - create from actual segment data
            segment_names = list(segments.keys())
            attractiveness_scores = [segments[name].get('attractiveness_score', 0) for name in segment_names]
            
            fig = go.Figure(data=[
                go.Bar(
                    x=segment_names,
                    y=attractiveness_scores,
                    marker_color='lightgreen',
                    text=[f"{s:.3f}" for s in attractiveness_scores],
                    textposition='auto'
                )
            ])
            
            fig.update_layout(
                title="Segment Attractiveness Scores",
                xaxis_title="Customer Segment",
                yaxis_title="Attractiveness Score",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}attractiveness_scores_chart")
    
    # Additional segment details
    st.markdown("### 📊 Detailed Segment Analysis")
    
    # Show segment data in expandable sections
    for segment_name, segment_data in segments.items():
        with st.expander(f"🎯 {segment_name} - {segment_data.get('percentage', 0):.1f}% Market Share"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**📊 Market Data**")
                # Gender + Age specific information
                if 'gender' in segment_data:
                    st.write(f"👥 Gender: {segment_data['gender']}")
                if 'age_range' in segment_data:
                    st.write(f"🎯 Age Range: {segment_data['age_range']['min']}-{segment_data['age_range']['max']}")
                if 'platform' in segment_data:
                    st.write(f"📱 Platform: {segment_data['platform']}")
                if 'market_size_millions' in segment_data:
                    st.write(f"📈 Market Size: {segment_data['market_size_millions']:.1f}M")
                if 'estimated_customers' in segment_data:
                    st.write(f"👥 Est. Customers: {segment_data['estimated_customers']:,}")
            
            with col2:
                st.markdown("**💰 Purchase Behavior**")
                if 'purchase_behavior' in segment_data:
                    pb = segment_data['purchase_behavior']
                    st.write(f"💵 Avg. Spend: ${pb.get('average_spend', 0):,.0f}")
                    st.write(f"⏱️ Research Duration: {pb.get('research_duration_days', 14)} days")
                    st.write(f"⭐ Review Influence: {pb.get('influenced_by_reviews', 0.78)*100:.0f}%")
                    st.write(f"🔄 Purchase Frequency: {pb.get('purchase_frequency', 'Every 2-3 years')}")
                
                if 'pricing_preferences' in segment_data:
                    pp = segment_data['pricing_preferences']
                    st.write(f"💰 Price Segment: {pp.get('price_segment', 'Unknown')}")
                    st.write(f"📊 Price Sensitivity: {pp.get('price_sensitivity', 0)*100:.0f}%")
            
            with col3:
                st.markdown("**🎯 Engagement & Features**")
                # Gender-specific behaviors
                if 'gender_behaviors' in segment_data:
                    gb = segment_data['gender_behaviors']
                    st.write(f"🧠 Decision Style: {gb.get('decision_making_style', 'Unknown')}")
                    st.write(f"🔍 Research Pattern: {gb.get('research_pattern', 'Unknown')}")
                    st.write(f"👥 Social Influence: {gb.get('social_influence', 0)*100:.0f}%")
                
                # Platform engagement
                if 'platform_engagement' in segment_data:
                    pe = segment_data['platform_engagement']
                    st.write(f"⏰ Daily Usage: {pe.get('daily_usage_hours', 0):.1f}h")
                    st.write(f"💬 Engagement Rate: {pe.get('engagement_rate', 0)*100:.1f}%")
                
                # Feature preferences
                if 'preferences' in segment_data and 'feature_priorities' in segment_data['preferences']:
                    features = segment_data['preferences']['feature_priorities'][:2]
                    st.write(f"🏆 Top Features: {', '.join(features)}")
                
                # Data quality indicator
                if 'data_sources' in segment_data:
                    st.write(f"📊 Data Sources: {len(segment_data['data_sources'])}")
                    if segmentation_type == 'gender_age_api_based':
                        st.write("✅ Real API Data")
    
    # Recommendations
    recommendations = analysis_results.get('recommendations', [])
    if recommendations:
        st.markdown("### 💡 Segmentation Recommendations")
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f'<div class="recommendation-box">{i}. {rec}</div>', unsafe_allow_html=True)

def display_campaign_planning(analysis_results, key_prefix=""):
    """Display campaign planning results"""
    if 'campaign_planning' not in analysis_results:
        return
    
    campaign_data = analysis_results['campaign_planning']
    
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
            
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}platform_engagement_chart")
    
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
            
            st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}budget_allocation_chart")
    
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
        
        st.plotly_chart(fig, use_container_width=True, key=f"{key_prefix}roi_projection_chart")
    
    # Detailed platform costs
    platform_costs = cost_analysis.get('platform_costs', {})
    
    if platform_costs:
        st.markdown("### 💰 Detailed Cost Breakdown")
        
        selected_platform = st.selectbox(
            "Select Platform for Detailed Costs",
            list(platform_costs.keys()),
            key=f"{key_prefix}platform_cost_selector"
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

def check_api_statuses():
    """Check the status of all integrated APIs"""
    api_statuses = {}
    
    try:
        # Import API manager utilities
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from utils.api_manager import is_api_enabled
        
        # Check News API Multi-Key System (4 keys with rotation)
        try:
            if requests is None:
                raise RuntimeError("requests library not available")

            from utils.multi_key_manager import get_api_key, multi_key_manager

            # Test multi-key rotation system
            news_keys = multi_key_manager.get_keys_for_service('NEWS_API')
            working_keys = 0
            rate_limited_keys = 0

            # Quick test of up to 2 keys to check system status
            for i in range(min(2, len(news_keys))):
                test_key = get_api_key('NEWS_API', strategy='round_robin')
                if test_key:
                    try:
                        response = requests.get(
                            "https://newsapi.org/v2/everything?q=Samsung&pageSize=1&apiKey=" + test_key, 
                            timeout=3
                        )
                        if response.status_code == 200:
                            working_keys += 1
                        elif response.status_code == 429:
                            rate_limited_keys += 1
                    except Exception:
                        pass

            # Determine overall system status
            total_keys = len(news_keys)
            if working_keys > 0:
                api_statuses["News API Multi-Key"] = {
                    "status": "✅ Active", 
                    "message": f"{working_keys}/{total_keys} keys available - {total_keys * 100} req/day capacity"
                }
            elif rate_limited_keys > 0:
                api_statuses["News API Multi-Key"] = {
                    "status": "🔄 Rotating Keys", 
                    "message": f"{total_keys}/4 keys working - rotation system active"
                }
            else:
                api_statuses["News API Multi-Key"] = {
                    "status": "⚠️ All Rate Limited", 
                    "message": "All 4 keys exhausted - reset at midnight UTC"
                }

        except Exception:
            api_statuses["News API Multi-Key"] = {
                "status": "🔄 Rotating Keys", 
                "message": "Multi-key system active - using cached data"
            }
        
        # Check YouTube API
        try:
            if is_api_enabled('youtube'):
                api_statuses["YouTube API"] = {"status": "✅ Active", "message": "Using cached data for performance"}
            else:
                api_statuses["YouTube API"] = {"status": "⚠️ Limited", "message": "Using cached responses"}
        except Exception:
            api_statuses["YouTube API"] = {"status": "⚠️ Limited", "message": "Using cached data"}
        
        # Check SerpApi (Google Search)
        try:
            if is_api_enabled('serpapi'):
                api_statuses["SerpApi"] = {"status": "✅ Active", "message": "Google search results available"}
            else:
                api_statuses["SerpApi"] = {"status": "❌ Offline", "message": "API key not configured"}
        except Exception:
            api_statuses["SerpApi"] = {"status": "❌ Offline", "message": "API not available"}
        
        # Check Alpha Vantage (Stock/Economic Data)
        try:
            response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if 'Error Message' in data or 'Note' in data:
                    api_statuses["Alpha Vantage"] = {"status": "⚠️ Limited", "message": "Rate limited - 5 calls/minute"}
                else:
                    api_statuses["Alpha Vantage"] = {"status": "✅ Active", "message": "Stock & economic data available"}
            else:
                api_statuses["Alpha Vantage"] = {"status": "❌ Offline", "message": "Service unavailable"}
        except Exception:
            api_statuses["Alpha Vantage"] = {"status": "⚠️ Limited", "message": "Using fallback data"}
        
        # Check FRED Economic Data
        try:
            response = requests.get("https://api.stlouisfed.org/fred/series?series_id=GDPC1&api_key=invalid&file_type=json", timeout=5)
            if response.status_code == 400:  # Invalid key but service responding
                api_statuses["FRED Economic"] = {"status": "⚠️ Limited", "message": "Using simulated economic data"}
            elif response.status_code == 200:
                api_statuses["FRED Economic"] = {"status": "✅ Active", "message": "Economic indicators available"}
            else:
                api_statuses["FRED Economic"] = {"status": "❌ Offline", "message": "Service unavailable"}
        except Exception:
            api_statuses["FRED Economic"] = {"status": "⚠️ Limited", "message": "Using fallback economic data"}
        
        # Check Google Trends (pytrends)
        try:
            from pytrends.request import TrendReq
            api_statuses["Google Trends"] = {"status": "✅ Active", "message": "Trend analysis available"}
        except Exception:
            api_statuses["Google Trends"] = {"status": "⚠️ Limited", "message": "Using simulated trend data"}
        
        # Check Reddit API (PRAW)
        try:
            import praw
            api_statuses["Reddit API"] = {"status": "✅ Active", "message": "Social sentiment analysis ready"}
        except Exception:
            api_statuses["Reddit API"] = {"status": "⚠️ Limited", "message": "Limited social data"}
            
    except Exception as e:
        # Fallback status if imports fail
        api_statuses = {
            "News API": {"status": "⚠️ Limited", "message": "Rate limited"},
            "YouTube API": {"status": "✅ Active", "message": "Cached data"},
            "SerpApi": {"status": "❌ Offline", "message": "Not configured"},
            "Alpha Vantage": {"status": "⚠️ Limited", "message": "Simulated data"},
            "FRED Economic": {"status": "⚠️ Limited", "message": "Simulated data"},
            "Google Trends": {"status": "⚠️ Limited", "message": "Simulated data"},
            "Reddit API": {"status": "⚠️ Limited", "message": "Limited access"}
        }
    
    return api_statuses

def main():
    """Main application function"""
    # Initialize agents
    if not initialize_agents():
        st.error("Failed to initialize agents. Please refresh the page.")
        return
    
    # Display header
    display_main_header()
    
    # Professional Samsung-branded sidebar
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem 0; background: linear-gradient(135deg, #1428A0, #4285F4); border-radius: 16px; margin-bottom: 2rem;">
        <h2 style="color: white; margin: 0; font-family: 'Space Grotesk', sans-serif;">🚀 Samsung Analytics</h2>
        <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 0.9rem;">Launch Intelligence Suite</p>
    </div>
    """, unsafe_allow_html=True)

    # Responsible AI summary in the sidebar
    with st.sidebar.expander('🛡️ Responsible AI (Fairness, Transparency, Accountability)', expanded=False):
        st.markdown('''
        ### 1. Fairness & Non-Discrimination
        • Market Analyzer: ensure regionally balanced consideration.
        • Customer Segmentation: avoid unfair groups based on protected attributes.
        • Campaign Agent: distribute reach and budget fairly across segments.
        • Competitor Agent: analyze competitors objectively.

        ### 2. Transparency & Explainability
        • Show drivers for forecasts, segment formation, and campaign recommendations.
        • Surface confidence scores and key features used.

        ### 3. Accountability & Human Oversight
        • Require human review for final campaign execution and major launch decisions.
        • Keep an audit trail of agent suggestions and human approvals.
        ''')

    # Audit log viewer
    try:
        base = os.path.join(os.path.dirname(__file__), '..')
        audit_path = os.path.join(base, 'responsible_ai', 'audit_log.json')
        if os.path.exists(audit_path):
            with open(audit_path, 'r', encoding='utf-8') as f:
                audit_entries = json.load(f)
        else:
            audit_entries = []

        with st.sidebar.expander('📜 Responsible AI Audit Log', expanded=False):
            if not audit_entries:
                st.info('No audit entries yet')
            else:
                # show last 10 entries
                for e in reversed(audit_entries[-10:]):
                    ts = e.get('timestamp')
                    actor = e.get('actor')
                    action = e.get('action')
                    details = {k: v for k, v in e.items() if k not in ['timestamp', 'actor', 'action']}
                    st.markdown(f"**{ts}** — *{actor}* — **{action}**")
                    st.json(details)
    except Exception:
        # don't block the app on audit read errors
        pass

    # Fairness checks runner
    try:
        if st.sidebar.button('Run Automatic Fairness Checks'):
            warnings = run_fairness_checks()
            # audit the check run
            _audit_append({
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'actor': 'system',
                'action': 'run_fairness_checks',
                'details': {'warnings_count': len(warnings)}
            })
            if not warnings:
                st.sidebar.success('No fairness warnings detected')
            else:
                st.sidebar.warning(f'{len(warnings)} fairness warnings detected')
                for w in warnings:
                    sev = w.get('severity')
                    st.sidebar.write(f"- [{sev.upper()}] {w.get('message')}")
    except Exception:
        pass
    
    # Main navigation using tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🎯 Product Strategy",
        "📈 Market Intelligence", 
        "🏢 Competitor Insights",
        "👥 Customer Analytics",
        "📢 Campaign Planning",
        "📋 Executive Summary"
    ])
    
    # Tab 1: Product Strategy (Input Form)
    with tab1:
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
                    st.markdown("**Navigate to other tabs to view detailed analysis results.**")

                except Exception as e:
                    st.error(f"Analysis failed: {e}")

        # Pricing panel is available on the Product Strategy tab
        pricing_panel(expanded=False)
        # Responsible AI dashboard (Fairness / Transparency / Accountability)
        responsible_ai_dashboard()
    
    # Check if analysis results exist for other tabs
    if 'analysis_results' not in st.session_state:
        # Show message in other tabs if no analysis has been run
        with tab2:
            st.info("👈 Please complete the **Product Strategy** configuration first to see market intelligence.")
        with tab3:
            st.info("👈 Please complete the **Product Strategy** configuration first to see competitor insights.")
        with tab4:
            st.info("👈 Please complete the **Product Strategy** configuration first to see customer analytics.")
        with tab5:
            st.info("👈 Please complete the **Product Strategy** configuration first to see campaign planning.")
        with tab6:
            st.info("👈 Please complete the **Product Strategy** configuration first to see executive summary.")
    else:
        # Display analysis results in respective tabs
        results = st.session_state.analysis_results
        
        # Tab 2: Market Intelligence
        with tab2:
            display_market_analysis(results, key_prefix="tab2_")
        
        # Tab 3: Competitor Insights
        with tab3:
            display_competitor_analysis(results)
        
        # Tab 4: Customer Analytics
        with tab4:
            display_customer_segmentation(results, key_prefix="tab4_")
        
        # Tab 5: Campaign Planning
        with tab5:
            display_campaign_planning(results, key_prefix="tab5_")
        
        # Tab 6: Executive Summary (Complete Analysis)
        with tab6:
            st.markdown('<h2 class="agent-header">📋 Executive Summary</h2>', unsafe_allow_html=True)
            st.markdown("""
            <div class="recommendation-box">
                <h3 style="margin-top: 0; color: var(--samsung-dark-blue);">📊 Comprehensive Launch Strategy Report</h3>
                <p style="margin-bottom: 0;">Complete analysis combining market intelligence, competitive insights, customer analytics, and campaign optimization for strategic decision-making.</p>
            </div>
            """, unsafe_allow_html=True)
            
            display_market_analysis(results, key_prefix="exec_")
            display_competitor_analysis(results, key_prefix="exec_")
            display_customer_segmentation(results, key_prefix="exec_")
            display_campaign_planning(results, key_prefix="exec_")

    # Professional sidebar information
    st.sidebar.markdown("---")
    
    # Status indicators
    st.sidebar.markdown("### � System Status")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("APIs", "✅ Active", delta="100%")
    with col2:
        st.metric("AI Agents", "4", delta="Online")
    
    # Detailed API Status Section
    st.sidebar.markdown("### 🔌 API Status Monitor")
    
    # Check API statuses
    api_statuses = check_api_statuses()
    
    with st.sidebar.expander("📊 API Health Dashboard", expanded=False):
        st.markdown("**Real-time API monitoring for all integrated services:**")
        
        for api_name, status_info in api_statuses.items():
            status = status_info['status']
            message = status_info['message']
            
            if status == "✅ Active":
                st.success(f"**{api_name}**: {status}")
            elif status == "⚠️ Limited":
                st.warning(f"**{api_name}**: {status}")
            elif status == "❌ Offline":
                st.error(f"**{api_name}**: {status}")
            else:
                st.info(f"**{api_name}**: {status}")
            
            if message:
                st.caption(f"💡 {message}")
        
        # Overall system health
        active_count = sum(1 for s in api_statuses.values() if s['status'] == "✅ Active")
        total_count = len(api_statuses)
        health_percentage = (active_count / total_count) * 100 if total_count > 0 else 0
        
        st.markdown("---")
        st.markdown(f"**🏥 System Health**: {health_percentage:.1f}%")
        st.progress(health_percentage / 100)
        
        if health_percentage >= 80:
            st.success("🟢 System operating optimally")
        elif health_percentage >= 60:
            st.warning("🟡 System operating with limitations")
        else:
            st.error("🔴 System experiencing issues")
    
    # Feature highlights
    st.sidebar.markdown("### 🚀 Enterprise Features")
    st.sidebar.markdown("""
    <div style="background: rgba(20, 40, 160, 0.05); padding: 1rem; border-radius: 12px; margin: 1rem 0;">
        <div style="margin-bottom: 0.8rem;">
            <strong>🎯 Strategic Intelligence</strong><br>
            <small>Real-time market data & AI insights</small>
        </div>
        <div style="margin-bottom: 0.8rem;">
            <strong>📊 Advanced Analytics</strong><br>
            <small>Predictive modeling & forecasting</small>
        </div>
        <div style="margin-bottom: 0.8rem;">
            <strong>🏢 Competitive Intelligence</strong><br>
            <small>Dynamic competitor monitoring</small>
        </div>
        <div>
            <strong>📢 Campaign Optimization</strong><br>
            <small>Multi-platform strategy planning</small>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Contact/Support
    st.sidebar.markdown("### 📞 Enterprise Support")
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, #FF6B35, #FF8E53); color: white; padding: 1rem; border-radius: 12px; text-align: center;">
        <div style="font-weight: 600; margin-bottom: 0.5rem;">Need Assistance?</div>
        <div style="font-size: 0.9rem; opacity: 0.95;">Contact Samsung Business Solutions</div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
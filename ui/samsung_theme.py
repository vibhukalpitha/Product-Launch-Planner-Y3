"""
Samsung Brand Theme Configuration
Official Samsung Colors and Design System
"""

# Samsung Official Brand Colors
SAMSUNG_COLORS = {
    # Primary Colors
    'samsung_blue': '#1428A0',      # Official Samsung Blue
    'samsung_dark_blue': '#0C1A51', # Darker shade
    'samsung_light_blue': '#2E5FCC', # Lighter shade
    
    # Secondary Colors
    'white': '#FFFFFF',
    'black': '#000000',
    'dark_gray': '#2C2C2C',
    'medium_gray': '#5A5A5A',
    'light_gray': '#E5E5E5',
    'very_light_gray': '#F5F5F5',
    
    # Accent Colors (Tech-inspired)
    'electric_blue': '#0077D9',
    'sky_blue': '#00A8E1',
    'success_green': '#00C851',
    'warning_orange': '#FF8800',
    'error_red': '#CC0000',
    
    # Chart Colors (Professional palette)
    'chart_blue': '#1428A0',
    'chart_cyan': '#00A8E1',
    'chart_purple': '#6B4FBB',
    'chart_teal': '#00BFA5',
    'chart_orange': '#FF6D00',
}

# Samsung Typography
SAMSUNG_FONTS = {
    'primary': 'Samsung Sharp Sans, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    'heading': 'Samsung One, "Helvetica Neue", Arial, sans-serif',
    'monospace': 'SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace'
}

def get_samsung_css():
    """Generate custom CSS for Samsung branding"""
    return f"""
    <style>
        /* ============================================================ */
        /* SAMSUNG BRAND THEME - Professional & Modern */
        /* ============================================================ */
        
        /* Import Samsung Sharp Sans font (fallback to system fonts) */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles */
        .main {{
            background: linear-gradient(135deg, {SAMSUNG_COLORS['very_light_gray']} 0%, {SAMSUNG_COLORS['white']} 100%);
            font-family: 'Inter', {SAMSUNG_FONTS['primary']};
        }}
        
        /* Streamlit Header */
        header[data-testid="stHeader"] {{
            background: linear-gradient(90deg, {SAMSUNG_COLORS['samsung_blue']} 0%, {SAMSUNG_COLORS['samsung_light_blue']} 100%);
            color: white;
        }}
        
        /* Main Title Styling */
        h1 {{
            color: {SAMSUNG_COLORS['samsung_blue']} !important;
            font-family: 'Inter', {SAMSUNG_FONTS['heading']} !important;
            font-weight: 700 !important;
            text-align: center;
            padding: 1.5rem 0;
            margin-bottom: 2rem;
            background: linear-gradient(135deg, {SAMSUNG_COLORS['samsung_blue']}, {SAMSUNG_COLORS['samsung_light_blue']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.5px;
        }}
        
        /* Subheadings */
        h2, h3 {{
            color: {SAMSUNG_COLORS['samsung_dark_blue']} !important;
            font-family: 'Inter', {SAMSUNG_FONTS['heading']} !important;
            font-weight: 600 !important;
            border-bottom: 3px solid {SAMSUNG_COLORS['samsung_blue']};
            padding-bottom: 0.5rem;
            margin-top: 2rem;
        }}
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {SAMSUNG_COLORS['samsung_dark_blue']} 0%, {SAMSUNG_COLORS['samsung_blue']} 100%);
            color: white;
        }}
        
        section[data-testid="stSidebar"] * {{
            color: white !important;
        }}
        
        section[data-testid="stSidebar"] .stTextInput label,
        section[data-testid="stSidebar"] .stNumberInput label,
        section[data-testid="stSidebar"] .stDateInput label,
        section[data-testid="stSidebar"] .stSelectbox label {{
            color: white !important;
            font-weight: 500 !important;
        }}
        
        section[data-testid="stSidebar"] input {{
            background-color: rgba(255, 255, 255, 0.15) !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 8px;
        }}
        
        section[data-testid="stSidebar"] input::placeholder {{
            color: rgba(255, 255, 255, 0.6) !important;
        }}
        
        /* Buttons - Samsung Style */
        .stButton > button {{
            background: linear-gradient(135deg, {SAMSUNG_COLORS['samsung_blue']} 0%, {SAMSUNG_COLORS['samsung_light_blue']} 100%);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(20, 40, 160, 0.3);
            text-transform: uppercase;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(20, 40, 160, 0.4);
            background: linear-gradient(135deg, {SAMSUNG_COLORS['samsung_light_blue']} 0%, {SAMSUNG_COLORS['electric_blue']} 100%);
        }}
        
        .stButton > button:active {{
            transform: translateY(0);
        }}
        
        /* Metrics - Samsung Cards */
        div[data-testid="stMetricValue"] {{
            color: {SAMSUNG_COLORS['samsung_blue']} !important;
            font-size: 2rem !important;
            font-weight: 700 !important;
        }}
        
        div[data-testid="stMetricLabel"] {{
            color: {SAMSUNG_COLORS['dark_gray']} !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 1px;
        }}
        
        div[data-testid="stMetricDelta"] {{
            font-weight: 500 !important;
        }}
        
        /* Info/Success/Warning Boxes */
        div[data-testid="stAlert"] {{
            border-radius: 12px;
            border-left: 5px solid {SAMSUNG_COLORS['samsung_blue']};
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 1rem 1.5rem;
            background: white;
        }}
        
        .stSuccess {{
            border-left-color: {SAMSUNG_COLORS['success_green']} !important;
            background: linear-gradient(90deg, rgba(0, 200, 81, 0.05) 0%, white 100%) !important;
        }}
        
        .stInfo {{
            border-left-color: {SAMSUNG_COLORS['electric_blue']} !important;
            background: linear-gradient(90deg, rgba(0, 119, 217, 0.05) 0%, white 100%) !important;
        }}
        
        .stWarning {{
            border-left-color: {SAMSUNG_COLORS['warning_orange']} !important;
            background: linear-gradient(90deg, rgba(255, 136, 0, 0.05) 0%, white 100%) !important;
        }}
        
        /* Expander - Samsung Accordion */
        div[data-testid="stExpander"] {{
            border: 2px solid {SAMSUNG_COLORS['light_gray']};
            border-radius: 12px;
            background: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            margin-bottom: 1rem;
        }}
        
        div[data-testid="stExpander"] summary {{
            background: linear-gradient(90deg, {SAMSUNG_COLORS['very_light_gray']} 0%, white 100%);
            color: {SAMSUNG_COLORS['samsung_blue']};
            font-weight: 600;
            padding: 1rem;
            border-radius: 10px;
        }}
        
        div[data-testid="stExpander"] summary:hover {{
            background: linear-gradient(90deg, {SAMSUNG_COLORS['light_gray']} 0%, white 100%);
        }}
        
        /* Tables */
        table {{
            border-collapse: separate;
            border-spacing: 0;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }}
        
        thead tr {{
            background: linear-gradient(90deg, {SAMSUNG_COLORS['samsung_blue']} 0%, {SAMSUNG_COLORS['samsung_light_blue']} 100%);
            color: white;
        }}
        
        thead th {{
            color: white !important;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 0.5px;
            padding: 1rem;
        }}
        
        tbody tr:nth-child(even) {{
            background-color: {SAMSUNG_COLORS['very_light_gray']};
        }}
        
        tbody tr:hover {{
            background-color: rgba(20, 40, 160, 0.05);
        }}
        
        tbody td {{
            padding: 0.75rem 1rem;
            border-bottom: 1px solid {SAMSUNG_COLORS['light_gray']};
        }}
        
        /* Plotly Charts - Samsung Theme */
        .js-plotly-plot {{
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            background: white;
            padding: 1rem;
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            background-color: {SAMSUNG_COLORS['very_light_gray']};
            border-radius: 12px;
            padding: 0.5rem;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            color: {SAMSUNG_COLORS['medium_gray']};
            border-radius: 8px;
            font-weight: 500;
            padding: 0.75rem 1.5rem;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, {SAMSUNG_COLORS['samsung_blue']} 0%, {SAMSUNG_COLORS['samsung_light_blue']} 100%);
            color: white !important;
        }}
        
        /* Progress Bar */
        .stProgress > div > div > div > div {{
            background: linear-gradient(90deg, {SAMSUNG_COLORS['samsung_blue']} 0%, {SAMSUNG_COLORS['electric_blue']} 100%);
        }}
        
        /* Divider */
        hr {{
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent 0%, {SAMSUNG_COLORS['samsung_blue']} 50%, transparent 100%);
            margin: 2rem 0;
        }}
        
        /* Custom Samsung Badge */
        .samsung-badge {{
            display: inline-block;
            background: linear-gradient(135deg, {SAMSUNG_COLORS['samsung_blue']} 0%, {SAMSUNG_COLORS['samsung_light_blue']} 100%);
            color: white;
            padding: 0.25rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            box-shadow: 0 2px 8px rgba(20, 40, 160, 0.3);
        }}
        
        /* Loading Spinner */
        .stSpinner > div {{
            border-top-color: {SAMSUNG_COLORS['samsung_blue']} !important;
        }}
        
        /* Checkbox & Radio */
        .stCheckbox span, .stRadio span {{
            color: {SAMSUNG_COLORS['dark_gray']} !important;
        }}
        
        /* File Uploader */
        .stFileUploader {{
            background: white;
            border: 2px dashed {SAMSUNG_COLORS['samsung_blue']};
            border-radius: 12px;
            padding: 2rem;
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            h1 {{
                font-size: 2rem !important;
            }}
            
            .stButton > button {{
                padding: 0.6rem 1.5rem;
                font-size: 0.9rem;
            }}
        }}
        
        /* Custom Animation */
        @keyframes fadeIn {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .main > div {{
            animation: fadeIn 0.5s ease-out;
        }}
    </style>
    """

def get_samsung_plotly_theme():
    """Get Plotly theme configuration for Samsung branding"""
    return {
        'layout': {
            'font': {
                'family': 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                'size': 12,
                'color': SAMSUNG_COLORS['dark_gray']
            },
            'title': {
                'font': {
                    'size': 20,
                    'color': SAMSUNG_COLORS['samsung_blue'],
                    'family': 'Inter, sans-serif'
                },
                'x': 0.5,
                'xanchor': 'center'
            },
            'plot_bgcolor': 'white',
            'paper_bgcolor': 'white',
            'colorway': [
                SAMSUNG_COLORS['samsung_blue'],
                SAMSUNG_COLORS['electric_blue'],
                SAMSUNG_COLORS['chart_cyan'],
                SAMSUNG_COLORS['chart_teal'],
                SAMSUNG_COLORS['chart_purple'],
                SAMSUNG_COLORS['chart_orange'],
            ],
            'xaxis': {
                'gridcolor': SAMSUNG_COLORS['light_gray'],
                'linecolor': SAMSUNG_COLORS['medium_gray'],
                'zerolinecolor': SAMSUNG_COLORS['light_gray'],
            },
            'yaxis': {
                'gridcolor': SAMSUNG_COLORS['light_gray'],
                'linecolor': SAMSUNG_COLORS['medium_gray'],
                'zerolinecolor': SAMSUNG_COLORS['light_gray'],
            },
            'hovermode': 'x unified',
            'hoverlabel': {
                'bgcolor': SAMSUNG_COLORS['samsung_dark_blue'],
                'font': {'color': 'white', 'size': 13},
                'bordercolor': SAMSUNG_COLORS['samsung_blue']
            }
        }
    }

def get_samsung_chart_colors():
    """Get Samsung brand colors for charts"""
    return [
        SAMSUNG_COLORS['samsung_blue'],
        SAMSUNG_COLORS['electric_blue'],
        SAMSUNG_COLORS['chart_cyan'],
        SAMSUNG_COLORS['chart_teal'],
        SAMSUNG_COLORS['chart_purple'],
        SAMSUNG_COLORS['chart_orange'],
    ]


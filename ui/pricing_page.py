"""
Pricing and Commercialization Comparison Page
Shows pricing tiers and upgrade options for advanced features
"""

import streamlit as st
import pandas as pd
import os

def display_pricing_comparison():
    """Display the pricing comparison table with upgrade options"""
    import re  # For markdown bold conversion
    
    st.markdown("""
    <style>
    .pricing-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .pricing-table {
        width: 100%;
        border-collapse: collapse;
        margin: 2rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .pricing-table th {
        background: #f8f9fa;
        padding: 1.5rem 1rem;
        text-align: center;
        font-weight: 600;
        border-bottom: 2px solid #dee2e6;
    }
    .pricing-table td {
        padding: 1rem;
        text-align: center;
        border-bottom: 1px solid #dee2e6;
    }
    .pricing-table tr:hover {
        background: #f8f9fa;
    }
    .plan-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
    }
    .most-popular {
        background-color: #E0F7FA;
        color: #007B8A;
        font-size: 0.8em;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: bold;
    }
    .price {
        font-size: 2rem;
        font-weight: bold;
        color: #007B8A;
        margin: 0.5rem 0;
    }
    .price-note {
        font-size: 0.9em;
        color: #007B8A;
    }
    .feature-category {
        background: #e9ecef;
        font-weight: 600;
        text-align: left !important;
        padding: 1rem !important;
    }
    .feature-row {
        text-align: left !important;
        padding-left: 2rem !important;
    }
    .checkmark {
        color: #28a745;
        font-size: 1.2rem;
    }
    .crossmark {
        color: #dc3545;
        font-size: 1.2rem;
    }
    .feature-detail {
        font-size: 0.9em;
        color: #555;
    }
    .upgrade-button {
        margin-top: 1rem;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="pricing-header">
        <h1>🚀 Unlock Advanced Features</h1>
        <p>Upgrade to access Customer Segmentation, Campaign Planning, and more!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features comparison table
    st.markdown("## 📊 Feature Comparison")
    
    # Try to load CSV file
    csv_path = r"C:\Users\USER\Desktop\based on given details can give a table wise comp... - based on given details can give a table wise comp....csv"
    
    try:
        if os.path.exists(csv_path):
            # Load CSV data with first column as index, treating empty strings properly
            df = pd.read_csv(csv_path, index_col=0, keep_default_na=False)
            
            # Reset index to make first column a regular column
            df = df.reset_index()
            
            # Rename the index column to empty string (for Feature column)
            df = df.rename(columns={'index': ''})
            
            # Display the dataframe with HTML rendering enabled
            st.markdown("### Complete Pricing & Feature Comparison")
            
            # Build custom HTML table to have better control
            html = '<table class="pricing-comparison-table">\n'
            
            # Header row
            html += '<thead>\n<tr>\n'
            for i, col in enumerate(df.columns):
                # First column should say "Feature", others render HTML
                if i == 0:
                    html += '<th>Feature</th>\n'
                else:
                    # Render HTML in column headers (for "MOST POPULAR" badge)
                    html += f'<th>{col}</th>\n'
            html += '</tr>\n</thead>\n'
            
            # Body rows
            html += '<tbody>\n'
            first_col = df.columns[0]  # Get the name of first column (empty string)
            other_cols = df.columns[1:]  # Get other column names
            
            for idx, row in df.iterrows():
                # Get values, treating empty strings properly
                first_val = str(row[first_col]).strip()
                other_vals = [str(row[col]).strip() for col in other_cols]
                
                # Check if this is a category row (first cell not empty, all others empty)
                is_category = first_val != '' and all(val == '' for val in other_vals)
                
                # Check if this is a separator row (all cells empty)
                is_separator = first_val == '' and all(val == '' for val in other_vals)
                
                if is_category:
                    # Category row - span all columns
                    html += f'<tr class="category-row"><td colspan="{len(df.columns)}">{first_val}</td></tr>\n'
                elif is_separator:
                    # Empty separator row
                    html += f'<tr class="separator-row"><td colspan="{len(df.columns)}">&nbsp;</td></tr>\n'
                else:
                    # Regular data row
                    html += '<tr>\n'
                    # Process markdown bold (**text**) to HTML bold (<strong>text</strong>)
                    first_val_processed = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', first_val)
                    html += f'<td>{first_val_processed}</td>\n'
                    for col in other_cols:
                        cell_val = str(row[col])
                        # Process markdown bold in cell values
                        cell_val_processed = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', cell_val)
                        html += f'<td>{cell_val_processed}</td>\n'
                    html += '</tr>\n'
            
            html += '</tbody>\n</table>'
            
            # Add custom styling for the table
            st.markdown("""
            <style>
            .pricing-comparison-table {
                width: 100%;
                border-collapse: collapse;
                margin: 2rem 0;
                font-size: 0.95rem;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                background: white;
            }
            .pricing-comparison-table thead tr {
                background-color: #5a67d8 !important;
            }
            .pricing-comparison-table th {
                padding: 15px 12px;
                border: 1px solid #ddd;
                text-align: center;
                font-weight: 600;
                background-color: #5a67d8;
                color: white !important;
                font-size: 1rem;
            }
            .pricing-comparison-table th:first-child {
                text-align: left;
                padding-left: 20px;
            }
            .pricing-comparison-table td {
                padding: 12px 15px;
                border: 1px solid #ddd;
                text-align: center;
                vertical-align: middle;
                line-height: 1.6;
            }
            .pricing-comparison-table tbody tr:not(.category-row):not(.separator-row):nth-child(even) {
                background-color: #f8f9fa;
            }
            .pricing-comparison-table tbody tr:not(.category-row):not(.separator-row):hover {
                background-color: #e9ecef;
            }
            .pricing-comparison-table tbody tr td:first-child {
                text-align: left;
                font-weight: 500;
                padding-left: 20px;
            }
            /* Category rows */
            .pricing-comparison-table .category-row {
                background-color: #e9ecef !important;
            }
            .pricing-comparison-table .category-row td {
                font-weight: 700;
                text-align: left !important;
                padding: 12px 20px !important;
                color: #2d3748;
                font-size: 1rem;
            }
            /* Separator rows */
            .pricing-comparison-table .separator-row td {
                padding: 5px !important;
                border: none !important;
                background: white !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Display the HTML table
            st.markdown(html, unsafe_allow_html=True)
            
            # Add upgrade buttons below the table
            _display_upgrade_buttons(key_suffix="_csv")
            
        else:
            st.warning(f"CSV file not found at: {csv_path}")
            st.info("Displaying default pricing comparison...")
            # Fall back to hardcoded data if CSV not found
            _display_fallback_comparison()
    except Exception as e:
        st.error(f"Error loading CSV: {str(e)}")
        st.info("Displaying default pricing comparison...")
        _display_fallback_comparison()

def _display_upgrade_buttons(key_suffix=""):
    """Display upgrade buttons for Pro, Business, and Enterprise plans"""
    
    # Upgrade CTAs
    st.markdown("")  # Spacing
    st.markdown("## 🎯 Ready to Upgrade?")
    st.markdown("Choose the plan that's right for you and unlock advanced features!")
    
    st.markdown("")  # Spacing
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 💼 Pro Plan")
        st.markdown("**$1,500/month**")
        st.markdown("Perfect for small teams")
        st.markdown("")
        if st.button("🚀 Upgrade to Pro", key=f"upgrade_pro{key_suffix}", use_container_width=True, type="primary"):
            # Set session state to unlock Pro features
            st.session_state['user_plan'] = 'pro'
            st.balloons()
            st.success("🎉 Congratulations! Pro Plan activated!")
            st.info("✨ Refreshing to show your premium features...")
            st.rerun()
    
    with col2:
        st.markdown("### 🚀 Business Plan")
        st.markdown("**$12,000/month**")
        st.markdown("Best for growing companies")
        st.markdown("")
        if st.button("🚀 Upgrade to Business", key=f"upgrade_business{key_suffix}", use_container_width=True, type="primary"):
            # Set session state to unlock Business features
            st.session_state['user_plan'] = 'business'
            st.balloons()
            st.success("🎉 Congratulations! Business Plan activated!")
            st.info("✨ Refreshing to show your premium features...")
            st.rerun()
    
    with col3:
        st.markdown("### 🏢 Enterprise Plan")
        st.markdown("**Custom Pricing**")
        st.markdown("For large organizations")
        st.markdown("")
        if st.button("📧 Contact Sales", key=f"upgrade_enterprise{key_suffix}", use_container_width=True, type="primary"):
            # Set session state to unlock Enterprise features
            st.session_state['user_plan'] = 'enterprise'
            st.balloons()
            st.success("🎉 Congratulations! Enterprise Plan activated!")
            st.info("✨ Refreshing to show your premium features...")
            st.rerun()

def _display_fallback_comparison():
    """Display fallback comparison table if CSV is not available"""
    comparison_data = {
        "Feature": [
            "Market Trend Analyzer",
            "Competitor Tracking",
            "Customer Segmentation",
            "Campaign Planner",
            "Users",
            "Data History",
            "Support Level",
            "Integrations",
        ],
        "Starter": [
            "✅ (3 topics)",
            "✅ (3 competitors)",
            "❌",
            "❌",
            "1 User",
            "30 Days",
            "Community Support",
            "❌",
        ],
        "Pro": [
            "✅ (50 topics)",
            "✅ (50 competitors)",
            "✅ (Basic segmentation)",
            "❌",
            "5 Users",
            "1 Year",
            "Standard Email Support",
            "✅ (Slack, Analytics)",
        ],
        "Business": [
            "✅ (Unlimited topics)",
            "✅ (Unlimited competitors)",
            "✅ (Advanced behavioral)",
            "✅ (Full planning & budget)",
            "25 Users",
            "3 Years",
            "Dedicated Account Manager",
            "✅ (Salesforce, Marketo)",
        ],
        "Enterprise": [
            "✅ (Custom-trained models)",
            "✅ (Predictive analysis)",
            "✅ (CRM integration)",
            "✅ (Full + ROI simulation)",
            "Unlimited",
            "Unlimited",
            "Dedicated Solutions Engineer",
            "✅ (Data lakes, Azure)",
        ]
    }
    
    # Build and display comparison table
    df_comparison = pd.DataFrame(comparison_data)
    
    # Convert to HTML with styling
    html = df_comparison.to_html(index=False, escape=False, classes='pricing-comparison-table')
    
    st.markdown("""
    <style>
    .pricing-comparison-table {
        width: 100%;
        border-collapse: collapse;
        margin: 2rem 0;
        font-size: 0.95rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .pricing-comparison-table thead tr {
        background-color: #667eea;
        color: white;
        text-align: center;
    }
    .pricing-comparison-table th,
    .pricing-comparison-table td {
        padding: 12px 15px;
        border: 1px solid #ddd;
        text-align: center;
    }
    .pricing-comparison-table tbody tr:nth-child(even) {
        background-color: #f8f9fa;
    }
    .pricing-comparison-table tbody tr:hover {
        background-color: #e9ecef;
    }
    .pricing-comparison-table tbody tr td:first-child {
        text-align: left;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(html, unsafe_allow_html=True)
    
    # Add upgrade buttons
    _display_upgrade_buttons(key_suffix="_fallback")

def show_upgrade_modal(feature_name):
    """Show upgrade modal when user tries to access locked features"""
    
    st.warning(f"🔒 **{feature_name}** is a premium feature")
    
    st.markdown("""
    ### Unlock this feature by upgrading!
    
    **Available in:**
    - 💼 **Pro Plan** - Starting at $1,500/month
    - 🚀 **Business Plan** - Starting at $12,000/month
    - 🏢 **Enterprise Plan** - Custom pricing
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎯 View Pricing Plans", use_container_width=True, type="primary"):
            st.session_state.show_pricing = True
            st.rerun()
    
    with col2:
        if st.button("📧 Contact Sales", use_container_width=True):
            st.success("Sales team will contact you within 24 hours!")


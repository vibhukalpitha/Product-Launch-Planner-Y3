#!/usr/bin/env python3
"""
Test script for city sales bar charts
Tests the Plotly chart functionality to ensure no errors
"""

import plotly.graph_objects as go
import plotly.express as px

def test_city_bar_charts():
    """Test all three types of city sales charts"""
    print("🧪 Testing City Sales Bar Charts...")
    
    # Sample city sales data
    cities = ['Seoul', 'Tokyo', 'New York', 'London', 'Berlin', 'Mumbai', 'Singapore', 'Sydney']
    volumes = [150000, 135000, 120000, 110000, 95000, 85000, 75000, 65000]
    
    print(f"📊 Sample data: {len(cities)} cities, volumes: {volumes[0]:,} to {volumes[-1]:,}")
    
    # Test 1: Vertical Bar Chart
    try:
        print("\n🧪 Test 1: Vertical Bar Chart")
        
        # Create color gradient
        max_volume = max(volumes)
        colors = []
        for volume in volumes:
            intensity = volume / max_volume
            if intensity > 0.8:
                colors.append('#1f4e79')  # Dark blue
            elif intensity > 0.6:
                colors.append('#2e86ab')  # Medium blue
            elif intensity > 0.4:
                colors.append('#a23b72')  # Purple
            elif intensity > 0.2:
                colors.append('#f18f01')  # Orange
            else:
                colors.append('#c73e1d')  # Red
        
        fig_vertical = go.Figure()
        fig_vertical.add_trace(go.Bar(
            x=cities,
            y=volumes,
            name="Sales Volume",
            marker=dict(
                color=colors,
                line=dict(color='white', width=1),
                opacity=0.8
            ),
            text=[f"{v:,.0f}" for v in volumes],
            textposition='auto',
            textfont=dict(color='white', size=10),
            hovertemplate="<b>%{x}</b><br>Sales Volume: %{y:,.0f}<br><extra></extra>"
        ))
        
        fig_vertical.update_layout(
            title=dict(
                text="🏙️ City Sales Performance (Vertical)",
                font=dict(size=18, color='#1f4e79'),
                x=0.5
            ),
            xaxis=dict(
                title="City",
                title_font=dict(size=14, color='#2e86ab'),
                tickangle=-45,
                tickfont=dict(size=11)
            ),
            yaxis=dict(
                title="Sales Volume",
                title_font=dict(size=14, color='#2e86ab'),
                tickfont=dict(size=11)
            ),
            height=500
        )
        
        print("✅ Vertical bar chart created successfully")
        
    except Exception as e:
        print(f"❌ Vertical bar chart failed: {e}")
        return False
    
    # Test 2: Horizontal Bar Chart
    try:
        print("\n🧪 Test 2: Horizontal Bar Chart")
        
        cities_rev = cities[::-1]
        volumes_rev = volumes[::-1]
        colors_rev = colors[::-1]
        
        fig_horizontal = go.Figure()
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
                text="📈 City Sales Performance (Horizontal)",
                font=dict(size=16, color='#1f4e79'),
                x=0.5
            ),
            xaxis=dict(
                title="Sales Volume",
                title_font=dict(size=14, color='#2e86ab')
            ),
            yaxis=dict(
                title="Cities",
                title_font=dict(size=14, color='#2e86ab'),
                tickfont=dict(size=11)
            ),
            height=400
        )
        
        print("✅ Horizontal bar chart created successfully")
        
    except Exception as e:
        print(f"❌ Horizontal bar chart failed: {e}")
        return False
    
    # Test 3: Pie Chart
    try:
        print("\n🧪 Test 3: Pie Chart")
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=cities[:6],  # Top 6 cities
            values=volumes[:6],
            textinfo='label+percent',
            textposition='auto',
            marker=dict(
                colors=['#1f4e79', '#2e86ab', '#a23b72', '#f18f01', '#c73e1d', '#3d5a80'],
                line=dict(color='white', width=2)
            ),
            hovertemplate="<b>%{label}</b><br>Sales: %{value:,.0f}<br>Share: %{percent}<br><extra></extra>"
        )])
        
        fig_pie.update_layout(
            title=dict(
                text="🥧 City Market Share Distribution",
                font=dict(size=16, color='#1f4e79'),
                x=0.5
            ),
            height=500
        )
        
        print("✅ Pie chart created successfully")
        
    except Exception as e:
        print(f"❌ Pie chart failed: {e}")
        return False
    
    print("\n🎉 All chart tests passed!")
    print("📊 Charts are ready for Streamlit integration")
    return True

if __name__ == "__main__":
    success = test_city_bar_charts()
    if success:
        print("\n✅ Chart functionality test: PASSED")
    else:
        print("\n❌ Chart functionality test: FAILED")
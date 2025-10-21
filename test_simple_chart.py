#!/usr/bin/env python3
"""
Simple City Sales Chart Test
Creates a clean vertical bar chart without complex overlays
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np

def create_simple_city_chart():
    """Create a simple, clean city sales bar chart"""
    
    # Sample data like what the app would generate
    cities = ['Tokyo', 'New York', 'Singapore', 'London', 'Seoul', 'Mumbai', 'Berlin', 'Sydney', 'Toronto', 'Dubai']
    volumes = [145000, 132000, 125000, 118000, 112000, 95000, 88000, 82000, 75000, 68000]
    
    # Create simple color gradient
    max_vol = max(volumes)
    colors = []
    for vol in volumes:
        intensity = vol / max_vol
        if intensity > 0.8:
            colors.append('#1f4e79')  # Dark blue
        elif intensity > 0.6:
            colors.append('#2e86ab')  # Medium blue  
        elif intensity > 0.4:
            colors.append('#5d9cec')  # Light blue
        elif intensity > 0.2:
            colors.append('#95c5f7')  # Very light blue
        else:
            colors.append('#c5e2ff')  # Pale blue
    
    # Create the bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=cities,
        y=volumes,
        name="Sales Volume",
        marker=dict(
            color=colors,
            line=dict(color='white', width=1.5),
            opacity=0.9
        ),
        text=[f"{v:,.0f}" for v in volumes],
        textposition='outside',
        textfont=dict(color='#333333', size=11, family='Arial'),
        hovertemplate="<b>%{x}</b><br>Sales Volume: %{y:,.0f}<br><extra></extra>"
    ))
    
    # Clean layout
    fig.update_layout(
        title=dict(
            text="🏙️ Top Performing Cities for Samsung Products",
            font=dict(size=20, color='#1f4e79', family='Arial'),
            x=0.5,
            y=0.95
        ),
        xaxis=dict(
            title="Cities",
            title_font=dict(size=14, color='#2e86ab', family='Arial'),
            tickangle=-45,
            tickfont=dict(size=12, color='#333333', family='Arial'),
            gridcolor='rgba(200,200,200,0.2)',
            gridwidth=1,
            showgrid=False,
            linecolor='#cccccc',
            linewidth=1
        ),
        yaxis=dict(
            title="Average Sales Volume",
            title_font=dict(size=14, color='#2e86ab', family='Arial'),
            tickfont=dict(size=12, color='#333333', family='Arial'),
            gridcolor='rgba(200,200,200,0.3)',
            gridwidth=1,
            showgrid=True,
            linecolor='#cccccc',
            linewidth=1
        ),
        height=650,
        width=1000,
        showlegend=False,  # Remove legend for cleaner look
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=80, r=40, t=100, b=150)  # Extra bottom margin for city names
    )
    
    return fig

if __name__ == "__main__":
    # Test the chart
    fig = create_simple_city_chart()
    print("✅ Simple city chart created successfully!")
    print("📊 Chart ready for Streamlit display")
    
    # Show chart dimensions and data
    print(f"📏 Chart size: 1000x650 pixels")
    print(f"🏙️ Cities: 10")
    print(f"📈 Volume range: 68,000 - 145,000")
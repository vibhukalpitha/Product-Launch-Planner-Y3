# 📱 Samsung Product Launch Planner

An intelligent AI-powered system designed specifically for Samsung to plan and optimize product launches using 4 specialized agents and free APIs.

## 🌟 System Overview

The Samsung Product Launch Planner is a comprehensive multi-agent system that helps Samsung plan successful product launches by analyzing market trends, competitors, customer segments, and optimal marketing campaigns. The system uses only free APIs and provides interactive visualizations through a Streamlit interface.

## 🤖 The Four Agents

### 1. 🔍 Market Trend Analyzer Agent
**Purpose**: Analyzes market trends, historical sales, and forecasts future performance

**Inputs**:
- Product category (smartphones, tablets, laptops, wearables, TV, appliances)
- Product price
- Product description

**Outputs**:
- Historical sales data analysis (past 3 years)
- Market growth rate and trends
- Sales forecast (next 12 months)
- Price vs. market average comparison
- Top performing cities analysis
- Market-based recommendations
- Interactive charts:
  - Historical sales trends
  - Sales forecast with confidence intervals
  - City performance comparison
  - Market trends radar chart

**Free APIs Used**:
- FakeStore API (for demo product data)
- World Bank API (for economic indicators)
- Generated realistic market data based on category patterns

### 2. 🏢 Competitor Tracking Agent
**Purpose**: Monitors competitors, analyzes pricing strategies, and social media sentiment

**Inputs**:
- Product category
- Product price
- Target market

**Outputs**:
- Competitor price comparison with major brands
- Price positioning analysis (budget/standard/premium)
- Social media sentiment analysis for competitors
- Sample social media feedback and reviews
- Trending topics and discussions
- Competitive recommendations
- Interactive charts:
  - Price comparison bar chart
  - Sentiment analysis comparison
  - Market share visualization

**Competitors Analyzed by Category**:
- **Smartphones**: Apple, Google, OnePlus, Xiaomi, Huawei
- **Tablets**: Apple, Microsoft, Lenovo, Amazon
- **Laptops**: Apple, Dell, HP, Lenovo, ASUS
- **Wearables**: Apple, Fitbit, Garmin, Amazfit
- **TV**: LG, Sony, TCL, Hisense, Panasonic
- **Appliances**: LG, Whirlpool, GE, Bosch, Electrolux

**Free APIs Used**:
- FakeStore API (for competitor product data)
- Reddit API (for social media sentiment - limited free tier)
- Simulated social media sentiment based on realistic patterns

### 3. 👥 Customer Segmentation Agent
**Purpose**: Identifies and analyzes customer segments using demographic and behavioral data

**Inputs**:
- Product category
- Target demographics
- Market data from other agents

**Outputs**:
- 4 distinct customer segments:
  - **Tech Enthusiasts**: Early adopters, high tech adoption
  - **Value Seekers**: Price-conscious, value-focused buyers
  - **Brand Loyalists**: High brand loyalty, established preferences
  - **Conservative Buyers**: Traditional, low-risk preferences
- Segment characteristics and attractiveness scores
- Feature priorities for each segment
- Preferred marketing channels
- Purchase drivers and communication styles
- Targeted recommendations for each segment
- Interactive charts:
  - Segment size distribution
  - Attractiveness scores
  - Segment characteristics radar chart
  - Age distribution by segment

**Analysis Metrics**:
- Tech adoption rate
- Price sensitivity
- Brand loyalty
- Social media usage
- Sustainability concern
- Purchase frequency
- Online shopping preference

### 4. 📢 Campaign Planning Agent
**Purpose**: Designs optimal marketing campaigns based on audience, budget, and platform effectiveness

**Inputs**:
- Target age groups (18-24, 25-34, 35-44, 45-54, 55+)
- Selected social media platforms (checkboxes)
- Campaign budget ($)
- Campaign duration (days)

**Outputs**:
- Platform effectiveness analysis for target audience
- Top 2 recommended platforms for maximum ROI
- Detailed cost breakdown by platform:
  - Estimated clicks and impressions
  - Cost per click (CPC) and cost per impression (CPM)
  - Reach and engagement projections
  - ROI calculations
- Budget allocation strategy (70% primary, 30% secondary platform)
- Budget vs. actual cost comparison
- Campaign timeline with key milestones
- Success metrics and KPIs
- Interactive charts:
  - Platform effectiveness scores
  - Budget allocation pie chart
  - ROI projection by platform
  - Campaign timeline

**Social Media Platforms Supported**:
- **Facebook**: Broad demographic reach, cost-effective
- **Instagram**: Young audience, high engagement
- **TikTok**: Gen Z focus, viral potential
- **YouTube**: Video content, high reach
- **Twitter**: Real-time engagement, news-focused
- **LinkedIn**: Professional audience, B2B focus
- **Snapchat**: Young demographics, AR features

## 🔄 Agent Communication Flow

```
User Input (Product Info) 
         ↓
Communication Coordinator
         ↓
1. Market Trend Analyzer
   - Analyzes market conditions
   - Generates sales forecasts
   - Shares data with other agents
         ↓
2. Competitor Tracking Agent
   - Uses market data for context
   - Analyzes competitive landscape
   - Provides pricing insights
         ↓
3. Customer Segmentation Agent
   - Uses market and competitor data
   - Segments customers
   - Identifies target preferences
         ↓
4. Campaign Planning Agent
   - Uses all previous agent data
   - Designs optimal campaigns
   - Calculates ROI and costs
         ↓
Comprehensive Results Dashboard
```

## 🖥️ Frontend (Streamlit UI)

### Main Input Form
**Product Information**:
- Product Name (text input)
- Product Category (dropdown)
- Product Price (number input)
- Product Description (text area)
- Expected Launch Date (date picker)

**Target Audience & Campaign Settings**:
- Target Age Groups (multi-select checkboxes)
- Preferred Social Media Platforms (multi-select checkboxes)
- Campaign Budget (number input)
- Campaign Duration in days (number input)

### Output Sections

#### 1. Market Analysis Dashboard
- **Key Metrics**: Market growth rate, average price, forecast, saturation
- **Charts**: Historical sales, forecast trends, city performance, market trends
- **Recommendations**: Price positioning, market opportunities, city focus

#### 2. Competitor Analysis Dashboard
- **Price Comparison**: Your price vs. competitors with visual comparison
- **Sentiment Analysis**: Competitor sentiment scores and trending topics
- **Social Media Insights**: Sample feedback from social platforms
- **Recommendations**: Competitive positioning and feature differentiation

#### 3. Customer Segmentation Dashboard
- **Segment Overview**: 4 segments with sizes and attractiveness scores
- **Detailed Analysis**: Characteristics, preferences, and strategies per segment
- **Visualizations**: Segment distribution, radar charts, age demographics
- **Recommendations**: Primary targets and messaging strategies

#### 4. Campaign Planning Dashboard
- **Platform Recommendations**: Top 2 platforms with effectiveness scores
- **Budget Analysis**: Allocation, costs, and budget comparison
- **Performance Projections**: Reach, clicks, engagement, ROI
- **Campaign Timeline**: Phases, milestones, and key activities
- **Recommendations**: Optimization strategies and success metrics

## 🆓 Free APIs Used

### Market Data
- **FakeStore API**: Product categories and pricing data
- **World Bank API**: Economic indicators and market data
- **Simulated Data**: Realistic market trends based on industry patterns

### Competitor Intelligence
- **FakeStore API**: Competitor product information
- **Reddit API**: Social media sentiment (limited free tier)
- **Simulated Sentiment**: Based on realistic brand perception patterns

### Social Media Analytics
- **Platform Data**: Cost estimates based on industry standards
- **Demographic Data**: Platform user distribution and engagement rates
- **Simulated Metrics**: Realistic campaign performance projections

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone the repository**:
```bash
git clone https://github.com/vibhukalpitha/Product-Launch-Planner-Y3.git
cd Product-Launch-Planner-Y3
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure API keys** (optional):
   - Edit `config.json` to add your API keys for enhanced functionality
   - The system works with simulated data without API keys

4. **Run the application**:
```bash
streamlit run ui/streamlit_app.py
```

5. **Access the application**:
   - Open your browser and go to `http://localhost:8501`

## 📁 Project Structure

```
Product-Launch-Planner-Y3/
├── agents/
│   ├── communication_coordinator.py    # Inter-agent communication
│   ├── market_trend_analyzer.py       # Market analysis agent
│   ├── competitor_tracking_agent.py   # Competitor analysis agent
│   ├── customer_segmentation_agent.py # Customer segmentation agent
│   └── campaign_planning_agent.py     # Campaign planning agent
├── ui/
│   └── streamlit_app.py               # Main Streamlit interface
├── utils/
│   └── helpers.py                     # Utility functions
├── data/                              # Data storage (created at runtime)
├── config.json                        # Configuration settings
├── requirements.txt                   # Python dependencies
└── README.md                         # This file
```

## 🎯 Sample Use Case

**Scenario**: Samsung wants to launch the Galaxy S25 Ultra

**Inputs**:
- Product: Galaxy S25 Ultra
- Category: Smartphones
- Price: $1,200
- Target Audience: 25-34, 35-44 age groups
- Platforms: Facebook, Instagram, YouTube
- Budget: $50,000
- Duration: 30 days

**Expected Outputs**:
1. **Market Analysis**: 15% growth in premium smartphone market, $1,200 is 5% above average
2. **Competitor Analysis**: Apple iPhone 15 Pro at $1,299, positive sentiment for camera features
3. **Customer Segmentation**: Tech Enthusiasts (30%) as primary target, focus on camera and performance
4. **Campaign Planning**: Instagram primary (40% budget), Facebook secondary (30% budget), projected 250% ROI

## 🔧 Customization

### Adding New APIs
1. Update the respective agent's `apis` dictionary
2. Implement new methods for API integration
3. Add rate limiting and error handling
4. Update `config.json` with new API settings

### Modifying Segments
1. Edit `CustomerSegmentationAgent.age_segments`
2. Adjust clustering parameters in `perform_clustering()`
3. Update visualization logic

### Adding Platforms
1. Update `CampaignPlanningAgent.platforms`
2. Add demographic and cost data
3. Update UI platform selection options

## 📊 Key Features

- **Real-time Analysis**: Live processing of market and competitor data
- **Interactive Visualizations**: Dynamic charts and graphs with Plotly
- **Comprehensive Insights**: End-to-end launch strategy from market to campaign
- **Cost-Effective**: Uses only free APIs and open-source tools
- **Samsung-Focused**: Tailored specifically for Samsung's product portfolio
- **Scalable Architecture**: Easy to extend with new agents and features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation in the `docs/` folder

## 🔮 Future Enhancements

- Real-time social media monitoring
- Advanced AI/ML models for better predictions
- Integration with Samsung's internal databases
- Mobile app version
- Multi-language support
- Advanced A/B testing capabilities

"""
Minimal communication_coordinator stub for development/testing.
Provides a Coordinator with a minimal API expected by agents and the UI.
This is a safe, non-production stub intended to unblock the UI when the real
implementation is missing.
"""
from typing import Any, Dict, Optional

class ProductInfo:
    def __init__(
        self,
        name: str = "",
        category: str = "",
        price: Optional[float] = None,
        description: Optional[str] = None,
        target_audience: Optional[Dict[str, Any]] = None,
        launch_date: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        # Accept the common fields used across the UI and tests and store any extra kwargs
        self.name = name
        self.category = category
        self.price = price
        self.description = description
        self.target_audience = target_audience or {}
        self.launch_date = launch_date
        self.details = details or {}
        # Preserve other unexpected fields for forward compatibility
        for k, v in kwargs.items():
            setattr(self, k, v)

class Coordinator:
    def __init__(self):
        self._agents = {}
        self._shared = {}

    def send_message(self, sender: str, agent_name: str, message_type: str, data: dict = None, timeout: float = 10):
        """Route a message from a sender to a registered agent.

        This is a minimal router used by the Streamlit UI. It creates a
        small Message object and calls the agent's `receive_message` if
        available, otherwise it will try to call a method on the agent
        that matches `message_type` with `data` as kwargs.
        """
        class Message:
            def __init__(self, sender, message_type, data=None):
                self.sender = sender
                self.message_type = message_type
                self.data = data or {}

        agent = self._agents.get(agent_name)
        if not agent:
            print(f"⚠️ Coordinator: agent '{agent_name}' not registered")
            return None

        msg = Message(sender, message_type, data or {})

        # Prefer the unified receive_message entrypoint if present
        try:
            if hasattr(agent, 'receive_message'):
                return agent.receive_message(msg)

            # Fallback: try to call a method that matches message_type
            if hasattr(agent, message_type):
                method = getattr(agent, message_type)
                if callable(method):
                    # If data is a dict, pass as kwargs when method accepts them
                    try:
                        return method(**(data or {}))
                    except TypeError:
                        return method(data or {})

            print(f"⚠️ Coordinator: agent '{agent_name}' cannot handle message type '{message_type}'")
            return None
        except Exception as e:
            print(f"⚠️ Coordinator: error routing message to '{agent_name}': {e}")
            return None

    def register_agent(self, name: str, agent: Any):
        self._agents[name] = agent

    def get_shared_data(self) -> Dict[str, Any]:
        return self._shared

    def set_shared_data(self, key: str, value: Any):
        self._shared[key] = value

    def orchestrate_analysis(self, product_info: ProductInfo) -> Dict[str, Any]:
        """Orchestrate comprehensive analysis using all agents"""
        try:
            print(f"🔄 Starting analysis for {product_info.name}...")
            
            # Initialize agents
            from market_trend_analyzer import MarketTrendAnalyzer
            from competitor_tracking_agent import CompetitorTrackingAgent
            from customer_segmentation_agent import CustomerSegmentationAgent
            from campaign_planning_agent import CampaignPlanningAgent
            
            # Create agent instances
            market_analyzer = MarketTrendAnalyzer(self)
            competitor_agent = CompetitorTrackingAgent(self)
            customer_agent = CustomerSegmentationAgent(self)
            campaign_agent = CampaignPlanningAgent(self)
            
            print("✅ All agents initialized successfully")
            
            # Run analysis
            results = {
                'product': {
                    'name': getattr(product_info, 'name', None),
                    'category': getattr(product_info, 'category', None),
                    'price': getattr(product_info, 'price', None),
                    'description': getattr(product_info, 'description', None),
                    'target_audience': getattr(product_info, 'target_audience', None),
                    'launch_date': getattr(product_info, 'launch_date', None)
                },
                'status': 'completed',
                'details': {}
            }
            
            # Market Analysis
            print("📈 Running market analysis...")
            try:
                # Convert ProductInfo to dict for agent compatibility
                product_dict = {
                    'name': getattr(product_info, 'name', None),
                    'category': getattr(product_info, 'category', None),
                    'price': getattr(product_info, 'price', None),
                    'description': getattr(product_info, 'description', None),
                    'target_audience': getattr(product_info, 'target_audience', None),
                    'launch_date': getattr(product_info, 'launch_date', None)
                }
                market_results = market_analyzer.analyze_market_trends(product_dict)
                results['market_analysis'] = market_results
                print("✅ Market analysis completed")
            except Exception as e:
                print(f"⚠️ Market analysis failed: {e}")
                results['market_analysis'] = {'error': str(e)}
            
            # Competitor Analysis
            print("🏢 Running competitor analysis...")
            try:
                competitor_results = competitor_agent.analyze_competitors(product_dict)
                results['competitor_analysis'] = competitor_results
                print("✅ Competitor analysis completed")
            except Exception as e:
                print(f"⚠️ Competitor analysis failed: {e}")
                results['competitor_analysis'] = {'error': str(e)}
            
            # Customer Segmentation
            print("👥 Running customer segmentation...")
            try:
                customer_results = customer_agent.segment_customers(product_dict)
                results['customer_segmentation'] = customer_results
                print("✅ Customer segmentation completed")
            except Exception as e:
                print(f"⚠️ Customer segmentation failed: {e}")
                results['customer_segmentation'] = {'error': str(e)}
            
            # Campaign Planning
            print("📢 Running campaign planning...")
            try:
                campaign_results = campaign_agent.plan_campaign(product_dict)
                results['campaign_planning'] = campaign_results
                print("✅ Campaign planning completed")
            except Exception as e:
                print(f"⚠️ Campaign planning failed: {e}")
                results['campaign_planning'] = {'error': str(e)}
            
            print("🎉 Analysis orchestration completed successfully!")
            return results
            
        except Exception as e:
            print(f"❌ Analysis orchestration failed: {e}")
            return {
                'product': {
                    'name': getattr(product_info, 'name', None),
                    'category': getattr(product_info, 'category', None),
                    'price': getattr(product_info, 'price', None),
                    'description': getattr(product_info, 'description', None),
                    'target_audience': getattr(product_info, 'target_audience', None),
                    'launch_date': getattr(product_info, 'launch_date', None)
                },
                'status': 'failed',
                'error': str(e),
                'details': {}
            }

# module-level convenience objects expected by imports
coordinator = Coordinator()

# Also expose the class for tests that expect it
CommunicationCoordinator = Coordinator

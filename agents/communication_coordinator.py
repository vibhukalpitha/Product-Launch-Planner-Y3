"""
Communication Coordinator for Product Launch Planner
Manages inter-agent communication and data flow
"""
import json
from typing import Dict, Any, List
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class ProductInfo:
    """Product information structure"""
    name: str
    category: str
    price: float
    description: str
    target_audience: Dict[str, Any]
    launch_date: str

@dataclass
class CommunicationMessage:
    """Message structure for inter-agent communication"""
    sender: str
    receiver: str
    message_type: str
    data: Dict[str, Any]
    timestamp: str

class CommunicationCoordinator:
    """Manages communication between all agents"""
    
    def __init__(self):
        self.agents = {}
        self.message_queue = []
        self.shared_data = {
            'product_info': None,
            'market_analysis': None,
            'competitor_analysis': None,
            'customer_segments': None,
            'campaign_plan': None
        }
    
    def register_agent(self, agent_name: str, agent_instance):
        """Register an agent with the coordinator"""
        self.agents[agent_name] = agent_instance
        print(f"Agent {agent_name} registered successfully")
    
    def send_message(self, sender: str, receiver: str, message_type: str, data: Dict[str, Any]):
        """Send message between agents"""
        message = CommunicationMessage(
            sender=sender,
            receiver=receiver,
            message_type=message_type,
            data=data,
            timestamp=datetime.now().isoformat()
        )
        self.message_queue.append(message)
        return self.deliver_message(message)
    
    def deliver_message(self, message: CommunicationMessage):
        """Deliver message to target agent"""
        if message.receiver in self.agents:
            return self.agents[message.receiver].receive_message(message)
        else:
            print(f"Agent {message.receiver} not found")
            return None
    
    def update_shared_data(self, data_type: str, data: Dict[str, Any]):
        """Update shared data accessible by all agents"""
        self.shared_data[data_type] = data
        print(f"Shared data updated: {data_type}")
    
    def get_shared_data(self, data_type: str = None):
        """Get shared data"""
        if data_type:
            return self.shared_data.get(data_type)
        return self.shared_data
    
    def orchestrate_analysis(self, product_info: ProductInfo):
        """Orchestrate the complete analysis workflow"""
        print("Starting product launch analysis...")
        
        # Store product info
        self.update_shared_data('product_info', asdict(product_info))
        
        # Communication flow:
        # 1. Market Trend Analyzer analyzes market conditions
        # 2. Competitor Tracking Agent analyzes competition
        # 3. Customer Segmentation Agent segments customers
        # 4. Campaign Planner creates campaign strategy
        
        results = {}
        
        # Step 1: Market Analysis
        if 'market_analyzer' in self.agents:
            market_result = self.send_message(
                'coordinator', 'market_analyzer', 'analyze_market', 
                {'product_info': asdict(product_info)}
            )
            results['market_analysis'] = market_result
            self.update_shared_data('market_analysis', market_result)
        
        # Step 2: Competitor Analysis
        if 'competitor_tracker' in self.agents:
            competitor_result = self.send_message(
                'coordinator', 'competitor_tracker', 'analyze_competitors',
                {'product_info': asdict(product_info), 'market_data': results.get('market_analysis')}
            )
            results['competitor_analysis'] = competitor_result
            self.update_shared_data('competitor_analysis', competitor_result)
        
        # Step 3: Customer Segmentation
        if 'customer_segmenter' in self.agents:
            segmentation_result = self.send_message(
                'coordinator', 'customer_segmenter', 'segment_customers',
                {
                    'product_info': asdict(product_info),
                    'market_data': results.get('market_analysis'),
                    'competitor_data': results.get('competitor_analysis')
                }
            )
            results['customer_segments'] = segmentation_result
            self.update_shared_data('customer_segments', segmentation_result)
        
        # Step 4: Campaign Planning
        if 'campaign_planner' in self.agents:
            campaign_result = self.send_message(
                'coordinator', 'campaign_planner', 'plan_campaign',
                {
                    'product_info': asdict(product_info),
                    'market_data': results.get('market_analysis'),
                    'competitor_data': results.get('competitor_analysis'),
                    'customer_data': results.get('customer_segments')
                }
            )
            results['campaign_plan'] = campaign_result
            self.update_shared_data('campaign_plan', campaign_result)
        
        return results

# Global coordinator instance
coordinator = CommunicationCoordinator()
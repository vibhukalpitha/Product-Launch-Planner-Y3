import sys, os, json
sys.path.append(os.path.abspath('.'))
from agents.competitor_tracking_agent import CompetitorTrackingAgent

class DummyCoordinator:
    def register_agent(self, name, agent):
        pass

co = DummyCoordinator()
agent = CompetitorTrackingAgent(co)
product_info = {'name':'Galaxy S25 Ultra','category':'Smartphones','price':1200,'price_range':'premium'}
res = agent.analyze_competitors(product_info)
market_insights = res.get('competitor_discovery', {}).get('market_insights')
sentiment = res.get('sentiment_analysis', {})
print('--- MARKET_INSIGHTS ---')
print(json.dumps(market_insights, indent=2))
print('--- SENTIMENT KEYS ---')
print(list(sentiment.keys()))
for k in list(sentiment.keys())[:3]:
    print(f"--- SAMPLE SENTIMENT for {k} ---")
    print(json.dumps(sentiment[k], indent=2))

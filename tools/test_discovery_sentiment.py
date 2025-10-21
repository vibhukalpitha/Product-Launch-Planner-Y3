import sys, os, json
sys.path.append(os.path.abspath('.'))
from agents.competitor_tracking_agent import CompetitorTrackingAgent
class DummyCoordinator:
    def register_agent(self, name, agent):
        pass
co = DummyCoordinator()
agent = CompetitorTrackingAgent(co)
# Test discovery
disc = agent.discover_intelligent_competitors('Galaxy S25 Ultra', 'Smartphones', 'premium')
print('DISCOVERY market_insights:')
print(json.dumps(disc.get('market_insights',{}), indent=2))
# Test sentiment on discovered competitors
all_disc = disc.get('direct_competitors',[]) + disc.get('indirect_competitors',[])
sent = agent.get_social_media_sentiment('smartphones', all_disc[:5])
print('\nSENTIMENT keys:', list(sent.keys()))
for k,v in sent.items():
    print(f'---{k}---')
    print(json.dumps(v, indent=2))
    print('----')

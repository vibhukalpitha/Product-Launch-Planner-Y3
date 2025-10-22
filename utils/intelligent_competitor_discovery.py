"""
Minimal fallback for IntelligentCompetitorDiscovery used by the agent when the real module is missing.
This provides a safe default implementation returning a structured discovery result.
"""
from datetime import datetime
from typing import Dict, Any

class IntelligentCompetitorDiscovery:
    def __init__(self):
        # lightweight placeholder
        pass

    def discover_competitors(self, product_name: str, category: str, price_range: str = None) -> Dict[str, Any]:
        # Return a simple discovery result similar to the agent's fallback structure
        fallback_competitors = {
            'smartphones': ['Apple', 'Google', 'OnePlus', 'Xiaomi', 'Huawei', 'Samsung'],
            'laptops': ['Apple', 'Dell', 'HP', 'Lenovo'],
            'tablets': ['Apple', 'Samsung', 'Microsoft', 'Amazon']
        }
        comps = fallback_competitors.get(category.lower(), fallback_competitors['smartphones'])
        return {
            'product_name': product_name,
            'category': category,
            'price_range': price_range,
            'discovery_timestamp': datetime.now().isoformat(),
            'direct_competitors': comps[:4],
            'indirect_competitors': comps[4:6] if len(comps) > 4 else [],
            'emerging_competitors': [],
            'confidence_scores': {c: 0.5 for c in comps},
            'discovery_sources': {c: ['fallback_stub'] for c in comps},
            'market_insights': {
                'market_analysis': {
                    'total_identified_competitors': len(comps),
                    'direct_threats': min(4, len(comps)),
                    'market_fragmentation': 'Medium',
                    'category': category
                },
                'competitive_landscape': {},
                'strategic_recommendations': ['Fallback discovery used: install real discovery module for better results']
            }
        }

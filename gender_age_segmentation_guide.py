"""
Enhanced Customer Segmentation with Age + Gender API Integration
=============================================================
This script shows how to modify your customer segmentation to use:
1. Age groups (18-24, 25-34, 35-44, 45-54, 55+)
2. Gender (Male, Female, Non-binary)
3. Real API data from Census Bureau, Facebook Marketing API, etc.
"""

# Gender-based segmentation example for your system
GENDER_AGE_SEGMENTS = {
    # Male segments by age
    "Male 18-24": {
        "demographics": {"gender": "Male", "age_min": 18, "age_max": 24},
        "api_sources": ["Census Bureau", "Facebook Marketing API", "Google Analytics"],
        "characteristics": {
            "tech_adoption": 0.85,
            "gaming_interest": 0.75,
            "sports_interest": 0.65,
            "price_sensitivity": 0.70,
            "brand_loyalty": 0.45
        }
    },
    "Male 25-34": {
        "demographics": {"gender": "Male", "age_min": 25, "age_max": 34},
        "api_sources": ["Census Bureau", "Facebook Marketing API", "LinkedIn API"],
        "characteristics": {
            "tech_adoption": 0.80,
            "career_focused": 0.85,
            "family_oriented": 0.60,
            "price_sensitivity": 0.65,
            "brand_loyalty": 0.55
        }
    },
    "Male 35-44": {
        "demographics": {"gender": "Male", "age_min": 35, "age_max": 44},
        "api_sources": ["Census Bureau", "Facebook Marketing API", "Consumer Survey APIs"],
        "characteristics": {
            "tech_adoption": 0.70,
            "family_oriented": 0.80,
            "career_established": 0.85,
            "price_sensitivity": 0.50,
            "brand_loyalty": 0.70
        }
    },
    
    # Female segments by age  
    "Female 18-24": {
        "demographics": {"gender": "Female", "age_min": 18, "age_max": 24},
        "api_sources": ["Census Bureau", "Instagram API", "TikTok Analytics"],
        "characteristics": {
            "social_media_usage": 0.90,
            "fashion_interest": 0.80,
            "sustainability_concern": 0.75,
            "price_sensitivity": 0.75,
            "influencer_trust": 0.70
        }
    },
    "Female 25-34": {
        "demographics": {"gender": "Female", "age_min": 25, "age_max": 34},
        "api_sources": ["Census Bureau", "Facebook Marketing API", "Pinterest API"],
        "characteristics": {
            "career_focused": 0.85,
            "health_wellness": 0.80,
            "family_planning": 0.65,
            "price_sensitivity": 0.60,
            "quality_focused": 0.80
        }
    },
    "Female 35-44": {
        "demographics": {"gender": "Female", "age_min": 35, "age_max": 44},
        "api_sources": ["Census Bureau", "Facebook Marketing API", "Consumer Research APIs"],
        "characteristics": {
            "family_oriented": 0.85,
            "health_conscious": 0.85,
            "time_constrained": 0.80,
            "price_sensitivity": 0.45,
            "brand_loyalty": 0.75
        }
    }
}

def get_api_data_sources_for_gender_segmentation():
    """Available APIs for gender + age segmentation"""
    return {
        "Census Bureau API": {
            "endpoint": "https://api.census.gov/data/2021/acs/acs1",
            "data_provided": "Population by age and gender",
            "requires_key": True,
            "cost": "Free"
        },
        "Facebook Marketing API": {
            "endpoint": "https://graph.facebook.com/v18.0/insights",
            "data_provided": "Audience demographics by age and gender",
            "requires_key": True,
            "cost": "Free for basic"
        },
        "Google Analytics Demographics API": {
            "endpoint": "https://analyticsreporting.googleapis.com/v4/reports:batchGet",
            "data_provided": "Website visitor demographics",
            "requires_key": True,
            "cost": "Free"
        },
        "Consumer Expenditure Survey API": {
            "endpoint": "https://api.bls.gov/publicAPI/v2/timeseries/data/",
            "data_provided": "Spending patterns by demographics",
            "requires_key": True,
            "cost": "Free"
        },
        "Pew Research API": {
            "endpoint": "Custom research data endpoints",
            "data_provided": "Social trends by age and gender",
            "requires_key": False,
            "cost": "Free for academic use"
        }
    }

print("🎯 Age + Gender Segmentation Strategy")
print("="*50)
print()
print("📊 RECOMMENDED SEGMENTS:")
for segment_name, data in GENDER_AGE_SEGMENTS.items():
    demo = data['demographics']
    print(f"   {segment_name}: {demo['gender']} aged {demo['age_min']}-{demo['age_max']}")

print()
print("🔑 API DATA SOURCES:")
apis = get_api_data_sources_for_gender_segmentation()
for api_name, info in apis.items():
    print(f"   ✅ {api_name}: {info['data_provided']} ({info['cost']})")

print()
print("💡 IMPLEMENTATION STEPS:")
print("   1. Modify customer_segmentation_agent.py")
print("   2. Add gender parameter to API calls")
print("   3. Update segment creation logic")
print("   4. Integrate with Census Bureau API")
print("   5. Add Facebook Marketing API gender filtering")
print("   6. Update visualization components")
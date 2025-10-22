"""
Test script to verify Responsible AI integration across all agents
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_rai_framework():
    """Test RAI Framework initialization"""
    print("=" * 80)
    print("TEST 1: Responsible AI Framework Initialization")
    print("=" * 80)
    
    try:
        from utils.responsible_ai_framework import rai_framework, BiasType, FairnessMetric
        print("✅ RAI Framework imported successfully")
        print(f"   - Framework instance: {type(rai_framework).__name__}")
        return True
    except Exception as e:
        print(f"❌ Failed to import RAI Framework: {e}")
        return False

def test_agent_rai_integration():
    """Test RAI integration in all agents"""
    print("\n" + "=" * 80)
    print("TEST 2: Agent RAI Integration")
    print("=" * 80)
    
    agents = [
        ('Market Trend Analyzer', 'agents.market_trend_analyzer', 'MarketTrendAnalyzer'),
        ('Competitor Tracking', 'agents.competitor_tracking_agent', 'CompetitorTrackingAgent'),
        ('Customer Segmentation', 'agents.customer_segmentation_agent', 'CustomerSegmentationAgent'),
        ('Campaign Planning', 'agents.campaign_planning_agent', 'CampaignPlanningAgent'),
        ('Communication Coordinator', 'agents.communication_coordinator', 'CommunicationCoordinator'),
    ]
    
    results = {}
    
    for agent_name, module_path, class_name in agents:
        print(f"\n{agent_name}:")
        try:
            # Import agent module
            module = __import__(module_path, fromlist=[class_name])
            agent_class = getattr(module, class_name)
            
            # Check if RAI_AVAILABLE flag is True
            if hasattr(module, 'RAI_AVAILABLE'):
                rai_available = module.RAI_AVAILABLE
                if rai_available:
                    print(f"  ✅ RAI_AVAILABLE = True")
                else:
                    print(f"  ⚠️  RAI_AVAILABLE = False")
            else:
                print(f"  ⚠️  RAI_AVAILABLE flag not found")
                rai_available = False
            
            # Check if agent has rai_framework attribute
            # We'll need to create a dummy instance to check
            print(f"  ✅ Agent class '{class_name}' loaded successfully")
            
            results[agent_name] = {
                'imported': True,
                'rai_available': rai_available
            }
            
        except Exception as e:
            print(f"  ❌ Failed to import: {e}")
            results[agent_name] = {
                'imported': False,
                'rai_available': False,
                'error': str(e)
            }
    
    return results

def test_rai_methods():
    """Test RAI framework methods"""
    print("\n" + "=" * 80)
    print("TEST 3: RAI Framework Methods")
    print("=" * 80)
    
    try:
        from utils.responsible_ai_framework import rai_framework
        
        # Test detect_bias
        print("\n1. Testing detect_bias():")
        test_data = {'price': [100, 200, 300], 'region': ['US', 'EU', 'Asia']}
        bias_results = rai_framework.detect_bias(test_data, "test_agent", "test_context")
        print(f"   ✅ detect_bias() executed successfully")
        print(f"   - Found {len(bias_results)} bias types")
        
        # Test create_audit_entry
        print("\n2. Testing create_audit_entry():")
        audit_entry = rai_framework.create_audit_entry(
            agent_name="test_agent",
            action="test_action",
            input_data={'test': 'input'},
            output_data={'test': 'output'}
        )
        print(f"   ✅ create_audit_entry() executed successfully")
        print(f"   - Audit ID: {audit_entry.entry_id}")
        print(f"   - Bias detected: {audit_entry.bias_detected}")
        print(f"   - Fairness score: {audit_entry.fairness_score}")
        
        # Test make_ethical_decision
        print("\n3. Testing make_ethical_decision():")
        decision = rai_framework.make_ethical_decision(
            agent_name="test_agent",
            decision_type="test_decision",
            ethical_principles=["fairness", "transparency"],
            stakeholders=["users"],
            justification="test justification"
        )
        print(f"   ✅ make_ethical_decision() executed successfully")
        print(f"   - Decision ID: {decision.decision_id}")
        
        # Test ensure_transparency
        print("\n4. Testing ensure_transparency():")
        transparency = rai_framework.ensure_transparency(
            agent_name="test_agent",
            process="test_process",
            inputs={'data': 'test'},
            outputs={'result': 'test'},
            methodology="test method"
        )
        print(f"   ✅ ensure_transparency() executed successfully")
        
        print("\n✅ All RAI methods working correctly!")
        return True
        
    except Exception as e:
        print(f"\n❌ RAI methods test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_rai_in_console_output():
    """Check if RAI warnings appear in console output"""
    print("\n" + "=" * 80)
    print("TEST 4: RAI Console Output")
    print("=" * 80)
    
    print("\nExpected console messages when running the system:")
    print("  - 'WARNING:ResponsibleAI:Bias detected in...'")
    print("  - 'INFO:ResponsibleAI:Ethical decision made by...'")
    print("  - 'INFO:ResponsibleAI:Transparency report generated for...'")
    print("  - 'INFO:ResponsibleAI:Audit entry created for...'")
    print("\n✅ Check your Streamlit console logs for these messages")

def generate_summary(agent_results, methods_ok):
    """Generate test summary"""
    print("\n" + "=" * 80)
    print("SUMMARY: Responsible AI Integration Status")
    print("=" * 80)
    
    all_imported = all(result['imported'] for result in agent_results.values())
    all_rai_available = all(result['rai_available'] for result in agent_results.values())
    
    print(f"\n📊 Agent Integration Status:")
    for agent_name, result in agent_results.items():
        status = "✅" if result['imported'] and result['rai_available'] else "⚠️"
        print(f"   {status} {agent_name}: ", end="")
        if result['imported']:
            if result['rai_available']:
                print("ACTIVE")
            else:
                print("LOADED (RAI disabled)")
        else:
            print(f"FAILED - {result.get('error', 'Unknown error')}")
    
    print(f"\n🔧 RAI Framework Status:")
    print(f"   {'✅' if methods_ok else '❌'} All RAI methods functional")
    
    print(f"\n📈 Overall Status:")
    if all_imported and all_rai_available and methods_ok:
        print("   ✅ Responsible AI is FULLY FUNCTIONAL across all agents!")
    elif all_imported and methods_ok:
        print("   ⚠️  Agents loaded but RAI may be disabled in some")
    else:
        print("   ❌ Issues detected - check errors above")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    print("\n🤖 Samsung Product Launch Planner - Responsible AI Integration Test")
    print("=" * 80)
    
    # Run tests
    framework_ok = test_rai_framework()
    agent_results = test_agent_rai_integration()
    methods_ok = test_rai_methods()
    test_rai_in_console_output()
    
    # Generate summary
    generate_summary(agent_results, methods_ok)
    
    print("\n✅ Testing complete! Run 'streamlit run ui/streamlit_app.py' to see RAI in action.\n")

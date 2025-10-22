Responsible AI verification checklist

Quick checks to validate the three core principles are active in the system:

1) Fairness
- Review `responsible_ai/audit_log.json` for actions that mention regional targeting or unequal budgets.
- Spot-check segment definitions in `Customer Segmentation` tab to ensure protected attributes are not used as primary split features.

2) Transparency
- For any prediction (market forecast, segment), ensure the UI shows the top 3 features and a confidence score.
- Audit log should record when an agent produced a suggestion and what inputs it used.

3) Accountability
- Check that major actions (campaign finalization, agent assignment) are logged in `responsible_ai/audit_log.json` with actor and timestamp.
- Ensure a human approval step is required before executing campaigns (manual check in UI or logs).

How to test now (manual):
1. Open the Streamlit app and go to "Product Strategy" tab.
2. Under "Pricing Plans & Agent Assignment" assign an agent to a plan and click Save.
3. Open `responsible_ai/audit_log.json` or use the sidebar "Audit Log" expander — you should see a new entry with timestamp, actor=user, action=assign_agent_plan.

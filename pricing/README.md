Pricing feature

Quick Flask app that exposes:
- GET / -> UI
- GET /api/plans -> list of plans
- GET /api/agents -> list of agents
- POST /api/assign {agent_id, plan_id} -> assign an agent to a plan

Run:

1. pip install -r requirements.txt
2. python pricing/app.py

Open http://localhost:8080

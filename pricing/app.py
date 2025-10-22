from flask import Flask, jsonify, request, render_template, send_from_directory
from pathlib import Path
import json

BASE_DIR = Path(__file__).parent
PLANS_FILE = BASE_DIR / "data" / "plans.json"
AGENTS_FILE = BASE_DIR / "data" / "agents.json"

app = Flask(__name__, template_folder=str(BASE_DIR / 'templates'), static_folder=str(BASE_DIR / 'static'))


def read_json(path: Path):
    if not path.exists():
        return []
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/plans')
def get_plans():
    plans = read_json(PLANS_FILE)
    return jsonify(plans)


@app.route('/api/agents')
def get_agents():
    agents = read_json(AGENTS_FILE)
    return jsonify(agents)


@app.route('/api/assign', methods=['POST'])
def assign_agent():
    body = request.json or {}
    agent_id = body.get('agent_id')
    plan_id = body.get('plan_id')
    agents = read_json(AGENTS_FILE)
    # find agent
    for a in agents:
        if a.get('id') == agent_id:
            a['plan_id'] = plan_id
            write_json(AGENTS_FILE, agents)
            return jsonify({'ok': True, 'agent': a})
    return jsonify({'ok': False, 'error': 'agent not found'}), 404


if __name__ == '__main__':
    app.run(debug=True, port=8081)

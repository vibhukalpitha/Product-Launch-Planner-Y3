async function fetchJSON(path) {
  const res = await fetch(path);
  return res.json();
}

function el(tag, cls, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text) e.textContent = text;
  return e;
}

async function load() {
  const plans = await fetchJSON('/api/plans');
  const agents = await fetchJSON('/api/agents');

  const plansDiv = document.getElementById('plans');
  plansDiv.innerHTML = '';

  plans.forEach(plan => {
    const card = el('div', 'plan-card');
    card.appendChild(el('h3', null, `${plan.name} – $${plan.price_per_month}/mo`));
    const ul = el('ul');
    plan.features.forEach(f => ul.appendChild(el('li', null, f)));
    card.appendChild(ul);
    plansDiv.appendChild(card);
  });

  const agentsDiv = document.getElementById('agents');
  agentsDiv.innerHTML = '';
  agents.forEach(agent => {
    const row = el('div', 'agent-row');
    row.appendChild(el('div', 'agent-name', agent.name));
    const select = document.createElement('select');
    select.innerHTML = '<option value="">(no plan)</option>' + plans.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
    select.value = agent.plan_id || '';
    select.addEventListener('change', async () => {
      await fetch('/api/assign', {method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({agent_id: agent.id, plan_id: select.value || null})});
      load();
    });
    row.appendChild(select);
    row.appendChild(el('div', 'agent-status', agent.status));
    agentsDiv.appendChild(row);
  });
}

window.addEventListener('DOMContentLoaded', load);

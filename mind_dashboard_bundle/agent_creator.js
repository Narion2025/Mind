const API_BASE = window.API_BASE || '';

const form = document.getElementById('agentForm');
form.onsubmit = async (e) => {
  e.preventDefault();
  const payload = {
    name: document.getElementById('name').value.trim(),
    farbe: document.getElementById('farbe').value.trim(),
    fokus: document.getElementById('fokus').value.trim(),
    beschreibung: document.getElementById('beschreibung').value.trim()
  };
  const res = await fetch(`${API_BASE}/agents`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  const status = document.getElementById('status');
  if(res.ok){
    status.textContent = 'Agent erstellt';
    form.reset();
  }else{
    status.textContent = 'Fehler: ' + await res.text();
  }
};

const API_BASE = window.API_BASE || '';

async function fetchAnchors() {
  const res = await fetch(`${API_BASE}/anchors`);
  if (!res.ok) return;
  const data = await res.json();
  const tbody = document.querySelector('#anchors tbody');
  tbody.innerHTML = '';
  data.forEach(a => {
    const tr = document.createElement('tr');
    const status = a.online ? 'online' : 'offline';
    tr.innerHTML = `<td>${a.gpt_id}</td><td>${a.identity}</td><td>${a.model}</td><td><span class="badge ${status}">${status}</span></td>`;
    tbody.appendChild(tr);
  });
}

document.getElementById('addBtn').onclick = () => {
  document.getElementById('modal').classList.remove('hidden');
};

document.getElementById('cancelBtn').onclick = () => {
  document.getElementById('modal').classList.add('hidden');
};

document.getElementById('anchorForm').onsubmit = async (e) => {
  e.preventDefault();
  const id = document.getElementById('gpt_id').value;
  const payload = {
    identity: document.getElementById('identity').value,
    model: document.getElementById('model').value,
    version: document.getElementById('version').value,
    online: true
  };
  const res = await fetch(`${API_BASE}/anchors/${id}`, {
    method: 'PUT',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
  });
  if (res.ok) {
    document.getElementById('modal').classList.add('hidden');
    fetchAnchors();
  } else {
    alert('Fehler');
  }
};

fetchAnchors();
setInterval(fetchAnchors, 5000);

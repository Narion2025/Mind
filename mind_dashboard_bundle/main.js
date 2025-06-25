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
    tr.innerHTML = `<td>${a.gpt_id}</td><td>${a.identity}</td><td>${a.model}</td><td><span class="badge ${status}">${status}</span></td><td><button class="pauseBtn" data-id="${a.gpt_id}">Pause</button> <button class="deleteBtn" data-id="${a.gpt_id}">Delete</button></td>`;
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
    op: 'connect',
    identity: document.getElementById('identity').value,
    model: document.getElementById('model').value,
    params: {}
  };
  const res = await fetch(`${API_BASE}/agents/${id}/action`, {
    method: 'POST',
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

document.addEventListener('click', async (e) => {
  if (e.target.classList.contains('pauseBtn')) {
    const id = e.target.dataset.id;
    await fetch(`${API_BASE}/agents/${id}/action`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({op: 'pause'})
    });
    fetchAnchors();
  }
  if (e.target.classList.contains('deleteBtn')) {
    const id = e.target.dataset.id;
    if (!confirm('Delete Agent?')) return;
    await fetch(`${API_BASE}/agents/${id}/action`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({op: 'delete'})
    });
    fetchAnchors();
  }
});

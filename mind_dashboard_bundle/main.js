const API_BASE = window.API_BASE || '';
const ROLES = window.ROLES || ['anchor.read','anchor.write'];

let anchors = [];

async function loadCapabilities() {
  const res = await fetch(`${API_BASE}/capabilities`);
  if (!res.ok) return;
  const models = await res.json();
  const sel = document.getElementById('model');
  sel.innerHTML = '';
  models.forEach(m => {
    const opt = document.createElement('option');
    opt.value = m;
    opt.textContent = m;
    sel.appendChild(opt);
  });
}

function renderAnchors() {
  const tbody = document.querySelector('#anchors tbody');
  tbody.innerHTML = '';
  anchors.forEach(a => {
    const tr = document.createElement('tr');
    const status = a.online ? 'online' : 'offline';
    tr.innerHTML = `<td>${a.gpt_id}</td><td>${a.identity}</td><td>${a.model}</td><td><span class="badge ${status}">${status}</span></td>`;
    tr.onclick = () => showDetail(a);
    tbody.appendChild(tr);
  });
}

async function fetchAnchors() {
  const res = await fetch(`${API_BASE}/anchors`);
  if (!res.ok) return;
  anchors = await res.json();
  renderAnchors();
}

function showDetail(a) {
  document.getElementById('detailTitle').textContent = a.identity;
  document.getElementById('detail').classList.remove('hidden');
  document.getElementById('pauseBtn').onclick = () => sendAction(a.gpt_id, 'pause');
  document.getElementById('resumeBtn').onclick = () => sendAction(a.gpt_id, 'resume');
}

async function sendAction(id, op) {
  await fetch(`${API_BASE}/agents/${id}/action`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({op})
  });
}

function connectWS() {
  const ws = new WebSocket((location.protocol === 'https:' ? 'wss' : 'ws') + '://' + location.host + `${API_BASE}/ws/updates`);
  ws.onmessage = e => {
    const msg = JSON.parse(e.data);
    if (msg.event === 'anchor') {
      const idx = anchors.findIndex(a => a.gpt_id === msg.data.gpt_id);
      if (idx >= 0) anchors[idx] = msg.data; else anchors.push(msg.data);
      renderAnchors();
    }
  };
  ws.onclose = () => setTimeout(connectWS, 1000);
}

document.getElementById('addBtn').onclick = () => {
  document.querySelector('.step1').classList.remove('hidden');
  document.querySelector('.step2').classList.add('hidden');
  document.getElementById('modal').classList.remove('hidden');
};

document.getElementById('nextBtn').onclick = () => {
  document.querySelector('.step1').classList.add('hidden');
  document.querySelector('.step2').classList.remove('hidden');
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

loadCapabilities();
fetchAnchors();
connectWS();

document.querySelectorAll('.hide-write').forEach(el => {
  if (ROLES.includes('anchor.write')) el.style.display='';
});

const API_BASE = window.API_BASE || '';
let functions = [];

function authHeaders(extra={}){
  const token = localStorage.getItem('token');
  return Object.assign({'Authorization': 'Bearer ' + token}, extra);
}

async function loadFunctions(){
  const res = await fetch(`${API_BASE}/functions`, {headers: authHeaders()});
  if(!res.ok) return;
  functions = await res.json();
  renderFunctions();
}

function renderFunctions(){
  const term = document.getElementById('search').value.toLowerCase();
  const groups = {};
  functions.forEach(fn=>{
    if(term && !fn.name.toLowerCase().includes(term) && !fn.group.toLowerCase().includes(term)) return;
    if(!groups[fn.group]) groups[fn.group] = [];
    groups[fn.group].push(fn);
  });
  const container = document.getElementById('groups');
  container.innerHTML = '';
  Object.entries(groups).forEach(([group,fns])=>{
    const sec = document.createElement('section');
    const h = document.createElement('h3');
    h.textContent = group;
    sec.appendChild(h);
    fns.forEach(fn=>{
      const div = document.createElement('div');
      div.className = 'function';
      const color = fn.runtime_status==='running' ? 'green' : (fn.env_missing.length?'orange':'gray');
      div.innerHTML = `<span class="label">${fn.name}</span>
        <span class="pill" style="background:${color}"></span>
        <button class="startBtn" data-name="${fn.name}" ${fn.env_missing.length?'disabled':''}>▶</button>
        <button class="logBtn" data-name="${fn.name}">Logs</button>`;
      div.title = fn.description + (fn.env_missing.length?`\nMissing: ${fn.env_missing.join(', ')}`:'');
      sec.appendChild(div);
    });
    container.appendChild(sec);
  });
}

document.getElementById('search').oninput = renderFunctions;

document.addEventListener('click', async e=>{
  if(e.target.classList.contains('startBtn')){
    const name = e.target.dataset.name;
    await fetch(`${API_BASE}/functions/${encodeURIComponent(name)}/start`,{method:'POST',headers:authHeaders()});
    loadFunctions();
  }
  if(e.target.classList.contains('logBtn')){
    openLogs(e.target.dataset.name);
  }
});

function openLogs(name){
  const drawer=document.getElementById('logDrawer');
  drawer.classList.remove('hidden');
  const pre=document.getElementById('logs');
  pre.textContent='';
  const proto=location.protocol==='https:'?'wss':'ws';
  const ws=new WebSocket(`${proto}://${location.host}/ws/logs/${encodeURIComponent(name)}`);
  ws.onmessage=e=>{pre.textContent+=e.data+'\n';pre.scrollTop=pre.scrollHeight;};
  document.getElementById('closeLogs').onclick=()=>{ws.close();drawer.classList.add('hidden');};
}

document.getElementById('openTerminal').onclick = () => {
  const drawer = document.getElementById('terminalDrawer');
  drawer.classList.remove('hidden');
  const pre = document.getElementById('terminalOutput');
  pre.textContent = '';
  const input = document.getElementById('terminalInput');
  const proto = location.protocol === 'https:' ? 'wss' : 'ws';
  const ws = new WebSocket(`${proto}://${location.host}/ws/terminal`);
  ws.onmessage = e => { pre.textContent += e.data; pre.scrollTop = pre.scrollHeight; };
  input.onkeydown = ev => {
    if(ev.key === 'Enter'){
      ws.send(input.value + '\n');
      input.value = '';
    }
  };
  document.getElementById('closeTerminal').onclick = () => { ws.close(); drawer.classList.add('hidden'); };
};

// Anchor logic from legacy dashboard
async function fetchAnchors(){
  const res=await fetch(`${API_BASE}/anchors`, {headers: authHeaders()});
  if(!res.ok) return;
  const data=await res.json();
  const container=document.getElementById('agents');
  container.innerHTML='';
  data.forEach(a=>{
    const div=document.createElement('div');
    const status=a.online?'online':'offline';
    div.innerHTML=`<span>${a.gpt_id} (${a.model})</span> <span class="badge ${status}">${status}</span>`;
    container.appendChild(div);
  });
}

loadFunctions();
fetchAnchors();
setInterval(()=>{loadFunctions();fetchAnchors();},5000);

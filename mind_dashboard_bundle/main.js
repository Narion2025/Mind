const API_BASE = window.API_BASE || '';
let functions = [];
let secrets = [];

async function loadFunctions(){
  const res = await fetch(`${API_BASE}/functions`);
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
    await fetch(`${API_BASE}/functions/${encodeURIComponent(name)}/start`,{method:'POST'});
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

// Settings panel
async function loadSecrets(){
  const res = await fetch(`${API_BASE}/secrets`, {headers:{'X-Role':'secrets.edit'}});
  if(!res.ok) return;
  secrets = await res.json();
  const list = document.getElementById('secretList');
  list.innerHTML='';
  secrets.forEach(s=>{
    const li=document.createElement('li');
    li.textContent=`${s.key}: ${s.masked}`;
    const del=document.createElement('button');
    del.textContent='Del';
    del.dataset.key=s.key;
    li.appendChild(del);
    list.appendChild(li);
  });
}

document.getElementById('settingsBtn').onclick=()=>{
  const p=document.getElementById('settingsPanel');
  p.classList.toggle('hidden');
  if(!p.classList.contains('hidden')) loadSecrets();
};

document.getElementById('closeSettings').onclick=()=>{
  document.getElementById('settingsPanel').classList.add('hidden');
};

document.getElementById('envFile').onchange=async e=>{
  const file=e.target.files[0];
  if(!file) return;
  const fd=new FormData();
  fd.append('file', file);
  await fetch(`${API_BASE}/secrets/upload`,{method:'POST',headers:{'X-Role':'secrets.edit'},body:fd});
  loadSecrets();
};

document.getElementById('kvForm').onsubmit=async e=>{
  e.preventDefault();
  const key=document.getElementById('keyName').value;
  const val=document.getElementById('keyValue').value;
  await fetch(`${API_BASE}/secrets/upload`,{
    method:'POST',
    headers:{'Content-Type':'application/json','X-Role':'secrets.edit'},
    body:JSON.stringify({key:key,value:val})
  });
  e.target.reset();
  loadSecrets();
};

document.getElementById('secretList').addEventListener('click',async e=>{
  if(e.target.tagName==='BUTTON'){
    const key=e.target.dataset.key;
    await fetch(`${API_BASE}/secrets/${encodeURIComponent(key)}`,{method:'DELETE',headers:{'X-Role':'secrets.edit'}});
    loadSecrets();
  }
});

// Anchor logic from legacy dashboard
async function fetchAnchors(){
  const res=await fetch(`${API_BASE}/anchors`);
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

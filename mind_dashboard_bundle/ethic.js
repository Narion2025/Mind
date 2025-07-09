const API_BASE = window.API_BASE || '';
const balance = document.getElementById('balance');

async function load(){
  const res = await fetch(`${API_BASE}/ethic`, {
    headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
  });
  if(res.ok){
    const data = await res.json();
    balance.textContent = data.coins;
  }
}

document.getElementById('mineBtn').onclick = async () => {
  const res = await fetch(`${API_BASE}/ethic/resonate`, {
    method: 'POST',
    headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
  });
  if(res.ok){
    const data = await res.json();
    balance.textContent = data.coins;
  }
};

load();

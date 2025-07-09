const API_BASE = window.API_BASE || '';

const status = document.getElementById('status');

document.getElementById('loginForm').onsubmit = async e => {
  e.preventDefault();
  const payload = {
    username: document.getElementById('loginUser').value.trim(),
    password: document.getElementById('loginPass').value
  };
  const res = await fetch(`${API_BASE}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if(res.ok){
    const data = await res.json();
    localStorage.setItem('token', data.token);
    location.href = 'mind_control.html';
  } else {
    status.textContent = 'Login fehlgeschlagen';
  }
};

document.getElementById('regForm').onsubmit = async e => {
  e.preventDefault();
  const payload = {
    username: document.getElementById('regUser').value.trim(),
    email: document.getElementById('regEmail').value.trim(),
    password: document.getElementById('regPass').value
  };
  const res = await fetch(`${API_BASE}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if(res.ok){
    status.textContent = 'Registriert. Bitte einloggen.';
  }else{
    status.textContent = 'Registrierung fehlgeschlagen';
  }
};

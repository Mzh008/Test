async function login() {
  const username = document.getElementById('login-username').value;
  const password = document.getElementById('login-password').value;
  const res = await fetch('/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  if (res.ok) {
    window.location = 'chat.html';
  } else {
    alert('Login failed');
  }
}

async function register() {
  const username = document.getElementById('register-username').value;
  const password = document.getElementById('register-password').value;
  const res = await fetch('/api/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  if (res.ok) {
    alert('Registered successfully');
  } else {
    alert('Registration failed');
  }
}

async function sendMessage() {
  const input = document.getElementById('chat-input');
  const message = input.value;
  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  });
  if (res.ok) {
    const data = await res.json();
    addChat('You: ' + message);
    addChat('Bot: ' + data.reply);
    input.value = '';
  } else if (res.status === 401) {
    window.location = 'index.html';
  }
}

async function logout() {
  await fetch('/api/logout', { method: 'POST' });
  window.location = 'index.html';
}

function addChat(text) {
  const box = document.getElementById('chat-box');
  const div = document.createElement('div');
  div.textContent = text;
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}

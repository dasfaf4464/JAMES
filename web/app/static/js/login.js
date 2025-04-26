function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
  
    fetch('/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        // 로그인 성공 시 홈 페이지로 이동
        window.location.href = data.redirect_url;
      } else {
        alert(data.message);
      }
    })
    .catch(err => {
      console.error('Login error:', err);
    });
  }
document.addEventListener("DOMContentLoaded", function () {
  document.getElementById('login-button').addEventListener('click', (event) => {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    })
      .then(res => res.json())
      .then(data => {
        if (data.isSuccess) {
          window.location.href = data.redirect_url;
        } else {
          alert(data.message);
        }
      })
      .catch(err => {
        console.error('Login error:', err);
      });
  });

  document.getElementById('register-button').addEventListener('click', (event) => {
    event.preventDefault();
    window.location.href = '/register';
  });
});


document.addEventListener('DOMContentLoaded', () => {
  fetch('/auth/check_key')
    .then(response => {
      if (!response.ok) {
        throw new Error('서버 응답 오류');
      }
      return response.json();
    })
    .then(data => {
      console.log("사용자 인증 응답:", data);

      if (data.redirect_url) {
        if (window.location.origin != data.redirect_url) {
          window.location.href = data.redirect_url;
        }
      }

      if (data.message) {
        console.log("서버 메시지:", data.message);
      }
    })
    .catch(error => {
      console.error("인증 확인 실패:", error);
    });
});

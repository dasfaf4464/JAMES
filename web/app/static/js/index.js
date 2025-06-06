/**
 * 로그인 버튼 클릭시 id, pw 를 auth/login으로 전달
 */
document.addEventListener("DOMContentLoaded", function () {
  document.getElementById('login-button').addEventListener('click', (event) => {
    event.preventDefault();

    const id = document.getElementById('username').value;
    const pw = document.getElementById('password').value;

    fetch('/api/user/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, pw })
    })
      .then(res => res.json())
      .then(data => {
        if (data.login_result) {
          alert(data.login_message)
          window.location.href = '/home';
        } else {
          alert(data.login_message);
        }
      })
      .catch(err => {
        console.error('Login error:', err);
      });
  });
});


/**
 * 회원가입 버튼 클릭시 회원가입 페이지로 이동
 */
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('register-button').addEventListener('click', (event) => {
    event.preventDefault();
    window.location.href = '/register';
  });
});


/**
 * 세션 생성 모달 생성 및 api 연결
 */
document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("sessionModal");
  const openBtn = document.getElementById("create-session-button");
  const closeBtn = document.getElementById("closeModal");

  openBtn.addEventListener("click", function (event) {
    event.preventDefault();
    modal.style.display = "block";
  });

  closeBtn.addEventListener("click", function () {
    modal.style.display = "none";
  });

  window.addEventListener("click", function (event) {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  });

  document.getElementById("submitSessionBtn").addEventListener("click", (event) => {
    event.preventDefault();

    const title = document.getElementById("sessionTitleInput").value.trim();
    const description = document.getElementById("sessionexplain").value;
    const pw = document.getElementById("sessionPw").value;

    if (title) {
      modal.style.display = "none";

      fetch('/api/session/create/index', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description, pw })
      })
        .then(res => res.json())
        .then(data => {
          if (data.session_result) {
            alert(data.session_create_message + data.session_code);
            window.location.href = 'session/' + data.session_code;
          }
        })
        .catch(err => {
          alert("세션 생성 중 오류가 발생했습니다.");
          console.error(err);
        });

      document.getElementById("sessionTitleInput").value = "";
      document.getElementById("sessionexplain").value = "";
      document.getElementById("sessionPw").value = "";
    }
  });
});


/**
 * 세션 코드 입력후 그 코드로 이동
 */
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById('into-session-button').addEventListener('click', (event) => {
    event.preventDefault();

    const session_code = document.getElementById('session-code').value.trim();

    if (!session_code) {
      alert("세션 코드를 입력해주세요");
      return;
    }
    window.location.href = 'session/' + session_code;
  });
});


/**
 * 세션 코드 입력칸을 숫자와 대문자로 자동 변환
 */
function formatSessionCodeInput(value) {
  const cleaned = value.replace(/[^a-zA-Z0-9]/g, '').toUpperCase();
  const limited = cleaned.substring(0, 12);
  const groups = limited.match(/.{1,4}/g);
  return groups ? groups.join('-') : '';
}

document.addEventListener('DOMContentLoaded', function () {
  const sessionInput = document.getElementById('session-code');
  if (!sessionInput) return;

  let lastFormatted = '';

  sessionInput.addEventListener('input', () => {
    const raw = sessionInput.value.replace(/-/g, '');
    const formatted = formatSessionCodeInput(raw);
    if (formatted !== lastFormatted) {
      sessionInput.value = formatted;
      lastFormatted = formatted;
    }
  });
});
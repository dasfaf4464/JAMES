/**
 * 사용자 쿠키확인 및 발급
 */
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

/**
 * 로그인 버튼 클릭시 id, pw 를 auth/login으로 전달
 */
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
 * 세션 생성 코드 필요
 */


/**
 * 세션 코드 입력후 그 코드로 이동
 */
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById('into-session-button').addEventListener('click', (event) => {
    event.preventDefault();

    const session_code = document.getElementById('session-code').value.trim()

    if (!session_code) {
      alert("세션 코드를 입력해주세요");
      return;
    }

    fetch('room/join', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_code: session_code })
    })
      .then(res => res.json())
      .then(data => {
        if (data.success == true) {
          window.location.href = `/session/${session_code}`
        } else {
          alert("세션에 참여하지 못했습니다.")
        }
      })

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
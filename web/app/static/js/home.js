/**
 * 메뉴 - 프로필로 이동
 */
document.addEventListener("DOMContentLoaded", function () {
  document.getElementById('history-button').addEventListener('click', (event) => {
    event.preventDefault();
    window.location.href = '/profile';
  });
});

/**
 * 메뉴 - 로그아웃 버튼
 */
document.addEventListener("DOMContentLoaded", function () {
  document.getElementById('logout-button').addEventListener('click', (event) => {
    event.preventDefault();

    fetch('/api/user/logout', {
      method: 'POST'
    })
      .then(res => res.json())
      .then(data => {
        if (data.logout_result) {
          alert(data.logout_message)
          window.location.href = '/';
        } else {
          alert(data.message);
        }
      })
      .catch(err => {
        console.error('Logout error:', err);
      });
  });
});


document.getElementById("toggle-panel-button").addEventListener("click", function () {
  document.querySelector(".side-panel").classList.toggle("active");
});


document.getElementById("nav-toggle").addEventListener("click", () => {
  document.getElementById("nav-menu").classList.toggle("active");
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
    const temporaryInput = document.querySelector('input[name="chk_info"]:checked');
    console.log(temporaryInput)
    const pw = document.getElementById("sessionPw").value

    if (!temporaryInput) {
      alert("임시 여부를 선택해주세요.");
      return;
    }

    const temporary = temporaryInput.value;

    if (title) {
      modal.style.display = "none";

      fetch('/api/session/create/home', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description, temporary, pw })
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

    const session_code = document.getElementById('session-code').value.trim()

    if (!session_code) {
      alert("세션 코드를 입력해주세요");
      return;
    }

    window.location.href = `/session/${session_code}`;

  });
});

/**
 * 사이드 패널에서 세션 코드 입력시 숫자 영어 대문자 자동 변환
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

/**
 * 사용자가 현재 참여 중인 세션을 보여주는 최대 개수 설정(모바일:4 데스크탑:6) 
 * 참여 중인 세션 방 리스트 정보를 받아와서 보여줌
 */
document.addEventListener("DOMContentLoaded", () => {
  let currentPage = 0;

  function getItemsPerPage() {
    return window.matchMedia("(max-width: 768px)").matches ? 4 : 6;
  }

  function fetchSessions(page, size) {
    fetch(`/api/user/get/my_sessions?page=${page}&size=${size}`)
      .then(res => res.json())
      .then(data => {
        const sessionGroup = document.querySelector('.session-group');
        sessionGroup.innerHTML = '';

        data.forEach(sessions => {
          const li = document.createElement('li');
          li.className = 'session-group-item';

          li.innerHTML = `
            <p class="session-title">${sessions.name}</p>
            <p class="session-info">현재 입장 인원: ${sessions.people} <br>질문 수: ${sessions.questions}</p>
            <p class="session-period">${sessions.type}</p>
            <img class="session-icon" src="../static/image/computer.svg">
          `;

          li.addEventListener('click', () => {
            fetch(`/api/session/get/detail?session_code=${sessions.session_key}`)
              .then(res => res.json())
              .then(detail => {
                sessionPanel(detail);
              })
              .catch(err => {
                console.error('세션 상세 정보 불러오기 실패:', err);
              });
          });

          sessionGroup.appendChild(li);
        });

        document.getElementById("frontB").disabled = (page === 0);
        document.getElementById("backB").disabled = data.length < size;
      })
      .catch(error => {
        console.error("세션 불러오기 실패:", error);
      });
  }

  fetchSessions(currentPage, getItemsPerPage());

  document.getElementById("frontB").addEventListener("click", () => {
    if (currentPage > 0) {
      currentPage--;
      fetchSessions(currentPage, getItemsPerPage());
    }
  });

  document.getElementById("backB").addEventListener("click", () => {
    currentPage++;
    fetchSessions(currentPage, getItemsPerPage());
  });

  window.addEventListener("resize", () => {
    currentPage = 0;
    fetchSessions(currentPage, getItemsPerPage());
  });
});

/**
 * sessionPanel 생성 함수 구현
 */
function sessionPanel(session) {
  const panel = document.querySelector(".side-panel");
  const myPanel = panel.innerHTML;

  const returnMyPanel = () => {
    panel.innerHTML = myPanel;
  };

  panel.innerHTML = `
    <div class="session-panel-wrapper">
      <button id="exit-button"><img src="../static/image/cancle.svg"></button>
      <br><br><h3>${session.name}</h3>

      <p id="session-create-day">세션 생성일: ${session.created_date || "-"}</p>

      <div class="session-info-box">
        <p id="session-description">${session.description || "설명 없음"}</p>
      </div>

      <div class="session-info-box">
        <p>현재 참여 인원수 : ${session.people}</p>
      </div>

      <div class="session-info-box">
        <p>올라온 질문 수 : ${session.questions}</p>
      </div>

      <button id="join-session">세션 입장하기</button>
      <button id="exit-session">세션 나가기</button>

      <div class="session-info-box">
        <p>세션 입장 시간 : ${session.entered_at || "-"}</p>
      </div>
      <div class="session-info-box">
        <p>세션 생성 시간 : ${session.created_time || "-"}</p>
      </div>
    </div>
  `;

  document.getElementById('exit-button').addEventListener('click', returnMyPanel);
  document.getElementById('join-session').addEventListener('click', () => {
    window.location.href = `/session/${session.session_key}`;
    console.log(session.session_key)
  });
  document.getElementById('exit-session').addEventListener('click', () => {
    const sessionCode = session.session_key;

    if (!sessionCode) {
      alert("세션 코드가 없습니다.");
      return;
    }

    fetch('api/user/exit/session', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ session_code: sessionCode })
    })
      .then(res => res.json())
      .then(data => {
        if (data.exit_result) {
          alert(data.exit_message);
          window.location.reload();
        } else {
          alert(data.exit_message);
        }
      })
      .catch(err => {
        console.error("나가기 요청 실패:", err);
        alert("오류가 발생했습니다.");
      });
  });
}
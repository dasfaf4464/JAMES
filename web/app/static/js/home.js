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

/**
 * 세션 설명 사이드 패널 생성
 */
document.addEventListener("DOMContentLoaded", () => {
  const panel = document.getElementsByClassName("side-panel")[0];
  const myPanel = panel.innerHTML;

  const returnMyPanel = () => {
    panel.innerHTML = myPanel;
  };

  const sessionPanel = () => {
    panel.innerHTML = `
        <div class="session-panel-wrapper">
            <button id="exit-button" onclick="returnMyPanel()"><img src="../static/image/cancle.svg"></button>
            <br><br><h3>session title</h3>

            <p id="session-create-day">세션 생성일: </p>

            <div class="session-info-box">
                <p id="session-discription">설명이 깁니다. 설명이 깁니다. 설명이 깁니다. 설명이 깁니다. 설명이 깁니다.</p>
            </div>

            <div class="session-info-box">
                <p>현재 참여 인원수 : </p>
            </div>

            <div class="session-info-box">
                <p>올라온 질문 수 : </p>
            </div>

            <button id="join-session">세션 입장하기</button>
            <button id="exit-session">세션 나가기</button>

            <div class="session-info-box">
                <p>세션 입장 시간 : </p>
            </div>
                        <div class="session-info-box">
                <p>세션 생성 시간 : </p>
            </div>
        </div>
    `;

    document.getElementById('exit-button').addEventListener('click', returnMyPanel);
  };

  document.querySelectorAll('.session-list ul li').forEach(sessionItem => {
    sessionItem.addEventListener('click', () => {
      sessionPanel();
    });
  });
});

var sessionList = document.querySelectorAll('.session-list ul li');

for (var i = 0; i < sessionList.length; i++) {
  sessionList[i].addEventListener('click', function () {
    sessionPanel();
  });
}

function returnMyPanel() {
  panel.innerHTML = myPanel;
}

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

    if (!temporaryInput) {
      alert("임시 여부를 선택해주세요.");
      return;
    }

    const temporary = temporaryInput.value;

    if (title) {
      modal.style.display = "none";
      let session_code = null;

      fetch('/room/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description, temporary })
      })
        .then(res => res.json())
        .then(data => {
          if (data.error == false) {
            alert("세션이 생성되었습니다.\n세션 코드 : " + data.session_code);
            session_code = data.session_code;
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
          } else {
            alert("세션 생성 중 오류가 발생했습니다.\n오류 코드: " + data.error);
          }
        })
        .catch(err => {
          alert("서버와 통신 중 오류가 발생했습니다.");
          console.error(err);
        });

      document.getElementById("sessionTitleInput").value = "";
      document.getElementById("sessionexplain").value = "";
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
 * 이거 뭔지 주석좀
 */
document.addEventListener("DOMContentLoaded", () => {
  const sessionItems = document.querySelectorAll(".session-group-item");

  // 화면 크기에 따라 한 페이지에 보여줄 개수를 설정
  function getItemsPerPage() {
    return window.matchMedia("(max-width: 768px)").matches ? 4 : 6;
  }

  let itemsPerPage = getItemsPerPage();
  let currentPage = 0;

  function showPage(page) {
    itemsPerPage = getItemsPerPage(); // 현재 화면 크기에 따라 업데이트
    const start = page * itemsPerPage;
    const end = start + itemsPerPage;

    sessionItems.forEach((item, index) => {
      item.style.display = (index >= start && index < end) ? "flex" : "none";
    });

    document.getElementById("frontB").disabled = (page === 0);
    document.getElementById("backB").disabled = (end >= sessionItems.length);
  }

  showPage(currentPage);

  document.getElementById("frontB").addEventListener("click", () => {
    if (currentPage > 0) {
      currentPage--;
      showPage(currentPage);
    }
  });

  document.getElementById("backB").addEventListener("click", () => {
    if ((currentPage + 1) * getItemsPerPage() < sessionItems.length) {
      currentPage++;
      showPage(currentPage);
    }
  });

  // 창 크기 변경 시 자동 업데이트 (선택사항)
  window.addEventListener("resize", () => {
    currentPage = 0;
    showPage(currentPage);
  });
});

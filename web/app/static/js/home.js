document.addEventListener("DOMContentLoaded", function () {
  document.getElementById('history-button').addEventListener('click', (event) => {
    event.preventDefault();
    window.location.href = '/history';
});
});

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


document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('logout-button').addEventListener('click', (event) => {
        event.preventDefault();

        fetch('/auth/logout', {
            method: 'POST'
        })
            .then(res => res.json())
            .then(data => {
                if (data.isSuccess) {
                    alert(data.message)
                    window.location.href = data.redirect_url;
                } else {
                    alert(data.message);
                }
            })
            .catch(err => {
                console.error('Logout error:', err);
            });
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

  document.getElementById("submitSessionBtn").addEventListener("click", () => {
    const title = document.getElementById("sessionTitleInput").value.trim();
    if (title) {
      alert(`새 세션 제목: "${title}"`);
      modal.style.display = "none";
      document.getElementById("sessionTitleInput").value = "";
      // TODO: 서버에 세션 생성 요청 보내기
    }
  });

});document.addEventListener("DOMContentLoaded", () => {
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
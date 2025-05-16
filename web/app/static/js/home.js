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
});

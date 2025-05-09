var panel = document.getElementsByClassName("side-panel")[0];
const myPanel = document.getElementsByClassName("side-panel")[0].innerHTML;

function sessionPanel() {
    panel.innerHTML = `
        <div class="session-panel-wrapper">
        <button id="exit-button" onclick="returnMyPanel()"><img src="../static/image/cancle.svg"></button>
        <p>session title</p>
        <p id="session-discription">diasdasdasdasdasdscription</p>
        <p>현재 참여 인원수 : </p>
        <p>올라온 질문 수 : </p>
        <button id="join-session">세션 입장하기</button>
        <button id="exit-session">세션 나가기</button>
        <p>세션 생성일: </p>
        </div>
    `;
}

var sessionList = document.querySelectorAll('.session-list ul li');

for (var i = 0; i < sessionList.length; i++) {
    sessionList[i].addEventListener('click', function () {
        sessionPanel();
    });
}

function returnMyPanel() {
    panel.innerHTML = myPanel;
}

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

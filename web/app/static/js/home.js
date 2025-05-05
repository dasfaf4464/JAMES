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
    sessionList[i].addEventListener('click', function() {
        sessionPanel();
    });
}

function returnMyPanel() {
    panel.innerHTML = myPanel;
}
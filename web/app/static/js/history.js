const actions = ["Unmute를 만난 지 ", "열심히 공부한 지", "질문을 생각한 지", "강연자와 소통한 지",
    "자신감을 얻은 지", "성공을 꿈꾼 지", "성장을 느낀 지", "문제를 해결한 지", "도전을 시작한 지", 
    "열정적인 사람이 된 지"];

let currentActionIndex = 0;

function rotateActionText() {
    const actionElement = document.getElementById("action-text");
    actionElement.textContent = actions[currentActionIndex];
    currentActionIndex = (currentActionIndex + 1) % actions.length;
}

rotateActionText();

setInterval(rotateActionText, 10000);

function myQuestion() {
    const button_color = window.getComputedStyle(document.getElementById("my-question")).backgroundColor;
    document.getElementById('content-box').style.backgroundColor = button_color;
}
  
function myAnswer() {
    const button_color = window.getComputedStyle(document.getElementById("my-answer")).backgroundColor;
    document.getElementById("content-box").style.backgroundColor = button_color;
}

function saving() {
    const button_color = window.getComputedStyle(document.getElementById("saving")).backgroundColor;
    document.getElementById("content-box").style.backgroundColor = button_color;
}

function myProfile() {
    const button_color = window.getComputedStyle(document.getElementById("my-profile")).backgroundColor;
    document.getElementById("content-box").style.backgroundColor = button_color;
}
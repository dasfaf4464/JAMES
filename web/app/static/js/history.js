const actions = ["Unmute를 만난 지 ", "열심히 공부한 지", "질문을 생각한 지", "강연자와 소통한 지",
    "자신감을 얻은 지", "성공을 꿈꾼 지", "성장을 느낀 지", "문제를 해결한 지", "도전을 시작한 지",
    "열정적인 사람이 된 지", "새로운 목표를 세운 지 ", "혼자가 아님을 느낀 지 ", "다시 도전할 용기를 낸 지 ",
    "내 이야기를 꺼낸 지 ", "누군가의 질문에 감동한 지 ", "배움의 재미를 느낀 지 ", "내 생각을 확신하게 된 지 ",
    "처음 손을 들었던 지 ", "공감받는 경험을 한 지 ", "성장을 공유한 지 "];

let currentActionIndex = 0;

function rotateActionText() {
    const actionElement = document.getElementById("action-text");
    actionElement.textContent = actions[currentActionIndex];
    currentActionIndex = (currentActionIndex + 1) % actions.length;
}

rotateActionText();

setInterval(rotateActionText, 10000);
document.addEventListener("DOMContentLoaded", function () {
    const outputDiv = document.querySelector("#content-output");

    const buttons = {
        "내가 한 질문 보기": [
            { title: "질문 1: 자바스크립트란?", content: "자바스크립트는 웹에서 동작하는 프로그래밍 언어입니다." },
            { title: "질문 2: HTTP와 HTTPS?", content: "HTTPS는 암호화된 HTTP 프로토콜입니다." }
        ],
        "내가 한 대답 보기": [
            { title: "대답 1", content: "DOM은 문서 객체 모델입니다." },
            { title: "대답 2", content: "CSS는 스타일을 지정합니다." }
        ],
        "저장한 질의응답 보기": [
            { title: "Q&A 1", content: "Q: 변수란?\nA: 데이터를 저장하는 공간입니다." }
        ]
    };

    const buttonElements = document.querySelectorAll("main > div:first-child button");

    buttonElements.forEach((btn) => {
        btn.addEventListener("click", () => {
            const items = buttons[btn.textContent] || [];
            outputDiv.innerHTML = "";

            items.forEach((item, index) => {
                const li = document.createElement("li");
                li.textContent = item.title;
                li.style.cursor = "pointer";
                li.style.margin = "8px 0";
                li.style.fontWeight = "bold";

                const detail = document.createElement("div");
                detail.textContent = item.content;
                detail.style.display = "none";
                detail.style.paddingLeft = "16px";
                detail.style.color = "#333";

                li.addEventListener("click", () => {
                    detail.style.display = detail.style.display === "none" ? "block" : "none";
                });

                outputDiv.appendChild(li);
                outputDiv.appendChild(detail);
            });

            if (items.length === 0) {
                outputDiv.innerHTML = "<p>내용이 없습니다.</p>";
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('button');
    const contentOutput = document.getElementById('content-output');

    buttons.forEach(button => {
        button.addEventListener('click', function () {
            // 클릭된 버튼의 배경 색상으로 content-output 색상 변경
            const buttonColor = getComputedStyle(button).backgroundColor;
            contentOutput.style.backgroundColor = buttonColor;
        });
    });
});

/**
 * 화면 텍스트 변경
 */

const actions = ["Unmute를 만난 지 ", "열심히 공부한 지", "질문을 생각한 지", "강연자와 소통한 지",
    "자신감을 얻은 지", "성공을 꿈꾼 지", "성장을 느낀 지", "문제를 해결한 지", "도전을 시작한 지",
    "열정적인 사람이 된 지", "새로운 목표를 세운 지 ", "혼자가 아님을 느낀 지 ", "다시 도전할 용기를 낸 지 ",
    "내 이야기를 꺼낸 지 ", "누군가의 질문에 감동한 지 ", "배움의 재미를 느낀 지 ", "내 생각을 확신하게 된 지 ",
    "처음 손을 들었던 지 ", "공감받는 경험을 한 지 ", "성장을 공유한 지", "새로운 길을 걷기 시작한 지",
    "생각을 말로 표현하기 시작한 지", "나의 가능성을 믿기 시작한 지", "혼자가 아니라는 걸 느낀 지",
    "목표를 향해 나아간 지", "포기 대신 도전을 택한 지", "더 나은 내가 되기로 다짐한 지",
    "말 한마디의 힘을 알게 된 지", "내 이야기를 누군가 경청한 지", "배움이 즐거워진 지"];

let currentActionIndex = 0;

function rotateActionText() {
    const actionElement = document.getElementById("action-text");
    actionElement.textContent = actions[currentActionIndex];
    currentActionIndex = (currentActionIndex + 1) % actions.length;
}

rotateActionText();
setInterval(rotateActionText, 10000);

/**
 * 메뉴 메인화면 이동 버튼
 */
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('home-button').addEventListener('click', (event) => {
        event.preventDefault();
        window.location.href = '/home';
    });
});

/**
 * 레이아웃 변경 (3단계: list-view, grid-view, card-view)
 */
document.addEventListener("DOMContentLoaded", function () {
    const layoutButton = document.getElementById("layout-button");
    const containerDiv = document.querySelector(".myQuestionContainer");

    // 초기 상태: list-view 적용, 버튼 텍스트 초기화
    containerDiv.classList.add("list-view");
    layoutButton.textContent = "그리드 레이아웃";

    layoutButton.addEventListener("click", () => {
        if (containerDiv.classList.contains("list-view")) {
            containerDiv.classList.remove("list-view");
            containerDiv.classList.add("grid-view");
            layoutButton.textContent = "카드 레이아웃";
        } else if (containerDiv.classList.contains("grid-view")) {
            containerDiv.classList.remove("grid-view");
            containerDiv.classList.add("card-view");
            layoutButton.textContent = "리스트 레이아웃";
        } else if (containerDiv.classList.contains("card-view")) {
            containerDiv.classList.remove("card-view");
            containerDiv.classList.add("list-view");
            layoutButton.textContent = "그리드 레이아웃";
        }
    });
});

/**
 * 사용자 질문 불러오기 및 표시
 */
document.addEventListener("DOMContentLoaded", function () {
    const container = document.querySelector(".myQuestionContainer ul");
    const questionCountLi = document.createElement("li"); // 질문 개수 표시용 li
    container.prepend(questionCountLi);

    function loadMyQuestions() {
        fetch('/api/user/get/my_questions', { method: 'GET', credentials: 'include' })
            .then(response => {
                if (!response.ok) throw new Error("네트워크 오류");
                return response.json();
            })
            .then(posts => {
                container.innerHTML = ''; // 기존 내용 초기화
                container.appendChild(questionCountLi);

                questionCountLi.textContent = `질문 개수 : ${posts.length}`;

                if (posts.length === 0) {
                    const li = document.createElement("li");
                    li.textContent = "질문이 없습니다.";
                    container.appendChild(li);
                    return;
                }

                posts.forEach(post => {
                    const li = document.createElement("li");
                    li.innerHTML = `
                        <strong>원본 질문:</strong> ${post.original} <br>
                        <strong>LLM 질문:</strong> ${post.llm} <br>
                        <strong>카테고리:</strong> ${post.main} / ${post.sub} / ${post.minor} <br>
                        <small>작성일: ${post.create_at}</small>
                    `;
                    container.appendChild(li);
                });
            })
            .catch(error => {
                console.error(error);
                container.innerHTML = '<li>질문을 불러오는 데 실패했습니다.</li>';
            });
    }

    loadMyQuestions();
});

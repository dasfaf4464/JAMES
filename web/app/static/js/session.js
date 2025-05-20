document.addEventListener("DOMContentLoaded", function () {
  //websocket link start
  const path = window.location.pathname;
  const parts = path.split('/');
  const sessionCode = parts[parts.length - 1];
  console.log(sessionCode);

  const socket = io("http://localhost:5000", {
    query: {
      session_code: sessionCode
    }
  });
  //websocket link end

  //question-button start
  const questionButton = document.getElementById('questionButton');
  let canClick = true;

  /**
   * 연속 클릭 방지
   */
  questionButton.addEventListener('click', (event) => {
    event.preventDefault();

    if (!canClick) {
      return;
    }
    canClick = false

    /**
     * http 서버에 llm 연결 요청
     */
    const originaltext = document.getElementById('originaltext').value.trim();

    fetch('/room/llm', {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain' },
      body: originaltext
    })
      .then(res => res.json())
      .then(data => {
        if (data.error == 1) {
          alert("시스템 조작을 시도하였습니다. 질문을 다시 입력하세요.");
        } else {
          const llmPanel = document.querySelector('.LLM-list-panel');
          llmPanel.innerHTML = ''; // 기존 요약 박스 초기화

          data.text.forEach(summary => {
            const box = document.createElement('div');
            box.className = 'box';
            box.dataset.originaltext = summary.original
            box.textContent = summary.content;

            box.dataset.main = summary.category.main;
            box.dataset.sub = summary.category.sub;
            box.dataset.minor = summary.category.minor;

            box.addEventListener('click', () => {
              document.querySelectorAll('.LLM-list-panel .box').forEach(b => b.classList.remove('selected'));
              box.classList.add('selected');

              console.log(`Original: ${box.dataset.originaltext}`)
              console.log(`Main: ${box.dataset.main}`);
              console.log(`Sub: ${box.dataset.sub}`);
              console.log(`Minor: ${box.dataset.minor}`);
            });

            llmPanel.appendChild(box);
          });
        }
      })
      .catch(err => {
        console.error('error:', err);
      })
      .finally(() => {
        setTimeout(() => {
          canClick = true;
        }, 2000);
      });
  });
  //question-button end

  //LLM list start
  const boxes = document.querySelectorAll('.LLM-list-panel .box');

  boxes.forEach(box => {
    box.addEventListener('click', () => {
      boxes.forEach(b => b.classList.remove('selected'));
      box.classList.add('selected');
    });
  });
  //LLM list end


});

/*

document.addEventListener("DOMContentLoaded", function () {
  const summaryButton = document.querySelector('.summaryButton');
  const categoriesContainer = document.querySelector('.categories');

  summaryButton.addEventListener('click', (e) => {
    e.preventDefault();

    const selectedBox = document.querySelector('.LLM-list-panel .box.selected');
    if (!selectedBox) {
      alert("요약된 질문을 먼저 선택해주세요.");
      return;
    }

    const selectedSummary = selectedBox.textContent;

    // 요약된 질문을 서버로 전송하여 해당 카테고리를 하나 받아옴
    fetch('/auth/get_category', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ summary: selectedSummary })
    })
      .then(res => res.json())
      .then(data => {
        // 서버에서 단일 category 문자열 응답: 예 { category: "운영체제" }
        if (data.category) {
          const box = document.createElement('div');
          box.className = 'category-box';

          const p = document.createElement('p');
          p.textContent = data.category;

          box.appendChild(p);
          categoriesContainer.appendChild(box);
        } else {
          alert("서버에서 카테고리를 받지 못했습니다.");
        }
      })
      .catch(err => {
        console.error('카테고리 요청 실패:', err);
      });
  });
});
재작성 필요
*/
/*
document.addEventListener("DOMContentLoaded", function () {
  const summaryButton = document.querySelector('.summaryButton');
  const categoriesContainer = document.querySelector('.categories');

  summaryButton.addEventListener('click', (e) => {
    e.preventDefault();

    // 선택된 요약 질문 찾기 (테스트용이지만 실제 구조 유지)
    const selectedBox = document.querySelector('.LLM-list-panel .box.selected');
    if (!selectedBox) {
      alert("요약된 질문을 먼저 선택해주세요.");
      return;
    }

    const selectedSummary = selectedBox.textContent;

    // 🧪 임시 카테고리 (선택된 요약에 따라 임의 생성)
    const fakeCategory = generateFakeCategory(selectedSummary);

    // category-box 생성
    const box = document.createElement('div');
    box.className = 'category-box';

    const p = document.createElement('p');
    p.textContent = fakeCategory;

    box.appendChild(p);
    categoriesContainer.appendChild(box);
  });

  // 임시로 요약 문장에 따라 카테고리 뽑아내는 함수
  function generateFakeCategory(summary) {
    if (summary.includes("AI") || summary.includes("인공지능")) return "AI";
    if (summary.includes("운영체제") || summary.includes("커널")) return "운영체제";
    if (summary.includes("네트워크")) return "네트워크";
    if (summary.includes("프론트엔드")) return "웹개발";
    return "기타";
  }
});
*/
/**
 * 주석 적을때 함수에 기능, 인수, 반환값 필요/
 * 서버 요청이면 보내는 데이터 타입, 종류, 받는 데이터 타입, 종류 작성 
 * dom에 event 연결하는 람다 함수방식으로 contentload 안에 적을 거면 전부 다 안에 작성 필요
 * 
 * 해야할 일 : 세션 접속시 참여 API로 session의 옵션 확인(비밀번호, 사용자 키) -> 이후 세션 초기화 후 사용자 웹소켓 연결
 * 세션 웹소켓 연결 후 메세지 발신 이벤트 연결 (버튼 클릭시, 에러코드 2번인 선택지는 선택 불가능 하도록 작성), 서버에서 보내는 메세지 처리 함수(메세지 수신 이후 해당 정보에 css)
 * 카테고리 선택시 AJAX HTTP로 질문 리스트 가져오는 API 연결
 * 
 * 세션 관련된 api는 api/room.py 에서 찾아보기
 */
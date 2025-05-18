document.addEventListener("DOMContentLoaded", function () {
  document.getElementById('questionButton').addEventListener('click', (event) => {
    event.preventDefault();

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
          alert(`총 ${data.text}개의 요약을 받았습니다.`);

          const llmPanel = document.querySelector('.LLM-list-panel');
          llmPanel.innerHTML = ''; // 기존 요약 박스 초기화

          // text_list 순회하며 박스 추가
          data.text.forEach(summary => {
            const box = document.createElement('div');
            box.className = 'box';
            box.textContent = summary.content; // ✅ 텍스트만 표시

            // ✅ 데이터로 카테고리를 보존 (예: dataset 사용)
            box.dataset.main = summary.category.main;
            box.dataset.sub = summary.category.sub;
            box.dataset.minor = summary.category.minor;

            // 선택 이벤트 연결
            box.addEventListener('click', () => {
              document.querySelectorAll('.LLM-list-panel .box').forEach(b => b.classList.remove('selected'));
              box.classList.add('selected');

              // 선택된 박스의 카테고리 정보 사용 가능
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
      });
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const boxes = document.querySelectorAll('.LLM-list-panel .box');

  boxes.forEach(box => {
    box.addEventListener('click', () => {
      boxes.forEach(b => b.classList.remove('selected'));
      box.classList.add('selected');
    });
  });
});

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
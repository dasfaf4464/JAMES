document.addEventListener("DOMContentLoaded", function () {
  document.getElementById('questionButton').addEventListener('click', (event) => {
    event.preventDefault();

    const originaltext = document.getElementById('originaltext').value.trim();

    fetch('/auth/post_question', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ originaltext })
    })
      .then(res => res.json())
      .then(data => {
        if (data.error == 1) {
          alert("시스템 조작을 시도하였습니다. 질문을 다시 입력하세요.");
        } else {
          alert(`총 ${data.count}개의 요약을 받았습니다.`);

          const llmPanel = document.querySelector('.LLM-list-panel');
          llmPanel.innerHTML = ''; // 기존 요약 박스 초기화

          // text_list 순회하며 박스 추가
          data.text.forEach(summary => {
            const box = document.createElement('div');
            box.className = 'box';
            box.textContent = summary;

            // 선택 이벤트 연결
            box.addEventListener('click', () => {
              document.querySelectorAll('.LLM-list-panel .box').forEach(b => b.classList.remove('selected'));
              box.classList.add('selected');
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
*/

// 질문 전송 후 요약 리스트 받아오기
document.addEventListener("DOMContentLoaded", function () {
  document.getElementById('questionButton').addEventListener('click', (event) => {
    event.preventDefault();

    const originaltext = document.getElementById('originaltext').value.trim();

    fetch('/auth/post_question', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ originaltext })
    })
      .then(res => res.json())
      .then(data => {
        if (data.error == 1) {
          alert("시스템 조작을 시도하였습니다. 질문을 다시 입력하세요.");
        } else {
          alert(`총 ${data.count}개의 요약을 받았습니다.`);

          const llmPanel = document.querySelector('.LLM-list-panel');
          llmPanel.innerHTML = ''; // 기존 요약 박스 초기화

          // 요약 리스트 박스 생성
          data.text.forEach(summary => {
            const box = document.createElement('div');
            box.className = 'box';
            box.textContent = summary;

            box.addEventListener('click', () => {
              document.querySelectorAll('.LLM-list-panel .box').forEach(b => b.classList.remove('selected'));
              box.classList.add('selected');
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

// 선택 이벤트 (기본 박스용)
document.addEventListener('DOMContentLoaded', function () {
  const boxes = document.querySelectorAll('.LLM-list-panel .box');

  boxes.forEach(box => {
    box.addEventListener('click', () => {
      boxes.forEach(b => b.classList.remove('selected'));
      box.classList.add('selected');
    });
  });
});

// 📌 요약을 바탕으로 카테고리 생성 및 카운팅
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

document.querySelectorAll('.category-box').forEach(box => {
  box.style.transform = "scale(5)";
});

    const selectedSummary = selectedBox.textContent;
    const fakeCategory = generateFakeCategory(selectedSummary);

    // 기존 카테고리 박스가 있는지 확인
    const existingBox = Array.from(categoriesContainer.querySelectorAll('.category-box')).find(box => {
      return box.dataset.category === fakeCategory;
    });

if (existingBox) {
  let count = parseInt(existingBox.dataset.count || "1", 10);
  count += 1;
  existingBox.dataset.count = count;
  existingBox.querySelector('p').textContent = `${fakeCategory} ×${count}`;

  // ✅ 직접 width/height 조절 방식
  const baseSize = 120; // 초기 사이즈 (px)
  const newSize = baseSize + (count - 1) * 40; // 40px씩 증가
  existingBox.style.width = `${newSize}px`;
  existingBox.style.height = `${newSize}px`;

  // 시각적으로 확인하기 쉽게 테두리나 색 강조
  existingBox.style.border = "2px solid #007acc";
  console.log("Size updated:", newSize + "px");
}
 else {
  const box = document.createElement('div');
box.className = 'category-box';
box.dataset.category = fakeCategory;
box.dataset.count = 1;

const p = document.createElement('p');
p.textContent = fakeCategory;

box.appendChild(p);
categoriesContainer.appendChild(box);

// 기본 크기 설정
box.style.width = '120px';
box.style.height = '120px';

}
  });

  // 요약 문장으로부터 카테고리 추출 (임시 분류 기준)
  function generateFakeCategory(summary) {
    if (summary.includes("AI") || summary.includes("인공지능")) return "AI";
    if (summary.includes("운영체제") || summary.includes("커널")) return "운영체제";
    if (summary.includes("네트워크")) return "네트워크";
    if (summary.includes("프론트엔드")) return "웹개발";
    return "기타";
  }
});


const session_categories = new Map();

/**
 * 소켓 연결
 */
let socket = null
const path = window.location.pathname;
const parts = path.split('/');
const sessionCode = parts[parts.length - 1];

document.addEventListener("DOMContentLoaded", () => {
  console.log(sessionCode);

  socket = io("http://localhost:5000", {
    query: {
      session_code: sessionCode
    }
  });

  socket.emit("session", sessionCode)

  socket.on("update", (data) => {
    let is_in = session_categories.get(data.category)
    if (!is_in) {
      session_categories.set(data.category, 1);
    } else {
      session_categories.set(data.category, is_in + 1);
    }

    const existingBox = Array.from(categoriesContainer.querySelectorAll('.category-box'))
      .find(b => b.dataset.category === category);

    if (existingBox) {
      existingBox.dataset.count = is_in;

      existingBox.querySelector('p').textContent = `${category}`;

      const baseSize = 120;
      const newSize = baseSize + (count - 1) * 40;

      existingBox.style.width = `${newSize}px`;
      existingBox.style.height = `${newSize}px`;
    } else {

      const catBox = document.createElement('div');
      catBox.className = 'category-box';
      catBox.dataset.category = category;
      catBox.dataset.count = count;

      const p = document.createElement('p');
      p.textContent = `${category}`;
      catBox.appendChild(p);

      categoriesContainer.appendChild(catBox);

      catBox.style.width = '120px';
      catBox.style.height = '120px';

      catBox.addEventListener('click', () => {
        paginationState.currentCategory = category;
        paginationState.currentSummary = summary;
        paginationState.currentPage = 0;

        fetch('/')
      });
    }

  })
});

/**
 * 사용자 쿠키 확인
 */
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

/**
 * llm값 받아오고 받아온 값 출력 박스 생성
 */
document.addEventListener("DOMContentLoaded", () => {
  const questionButton = document.getElementById('questionButton');
  let canClick = true;

  questionButton.addEventListener('click', (event) => {
    event.preventDefault();
    if (!canClick) return;
    canClick = false;

    const originaltext = document.getElementById('originaltext').value.trim();
    const path = window.location.pathname;
    const parts = path.split('/');
    const sessionCode = parts[2];

    fetch('/room/llm', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: originaltext, session_code: sessionCode })
    })
      .then(res => res.json())
      .then(data => {
        if (data.error == 1) {
          alert("시스템 조작을 시도하였습니다. 질문을 다시 입력하세요.");
          return;
        }

        const llmPanel = document.querySelector('.LLM-list-panel');
        llmPanel.innerHTML = '';

        data.text.forEach(summary => {
          const box = document.createElement('div');
          box.className = 'box';
          box.textContent = summary.content;
          box.dataset.main = summary.category.main;
          box.dataset.sub = summary.category.sub;
          box.dataset.minor = summary.category.minor;
          box.dataset.key = summary.key;
          box.dataset.error = summary.error;

          box.innerHTML = `
          <div class="summary-text">${summary.content}</div>
          <div class="category-info">
          <span class="main">( ${summary.category.main}</span> /
          <span class="sub"> ${summary.category.sub}</span> /
          <span class="minor"> ${summary.category.minor} )</span>
          </div>
          `;

          box.addEventListener('click', () => {
            document.querySelectorAll('.LLM-list-panel .box')
              .forEach(b => b.classList.remove('selected'));
            box.classList.add('selected');

            console.log(`llm: ${box.textContent}`);
            console.log(`Main: ${box.dataset.main}`);
            console.log(`Sub: ${box.dataset.sub}`);
            console.log(`Minor: ${box.dataset.minor}`);
            console.log(`key: ${box.dataset.key}`);
            console.log(`error: ${box.dataset.error}`);
          });

          llmPanel.appendChild(box);
        });
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
});

/**
 * 선택한 박스 이벤트
 */
document.addEventListener("DOMContentLoaded", () => {
  let selectedBox = null;

  const llmPanel = document.querySelector('.LLM-list-panel');

  llmPanel.addEventListener('click', (event) => {
    const box = event.target.closest('.box');
    if (!box) return;

    document.querySelectorAll('.LLM-list-panel .box').forEach(b => {
      b.classList.remove('selected');
    });

    box.classList.add('selected');
    selectedBox = box;
  });

  const summaryButton = document.querySelector('.summaryButton');
  summaryButton.addEventListener('click', (event) => {
    event.preventDefault();

    if (!selectedBox) {
      alert('요약 항목을 선택하세요.');
      return;
    }

    console.log(`${selectedBox.dataset.key}`);

    const data = {
      session_code: window.location.pathname.split('/').pop(),
      key: selectedBox.dataset.key,
    };

    socket.emit("send_llm", data)
  });
});
const sessionCode = window.location.pathname.split('/').pop();
let socket = null;
let session_categories = new Map();
let selectedBox = null;

const paginationState = {
  currentCategory: null,
  currentSummary: null,
  currentPage: 0,
};

document.addEventListener("DOMContentLoaded", () => {
  fetch(`/api/session/${sessionCode}/get/info`)
    .then(res => res.json())
    .then(data => {
      if (!data.session_exists) {
        showInvalidSessionModal();
      } else if (data.session_lock) {
        showPasswordModal();
      } else {
        initializeApp();
      }
    });

  clearListPanel();
  setupSummaryButton();
});

function showInvalidSessionModal() {
  document.getElementById("invalidSessionModal").style.display = 'flex';
}

function showPasswordModal() {
  const modal = document.getElementById("passwordModal");
  const button = document.getElementById("enterSessionBtn");
  const errorText = document.getElementById("passwordError");

  modal.style.display = 'flex';

  button.addEventListener("click", () => {
    const pw = document.getElementById("sessionPassword").value;

    fetch(`/api/session/${sessionCode}/pass`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password: pw })
    })
      .then(res => res.json())
      .then(result => {
        if (result.valid) {
          modal.style.display = 'none';
          initializeApp();
        } else {
          errorText.style.display = 'block';
        }
      });
  });
}

function init_socket() {
  socket = io({ query: { session_code: sessionCode } });
  return socket;
}

function register_socket_event(socket, category_memory) {
  const categoriesContainer = document.querySelector('.categories');

  socket.on("init_categories", (data) => {
    const categoriesContainer = document.querySelector('.categories');

    Object.entries(data).forEach(([key, value]) => {
      category_memory.set(key, value);

      const existingBox = Array.from(categoriesContainer.querySelectorAll('.category-box'))
        .find(b => b.dataset.category === key);

      if (!existingBox) {
        const catBox = document.createElement('div');
        catBox.className = 'category-box';
        catBox.dataset.category = key;
        catBox.dataset.count = value;

        const p = document.createElement('p');
        p.textContent = `${key}`;
        catBox.appendChild(p);

        categoriesContainer.appendChild(catBox);

        const baseSize = 120;
        const newSize = baseSize + (value - 1) * 40;
        catBox.style.width = `${newSize}px`;
        catBox.style.height = `${newSize}px`;
      }
    });

    console.log("Initialized categories:", category_memory);
  });

  socket.on("update", (data) => {
    const category = data.category;
    console.log(category)

    let count = category_memory.get(category) || 0;
    count++;
    category_memory.set(category, count);
    console.log(category_memory)
    const existingBox = Array.from(categoriesContainer.querySelectorAll('.category-box'))
      .find(b => b.dataset.category === category);

    if (existingBox) {
      existingBox.dataset.count = count;
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
    }
  });
}

function initializeApp() {
  socket = init_socket();
  register_socket_event(socket, session_categories);

  const questionButton = document.getElementById('questionButton');
  let canClick = true;

  questionButton.addEventListener('click', (event) => {
    event.preventDefault();
    if (!canClick) return;
    canClick = false;

    const originaltext = document.getElementById('originaltext').value.trim();

    fetch(`/api/post/${sessionCode}/refine_text`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: originaltext })
    })
      .then(res => res.json())
      .then(data => {
        if (data.length > 0 && data[0].error === 1) {
          alert("허용되지 않는 입력입니다. 질문을 다시 입력하세요.");
          return;
        }

        const llmPanel = document.querySelector('.LLM-list-panel');
        llmPanel.innerHTML = '';

        data.forEach(summary => {
          const box = document.createElement('div');
          box.className = 'box';
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
            selectedBox = box;

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

  document.querySelector('.categories').addEventListener('click', (e) => {
    const box = e.target.closest('.category-box');
    if (!box) return;

    const categoryName = box.dataset.category;
    const count = box.dataset.count;

    fetch(`/api/post/${sessionCode}/get/questions?category=${categoryName}&start=0&count=30`)
      .then(response => {
        if (!response.ok) {
          throw new Error(`서버 오류: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('받은 데이터:', data);

        if (!Array.isArray(data)) {
          throw new Error('데이터가 배열이 아닙니다.');
        }

        const questionsList = document.getElementById('category-list-panel');
        if (!questionsList) {
          console.error('질문 목록을 표시할 요소가 없습니다.');
          return;
        }

        questionsList.innerHTML = data.map(q => `
      <div class="category-title"> #${q.category || q.minor || ''}</div>
      <div class="question-box">
      <div class="box">
        <p><strong>원본:</strong> ${q.original || q.original_text || ''}</p>
        <p><strong>정제:</strong> ${q.refined_text || q.llm || ''}</p>
      </div>
      <textarea class="memo" placeholder="메모를 입력하세요."></textarea>
      </div>
    `).join('');
      })
      .catch(error => {
        console.error('질문 목록 가져오기 실패:', error);
      });
  });


}

function setupSummaryButton() {
  const summaryButton = document.querySelector('.summaryButton');
  summaryButton.addEventListener('click', (event) => {
    event.preventDefault();

    if (!selectedBox) {
      alert('요약 항목을 선택하세요.');
      return;
    }

    const data = {
      session_code: sessionCode,
      key: selectedBox.dataset.key,
    };

    socket.emit("select", data);

    document.querySelector('.LLM-list-panel').innerHTML = '';
    document.getElementById('originaltext').value = '';
    selectedBox = null;
  });
}

function clearListPanel() {
  const llmPanel = document.querySelector('.LLM-list-panel');
  if (llmPanel) {
    llmPanel.innerHTML = '';
  }
  selectedBox = null;
}

const categoryPanel = document.querySelector('.cartegory-list-panel');
const llmPanel = document.querySelector('.LLM-list-panel');
const offsetTrigger = 1;

if (window.innerWidth > 767) {
  window.addEventListener('scroll', () => {
    const scrollY = window.scrollY;
    const offset = Math.max(0, scrollY - offsetTrigger);

    categoryPanel.style.transform = `translateY(${offset}px)`;
    llmPanel.style.transform = `translateY(${offset}px)`;
  });
}

function openRightPanel() {
  document.querySelector('.right-panel').classList.add('active');
  document.getElementById('overlay').classList.add('active');
}

function closeRightPanel() {
  document.querySelector('.right-panel').classList.remove('active');
  document.getElementById('overlay').classList.remove('active');
}


/**
 * 1.
 * initializeApp 안에 fetch /api/post/${sessionCode}/get/questions?category="main/sub"&start=0&count=""
 * 이걸로 생성된 카테고리박스에 이벤트 붙이고 보여주기
 * 
 * 2. submit 버튼 누르면 llm에서 온 정보들 전부 없애기
 * 
 * 3. 처음 세션 입장시 61-68번째 줄에 있는 함수들 채우기
 *  -- 처음 세션 입장시 category_memory에 정보들 가져와진거 보여주는 함수
 * 
 * 4. 카테고리 박스 커지는거 테스트 못했음
 */
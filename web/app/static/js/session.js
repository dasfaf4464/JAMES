const sessionCode = window.location.pathname.split('/').pop();
let socket = null;

document.addEventListener("DOMContentLoaded", () => {
  fetch(`/api/session/${sessionCode}/get/info`)
    .then(res => res.json())
    .then(data => {
      if (!data.session_exist) {
        showInvalidSessionModal();
      } else if (data.session_lock) {
        showPasswordModal();
      } else {
        initializeApp();
      }
    });
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

// 소켓 생성
function init_socket() {
  socket = io({
    query: {
      session_code: sessionCode
    }
  });
  return socket;
}

// 웹소켓 이벤트 등록
function register_socket_event(socket, category_memory) {
  socket.on("init_categories", (data) => {
    Object.entries(data).forEach(([key, value]) => {
      category_memory.set(key, value);
    });

    //TODO: 여기서 처음 입장했을때 기존에 존재하는 카테고리 보여주기
    console.log("Initialized categories:", category_memory);
  });

  socket.on("update", (data) => {
    console.log("update categories:", category_memory);
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
}

// 모든 초기화
function initializeApp() {
  const session_categories = new Map();
  let socket = init_socket();
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
}

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

    socket.emit("select", data)
  });

  clearListPanel();
});

function clearListPanel() {
  const llmPanel = document.querySelector('.LLM-list-panel');
  llmPanel.innerHTML = '';
  selectedBox = null;
}
const session_categories = new Map();

/**
 * 소켓 연결
 */
const socket = null
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

    fetch('/room/llm', {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain' },
      body: originaltext
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

          box.dataset.index = index;
          box.dataset.originaltext = summary.original;
          box.textContent = summary.content;

          box.dataset.main = summary.category.main;
          box.dataset.sub = summary.category.sub;
          box.dataset.minor = summary.category.minor;

          box.addEventListener('click', () => {
            document.querySelectorAll('.LLM-list-panel .box')
              .forEach(b => b.classList.remove('selected'));
            box.classList.add('selected');

            console.log(`Original: ${box.dataset.originaltext}`);
            console.log(`Main: ${box.dataset.main}`);
            console.log(`Sub: ${box.dataset.sub}`);
            console.log(`Minor: ${box.dataset.minor}`);
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
  const boxes = document.querySelectorAll('.LLM-list-panel .box');
  let selectedBox = null;

  boxes.forEach(box => {
    box.addEventListener('click', () => {
      boxes.forEach(b => b.classList.remove('selected'));
      box.classList.add('selected');
      selectedBox = box;
    });
  });

  const summaryButton = document.getElementsByClassName('summaryButton')
  summaryButton.addEventListener('click', (event) => {
    event.preventDefault()
    console.log(`${selectedBox.dataset.llm}`);
    alert('sf');
  });
});

/**
* summaryButton 클릭 시 서버에 emit 요청
*/
summaryButton.addEventListener('click', (e) => {
  e.preventDefault();

  const selectedBox = document.querySelector('.LLM-list-panel .box.selected');
  if (!selectedBox) {
    alert("요약된 질문을 먼저 선택해주세요.");
    return;
  }

  const mainCategory = selectedBox.dataset.main;
  const subCategory = selectedBox.dataset.sub;
  const summaryIndex = selectedBox.dataset.index;

  socket.emit('create_category', {
    main: mainCategory,
    sub: subCategory,
    summaryIndex: summaryIndex
  });
});

const categoriesContainer = document.querySelector('.categories');

/**
 * 질문리스트를 서버에서 일정 개수만 받아오기 위한 객체 변수 선언
 */
const paginationState = {
  currentCategory: null,
  currentSummary: null,
  currentPage: 0,
  pageSize: 5
};

/**
* 모든 사용자 화면에 한 사용자가 선택한 질문의 카테고리를 'main/sub' 형식으로 category-box 생성
*/
socket.on('new_category_created', (data) => {
  const { category, summary, count } = data;
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

    catBox.addEventListener('click', () => {
      paginationState.currentCategory = category;
      paginationState.currentSummary = summary;
      paginationState.currentPage = 0;

      socket.emit('get_questions_by_summary', {
        summaryIndex: summaryIndex,
        category: category,
        page: 0,
        limit: paginationState.pageSize
      }, { once: true });
    });
  }
});

/**
* 질문 리스트를 받고 .category-list-panel에 표시(질문 리스트와 메모 생성)
*/
socket.on('questions_for_summary', (data) => {
  const { category, questions, hasMore } = data;
  const listPanel = document.querySelector('.cartegory-list-panel');

  if (paginationState.currentPage === 0) {
    listPanel.innerHTML = `<div class="category-title">#${category}</div>`;
  }

  questions.forEach((q, index) => {
    const wrapper = document.createElement('div');
    wrapper.className = 'question-box';

    const questionDiv = document.createElement('div');
    questionDiv.className = 'box';
    questionDiv.textContent = q;

    const memo = document.createElement('textarea');
    memo.className = 'memo';
    memo.placeholder = '메모를 입력하세요.';

    memo.addEventListener('input', () => {
      socket.emit('save_memo', {
        session: sessionCode,
        category: category,
        question: q,
        memo: memo.value
      });
    });

    wrapper.appendChild(questionDiv);
    wrapper.appendChild(memo);
    listPanel.appendChild(wrapper);
  });

  const prevBtn = document.getElementById('load-more-btn');
  if (prevBtn) prevBtn.remove();

  if (hasMore) {
    const loadMore = document.createElement('button');
    loadMore.id = 'load-more-btn';
    loadMore.textContent = '더보기';
    loadMore.className = 'btn btn-outline-secondary mt-2';
    loadMore.addEventListener('click', () => {
      paginationState.currentPage += 1;
      socket.emit('get_questions_by_summary', {
        summary: paginationState.currentSummary,
        category: paginationState.currentCategory,
        page: paginationState.currentPage,
        limit: paginationState.pageSize
      });
    });
    listPanel.appendChild(loadMore);
  }
});

/**
*서버에서 get_questions_by_summary 요청을 받았을 때, 해당 page와 limit을 이용해 질문을 슬라이싱해서 응답
@socketio.on('get_questions_by_summary')
def handle_questions_paginated(data):
    summary = data.get('summary')
    category = data.get('category')
    page = int(data.get('page', 0))
    limit = int(data.get('limit', 5))

    all_questions = db.get(category, [])
    start = page * limit
    end = start + limit
    paged_questions = all_questions[start:end]
    has_more = end < len(all_questions)

    emit('questions_for_summary', {
        'category': category,
        'questions': paged_questions,
        'hasMore': has_more
    }, to=request.sid)
*/

/**
* 서버에서 category = {main}/{sub} 만들어서 전달, {main}/{sub}의 count 증가 관리하는 코드 필요

from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# 카테고리 count 상태를 서버에서 유지
category_counts = {}

@socketio.on('connect')
def handle_connect():
    print('사용자 연결됨:', request.sid)

@socketio.on('create_category')
def handle_create_category(data):
    main = data.get('main')
    sub = data.get('sub')
    summary = data.get('summary')

    if not main or not sub:
        return

    category = f"{main}/{sub}"

    # 카운트 증가
    if category not in category_counts:
        category_counts[category] = 1
    else:
        category_counts[category] += 1

    count = category_counts[category]

    # 전체 사용자에게 카테고리 생성 이벤트 전송
    emit('new_category_created', {
        'category': category,
        'summary': summary,
        'count': count
    }, broadcast=True)
*/

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

      const baseSize = 120;
      const newSize = baseSize + (count - 1) * 40;
      existingBox.style.width = `${newSize}px`;
      existingBox.style.height = `${newSize}px`;
      existingBox.style.border = "2px solid #007acc";
    } else {
      const box = document.createElement('div');
      box.className = 'category-box';
      box.dataset.category = fakeCategory;
      box.dataset.count = 1;

      const p = document.createElement('p');
      p.textContent = fakeCategory;
      box.appendChild(p);
      categoriesContainer.appendChild(box);

      box.style.width = '120px';
      box.style.height = '120px';

      // ✅ 여기서 클릭 이벤트 연결
      box.addEventListener('click', () => {
        const listPanel = document.querySelector('.cartegory-list-panel');
        listPanel.innerHTML = `<div class="category-title">#${fakeCategory}</div>`;

        // 📌 임시 질문 리스트
        const dummyQuestions = generateDummyQuestions(fakeCategory);

        dummyQuestions.forEach(q => {
          const div = document.createElement('div');
          div.className = 'box';
          div.textContent = q;
          listPanel.appendChild(div);
        });
      });
    }
  });

  // 요약 문장으로부터 카테고리 추출
  function generateFakeCategory(summary) {
    if (summary.includes("AI") || summary.includes("인공지능")) return "AI";
    if (summary.includes("운영체제") || summary.includes("커널")) return "운영체제";
    if (summary.includes("네트워크")) return "네트워크";
    if (summary.includes("프론트엔드")) return "웹개발";
    return "기타";
  }

  // 카테고리별 임시 질문 생성기
  function generateDummyQuestions(category) {
    switch (category) {
      case "AI":
        return ["AI란 무엇인가?", "머신러닝과 딥러닝 차이", "ChatGPT의 원리"];
      case "운영체제":
        return ["프로세스와 스레드 차이", "커널이 하는 일은?", "시스템 콜이란?"];
      case "네트워크":
        return ["OSI 7계층 설명", "TCP와 UDP의 차이", "IP 주소란?"];
      case "웹개발":
        return ["프론트엔드와 백엔드 차이", "HTML/CSS/JS 역할", "SPA vs MPA"];
      default:
        return ["기타 질문1", "기타 질문2", "기타 질문3"];
    }
  }
});
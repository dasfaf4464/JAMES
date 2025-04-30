const form = document.querySelector("form");
const input = document.getElementById("QBar");
const button = document.getElementById("button-addon2");
const questionList = document.getElementById("questionList");

function addQuestion() {
  const sentence = input.value.trim();
  if (!sentence) return;

  const words = sentence.split(/\s+/);
  const randomWord = words[Math.floor(Math.random() * words.length)];

  const wordContainer = document.createElement("div");
  wordContainer.className = "mb-2";

  const wordButton = document.createElement("button");
  wordButton.className = "btn btn-sm btn-warning me-2";
  wordButton.textContent = randomWord;

  const result = document.createElement("div");
  result.className = "alert alert-primary mt-2";
  result.textContent = sentence;
  result.style.display = "none"; // 초기에는 숨김

  // 버튼 클릭 시 토글 동작
  wordButton.addEventListener("click", () => {
    if (result.style.display === "none") {
      result.style.display = "block";
    } else {
      result.style.display = "none";
    }
  });

  wordContainer.appendChild(wordButton);
  wordContainer.appendChild(result);
  questionList.prepend(wordContainer);

  input.value = "";
}

button.addEventListener("click", addQuestion);
form.addEventListener("submit", (e) => {
  e.preventDefault();
  addQuestion();
});


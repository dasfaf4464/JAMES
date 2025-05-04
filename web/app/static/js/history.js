function myQuestion() {
    const button_color = window.getComputedStyle(document.getElementById("my-question")).backgroundColor;
    document.getElementById('content-box').style.backgroundColor = button_color;
}
  
function myAnswer() {
    const button_color = window.getComputedStyle(document.getElementById("my-answer")).backgroundColor;
    document.getElementById("content-box").style.backgroundColor = button_color;
}

function saving() {
    const button_color = window.getComputedStyle(document.getElementById("saving")).backgroundColor;
    document.getElementById("content-box").style.backgroundColor = button_color;
}

function myProfile() {
    const button_color = window.getComputedStyle(document.getElementById("my-profile")).backgroundColor;
    document.getElementById("content-box").style.backgroundColor = button_color;
}
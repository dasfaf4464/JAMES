document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('create-name-button').addEventListener('click', function (event) {
        event.preventDefault();

        fetch('/generate-name', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('name-input').value = data.name;
        })
        .catch(error => {
            console.error("에러 발생: " + error);
        });
    });

    document.getElementById('register-button').addEventListener('click', function (event) {
        event.preventDefault();

        const id = document.getElementById('uid').value;
        const pw = document.getElementById('pw').value;
        const email = document.getElementById('email').value;
        const name = document.getElementById('name-input').value;

        const userData = {
            id: id,
            pw: pw,
            email: email,
            name: name
        };

        fetch('/signup', {  // <--- 여기 수정
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || '계정 생성 완료');
            if (data.success) {
                window.location.href = '/';  // <--- 성공 시 인덱스로 이동
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('계정 생성 중 오류 발생');
        });
    });
});

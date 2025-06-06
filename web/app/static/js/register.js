/**
 * 이름 생성 요청
 */
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById('create-name-button').addEventListener('click', function (event) {
        event.preventDefault();

        fetch('/api/user/name', {
            method: 'GET',
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('name-input').value = data.name;
        })
        .catch(error => {
            console.error("에러 발생: " + error);
        });
    });
});

/**
 * 회원 정보 전달, 등록 요청
 */
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('register-button').addEventListener('click', function (event) {
        event.preventDefault();

        const id = document.getElementById('uid').value.trim();
        const pw = document.getElementById('pw').value;
        const email = document.getElementById('email').value.trim();
        const name = document.getElementById('name-input').value.trim();

        const idValid = /^[A-Za-z0-9]{5,20}$/.test(id);
        if (!idValid) {
            alert('아이디는 영어와 숫자를 조합하여 5자 이상 20자 이하로 입력해주세요.');
            return;
        }

        if (pw.length < 7 || pw.length > 20) {
            alert('비밀번호는 7자 이상 20자 이하로 입력해주세요.');
            return;
        }

        if (!name) {
            alert('이름을 입력하거나 생성해주세요.');
            return;
        }

        const userData = {
            id: id,
            pw: pw,
            email: email,
            name: name
        };

        fetch('/api/user/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        })
            .then(response => response.json())
            .then(data => {
                alert(data.register_message);
                if (data.register_result) {
                    window.location.href = '/';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('계정 생성 중 오류 발생');
            });
    });
});
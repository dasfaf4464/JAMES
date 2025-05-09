document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('create-name-button').addEventListener('click', function (event) {
        event.preventDefault();

        fetch('/auth/generate_name', {
            method: 'GET',
        })
            .then(response => response.text())
            .then(name => {
                document.getElementById('name-input').value = name;
            })
            .catch(error => {
                console.error("에러 발생: " + error);
            });
    });

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

        fetch('/auth/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                if (data.isSuccess) {
                    window.location.href = data.redirect_url;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('계정 생성 중 오류 발생');
            });
    });
});
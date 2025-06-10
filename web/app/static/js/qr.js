function clearInput() {
    var urlInput = document.getElementById("urlInput");
    urlInput.value = '';
}

function handleKeyPress(event) {
    if (event.key === "Enter") {
        generateQRCode();
    }
}

function generateQRCode() {
    var urlInput = document.getElementById("urlInput");
    var urlToEncode = urlInput.value;

    if (!urlToEncode) {
        alert("URL을 입력하세요.");
        return;
    }

    var qrcodeDiv = document.getElementById("qrcode");

    qrcodeDiv.innerHTML = "";

    var qrcode = new QRCode(qrcodeDiv, {
        text: urlToEncode,
        width: 128,
        height: 128,
    });
}
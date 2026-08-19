// LinkedIn용(company_logo)과 Adiga용(univ_logo) 파일 인풋을 모두 선택합니다.
const fileInputs = document.querySelectorAll('input[name="company_logo"], input[name="univ_logo"]');
const canvas = document.getElementById("logoCanvas");
const ctx = canvas.getContext("2d");

let img = new Image();

let markerX = null;
let markerY = null;

// 두 파일 인풋 모두에 'change' 이벤트 리스너를 달아줍니다.
fileInputs.forEach(function (fileInput) {
    fileInput.addEventListener("change", function (e) {
        const file = e.target.files[0];

        if (!file) return;

        img = new Image();

        img.onload = function () {
            canvas.width = img.width;
            canvas.height = img.height;

            // 새 이미지를 올리면 기존 마커(빨간 동그라미) 초기화
            markerX = null;
            markerY = null;

            drawCanvas();
        };

        img.src = URL.createObjectURL(file);
    });
});

function drawCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (img.src) {
        ctx.drawImage(img, 0, 0);
    }

    if (markerX !== null) {
        ctx.beginPath();
        ctx.arc(markerX, markerY, 8, 0, Math.PI * 2);
        ctx.lineWidth = 2;
        ctx.strokeStyle = "red";
        ctx.stroke();
    }
}

if (canvas) {
    canvas.addEventListener("click", function (e) {
        // 이미지가 로드되지 않았을 때는 클릭 무시
        if (!img.src) return;

        const rect = canvas.getBoundingClientRect();

        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;

        markerX = Math.floor((e.clientX - rect.left) * scaleX);
        markerY = Math.floor((e.clientY - rect.top) * scaleY);

        const pixel = ctx.getImageData(markerX, markerY, 1, 1).data;

        const hex = rgbToHex(pixel[0], pixel[1], pixel[2]);

        document.getElementById("pickedColor").value = hex;
        document.getElementById("pickedColorPreview").value = hex;

        drawCanvas();
    });
}

function rgbToHex(r, g, b) {
    return "#" + [r, g, b].map(function (x) {
        const hex = x.toString(16);
        return hex.length === 1 ? "0" + hex : hex;
    }).join("");
}

function applyColor(name) {
    const colorInput = document.getElementById("pickedColor");
    if (!colorInput || !colorInput.value) {
        alert("먼저 로고 이미지에서 색상을 추출해주세요.");
        return;
    }

    const color = colorInput.value;
    const targetInput = document.querySelector(`input[name="${name}"]`);

    if (targetInput) {
        targetInput.value = color;
    }
}

function copyText(elementId) {
    const textarea = document.getElementById(elementId);
    if (!textarea) return;

    textarea.select();
    textarea.setSelectionRange(0, 99999);

    navigator.clipboard.writeText(textarea.value)
        .then(() => {
            alert("복사되었습니다!"); // 복사 확인 메시지 추가
        })
        .catch(err => {
            document.execCommand('copy');
            alert("복사되었습니다!");
        });
}
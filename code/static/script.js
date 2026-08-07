const fileInput = document.querySelector('input[name="company_logo"]');
const canvas = document.getElementById("logoCanvas");
const ctx = canvas.getContext("2d");

let img = new Image();

let markerX = null;
let markerY = null;

fileInput.addEventListener("change", function (e) {

    const file = e.target.files[0];

    if (!file) return;

    img = new Image();

    img.onload = function () {

        canvas.width = img.width;
        canvas.height = img.height;

        drawCanvas();

    };

    img.src = URL.createObjectURL(file);

});

function drawCanvas() {

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.drawImage(img, 0, 0);

    if (markerX !== null) {

        ctx.beginPath();
        ctx.arc(markerX, markerY, 8, 0, Math.PI * 2);
        ctx.lineWidth = 2;
        ctx.strokeStyle = "red";
        ctx.stroke();

    }

}

canvas.addEventListener("click", function (e) {

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

function rgbToHex(r, g, b) {

    return "#" + [r, g, b].map(function (x) {

        const hex = x.toString(16);

        return hex.length === 1 ? "0" + hex : hex;

    }).join("");

}

function applyColor(name) {

    const color = document.getElementById("pickedColor").value;

    document.querySelector(`input[name="${name}"]`).value = color;
}

function copyText(elementId) {
    const textarea = document.getElementById(elementId);
    if (!textarea) return;

    textarea.select();
    textarea.setSelectionRange(0, 99999);

    navigator.clipboard.writeText(textarea.value)
        .then(() => {
        })
        .catch(err => {
            document.execCommand('copy');
        });
}
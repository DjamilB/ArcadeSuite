let canvas;
let ctx;
let imageData;

document.addEventListener("DOMContentLoaded", function () {
    canvas = document.getElementById('gameCanvas');
    ctx = canvas.getContext('2d');
    imageData = ctx.createImageData(canvas.width, canvas.height);
})

function updateCanvas(base64Data) {
    const binaryData = atob(base64Data);  // Decode Base64 string to binary
    var pixelData = new Uint8ClampedArray(binaryData.length);
    for (let i = 0; i < binaryData.length; i++) {
        pixelData[i] = binaryData.charCodeAt(i);  // Convert binary string to byte array
    }
    imageData.data.set(pixelData);  // Set pixel data on canvas
    ctx.putImageData(imageData, 0, 0);  // Render to canvas
}

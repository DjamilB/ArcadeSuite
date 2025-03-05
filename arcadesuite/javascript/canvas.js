const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const imageData = ctx.createImageData(640, 840);

function updateCanvas(base64Data) {
    const binaryData = atob(base64Data);  // Decode Base64 string to binary
    var pixelData = new Uint8ClampedArray(binaryData.length);
    for (let i = 0; i < binaryData.length; i++) {
        pixelData[i] = binaryData.charCodeAt(i);  // Convert binary string to byte array
    }
    imageData.data.set(pixelData);  // Set pixel data on canvas
    ctx.putImageData(imageData, 0, 0);  // Render to canvas
};

// 📷 Real Camera
if (document.getElementById("video")) {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
      document.getElementById("video").srcObject = stream;
    });
}

function capture() {
  let video = document.getElementById("video");
  let canvas = document.getElementById("canvas");
  let ctx = canvas.getContext("2d");

  ctx.drawImage(video, 0, 0, 300, 250);

  let imageData = ctx.getImageData(150, 125, 1, 1).data;
  let r = imageData[0];
  let g = imageData[1];
  let b = imageData[2];

  document.getElementById("colorResult").innerHTML =
    `Detected Color RGB(${r}, ${g}, ${b})`;
}

// 🤖 Ingredient AI Logic
function analyzeIngredients() {
  let input = document.getElementById("ingredients").value.toLowerCase();
  let result = document.getElementById("result");
  result.innerHTML = "";

  let harmfulDB = ["paraben", "sulfate", "phthalate", "triclosan"];

  input.split(",").forEach(item => {
    let li = document.createElement("li");
    if (harmfulDB.some(h => item.includes(h))) {
      li.innerHTML = item.trim() + " ❌ Risky";
      li.style.color = "red";
    } else {
      li.innerHTML = item.trim() + " ✅ Safe";
      li.style.color = "green";
    }
    result.appendChild(li);
  });
}

// 💄 Virtual Makeup
function applyLipstick(color) {
  let lip = document.getElementById("lipstick");
  lip.style.background = color;
}
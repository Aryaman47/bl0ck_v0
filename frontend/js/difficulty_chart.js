import { state } from "./state.js";

const history = [];
const maxPoints = 30;

export function recordDifficulty(diff) {
  history.push(diff);
  if (history.length > maxPoints) history.shift();
  drawChart();
}

function drawChart() {
  const canvas = document.getElementById("difficultyChart");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  if (history.length < 2) return;

  const maxDiff = 10;
  const stepX = canvas.width / (maxPoints - 1);

  ctx.beginPath();
  ctx.strokeStyle = "#1f8feb";
  ctx.lineWidth = 2;

  history.forEach((value, i) => {
    const x = i * stepX;
    const y = canvas.height - (value / maxDiff) * canvas.height;

    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });

  ctx.stroke();
}

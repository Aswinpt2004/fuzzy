const chartDiv = document.getElementById("chart");
const sliderArea = document.getElementById("slider-area");
const explainBtn = document.getElementById("explain-btn");
const explainBox = document.getElementById("explanation-box");
const explainText = document.getElementById("explanation-text");
const explanationLoading = document.getElementById("explanation-loading");
let mfType = document.getElementById("mf_type").value;

// ---------- Create Sliders + Inputs ----------
function createSliders(type) {
  sliderArea.innerHTML = "";
  let paramLabels = [];
  if (type === "Triangular") paramLabels = ["a", "b", "c"];
  else if (type === "Trapezoidal") paramLabels = ["a", "b", "c", "d"];
  else if (type === "Gaussian") paramLabels = ["mean", "sigma"];

  paramLabels.forEach(label => {
    const container = document.createElement("div");
    container.className = "slider-container";
    container.innerHTML = `
      <div class="slider-label">
        <label>${label}: </label>
        <input type="number" id="num-${label}" value="5" min="0" max="10" step="0.1" class="num-input">
      </div>
      <input type="range" min="0" max="10" step="0.1" value="5" id="slider-${label}">
    `;
    sliderArea.appendChild(container);
  });

  const sliders = sliderArea.querySelectorAll("input[type='range']");
  sliders.forEach(slider => {
    const label = slider.id.split("-")[1];
    const numInput = document.getElementById(`num-${label}`);
    slider.addEventListener("input", () => {
      numInput.value = slider.value;
      updatePlot();
    });
    numInput.addEventListener("input", () => {
      slider.value = numInput.value;
      updatePlot();
    });
  });

  updatePlot();
}

// ---------- Fetch & Update Plot ----------
async function updatePlot() {
  const sliders = sliderArea.querySelectorAll("input[type='range']");
  const params = Array.from(sliders).map(s => parseFloat(s.value));
  const body = { mf_type: mfType, params: params };

  const res = await fetch("/api/membership", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  if (!res.ok) return console.error("Backend error:", res.status);

  const data = await res.json();
  if (data.error) return console.error(data.error);

  const trace = {
    x: data.x,
    y: data.y,
    mode: "lines",
    line: { color: "black", width: 3 },
    fill: "tozeroy",
    name: mfType
  };

  const layout = {
    title: `${mfType} Membership Function`,
    paper_bgcolor: "#fff",
    plot_bgcolor: "#fff",
    font: { color: "#000" },
    yaxis: { range: [0, 1.05], title: "Membership (μ)" },
    xaxis: { title: "Universe of Discourse (x)" }
  };

  Plotly.newPlot(chartDiv, [trace], layout);
}

// ---------- Explain Button ----------
explainBtn.addEventListener("click", async () => {
  explanationLoading.style.display = "inline";
  explainBtn.disabled = true;
  try {
    const sliders = sliderArea.querySelectorAll("input[type='range']");
    const params = Array.from(sliders).map(s => parseFloat(s.value));
    const res = await fetch("/api/membership/explain", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mf_type: mfType, params })
    });
    const data = await res.json();
    explainBox.style.display = "block";
    explainText.innerHTML = data.explanation || "No explanation returned.";
    MathJax.typeset([explainText]);
  } finally {
    explanationLoading.style.display = "none";
    explainBtn.disabled = false;
  }
});

// ---------- MF Type Change ----------
document.getElementById("mf_type").addEventListener("change", e => {
  mfType = e.target.value;
  createSliders(mfType);
});

// ---------- Init ----------
createSliders(mfType);

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

  switch (type) {
    case "Triangular":
      paramLabels = ["a (Start)", "b (Peak)", "c (End)"];
      break;
    case "Trapezoidal":
      paramLabels = ["a (Start)", "b (Peak Start)", "c (Peak End)", "d (End)"];
      break;
    case "Gaussian":
      paramLabels = ["\u03C3 (Width)", "c (Center)"];
      break;
    case "Bell":
      paramLabels = ["a (Width)", "b (Slope)", "c (Center)"];
      break;
    case "Sigmoid":
      paramLabels = ["a (Slope)", "c (Center)"];
      break;
  }

  paramLabels.forEach(label => {
    const paramName = label.split(" ")[0];
    const container = document.createElement("div");
    container.className = "slider-container";
    container.innerHTML = `
      <div class="slider-label">
        <label>${label}: </label>
        <input type="number" id="num-${paramName}" value="5" min="0" max="10" step="0.1" class="num-input">
      </div>
      <input type="range" min="0" max="10" step="0.1" value="5" id="slider-${paramName}">
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
    line: { color: "#000000", width: 4 },
    fill: "tozeroy",
    fillcolor: "rgba(0, 0, 0, 0.2)",
    name: mfType
  };

  const layout = {
    title: {
      text: `${mfType} Membership Function`,
      font: { size: 20, color: '#000', weight: 'bold' }
    },
    paper_bgcolor: "#ffffff",
    plot_bgcolor: "#ffffff",
    font: { color: "#000000", size: 14 },
    margin: { t: 80, b: 80, l: 80, r: 80 },
    yaxis: { 
      range: [0, 1.05], 
      title: { text: "Membership (μ)", font: { size: 16 } },
      gridcolor: '#e0e0e0',
      zerolinecolor: '#000000',
      zerolinewidth: 2
    },
    xaxis: { 
      title: { text: "Universe of Discourse (x)", font: { size: 16 } },
      gridcolor: '#e0e0e0'
    },
    height: 500
  };

  Plotly.newPlot(chartDiv, [trace], layout, {responsive: true});
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

createSliders(mfType);

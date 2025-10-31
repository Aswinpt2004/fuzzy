function plotMatrix(id, matrix, title) {
  const data = [{
    z: matrix,
    type: 'heatmap',
    colorscale: 'Viridis'
  }];
  const layout = {
    title: title,
    margin: { t: 30, l: 40, r: 30, b: 40 },
    xaxis: { title: "Columns" },
    yaxis: { title: "Rows" }
  };
  Plotly.newPlot(id, data, layout);
}





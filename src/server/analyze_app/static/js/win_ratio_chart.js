import ChartInterface from "./chartInterface.js";

class WinRatioChart extends ChartInterface {
  constructor() {
    super("win_ratio_per_color");
  }

  createChart(data) {
    return new Chart($(this.chartId), {
      type: "bar",
      data: {
        labels: ["Win", "Draw", "Loss"],
        datasets: [
          {
            data: data.white,
          },
          {
            data: data.black,
          },
        ],
      },
      options: {
        plugins: {
          legend: { position: "bottom" },
        },
      },
    });
  }

  updateChart(hostName) {
    const data = this.data[hostName];
    const datasets = this.chart.data.datasets;

    datasets[0].data = data.white;
    datasets[1].data = data.black;

    datasets[0].label = `White (total ${data.white.reduce((a, b) => a + b)})`;
    datasets[1].label = `Black (total ${data.black.reduce((a, b) => a + b)})`;

    this.chart.update();
  }
}

$(document).ready(() => {
  new WinRatioChart();
});

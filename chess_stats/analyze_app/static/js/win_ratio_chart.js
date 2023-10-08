import ChartInterface from "./chartInterface.js";
Chart.defaults.color = "#DEE2E6";
Chart.defaults.font.size = 15;

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
            backgroundColor: "#ced4da",

            data: data.white,
          },
          {
            backgroundColor: "#3e4752",
            data: data.black,
          },
        ],
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

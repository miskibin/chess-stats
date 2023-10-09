import ChartInterface from "./chartInterface.js";

class AvgMoveTimeChart extends ChartInterface {
  constructor() {
    super("avg_time_per_move");
  }
  prepareData(chartData) {
    return {
      labels: Object.keys(chartData.player),
      datasets: [
        {
          data: Object.values(chartData.player),
          label: "Player",
          backgroundColor: "#d7B711",
        },
        {
          data: Object.values(chartData.opponent),
          label: "Opponent",
          backgroundColor: "#e56aa1",
        },
      ],
    };
  }

  createChart(data) {
    const chartData = this.prepareData(data);
    return new Chart($(this.chartId), {
      type: "bar",
      data: {},
      options: {
        maintainAspectRatio: false,
        aspectRatio: 0.7,
      },
    });
  }

  updateChart(hostName) {
    let chartData = this.data[hostName];
    this.chart.data = this.prepareData(chartData);
    this.chart.update();
  }
}

$(document).ready(() => {
  new AvgMoveTimeChart();
});

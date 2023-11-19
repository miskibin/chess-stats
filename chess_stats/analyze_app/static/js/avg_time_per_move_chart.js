import ChartInterface from "./chartInterface.js";

const camelCaseToSentenceCase = (camelCaseString) => {
  let result = camelCaseString.replace(/_/g, " ");
  return result.charAt(0).toUpperCase() + result.slice(1);
};

class AvgMoveTimeChart extends ChartInterface {
  constructor() {
    super("avg_time_per_move");
  }
  prepareData(chartData) {
    return {
      labels: Object.keys(chartData.player).map((key) =>
        camelCaseToSentenceCase(key)
      ),
      datasets: [
        {
          data: Object.values(chartData.player),
          label: "Player",
          // backgroundColor: "#d7B711",
        },
        {
          data: Object.values(chartData.opponent),
          label: "Opponent",
          // backgroundColor: "#e56aa1",
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
        scales: {
          y: {
            title: {
              display: true,
              text: "Time (s)",
            },
          },
          x: {
            title: {
              display: true,
              text: "Game Phase",
            },
          },
        },
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

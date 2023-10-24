import ChartInterface from "./chartInterface.js";

class EloOverTimeChart extends ChartInterface {
  constructor() {
    super("player_elo_over_time");
  }

  createChart(data) {
    const lichessData = data.filter((record) => record.host == "lichess.org");
    const chessComData = data.filter((record) => record.host == "chess.com");
    return new Chart($(this.chartId), {
      type: "line", // Set the chart type to "line"
      data: {
        labels: data.map((entry) => entry.x), // Use the 'x' values as labels
        datasets: [
          {
            label: "Lichess elo", // Label for the Lichess dataset
            data: lichessData.map((entry) => entry.y), // Use Lichess data for the 'y' values
            pointRadius: 2,
            tension: 0.2,
          },
          {
            label: "Chess.com elo", // Label for the Chess.com dataset
            pointRadius: 2,
            tension: 0.2,
            data: chessComData.map((entry) => entry.y), // Use Chess.com data for the 'y' values
          },
        ],
      },
      options: {
        // maintainAspectRatio: false,
        // aspectRatio: 1,
        scales: {
          x: {
            type: "time",
          },
        },
      },
    });
  }

  updateChart(hostName) {
    const data = this.data[hostName];
    this.chart.data.labels = data.map((entry) => entry.x);
    if (!data.some((entry) => entry.host == "lichess.org")) {
      this.chart.data.datasets[0].data = [];
      this.chart.data.datasets[1].data = data.map((entry) => entry.y);
    } else if (!data.some((entry) => entry.host == "chess.com")) {
      this.chart.data.datasets[1].data = [];
      this.chart.data.datasets[0].data = data.map((entry) => entry.y);
    } else {
      this.chart.data.datasets[0].data = data
        .filter((entry) => entry.host == "lichess.org")
        .map((entry) => entry.y);
      this.chart.data.datasets[1].data = data
        .filter((entry) => entry.host == "chess.com")
        .map((entry) => entry.y);
    }

    this.chart.update();
  }
}

$(document).ready(() => {
  new EloOverTimeChart();
});

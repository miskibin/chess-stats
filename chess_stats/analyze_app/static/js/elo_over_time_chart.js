import ChartInterface from "./chartInterface.js";

class EloOverTimeChart extends ChartInterface {
  constructor() {
    super("player_elo_over_time");
  }

  createChart(data) {
    const lichessData = data.filter((record) => record.host == "lichess.org");
    const chessComData = data.filter((record) => record.host == "chess.com");

    return new Chart($(this.chartId), {
      type: "line",
      data: {
        datasets: [
          {
            label: "Lichess elo",
            data: lichessData.map((entry) => ({ x: entry.x, y: entry.y })),
            pointRadius: 2,
            tension: 0.2,
            fill: false,
          },
          {
            label: "Chess.com elo",
            data: chessComData.map((entry) => ({ x: entry.x, y: entry.y })),
            pointRadius: 2,
            tension: 0.2,
            fill: false,
          },
        ],
      },
      options: {
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
    const lichessData = data.filter((record) => record.host == "lichess.org");
    const chessComData = data.filter((record) => record.host == "chess.com");

    this.chart.data.datasets[0].data = lichessData.map((entry) => ({
      x: entry.x,
      y: entry.y,
    }));
    this.chart.data.datasets[1].data = chessComData.map((entry) => ({
      x: entry.x,
      y: entry.y,
    }));

    this.chart.update();
  }
}

$(document).ready(() => {
  new EloOverTimeChart();
});

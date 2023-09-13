import ChartInterface from "./chartInterface.js";

class EloOverTimeChart extends ChartInterface {
  constructor() {
    super("win_ratio_per_color");
  }

  createChart(data) {
    return new Chart($(this.chartId), {
      type: "line", // Set the chart type to "line"
      data: {
        labels: data.map((entry) => entry.x), // Use the 'x' values as labels
        datasets: [
          {
            label: "Lichess Win Ratio", // Label for the Lichess dataset
            data: data.map((entry) => entry.y), // Use Lichess data for the 'y' values
          },
          {
            label: "Chess.com Win Ratio", // Label for the Chess.com dataset
            data: chessComData.map((entry) => entry.y), // Use Chess.com data for the 'y' values
          },
        ],
      },
      options: {
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              font: {
                size: 15,
              },
            },
          },
        },
        responsive: true,
        scales: {
          x: {
            type: "time",
            time: {
              unit: "month",
            },
            ticks: {
              font: {
                size: 15,
              },
            },
          },
          y: {
            ticks: {
              font: {
                size: 15,
              },
            },
          },
        },
      },
    });
  }

  updateChart(hostName) {
    const data = this.data[hostName];

    this.chart.update();
  }
}

$(document).ready(() => {
  new EloOverTimeChart();
});

// $(document).ready(function () {
//   const winRatioData = JSON.parse($("#data").text())["player_elo_over_time"];
//   const chart = createChart(winRatioData);
//   console.log(winRatioData);
//   function createChart(data) {
//     let chessComData = winRatioData.filter(
//       (record) => record.host == "chess.com"
//     );
//     let lichessData = winRatioData.filter(
//       (record) => record.host == "lichess.org"
//     );

//   // Initial chart setup
//   $("#player_elo_over_time_all").prop("checked", true);
//   updateChart(winRatioData);

//   $("#player_elo_over_time_all").click(() => updateChart(winRatioData));
//   $("#player_elo_over_time_chess_com").click(() =>
//     updateChart(winRatioData.filter((record) => record.host === "chess.com"))
//   );
//   $("#player_elo_over_time_lichess").click(() =>
//     updateChart(winRatioData.filter((record) => record.host === "lichess.org"))
//   );
//   function updateChart(data) {
//     // Update labels for both datasets (Lichess and Chess.com)
//     chart.data.labels = data.map((entry) => entry.x);
//     // Check if there is data for Lichess (at least one data point)
//     if (!data.some((entry) => entry.host == "lichess.org")) {
//       chart.data.datasets[0].data = [];
//       chart.data.datasets[1].data = data.map((entry) => entry.y);
//     } else if (!data.some((entry) => entry.host == "chess.com")) {
//       chart.data.datasets[1].data = [];
//       chart.data.datasets[0].data = data.map((entry) => entry.y);
//     } else {
//       chart.data.datasets[0].data = data
//         .filter((entry) => entry.host == "lichess.org")
//         .map((entry) => entry.y);
//       chart.data.datasets[1].data = data
//         .filter((entry) => entry.host == "chess.com")
//         .map((entry) => entry.y);
//     }
//     // set x axis min value to the min date

//     chart.update();
//   }
// });

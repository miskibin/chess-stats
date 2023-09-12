$(document).ready(function () {
  const winRatioData = JSON.parse($("#data").text())["player_elo_over_time"];
  const chart = createChart(winRatioData);
  console.log(winRatioData);
  function createChart(data) {
    return new Chart($("#player_elo_over_time_chart"), {
      type: "line", // Set the chart type to "line"
      data: {
        labels: data.map((entry) => entry.x), // Use the 'x' values as labels
        datasets: [
          {
            label: "Win Ratio", // Label for the dataset
            data: data.map((entry) => entry.y), // Use the 'y' values as data points
            borderColor: "blue", // Line color
            backgroundColor: "rgba(0, 0, 255, 0.2)", // Line fill color
            borderWidth: 2, // Line width
            pointRadius: 5, // Point size
            pointBackgroundColor: "blue", // Point color
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
            stacked: true,
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

  // Initial chart setup
  $("#player_elo_over_time_all").prop("checked", true);
  updateChart(winRatioData);

  $("#player_elo_over_time_all").click(() => updateChart(winRatioData));
  $("#player_elo_over_time_chess_com").click(() =>
    updateChart(winRatioData.filter((record) => record.host === "chess.com"))
  );
  $("#player_elo_over_time_lichess").click(() =>
    updateChart(winRatioData.filter((record) => record.host === "lichess.org"))
  );

  function updateChart(data) {
    chart.data.labels = data.map((entry) => entry.x);
    chart.data.datasets[0].data = data.map((entry) => entry.y);
    chart.update();
  }
});

// $(document).ready(function () {
//   function createEloOverTimeChart(data, label, borderColor) {
//     return new Chart($("#player_elo_over_time"), {
//       type: "line",
//       data: {
//         datasets: [
//           {
//             label: label,
//             data: data,
//             fill: true,
//             backgroundColor: "rgba(72,72,176,0.2)",
//             borderColor: borderColor,
//             borderWidth: 4,
//             borderDash: [],
//             borderDashOffset: 0.0,
//             pointBackgroundColor: borderColor,
//             pointBorderColor: "rgba(255,255,255,0)",
//             pointHoverBackgroundColor: borderColor,
//             pointBorderWidth: 20,
//             pointHoverRadius: 4,
//             pointHoverBorderWidth: 15,
//             pointRadius: 4,
//             tension: 0.4,
//           },
//         ],
//       },
//       options: {
//         plugins: {
//           legend: {
//             position: "bottom",
//             labels: {
//               font: {
//                 size: 15,
//               },
//             },
//           },
//         },
//         responsive: true,
//         scales: {
//           x: {
//             type: "time",
//             time: {
//               unit: "month",
//             },
//             ticks: {
//               font: {
//                 size: 15,
//               },
//             },
//           },
//           y: {
//             stacked: true,
//             ticks: {
//               font: {
//                 size: 15,
//               },
//             },
//           },
//         },
//       },
//     });
//   }

//   function updateChart(chart, data, label, borderColor) {
//     chart.destroy();
//     chart = createEloOverTimeChart(data, label, borderColor);
//     chart.data.datasets[0].data = data;
//     chart.data.datasets[0].label = label;
//     chart.update();
//     return chart;
//   }

//   const playerEloOverTime = JSON.parse($("#data").text())[
//     "player_elo_over_time"
//   ];
//   const chessComData = playerEloOverTime.filter((d) => d.host === "chess.com");
//   const lichessData = playerEloOverTime.filter((d) => d.host === "lichess.org");

//   let chart = createEloOverTimeChart(chessComData, "Chess.com Elo", "#d048b6");

//   $("#player_elo_over_chess_com").click(function () {
//     chart = updateChart(chart, chessComData, "Chess.com Elo", "#d048b6");
//   });

//   $("#player_elo_over_time_lichess").click(function () {
//     chart = updateChart(
//       chart,
//       lichessData,
//       "lichess Elo",
//       "rgba(255, 0, 232, 0.6)"
//     );
//   });
// });

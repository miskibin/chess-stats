var data2 = {
  "chess.com": {
    white: [7, 0, 6],
    black: [6, 1, 5],
  },
  "lichess.org": {
    white: [9, 2, 3],
    black: [3, 1, 7],
  },
};

function win_ratio_chart(win_ratio) {
  const labels = ["Win", "Draw", "Loss"];
  const data = {
    labels: labels,

    datasets: [
      {
        label: `White (total ${win_ratio.white.reduce((a, b) => a + b, 0)})`,
        data: win_ratio.white,
        borderWidth: 2,
        backgroundColor: "rgba(183, 183, 183, 1)",
        borderColor: "rgba(0, 0, 0, 1)",
        borderRadius: 2,
        borderSkipped: false,
      },
      {
        backgroundColor: "rgba(26, 24, 25, 1)",
        borderColor: "rgba(222, 236, 236, 1)",
        label: `Black (total ${win_ratio.black.reduce((a, b) => a + b, 0)})`,
        data: win_ratio.black,
        borderWidth: 2,
        borderRadius: 2,
        borderSkipped: false,
      },
    ],
  };

  const config = {
    type: "bar",
    data: data,
    options: {
      plugins: {
        legend: {
          position: "bottom",

          labels: {
            // This more specific font property overrides the global property
            font: {
              size: 15,
            },
          },
        },
      },
      responsive: true,
      scales: {
        x: {
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
  };
  const myChart = new Chart(document.getElementById("win_ratio_chart"), config);
  return myChart;
}

const win_ratio_data = JSON.parse(document.getElementById("data").textContent)[
  "win_ratio_per_color"
];
console.log(data);
const chess_com_win_ratio = win_ratio_data["chess.com"];
const lichess_win_ratio = win_ratio_data["lichess.org"];
total_data = win_ratio_data["total"];

ratio_chart = win_ratio_chart(total_data);

document.getElementById("win-ratio").onclick = function () {
  ratio_chart.data.datasets[0].data = total_data["white"];
  ratio_chart.data.datasets[1].data = total_data["black"];
  ratio_chart.data.datasets[0].label = `White (total ${total_data[
    "white"
  ].reduce((a, b) => a + b, 0)})`;
  ratio_chart.data.datasets[1].label = `Black (total ${total_data[
    "black"
  ].reduce((a, b) => a + b, 0)})`;

  ratio_chart.update();
};

// toggle between chess.com and lichess.org data
document.getElementById("chess-com-win-ratio").onclick = function () {
  ratio_chart.data.datasets[0].data = chess_com_win_ratio["white"];
  ratio_chart.data.datasets[1].data = chess_com_win_ratio["black"];
  ratio_chart.data.datasets[0].label = `White (total ${chess_com_win_ratio[
    "white"
  ].reduce((a, b) => a + b, 0)})`;
  ratio_chart.data.datasets[1].label = `Black (total ${chess_com_win_ratio[
    "black"
  ].reduce((a, b) => a + b, 0)})`;

  ratio_chart.update();
};

document.getElementById("lichess-win-ratio").onclick = function () {
  ratio_chart.data.datasets[0].data = lichess_win_ratio["white"];
  ratio_chart.data.datasets[1].data = lichess_win_ratio["black"];
  ratio_chart.data.datasets[0].label = `White (total ${lichess_win_ratio[
    "white"
  ].reduce((a, b) => a + b, 0)})`;
  ratio_chart.data.datasets[1].label = `Black (total ${lichess_win_ratio[
    "black"
  ].reduce((a, b) => a + b, 0)})`;

  ratio_chart.update();
};

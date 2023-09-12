function openings_chart(openings, title) {
  console.log(openings);
  const data = {
    labels: openings.map((opening) => opening.opening),
    datasets: [
      {
        label: "Win",
        data: openings.map((opening) => opening.win),
        backgroundColor: "rgba(0, 255, 0, 0.4)",
        borderColor: "rgba(0, 255, 0, 1)",
        borderWidth: 1,
      },
      {
        label: "Lost",
        data: openings.map((opening) => opening.lost),
        backgroundColor: "rgba(255, 0, 0, 0.4)",
        borderColor: "rgba(255, 0, 0, 1)",
        borderWidth: 1,
      },
      {
        label: "Draw",
        data: openings.map((opening) => opening.draws),
        backgroundColor: "rgba(0, 0, 255, 0.4)",
        borderColor: "rgba(0, 0, 255, 1)",
        borderWidth: 1,
      },
    ],
  };

  const ctx = $("#win_ratio_per_opening_and_color_chart");
  const myChart = new Chart(ctx, {
    type: "bar",
    data: data,
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

$(document).ready(function () {
  const openingsData = JSON.parse($("#data").text())[
    "win_ratio_per_opening_and_color"
  ];
  openings_chart(openingsData[0], "Openings score as white");
  openings_chart(openingsData[1], "Openings score as black");
});

function updateChart(data) {
  chart.data.datasets[0].data = data.white;
  chart.data.datasets[1].data = data.black;
  chart.data.datasets[0].label = `White (total ${data.white.reduce(
    (a, b) => a + b,
    0
  )})`;
  chart.data.datasets[1].label = `Black (total ${data.black.reduce(
    (a, b) => a + b,
    0
  )})`;
  chart.update();
}
$("#win_ratio_per_opening_and_color_all").prop("checked", true);
updateChart(winRatioData["total"]);
$("#win_ratio_per_opening_and_color_all").click(() =>
  updateChart(winRatioData["total"])
);
$("#win_ratio_per_opening_and_color_chess_com").click(() =>
  updateChart(winRatioData["chess.com"])
);
$("#win_ratio_per_opening_and_color_lichess").click(() =>
  updateChart(winRatioData["lichess.org"])
);

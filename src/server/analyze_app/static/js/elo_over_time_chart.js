function elo_over_time_chart(player_elo_over_time) {
  console.log(player_elo_over_time);

  const data = {
    datasets: [
      {
        label: "chess com elo",
        data: player_elo_over_time,
        fill: true,
        backgroundColor: "rgba(72,72,176,0.2)",
        borderColor: "#d048b6",
        borderWidth: 4,
        borderDash: [],
        borderDashOffset: 0.0,
        pointBackgroundColor: "#d048b6",
        pointBorderColor: "rgba(255,255,255,0)",
        pointHoverBackgroundColor: "#d048b6",
        pointBorderWidth: 20,
        pointHoverRadius: 4,
        pointHoverBorderWidth: 15,
        pointRadius: 4,
        tension: 0.4,
      },
    ],
  };

  const config = {
    type: "line",
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
  };
  return (elo_over_time_chart_object = new Chart(
    document.getElementById("elo_over_time_chart").getContext("2d"),
    config
  ));
}
player_elo_over_time = JSON.parse(document.getElementById("data").textContent)[
  "player_elo_over_time"
];
const chess_com_data = player_elo_over_time.filter(function (d) {
  return d.host == "chess.com";
});
// get data where host is lichess.org
const lichess_data = player_elo_over_time.filter(function (d) {
  return d.host == "lichess.org";
});

chart = elo_over_time_chart(chess_com_data);
// on click of chess.com toggle
document.getElementById("chess-com-elo").onclick = function () {
  chart.destroy();
  chart = elo_over_time_chart(chess_com_data);
  chart.data.datasets[0].data = chess_com_data;
  chart.data.datasets[0].label = "Chess.com Elo";
  chart.update();
};
document.getElementById("lichess-elo").onclick = function () {
  chart.destroy();
  chart = elo_over_time_chart(lichess_data);
  chart.data.datasets[0].label = "lichess Elo";
  chart.data.datasets[0].borderColor = "rgba(255, 0, 232, 0.6)";
  // ovveride the scale
  chart.update();
};

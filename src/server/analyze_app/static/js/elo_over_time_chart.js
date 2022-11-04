function elo_over_time_chart(elo_over_time) {
  console.log(elo_over_time);
  const data = {
    datasets: [
      {
        label: "chess com elo",
        data: elo_over_time,
        fill: true,
        backgroundColor: "rgba(72,72,176,0.4)",
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
          stacked: true,
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
  const myChart = new Chart(
    document.getElementById("elo_over_time_chart").getContext("2d"),
    config
  );
}
player_elo_over_time = JSON.parse(document.getElementById("data").textContent)[
  "player_elo_over_time"
];
elo_over_time_chart(player_elo_over_time);

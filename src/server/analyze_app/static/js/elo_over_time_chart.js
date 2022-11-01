function elo_over_time_chart(elo_over_time) {
  console.log(elo_over_time);
  const data = {
    datasets: [
      {
        label: "chess com elo",
        data: elo_over_time,
        lineTension: 0,
        backgroundColor: "rgba(246, 15, 36, 0)",
        borderColor: "rgba(246, 15, 36, 0.6)",
      },
    ],
  };

  const config = {
    type: "line",
    data: data,
    options: {
      elements: {
        point: {
          radius: 0,
        },
      },
      scales: {
        x: {
          type: "time",
          time: {
            unit: "month",
          },
        },
      },
      responsive: true,
      plugins: {
        legend: {
          position: "top",
        },
        title: {
          display: true,
          text: "your elo over time",
          font: {
            size: 50,
            weight: "bold",
            lineHeight: 1.2,
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

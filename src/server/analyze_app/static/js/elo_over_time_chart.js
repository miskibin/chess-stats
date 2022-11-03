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
      tooltips: {
        backgroundColor: "#fff",
        titleFontColor: "#333",
        bodyFontColor: "#666",
        bodySpacing: 4,
        xPadding: 12,
        mode: "nearest",
        intersect: 0,
        position: "nearest",
      },
      responsive: true,
      elements: {
        point: {
          radius: 5,

          hoverRadius: 5,

          hoverBorderWidth: 2,

          hoverBackgroundColor: "rgba(246, 15, 36, 0.6)",
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

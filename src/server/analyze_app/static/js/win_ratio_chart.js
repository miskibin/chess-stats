function win_ratio_chart() {
  let win_ratio = JSON.parse(document.getElementById("data").textContent)[
    "win_ratio_per_color"
  ];
  console.log(win_ratio);
  const labels = ["Win", "Draw", "Loss"];
  const data = {
    labels: labels,

    datasets: [
      {
        label: `White (total ${win_ratio[0] + win_ratio[1] + win_ratio[2]})`,
        data: win_ratio.slice(0, 3),
        borderWidth: 2,
        backgroundColor: "rgba(183, 183, 183, 1)",
        borderColor: "rgba(0, 0, 0, 1)",
        borderRadius: 2,
        borderSkipped: false,
      },
      {
        backgroundColor: "rgba(26, 24, 25, 1)",
        borderColor: "rgba(222, 236, 236, 1)",
        label: `Black (total ${win_ratio[3] + win_ratio[4] + win_ratio[5]})`,
        data: win_ratio.slice(3),
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
  const myChart = new Chart(document.getElementById("bar_chart"), config);
}
win_ratio_chart();

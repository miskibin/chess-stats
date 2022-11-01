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
        backgroundColor: "rgba(183, 183, 183, 0.72)",
        borderColor: "rgba(0, 0, 0, .6)",
        borderRadius: 2,
        borderSkipped: false,
      },
      {
        backgroundColor: "rgba(26, 24, 25, 0.8)",
        borderColor: "rgba(46, 36, 36, 0.2)",
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
      responsive: true,
      plugins: {
        legend: {
          position: "top",
        },
        title: {
          display: true,
          text: "Win ratio",
          font: {
            size: 50,
            weight: "bold",
            lineHeight: 1.2,
          },
        },
      },
    },
  };
  const myChart = new Chart(document.getElementById("bar_chart"), config);
}
win_ratio_chart();

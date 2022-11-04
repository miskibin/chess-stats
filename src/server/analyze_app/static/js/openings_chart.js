function openings_chart(openings, title, id) {
  console.log(openings);
  let data = {
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
  let ctx = document.getElementById(id).getContext("2d");
  let myChart = new Chart(ctx, {
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
  });
}
let openings = JSON.parse(document.getElementById("data").textContent)[
  "win_ratio_per_opening_and_color"
];
openings_chart(openings[0], "Openings score as white", "white_openings_chart");
openings_chart(openings[1], "Openings score as black", "black_openings_chart");

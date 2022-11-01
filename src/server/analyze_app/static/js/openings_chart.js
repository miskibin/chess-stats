function openings_chart(openings, title, id) {
  console.log(openings);
  let data = {
    labels: openings.map((opening) => opening.opening),
    datasets: [
      {
        label: "Win",
        data: openings.map((opening) => opening.win),
        backgroundColor: "rgba(0, 255, 0, 0.2)",
        borderColor: "rgba(0, 255, 0, 1)",
        borderWidth: 1,
      },
      {
        label: "Lost",
        data: openings.map((opening) => opening.lost),
        backgroundColor: "rgba(255, 0, 0, 0.2)",
        borderColor: "rgba(255, 0, 0, 1)",
        borderWidth: 1,
      },
      {
        label: "Draw",
        data: openings.map((opening) => opening.draws),
        backgroundColor: "rgba(0, 0, 255, 0.2)",
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
      responsive: true,
      plugins: {
        legend: {},
        title: {
          display: true,
          text: title,
          font: {
            size: 50,
            weight: "bold",
            lineHeight: 1.2,
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

function mistakes_per_phase_chart(mistakes, title) {
  var ctx = document
    .getElementById("mistakes_per_phase_chart")
    .getContext("2d");
  data = {
    labels: ["Opening", "Middle", "End"],
    datasets: [
      {
        label: "Inaccurate",
        backgroundColor: "rgba(0, 132, 0, 0.6)",
        borderColor: "rgba(0, 132, 0,1)",
        borderWidth: 1,
        hoverBackgroundColor: "rgba(0, 132, 0,0.8)",
        hoverBorderColor: "rgba(0, 132, 0,1)",
        data: [
          mistakes["Opening"][0],
          mistakes["Middle"][0],
          mistakes["End"][0],
        ],
      },
      {
        label: "mistakes",
        backgroundColor: "rgba(0, 99, 132, 0.6)",
        borderColor: "rgba(0,99,132,1)",
        borderWidth: 1,
        hoverBackgroundColor: "rgba(0,99,132,0.8)",
        hoverBorderColor: "rgba(0,99,132,1)",
        data: [
          mistakes["Opening"][1],
          mistakes["Middle"][1],
          mistakes["End"][1],
        ],
      },
      {
        label: "blunders",
        backgroundColor: "rgba(255, 99, 132, 0.6)",
        borderColor: "rgba(255,99,132,1)",
        borderWidth: 1,
        hoverBackgroundColor: "rgba(255,99,132,0.8)",
        hoverBorderColor: "rgba(255,99,132,1)",
        data: [
          mistakes["Opening"][2],
          mistakes["Middle"][2],
          mistakes["End"][2],
        ],
      },
    ],
  };

  var myChart = new Chart(ctx, {
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
          stacked: true,

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
  });
}

mistakes = JSON.parse(document.getElementById("data").textContent)[
  "mistakes_per_phase"
];
console.log(mistakes);
mistakes_per_phase_chart(mistakes, "Mistakes per phase");

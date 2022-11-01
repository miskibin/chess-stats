openings = [
  {
    opening: "Sicilian Defense: Alapin Variation",
    count: 10,
    win: 3,
    lost: 3,
    draws: 4,
  },
  {
    opening: "Vienna Game: Vienna Gambit",
    count: 8,
    win: 4,
    lost: 4,
    draws: 0,
  },
  {
    opening: "Sicilian Defense: Old Sicilian",
    count: 7,
    win: 4,
    lost: 3,
    draws: 0,
  },
  {
    opening: "Sicilian Defense: Bowdler Attack",
    count: 4,
    win: 2,
    lost: 2,
    draws: 0,
  },
  {
    opening: "Caro-Kann Defense",
    count: 3,
    win: 0,
    lost: 2,
    draws: 1,
  },
];

function openings_chart() {
  let openings = JSON.parse(document.getElementById("data").textContent)[
    "openings"
  ];
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
        label: "Draws",
        data: openings.map((opening) => opening.draws),
        backgroundColor: "rgba(0, 0, 255, 0.2)",
        borderColor: "rgba(0, 0, 255, 1)",
        borderWidth: 1,
      },
    ],
  };
  let ctx = document.getElementById("openings_chart").getContext("2d");
  let myChart = new Chart(ctx, {
    type: "bar",
    data: data,
    options: {
      responsive: true,
      plugins: {
        legend: {},
        title: {
          display: true,
          text: "Win ratio per opening",
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
openings_chart();

[
  [
    {
      opening: "Sicilian Defense: Alapin Variation",
      count: 19,
      win: 9,
      lost: 7,
      draws: 4,
    },
    {
      opening: "Vienna Game: Vienna Gambit",
      count: 17,
      win: 8,
      lost: 9,
      draws: 0,
    },
    {
      opening: "Caro-Kann Defense",
      count: 11,
      win: 3,
      lost: 7,
      draws: 1,
    },
    {
      opening: "Vienna Game",
      count: 8,
      win: 3,
      lost: 4,
      draws: 1,
    },
    {
      opening: "French Defense: Queen's Knight",
      count: 4,
      win: 2,
      lost: 1,
      draws: 1,
    },
  ],
  [
    {
      opening: "Sicilian Defense: Old Sicilian",
      count: 10,
      win: 6,
      lost: 4,
      draws: 0,
    },
    {
      opening: "Sicilian Defense: Bowdler Attack",
      count: 7,
      win: 4,
      lost: 3,
      draws: 0,
    },
    {
      opening: "Sicilian Defense: McDonnell Attack",
      count: 6,
      win: 3,
      lost: 2,
      draws: 1,
    },
    {
      opening: "Queen's Gambit Declined: Normal Defense",
      count: 4,
      win: 3,
      lost: 1,
      draws: 0,
    },
    {
      opening: "Sicilian Defense",
      count: 4,
      win: 3,
      lost: 1,
      draws: 0,
    },
  ],
];

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
        label: "Draws",
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
  "openings_per_color"
];
openings_chart(openings[0], "White openings", "white_openings_chart");
openings_chart(openings[1], "Black openings", "black_openings_chart");

$(document).ready(function () {
  const labels = ["Win", "Draw", "Loss"];
  const winRatioData = JSON.parse($("#data").text())["win_ratio_per_color"];
  const chart = createChart(winRatioData["total"]);

  function createChart(data) {
    return new Chart($("#win_ratio_per_color_chart"), {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            data: data.white,
          },
          {
            data: data.black,
          },
        ],
      },
      options: {
        plugins: {
          legend: { position: "bottom" },
        },
      },
    });
  }

  function updateChart(data) {
    chart.data.datasets[0].data = data.white;
    chart.data.datasets[1].data = data.black;
    chart.data.datasets[0].label = `White (total ${data.white.reduce(
      (a, b) => a + b,
      0
    )})`;
    chart.data.datasets[1].label = `Black (total ${data.black.reduce(
      (a, b) => a + b,
      0
    )})`;
    chart.update();
  }
  $("#win_ratio_per_color_all").prop("checked", true);
  updateChart(winRatioData["total"]);
  $("#win_ratio_per_color_all").click(() => updateChart(winRatioData["total"]));
  $("#win_ratio_per_color_chess_com").click(() =>
    updateChart(winRatioData["chess.com"])
  );
  $("#win_ratio_per_color_lichess").click(() =>
    updateChart(winRatioData["lichess.org"])
  );
});

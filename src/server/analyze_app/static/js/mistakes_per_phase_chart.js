import ChartInterface from "./chartInterface.js";

class MistakesChart extends ChartInterface {
  constructor() {
    super("mistakes_per_phase");
  }

  prepareData(mistakes) {
    return {
      labels: ["Opening", "Middle", "End"],
      datasets: [
        {
          label: "Inaccuracies",
          data: [
            mistakes["Opening"][0],
            mistakes["Middle"][0],
            mistakes["End"][0],
          ],
        },
        {
          label: "Mistakes",
          data: [
            mistakes["Opening"][1],
            mistakes["Middle"][1],
            mistakes["End"][1],
          ],
        },
        {
          label: "Blunders",
          data: [
            mistakes["Opening"][2],
            mistakes["Middle"][2],
            mistakes["End"][2],
          ],
        },
      ],
    };
  }

  createChart(data) {
    return new Chart($(this.chartId), {
      type: "bar",
      data: this.prepareData(data),
      options: {
        responsive: true,
        scales: {
          x: {
            stacked: true,
          },
          y: {
            stacked: true,
          },
        },
      },
    });
  }

  updateChart(hostName) {
    const data = this.data[hostName];
    this.chart.data = this.prepareData(data);
    this.chart.update();
  }
}

$(document).ready(() => {
  new MistakesChart();
});

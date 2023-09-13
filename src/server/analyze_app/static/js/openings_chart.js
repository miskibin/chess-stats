import ChartInterface from "./chartInterface.js";

class OpeningsChart extends ChartInterface {
  constructor(fieldName) {
    super(fieldName);
  }

  prepareData(data) {
    return {
      labels: data.map((opening) => opening.opening),
      datasets: [
        {
          label: "Win",
          data: data.map((opening) => opening.win),
        },
        {
          label: "Lost",
          data: data.map((opening) => opening.lost),
        },
        {
          label: "Draw",
          data: data.map((opening) => opening.draws),
        },
      ],
    };
  }

  createChart(data) {
    console.log(data);
    const chartData = this.prepareData(data);

    return new Chart($(this.chartId), {
      type: "bar",
      data: chartData,
      options: {
        plugins: {
          legend: {
            position: "bottom",
            labels: {
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

  updateChart(hostName) {
    let data = this.data[hostName];
    this.chart.data = this.prepareData(data);
    this.chart.update();
  }
}

$(document).ready(() => {
  new OpeningsChart("win_ratio_per_opening_as_white");
  new OpeningsChart("win_ratio_per_opening_as_black");
});

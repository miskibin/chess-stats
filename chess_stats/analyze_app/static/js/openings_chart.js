import ChartInterface from "./chartInterface.js";

class OpeningsChart extends ChartInterface {
  constructor(fieldName) {
    super(fieldName);
  }

  prepareData(chartData) {
    return {
      labels: chartData.map((opening) => opening.opening),
      datasets: [
        {
          label: "Win",
          data: chartData.map((opening) => opening.win),
        },
        {
          label: "loss",
          data: chartData.map((opening) => opening.loss),
        },
        {
          label: "draw",
          data: chartData.map((opening) => opening.draw),
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
    });
  }

  updateChart(hostName) {
    let chartData = this.data[hostName];
    this.chart.data = this.prepareData(chartData);
    this.chart.update();
  }
}

$(document).ready(() => {
  new OpeningsChart("win_ratio_per_opening_as_white");
  new OpeningsChart("win_ratio_per_opening_as_black");
});

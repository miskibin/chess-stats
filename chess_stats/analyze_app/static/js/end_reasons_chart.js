import ChartInterface from "./chartInterface.js";

class OpeningsChart extends ChartInterface {
  constructor(fieldName) {
    super(fieldName);
  }

  prepareData(chartData) {
    return {
      //   labels: chartData.win.map((data) => data.end_reason),
      labels: ["mate", "resign", "timeout"],
      datasets: [
        {
          label: "Win",
          data: chartData.win.map((data) => data.count),
        },
        {
          label: "loss",
          data: chartData.loss.map((data) => data.count),
        },
      ],
    };
  }

  createChart(data) {
    console.log(data);
    const chartData = this.prepareData(data);

    return new Chart($(this.chartId), {
      type: "radar",
      data: chartData,
      options: {
        tension: 0.2,
        maintainAspectRatio: false,
        aspectRatio: 0.7,
      },
    });
  }

  updateChart(hostName) {
    let chartData = this.data[hostName];
    this.chart.data = this.prepareData(chartData);
    this.chart.update();
  }
}

$(document).ready(() => {
  new OpeningsChart("end_reasons");
});

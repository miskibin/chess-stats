import ChartInterface from "./chartInterface.js";

class OpponentRatingChart extends ChartInterface {
  constructor(fieldName) {
    super(fieldName);
  }

  prepareData(chartData) {
    return {
      labels: ["Win", "Draw", "Loss"], // Each subplot will have win and loss as labels
      datasets: [
        {
          label: "Higher rated opponent",
          data: chartData.higher_ratio, // Assuming the ratio is in percentage. Subtract from 100 to get loss ratio.
          backgroundColor: ["#66EE99", "#447788", "#EE4455"],
        },
        {
          label: "Simmilar rated opponent",
          data: chartData.similar_ratio, // Assuming the ratio is in percentage.
          backgroundColor: ["#66EE99", "#447788", "#EE4455"],
        },
        {
          label: "Lower rated opponent",
          data: chartData.lower_ratio, // Assuming the ratio is in percentage.
          backgroundColor: ["#66EE99", "#447788", "#EE4455"],
        },
      ],
    };
  }

  createChart(data) {
    console.log(data);
    const chartData = this.prepareData(data);

    return new Chart($(this.chartId), {
      type: "doughnut", // Using doughnut for better distinction, but you can use 'pie' if preferred
      data: chartData,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        aspectRatio: 0.7,
        legend: {
          position: "top",
        },
        tooltips: {
          mode: "index",
          intersect: false,
        },
        plugins: {
          labels: {
            render: "percentage",
            precision: 2,
          },
        },
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
  new OpponentRatingChart("win_per_opponent_rating");
});

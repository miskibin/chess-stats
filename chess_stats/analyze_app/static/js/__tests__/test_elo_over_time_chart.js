const EloOverTimeChart = require("../elo_over_time_chart");
describe("EloOverTimeChart", () => {
  let chart;

  beforeEach(() => {
    chart = new EloOverTimeChart("field");
    chart.data = {
      "lichess.org": [
        { host: "lichess.org", x: 1, y: 1 },
        { host: "lichess.org", x: 2, y: 2 },
      ],
      "chess.com": [
        { host: "chess.com", x: 3, y: 3 },
        { host: "chess.com", x: 4, y: 4 },
      ],
    };
    chart.chart = {
      data: {
        datasets: [{ data: [] }, { data: [] }],
      },
      update: jest.fn(),
    };
  });

  test("updates chart data based on hostName", () => {
    chart.updateChart("lichess.org");
    expect(chart.chart.data.datasets[0].data).toEqual([
      { x: 1, y: 1 },
      { x: 2, y: 2 },
    ]);
    expect(chart.chart.data.datasets[1].data).toEqual([]);

    chart.updateChart("chess.com");
    expect(chart.chart.data.datasets[0].data).toEqual([]);
    expect(chart.chart.data.datasets[1].data).toEqual([
      { x: 3, y: 3 },
      { x: 4, y: 4 },
    ]);
  });

  test('combines data from all sources when hostName is "all"', () => {
    chart.updateChart("all");
    expect(chart.chart.data.datasets[0].data).toEqual([
      { x: 1, y: 1 },
      { x: 2, y: 2 },
    ]);
    expect(chart.chart.data.datasets[1].data).toEqual([
      { x: 3, y: 3 },
      { x: 4, y: 4 },
    ]);
  });
});

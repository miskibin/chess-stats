/**
 * Interface for creating and updating charts associated with different hosts.
 * Subclasses must implement the `updateChart(hostName)` method to define
 * how the chart is updated for a specific host.
 *
 * @class ChartInterface
 */
class ChartInterface {
  chartSuffix = "_chart";

  /**
   * @static
   * @property {string[]} hosts - Array of host names.
   */
  static hosts = ["total", "chess_com", "lichess_org"];

  constructor(fieldName) {
    this.data = JSON.parse($("#data").text())[fieldName];

    this.chartId = `#${fieldName}${this.chartSuffix}`;
    if (!this.data) {
      console.log("No data provided for chart initialization");
      return;
    }
    this.chart = this.createChart(this.data["total"]);
    /**
     * @property {Object} buttons - A dictionary of button names associated with hosts.
     */
    this.buttons = {};
    for (const host of ChartInterface.hosts) {
      this.buttons[host] = `#${fieldName}_${host}`;
    }
    ChartInterface.hosts.forEach((host) => {
      $(this.buttons[host]).click(() => this.updateChart(host));
    });

    this.updateChart("total");
  }

  updateChart(hostName) {
    throw new Error(
      "Subclasses must implement the updateChart(hostName) method."
    );
  }
  createChart(data) {
    throw new Error("Subclasses must implement the createChart(data) method.");
  }
}
export default ChartInterface;

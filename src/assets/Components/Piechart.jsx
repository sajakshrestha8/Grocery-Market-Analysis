import { Pie } from "recharts";

export default function Piechart() {
  const chartData = {
    labels: ["January", "February", "March", "April", "May", "June"],
    datasets: [
      {
        label: "Monthly Sales",
        data: [85000, 23000, 18000, 22000, 25000, 20000],
        backgroundColor: [
          "#FF6384",
          "#36A2EB",
          "#FFCE56",
          "#FF9F40",
          "#4BC0C0",
          "#9966FF",
        ],
        hoverBackgroundColor: [
          "#FF6384",
          "#36A2EB",
          "#FFCE56",
          "#FF9F40",
          "#4BC0C0",
          "#9966FF",
        ],
      },
    ],
  };

  return (
    <div>
      <h2>Monthly Sales Pie Chart</h2>
      <Pie data={chartData} />
    </div>
  );
}

import React from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const PointsChart = () => {
  const sampleData = {
    dates: [
      "2023-05-01",
      "2023-05-03",
      "2023-05-05",
      "2023-05-07",
      "2023-05-09",
    ],
    points: [22, 30, 25, 28, 32],
  };

  const chartData = {
    labels: sampleData.dates,
    datasets: [
      {
        label: "Points",
        data: sampleData.points,
        fill: false,
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderColor: "rgba(75, 192, 192, 1)",
      },
    ],
  };

  const options = {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  return (
    <div className="bg-white shadow rounded p-4">
      <h2 className="text-xl font-bold mb-2">Player Points in Last 5 Games</h2>
      <Line data={chartData} options={options} />
    </div>
  );
};

export default PointsChart;

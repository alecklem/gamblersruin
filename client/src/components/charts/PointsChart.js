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

const PointsChart = ({ data }) => {
  const chartData = {
    labels: data.dates,
    datasets: [
      {
        label: "Points",
        data: data.points,
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
    <div className="bg-white shadow rounded p-4 h-64">
      <h2 className="text-xl font-bold mb-2 text-center">Last 5 PPG</h2>
      <Line data={chartData} options={options} />
    </div>
  );
};

export default PointsChart;

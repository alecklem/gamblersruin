import React from "react";
import { Line } from "react-chartjs-2";

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
    <div className="bg-white shadow rounded p-4">
      <h2 className="text-xl font-bold mb-2">Player Points in Last 5 Games</h2>
      <Line data={chartData} options={options} />
    </div>
  );
};

export default PointsChart;

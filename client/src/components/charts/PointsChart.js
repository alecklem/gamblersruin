import {
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  Title,
  Tooltip,
} from "chart.js";
import ChartDataLabels from "chartjs-plugin-datalabels";
import React from "react";
import { Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ChartDataLabels
);

const PointsChart = ({ data }) => {
  const chartData = {
    labels: data.dates.reverse(), // Reverse to make the dates from farthest to closest
    datasets: [
      {
        label: "Points",
        data: data.points.reverse(), // Reverse to match the order of dates
        fill: false,
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderColor: "rgba(75, 192, 192, 1)",
      },
    ],
  };

  const options = {
    plugins: {
      legend: {
        display: false, // Hide the legend
      },
      datalabels: {
        display: true,
        color: "black",
        align: "top",
        formatter: function (value) {
          return value;
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          padding: 10, // Add padding to prevent values from getting cut off
        },
      },
      x: {
        ticks: {
          padding: 10, // Add padding to prevent values from getting cut off
        },
      },
    },
    layout: {
      padding: {
        top: 20, // Add top padding
        left: 20, // Add left padding
        right: 10, // Reduce right padding
      },
    },
  };

  return (
    <div className="bg-white shadow rounded p-4">
      <h2 className="text-xl font-bold mb-2">L5 PPG</h2>
      <Line data={chartData} options={options} />
    </div>
  );
};

export default PointsChart;

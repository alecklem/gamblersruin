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

const ReboundsAgainstOpponentChart = ({ data }) => {
  const chartData = {
    labels: data.dates,
    datasets: [
      {
        label: `Rebounds vs ${data.opponent}`,
        data: data.rebounds,
        fill: false,
        borderColor: "purple",
        backgroundColor: "purple",
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: `Rebounds Against ${data.opponent}`,
      },
    },
  };

  return <Line data={chartData} options={options} />;
};

export default ReboundsAgainstOpponentChart;

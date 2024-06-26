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

const StatsChart = ({ data, label, title, dataLabel }) => {
  console.log(data.betNumber);
  const betAmount = data.betNumber;
  const betArray = [];
  for (let i = 0; i < data.value.length; i++) {
    betArray.push(betAmount);
  }
  const chartData = {
    labels: data.dates.reverse(), // Reverse to make the dates from farthest to closest
    datasets: [
      {
        label: dataLabel,
        data: data.value.reverse(), // Reverse to match the order of dates
        fill: false,
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 3, // Adjust the thickness of the green line here
      },
      {
        label: "Bet Amount",
        data: betArray,
        fill: false,
        borderColor: "rgba(255, 0, 0, 1)",
        borderWidth: 2,
        pointRadius: 0,
        hoverBorderColor: "rgba(255, 0, 0, 1)",
        hoverBorderWidth: 2,
        hoverRadius: 0,
      },
    ],
  };

  const options = {
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        callbacks: {
          label: function (context) {
            if (context.dataset.label === "Bet Amount") {
              return `Bet Value: ${betAmount}`;
            }
            return context.raw;
          },
        },
        mode: "nearest", // Change the tooltip mode to 'nearest'
        intersect: false, // Ensures the tooltip shows even if not intersecting a point
      },
      datalabels: {
        display: true,
        color: "black",
        align: "top",
        borderRadius: 3,
        padding: 6,
        font: {
          size: 15, // Adjust font size here
          weight: "bold",
        },
        z: 10, // Ensures data labels are on top
        clip: false, // Prevents labels from being clipped at the chart edge
        formatter: function (value, context) {
          if (context.dataset.label === "Bet Amount") {
            return ""; // Do not display label for Bet Amount
          }
          return value;
        },
      },
    },
    scales: {
      y: {
        ticks: {
          padding: 10, // Add padding to prevent values from getting cut off
        },
        beginAtZero: false, // Ensures the chart starts from zero
      },
      x: {
        ticks: {
          padding: 10, // Add padding to prevent values from getting cut off
        },
      },
    },
    layout: {
      padding: {
        top: 20, // Adds padding to the top to prevent labels from getting cut off
      },
    },
    hover: {
      mode: "nearest",
      intersect: false,
    },
  };

  return (
    <div className="bg-white shadow rounded p-4">
      <h2 className="text-xl font-bold mb-2">{title}</h2>
      <Line data={chartData} options={options} />
    </div>
  );
};

export default StatsChart;

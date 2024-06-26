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

const getContrastingColor = (rgb) => {
  const [r, g, b] = rgb.match(/\d+/g).map(Number);
  const brightness = (r * 299 + g * 587 + b * 114) / 1000;
  return brightness > 125 ? "black" : "white";
};

// Function to convert RGB to RGBA with the given opacity
const rgbToRgba = (rgb, opacity) => {
  const [r, g, b] = rgb.match(/\d+/g).map(Number);
  return `rgba(${r}, ${g}, ${b}, ${opacity})`;
};

const StatsChart = ({ data, label, title, dataLabel }) => {
  const betAmount = data.betNumber;
  const betArray = [];
  for (let i = 0; i < data.value.length; i++) {
    betArray.push(betAmount);
  }

  const primaryColor = data.player_team_colors[0];
  const secondaryColor = data.player_team_colors[1];
  const contrastingTextColor = getContrastingColor(secondaryColor);

  // Determine max value for y-axis
  const maxValue = Math.max(...data.value);

  // Set the opacity level here (0 to 1)
  const opacityLevel = 0.85; // 80% opacity
  const backgroundColorWithOpacity = rgbToRgba(secondaryColor, opacityLevel);

  const chartData = {
    labels: data.dates, // Reverse to make the dates from farthest to closest
    datasets: [
      {
        label: dataLabel,
        data: data.value, // Reverse to match the order of dates
        fill: false,
        backgroundColor: primaryColor,
        borderColor: primaryColor,
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
          title: function () {
            return ""; // Remove the title (date) from the tooltip
          },
          label: function (context) {
            if (context.dataset.label === "Bet Amount") {
              return `Bet Value: ${betAmount}`;
            }
            return `Value: ${context.raw}`;
          },
        },
        mode: "nearest", // Change the tooltip mode to 'nearest'
        intersect: false, // Ensures the tooltip shows even if not intersecting a point
      },
      datalabels: {
        display: true,
        color: contrastingTextColor,
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
          color: contrastingTextColor,
        },
        beginAtZero: false,
        suggestedMax: maxValue + 1, // Adds extra space above the highest data point
      },
      x: {
        ticks: {
          padding: 10, // Add padding to prevent values from getting cut off
          color: contrastingTextColor,
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
    <div
      className="shadow rounded p-4"
      style={{
        backgroundColor: backgroundColorWithOpacity,
        color: contrastingTextColor,
      }} // Lower the opacity and set text color
    >
      <h2 className="text-xl font-bold mb-2">{title}</h2>
      <Line data={chartData} options={options} />
    </div>
  );
};

export default StatsChart;

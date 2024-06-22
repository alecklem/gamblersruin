import React from "react";
import { Line } from "react-chartjs-2";

const AssistsChart = ({ data }) => {
  const chartData = {
    labels: data.dates,
    datasets: [
      {
        label: "Assists",
        data: data.assists,
        fill: false,
        borderColor: "blue",
      },
    ],
  };

  return <Line data={chartData} />;
};

export default AssistsChart;

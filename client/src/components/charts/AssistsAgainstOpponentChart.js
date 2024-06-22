import React from "react";
import { Line } from "react-chartjs-2";

const AssistsAgainstOpponentChart = ({ data }) => {
  const chartData = {
    labels: data.dates,
    datasets: [
      {
        label: `Assists vs ${data.opponent}`,
        data: data.assists,
        fill: false,
        borderColor: "red",
      },
    ],
  };

  return <Line data={chartData} />;
};

export default AssistsAgainstOpponentChart;

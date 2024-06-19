import React, { useState } from "react";

const OpponentDefensiveRating = ({ metrics }) => {
  const [showAdvanced, setShowAdvanced] = useState(false);

  const teamMetricsLabels = [
    { label: "Defensive Rating", value: metrics[7] },
    { label: "Offensive Rating", value: metrics[8] },
    { label: "Net Rating", value: metrics[9] },
    { label: "Assist Ratio", value: metrics[10] },
    { label: "Offensive Rebound Percentage", value: metrics[11] },
    { label: "Defensive Rebound Percentage", value: metrics[12] },
    { label: "Rebound Percentage", value: metrics[13] },
    { label: "Turnover Percentage", value: metrics[14] },
    { label: "Usage Percentage", value: metrics[15] },
    { label: "Pace", value: metrics[16] },
  ];

  const advancedMetricsLabels = [
    { label: "Team ID", value: metrics[0] },
    { label: "Team Name", value: metrics[1] },
    { label: "Games Played", value: metrics[2] },
    { label: "Wins", value: metrics[3] },
    { label: "Losses", value: metrics[4] },
    { label: "Win Percentage", value: metrics[5] },
    { label: "Minutes", value: metrics[6] },
    { label: "Games Played Rank", value: metrics[17] },
    { label: "Wins Rank", value: metrics[18] },
    { label: "Losses Rank", value: metrics[19] },
    { label: "Win Percentage Rank", value: metrics[20] },
    { label: "Minutes Rank", value: metrics[21] },
    { label: "Offensive Rating Rank", value: metrics[22] },
    { label: "Defensive Rating Rank", value: metrics[23] },
    { label: "Net Rating Rank", value: metrics[24] },
    { label: "Assist Ratio Rank", value: metrics[25] },
    { label: "Offensive Rebound Percentage Rank", value: metrics[26] },
    { label: "Defensive Rebound Percentage Rank", value: metrics[27] },
    { label: "Rebound Percentage Rank", value: metrics[28] },
    { label: "Turnover Percentage Rank", value: metrics[29] },
    { label: "Usage Percentage Rank", value: metrics[30] },
    { label: "Pace Rank", value: metrics[31] },
  ];

  return (
    <div>
      <ul>
        {teamMetricsLabels.map((metric, index) => (
          <li key={index}>
            <strong>{metric.label}:</strong> {metric.value}
          </li>
        ))}
      </ul>
      <button
        onClick={() => setShowAdvanced(!showAdvanced)}
        className="bg-blue-500 text-white px-4 py-2 rounded mt-4"
      >
        {showAdvanced ? "Hide Advanced Stats" : "Show Advanced Stats"}
      </button>
      {showAdvanced && (
        <ul className="mt-4">
          {advancedMetricsLabels.map((metric, index) => (
            <li key={index}>
              <strong>{metric.label}:</strong> {metric.value}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default OpponentDefensiveRating;

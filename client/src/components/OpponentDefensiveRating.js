import React, { useState } from "react";

const OpponentDefensiveRating = ({ metrics }) => {
  const [showAdvanced, setShowAdvanced] = useState(false);

  const teamMetricsLabels = [
    { label: "Defensive Rating", value: metrics["E_DEF_RATING"] },
    { label: "Offensive Rating", value: metrics["E_OFF_RATING"] },
    { label: "Net Rating", value: metrics["E_NET_RATING"] },
    { label: "Assist Ratio", value: metrics["E_AST_RATIO"] },
    { label: "Offensive Rebound Percentage", value: metrics["E_OREB_PCT"] },
    { label: "Defensive Rebound Percentage", value: metrics["E_DREB_PCT"] },
    { label: "Rebound Percentage", value: metrics["E_REB_PCT"] },
    { label: "Turnover Percentage", value: metrics["E_TOV_PCT"] },
    { label: "Pace", value: metrics["E_PACE"] },
  ];

  const advancedMetricsLabels = [
    { label: "Team Name", value: metrics["TEAM_NAME"] },
    { label: "Games Played", value: metrics["GP"] },
    { label: "Wins", value: metrics["W"] },
    { label: "Losses", value: metrics["L"] },
    { label: "Win Percentage", value: metrics["W_PCT"] },
    { label: "Minutes", value: metrics["MIN"] },
    { label: "Games Played Rank", value: metrics["GP_RANK"] },
    { label: "Wins Rank", value: metrics["W_RANK"] },
    { label: "Losses Rank", value: metrics["L_RANK"] },
    { label: "Win Percentage Rank", value: metrics["W_PCT_RANK"] },
    { label: "Minutes Rank", value: metrics["MIN_RANK"] },
    { label: "Offensive Rating Rank", value: metrics["E_OFF_RATING_RANK"] },
    { label: "Defensive Rating Rank", value: metrics["E_DEF_RATING_RANK"] },
    { label: "Net Rating Rank", value: metrics["E_NET_RATING_RANK"] },
    { label: "Assist Ratio Rank", value: metrics["E_AST_RATIO_RANK"] },
    {
      label: "Offensive Rebound Percentage Rank",
      value: metrics["E_OREB_PCT_RANK"],
    },
    {
      label: "Defensive Rebound Percentage Rank",
      value: metrics["E_DREB_PCT_RANK"],
    },
    { label: "Rebound Percentage Rank", value: metrics["E_REB_PCT_RANK"] },
    { label: "Turnover Percentage Rank", value: metrics["E_TOV_PCT_RANK"] },
    { label: "Pace Rank", value: metrics["E_PACE_RANK"] },
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

import React, { useState } from "react";

const PlayerEstimatedMetrics = ({ metrics }) => {
  const playerMetricsLabels = [
    { label: "Minutes", value: metrics["MIN"], rank: metrics["MIN_RANK"] },
    {
      label: "Offensive Rating",
      value: metrics["E_OFF_RATING"],
      rank: metrics["E_OFF_RATING_RANK"],
    },
    {
      label: "Defensive Rating",
      value: metrics["E_DEF_RATING"],
      rank: metrics["E_DEF_RATING_RANK"],
    },
    {
      label: "Net Rating",
      value: metrics["E_NET_RATING"],
      rank: metrics["E_NET_RATING_RANK"],
    },
    {
      label: "Assist Ratio",
      value: metrics["E_AST_RATIO"],
      rank: metrics["E_AST_RATIO_RANK"],
    },
    {
      label: "Offensive Rebound Percentage",
      value: metrics["E_OREB_PCT"],
      rank: metrics["E_OREB_PCT_RANK"],
    },
    {
      label: "Defensive Rebound Percentage",
      value: metrics["E_DREB_PCT"],
      rank: metrics["E_DREB_PCT_RANK"],
    },
    {
      label: "Rebound Percentage",
      value: metrics["E_REB_PCT"],
      rank: metrics["E_REB_PCT_RANK"],
    },
    {
      label: "Turnover Percentage",
      value: metrics["E_TOV_PCT"],
      rank: metrics["E_TOV_PCT_RANK"],
    },
    {
      label: "Usage Percentage",
      value: metrics["E_USG_PCT"],
      rank: metrics["E_USG_PCT_RANK"],
    },
    { label: "Pace", value: metrics["E_PACE"], rank: metrics["E_PACE_RANK"] },
    { label: "Games Played", value: metrics["GP"], rank: metrics["GP_RANK"] },
    { label: "Wins", value: metrics["W"], rank: metrics["W_RANK"] },
    { label: "Losses", value: metrics["L"], rank: metrics["L_RANK"] },
    {
      label: "Win Percentage",
      value: metrics["W_PCT"],
      rank: metrics["W_PCT_RANK"],
    },
  ];

  return (
    <div>
      <ul>
        {playerMetricsLabels.map((metric, index) => (
          <li key={index}>
            <strong>{metric.label}:</strong> {metric.value}{" "}
            {metric.rank && `[#${metric.rank}]`}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PlayerEstimatedMetrics;

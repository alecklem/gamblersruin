import React from "react";
import PointsChart from "../Charts/PointsChart";

const PointsDashboard = ({ data }) => {
  return (
    <div className="p-4">
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <div className="bg-white shadow rounded p-4">
          <h2 className="text-xl font-bold mb-2">Team Abbreviation</h2>
          <p>{data.team_abbreviation}</p>
        </div>
        <div className="bg-white shadow rounded p-4">
          <h2 className="text-xl font-bold mb-2">Points Per Game</h2>
          <p>{data.points_per_game}</p>
        </div>
        <PointsChart
          data={{
            dates: ["Game 1", "Game 2", "Game 3", "Game 4", "Game 5"],
            points: data.player_points_in_last_5_games,
          }}
        />
        {/* Add more modular boxes for other stats as needed */}
      </div>
    </div>
  );
};

export default PointsDashboard;

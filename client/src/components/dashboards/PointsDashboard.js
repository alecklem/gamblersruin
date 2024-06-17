import React from "react";
import PointsChart from "../charts/PointsChart";
import PointsAgainstOpponentChart from "../charts/PointsAgainstOpponentChart";

const PointsDashboard = ({ data }) => {
  return (
    <div className="p-4 w-full flex flex-col items-center">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full max-w-2xl">
        <div className="bg-white shadow rounded p-4 flex items-center justify-center h-24">
          <h2 className="text-xl font-bold text-center">{data.matchup}</h2>
        </div>
        <div className="bg-white shadow rounded p-4 h-24">
          <h2 className="text-xl font-bold mb-2 text-center">
            Points Per Game
          </h2>
          <p className="text-center">{data.points_per_game}</p>
        </div>
      </div>
      <div className="w-full mt-4 max-w-lg">
        <PointsChart
          data={{
            dates: data.last_5_game_dates,
            points: data.player_points_in_last_5_games,
          }}
        />
      </div>
      {data.player_points_against_opponent.length > 0 && (
        <div className="w-full mt-4 max-w-lg">
          <PointsAgainstOpponentChart
            data={{
              points: data.player_points_against_opponent,
              dates: data.opponent_game_dates,
              opponent: data.opponent_team_abbreviation,
            }}
          />
        </div>
      )}
    </div>
  );
};

export default PointsDashboard;

import React from "react";
import PointsChart from "../charts/PointsChart";
import PointsAgainstOpponentChart from "../charts/PointsAgainstOpponentChart";
import PlayerEstimatedMetrics from "../PlayerEstimatedMetrics";
import OpponentDefensiveRating from "../OpponentDefensiveRating";
import RestDays from "../RestDays";

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
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full mt-4">
        <div className="bg-white shadow rounded p-4 h-24">
          <h2 className="text-xl font-bold mb-2 text-center">
            Home vs. Away PPG
          </h2>
          <p className="text-center">
            {data.home_points_per_game.toFixed(2)} vs.{" "}
            {data.away_points_per_game.toFixed(2)}
          </p>
        </div>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full mt-4">
        <div className="w-full max-w-md">
          <PointsChart
            data={{
              dates: data.last_5_game_dates,
              points: data.player_points_in_last_5_games,
            }}
          />
        </div>
        {data.player_points_against_opponent.length > 0 && (
          <div className="w-full max-w-md">
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
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full mt-4">
        <div className="bg-white shadow rounded p-4 h-24">
          <h2 className="text-xl font-bold mb-2 text-center">
            Rest Days Between Last 5 Games
          </h2>
          <RestDays
            gameDates={data.last_5_game_dates}
            restDays={data.rest_days}
          />
        </div>
        <div className="bg-white shadow rounded p-4 h-auto">
          <h2 className="text-xl font-bold mb-2 text-center">
            Player Estimated Metrics
          </h2>
          <PlayerEstimatedMetrics metrics={data.player_metrics} />
        </div>
        <div className="bg-white shadow rounded p-4 h-auto">
          <h2 className="text-xl font-bold mb-2 text-center">
            Opponent Defensive Rating
          </h2>
          <OpponentDefensiveRating metrics={data.team_metrics} />
        </div>
      </div>
    </div>
  );
};

export default PointsDashboard;

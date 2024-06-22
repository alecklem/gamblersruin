import React from "react";
import AssistsChart from "../charts/AssistsChart";
import AssistsAgainstOpponentChart from "../charts/AssistsAgainstOpponentChart";
import PlayerEstimatedMetrics from "../PlayerEstimatedMetrics";
import OpponentDefensiveRating from "../OpponentDefensiveRating";
import RestDays from "../RestDays";

const AssistsDashboard = ({ data }) => {
  return (
    <div className="p-4 w-full flex flex-col items-center">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full max-w-2xl">
        <div className="bg-white shadow rounded p-4 flex items-center justify-center h-24">
          <h2 className="text-xl font-bold text-center">{data.matchup}</h2>
        </div>
        <div className="bg-white shadow rounded p-4 h-24">
          <h2 className="text-xl font-bold mb-2 text-center">
            Assists Per Game
          </h2>
          <p className="text-center">{data.assists_per_game}</p>
        </div>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full mt-4">
        <div className="bg-white shadow rounded p-4 h-24">
          <h2 className="text-xl font-bold mb-2 text-center">
            Home vs. Away APG
          </h2>
          <p className="text-center">
            {data.home_assists_per_game.toFixed(2)} vs.{" "}
            {data.away_assists_per_game.toFixed(2)}
          </p>
        </div>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full mt-4">
        <div className="w-full max-w-md">
          <AssistsChart
            data={{
              dates: data.last_5_game_dates,
              assists: data.player_assists_in_last_5_games,
            }}
          />
        </div>
        {data.player_assists_against_opponent.length > 0 && (
          <div className="w-full max-w-md">
            <AssistsAgainstOpponentChart
              data={{
                assists: data.player_assists_against_opponent,
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

export default AssistsDashboard;

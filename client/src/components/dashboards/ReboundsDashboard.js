import React from "react";
import ReboundsChart from "../charts/ReboundsChart";
import ReboundsAgainstOpponentChart from "../charts/ReboundsAgainstOpponentChart";
import PlayerEstimatedMetrics from "../PlayerEstimatedMetrics";
import OpponentDefensiveRating from "../OpponentDefensiveRating";
import RestDays from "../RestDays";

const ReboundsDashboard = ({ data }) => {
  if (!data) {
    return <div>Loading...</div>;
  }

  const {
    matchup,
    rebounds_per_game,
    home_rebounds_per_game,
    away_rebounds_per_game,
    last_5_game_dates,
    player_rebounds_in_last_5_games,
    player_rebounds_against_opponent,
    opponent_game_dates,
    opponent_team_abbreviation,
    rest_days,
    player_metrics,
    team_metrics,
  } = data;

  return (
    <div className="p-4 w-full flex flex-col items-center">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full max-w-2xl">
        <div className="bg-white shadow rounded p-4 flex items-center justify-center h-24">
          <h2 className="text-xl font-bold text-center">{matchup || "N/A"}</h2>
        </div>
        <div className="bg-white shadow rounded p-4 h-24">
          <h2 className="text-xl font-bold mb-2 text-center">
            Rebounds Per Game
          </h2>
          <p className="text-center">
            {rebounds_per_game?.toFixed(2) || "N/A"}
          </p>
        </div>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full mt-4">
        <div className="bg-white shadow rounded p-4 h-24">
          <h2 className="text-xl font-bold mb-2 text-center">
            Home vs. Away RPG
          </h2>
          <p className="text-center">
            {home_rebounds_per_game?.toFixed(2) || "N/A"} vs.{" "}
            {away_rebounds_per_game?.toFixed(2) || "N/A"}
          </p>
        </div>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full mt-4">
        <div className="w-full max-w-md">
          <ReboundsChart
            data={{
              dates: last_5_game_dates || [],
              rebounds: player_rebounds_in_last_5_games || [],
            }}
          />
        </div>
        {player_rebounds_against_opponent?.length > 0 && (
          <div className="w-full max-w-md">
            <ReboundsAgainstOpponentChart
              data={{
                rebounds: player_rebounds_against_opponent,
                dates: opponent_game_dates || [],
                opponent: opponent_team_abbreviation || "N/A",
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
            gameDates={last_5_game_dates || []}
            restDays={rest_days || []}
          />
        </div>
        <div className="bg-white shadow rounded p-4 h-auto">
          <h2 className="text-xl font-bold mb-2 text-center">
            Player Estimated Metrics
          </h2>
          <PlayerEstimatedMetrics metrics={player_metrics || {}} />
        </div>
        <div className="bg-white shadow rounded p-4 h-auto">
          <h2 className="text-xl font-bold mb-2 text-center">
            Opponent Defensive Rating
          </h2>
          <OpponentDefensiveRating metrics={team_metrics || {}} />
        </div>
      </div>
    </div>
  );
};

export default ReboundsDashboard;

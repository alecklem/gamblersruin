import React from "react";
import PlayerEstimatedMetrics from "../PlayerEstimatedMetrics";
import OpponentDefensiveRating from "../OpponentDefensiveRating";
import RestDays from "../RestDays";
import StatsChart from "../charts/StatsChart";

const ReboundsDashboard = ({ data }) => {
  const playerColors = data.player_team_colors;
  const opponentColors = data.opponent_team_colors;

  const getTeamColorStyle = (colors) => {
    return {
      color: colors[0],
    };
  };

  return (
    <div>
      <div className="pt-10 px-10">
        <div className="w-full grid grid-flow-column-dense grid-cols-5 grid-rows-9 gap-6">
          <div className="bg-white shadow rounded flex items-center justify-center h-24">
            <h2 className="text-xl font-bold text-center">
              <span style={getTeamColorStyle(playerColors)}>
                {data.team_abbreviation}
              </span>{" "}
              vs.{" "}
              <span style={getTeamColorStyle(opponentColors)}>
                {data.opponent_team_abbreviation}
              </span>
            </h2>
          </div>
          <div className="bg-white shadow rounded p-4 h-24">
            <h2 className="text-xl font-bold mb-2 text-center">
              Rebounds Per Game
            </h2>
            <p className="text-center">{data.rebounds_per_game}</p>
          </div>
          <div className="bg-white shadow rounded p-4 h-24">
            <h2 className="text-xl font-bold mb-2 text-center">
              Home vs. Away PPG
            </h2>
            <p className="text-center">
              {data.home_rebounds_per_game.toFixed(2)} vs.{" "}
              {data.away_rebounds_per_game.toFixed(2)}
            </p>
          </div>
          <div className="col-span-2 ">
            <div className="bg-white shadow rounded p-4 h-24">
              <h2 className="text-xl font-bold mb-2 text-center">
                Rest Days Between Last 5 Games
              </h2>
              <RestDays
                gameDates={data.last_5_game_dates}
                restDays={data.rest_days}
              />
            </div>
          </div>
          <div className="col-span-2 row-span-3">
            <StatsChart
              data={{
                dates: data.opponent_game_dates,
                value: data.player_rebounds_against_opponent,
                betNumber: data.betNumber,
                player_team_colors: data.player_team_colors,
                opponent_team_colors: data.opponent_team_colors,
              }}
              label="Rebounds"
              title={`Rebounds against ${data.opponent_team_abbreviation}`}
              dataLabel="Rebounds"
            />
          </div>
          <div className="col-span-2 row-span-3">
            <StatsChart
              data={{
                dates: data.last_5_game_dates,
                value: data.player_rebounds_in_last_5_games,
                betNumber: data.betNumber,
                player_team_colors: data.player_team_colors,
                opponent_team_colors: data.opponent_team_colors,
              }}
              label="Rebounds"
              title="L5 RPG"
              dataLabel="Rebounds"
            />
          </div>
          <div className="col-span-2 row-span-4">
            <div className="bg-white shadow rounded p-4 h-auto">
              <h2 className="text-xl font-bold mb-2 text-center">
                Player Estimated Metrics
              </h2>
              <PlayerEstimatedMetrics metrics={data.player_metrics} />
            </div>
          </div>
          <div className="col-span-2 row-span-4">
            <div className="bg-white shadow rounded p-4 h-auto">
              <h2 className="text-xl font-bold mb-2 text-center">
                Opponent Defensive Rating
              </h2>
              <OpponentDefensiveRating metrics={data.team_metrics} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReboundsDashboard;

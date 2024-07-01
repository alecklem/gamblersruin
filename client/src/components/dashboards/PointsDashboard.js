import React from "react";
import OpponentDefensiveRating from "../OpponentDefensiveRating";
import PlayerEstimatedMetrics from "../PlayerEstimatedMetrics";
import RestDays from "../RestDays";
import StatsChart from "../charts/StatsChart";

const PointsDashboard = ({ data }) => {
  const playerColors = data.player_team_colors;
  const opponentColors = data.opponent_team_colors;

  const getTeamColorStyle = (colors) => {
    return {
      color: colors[0],
    };
  };

  // Function to sort the dates and corresponding points in order of furthest to most recent
  const sortDatesAndPoints = (dates, points) => {
    const seasonStartYear = new Date().getFullYear() - 1; // Assuming the season starts in the previous year

    const datePointsArray = dates.map((date, index) => ({
      date,
      points: points[index],
    }));

    datePointsArray.sort((a, b) => {
      const [aMonth, aDay] = a.date.split("/").map(Number);
      const [bMonth, bDay] = b.date.split("/").map(Number);

      const aDate = new Date(
        aMonth >= 8 ? seasonStartYear : seasonStartYear + 1,
        aMonth - 1,
        aDay
      );
      const bDate = new Date(
        bMonth >= 8 ? seasonStartYear : seasonStartYear + 1,
        bMonth - 1,
        bDay
      );

      return bDate - aDate;
    });

    return {
      sortedDates: datePointsArray.map((item) => item.date).reverse(),
      sortedPoints: datePointsArray.map((item) => item.points).reverse(),
    };
  };

  const {
    sortedDates: sortedOpponentGameDates,
    sortedPoints: sortedOpponentPoints,
  } = sortDatesAndPoints(
    data.opponent_game_dates,
    data.player_points_against_opponent
  );

  return (
    <div className="md:pt-10 md:px-10 pl-1.5 pt-5">
      <div className="w-full grid grid-flow-column-dense lg:grid-cols-5 lg:grid-rows-9 sm:grid-cols-2 sm:grid-rows-20 md:grid-cols-5 md:grid-rows-9 gap-6">
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
            Points Per Game
          </h2>
          <p className="text-center">{data.points_per_game}</p>
        </div>
        <div className="bg-white shadow rounded p-4 h-24">
          <h2 className="text-xl font-bold mb-2 text-center">
            Home vs. Away PPG
          </h2>
          <p className="text-center">
            {data.home_points_per_game.toFixed(2)} vs.{" "}
            {data.away_points_per_game.toFixed(2)}
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
              dates: sortedOpponentGameDates,
              value: sortedOpponentPoints,
              betNumber: data.betNumber,
              player_team_colors: data.player_team_colors,
              opponent_team_colors: data.opponent_team_colors,
            }}
            label="Points"
            title={`Points against ${data.opponent_team_abbreviation}`}
            dataLabel="Points"
          />
        </div>
        <div className="col-span-2 row-span-3">
          <StatsChart
            data={{
              dates: data.last_5_game_dates,
              value: data.player_points_in_last_5_games,
              betNumber: data.betNumber,
              player_team_colors: data.player_team_colors,
              opponent_team_colors: data.opponent_team_colors,
            }}
            label="Points"
            title="L5 PPG"
            dataLabel="Points"
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
  );
};

export default PointsDashboard;

import React, { useEffect, useState } from "react";
import axios from "axios";
import PointsDashboard from "./components/dashboards/PointsDashboard";
// Import other dashboards as needed

const PlayerList = () => {
  const [players, setPlayers] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [filteredPlayers, setFilteredPlayers] = useState([]);
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [selectedStat, setSelectedStat] = useState("POINTS");
  const [playerData, setPlayerData] = useState(null);
  const [isDropdownVisible, setIsDropdownVisible] = useState(false);

  const statsOptions = [
    "POINTS",
    "REBOUNDS",
    "ASSISTS",
    "3PT",
    "3PTA",
    "FG",
    "FGA",
    "STEALS",
    "BLOCKS",
    "STOCKS",
    "PRA",
    "PTS + REBOUNDS",
    "POINTS + ASSISTS",
    "TURNOVERS",
  ];

  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/loadplayers");
        setPlayers(response.data);
      } catch (error) {
        console.error("Error fetching player data:", error);
      }
    };

    fetchPlayers();
  }, []);

  useEffect(() => {
    const filtered = players.filter((player) =>
      player.full_name.toLowerCase().includes(searchQuery.toLowerCase())
    );
    setFilteredPlayers(filtered);
  }, [searchQuery, players]);

  const routeMappings = {
    POINTS: "points",
    REBOUNDS: "rebounds",
    ASSISTS: "assists",
    "3PT": "three_pointers",
    "3PTA": "three_point_attempts",
    FG: "field_goals",
    FGA: "field_goals_attempted",
    STEALS: "steals",
    BLOCKS: "blocks",
    STOCKS: "stocks",
    PRA: "pra",
    "PTS + REBOUNDS": "points_plus_rebounds",
    "POINTS + ASSISTS": "points_plus_assists",
    TURNOVERS: "turnovers",
  };

  const handleSave = async () => {
    if (selectedPlayer) {
      try {
        const route = `http://127.0.0.1:5000/${routeMappings[selectedStat]}`;
        const response = await axios.post(route, {
          player: selectedPlayer,
          category: selectedStat,
        });
        setPlayerData(response.data);
      } catch (error) {
        console.error("Error saving data:", error);
      }
    }
  };

  const handlePlayerClick = (player) => {
    setSelectedPlayer((prevSelected) => {
      if (prevSelected && prevSelected.id === player.id) {
        return null;
      } else {
        return player;
      }
    });
    setSearchQuery("");
  };

  const handleStatSelect = (stat) => {
    setSelectedStat(stat);
    setIsDropdownVisible(false);
  };

  const renderDashboard = () => {
    switch (selectedStat) {
      case "POINTS":
        return <PointsDashboard data={playerData} />;
      // Add cases for other stats and corresponding dashboards
      default:
        return null;
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Current NBA Players</h1>
      <div className="flex mb-4">
        <div className="w-1/3">
          {!selectedPlayer && (
            <input
              type="text"
              className="border rounded p-2 w-full"
              placeholder="Search for a player"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          )}
          <div className="relative inline-block text-left">
            <button
              className="inline-flex justify-center w-full rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-sm font-medium text-gray-700"
              onClick={() => setIsDropdownVisible(!isDropdownVisible)}
            >
              {selectedStat}
            </button>
            {isDropdownVisible && (
              <div className="origin-top-right absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5">
                <div
                  className="py-1"
                  role="menu"
                  aria-orientation="vertical"
                  aria-labelledby="options-menu"
                >
                  {statsOptions.map((stat) => (
                    <a
                      key={stat}
                      href="#"
                      onClick={() => handleStatSelect(stat)}
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
                      role="menuitem"
                    >
                      {stat}
                    </a>
                  ))}
                </div>
              </div>
            )}
          </div>
          <button
            onClick={handleSave}
            className="bg-blue-500 text-white px-4 py-2 rounded mt-2"
          >
            Save Selected Player
          </button>
        </div>
        <ul className="w-2/3">
          {selectedPlayer ? (
            <li
              key={selectedPlayer.id}
              onClick={() => handlePlayerClick(selectedPlayer)}
              className="cursor-pointer p-2 border-b"
            >
              <img
                width={60}
                src={`https://cdn.nba.com/headshots/nba/latest/1040x760/${selectedPlayer.id}.png`}
                alt={`${selectedPlayer.full_name}'s headshot`}
                className="inline-block mr-2"
              />
              {selectedPlayer.full_name}
            </li>
          ) : (
            filteredPlayers.map((player) => (
              <li
                key={player.id}
                onClick={() => handlePlayerClick(player)}
                className={`cursor-pointer p-2 border-b ${
                  selectedPlayer && selectedPlayer.id === player.id
                    ? "bg-gray-200"
                    : ""
                }`}
              >
                <img
                  width={60}
                  src={`https://cdn.nba.com/headshots/nba/latest/1040x760/${player.id}.png`}
                  alt={`${player.full_name}'s headshot`}
                  className="inline-block mr-2"
                />
                {player.full_name}
              </li>
            ))
          )}
        </ul>
      </div>
      {playerData && renderDashboard()}
    </div>
  );
};

export default PlayerList;

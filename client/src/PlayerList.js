import React, { useEffect, useState } from "react";
import axios from "axios";
import PointsDashboard from "./components/dashboards/PointsDashboard";
import StatDropdown from "./components/StatDropdown"; // Import the StatDropdown component
import "./styles/PlayerList.css"; // Import the CSS file

const PlayerList = () => {
  const [players, setPlayers] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [filteredPlayers, setFilteredPlayers] = useState([]);
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [selectedStat, setSelectedStat] = useState("POINTS");
  const [playerData, setPlayerData] = useState(null);
  const [isPlayerDropdownVisible, setIsPlayerDropdownVisible] = useState(false);

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
    setIsPlayerDropdownVisible(filtered.length > 0 && searchQuery.length > 0);
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
    setSelectedPlayer(player);
    setSearchQuery(player.full_name);
    setIsPlayerDropdownVisible(false);
  };

  const handleSearchQueryChange = (event) => {
    const query = event.target.value;
    setSearchQuery(query);
    setSelectedPlayer(null);
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
    <div className="player-list-container p-4">
      <h1 className="text-2xl font-bold mb-4">Enter Player and Prop Bet</h1>
      <div className="search-container flex flex-col items-center mb-4 w-full max-w-2xl">
        <div className="w-full flex items-center space-x-2">
          {selectedPlayer && (
            <img
              width={40}
              src={`https://cdn.nba.com/headshots/nba/latest/1040x760/${selectedPlayer.id}.png`}
              alt={`${selectedPlayer.full_name}'s headshot`}
              className="inline-block mr-2"
            />
          )}
          <div className="relative flex-grow">
            <input
              type="text"
              className="border rounded p-2 w-full h-12"
              placeholder="Search for a player"
              value={searchQuery}
              onChange={handleSearchQueryChange}
            />
            {isPlayerDropdownVisible && selectedPlayer == null && (
              <ul className="player-dropdown absolute w-full border border-gray-300 rounded mt-1 max-h-60 overflow-y-auto bg-white z-10">
                {filteredPlayers.map((player) => (
                  <li
                    key={player.id}
                    onClick={() => handlePlayerClick(player)}
                    className="cursor-pointer p-2 border-b hover:bg-gray-200 flex items-center"
                  >
                    <img
                      width={40}
                      src={`https://cdn.nba.com/headshots/nba/latest/1040x760/${player.id}.png`}
                      alt={`${player.full_name}'s headshot`}
                      className="inline-block mr-2"
                    />
                    {player.full_name}
                  </li>
                ))}
              </ul>
            )}
          </div>
          <div className="relative inline-block text-left h-12">
            <StatDropdown
              selectedStat={selectedStat}
              setSelectedStat={setSelectedStat}
            />
          </div>
          <button
            onClick={handleSave}
            className="bg-blue-500 text-white px-4 rounded h-12"
          >
            Save
          </button>
        </div>
      </div>
      {playerData && renderDashboard()}
    </div>
  );
};

export default PlayerList;

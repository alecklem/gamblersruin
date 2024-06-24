import React, { useEffect, useState } from "react";
import axios from "axios";
import PointsDashboard from "./components/dashboards/PointsDashboard";
import StatDropdown from "./components/StatDropdown";
import "./styles/PlayerList.css";
import AssistsDashboard from "./components/dashboards/AssistsDashboard";
import ReboundsDashboard from "./components/dashboards/ReboundsDashboard";

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
        const response = await axios.get(
          "http://gamblersruin-production.up.railway.app/loadplayers"
        );
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

  // Clear playerData when selectedStat changes
  useEffect(() => {
    setPlayerData(null);
  }, [selectedStat]);

  const routeMappings = {
    POINTS: "points",
    ASSISTS: "assists",
    REBOUNDS: "rebounds",
    // Add other mappings as needed
  };

  const handleSave = async () => {
    if (selectedPlayer) {
      try {
        const route = `http://gamblersruin-production.up.railway.app/${routeMappings[selectedStat]}`;
        const response = await axios.post(route, {
          player: { id: selectedPlayer.person_id },
        });
        setPlayerData({ ...response.data, playerId: selectedPlayer.person_id });
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
    if (!playerData) return null;

    switch (selectedStat) {
      case "POINTS":
        return <PointsDashboard data={playerData} />;
      case "ASSISTS":
        return <AssistsDashboard data={playerData} />;
      case "REBOUNDS":
        return <ReboundsDashboard data={playerData} />;
      default:
        return null;
    }
  };

  return (
    <div className="player-list-container">
      <h1 className="text-2xl font-bold mb-4 text-center">
        Enter Player and Prop Bet
      </h1>
      <div className="search-container flex flex-col items-center mb-4 w-full max-w-2xl">
        <div className="w-full flex items-center space-x-2 justify-center">
          <div className="relative pt-2.5">
            {selectedPlayer && (
              <img
                width={40}
                src={`https://cdn.nba.com/headshots/nba/latest/1040x760/${selectedPlayer.person_id}.png`}
                alt={`${selectedPlayer.full_name}'s headshot`}
                className="absolute left-0 top-1/2 transform -translate-y-1/2"
              />
            )}
            <input
              type="text"
              className="border rounded pl-12 w-96 h-12"
              placeholder="Search for a player"
              value={searchQuery}
              onChange={handleSearchQueryChange}
            />
            {isPlayerDropdownVisible && selectedPlayer == null && (
              <ul className="player-dropdown absolute w-96 border border-gray-300 rounded mt-1 max-h-60 overflow-y-auto bg-white z-10">
                {filteredPlayers.map((player) => (
                  <li
                    key={player.id}
                    onClick={() => handlePlayerClick(player)}
                    className="cursor-pointer p-2 border-b hover:bg-gray-200 flex items-center"
                  >
                    <img
                      width={40}
                      src={`https://cdn.nba.com/headshots/nba/latest/1040x760/${player.person_id}.png`}
                      alt={`${player.full_name}'s headshot`}
                      className="inline-block mr-2"
                    />
                    {player.full_name}
                  </li>
                ))}
              </ul>
            )}
          </div>
          <div className="relative inline-block text-left h-12 w-48">
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
      {renderDashboard()}
    </div>
  );
};

export default PlayerList;

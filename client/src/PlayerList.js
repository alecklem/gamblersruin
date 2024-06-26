import axios from "axios";
import React, { useEffect, useState } from "react";
import StatDropdown from "./components/StatDropdown";
import AssistsDashboard from "./components/dashboards/AssistsDashboard";
import PointsDashboard from "./components/dashboards/PointsDashboard";
import ReboundsDashboard from "./components/dashboards/ReboundsDashboard";
import "./styles/PlayerList.css";

const PlayerList = () => {
  const [players, setPlayers] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [filteredPlayers, setFilteredPlayers] = useState([]);
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [selectedStat, setSelectedStat] = useState("POINTS");
  const [localSelectedStat, setLocalSelectedStat] = useState("POINTS");
  const [playerData, setPlayerData] = useState(null);
  const [isPlayerDropdownVisible, setIsPlayerDropdownVisible] = useState(false);
  const [betQuantity, setBetQuantity] = useState(15.5);

  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        const response = await axios.get(`${BACKEND_URL}/loadplayers`);
        setPlayers(response.data);
      } catch (error) {
        console.error("Error fetching player data:", error);
      }
    };

    fetchPlayers();
  }, [BACKEND_URL]);

  useEffect(() => {
    const filtered = players.filter((player) =>
      player.full_name.toLowerCase().includes(searchQuery.toLowerCase())
    );
    setFilteredPlayers(filtered);
    setIsPlayerDropdownVisible(filtered.length > 0 && searchQuery.length > 0);
  }, [searchQuery, players]);

  const routeMappings = {
    POINTS: "points",
    ASSISTS: "assists",
    REBOUNDS: "rebounds",
    // Add other mappings as needed
  };

  const handleSave = async () => {
    if (selectedPlayer) {
      try {
        const route = `${BACKEND_URL}/${routeMappings[localSelectedStat]}`;
        const response = await axios.post(route, {
          player: { id: selectedPlayer.person_id },
        });
        setPlayerData({
          ...response.data,
          playerId: selectedPlayer.person_id,
          betNumber: betQuantity,
        });
        setSelectedStat(localSelectedStat);
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

  const handleBetQuantityChange = (event) => {
    const betAmount = event.target.value;
    setBetQuantity(betAmount);
  };

  const renderDashboard = () => {
    if (!playerData) return null;

    switch (selectedStat) {
      case "POINTS":
        return <PointsDashboard data={playerData} betQuantity={betQuantity} />;
      case "ASSISTS":
        return <AssistsDashboard data={playerData} betQuantity={betQuantity} />;
      case "REBOUNDS":
        return (
          <ReboundsDashboard data={playerData} betQuantity={betQuantity} />
        );
      default:
        return null;
    }
  };

  return (
    <div className="player-list-container">
      <h1 className="text-2xl font-bold mb-4 text-center">
        Enter Player and Prop Bet
      </h1>
      <div className="">
        <div className="flex gap-2">
          <div className="relative">
            {selectedPlayer && (
              <img
                width={40}
                src={`https://cdn.nba.com/headshots/nba/latest/1040x760/${selectedPlayer.person_id}.png`}
                alt={`${selectedPlayer.full_name}'s headshot`}
                className="absolute right-2 top-1/2 transform -translate-y-1/2"
              />
            )}
            <input
              type="text"
              className="border rounded pl-3 w-60 h-12"
              placeholder="Search for a player"
              value={searchQuery}
              onChange={handleSearchQueryChange}
            />
            {isPlayerDropdownVisible && selectedPlayer == null && (
              <ul className="player-dropdown absolute w-60 border border-gray-300 rounded mt-1 max-h-60 overflow-y-auto bg-white z-10">
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
          <div className="relative inline-block text-left w-30">
            <StatDropdown
              selectedStat={localSelectedStat}
              setSelectedStat={setLocalSelectedStat}
            />
          </div>
          <input
            type="text"
            placeholder={betQuantity}
            className="border rounded pl-3 w-16 h-12"
            value={betQuantity}
            onChange={handleBetQuantityChange}
          ></input>
          <button
            onClick={handleSave}
            className="bg-blue-500 text-white px-2 rounded" // Adjust padding here
          >
            Save
          </button>
        </div>
      </div>
      <div className="w-full">{renderDashboard()}</div>
    </div>
  );
};

export default PlayerList;

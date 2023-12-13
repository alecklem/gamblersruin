import React, { useEffect, useState } from "react";
import axios from "axios";

const PlayerList = () => {
  const [players, setPlayers] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [filteredPlayers, setFilteredPlayers] = useState([]);
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [selectedStat, setSelectedStat] = useState("POINTS");

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
    // Filter players based on the search query and selected stat
    const filtered = players.filter((player) =>
      player.full_name.toLowerCase().includes(searchQuery.toLowerCase())
    );

    setFilteredPlayers(filtered);
  }, [searchQuery, players, selectedStat]);

  const routeMappings = {
    "POINTS": "points",
    "REBOUNDS": "rebounds",
    "ASSISTS": "assists",
    "3PT": "three_pointers",
    "3PTA": "three_point_attempts",
    "FG": "field_goals",
    "FGA": "field_goals_attempted",
    "STEALS": "steals",
    "BLOCKS": "blocks",
    "STOCKS": "stocks",
    "PRA": "pra",
    "PTS + REBOUNDS": "points_plus_rebounds",
    "POINTS + ASSISTS": "points_plus_assists",
    "TURNOVERS": "turnovers",
  };
  
  const handleSave = async () => {
    if (selectedPlayer) {
      try {
        const route = `http://127.0.0.1:5000/${routeMappings[selectedStat]}`;
        const response = await axios.post(route, {
          player: selectedPlayer,
          category: selectedStat,
        });
  
        // Handle the response if needed
        console.log(response.data);
      } catch (error) {
        console.error("Error saving data:", error);
      }
    }
  };

  const handlePlayerClick = (player) => {
    // Toggle the selected player
    setSelectedPlayer((prevSelected) => {
      if (prevSelected && prevSelected.id === player.id) {
        // Unselect the player if already selected
        return null;
      } else {
        // Select the clicked player
        return player;
      }
    });

    // Reset the search query when unselecting a player
    setSearchQuery("");
  };

  const [isDropdownVisible, setIsDropdownVisible] = useState(false);

  const handleStatSelect = (stat) => {
    setSelectedStat(stat);
    setIsDropdownVisible(false); // Hide the dropdown after selecting a stat
  };

  return (
    <div>
      <h1>Current NBA Players</h1>
      <div className="search-container">
        <div>
          {!selectedPlayer && (
            <input
              type="text"
              placeholder="Search for a player"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          )}

          {/* Button for stat selection */}
          <div className="stat-dropdown">
            <button className="stat-button" onClick={() => setIsDropdownVisible(!isDropdownVisible)}>
              {selectedStat} {/* Display the selected stat in the button */}
            </button>
            {isDropdownVisible && (
              <ul className="stat-options">
                {statsOptions.map((stat) => (
                  <li key={stat} onClick={() => handleStatSelect(stat)}>
                    {stat}
                  </li>
                ))}
              </ul>
            )}
          </div>
          <button onClick={handleSave}>Save Selected Player</button>
        </div>

        <ul className="dropdown">
          {selectedPlayer ? (
            <li 
            key={selectedPlayer.id}
            onClick={() => handlePlayerClick(selectedPlayer)}
            >
              <img
                width={60}
                src={`https://cdn.nba.com/headshots/nba/latest/1040x760/${selectedPlayer.id}.png`}
                alt={`${selectedPlayer.full_name}'s headshot`}
              />
              {selectedPlayer.full_name}
            </li>
          ) : (
            filteredPlayers.map((player) => (
              <li
                key={player.id}
                onClick={() => handlePlayerClick(player)}
                className={selectedPlayer && selectedPlayer.id === player.id ? "selected" : ""}
              >
                <img
                  width={60}
                  src={`https://cdn.nba.com/headshots/nba/latest/1040x760/${player.id}.png`}
                  alt={`${player.full_name}'s headshot`}
                />
                {player.full_name}
              </li>
            ))
          )}
        </ul>
      </div>
    </div>
  );
};

export default PlayerList;
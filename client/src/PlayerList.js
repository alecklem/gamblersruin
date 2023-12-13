import React, { useEffect, useState } from "react";
import axios from "axios";

const PlayerList = () => {
  const [players, setPlayers] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [filteredPlayers, setFilteredPlayers] = useState([]);

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
    // Filter players based on the search query
    const filtered = players.filter((player) =>
      player.full_name.toLowerCase().includes(searchQuery.toLowerCase())
    );
    setFilteredPlayers(filtered);
  }, [searchQuery, players]);

  return (
    <div>
      <h1>Current NBA Players</h1>
      <div className="search-container">
        <input
          type="text"
          placeholder="Search for a player"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <ul className="dropdown">
          {filteredPlayers.map((player) => (
            <li key={player.id}>
              <img
                width={60}
                src={`https://cdn.nba.com/headshots/nba/latest/1040x760/${player.id}.png`}
                alt={`${player.full_name}'s headshot`}
              />
              {player.full_name}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default PlayerList;

import React, { useEffect, useState } from "react";
import axios from "axios";

const PlayerList = () => {
  const [players, setPlayers] = useState([]);

  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/loadplayers");
        console.log(response.data);
        setPlayers(response.data);
      } catch (error) {
        console.error("Error fetching player data:", error);
      }
    };

    fetchPlayers();
  }, []);

  return (
    <div>
      <h1>Current NBA Players</h1>
      <ul>
        {players.map((player) => (
          <li key={player.id}>
            <img
              width={60}
              src={`https://cdn.nba.com/headshots/nba/latest/1040x760/${player.id}.png`}
            ></img>
            {player.full_name}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PlayerList;

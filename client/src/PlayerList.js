import React, { useEffect, useState } from 'react';
import axios from 'axios';

const PlayerList = () => {
  const [players, setPlayers] = useState([]);

  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        const response = await axios.get('http://localhost:5000/loadplayers');
        setPlayers(response.data.players);
      } catch (error) {
        console.error('Error fetching player data:', error);
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
            {player.full_name} - {player.team}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PlayerList;

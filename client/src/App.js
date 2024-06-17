import React, { useState } from "react";
import "./App.css";
import PlayerList from "./PlayerList";
import PointsDashboard from "./components/dashboards/PointsDashboard";

function App() {
  const [selectedStat, setSelectedStat] = useState(null);
  const [playerData, setPlayerData] = useState(null);

  const handleStatSelection = (stat, data) => {
    setSelectedStat(stat);
    setPlayerData(data);
  };

  return (
    <div className="App">
      <PlayerList onStatSelection={handleStatSelection} />
      {selectedStat && (
        <div className="dashboard-container">
          {selectedStat === "POINTS" && <PointsDashboard data={playerData} />}
          {/* Add other dashboards here based on the selectedStat */}
        </div>
      )}
    </div>
  );
}

export default App;

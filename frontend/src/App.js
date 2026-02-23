import React, { useState } from "react";
import LogInteraction from "./components/LogInteraction";
import FollowupDashboard from "./components/FollowupDashboard";
import "./App.css";

function App() {
  const [page, setPage] = useState("log");

  return (
    <div>
      <div className="nav-container">
        <button
          className={`btn-toggle ${page === "log" ? "active" : ""}`}
          onClick={() => setPage("log")}
        >
          ➕ Log Interaction
        </button>

        <button
          className={`btn-toggle ${page === "dashboard" ? "active" : ""}`}
          onClick={() => setPage("dashboard")}
        >
          📊 Dashboard
        </button>
      </div>

      <div className="container">
        {page === "log" && <LogInteraction />}
        {page === "dashboard" && <FollowupDashboard />}
      </div>
    </div>
  );
}

export default App;
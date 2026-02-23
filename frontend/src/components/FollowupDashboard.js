import React, { useEffect, useState } from "react";
import axios from "axios";

const FollowupDashboard = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchAlerts();
  }, []);

  const fetchAlerts = async () => {
    try {
      const res = await axios.get(
        "http://127.0.0.1:8000/interactions/followup-alerts"
      );
      setData(res.data);
    } catch (err) {
      console.error(err);
      alert("Failed to load alerts");
    }
  };

  const getColor = (priority) => {
    if (priority === "HIGH") return "red";
    if (priority === "MEDIUM") return "orange";
    return "green";
  };

  return (
    <div style={{ padding: 30, fontFamily: "Inter" }}>
      <h2>🚨 Follow-Up Intelligence</h2>

      <table border="1" cellPadding="10" style={{ marginTop: 20 }}>
        <thead>
          <tr>
            <th>HCP Name</th>
            <th>Total Score</th>
            <th>Priority</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, idx) => (
            <tr key={idx}>
              <td>{item.hcp_name}</td>
              <td>{item.total_score}</td>
              <td style={{ color: getColor(item.priority), fontWeight: "bold" }}>
                {item.priority}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default FollowupDashboard;
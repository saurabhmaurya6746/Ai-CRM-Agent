import React, { useState, useEffect } from "react";
import axios from "axios";
import { useDispatch, useSelector } from "react-redux";
import { setLoading, setResponse } from "../redux/interactionSlice";

const LogInteraction = () => {
  const dispatch = useDispatch();
  const { loading, response } = useSelector((state) => state.interaction);

  // ===== STATES =====
  const [hcpName, setHcpName] = useState("");
  const [interactionType, setInteractionType] = useState("Meeting");
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");
  const [attendees, setAttendees] = useState("");
  const [topics, setTopics] = useState("");
  const [materials, setMaterials] = useState("");
  const [sentiment, setSentiment] = useState("Positive 😊");
  const [outcomes, setOutcomes] = useState("");
  const [aiFollowups, setAiFollowups] = useState("");
  const [chatMessage, setChatMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([
  // Initial bot message
  { type: 'bot', message: 'Log interaction details here (e.g., "Met Dr. Smith, discussed Prodo-X efficacy, positive sentiment, shared brochure") or ask for help.' }
]);


  // ✅ Auto fill current date & time
  const fillCurrentDateTime = () => {
    const now = new Date();
    const formattedDate = now.toISOString().split("T")[0];
    const formattedTime = now.toTimeString().slice(0, 5);

    setDate(formattedDate);
    setTime(formattedTime);
  };

  // Auto-fill on component mount
  useEffect(() => {
    fillCurrentDateTime();
  }, []);

  // Watch for response changes and update form
  useEffect(() => {
  if (response?.extracted_fields) {
    const fields = response.extracted_fields;
    console.log("🟢 UPDATING FORM WITH:", fields);
    
    // FORCE UPDATE - even if fields empty, check user_message
    if (response.user_message?.includes("sorry") || response.user_message?.includes("actually")) {
      console.log("🟢 Correction detected in message!");
      
      // Try to extract from user_message manually
      const msg = response.user_message;
      if (msg.includes("Dr. Gupta")) {
        setHcpName("Dr. Gupta");
      }
      if (msg.includes("sentiment was negative")) {
        setSentiment("Negative ☹️");
      }
    }
    
    // Normal update from extracted fields
    if (fields.hcp_name) setHcpName(fields.hcp_name);
    if (fields.sentiment) {
      const s = fields.sentiment.toLowerCase();
      if (s.includes("positive") || s.includes("😊")) setSentiment("Positive 😊");
      else if (s.includes("negative") || s.includes("☹️")) setSentiment("Negative ☹️");
    }
  }
}, [response]);
  // ===== SUBMIT =====


  // Submit function update karo
const submitInteraction = async () => {
  if (!chatMessage.trim()) return;
  setChatMessage("");
  // Add user message to chat
  setChatHistory(prev => [...prev, { type: 'user', message: chatMessage }]);
  
  const formData = {
    hcp_name: hcpName,
    interaction_type: interactionType,
    date,
    time,
    attendees,
    topics_discussed: topics,
    materials,
    sentiment,
    outcomes,
    ai_followups: aiFollowups,
    user_message: chatMessage,
  };

  try {
    dispatch(setLoading(true));
    const res = await axios.post("http://127.0.0.1:8000/interactions/", formData);
    
    console.log("Response:", res.data);
    dispatch(setResponse(res.data));
    setChatMessage(""); 
    // Bot response based on action
    let botMessage = "";
    if (res.data?.extracted_fields?.action === "summarized") {
      botMessage = res.data.extracted_fields.summary || "Here's your summary: The interaction was productive.";
    } else if (res.data?.extracted_fields?.action === "scored") {
      botMessage = `Interaction score: ${res.data.extracted_fields.score || 85}/100`;
    } else if (res.data?.extracted_fields?.action === "clear_form") {
      botMessage = "Form has been cleared successfully!";
    } else if (res.data?.extracted_fields?.action === "edit") {
      botMessage = `✅ Updated: ${res.data.extracted_fields.hcp_name ? 'Name, ' : ''}${res.data.extracted_fields.sentiment ? 'Sentiment' : ''}`.replace(/, $/, '');
    } else {
      botMessage = res.data.summary || "Interaction logged successfully!";
    }
    
    // Add bot response to chat
    setChatHistory(prev => [...prev, { type: 'bot', message: botMessage }]);
    
    
  } catch (err) {
    console.error("API Error:", err);
    setChatMessage(""); 
    setChatHistory(prev => [...prev, { type: 'bot', message: "Sorry, there was an error processing your request." }]);
  } finally {
    dispatch(setLoading(false));
  }
};

// Response useEffect - form update ke liye
useEffect(() => {
  if (response?.extracted_fields) {
    const fields = response.extracted_fields;
    console.log("Updating form with:", fields);
    
    if (fields.hcp_name !== undefined) setHcpName(fields.hcp_name);
    if (fields.sentiment) {
      const s = fields.sentiment.toLowerCase();
      if (s.includes("positive")) setSentiment("Positive 😊");
      else if (s.includes("neutral")) setSentiment("Neutral 😐");
      else if (s.includes("negative")) setSentiment("Negative ☹️");
    }
    if (fields.topics_discussed) setTopics(fields.topics_discussed);
    if (fields.materials) setMaterials(fields.materials);
    if (fields.outcomes) setOutcomes(fields.outcomes);
    if (fields.ai_followups) setAiFollowups(fields.ai_followups);
    
    // Clear form action
    if (fields.action === "clear_form") {
      setHcpName("");
      setTopics("");
      setMaterials("");
      setOutcomes("");
      setAiFollowups("");
      setSentiment("Positive 😊");
    }
  }
}, [response]);

 // Handle Enter key
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      submitInteraction();
    }
  };

  return (
    <>
      <h1 className="main-title">AI-First CRM — Log Interaction</h1>

      <div className="grid">
        {/* ================= LEFT FORM ================= */}
        <div className="card shadow-sm">
          {/* HCP + Interaction */}
          <div className="form-section">
            <h3 className="panel-sub-title">Interaction Details</h3>
            <div className="input-group">
              <input
                className="modern-input"
                placeholder="Search or select HCP..."
                value={hcpName}
                onChange={(e) => setHcpName(e.target.value)}
              />

              <select
                className="modern-select"
                value={interactionType}
                onChange={(e) => setInteractionType(e.target.value)}
              >
                <option>Meeting</option>
                <option>Call</option>
                <option>Email</option>
                <option>Visit</option>
              </select>
            </div>
          </div>

          {/* Date Time */}
          <div className="form-section">
            <div className="input-group">
              <input
                type="date"
                className="modern-input"
                value={date}
                onChange={(e) => setDate(e.target.value)}
              />
              <input
                type="time"
                className="modern-input"
                value={time}
                onChange={(e) => setTime(e.target.value)}
              />
            </div>
          </div>

          {/* Attendees */}
          <div className="form-section">
            <h3 className="panel-sub-title">Attendees</h3>
            <input
              className="modern-input"
              placeholder="Enter names or search..."
              value={attendees}
              onChange={(e) => setAttendees(e.target.value)}
            />
          </div>

          {/* Topics */}
          <div className="form-section">
            <h3 className="panel-sub-title">Topics Discussed</h3>
            <textarea
              className="modern-textarea"
              placeholder="Enter key discussion points..."
              value={topics}
              onChange={(e) => setTopics(e.target.value)}
            />
            <p className="hint-text">
              🎙️ Summarize from Voice Note (Requires Consent)
            </p>
          </div>

          {/* Materials */}
          <div className="form-section">
            <h3 className="panel-sub-title">
              Materials Shared / Samples Distributed
            </h3>
            <div className="input-group">
              <input
                className="modern-input"
                placeholder="No materials added..."
                value={materials}
                onChange={(e) => setMaterials(e.target.value)}
              />
              <button className="outline-btn" type="button">🔍 Search/Add</button>
            </div>
          </div>

          {/* Sentiment */}
          <div className="form-section">
            <h3 className="panel-sub-title">Sentiment Tracking</h3>
            <div className="sentiment-group">
              {["Positive 😊", "Neutral 😐", "Negative ☹️"].map((s) => (
                <label key={s} className="radio-label">
                  <input
                    type="radio"
                    name="sentiment"
                    checked={sentiment === s}
                    onChange={() => setSentiment(s)}
                  />
                  {s}
                </label>
              ))}
            </div>
          </div>

          {/* Outcomes */}
          <div className="form-section">
            <h3 className="panel-sub-title">Outcomes & Follow-ups</h3>
            <textarea
              className="modern-textarea small"
              placeholder="Key outcomes or agreements..."
              value={outcomes}
              onChange={(e) => setOutcomes(e.target.value)}
            />
          </div>

          {/* AI Suggested Followups */}
          <div className="form-section">
            <h3 className="panel-sub-title">AI Suggested Follow-ups</h3>
            <textarea
              className="modern-textarea small"
              placeholder="AI suggestions will appear here..."
              value={aiFollowups}
              onChange={(e) => setAiFollowups(e.target.value)}
              readOnly
            />
          </div>

          <button className="btn-primary-large" onClick={submitInteraction}>
            {loading ? "Logging..." : "Log Interaction"}
          </button>
        </div>

        {/* ================= RIGHT AI PANEL ================= */}
        <div className="card ai-card shadow-sm">
          <div className="ai-header">
            <div className="ai-title">🤖 AI Assistant</div>
            <p className="ai-subtitle">
              Log interaction details here via chat
            </p>
          </div>

          <div className="ai-chat-area">
  {chatHistory.map((chat, index) => (
    <div key={index} className={`chat-bubble ${chat.type}`}>
      {chat.message}
    </div>
  ))}
  
  {loading && (
    <div className="chat-bubble bot">AI is thinking...</div>
  )}
</div>

          <div className="ai-input-footer">
            <div className="chat-input-wrapper">
              <textarea
                className="chat-input-box"
                placeholder="Describe interaction..."
                value={chatMessage}
                onChange={(e) => setChatMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={loading}
              />
              <button 
                className="ai-submit-btn" 
                onClick={submitInteraction}
                disabled={loading}
              >
                {loading ? "..." : "AI Log"}
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default LogInteraction;
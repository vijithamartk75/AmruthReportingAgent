import React, { useState } from "react";

function App() {
  const [input, setInput] = useState("");
  const [reply, setReply] = useState("");
  const API_URL = process.env.REACT_APP_API_URL;

  const sendMessage = async () => {
    const res = await fetch(`${API_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: input }),
    });
    const data = await res.json();
    setReply(data.reply);
  };
  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
    <h2>AI Agent</h2>
    <input
    value={input}
    onChange={(e) => setInput(e.target.value)}
    placeholder="Type your message"
    style={{ padding: "8px", marginRight: "10px" }}
    />
    <button onClick={sendMessage}>Send</button>
    <p style={{ marginTop: "20px" }}>{reply}</p>
    </div>
    );
  }

  export default App;

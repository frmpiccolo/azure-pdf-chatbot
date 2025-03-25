import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    await axios.post("http://localhost:8000/upload/", formData);
  };

  const handleAsk = async () => {
    const res = await axios.post("http://localhost:8000/chat/", {
      question,
    });
    setAnswer(res.data.answer);
  };

  return (
    <div>
      <h1>Azure PDF Chatbot</h1>
      <input type="file" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
      <button onClick={handleUpload}>Upload</button>
      <hr />
      <input type="text" value={question} onChange={(e) => setQuestion(e.target.value)} />
      <button onClick={handleAsk}>Ask</button>
      <p>Answer: {answer}</p>
    </div>
  );
}

export default App;

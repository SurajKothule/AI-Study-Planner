// src/pages/Roadmap.js
import React, { useState } from "react";

export default function Roadmap() {
  const [topic, setTopic] = useState("");
  const [roadmap, setRoadmap] = useState(null);
  const [error, setError] = useState("");

  const handleGenerate = async () => {
    if (!topic.trim()) {
      setError("Please enter a topic.");
      return;
    }

    setError("");
    setRoadmap(null);

    try {
      const response = await fetch(`http://127.0.0.1:5000/api/roadmap?topic=${encodeURIComponent(topic)}`);
      const data = await response.json();

      if (data && data.roadmap) {
        setRoadmap(data.roadmap);
      } else {
        setError("Failed to generate roadmap.");
      }
    } catch (err) {
      console.error(err);
      setError("Something went wrong. Please try again.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold text-center mb-6 text-purple-700">📍 AI Study Roadmap</h1>

      <div className="max-w-xl mx-auto bg-white p-6 rounded-lg shadow-lg">
        <label className="block mb-2 font-semibold text-gray-700">
          Enter a topic you want a roadmap for:
        </label>
        <input
          type="text"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          className="w-full border border-gray-300 rounded px-3 py-2 mb-4"
          placeholder="e.g., Python, Machine Learning"
        />
        <button
          onClick={handleGenerate}
          className="w-full bg-purple-600 text-white py-2 rounded hover:bg-purple-700 transition"
        >
          Generate Roadmap
        </button>

        {error && <p className="text-red-600 mt-4 text-center">⚠️ {error}</p>}
{roadmap && (
  <div className="mt-6">
    <h2 className="text-xl font-bold mb-2 text-green-600">🛣️ Roadmap:</h2>
    <ul className="list-disc pl-6 space-y-2 text-gray-800">
      {roadmap
        .split('\n')
        .filter(line => line.trim() !== '')
        .map((step, index) => (
          <li key={index}>{step}</li>
        ))}
    </ul>
  </div>
)}
        
      </div>
    </div>
  );
}

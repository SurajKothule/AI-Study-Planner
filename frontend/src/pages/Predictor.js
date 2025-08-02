// ✅ src/pages/Predictor.js
import React, { useState } from "react";

export default function Predictor() {
  const [freeTime, setFreeTime] = useState("");
  const [days, setDays] = useState("");
  const [engagement, setEngagement] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:5000/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          free_time_minutes: parseFloat(freeTime),
          days_completed: parseInt(days),
          engagement_score: parseFloat(engagement),
        }),
      });

      if (!response.ok) throw new Error("API request failed");
      const data = await response.json();
      setResult(data.predicted_minutes);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h2 className="text-3xl font-bold text-center mb-6">📊 AI Study Time Predictor</h2>
      <form onSubmit={handleSubmit} className="max-w-xl mx-auto bg-white shadow p-6 rounded-lg space-y-4">
        <div>
          <label className="block font-medium">Free Time Available (minutes)</label>
          <input
            type="number"
            min="0"
            className="w-full mt-1 border border-gray-300 rounded px-3 py-2"
            placeholder="E.g., 120"
            value={freeTime}
            onChange={(e) => setFreeTime(e.target.value)}
            required
          />
        </div>
        <div>
          <label className="block font-medium">Days Completed</label>
          <input
            type="number"
            min="0"
            className="w-full mt-1 border border-gray-300 rounded px-3 py-2"
            placeholder="E.g., 5"
            value={days}
            onChange={(e) => setDays(e.target.value)}
            required
          />
        </div>
        <div>
          <label className="block font-medium">Engagement Score (0 to 1)</label>
          <input
            type="number"
            step="0.01"
            min="0"
            max="1"
            className="w-full mt-1 border border-gray-300 rounded px-3 py-2"
            placeholder="E.g., 0.8"
            value={engagement}
            onChange={(e) => setEngagement(e.target.value)}
            required
          />
        </div>
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
        >
          Predict Study Minutes
        </button>
      </form>
      {result !== null && (
        <div className="mt-6 text-center text-lg font-semibold text-green-600">
          ✅ Predicted Study Minutes: {result.toFixed(2)}
        </div>
      )}
      {error && <div className="mt-4 text-center text-red-600">⚠️ {error}</div>}
    </div>
  );
}

// src/pages/Resource.js
import React, { useState, useMemo } from "react";
import ResourceList from "../components/ResourceList";
const API = process.env.REACT_APP_API_BASE || "http://127.0.0.1:5000";

// Centralized API Service Layer
export const apiService = {
  getResources: async (topic) => {
    const response = await fetch(`${API}/api/resources?topic=${encodeURIComponent(topic)}`);
    if (!response.ok) throw new Error("Failed to fetch resources");
    return response.json();
  },
  predictStudyTime: async (data) => {
    const response = await fetch(`${API}/api/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Failed to predict study time");
    return response.json();
  },
};

export default function Resource() {
  const [query, setQuery] = useState("");
  const [resources, setResources] = useState(null);
  const [searchError, setSearchError] = useState("");

  const handleSearch = async () => {
    setSearchError("");
    setResources(null);

    try {
      const data = await apiService.getResources(query);
      setResources(data);
    } catch (err) {
      setSearchError(err.message);
    }
  };

  // Memoize the resource lists to avoid unnecessary re-renders
  const memoizedResources = useMemo(() => resources, [resources]);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h2 className="text-3xl font-bold text-center mb-6">
        🎓 Search Learning Resources
      </h2>
      <div className="max-w-xl mx-auto">
        <div className="flex gap-2 mb-4">
          <input
            type="text"
            className="w-full border border-gray-300 rounded px-3 py-2"
            placeholder="E.g., Machine Learning"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button
            onClick={handleSearch}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition"
          >
            Search
          </button>
        </div>
        {searchError && (
          <div className="text-red-600 text-center mb-2">⚠️ {searchError}</div>
        )}
        {memoizedResources && <ResourceList resources={memoizedResources} />}

        {!memoizedResources && (
          <p className="text-sm text-gray-500 text-center mt-2">
            Enter a topic to find videos, courses, and repositories.
          </p>
        )}
      </div>
    </div>
  );
}

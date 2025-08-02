// src/pages/Resource.js
import React, { useState } from "react";
import ResourceList from "../components/ResourceList";

export default function Resource() {
  const [query, setQuery] = useState("");
  const [resources, setResources] = useState(null);
  const [searchError, setSearchError] = useState("");

  const handleSearch = async () => {
    setSearchError("");
    setResources(null);

    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/resources?topic=${encodeURIComponent(query)}`
      );
      if (!res.ok) throw new Error("Failed to fetch resources");
      const data = await res.json();
      setResources(data);
    } catch (err) {
      setSearchError(err.message);
    }
  };

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
        {resources && <ResourceList resources={resources} />}

        {!resources && (
          <p className="text-sm text-gray-500 text-center mt-2">
            Enter a topic to find videos, courses, and repositories.
          </p>
        )}
      </div>
    </div>
  );
}

// frontend/src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Resource from "./pages/Resource";
import Roadmap from "./pages/Roadmap";
import InterviewPrep from "./pages/InterviewPrep"; // ✅ Add this import



function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/resources" element={<Resource />} />
        <Route path="/roadmap" element={<Roadmap />} />
        <Route path="/interview-prep" element={<InterviewPrep />} /> {/* ✅ Add this route */}
      </Routes>
    </Router>
  );
}

export default App;

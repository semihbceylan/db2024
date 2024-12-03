import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/home'; // Ensure 'home.js' matches the actual file case
import Chains from './pages/chains'; // Ensure 'chains.js' matches the actual file case
import EOAs from './pages/eoas'; // Ensure 'eoas.js' matches the actual file case

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/table2" element={<Chains />} />
        <Route path="/table1" element={<EOAs />} />
      </Routes>
    </Router>
  );
}

export default App;

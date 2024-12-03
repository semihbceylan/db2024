import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NFTs from './pages/nfts';
import Chains from './pages/chains';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/table1" element={<NFTs />} />
        <Route path="/table2" element={<Chains />} />
      </Routes>
    </Router>
  );
}

export default App;

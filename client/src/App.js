import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NFTs from './pages/nfts';
import Chains from './pages/chains';
import Blocks from './pages/blocks';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/table1" element={<NFTs />} />
        <Route path="/table2" element={<Chains />} />
        <Route path="/table3" element={<Blocks />} />
      </Routes>
    </Router>
  );
}

export default App;

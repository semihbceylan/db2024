import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Eoas from './pages/eoas';
import Chains from './pages/chains';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/table1" element={<Eoas />} />
        <Route path="/table2" element={<Chains />} />
      </Routes>
    </Router>
  );
}

export default App;

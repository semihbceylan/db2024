import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Eoas from './pages/eoas';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/table1" element={<Eoas />} />
      </Routes>
    </Router>
  );
}

export default App;

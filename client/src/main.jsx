import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { createRoot } from 'react-dom/client'
import { StrictMode } from 'react'

import TableRoute from './pages/tableRoute'
import Admin from './pages/admin'
import Home from './pages/home'
import NFTs from './pages/nfts'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/nfts" element={<NFTs />} />
        <Route path="/:tableName/:primaryKey" element={<TableRoute />} />
        <Route path="/admin" element={<Admin />} />
        <Route path="/*" element={<><h1>404 - Page Not Found</h1></>} />
      </Routes>
    </Router>
  </StrictMode>
)
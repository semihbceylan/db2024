import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { createRoot } from 'react-dom/client'
import { StrictMode } from 'react'

import TableRoute from './pages/TableRoute'
import Admin from './pages/Admin'
import Home from './pages/Home'
import NFTs from './pages/NFTs'

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
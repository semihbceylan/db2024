import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useParams } from 'react-router-dom';
import Home from './pages/home';
import NFTs from './pages/nfts';
import Chains from './pages/chains';
import Blocks from './pages/blocks';
import Data from './pages/data';

const NotFoundPage = () => <h1>404 - Page Not Found</h1>;

const VALID_TABLES = ['blocks', 'transactions', 'addresses'];
const TableWrapper = () => {
  const { tableName } = useParams();

  if (!VALID_TABLES.includes(tableName)) {
    return <NotFoundPage />;
  }

  return <Table />;
};

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/table1" element={<NFTs />} />
        <Route path="/table2" element={<Chains />} />
        <Route path="/table3" element={<Blocks />} />
        <Route path="/:tableName/:primaryKey" element={<TableWrapper />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Router>
  );
}

export default App;

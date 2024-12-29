import React, { useState, useEffect } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import logo from '../assets/logo.png';
import '../styles/navbar.css';
import nftIcon from '../assets/nft.png';
import blockIcon from '../assets/blocks.png';

const Navbar = () => {
  const [showCard, setShowCard] = useState(false);
  const [queryParam, setQueryParam] = useState('');
  const navigate = useNavigate();
  const [chains, setChains] = useState([]);
  const [selectedTable, setSelectedTable] = useState('');
  const [selectedChain, setSelectedChain] = useState('');

  useEffect(() => {
    (async () => {
      // Fetch the chain data from your API
      // const response = await axios.get("/api/takeChains");
      // setChains(response.data);
      // For now, we'll use mocked data
      setChains([
        { id: 1, name: 'Chain 1' },
        { id: 2, name: 'Chain 2' },
        { id: 3, name: 'Chain 3' },
      ]);
    })();
  }, []);

  const handleQuery = () => {
    if (queryParam.trim() === '') {
      alert(`Please enter a ${selectedTable.slice(0, -1)} identifier.`);
      return;
    }

    if (selectedTable === '') {
      alert('Please select a table.');
      return;
    }

    // For tables other than 'addresses', require selectedChain
    if (selectedTable !== 'addresses' && selectedChain === '') {
      alert('Please select a chain.');
      return;
    }

    // Construct navigation path based on whether chain is required
    let path = '';
    if (selectedTable === 'addresses') {
      path = `/${selectedTable}/${queryParam}`;
    } else {
      path = `/${selectedTable}/${selectedChain}/${queryParam}`;
    }

    navigate(path);
  };

  // Determine placeholder and label based on selectedTable
  const tableNameSingular = selectedTable ? selectedTable.slice(0, -1).toUpperCase() : 'ITEM';
  let placeholderText = `Enter ${tableNameSingular} Identifier`;
  if (selectedTable === 'nfts') {
    placeholderText = 'Enter NFT Token ID';
  } else if (selectedTable === 'addresses') {
    placeholderText = 'Enter Address';
  }

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <NavLink to="/" className="logo-container">
          <img src={logo} alt="Logo" className="logo-image" />
          <span className="project-name">DataBees</span>
        </NavLink>
        <div className="navbar-links">
          <div className="block-link-wrapper">
            <div
              className="nav-link block-link"
              onClick={() => setShowCard(!showCard)}
            >
              <img src={blockIcon} alt="Block Icon" className="block-icon" />
              Block Explorer
            </div>
            {showCard && (
              <div className="block-card">
                <h3>Query a {tableNameSingular}</h3>
                <div className="selections">
                  <select
                    className="block-select"
                    value={selectedTable}
                    onChange={event => {
                      setSelectedTable(event.target.value);
                      setSelectedChain(''); // Reset chain when table changes
                      setQueryParam('');    // Reset query parameter
                    }}
                  >
                    <option value="" disabled>
                      Choose Table
                    </option>
                    <option value="addresses">Addresses</option>
                    <option value="blocks">Blocks</option>
                    <option value="transactions">Transactions</option>
                    <option value="nfts">NFTs</option>
                  </select>
                  {/* Show chain selection unless 'addresses' is selected */}
                  {selectedTable && selectedTable !== 'addresses' ? (
                    <select
                      className="block-select"
                      value={selectedChain}
                      onChange={e => setSelectedChain(e.target.value)}
                    >
                      <option value="" disabled>
                        Choose Chain
                      </option>
                      {chains.map(chain => (
                        <option key={chain.id} value={chain.id}>
                          {chain.name}
                        </option>
                      ))}
                    </select>
                  ) : null}
                </div>
                <input
                  type="text"
                  className="block-input"
                  placeholder={placeholderText}
                  value={queryParam}
                  onChange={e => setQueryParam(e.target.value)}
                />
                <button className="block-button" onClick={handleQuery}>
                  Query
                </button>
              </div>
            )}
          </div>
          <NavLink
            to="/nft"
            className="nav-link"
            activeclassname="active-link"
          >
            <img src={nftIcon} alt="NFT Icon" className="nft-icon" />
            NFT Page
          </NavLink>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
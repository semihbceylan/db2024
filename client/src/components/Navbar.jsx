import React, { useState, useEffect } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import logo from '../assets/logo.png';
import '../styles/navbar.css';
import nftIcon from '../assets/nft.png';
import blockIcon from '../assets/blocks.png';

const Navbar = () => {
	const [showCard, setShowCard] = useState(false);
	const [blockNumber, setBlockNumber] = useState('');
	const navigate = useNavigate();
	const [chains, setChains] = useState([]);
	const [selectedTable, setSelectedTable] = useState('');
	const [selectedChain, setSelectedChain] = useState('');


	useEffect(() => {
		(async () => {
			/*const response = await axios.get("/api/takeChains");
            setChains(response.data);*/
			setChains([
				{ id: 1, name: 'Chain 1' },
				{ id: 2, name: 'Chain 2' },
				{ id: 3, name: 'Chain 3' },
			]);
		})();
	}, []); 

	const handleQuery = () => {
		if (blockNumber.trim() === '') {
			alert('Please enter a block number.');
			return;
		}

		if (selectedTable === 'blocks') {
			if (selectedChain === '') {
				alert('Please select a chain.');
				return;
			}
			// Navigate with selectedChain when the table is blocks
			navigate(`/${selectedTable}/${selectedChain}/${blockNumber}`);
		} else if (selectedTable === 'addresses') {
			// Navigate to addresses without selectedChain
			navigate(`/${selectedTable}/${blockNumber}`);
		} else {
			// Default behavior for other tables
			navigate(`/${selectedTable}/${blockNumber}`);
		}
	};

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
									<h3>Query a Block</h3>
									<div className="selections">
										<select
											className="block-select"
											value={selectedTable}
											onChange={event => {
												setSelectedTable(event.target.value);
											}}
										>
											<option value="" disabled>
												Choose Table
											</option>
											<option value="addresses">Addresses</option>
											<option value="blocks">Blocks</option>
											<option value="transactions">Transactions</option>
										</select>
										{selectedTable === 'blocks' ? (
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
										placeholder="Enter Block Number"
										value={blockNumber}
										onChange={e => setBlockNumber(e.target.value)}
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

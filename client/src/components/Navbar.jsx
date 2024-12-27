import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import logo from '../assets/logo.png';
import '../styles/navbar.css';
import nftIcon from '../assets/nft.png';
import blockIcon from '../assets/blocks.png';

const Navbar = () => {
	const [showCard, setShowCard] = useState(false);
	const [blockNumber, setBlockNumber] = useState('');
	const navigate = useNavigate();

	const handleQuery = () => {
		if (blockNumber.trim() !== '') {
			navigate(`/blocks/${blockNumber}`);
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
					<NavLink to="/nft" className="nav-link" activeclassname="active-link">
						<img src={nftIcon} alt="NFT Icon" className="nft-icon" />
						NFT Page
					</NavLink>
					<div className="block-link-wrapper">
						<div
							className="nav-link block-link"
							onClick={() => setShowCard(!showCard)}
						>
							<img src={blockIcon} alt="Block Icon" className="block-icon" />
							Blocks
						</div>
						{showCard && (
							<div className="block-card">
								<h3>Query a Block</h3>
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
				</div>
			</div>
		</nav>
	);
};

export default Navbar;

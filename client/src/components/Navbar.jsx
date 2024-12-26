import React from 'react';
import { NavLink } from 'react-router-dom';
import logo from '../assets/logo.png'; 
import '../styles/navbar.css';
import nftIcon from '../assets/nft.png'; 
import blockIcon from '../assets/blocks.png';

const Navbar = () => {
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
					<NavLink
						to="/blocks"
						className="nav-link"
						activeclassname="active-link"
					>
						<img src={blockIcon} alt="Block Icon" className="block-icon" />
						Blocks Page
					</NavLink>
				</div>
			</div>
		</nav>
	);
};



export default Navbar;

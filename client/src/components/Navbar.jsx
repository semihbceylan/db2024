import React from 'react';
import { NavLink } from 'react-router-dom';
import logo from '../assets/logo.png'; 
import '../styles/navbar.css';

const Navbar = () => {
	return (
		<nav className="navbar">
			<div className="navbar-container">
				<NavLink to="/" className="logo-container">
					<img src={logo} alt="Logo" className="logo-image" />
					<span className="project-name">DataBees</span>
				</NavLink>
				<div className="navbar-links">
					<NavLink to="/nft" className="nav-link" activeClassName="active-link">
						NFT Page
					</NavLink>
					<NavLink
						to="/blocks"
						className="nav-link"
						activeClassName="active-link"
					>
						Blocks Page
					</NavLink>
				</div>
			</div>
		</nav>
	);
};


export default Navbar;

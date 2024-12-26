import React from 'react';
import Navbar from '../components/Navbar';
import '../styles/index.css';

export default function Home () {
    return (
			<div>
				<Navbar />
				<div className="page-content">
					<h1>Home</h1>
					<p>Welcome to the home page!</p>
				</div>
			</div>
		);
}
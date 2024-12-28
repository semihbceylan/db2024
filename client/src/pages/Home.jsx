import React from 'react';
import Navbar from '../components/Navbar';
import '../styles/index.css';
import { ChainViewer } from '../components/chainViewer';
import Sections from '../components/sections';
export default function Home () {
    return (
			<div>
				<Navbar />
				<div className="page-content">
					<Sections />
					<div style={{ 
					display: 'flex', 
					gap: '20px', 
					padding: '20px',
					maxWidth: '1200px',
					margin: '0 auto'
					}}>
					
					
					<ChainViewer />
					</div>
				</div>
			</div>
		);
}
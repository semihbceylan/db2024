import '../styles/index.css';
import Navbar from '../components/Navbar';
import '../styles/nfts.css';
//import { require } from 'module';
import nftcardimg1 from '../assets/nft-card-img-1.jpg';

export default function NFTs () {
	return (
		<div className="page-content">
			<Navbar/>
			<div className="container">
				<h1>NFTs</h1>
				<p>Welcome to the table page!</p>
				<div className="nft-cards">
					<div className="nft-card">
						<div className="nft-card-img-wrapper"><img src={nftcardimg1} alt="NFT Card" /></div>
						<div className="details">
							<h2>Lorem ipsum dolor sit.</h2>
							<p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptatibus, veritatis.</p>
						</div>
					</div>
					<div className="nft-card">
						<div className="nft-card-img-wrapper"><img src={nftcardimg1} alt="NFT Card" /></div>
						<div className="details">
							<h2>Lorem ipsum dolor sit.</h2>
							<p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptatibus, veritatis.</p>
						</div>
					</div>
					<div className="nft-card">
						<div className="nft-card-img-wrapper"><img src={nftcardimg1} alt="NFT Card" /></div>
						<div className="details">
							<h2>Lorem ipsum dolor sit.</h2>
							<p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptatibus, veritatis.</p>
						</div>
					</div>
					<div className="nft-card">
						<div className="nft-card-img-wrapper"><img src={nftcardimg1} alt="NFT Card" /></div>
						<div className="details">
							<h2>Lorem ipsum dolor sit.</h2>
							<p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptatibus, veritatis.</p>
						</div>
					</div>
					<div className="nft-card">
						<div className="nft-card-img-wrapper"><img src={nftcardimg1} alt="NFT Card" /></div>
						<div className="details">
							<h2>Lorem ipsum dolor sit.</h2>
							<p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptatibus, veritatis.</p>
						</div>
					</div>
					<div className="nft-card">
						<div className="nft-card-img-wrapper"><img src={nftcardimg1} alt="NFT Card" /></div>
						<div className="details">
							<h2>Lorem ipsum dolor sit.</h2>
							<p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptatibus, veritatis.</p>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
}
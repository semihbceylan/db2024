import axios from 'axios';
import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import '../styles/index.css';
import '../styles/explorer.css';

export default function BlockExplorer() {
	const { tableName, primaryKey } = useParams();

	const [data, setData] = useState(null);

	useEffect(() => {
		(async () => {
			const response = await axios.get(`/api/${tableName}/${primaryKey}`);
			setData(response.data);
			setData(TEST_DATA);
		})();
	}, [primaryKey]);

	return data != null ? (
		<>
			<Navbar />
			<div className="page-content">
				<div className="block-explorer-page">
					<header className="block-header">
						<h1 className="block-title">{data.tableName}</h1>
						<span className="block-primary-key">
							{Array.isArray(data.primaryKey)
								? data.primaryKey.join(', ')
								: data.primaryKey}
						</span>
					</header>
					<div className="block-details">
						{Object.entries(data).map(
							([key, value]) =>
								key !== 'tableName' &&
								key !== 'primaryKey' && (
									<div key={key} className="block-detail-item">
										<span className="block-detail-key">
											{key.replace('_', ' ')}:
										</span>
										<span className="block-detail-value">
											{typeof value === 'object'
												? JSON.stringify(value)
												: value.toString()}
										</span>
									</div>
								)
						)}
					</div>
				</div>
			</div>
		</>
	) : (
		<>
			<Navbar />
			<div className="loading-container">
				<h1>Loading...</h1>
			</div>
		</>
	);
}

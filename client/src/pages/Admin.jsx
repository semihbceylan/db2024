// src/pages/Admin.jsx
import { useState, useEffect } from 'react';
import axios from '../utils/axiosConfig';
import Navbar from '../components/Navbar';
import "../styles/admin.css";

export default function Admin () {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [chains, setChains] = useState([]);
    const [selectedTable, setSelectedTable] = useState("");
    const [selectedOperation, setSelectedOperation] = useState("");
    const [formData, setFormData] = useState({});
    const [message, setMessage] = useState("");

    useEffect(() => {
        if (isAuthenticated && selectedTable === "chains" && selectedOperation === "GET_ALL") {
            axios.get('/chains/')
                .then(response => setChains(response.data))
                .catch(error => {
                    console.error("Error fetching chains:", error);
                    setMessage("Failed to fetch chains.");
                });
        }
    }, [isAuthenticated, selectedTable, selectedOperation]);

    const handleChange = (e) => {
        setFormData({...formData, [e.target.name]: e.target.value});
    };

    const handleSubmit = async () => {
        setMessage("");
        try {
            let response;
            switch(selectedTable) {
                case "addresses":
                    if(selectedOperation === "GET") {
                        response = await axios.get(`/addresses/${formData.address}`);
                        setMessage(JSON.stringify(response.data));
                    }
                    else if(selectedOperation === "POST") {
                        response = await axios.post(`/addresses/${formData.address}`, {});
                        setMessage(response.data.message);
                    }
                    else if(selectedOperation === "DELETE") {
                        response = await axios.delete(`/addresses/${formData.address}`);
                        setMessage(response.data.message);
                    }
                    break;
                case "blocks":
                    if(selectedOperation === "GET") {
                        response = await axios.get(`/blocks/${formData.chain_id}/${formData.block_number}`);
                        setMessage(JSON.stringify(response.data));
                    }
                    else if(selectedOperation === "POST") {
                        response = await axios.post(`/blocks/${formData.chain_id}/${formData.block_number}`, {});
                        setMessage(response.data.message);
                    }
                    else if(selectedOperation === "FULL_POST") {
                        response = await axios.post(`/blocks/full/${formData.chain_id}/${formData.block_number}`, {});
                        setMessage(response.data.message);
                    }
                    else if(selectedOperation === "DELETE") {
                        response = await axios.delete(`/blocks/${formData.chain_id}/${formData.block_number}`);
                        setMessage(response.data.message);
                    }
                    break;
                case "chains":
                    if(selectedOperation === "GET_ALL") {
                        response = await axios.get(`/chains/`);
                        setMessage(JSON.stringify(response.data));
                    }
                    else if(selectedOperation === "GET") {
                        response = await axios.get(`/chains/${formData.chain_id}`);
                        setMessage(JSON.stringify(response.data));
                    }
                    else if(selectedOperation === "POST") {
                        response = await axios.post(`/chains/`, {
                            chain_id: parseInt(formData.chain_id),
                            chain_name: formData.chain_name,
                            native_currency: formData.native_currency,
                            explorer_url: formData.explorer_url,
                            rpc_url: formData.rpc_url
                        });
                        setMessage(response.data.message);
                    }
                    else if(selectedOperation === "PUT") {
                        response = await axios.put(`/chains/${formData.chain_id}`, {
                            chain_name: formData.chain_name,
                            native_currency: formData.native_currency,
                            explorer_url: formData.explorer_url,
                            rpc_url: formData.rpc_url
                        });
                        setMessage(response.data.message);
                    }
                    else if(selectedOperation === "DELETE") {
                        response = await axios.delete(`/chains/${formData.chain_id}`);
                        setMessage(response.data.message);
                    }
                    break;
                case "nfts":
                    if(selectedOperation === "GET_ALL") {
                        response = await axios.get(`/nfts/`);
                        setMessage(JSON.stringify(response.data));
                    }
                    else if(selectedOperation === "GET_CONTRACT") {
                        response = await axios.get(`/nfts/${formData.chain_id}/${formData.contract_address}`);
                        setMessage(JSON.stringify(response.data));
                    }
                    else if(selectedOperation === "GET_NFT") {
                        response = await axios.get(`/nfts/${formData.chain_id}/${formData.contract_address}/${formData.token_id}`);
                        setMessage(JSON.stringify(response.data));
                    }

                    else if(selectedOperation === "DELETE_CONTRACT") {
                        response = await axios.delete(`/nfts/${formData.chain_id}/${formData.contract_address}`);
                        setMessage(response.data.message);
                    }
                    else if(selectedOperation === "DELETE_NFT") {
                        response = await axios.delete(`/nfts/${formData.chain_id}/${formData.contract_address}/${formData.token_id}`);
                        setMessage(response.data.message);
                    }
                    else if(selectedOperation === "ALL_POST") {
                        response = await axios.post(`/nfts/`, {});
                        setMessage(response.data.message);
                    }
                    break;
                case "transactions":
                    if(selectedOperation === "GET") {
                        response = await axios.get(`/transactions/${formData.chain_id}/${formData.tx_hash}`);
                        setMessage(JSON.stringify(response.data));
                    }
                    else if(selectedOperation === "POST") {
                        response = await axios.post(`/transactions/${formData.chain_id}/${formData.tx_hash}`, {});
                        setMessage(response.data.message);
                    }
                    else if(selectedOperation === "FULL_POST") {
                        response = await axios.post(`/transactions/full/${formData.chain_id}/${formData.tx_hash}`, {});
                        setMessage(response.data.message);
                    }
                    else if(selectedOperation === "DELETE") {
                        response = await axios.delete(`/transactions/${formData.chain_id}/${formData.tx_hash}`);
                        setMessage(response.data.message);
                    }
                    break;
                default:
                    setMessage("Invalid table or operation.");
            }
        } catch (error) {
            if(error.response && error.response.data && error.response.data.error){
                setMessage(`Error: ${error.response.data.error}`);
            }
            else {
                setMessage("An unexpected error occurred.");
            }
        }
    };

    const renderForm = () => {
        switch(selectedTable) {
            case "addresses":
                return (
                    <>
                        {(selectedOperation === "GET" || selectedOperation === "POST" || selectedOperation === "FULL_POST" || selectedOperation === "DELETE") && (
                            <input 
                                type="text" 
                                name="address" 
                                placeholder="Address" 
                                value={formData.address || ""}
                                onChange={handleChange}
                            />
                        )}
                    </>
                );
            case "blocks":
                return (
                    <>
                        {(selectedOperation === "GET" || selectedOperation === "POST" || selectedOperation === "FULL_POST" || selectedOperation === "DELETE") && (
                            <>
                                <input 
                                    type="number" 
                                    name="chain_id" 
                                    placeholder="Chain ID" 
                                    value={formData.chain_id || ""}
                                    onChange={handleChange}
                                />
                                <input 
                                    type="number" 
                                    name="block_number" 
                                    placeholder="Block Number" 
                                    value={formData.block_number || ""}
                                    onChange={handleChange}
                                />
                            </>
                        )}
                    </>
                );
            case "chains":
                return (
                    <>
                        {(selectedOperation === "GET" || selectedOperation === "DELETE" || selectedOperation === "PUT" || selectedOperation === "GET_ALL") && (
                            <input 
                                type="number" 
                                name="chain_id" 
                                placeholder="Chain ID" 
                                value={formData.chain_id || ""}
                                onChange={handleChange}
                            />
                        )}
                        {(selectedOperation === "POST" || selectedOperation === "PUT") && (
                            <>
                                <input 
                                    type="text" 
                                    name="chain_name" 
                                    placeholder="Chain Name" 
                                    value={formData.chain_name || ""}
                                    onChange={handleChange}
                                />
                                <input 
                                    type="text" 
                                    name="native_currency" 
                                    placeholder="Native Currency" 
                                    value={formData.native_currency || ""}
                                    onChange={handleChange}
                                />
                                <input 
                                    type="text" 
                                    name="explorer_url" 
                                    placeholder="Explorer URL" 
                                    value={formData.explorer_url || ""}
                                    onChange={handleChange}
                                />
                                <input 
                                    type="text" 
                                    name="rpc_url" 
                                    placeholder="RPC URL" 
                                    value={formData.rpc_url || ""}
                                    onChange={handleChange}
                                />
                            </>
                        )}
                    </>
                );
            case "nfts":
                return (
                    <>
                        {(selectedOperation === "GET_CONTRACT" || selectedOperation === "DELETE_CONTRACT" || selectedOperation === "POST_CONTRACT") && (
                            <>
                                <input 
                                    type="number" 
                                    name="chain_id" 
                                    placeholder="Chain ID" 
                                    value={formData.chain_id || ""}
                                    onChange={handleChange}
                                />
                                <input 
                                    type="text" 
                                    name="contract_address" 
                                    placeholder="Contract Address" 
                                    value={formData.contract_address || ""}
                                    onChange={handleChange}
                                />
                            </>
                        )}
                        {(selectedOperation === "GET_NFT" || selectedOperation === "DELETE_NFT" || selectedOperation === "POST_NFT") && (
                            <>
                                <input 
                                    type="number" 
                                    name="chain_id" 
                                    placeholder="Chain ID" 
                                    value={formData.chain_id || ""}
                                    onChange={handleChange}
                                />
                                <input 
                                    type="text" 
                                    name="contract_address" 
                                    placeholder="Contract Address" 
                                    value={formData.contract_address || ""}
                                    onChange={handleChange}
                                />
                                <input 
                                    type="number" 
                                    name="token_id" 
                                    placeholder="Token ID" 
                                    value={formData.token_id || ""}
                                    onChange={handleChange}
                                />
                            </>
                        )}
                        {(selectedOperation === "GET_OWNER") && (
                            <input 
                                type="text" 
                                name="owner" 
                                placeholder="Owner Address" 
                                value={formData.owner || ""}
                                onChange={handleChange}
                            />
                        )}
                        {(selectedOperation === "ALL_POST") && (
                            <></>
                        )}
                    </>
                );
            case "transactions":
                return (
                    <>
                        {(selectedOperation === "GET" || selectedOperation === "POST" || selectedOperation === "FULL_POST" || selectedOperation === "DELETE") && (
                            <>
                                <input 
                                    type="number" 
                                    name="chain_id" 
                                    placeholder="Chain ID" 
                                    value={formData.chain_id || ""}
                                    onChange={handleChange}
                                />
                                <input 
                                    type="text" 
                                    name="tx_hash" 
                                    placeholder="Transaction Hash" 
                                    value={formData.tx_hash || ""}
                                    onChange={handleChange}
                                />
                            </>
                        )}
                    </>
                );
            default:
                return null;
        }
    };

    return isAuthenticated ? (
        <div>
            <Navbar />
            <div className="page-content">
                <div className="input-card">
                    <h2>Admin Panel</h2>
                    <div className="selections">
                        <select onChange={(e) => { setSelectedTable(e.target.value); setSelectedOperation(""); setFormData({}); setMessage(""); }} value={selectedTable}>
                            <option value="" disabled>Choose Table</option>
                            <option value="addresses">Addresses</option>
                            <option value="blocks">Blocks</option>
                            <option value="chains">Chains</option>
                            <option value="nfts">NFTs</option>
                            <option value="transactions">Transactions</option>
                        </select>
                        {selectedTable && (
                            <select onChange={(e) => { setSelectedOperation(e.target.value); setFormData({}); setMessage(""); }} value={selectedOperation}>
                                <option value="" disabled>Choose Operation</option>
                                {selectedTable === "chains" ? (
                                    <>
                                        <option value="GET_ALL">GET All</option>
                                        <option value="GET">GET</option>
                                        <option value="DELETE">DELETE</option>
                                    </>
                                ) : selectedTable === "nfts" ? (
                                    <>
                                        <option value="GET_ALL">GET All</option>
                                        <option value="GET_NFT">GET NFT</option>
                                        <option value="DELETE_NFT">DELETE NFT</option>
                                    </>
                                ) : (
                                    <>
                                        <option value="GET">GET</option>
                                        <option value="DELETE">DELETE</option>
                                    </>
                                )}
                            </select>
                        )}
                    </div>
                    <div className="form-fields">
                        {renderForm()}
                    </div>
                    <button onClick={handleSubmit}>Submit</button>
                    {message && <div className="message">{message}</div>}
                </div>
            </div>
        </div>
    ) : (
        <div>
            <Navbar />
            <div className='page-content'>
                <button 
                    className="authentication" 
                    onClick={() => setIsAuthenticated(true)}
                >
                    Authenticate
                </button>
            </div>
        </div>
    );
}

// src/pages/Admin.jsx
import { useState } from 'react';
import axios from '../utils/axiosConfig';
import Navbar from '../components/Navbar';
import "../styles/admin.css";

export default function Admin() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [selectedTable, setSelectedTable] = useState("");
    const [selectedOperation, setSelectedOperation] = useState("");
    const [formData, setFormData] = useState({});
    const [message, setMessage] = useState("");
    const [insertType, setInsertType] = useState("normal"); // For Addresses and Blocks

    // Helper function to validate Ethereum addresses
    const isValidHexAddress = (address) => {
        return /^0x[a-fA-F0-9]{40}$/.test(address);
    };

    // Helper function to validate Transaction Hashes
    const isValidTxHash = (txHash) => {
        return /^0x[a-fA-F0-9]{64}$/.test(txHash);
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleInsertTypeChange = (e) => {
        setInsertType(e.target.value);
    };

    const handleSubmit = async () => {
        setMessage("");

        // Frontend Validation
        if (selectedOperation === "INSERT" || selectedOperation === "PUT") {
            if (selectedTable === "chains") {
                const requiredFields = ["chain_id", "chain_name", "native_currency", "explorer_url", "rpc_url"];
                for (let field of requiredFields) {
                    if (!formData[field]) {
                        setMessage(`Error: ${field.replace('_', ' ')} is required.`);
                        return;
                    }
                }
            }

            if (selectedTable === "nfts" && selectedOperation === "INSERT") {
                if (formData.contract_address && !isValidHexAddress(formData.contract_address)) {
                    setMessage("Error: Contract Address must be a valid hex address (e.g., 0x1234567890abcdef1234567890abcdef12345678).");
                    return;
                }
            }

            if (selectedTable === "nfts" && selectedOperation === "GET") {
                if (formData.contract_address && !isValidHexAddress(formData.contract_address)) {
                    setMessage("Error: Contract Address must be a valid hex address.");
                    return;
                }
            }

            if (selectedTable === "transactions" && selectedOperation === "INSERT") {
                if (formData.tx_hash && !isValidTxHash(formData.tx_hash)) {
                    setMessage("Error: Transaction Hash must be a valid hex transaction hash (e.g., 0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890).");
                    return;
                }
            }

            if (selectedTable === "transactions" && selectedOperation === "GET") {
                if (formData.tx_hash && !isValidTxHash(formData.tx_hash)) {
                    setMessage("Error: Transaction Hash must be a valid hex transaction hash.");
                    return;
                }
            }
        }

        try {
            let response;
            switch (selectedTable) {
                case "addresses":
                    if (selectedOperation === "GET") {
                        response = await axios.get(`/addresses/${formData.address}`);
                        setMessage(JSON.stringify(response.data, null, 2));
                    } else if (selectedOperation === "INSERT") {
                        if (insertType === "normal") {
                            response = await axios.post(`/addresses/${formData.address}`, {});
                        } else {
                            response = await axios.post(`/addresses/full/${formData.address}/`, {});
                        }
                        setMessage(response.data.message);
                    } else if (selectedOperation === "DELETE") {
                        response = await axios.delete(`/addresses/${formData.address}`);
                        setMessage(response.data.message);
                    }
                    break;
                case "blocks":
                    if (selectedOperation === "GET") {
                        response = await axios.get(`/blocks/${formData.chain_id}/${formData.block_number}`);
                        setMessage(JSON.stringify(response.data, null, 2));
                    } else if (selectedOperation === "INSERT") {
                        if (insertType === "normal") {
                            response = await axios.post(`/blocks/${formData.chain_id}/${formData.block_number}`, {});
                        } else {
                            response = await axios.post(`/blocks/full/${formData.chain_id}/${formData.block_number}`, {});
                        }
                        setMessage(response.data.message);
                    } else if (selectedOperation === "DELETE") {
                        response = await axios.delete(`/blocks/${formData.chain_id}/${formData.block_number}`);
                        setMessage(response.data.message);
                    } else if (selectedOperation === "GET_LATEST_BLOCKS") {
                        response = await axios.get(`/blocks/latest-blocks-for-each-chain`);
                        setMessage(JSON.stringify(response.data, null, 2));
                    }
                    break;
                case "chains":
                    if (selectedOperation === "GET_ALL") {
                        response = await axios.get(`/chains/`);
                        setMessage(JSON.stringify(response.data, null, 2));
                    } else if (selectedOperation === "GET") {
                        response = await axios.get(`/chains/${formData.chain_id}`);
                        setMessage(JSON.stringify(response.data, null, 2));
                    } else if (selectedOperation === "INSERT") {
                        response = await axios.post(`/chains/`, {
                            chain_id: parseInt(formData.chain_id),
                            chain_name: formData.chain_name,
                            native_currency: formData.native_currency,
                            explorer_url: formData.explorer_url,
                            rpc_url: formData.rpc_url
                        });
                        setMessage(response.data.message);
                    } else if (selectedOperation === "PUT") {
                        response = await axios.put(`/chains/${formData.chain_id}`, {
                            chain_name: formData.chain_name,
                            native_currency: formData.native_currency,
                            explorer_url: formData.explorer_url,
                            rpc_url: formData.rpc_url
                        });
                        setMessage(response.data.message);
                    } else if (selectedOperation === "DELETE") {
                        response = await axios.delete(`/chains/${formData.chain_id}`);
                        setMessage(response.data.message);
                    }
                    break;
                case "nfts":
                    if (selectedOperation === "GET_ALL") {
                        response = await axios.get(`/nfts/`);
                        setMessage(JSON.stringify(response.data, null, 2));
                    } else if (selectedOperation === "GET") {
                        if (formData.token_id) {
                            response = await axios.get(`/nfts/${formData.chain_id}/${formData.contract_address}/${formData.token_id}`);
                        } else {
                            response = await axios.get(`/nfts/${formData.chain_id}/${formData.contract_address}`);
                        }
                        setMessage(JSON.stringify(response.data, null, 2));
                    } else if (selectedOperation === "INSERT") {
                        if (formData.token_id) {
                            response = await axios.post(`/nfts/${formData.chain_id}/${formData.contract_address}/${formData.token_id}`, {});
                        } else {
                            response = await axios.post(`/nfts/${formData.chain_id}/${formData.contract_address}`, {});
                        }
                        setMessage(response.data.message);
                    } else if (selectedOperation === "DELETE") {
                        if (formData.token_id) {
                            response = await axios.delete(`/nfts/${formData.chain_id}/${formData.contract_address}/${formData.token_id}`);
                        } else {
                            response = await axios.delete(`/nfts/${formData.chain_id}/${formData.contract_address}`);
                        }
                        setMessage(response.data.message);
                    }
                    break;
                case "transactions":
                    if (selectedOperation === "GET") {
                        response = await axios.get(`/transactions/${formData.chain_id}/${formData.tx_hash}`);
                        setMessage(JSON.stringify(response.data, null, 2));
                    } else if (selectedOperation === "INSERT") {
                        response = await axios.post(`/transactions/${formData.chain_id}/${formData.tx_hash}`, {});
                        setMessage(response.data.message);
                    } else if (selectedOperation === "DELETE") {
                        response = await axios.delete(`/transactions/${formData.chain_id}/${formData.tx_hash}`);
                        setMessage(response.data.message);
                    }
                    break;
                default:
                    setMessage("Invalid table or operation.");
            }
        } catch (error) {
            if (error.response && error.response.data && error.response.data.error) {
                setMessage(`Error: ${error.response.data.error}`);
            } else if (error.response && error.response.data && error.response.data.message) {
                setMessage(`Error: ${error.response.data.message}`);
            } else {
                setMessage("An unexpected error occurred.");
            }
        }
    };

    const renderForm = () => {
        switch (selectedTable) {
            case "addresses":
                return (
                    <>
                        {(selectedOperation === "GET" || selectedOperation === "DELETE" || selectedOperation === "INSERT") && (
                            <>
                                <input
                                    type="text"
                                    name="address"
                                    placeholder="0x1234567890abcdef1234567890abcdef12345678"
                                    value={formData.address || ""}
                                    onChange={handleChange}
                                    required
                                />
                                {selectedOperation === "INSERT" && (
                                    <div className="insert-type">
                                        <label>
                                            <input
                                                type="radio"
                                                name="insertType"
                                                value="normal"
                                                checked={insertType === "normal"}
                                                onChange={handleInsertTypeChange}
                                            />
                                            Normal Insert
                                        </label>
                                        <label>
                                            <input
                                                type="radio"
                                                name="insertType"
                                                value="full"
                                                checked={insertType === "full"}
                                                onChange={handleInsertTypeChange}
                                            />
                                            Full Insert
                                        </label>
                                    </div>
                                )}
                            </>
                        )}
                    </>
                );
            case "blocks":
                return (
                    <>
                        {(selectedOperation === "GET" || selectedOperation === "DELETE" || selectedOperation === "INSERT" || selectedOperation === "GET_LATEST_BLOCKS") && (
                            <>
                                {selectedOperation !== "GET_LATEST_BLOCKS" && (
                                    <>
                                        <input
                                            type="number"
                                            name="chain_id"
                                            placeholder="Chain ID"
                                            value={formData.chain_id || ""}
                                            onChange={handleChange}
                                            required
                                        />
                                        <input
                                            type="number"
                                            name="block_number"
                                            placeholder="Block Number"
                                            value={formData.block_number || ""}
                                            onChange={handleChange}
                                            required
                                        />
                                    </>
                                )}
                                {selectedOperation === "INSERT" && (
                                    <div className="insert-type">
                                        <label>
                                            <input
                                                type="radio"
                                                name="insertType"
                                                value="normal"
                                                checked={insertType === "normal"}
                                                onChange={handleInsertTypeChange}
                                            />
                                            Normal Insert
                                        </label>
                                        <label>
                                            <input
                                                type="radio"
                                                name="insertType"
                                                value="full"
                                                checked={insertType === "full"}
                                                onChange={handleInsertTypeChange}
                                            />
                                            Full Insert
                                        </label>
                                    </div>
                                )}
                            </>
                        )}
                        {selectedOperation === "GET_LATEST_BLOCKS" && (
                            <p>No input fields required. Click Submit to fetch latest blocks.</p>
                        )}
                    </>
                );
            case "chains":
                return (
                    <>
                        {(selectedOperation === "GET_ALL" || selectedOperation === "GET" || selectedOperation === "DELETE" || selectedOperation === "INSERT" || selectedOperation === "PUT") && (
                            <>
                                {selectedOperation !== "GET_ALL" && (
                                    <input
                                        type="number"
                                        name="chain_id"
                                        placeholder="Chain ID"
                                        value={formData.chain_id || ""}
                                        onChange={handleChange}
                                        required
                                    />
                                )}
                                {(selectedOperation === "INSERT" || selectedOperation === "PUT") && (
                                    <>
                                        <input
                                            type="text"
                                            name="chain_name"
                                            placeholder="Chain Name"
                                            value={formData.chain_name || ""}
                                            onChange={handleChange}
                                            required
                                        />
                                        <input
                                            type="text"
                                            name="native_currency"
                                            placeholder="Native Currency (e.g., ETH, MATIC)"
                                            value={formData.native_currency || ""}
                                            onChange={handleChange}
                                            required
                                        />
                                        <input
                                            type="text"
                                            name="explorer_url"
                                            placeholder="Explorer URL (e.g., https://etherscan.io)"
                                            value={formData.explorer_url || ""}
                                            onChange={handleChange}
                                            required
                                        />
                                        <input
                                            type="text"
                                            name="rpc_url"
                                            placeholder="RPC URL (e.g., https://cloudflare-eth.com)"
                                            value={formData.rpc_url || ""}
                                            onChange={handleChange}
                                            required
                                        />
                                    </>
                                )}
                            </>
                        )}
                    </>
                );
            case "nfts":
                return (
                    <>
                        {(selectedOperation === "GET_ALL" || selectedOperation === "DELETE" || selectedOperation === "INSERT" || selectedOperation === "GET") && (
                            <>
                                {selectedOperation !== "GET_ALL" && (
                                    <>
                                        <input
                                            type="number"
                                            name="chain_id"
                                            placeholder="Chain ID"
                                            value={formData.chain_id || ""}
                                            onChange={handleChange}
                                            required
                                        />
                                        <input
                                            type="text"
                                            name="contract_address"
                                            placeholder="Contract Address (e.g., 0x1234567890abcdef1234567890abcdef12345678)"
                                            value={formData.contract_address || ""}
                                            onChange={handleChange}
                                            required
                                        />
                                        {(selectedOperation === "GET" || selectedOperation === "DELETE" || selectedOperation === "INSERT") && (
                                            <input
                                                type="text"
                                                name="token_id"
                                                placeholder="Token ID"
                                                value={formData.token_id || ""}
                                                onChange={handleChange}
                                                required
                                            />
                                        )}
                                    </>
                                )}
                            </>
                        )}
                    </>
                );
            case "transactions":
                return (
                    <>
                        {(selectedOperation === "GET" || selectedOperation === "DELETE" || selectedOperation === "INSERT") && (
                            <>
                                <input
                                    type="number"
                                    name="chain_id"
                                    placeholder="Chain ID"
                                    value={formData.chain_id || ""}
                                    onChange={handleChange}
                                    required
                                />
                                <input
                                    type="text"
                                    name="tx_hash"
                                    placeholder="Transaction Hash (e.g., 0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890)"
                                    value={formData.tx_hash || ""}
                                    onChange={handleChange}
                                    required
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
                        <select
                            onChange={(e) => {
                                setSelectedTable(e.target.value);
                                setSelectedOperation("");
                                setFormData({});
                                setInsertType("normal");
                                setMessage("");
                            }}
                            value={selectedTable}
                        >
                            <option value="" disabled>Choose Table</option>
                            <option value="addresses">Addresses</option>
                            <option value="blocks">Blocks</option>
                            <option value="chains">Chains</option>
                            <option value="nfts">NFTs</option>
                            <option value="transactions">Transactions</option>
                        </select>
                        {selectedTable && (
                            <select
                                onChange={(e) => {
                                    setSelectedOperation(e.target.value);
                                    setFormData({});
                                    setInsertType("normal");
                                    setMessage("");
                                }}
                                value={selectedOperation}
                            >
                                <option value="" disabled>Choose Operation</option>
                                {selectedTable === "chains" ? (
                                    <>
                                        <option value="GET_ALL">GET All</option>
                                        <option value="GET">GET</option>
                                        <option value="INSERT">INSERT</option>
                                        <option value="PUT">PUT</option>
                                        <option value="DELETE">DELETE</option>
                                    </>
                                ) : selectedTable === "blocks" ? (
                                    <>
                                        <option value="GET">GET</option>
                                        <option value="INSERT">INSERT</option>
                                        <option value="DELETE">DELETE</option>
                                        <option value="GET_LATEST_BLOCKS">GET Latest Blocks</option>
                                    </>
                                ) : selectedTable === "addresses" ? (
                                    <>
                                        <option value="GET">GET</option>
                                        <option value="INSERT">INSERT</option>
                                        <option value="DELETE">DELETE</option>
                                    </>
                                ) : selectedTable === "nfts" ? (
                                    <>
                                        <option value="GET_ALL">GET All</option>
                                        <option value="GET">GET</option>
                                        <option value="INSERT">INSERT</option>
                                        <option value="DELETE">DELETE</option>
                                    </>
                                ) : selectedTable === "transactions" ? (
                                    <>
                                        <option value="GET">GET</option>
                                        <option value="INSERT">INSERT</option>
                                        <option value="DELETE">DELETE</option>
                                    </>
                                ) : null}
                            </select>
                        )}
                    </div>
                    <div className="form-fields">
                        {renderForm()}
                    </div>
                    {/* Insert Type Selection for Addresses and Blocks */}
                    {((selectedTable === "addresses" && selectedOperation === "INSERT") ||
                      (selectedTable === "blocks" && selectedOperation === "INSERT")) && (
                        <div className="insert-type">
                            <label>
                                <input
                                    type="radio"
                                    name="insertType"
                                    value="normal"
                                    checked={insertType === "normal"}
                                    onChange={handleInsertTypeChange}
                                />
                                Normal Insert
                            </label>
                            <label>
                                <input
                                    type="radio"
                                    name="insertType"
                                    value="full"
                                    checked={insertType === "full"}
                                    onChange={handleInsertTypeChange}
                                />
                                Full Insert
                            </label>
                        </div>
                    )}
                    <button onClick={handleSubmit}>Submit</button>
                    {message && <pre className="message">{message}</pre>}
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

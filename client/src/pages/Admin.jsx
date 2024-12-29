import { useState, useEffect } from 'react';
import axios from 'axios';

import authenticate from '../utils/authenticate';
import Navbar from '../components/Navbar';
import "../styles/admin.css";

export default function Admin () {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [chains, setChains] = useState([]);
    const [selectedTable, setSelectedTable] = useState("");

    useEffect(() => {
        (async () => {
            /*const response = await axios.get("/api/takeChains");
            setChains(response.data);*/
            setChains([{id: 1, name: "Chain 1"}, {id: 2, name: "Chain 2"}, {id: 3, name: "Chain 3"}]);
        })();
    }, [isAuthenticated]); 

    return (isAuthenticated) ? (
        <div>
            <Navbar />
            <div className="page-content">
                <div className="input-card">
                    <input placeholder="Start Query" type="text" name="text" id="query-input" />
                    <div className="selections">
                        <select onChange={(event) => {setSelectedTable(event.target.value);}}>
                            <option value="" disabled selected>Choose Table</option>
                            <option value="addresses">Addresses</option>
                            <option value="blocks">Blocks</option>
                            <option value="chains">Chains</option>
                            <option value="transactions">Transactions</option>
                        </select>                   
                        {selectedTable === "blocks" ? (
                            <select>
                                <option value="" disabled selected>Choose Chain</option>
                                {chains.map((chain) => (
                                    <option value={chain.id}>{chain.name}</option>
                                ))}
                            </select>
                        ) : null}            
                    </div>
                    <div className="operations">
                        <button>INSERT</button>
                        <button>DELETE</button>
                    </div>
                </div>
            </div>
        </div>
    ) : (
        <div>
            <Navbar />
            <div className='page-content'>
                <button className="authentication" onClick={async () => {setIsAuthenticated(true/*await authenticate()*/);}}>Authenticate</button>
            </div>
        </div>
    );
}
import { useState, useEffect } from 'react';
import axios from 'axios';

import authenticate from '../utils/authenticate';
import "../styles/admin.css";

export default function Admin () {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [chains, setChains] = useState([]);
    const [selectedTable, setSelectedTable] = useState("");
    const [primaryKey, setPrimaryKey] = useState([]);
    const [operation, setOperation] = useState("");

    useEffect(() => {
        (async () => {
            const response = await axios.get("/api/takeChains");
            setChains(response.data);
            console.log(chains);
        })();
    }, [isAuthenticated]); 

    return (isAuthenticated) ? (
        <div>
            <form id="dynamicForm">
                <div className="form-group">
                    <label>Text Input:</label>
                    <input type="text" id="textInput" name="textInput" placeholder="Enter some text" />
                </div>

                <div className="form-group">
                    <label>Select Options:</label>
                    <select id="multiSelect" name="multiSelect" onChange={() => {console.log(event.target.value); setSelectedTable(event.target.value); setPrimaryKey([document.getElementById("textInput").value])}} multiple>
                        <option value="addresses">Addresses</option>
                        <option value="blocks">BLocks</option>
                        <option value="chains">Chains</option>
                        <option value="transactions">Transactions</option>
                    </select>
                </div>

                {selectedTable === "blocks" ? (<div className="form-group" id="extraSelectContainer">
                    <label>Additional Options:</label>
                    <select id="extraSelect" name="extraSelect" multiple onChange={() => {console.log(event.target.value); setPrimaryKey([document.getElementById("textInput").value, event.target.value])}}>
                        {chains.map((chain) => (
                            <option value={chain.id}>{chain.name}</option>
                        ))}
                    </select>
                </div>) : null}

                <div className="form-group">
                    <label>Select Options:</label>
                    <select id="opeartion" name="opeartion" onChange={() => {setOperation(event.target.value)}} multiple>
                        <option value="insert">INSERT</option>
                        <option value="delete">DELETE</option>
                    </select>
                </div>

                <button type="submit" onClick={() => {
                    event.preventDefault();
                    console.log(primaryKey, selectedTable, operation);
                }}>Submit</button>
            </form>
        </div>
    ) : (<><button onClick={async () => {setIsAuthenticated(await authenticate());}}>Authenticate</button></>);
}
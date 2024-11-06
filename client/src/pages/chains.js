import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Chains() {
  const [data, setData] = useState([]);

  useEffect(() => {
    console.log("Fetching data from /api/chains...");

    axios.get('/api/chains')
      .then(response => {
        console.log("Data fetched from /api/chains:", response.data);
        setData(response.data);
      })
      .catch(error => {
        console.error("Error fetching table data:", error);
      });
  }, []);

  console.log("Current state of data:", data);  // Logs current state on every render

  return (
    <div>
      <h1>Chains</h1>
      <table>
        <thead>
          <tr>
            <th>chain_id</th>
            <th>chain_name</th>
            <th>native_currency</th>
            <th>total_supply</th>
          </tr>
        </thead>
        <tbody>
          {data.length === 0 ? (
            <tr>
              <td colSpan="4">No data available</td>
            </tr>
          ) : (
            data.map((row, index) => (
              <tr key={index}>
                <td>{row.chain_id}</td>
                <td>{row.chain_name}</td>
                <td>{row.native_currency}</td>
                <td>{row.total_supply}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default Chains;

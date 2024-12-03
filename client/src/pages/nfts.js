import React, { useEffect, useState } from 'react';
import axios from 'axios';

function  NFTs() {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get('/api/NFTs')
      .then(response => setData(response.data))
      .catch(error => console.error("Error fetching table data:", error));
  }, []);

  return (
    <div>
      <h1>NFTs</h1>
      <table>
        <thead>
          <tr>
            
		  	<th>address</th>
            <th>chain_id</th>
            <th>owner</th>
			<th>token_id</th>
			<th>token_uri</th>
			<th>contract_type</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              <td>{row.id}</td>
              <td>{row.name}</td>
              <td>{row.value}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default NFTs;

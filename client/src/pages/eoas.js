import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Table1() {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get('/api/table1')
      .then(response => setData(response.data))
      .catch(error => console.error("Error fetching table data:", error));
  }, []);

  return (
    <div>
      <h1>EOAs</h1>
      <table>
        <thead>
          <tr>
            <th>publicKey</th>
            <th>balance</th>
            <th>erc20Count</th>
			<th>erc20Balance</th>
			<th>nftCount</th>
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

export default Table1;

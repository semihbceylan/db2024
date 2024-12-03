import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <h1>Welcome to the Data Dashboard</h1>
      <p>Select a table to view data:</p>
      <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', marginTop: '20px' }}>
        <Link
          to="/table2"
          style={{
            textDecoration: 'none',
            padding: '10px 20px',
            backgroundColor: '#007BFF',
            color: 'white',
            borderRadius: '5px',
            fontWeight: 'bold',
          }}
        >
          Chains Table
        </Link>
        <Link
          to="/table1"
          style={{
            textDecoration: 'none',
            padding: '10px 20px',
            backgroundColor: '#007BFF',
            color: 'white',
            borderRadius: '5px',
            fontWeight: 'bold',
          }}
        >
          Eoas Table
        </Link>
      </div>
    </div>
  );
}

export default Home;

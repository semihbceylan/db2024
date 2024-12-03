import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Blocks() {
    const [data, setData] = useState([]);
    
    useEffect(() => {
        console.log('Fetching data from /api/blocks...');
        
        axios
        .get('/api/blocks')
        .then(response => {
            console.log('Data fetched from /api/blocks:', response.data);
            setData(response.data);
        })
        .catch(error => {
            console.error('Error fetching table data:', error);
        });
    }, []);
    
    
    console.log('Current state of data:', data);

    return(
        <div>
            <h1>Blokcs</h1>
        </div>
    );

};




export default Blocks;

import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

export default function Table () {
    const {tableName, primaryKey} = useParams();
    const [data, setData] = useState(null);
    
    useEffect(() => {
        (async () => {
            const response = await axios.get(`http://localhost:5001/takeData/${tableName}/${primaryKey}`);
            setData(response.data);
        })();
    }, [primaryKey]);

    if (!data) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <ul>
                {Object.entries(data).map(([key, value]) => (
                  <li key={key}>
                    <strong>{key}:</strong> {value.toString()}
                 </li>
                ))}
            </ul>
        </div>
    );
}
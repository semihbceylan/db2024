import axios from 'axios';
import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';

export default function Table () {
    const { tableName, primaryKey } = useParams();

    const [data, setData] = useState(null);
    
    useEffect(() => {
        (async () => {
            const response = await axios.get(`/api/takeData/${tableName}/${primaryKey}`);
            setData(response.data);
        })();
    }, [primaryKey]);
    
    return (data != null) ? (
        <div>
            <ul>
                {Object.entries(data).map(([key, value]) => (
                  <li key={key}><strong>{key}:</strong> {value.toString()}</li>
                ))}
            </ul>
        </div>
    ) : (<><h1>Loading..</h1></>);
}
import axios from 'axios';
import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';

const TEST_DATA = {
    tableName: "blocks",
    primaryKey: 53565,
    block_number: 2068621,
    chain_id: 1,
    block_hash: "0x1f3211e19dbbfc7cfbd995053ca85a92c6f0b5f01c3fb9275577b1e0dc53cfe7",
    parent_hash: "0x76d520ebc07ad89932eb8f404f2afa30e3e832ff1819102f392f6e083c634cc3",
    miner: "0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8",
    transaction_count: 7,
    timestamp: "2016-08-14 05:30:06"
}

export default function BlockExplorer () {
    const { tableName, primaryKey } = useParams();

    const [data, setData] = useState(null);
    
    useEffect(() => {
        (async () => {
            // const response = await axios.get(`/api/takeData/${tableName}/${primaryKey}`);
            // setData(response.data);
            setData(TEST_DATA);
        })();
    }, [primaryKey]);
    
    return (data != null) ? (
        <>
            <Navbar />
            <div>
                <ul>
                    {Object.entries(data).map(([key, value]) => (
                    <li key={key}><strong>{key}:</strong> {value.toString()}</li>
                    ))}
                </ul>
            </div>
        </>
    ) : (<><h1>Loading..</h1></>);
}
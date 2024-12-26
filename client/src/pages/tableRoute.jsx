import { useParams } from 'react-router-dom'
import BlockExplorer from './blockExplorer';

export default function TableRoute () {
    return (["blocks", "transactions", "addresses"].includes(useParams().tableName)) ? <BlockExplorer /> : <><h1>404 - Page Not Found</h1></>;
}
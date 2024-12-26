import { useParams } from 'react-router-dom'
import Table from './table'

export default function TableRoute () {
    return (["blocks", "transactions", "addresses"].includes(useParams().tableName)) ? <Table /> : <><h1>404 - Page Not Found</h1></>;
}
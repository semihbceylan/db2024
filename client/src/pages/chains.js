import React, { useEffect, useState } from "react";
import axios from "axios";

function Chains() {
  const [data, setData] = useState([]);
  const [newRow, setNewRow] = useState({
    chain_id: "",
    chain_name: "",
    native_currency: "",
    total_supply: "",
  });
  const [editingRow, setEditingRow] = useState(null);

  // Base URL for the Flask API
  const API_BASE_URL = "http://192.168.1.106:5001";

  useEffect(() => {
    fetchData();
  }, []);

  // Fetch all chains
  const fetchData = () => {
    axios
      .get(`${API_BASE_URL}/chains`)
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  };

  // Add a new chain
  const addRow = (e) => {
    e.preventDefault();
    axios
      .post(`${API_BASE_URL}/chains`, newRow)
      .then(() => {
        fetchData();
        setNewRow({ chain_id: "", chain_name: "", native_currency: "", total_supply: "" });
      })
      .catch((error) => {
        console.error("Error adding row:", error);
      });
  };

  // Delete a chain by ID
  const deleteRow = (id) => {
    axios
      .delete(`${API_BASE_URL}/chains/${id}`)
      .then(() => {
        fetchData();
      })
      .catch((error) => {
        console.error("Error deleting row:", error);
      });
  };

  // Edit an existing chain
  const saveEdit = (id) => {
    axios
      .put(`${API_BASE_URL}/chains/${id}`, editingRow)
      .then(() => {
        fetchData();
        setEditingRow(null);
      })
      .catch((error) => {
        console.error("Error editing row:", error);
      });
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Chains Table</h1>

      {/* Add New Row Form */}
      <form onSubmit={addRow} style={{ marginBottom: "20px" }}>
        <h3>Add New Chain</h3>
        <input
          type="text"
          placeholder="Chain ID"
          value={newRow.chain_id}
          onChange={(e) => setNewRow({ ...newRow, chain_id: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Chain Name"
          value={newRow.chain_name}
          onChange={(e) => setNewRow({ ...newRow, chain_name: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Native Currency"
          value={newRow.native_currency}
          onChange={(e) => setNewRow({ ...newRow, native_currency: e.target.value })}
          required
        />
        <input
          type="number"
          placeholder="Total Supply"
          value={newRow.total_supply}
          onChange={(e) => setNewRow({ ...newRow, total_supply: e.target.value })}
          required
        />
        <button type="submit">Add Row</button>
      </form>

      {/* Table */}
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ backgroundColor: "#007BFF", color: "white" }}>
            <th style={{ padding: "10px", border: "1px solid #ddd" }}>Chain ID</th>
            <th style={{ padding: "10px", border: "1px solid #ddd" }}>Chain Name</th>
            <th style={{ padding: "10px", border: "1px solid #ddd" }}>Native Currency</th>
            <th style={{ padding: "10px", border: "1px solid #ddd" }}>Total Supply</th>
            <th style={{ padding: "10px", border: "1px solid #ddd" }}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {data.length === 0 ? (
            <tr>
              <td colSpan="5" style={{ textAlign: "center" }}>
                No data available
              </td>
            </tr>
          ) : (
            data.map((row) => (
              <tr key={row.chain_id} style={{ borderBottom: "1px solid #ddd" }}>
                <td style={{ padding: "10px" }}>
                  {editingRow?.chain_id === row.chain_id ? (
                    <input
                      type="text"
                      value={editingRow.chain_id}
                      onChange={(e) => setEditingRow({ ...editingRow, chain_id: e.target.value })}
                    />
                  ) : (
                    row.chain_id
                  )}
                </td>
                <td style={{ padding: "10px" }}>
                  {editingRow?.chain_id === row.chain_id ? (
                    <input
                      type="text"
                      value={editingRow.chain_name}
                      onChange={(e) => setEditingRow({ ...editingRow, chain_name: e.target.value })}
                    />
                  ) : (
                    row.chain_name
                  )}
                </td>
                <td style={{ padding: "10px" }}>
                  {editingRow?.chain_id === row.chain_id ? (
                    <input
                      type="text"
                      value={editingRow.native_currency}
                      onChange={(e) => setEditingRow({ ...editingRow, native_currency: e.target.value })}
                    />
                  ) : (
                    row.native_currency
                  )}
                </td>
                <td style={{ padding: "10px" }}>
                  {editingRow?.chain_id === row.chain_id ? (
                    <input
                      type="number"
                      value={editingRow.total_supply}
                      onChange={(e) => setEditingRow({ ...editingRow, total_supply: e.target.value })}
                    />
                  ) : (
                    row.total_supply
                  )}
                </td>
                <td style={{ padding: "10px" }}>
                  {editingRow?.chain_id === row.chain_id ? (
                    <button onClick={() => saveEdit(row.chain_id)}>Save</button>
                  ) : (
                    <>
                      <button onClick={() => setEditingRow(row)}>Edit</button>
                      <button onClick={() => deleteRow(row.chain_id)}>Delete</button>
                    </>
                  )}
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default Chains;

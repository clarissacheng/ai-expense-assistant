import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const api = axios.create({
  // When developing, CRA dev server proxies API requests to backend at /.
  // Use REACT_APP_API_BASE_URL to override in production builds.
  baseURL: process.env.REACT_APP_API_BASE_URL || "",
  withCredentials: true,
});

function App() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [summary, setSummary] = useState([]);
  const [categorySummary, setCategorySummary] = useState({});
  const [receipts, setReceipts] = useState([]);
  const [receiptId, setReceiptId] = useState(null);
  const [user, setUser] = useState(null);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    checkAuth();
  }, []);

  useEffect(() => {
    if (user) {
      refreshAll();
    }
  }, [user]);

  const checkAuth = async () => {
    try {
      const res = await api.get("/me/");
      setUser(res.data);
    } catch {
      setUser(null);
    }
  };

  const refreshAll = async () => {
    try {
      const res1 = await api.get("/summary/");
      setSummary(res1.data);

      const res2 = await api.get("/category_summary/");
      setCategorySummary(res2.data || {});

      const res3 = await api.get("/receipts/");
      setReceipts(res3.data || []);
    } catch (err) {
      console.error(err);
    }
  };

  const handleUpload = async () => {
    if (!user) {
      setMessage("Please login first.");
      return;
    }
    if (!file) {
      setMessage("Please choose a receipt image.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const res = await api.post("/upload/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    setData(res.data.data);
    setReceiptId(res.data.receipt_id);
    setMessage(`Receipt extracted. Estimated API cost: $${res.data.estimated_cost.toFixed(2)}`);
  };

  const handleChange = (field, value) => {
    setData({ ...data, [field]: value });
  };

  const handleSubmit = async () => {
    if (!receiptId) {
      setMessage("Upload a receipt before saving corrections.");
      return;
    }

    await api.put(`/receipt/${receiptId}`, data);
    await refreshAll();
    setReceiptId(null);
    setData(null);
    setFile(null);
    setMessage("Saved!");
  };

  const updateItem = (index, field, value) => {
    const updatedItems = [...(data.items || [])];
    updatedItems[index] = {
      ...updatedItems[index],
      [field]: value,
    };

    setData({
      ...data,
      items: updatedItems,
    });
  };

  const handleLogin = async () => {
    try {
      const res = await api.post("/login/", {
        username,
        password,
      });
      setUsername("");
      setPassword("");
      // try to use returned user info or fallback to /me/
      if (res.data && res.data.user) {
        setUser(res.data.user);
      } else {
        await checkAuth();
      }
      setMessage("Logged in.");
    } catch {
      setMessage("Invalid login.");
    }
  };

  const handleRegister = async () => {
    try {
      await api.post("/register/", {
        username,
        password,
      });
      setMessage("Registered successfully. Please log in.");
    } catch (error) {
      setMessage(error?.response?.data?.detail || "Registration failed.");
    }
  };

  const handleLogout = async () => {
    await api.post("/logout/");
    setUser(null);
    setData(null);
    setReceiptId(null);
    setSummary([]);
    setCategorySummary({});
    setReceipts([]);
    setMessage("Logged out.");
  };

  const chartData = summary.map((s) => ({
    store: s.store,
    total: Number(s.total),
  }));

  if (!user) {
    return (
      <div style={{ padding: 30, fontFamily: "Arial, sans-serif" }}>
        <h2>Login / Register</h2>
        <div style={card}>
          <input
            style={input}
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            style={input}
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button style={button} onClick={handleLogin}>
            Login
          </button>
          <button style={{ ...button, background: "#2196F3" }} onClick={handleRegister}>
            Register
          </button>
          {message && <p>{message}</p>}
        </div>
      </div>
    );
  }

  return (
    <div style={{ padding: "30px", fontFamily: "Arial, sans-serif", background: "#f5f6fa" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1>🧾 AI Expense Assistant</h1>
        <div>
          <span style={{ marginRight: 16 }}>User: {user.username}</span>
          <button style={{ ...button, background: "#f44336" }} onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>

      <div style={card}>
        <h2>Upload Receipt</h2>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button style={button} onClick={handleUpload}>
          Upload Receipt
        </button>
      </div>

      {data && (
        <div style={card}>
          <h2>Edit Extracted Data</h2>
          <label>Store Name</label>
          <input
            style={input}
            value={data.store_name || ""}
            onChange={(e) => handleChange("store_name", e.target.value)}
          />
          <label>Date</label>
          <input
            style={input}
            value={data.date || ""}
            onChange={(e) => handleChange("date", e.target.value)}
          />
          <label>Total</label>
          <input
            style={input}
            value={data.total || ""}
            onChange={(e) => handleChange("total", e.target.value)}
          />
          <h3>Items</h3>
          {(data.items || []).map((item, i) => (
            <div key={i} style={itemRow}>
              <input
                style={input}
                value={item.name}
                onChange={(e) => updateItem(i, "name", e.target.value)}
              />
              <input
                style={input}
                value={item.unit_price}
                onChange={(e) => updateItem(i, "unit_price", e.target.value)}
              />
              <input
                style={input}
                placeholder="Category"
                value={item.category || ""}
                onChange={(e) => updateItem(i, "category", e.target.value)}
              />
              <div style={{ fontSize: 12 }}>
                Qty: {item.quantity} | Total: ${item.total_price}
              </div>
            </div>
          ))}
          <button style={button} onClick={handleSubmit}>
            Save Corrections
          </button>
        </div>
      )}

      {(receipts.length > 0 || Object.keys(categorySummary).length > 0) && (
        <div style={grid}>
          <div style={column}>
            <div style={card}>
              <h3>Receipt History</h3>
              {receipts.length === 0 ? (
                <p>No receipts saved yet.</p>
              ) : (
                receipts.map((r) => (
                  <div key={r.id} style={historyItem}>
                    <b>{r.store_name}</b>
                    <div>${r.total}</div>
                    <div style={{ fontSize: 12 }}>{r.date}</div>
                  </div>
                ))
              )}
            </div>
          </div>

          <div style={column}>
            <div style={card}>
              <h3>Total Spending by Store</h3>
              {summary.map((item, i) => (
                <div key={i} style={summaryRow}>
                  <span>{item.store}</span>
                  <span>${item.total}</span>
                </div>
              ))}
            </div>

            <div style={card}>
              <h3>Spending Dashboard</h3>
              <div style={{ width: "100%", height: 250 }}>
                <ResponsiveContainer>
                  <BarChart data={chartData}>
                    <XAxis dataKey="store" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="total" fill="#4CAF50" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div style={card}>
              <h3>Spending by Category</h3>
              {Object.entries(categorySummary || {}).map(([cat, total]) => (
                <div key={cat} style={summaryRow}>
                  <span>{cat}</span>
                  <span>${total.toFixed(2)}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const grid = {
  display: "grid",
  gridTemplateColumns: "1fr 1fr",
  gap: "20px",
  marginTop: "20px",
};

const column = {
  display: "flex",
  flexDirection: "column",
  gap: "20px",
};

const card = {
  background: "white",
  padding: "20px",
  borderRadius: "12px",
  boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
};

const input = {
  width: "100%",
  padding: "8px",
  marginBottom: "10px",
  borderRadius: "6px",
  border: "1px solid #ccc",
};

const button = {
  marginTop: "10px",
  padding: "10px 15px",
  borderRadius: "8px",
  border: "none",
  background: "#4CAF50",
  color: "white",
  cursor: "pointer",
};

const itemRow = {
  marginBottom: "10px",
  padding: "10px",
  border: "1px solid #eee",
  borderRadius: "8px",
};

const historyItem = {
  padding: "10px",
  borderBottom: "1px solid #eee",
};

const summaryRow = {
  display: "flex",
  justifyContent: "space-between",
  padding: "5px 0",
};

export default App;

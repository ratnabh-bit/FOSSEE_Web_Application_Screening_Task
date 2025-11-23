import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, LineElement, PointElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import { Bar, Line, Pie } from 'react-chartjs-2';
import './App.css';

ChartJS.register(CategoryScale, LinearScale, BarElement, LineElement, PointElement, Title, Tooltip, Legend, ArcElement);

const API_BASE = 'http://localhost:8000/api';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [isRegistering, setIsRegistering] = useState(false);
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    if (token) {
      fetchDatasets();
    }
  }, [token]);

  const showMessage = (msg, isError = false) => {
    setMessage(msg);
    setTimeout(() => setMessage(''), 5000);
  };

  const handleAuth = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const endpoint = isRegistering ? '/register/' : '/login/';
      const data = isRegistering ? { username, password, email } : { username, password };
      const response = await axios.post(`${API_BASE}${endpoint}`, data);
      localStorage.setItem('token', response.data.token);
      setToken(response.data.token);
      showMessage(`${isRegistering ? 'Registered' : 'Logged in'} successfully!`);
    } catch (error) {
      showMessage(error.response?.data?.error || 'Authentication failed', true);
    }
    setLoading(false);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setDatasets([]);
    setSelectedDataset(null);
  };

  const fetchDatasets = async () => {
    try {
      const response = await axios.get(`${API_BASE}/datasets/`, {
        headers: { Authorization: `Token ${token}` }
      });
      setDatasets(response.data);
    } catch (error) {
      showMessage('Failed to fetch datasets', true);
    }
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      showMessage('Please select a file', true);
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post(`${API_BASE}/upload/`, formData, {
        headers: {
          Authorization: `Token ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      });
      showMessage('File uploaded successfully!');
      setFile(null);
      fetchDatasets();
    } catch (error) {
      showMessage(error.response?.data?.error || 'Upload failed', true);
    }
    setLoading(false);
  };

  const viewDataset = async (datasetId) => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE}/datasets/${datasetId}/`, {
        headers: { Authorization: `Token ${token}` }
      });
      setSelectedDataset(response.data);
    } catch (error) {
      showMessage('Failed to load dataset', true);
    }
    setLoading(false);
  };

  const downloadPDF = async (datasetId, filename) => {
    try {
      const response = await axios.get(`${API_BASE}/datasets/${datasetId}/pdf/`, {
        headers: { Authorization: `Token ${token}` },
        responseType: 'blob'
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `report_${filename}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      showMessage('PDF downloaded successfully!');
    } catch (error) {
      showMessage('Failed to download PDF', true);
    }
  };

  const deleteDataset = async (datasetId) => {
    if (!window.confirm('Are you sure you want to delete this dataset?')) return;
    
    try {
      await axios.delete(`${API_BASE}/datasets/${datasetId}/delete/`, {
        headers: { Authorization: `Token ${token}` }
      });
      showMessage('Dataset deleted successfully!');
      fetchDatasets();
      if (selectedDataset?.id === datasetId) {
        setSelectedDataset(null);
      }
    } catch (error) {
      showMessage('Failed to delete dataset', true);
    }
  };

  if (!token) {
    return (
      <div className="App">
        <div className="auth-container">
          <h1>Chemical Equipment Visualizer</h1>
          <form onSubmit={handleAuth} className="auth-form">
            <h2>{isRegistering ? 'Register' : 'Login'}</h2>
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            {isRegistering && (
              <input
                type="email"
                placeholder="Email (optional)"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            )}
            <button type="submit" disabled={loading}>
              {loading ? 'Processing...' : (isRegistering ? 'Register' : 'Login')}
            </button>
            <p>
              {isRegistering ? 'Already have an account?' : "Don't have an account?"}
              <button type="button" onClick={() => setIsRegistering(!isRegistering)} className="link-button">
                {isRegistering ? 'Login' : 'Register'}
              </button>
            </p>
          </form>
          {message && <div className={`message ${message.includes('fail') ? 'error' : ''}`}>{message}</div>}
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <header>
        <h1>Chemical Equipment Visualizer</h1>
        <button onClick={handleLogout} className="logout-btn">Logout</button>
      </header>

      {message && <div className={`message ${message.includes('fail') ? 'error' : ''}`}>{message}</div>}

      <div className="main-container">
        <div className="upload-section">
          <h2>Upload CSV</h2>
          <form onSubmit={handleUpload}>
            <input type="file" accept=".csv" onChange={handleFileChange} />
            <button type="submit" disabled={loading || !file}>
              {loading ? 'Uploading...' : 'Upload'}
            </button>
          </form>
        </div>

        <div className="datasets-section">
          <h2>Dataset History (Last 5)</h2>
          {datasets.length === 0 ? (
            <p>No datasets uploaded yet.</p>
          ) : (
            <div className="datasets-list">
              {datasets.map(dataset => (
                <div key={dataset.id} className="dataset-card">
                  <h3>{dataset.filename}</h3>
                  <p>Uploaded: {new Date(dataset.uploaded_at).toLocaleString()}</p>
                  <p>Total Equipment: {dataset.total_count}</p>
                  <div className="dataset-actions">
                    <button onClick={() => viewDataset(dataset.id)}>View Details</button>
                    <button onClick={() => downloadPDF(dataset.id, dataset.filename)}>Download PDF</button>
                    <button onClick={() => deleteDataset(dataset.id)} className="delete-btn">Delete</button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {selectedDataset && (
          <div className="details-section">
            <h2>Dataset Details: {selectedDataset.filename}</h2>
            
            <div className="summary-stats">
              <div className="stat-card">
                <h3>Total Count</h3>
                <p>{selectedDataset.total_count}</p>
              </div>
              <div className="stat-card">
                <h3>Avg Flowrate</h3>
                <p>{selectedDataset.avg_flowrate.toFixed(2)}</p>
              </div>
              <div className="stat-card">
                <h3>Avg Pressure</h3>
                <p>{selectedDataset.avg_pressure.toFixed(2)}</p>
              </div>
              <div className="stat-card">
                <h3>Avg Temperature</h3>
                <p>{selectedDataset.avg_temperature.toFixed(2)}</p>
              </div>
            </div>

            <div className="charts-container">
              <div className="chart">
                <h3>Equipment Type Distribution</h3>
                <Pie data={{
                  labels: Object.keys(selectedDataset.equipment_type_distribution),
                  datasets: [{
                    data: Object.values(selectedDataset.equipment_type_distribution),
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
                  }]
                }} />
              </div>

              <div className="chart">
                <h3>Average Parameters</h3>
                <Bar data={{
                  labels: ['Flowrate', 'Pressure', 'Temperature'],
                  datasets: [{
                    label: 'Average Values',
                    data: [selectedDataset.avg_flowrate, selectedDataset.avg_pressure, selectedDataset.avg_temperature],
                    backgroundColor: ['#36A2EB', '#FF6384', '#FFCE56']
                  }]
                }} />
              </div>
            </div>

            <div className="equipment-table">
              <h3>Equipment List</h3>
              <table>
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Flowrate</th>
                    <th>Pressure</th>
                    <th>Temperature</th>
                  </tr>
                </thead>
                <tbody>
                  {selectedDataset.equipment.map(eq => (
                    <tr key={eq.id}>
                      <td>{eq.equipment_name}</td>
                      <td>{eq.equipment_type}</td>
                      <td>{eq.flowrate.toFixed(1)}</td>
                      <td>{eq.pressure.toFixed(1)}</td>
                      <td>{eq.temperature.toFixed(1)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
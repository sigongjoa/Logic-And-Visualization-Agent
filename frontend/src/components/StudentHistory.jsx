import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // FastAPI backend URL

function StudentHistory() {
  const [studentId, setStudentId] = useState('std_kimminjun'); // Default student ID
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchHistory = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`${API_BASE_URL}/students/${studentId}/vector-history`);
      setHistory(response.data);
    } catch (err) {
      setError('Failed to fetch student history. Please ensure the backend is running and the student ID is valid.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [studentId]); // Refetch when studentId changes

  return (
    <div className="student-history">
      <h2>Student 4-Axis Model History</h2>
      <div className="input-group">
        <label htmlFor="studentId">Student ID:</label>
        <input
          type="text"
          id="studentId"
          value={studentId}
          onChange={(e) => setStudentId(e.target.value)}
          placeholder="Enter Student ID"
        />
        <button onClick={fetchHistory}>Fetch History</button>
      </div>

      {loading && <p>Loading history...</p>}
      {error && <p className="error">{error}</p>}

      {history.length > 0 ? (
        <div className="history-list">
          {history.map((entry, index) => (
            <div key={index} className="history-entry card">
              <h3>Entry ID: {entry.vector_id}</h3>
              <p><strong>Assessment ID:</strong> {entry.assessment_id}</p>
              <p><strong>Created At:</strong> {new Date(entry.created_at).toLocaleString()}</p>
              <div className="axes-data">
                <h4>Axis Scores:</h4>
                <ul>
                  <li>Axis 1 (Geo/Alg/Ana): {entry.axis1_geo} / {entry.axis1_alg} / {entry.axis1_ana}</li>
                  <li>Axis 2 (Opt/Piv/Dia): {entry.axis2_opt} / {entry.axis2_piv} / {entry.axis2_dia}</li>
                  <li>Axis 3 (Con/Pro/Ret): {entry.axis3_con} / {entry.axis3_pro} / {entry.axis3_ret}</li>
                  <li>Axis 4 (Acc/Gri): {entry.axis4_acc} / {entry.axis4_gri}</li>
                </ul>
              </div>
            </div>
          ))}
        </div>
      ) : (
        !loading && !error && <p>No history found for this student.</p>
      )}
    </div>
  );
}

export default StudentHistory;

import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const API_BASE_URL = 'http://localhost:8000'; // FastAPI backend URL

function SubmissionForm() {
  const [studentId, setStudentId] = useState('');
  const [problemText, setProblemText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/submissions`, {
        student_id: studentId,
        problem_text: problemText,
      });
      navigate('/submission-result', { state: { result: response.data } });
    } catch (err) {
      setError('Failed to submit problem. Please ensure the backend is running and inputs are valid.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="submission-form">
      <h2>Submit a Problem</h2>
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <label htmlFor="studentId">Student ID:</label>
          <input
            type="text"
            id="studentId"
            value={studentId}
            onChange={(e) => setStudentId(e.target.value)}
            placeholder="Enter Student ID (e.g., std_kimminjun)"
            required
          />
        </div>
        <div className="input-group">
          <label htmlFor="problemText">Problem Description:</label>
          <textarea
            id="problemText"
            value={problemText}
            onChange={(e) => setProblemText(e.target.value)}
            placeholder="Describe the problem (e.g., 이차함수와 그래프에 대해 설명하시오.)"
            rows="5"
            required
          ></textarea>
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Submitting...' : 'Submit Problem'}
        </button>
        {error && <p className="error">{error}</p>}
      </form>
    </div>
  );
}

export default SubmissionForm;

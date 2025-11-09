import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createSubmission } from '../api'; // Assuming api.js has createSubmission

function SubmissionForm() {
  const [studentId, setStudentId] = useState('');
  const [problemText, setProblemText] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null); // Clear previous errors

    try {
      const submissionData = { student_id: studentId, problem_text: problemText };
      const result = await createSubmission(submissionData);
      navigate('/submission-result', { state: { result } });
    } catch (err) {
      setError(err.message || 'An error occurred during submission.');
      console.error('Submission error:', err);
    }
  };

  return (
    <div className="submission-form-container">
      <h2>Submit a Problem</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="studentId">Student ID:</label>
          <input
            type="text"
            id="studentId"
            value={studentId}
            onChange={(e) => setStudentId(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="problemText">Problem Text:</label>
          <textarea
            id="problemText"
            value={problemText}
            onChange={(e) => setProblemText(e.target.value)}
            rows="5"
            required
          ></textarea>
        </div>
        <button type="submit">Submit</button>
      </form>
      {error && <p className="error-message">{error}</p>}
    </div>
  );
}

export default SubmissionForm;
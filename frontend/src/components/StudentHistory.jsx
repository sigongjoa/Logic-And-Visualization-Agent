import React, { useState, useEffect } from 'react';
import { getStudentSubmissions, getStudentAnkiCards, getStudentMastery } from '../api';

  const [studentId, setStudentId] = useState('std_kimminjun'); // Default student ID
  const [history, setHistory] = useState([]);
  const [submissions, setSubmissions] = useState([]); // New state for submissions
  const [ankiCards, setAnkiCards] = useState([]); // New state for Anki cards
  const [mastery, setMastery] = useState([]); // New state for student mastery
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchHistory = async () => {
    setLoading(true);
    setError(null);
    try {
      // Fetch vector history
      const historyResponse = await fetch(`http://localhost:8000/students/${studentId}/vector-history`);
      if (!historyResponse.ok) {
        throw new Error(`Failed to fetch vector history: ${historyResponse.statusText}`);
      }
      const historyData = await historyResponse.json();
      setHistory(historyData);

      // Fetch submissions
      const submissionsData = await getStudentSubmissions(studentId);
      setSubmissions(submissionsData);

      // Fetch Anki cards
      const ankiCardsData = await getStudentAnkiCards(studentId);
      setAnkiCards(ankiCardsData);

      // Fetch student mastery
      const masteryData = await getStudentMastery(studentId);
      setMastery(masteryData);

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
          <h3>Vector History:</h3>
          {history.map((entry, index) => (
            <div key={entry.vector_id || index} className="history-entry card">
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
        !loading && !error && <p>No vector history found for this student.</p>
      )}

      {submissions.length > 0 ? (
        <div className="submissions-list">
          <h3>Submissions:</h3>
          {submissions.map((submission, index) => (
            <div key={submission.submission_id || index} className="submission-entry card">
              <p><strong>Problem:</strong> {submission.problem_text}</p>
              <p><strong>Concept:</strong> {submission.concept_id}</p>
              <p><strong>Logical Path:</strong> {submission.logical_path_text}</p>
              <p><strong>Manim Video:</strong> <a href={submission.manim_data_path} target="_blank" rel="noopener noreferrer">Watch Video</a></p>
              <p><strong>Submitted At:</strong> {new Date(submission.created_at).toLocaleString()}</p>
            </div>
          ))}
        </div>
      ) : (
        !loading && !error && <p>No submissions found for this student.</p>
      )}

      {ankiCards.length > 0 ? (
        <div className="anki-cards-list">
          <h3>Anki Cards:</h3>
          {ankiCards.map((card, index) => (
            <div key={card.card_id || index} className="anki-card-entry card">
              <p><strong>Question:</strong> {card.question}</p>
              <p><strong>Answer:</strong> {card.answer}</p>
              <p><strong>Next Review:</strong> {new Date(card.next_review_date).toLocaleDateString()}</p>
            </div>
          ))}
        </div>
      ) : (
        !loading && !error && <p>No Anki cards found for this student.</p>
      )}

      {mastery.length > 0 ? (
        <div className="mastery-list">
          <h3>Concept Mastery:</h3>
          {mastery.map((entry, index) => (
            <div key={entry.concept_id || index} className="mastery-entry card">
              <p><strong>Concept ID:</strong> {entry.concept_id}</p>
              <p><strong>Mastery Score:</strong> {entry.mastery_score}</p>
              <p><strong>Status:</strong> {entry.status}</p>
              <p><strong>Last Updated:</strong> {new Date(entry.last_updated).toLocaleString()}</p>
            </div>
          ))}
        </div>
      ) : (
        !loading && !error && <p>No concept mastery data found for this student.</p>
      )}
    </div>
  );
}

export default StudentHistory;

import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // FastAPI backend URL

function StudentHistory() {
  const [studentId, setStudentId] = useState('std_kimminjun'); // Default student ID
  const [history, setHistory] = useState([]);
  const [submissions, setSubmissions] = useState([]); // New state for submissions
  const [ankiCards, setAnkiCards] = useState([]); // New state for Anki cards
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchHistory = async () => {
    setLoading(true);
    setError(null);
    try {
      // Fetch vector history
      const historyResponse = await axios.get(`${API_BASE_URL}/students/${studentId}/vector-history`);
      setHistory(historyResponse.data);

      // Simulate fetching submissions (will need a real API endpoint)
      const submissionsResponse = {
        data: [
          {
            submission_id: 'sub_123',
            problem_text: '이차함수와 그래프 문제',
            concept_id: 'C_이차함수',
            logical_path_text: 'LLM analysis: The problem is about quadratic functions. Key steps involve identifying the vertex, roots, and graph properties.',
            manim_data_path: 'https://youtube.com/watch?v=quadratic_function_manim',
            created_at: new Date().toISOString(),
          },
          {
            submission_id: 'sub_456',
            problem_text: '피타고라스의 정리 활용',
            concept_id: 'C_피타고라스',
            logical_path_text: 'LLM analysis: The problem applies the Pythagorean theorem. Focus on identifying right triangles and side lengths.',
            manim_data_path: 'https://youtube.com/watch?v=pythagorean_theorem_manim',
            created_at: new Date().toISOString(),
          },
        ],
      };
      setSubmissions(submissionsResponse.data);

      // Simulate fetching Anki cards (will need a real API endpoint)
      const ankiCardsResponse = {
        data: [
          {
            card_id: 1,
            question: 'What is the key concept related to "이차함수와 그래프 문제"?',
            answer: 'The problem is primarily about "C_이차함수" and its logical path is: LLM analysis: The problem is about quadratic functions. Key steps involve identifying the vertex, roots, and graph properties.',
            next_review_date: new Date(new Date().setDate(new Date().getDate() + 1)).toISOString(),
          },
          {
            card_id: 2,
            question: 'What is the key concept related to "피타고라스의 정리 활용"?',
            answer: 'The problem is primarily about "C_피타고라스" and its logical path is: LLM analysis: The problem applies the Pythagorean theorem. Focus on identifying right triangles and side lengths.',
            next_review_date: new Date(new Date().setDate(new Date().getDate() + 2)).toISOString(),
          },
        ],
      };
      setAnkiCards(ankiCardsResponse.data);

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
    </div>
  );
}

export default StudentHistory;

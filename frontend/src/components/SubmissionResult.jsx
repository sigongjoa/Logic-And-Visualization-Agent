import React from 'react';
import { useLocation, Link } from 'react-router-dom';

function SubmissionResult() {
  const location = useLocation();
  const { result } = location.state || {};

  if (!result) {
    return (
      <div className="submission-result">
        <h2>No Submission Result Available</h2>
        <p>Please submit a problem first.</p>
        <Link to="/submit">Go to Submission Form</Link>
      </div>
    );
  }

  return (
    <div className="submission-result">
      <h2>Submission Successful!</h2>
      <div className="card">
        <h3>Submission ID: {result.submission_id}</h3>
        <p><strong>Status:</strong> {result.status}</p>
        <p><strong>Logical Path Text:</strong> {result.logical_path_text}</p>
        <p><strong>Concept ID:</strong> {result.concept_id}</p>
        {result.manim_content_url && (
          <p>
            <strong>Manim Content:</strong>{' '}
            <a href={result.manim_content_url} target="_blank" rel="noopener noreferrer">
              Watch Video
            </a>
          </p>
        )}
      </div>
      <Link to="/submit">Submit another problem</Link>
      <Link to="/history">View Student History</Link>
    </div>
  );
}

export default SubmissionResult;

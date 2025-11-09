import React from 'react';
import { useLocation } from 'react-router-dom';

function SubmissionResult() {
  const location = useLocation();
  const { result } = location.state || {};

  if (!result) {
    return (
      <div className="submission-result-container">
        <h2>No Submission Result Available</h2>
        <p>Please submit a problem first.</p>
      </div>
    );
  }

  return (
    <div className="submission-result-container">
      <h2>Submission Result</h2>
      <p><strong>Submission ID:</strong> {result.submission_id}</p>
      <p><strong>Status:</strong> {result.status}</p>
      <div className="logical-path">
        <h3>Logical Path Analysis:</h3>
        <p>{result.logical_path_text}</p>
      </div>
      <div className="manim-content">
        <h3>Manim Content:</h3>
        {result.manim_content_url ? (
          <p>View Manim animation: <a href={result.manim_content_url} target="_blank" rel="noopener noreferrer">{result.manim_content_url}</a></p>
        ) : (
          <p>No Manim content available for this submission.</p>
        )}
      </div>
    </div>
  );
}

export default SubmissionResult;
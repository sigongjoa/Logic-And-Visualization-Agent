import React, { useState, useEffect } from 'react';
import { getDraftReports } from '../api';

function CoachReportReview() {
  const [draftReports, setDraftReports] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDraftReports = async () => {
      setLoading(true);
      setError(null);
      try {
        const reports = await getDraftReports();
        setDraftReports(reports);
      } catch (err) {
        setError('Failed to fetch draft reports. Please ensure the backend is running.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchDraftReports();
  }, []);

  if (loading) {
    return <p>Loading draft reports...</p>;
  }

  if (error) {
    return <p className="error">{error}</p>;
  }

  return (
    <div className="coach-report-review">
      <h2>Draft Weekly Reports</h2>
      {draftReports.length === 0 ? (
        <p>No draft reports available.</p>
      ) : (
        <div className="report-list">
          {draftReports.map((report) => (
            <div key={report.report_id} className="report-card card">
              <h3>Report ID: {report.report_id}</h3>
              <p><strong>Student ID:</strong> {report.student_id}</p>
              <p><strong>Period:</strong> {new Date(report.period_start).toLocaleDateString()} - {new Date(report.period_end).toLocaleDateString()}</p>
              <p><strong>Status:</strong> {report.status}</p>
              {/* More details will be added here later */}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default CoachReportReview;
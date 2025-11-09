import React, { useState, useEffect } from 'react';
import { getDraftReports, getReportDetails, finalizeReport, sendReport } from '../api';

function CoachReportReview() {
  const [draftReports, setDraftReports] = useState([]);
  const [selectedReport, setSelectedReport] = useState(null);
  const [coachComment, setCoachComment] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [actionMessage, setActionMessage] = useState(null); // For success/error messages after actions

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

  useEffect(() => {
    fetchDraftReports();
  }, []);

  const handleReportClick = async (reportId) => {
    setLoading(true);
    setError(null);
    setActionMessage(null);
    try {
      const details = await getReportDetails(reportId);
      setSelectedReport(details);
      setCoachComment(details.coach_comment || ''); // Pre-fill if comment exists
    } catch (err) {
      setError(`Failed to fetch report details for report ${reportId}.`);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleFinalizeReport = async () => {
    if (!selectedReport) return;
    setLoading(true);
    setError(null);
    setActionMessage(null);
    try {
      await finalizeReport(selectedReport.report_id, coachComment);
      setActionMessage('Report finalized successfully!');
      setSelectedReport(null); // Clear selected report
      setCoachComment('');
      fetchDraftReports(); // Refresh the list of draft reports
    } catch (err) {
      setError(`Failed to finalize report ${selectedReport.report_id}.`);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSendReport = async () => {
    if (!selectedReport) return;
    setLoading(true);
    setError(null);
    setActionMessage(null);
    try {
      await sendReport(selectedReport.report_id);
      setActionMessage('Report sent successfully!');
      setSelectedReport(null); // Clear selected report
      setCoachComment('');
      fetchDraftReports(); // Refresh the list of draft reports
    } catch (err) {
      setError(`Failed to send report ${selectedReport.report_id}.`);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <p>Loading reports...</p>;
  }

  if (error) {
    return <p className="error">{error}</p>;
  }

  return (
    <div className="coach-report-review">
      <h2>Coach Report Review</h2>
      {actionMessage && <p className="success-message">{actionMessage}</p>}

      {selectedReport ? (
        <div className="report-detail card">
          <button onClick={() => setSelectedReport(null)}>Back to Drafts</button>
          <h3>Report ID: {selectedReport.report_id}</h3>
          <p><strong>Student ID:</strong> {selectedReport.student_id}</p>
          <p><strong>Period:</strong> {new Date(selectedReport.period_start).toLocaleDateString()} - {new Date(selectedReport.period_end).toLocaleDateString()}</p>
          <p><strong>Status:</strong> {selectedReport.status}</p>
          
          <h4>AI Summary:</h4>
          <pre>{selectedReport.ai_summary}</pre> {/* Use pre for pre-formatted text */}

          <h4>Coach Comment:</h4>
          <textarea
            value={coachComment}
            onChange={(e) => setCoachComment(e.target.value)}
            placeholder="Add your comments here..."
            rows="5"
            cols="50"
          ></textarea>
          <br />
          <button onClick={handleFinalizeReport} disabled={selectedReport.status === 'FINALIZED' || selectedReport.status === 'SENT'}>
            Finalize Report
          </button>
          <button onClick={handleSendReport} disabled={selectedReport.status !== 'FINALIZED'}>
            Send Report
          </button>
        </div>
      ) : (
        draftReports.length === 0 ? (
          <p>No draft reports available.</p>
        ) : (
          <div className="report-list">
            <h3>Draft Weekly Reports:</h3>
            {draftReports.map((report) => (
              <div key={report.report_id} className="report-card card" onClick={() => handleReportClick(report.report_id)}>
                <h3>Report ID: {report.report_id}</h3>
                <p><strong>Student ID:</strong> {report.student_id}</p>
                <p><strong>Period:</strong> {new Date(report.period_start).toLocaleDateString()} - {new Date(report.period_end).toLocaleDateString()}</p>
                <p><strong>Status:</strong> {report.status}</p>
                <p className="click-hint">(Click for details)</p>
              </div>
            ))}
          </div>
        )
      )}
    </div>
  );
}

export default CoachReportReview;
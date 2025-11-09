import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getStudentReports, getStudentLatestVector, getStudentSubmissions } from '../api';

const StudentDetail = () => {
  const { studentId } = useParams();
  const [reports, setReports] = useState([]);
  const [latestVector, setLatestVector] = useState(null);
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [reportsData, latestVectorData, submissionsData] = await Promise.all([
          getStudentReports(studentId),
          getStudentLatestVector(studentId),
          getStudentSubmissions(studentId),
        ]);
        setReports(reportsData);
        setLatestVector(latestVectorData);
        setSubmissions(submissionsData);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [studentId]);

  if (loading) {
    return <div className="student-detail-container">Loading student details...</div>;
  }

  if (error) {
    return <div className="student-detail-container">Error: {error.message}</div>;
  }

  return (
    <div className="student-detail-container">
      <h2>Student Details: {studentId}</h2>

      <h3>Latest Vector</h3>
      {latestVector ? (
        <div className="vector-data">
          <p>Vector ID: {latestVector.vector_id}</p>
          <p>Axis 1 (Geo, Alg, Ana): {latestVector.axis1_geo}, {latestVector.axis1_alg}, {latestVector.axis1_ana}</p>
          <p>Axis 2 (Opt, Piv, Dia): {latestVector.axis2_opt}, {latestVector.axis2_piv}, {latestVector.axis2_dia}</p>
          <p>Axis 3 (Con, Pro, Ret): {latestVector.axis3_con}, {latestVector.axis3_pro}, {latestVector.axis3_ret}</p>
          <p>Axis 4 (Acc, Gri): {latestVector.axis4_acc}, {latestVector.axis4_gri}</p>
        </div>
      ) : (
        <p>No latest vector data available.</p>
      )}

      <h3>Weekly Reports</h3>
      {reports.length > 0 ? (
        <ul className="report-list">
          {reports.map((report) => (
            <li key={report.report_id} className="report-list-item">
              <h4>Report ID: {report.report_id}</h4>
              <p>Period: {new Date(report.period_start).toLocaleDateString()} - {new Date(report.period_end).toLocaleDateString()}</p>
              <p>Status: {report.status}</p>
              <p>AI Summary: {report.ai_summary}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>No weekly reports available.</p>
      )}

      <h3>Submissions</h3>
      {submissions.length > 0 ? (
        <ul className="submission-list">
          {submissions.map((submission) => (
            <li key={submission.submission_id} className="submission-list-item">
              <h4>Submission ID: {submission.submission_id}</h4>
              <p>Status: {submission.status}</p>
              <p>Logical Path: {submission.logical_path_text}</p>
              <p>Concept ID: {submission.concept_id}</p>
              <p>Manim Content URL: <a href={submission.manim_content_url} target="_blank" rel="noopener noreferrer">{submission.manim_content_url}</a></p>
            </li>
          ))}
        </ul>
      ) : (
        <p>No submissions available.</p>
      )}
    </div>
  );
};

export default StudentDetail;

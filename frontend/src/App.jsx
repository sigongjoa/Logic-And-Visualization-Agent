import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import StudentHistory from './components/StudentHistory';
import SubmissionForm from './components/SubmissionForm';
import SubmissionResult from './components/SubmissionResult';
import CoachDashboard from './components/CoachDashboard';
import StudentDetail from './components/StudentDetail';
import CoachReportReview from './components/CoachReportReview';
import AssignmentReview from './components/AssignmentReview'; // New import
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/history">Student History</Link>
            </li>
            <li>
              <Link to="/submit">Submit Problem</Link>
            </li>
            <li>
              <Link to="/coach">Coach Dashboard</Link> {/* New navigation link */}
            </li>
            <li>
              <Link to="/coach/reports">Coach Report Review</Link> {/* New navigation link */}
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/history" element={<StudentHistory />} />
          <Route path="/submit" element={<SubmissionForm />} />
          <Route path="/submission-result" element={<SubmissionResult />} />
          <Route path="/coach" element={<CoachDashboard />} />
          <Route path="/coach/students/:studentId" element={<StudentDetail />} />
          <Route path="/coach/submissions/:submissionId" element={<AssignmentReview />} /> {/* New route */}
          <Route path="/coach/reports" element={<CoachReportReview />} />
        </Routes>
      </div>
    </Router>
  );
}

function Home() {
  return (
    <div>
      <h1>Welcome to Project ATLAS</h1>
      <p>Use the navigation to explore student data or submit problems.</p>
    </div>
  );
}

export default App;
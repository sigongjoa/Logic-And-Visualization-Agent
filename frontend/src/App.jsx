import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import StudentHistory from './components/StudentHistory';
import SubmissionForm from './components/SubmissionForm';
import SubmissionResult from './components/SubmissionResult';
import CoachDashboard from './components/CoachDashboard';
import StudentDetail from './components/StudentDetail';
import CoachReportReview from './components/CoachReportReview';
import AssignmentReview from './components/AssignmentReview';
import StudentDashboard from './components/StudentDashboard';
import CurriculumPage from './components/CurriculumPage';
import LoginPage from './components/LoginPage';
import NotificationCenter from './components/NotificationCenter'; // New import
import './App.css';

        <Routes>
          <Route path="/" element={<LoginPage />} /> {/* Set LoginPage as default route */}
          <Route path="/home" element={<Home />} />
          <Route path="/history" element={<StudentHistory />} />
          <Route path="/submit" element={<SubmissionForm />} />
          <Route path="/submission-result" element={<SubmissionResult />} />
          <Route path="/coach" element={<CoachDashboard />} />
          <Route path="/coach/students/:studentId" element={<StudentDetail />} />
          <Route path="/coach/submissions/:submissionId" element={<AssignmentReview />} />
          <Route path="/student/dashboard" element={<StudentDashboard />} />
          <Route path="/curriculum" element={<CurriculumPage />} />
          <Route path="/notifications" element={<NotificationCenter />} /> {/* New route */}
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
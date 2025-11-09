import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import StudentHistory from './components/StudentHistory';
import SubmissionForm from './components/SubmissionForm';
import SubmissionResult from './components/SubmissionResult';
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
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/history" element={<StudentHistory />} />
          <Route path="/submit" element={<SubmissionForm />} />
          <Route path="/submission-result" element={<SubmissionResult />} />
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
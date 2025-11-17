
import React, { useState, useCallback } from 'react';
import { Page, UserType } from './types';
import LoginPage from './components/LoginPage';
import CoachDashboard from './components/CoachDashboard';
import StudentDashboard from './components/StudentDashboard';
import AssignmentReviewPage from './components/AssignmentReviewPage';
import AssignmentSubmissionPage from './components/AssignmentSubmissionPage';
import CurriculumPage from './components/CurriculumPage';
import NotificationsPage from './components/NotificationsPage';
import StudentDetailsPage from './components/StudentDetailsPage';
import SubmissionHistoryPage from './components/SubmissionHistoryPage';
import SettingsPage from './components/SettingsPage';
import Sidebar from './components/Sidebar';

const App: React.FC = () => {
  const [currentPage, setCurrentPage] = useState<Page>(Page.Login);
  const [userType, setUserType] = useState<UserType | null>(null);
  const [currentStudentId, setCurrentStudentId] = useState<string | null>(null); // New state for student ID
  const [selectedSubmissionId, setSelectedSubmissionId] = useState<string | null>(null);

  const navigateTo = useCallback((page: Page, submissionId: string | null = null) => {
    setCurrentPage(page);
    setSelectedSubmissionId(submissionId);
  }, []);

  const handleLogin = (type: UserType) => {
    setUserType(type);
    if (type === 'coach') {
      setCurrentStudentId(null); // Coaches don't have a specific student ID for themselves
      navigateTo(Page.CoachDashboard);
    } else {
      setCurrentStudentId("std_test_report"); // Hardcode for testing purposes
      navigateTo(Page.StudentDashboard);
    }
  };

  const handleLogout = () => {
    setUserType(null);
    setCurrentStudentId(null); // Clear student ID on logout
    setSelectedSubmissionId(null); // Clear selected submission on logout
    navigateTo(Page.Login);
  };
  
  const renderPage = () => {
    switch (currentPage) {
      case Page.Login:
        return <LoginPage onLogin={handleLogin} />;
      case Page.CoachDashboard:
        return <CoachDashboard navigateTo={navigateTo} userType={userType} />;
      case Page.StudentDashboard:
        return <StudentDashboard navigateTo={navigateTo} userType={userType} currentStudentId={currentStudentId} />;
      case Page.AssignmentReview:
        return <AssignmentReviewPage navigateTo={navigateTo} userType={userType} submissionId={selectedSubmissionId} />;
      case Page.AssignmentSubmission:
        return <AssignmentSubmissionPage navigateTo={navigateTo} userType={userType} />;
      case Page.Curriculum:
        return <CurriculumPage navigateTo={navigateTo} userType={userType} />;
      case Page.Notifications:
        return <NotificationsPage navigateTo={navigateTo} userType={userType} />;
      case Page.StudentDetails:
        return <StudentDetailsPage navigateTo={navigateTo} userType={userType} />;
      case Page.SubmissionHistory:
        return <SubmissionHistoryPage navigateTo={navigateTo} userType={userType} />;
      case Page.Settings:
        return <SettingsPage navigateTo={navigateTo} userType={userType} />;
      default:
        return <LoginPage onLogin={handleLogin} />;
    }
  };

  return (
    <div className="flex">
      {currentPage !== Page.Login && <Sidebar navigateTo={navigateTo} onLogout={handleLogout} userType={userType}/>}
      <div className={`flex-grow ${currentPage !== Page.Login ? 'ml-64' : ''} transition-all duration-300`}>
        {renderPage()}
      </div>
    </div>
  );
};

export default App;

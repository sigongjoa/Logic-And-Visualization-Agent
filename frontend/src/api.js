const API_BASE_URL = 'http://localhost:8000'; // Assuming your FastAPI backend runs on this port

export const createSubmission = async (submissionData) => {
  const response = await fetch(`${API_BASE_URL}/submissions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(submissionData),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to create submission');
  }

  return response.json();
};

export const getAllStudents = async () => {
  const response = await fetch(`${API_BASE_URL}/students`);
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to fetch students');
  }
  return response.json();
};

export const getStudent = async (studentId) => {
    const response = await fetch(`${API_BASE_URL}/students/${studentId}`);
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Failed to fetch student ${studentId}`);
    }
    return response.json();
};

export const getCoaches = async () => {
  const response = await fetch(`${API_BASE_URL}/coaches`);
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to fetch coaches');
  }
  return response.json();
};

export const getCoach = async (coachId) => {
  const response = await fetch(`${API_BASE_URL}/coaches/${coachId}`);
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || `Failed to fetch coach ${coachId}`);
  }
  return response.json();
};

export const getStudentsByCoach = async (coachId) => {
  const response = await fetch(`${API_BASE_URL}/coaches/${coachId}/students`);
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || `Failed to fetch students for coach ${coachId}`);
  }
  return response.json();
};

export const getPendingSubmissionsByCoach = async (coachId) => {
  const response = await fetch(`${API_BASE_URL}/coaches/${coachId}/submissions?status=PENDING`);
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || `Failed to fetch pending submissions for coach ${coachId}`);
  }
  return response.json();
};

export const getCoachMemos = async (studentId) => {
    const response = await fetch(`${API_BASE_URL}/coach-memos/?student_id=${studentId}`);
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Failed to fetch memos for student ${studentId}`);
    }
    return response.json();
};

export const getSubmission = async (submissionId) => {
    const response = await fetch(`${API_BASE_URL}/submissions/${submissionId}`);
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Failed to fetch submission ${submissionId}`);
    }
    return response.json();
};

export const getCurriculums = async () => {
    const response = await fetch(`${API_BASE_URL}/curriculums`);
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to fetch curriculums');
    }
    return response.json();
};

export const getConcepts = async () => {
    const response = await fetch(`${API_BASE_URL}/concepts`);
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to fetch concepts');
    }
    return response.json();
};

export const getConceptRelations = async () => {
    const response = await fetch(`${API_BASE_URL}/concept-relations`);
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to fetch concept relations');
    }
    return response.json();
};

export const login = async (email_or_username, password, user_type) => {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email_or_username, password, user_type }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Login failed');
    }
    return response.json();
};

export const getNotifications = async () => {
    const response = await fetch(`${API_BASE_URL}/notifications/`);
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to fetch notifications');
    }
    return response.json();
};

export const markNotificationAsRead = async (notificationId) => {
    const response = await fetch(`${API_BASE_URL}/notifications/${notificationId}/read`, {
        method: 'PUT',
    });
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Failed to mark notification ${notificationId} as read`);
    }
    return response.json();
};

export const markAllNotificationsAsRead = async () => {
    const response = await fetch(`${API_BASE_URL}/notifications/mark-all-read`, {
        method: 'PUT',
    });
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to mark all notifications as read');
    }
    return response.json();
};

export const getStudentReports = async (studentId) => {
  const response = await fetch(`${API_BASE_URL}/students/${studentId}/reports`);
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || `Failed to fetch reports for student ${studentId}`);
  }
  return response.json();
};

export const getStudentLatestVector = async (studentId) => {
  const response = await fetch(`${API_BASE_URL}/coaches/students/${studentId}/latest_vector`);
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || `Failed to fetch latest vector for student ${studentId}`);
  }
  return response.json();
};

export const getStudentSubmissions = async (studentId) => {
  const response = await fetch(`${API_BASE_URL}/coaches/students/${studentId}/submissions`);
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || `Failed to fetch submissions for student ${studentId}`);
  }
  return response.json();
};

export const getStudentAnkiCards = async (studentId) => {
  const response = await fetch(`${API_BASE_URL}/coaches/students/${studentId}/anki-cards`);
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || `Failed to fetch Anki cards for student ${studentId}`);
  }
  return response.json();
};

export const getStudentMastery = async (studentId) => {
  const response = await fetch(`${API_BASE_URL}/students/${studentId}/mastery`);
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || `Failed to fetch student mastery for student ${studentId}`);
  }
  return response.json();
};

export const getDraftReports = async () => {
  const response = await fetch(`${API_BASE_URL}/reports/drafts`);
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to fetch draft reports');
  }
  return response.json();
};

export const getReportDetails = async (reportId) => {
  const response = await fetch(`${API_BASE_URL}/reports/${reportId}`);
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || `Failed to fetch report details for report ${reportId}`);
  }
  return response.json();
};

export const finalizeReport = async (reportId, coachComment) => {
  const response = await fetch(`${API_BASE_URL}/reports/${reportId}/finalize`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ coach_comment: coachComment }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || `Failed to finalize report ${reportId}`);
  }
  return response.json();
};

export const sendReport = async (reportId) => {
  const response = await fetch(`${API_BASE_URL}/reports/${reportId}/send`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || `Failed to send report ${reportId}`);
  }
  return response.json();
};
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

export const getStudents = async () => {
  const response = await fetch(`${API_BASE_URL}/coaches/students`);
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to fetch students');
  }
  return response.json();
};

export const getStudentReports = async (studentId) => {
  const response = await fetch(`${API_BASE_URL}/coaches/students/${studentId}/reports`);
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
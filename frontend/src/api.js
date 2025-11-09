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
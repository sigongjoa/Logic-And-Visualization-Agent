// frontend/services/api.ts

const API_BASE_URL = 'http://localhost:8000'; // Assuming the backend is running on port 8000

export interface Submission {
  submission_id: string;
  status: string;
  logical_path_text: string;
  concept_id: string | null;
  manim_content_url: string | null;
  audio_explanation_url: string | null;
  submitted_at: string | null;
  problem_text?: string; // Make problem_text optional as it's not in the SubmissionResult schema
}

export interface SubmissionReview {
  coach_id: string;
  decision: 'approved' | 'needs_revision';
  coach_feedback: string;
}

export const getSubmissionsForStudent = async (studentId: string): Promise<Submission[]> => {
  const response = await fetch(`${API_BASE_URL}/students/${studentId}/submissions`);
  if (!response.ok) {
    throw new Error('Failed to fetch submissions for student');
  }
  return response.json();
};

export const getSubmission = async (submissionId: string): Promise<Submission> => {
  const response = await fetch(`${API_BASE_URL}/submissions/${submissionId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch submission');
  }
  return response.json();
};

export const reviewSubmission = async (submissionId: string, review: SubmissionReview): Promise<void> => {
  const response = await fetch(`${API_BASE_URL}/submissions/${submissionId}/review`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(review),
  });
  if (!response.ok) {
    throw new Error('Failed to submit review');
  }
};

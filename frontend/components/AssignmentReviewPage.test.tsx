// frontend/components/AssignmentReviewPage.test.tsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import AssignmentReviewPage from './AssignmentReviewPage';
import * as api from '../services/api';

// Mock the api service
vi.mock('../services/api', () => ({
  getSubmission: vi.fn(),
  reviewSubmission: vi.fn(),
}));

const mockSubmission: api.Submission = {
  submission_id: 'sub_123',
  status: 'COMPLETE',
  logical_path_text: 'This is the AI logical path.',
  problem_text: 'Solve for x: 2x + 3 = 7',
  concept_id: 'C-ALG-001',
  manim_content_url: null,
  audio_explanation_url: null,
  submitted_at: new Date().toISOString(),
};

describe('AssignmentReviewPage', () => {
  beforeEach(() => {
    // Reset mocks before each test
    vi.resetAllMocks();
  });

  it('fetches and displays submission data on mount', async () => {
    (api.getSubmission as jest.Mock).mockResolvedValue(mockSubmission);

    render(<AssignmentReviewPage navigateTo={() => {}} />);

    expect(screen.getByText('Loading submission...')).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText("Student's Problem")).toBeInTheDocument();
    });

    expect(screen.getByText(mockSubmission.problem_text!)).toBeInTheDocument();
    expect(screen.getByText(mockSubmission.logical_path_text)).toBeInTheDocument();
  });

  it('shows an error message if fetching fails', async () => {
    (api.getSubmission as jest.Mock).mockRejectedValue(new Error('Failed to fetch'));

    render(<AssignmentReviewPage navigateTo={() => {}} />);

    await waitFor(() => {
      expect(screen.getByText('Failed to load submission data. Please try again.')).toBeInTheDocument();
    });
  });

  it('allows a coach to submit a review', async () => {
    (api.getSubmission as jest.Mock).mockResolvedValue(mockSubmission);
    (api.reviewSubmission as jest.Mock).mockResolvedValue(undefined);

    render(<AssignmentReviewPage navigateTo={() => {}} />);

    await waitFor(() => {
        expect(screen.getByText("Student's Problem")).toBeInTheDocument();
    });

    // Fill out the form
    fireEvent.click(screen.getByText('Needs Revision'));
    fireEvent.change(screen.getByPlaceholderText('Provide your feedback here...'), {
      target: { value: 'This is not correct.' },
    });

    // Submit the form
    fireEvent.click(screen.getByText('Submit Review'));

    // Check if the API was called correctly
    await waitFor(() => {
      expect(api.reviewSubmission).toHaveBeenCalledWith('sub_123', {
        coach_id: 'coach_review_test',
        decision: 'needs_revision',
        coach_feedback: 'This is not correct.',
      });
    });
  });
});

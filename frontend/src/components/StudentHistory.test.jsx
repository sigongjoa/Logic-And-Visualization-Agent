import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import StudentHistory from './StudentHistory';
import * as api from '../api';

// Mock the api module
vi.mock('../api');

const mockSubmissions = [
  {
    submission_id: 'sub_1',
    problem_text: 'Problem 1',
    submitted_at: new Date().toISOString(),
    status: 'COMPLETE',
  },
  {
    submission_id: 'sub_2',
    problem_text: 'Problem 2',
    submitted_at: new Date().toISOString(),
    status: 'PENDING',
  },
];

const renderComponent = () => {
  return render(
    <MemoryRouter>
      <StudentHistory />
    </MemoryRouter>
  );
};

describe('StudentHistory', () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  test('renders loading state and then the submission history table', async () => {
    api.getStudentSubmissions.mockResolvedValue(mockSubmissions);

    renderComponent();

    expect(screen.getByText(/Loading history.../i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('Problem 1')).toBeInTheDocument();
    });

    expect(screen.getByText('Problem 2')).toBeInTheDocument();
    expect(screen.getByText('COMPLETE')).toBeInTheDocument();
    expect(screen.getByText('PENDING')).toBeInTheDocument();

    expect(api.getStudentSubmissions).toHaveBeenCalledWith('std_test_1');
  });

  test('renders error state on API failure', async () => {
    const errorMessage = 'Failed to fetch submission history.';
    api.getStudentSubmissions.mockRejectedValue(new Error(errorMessage));

    renderComponent();

    await waitFor(() => {
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });
  });
});

import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import StudentDashboard from './StudentDashboard';
import * as api from '../api';

// Mock the api module
vi.mock('../api');

const mockStudent = {
  student_id: 'std_test_1',
  student_name: 'Test Student 1',
};

const mockSubmissions = [
  { submission_id: 'sub_1', student_id: 'std_test_1', problem_text: 'Problem 1', status: 'PENDING' },
  { submission_id: 'sub_2', student_id: 'std_test_1', problem_text: 'Problem 2', status: 'COMPLETE' },
];

const mockMastery = [
  { student_id: 'std_test_1', concept_id: 'C1', mastery_score: 90, status: 'MASTERED' },
  { student_id: 'std_test_1', concept_id: 'C2', mastery_score: 70, status: 'IN_PROGRESS' },
];

describe('StudentDashboard', () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  test('renders loading state and then the dashboard with student data', async () => {
    api.getStudent.mockResolvedValue(mockStudent);
    api.getStudentSubmissions.mockResolvedValue(mockSubmissions);
    api.getStudentMastery.mockResolvedValue(mockMastery);

    render(<StudentDashboard />);

    expect(screen.getByText(/Loading student dashboard.../i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText(/Welcome back, Test Student 1!/i)).toBeInTheDocument();
    });

    // Check Learning Status
    expect(screen.getByText(/Overall Progress/i)).toBeInTheDocument();
    expect(screen.getByText("80%")).toBeInTheDocument(); // (90+70)/2
    expect(screen.getByText(/Skills Mastered/i)).toBeInTheDocument();
    expect(screen.getByText("1")).toBeInTheDocument();

    // Check Upcoming Assignments
    expect(screen.getByText(/Upcoming Assignments/i)).toBeInTheDocument();
    expect(screen.getByText(/Problem 1/i)).toBeInTheDocument();
    expect(screen.queryByText(/Problem 2/i)).not.toBeInTheDocument(); // Should not show completed submissions

    // Check API calls
    expect(api.getStudent).toHaveBeenCalledWith('std_test_1');
    expect(api.getStudentSubmissions).toHaveBeenCalledWith('std_test_1');
    expect(api.getStudentMastery).toHaveBeenCalledWith('std_test_1');
  });

  test('renders error state on API failure', async () => {
    const errorMessage = 'Failed to fetch data';
    api.getStudent.mockRejectedValue(new Error(errorMessage));
    api.getStudentSubmissions.mockRejectedValue(new Error(errorMessage));
    api.getStudentMastery.mockRejectedValue(new Error(errorMessage));

    render(<StudentDashboard />);

    await waitFor(() => {
      expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument();
    });
  });
});
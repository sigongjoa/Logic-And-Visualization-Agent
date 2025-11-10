import React from 'react';
import { render, screen, waitFor, within } from '@testing-library/react';
import { vi } from 'vitest';
import CoachDashboard from './CoachDashboard';
import * as api from '../api';

// Mock the api module
vi.mock('../api');

const mockCoach = {
  coach_id: 'coach_test_1',
  coach_name: 'Test Coach',
};

const mockStudents = [
  { student_id: 'std_coach_1', student_name: 'Coach Student 1', created_at: new Date().toISOString() },
  { student_id: 'std_coach_2', student_name: 'Coach Student 2', created_at: new Date().toISOString() },
];

const mockSubmissions = [
    { submission_id: 'sub_coach_2', student_id: 'std_coach_1', logical_path_text: 'Path 2', status: 'PENDING', concept_id: 'C_COACH_2', manim_content_url: '' },
];

describe('CoachDashboard', () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  test('renders loading state initially, then displays coach, student, and submission data', async () => {
    // Setup mock implementations
    api.getCoach.mockResolvedValue(mockCoach);
    api.getStudentsByCoach.mockResolvedValue(mockStudents);
    api.getPendingSubmissionsByCoach.mockResolvedValue(mockSubmissions);

    render(<CoachDashboard />);

    // 1. Check for loading state
    expect(screen.getByText(/Loading.../i)).toBeInTheDocument();

    // 2. Wait for the component to render the fetched data
    await waitFor(() => {
      expect(screen.getByText(mockCoach.coach_name)).toBeInTheDocument();
    });

    // 3. Assert that all data is displayed in the correct sections
    expect(screen.getByText(mockCoach.coach_name)).toBeInTheDocument();

    const studentList = screen.getByTestId('my-students-list');
    expect(within(studentList).getByText(mockStudents[0].student_name)).toBeInTheDocument();
    expect(within(studentList).getByText(mockStudents[1].student_name)).toBeInTheDocument();

    const submissionList = screen.getByTestId('submissions-review-list');
    // The student name also appears in the submission list
    expect(within(submissionList).getByText(mockStudents[0].student_name)).toBeInTheDocument();
    expect(within(submissionList).getByText(mockSubmissions[0].logical_path_text)).toBeInTheDocument();


    // Ensure the API functions were called
    expect(api.getCoach).toHaveBeenCalledWith('coach_test_1');
    expect(api.getStudentsByCoach).toHaveBeenCalledWith('coach_test_1');
    expect(api.getPendingSubmissionsByCoach).toHaveBeenCalledWith('coach_test_1');
  });

  test('renders error state when API calls fail', async () => {
    const errorMessage = 'Failed to fetch data';
    api.getCoach.mockRejectedValue(new Error(errorMessage));
    api.getStudentsByCoach.mockRejectedValue(new Error(errorMessage));
    api.getPendingSubmissionsByCoach.mockRejectedValue(new Error(errorMessage));


    render(<CoachDashboard />);

    // Wait for the error message to be displayed
    await waitFor(() => {
      expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument();
    });
  });
});
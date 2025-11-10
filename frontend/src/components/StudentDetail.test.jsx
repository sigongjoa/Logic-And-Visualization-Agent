import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import StudentDetail from './StudentDetail';
import * as api from '../api';

// Mock the api module
vi.mock('../api');

const mockStudent = {
  student_id: 'std_1',
  student_name: 'Test Student',
};

const mockSubmissions = [
  { submission_id: 'sub_1', student_id: 'std_1', logical_path_text: 'Submission 1 Text', status: 'COMPLETE', submitted_at: new Date().toISOString() },
];

const mockMemos = [
  { memo_id: 1, student_id: 'std_1', memo_text: 'Memo 1 Text', created_at: new Date().toISOString() },
];

const renderComponent = () => {
  return render(
    <MemoryRouter initialEntries={['/students/std_1']}>
      <Routes>
        <Route path="/students/:studentId" element={<StudentDetail />} />
      </Routes>
    </MemoryRouter>
  );
};

describe('StudentDetail', () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  test('renders loading state and then student details', async () => {
    api.getStudent.mockResolvedValue(mockStudent);
    api.getStudentSubmissions.mockResolvedValue(mockSubmissions);
    api.getCoachMemos.mockResolvedValue(mockMemos);

    renderComponent();

    expect(screen.getByText(/Loading student details.../i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText(mockStudent.student_name)).toBeInTheDocument();
    });

    expect(screen.getByText(mockSubmissions[0].logical_path_text)).toBeInTheDocument();
    expect(screen.getByText(mockMemos[0].memo_text)).toBeInTheDocument();

    expect(api.getStudent).toHaveBeenCalledWith('std_1');
    expect(api.getStudentSubmissions).toHaveBeenCalledWith('std_1');
    expect(api.getCoachMemos).toHaveBeenCalledWith('std_1');
  });

  test('renders error state on API failure', async () => {
    const errorMessage = 'Failed to fetch';
    api.getStudent.mockRejectedValue(new Error(errorMessage));
    api.getStudentSubmissions.mockRejectedValue(new Error(errorMessage));
    api.getCoachMemos.mockRejectedValue(new Error(errorMessage));

    renderComponent();

    await waitFor(() => {
      expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument();
    });
  });
});

import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import AssignmentReview from './AssignmentReview';
import * as api from '../api';

// Mock the api module
vi.mock('../api');

const mockSubmission = {
  submission_id: 'sub_1',
  student_id: 'std_1',
  problem_text: 'Test Problem Text',
  logical_path_text: 'Test Logical Path',
  status: 'COMPLETE',
  manim_content_url: 'https://youtube.com/test_manim',
};

const mockStudent = {
  student_id: 'std_1',
  student_name: 'Test Student',
};

const mockLatestVector = {
  axis1_geo: 70,
  axis1_alg: 80,
  axis1_ana: 75,
  axis2_opt: 60,
  axis2_piv: 65,
  axis2_dia: 70,
  axis3_con: 85,
  axis3_pro: 90,
  axis3_ret: 80,
  axis4_acc: 95,
  axis4_gri: 70,
};

const renderComponent = (submissionId = 'sub_1') => {
  return render(
    <MemoryRouter initialEntries={[`/coach/submissions/${submissionId}`]}>
      <Routes>
        <Route path="/coach/submissions/:submissionId" element={<AssignmentReview />} />
      </Routes>
    </MemoryRouter>
  );
};

describe('AssignmentReview', () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  test('renders loading state and then submission details', async () => {
    api.getSubmission.mockResolvedValue(mockSubmission);
    api.getStudent.mockResolvedValue(mockStudent);
    api.getStudentLatestVector.mockResolvedValue(mockLatestVector);

    renderComponent();

    expect(screen.getByText(/Loading assignment review.../i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText(/Assignment Review/i)).toBeInTheDocument();
    });

    expect(screen.getByText(`Student: ${mockStudent.student_name} (${mockStudent.student_id})`)).toBeInTheDocument();
    expect(screen.getByText(`Problem: ${mockSubmission.problem_text}`)).toBeInTheDocument();
    expect(screen.getByText(`Logical Path: ${mockSubmission.logical_path_text}`)).toBeInTheDocument();
    expect(screen.getByText(`Status: ${mockSubmission.status}`)).toBeInTheDocument();
    expect(screen.getByText(`Manim Video:`)).toBeInTheDocument();
    expect(screen.getByRole('link', { name: mockSubmission.manim_content_url })).toHaveAttribute('href', mockSubmission.manim_content_url);

    expect(screen.getByText(/Student's Latest 4-Axis Model/i)).toBeInTheDocument();
    expect(screen.getByText(`Axis 1 Geo: ${mockLatestVector.axis1_geo}`)).toBeInTheDocument();
    expect(screen.getByText(`Axis 4 Gri: ${mockLatestVector.axis4_gri}`)).toBeInTheDocument();

    expect(api.getSubmission).toHaveBeenCalledWith('sub_1');
    expect(api.getStudent).toHaveBeenCalledWith('std_1');
    expect(api.getStudentLatestVector).toHaveBeenCalledWith('std_1');
  });

  test('renders error state on API failure', async () => {
    const errorMessage = 'Failed to fetch submission';
    api.getSubmission.mockRejectedValue(new Error(errorMessage));
    api.getStudent.mockRejectedValue(new Error(errorMessage));
    api.getStudentLatestVector.mockRejectedValue(new Error(errorMessage));

    renderComponent();

    await waitFor(() => {
      expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument();
    });
  });

  test('renders "Submission or Student not found" if data is missing', async () => {
    api.getSubmission.mockResolvedValue(null);
    api.getStudent.mockResolvedValue(null);
    api.getStudentLatestVector.mockResolvedValue(null);

    renderComponent();

    await waitFor(() => {
      expect(screen.getByText(/Submission or Student not found./i)).toBeInTheDocument();
    });
  });
});

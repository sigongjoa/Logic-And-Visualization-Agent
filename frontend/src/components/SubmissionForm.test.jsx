import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import SubmissionForm from './SubmissionForm';
import * as api from '../api';

// Mock the api module and react-router-dom
vi.mock('../api');
const mockedNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockedNavigate,
  };
});

describe('SubmissionForm', () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  test('renders the form correctly', () => {
    render(<SubmissionForm />, { wrapper: MemoryRouter });
    expect(screen.getByText(/Submit Your Problem/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Start writing your problem here.../i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Submit for Analysis/i })).toBeInTheDocument();
  });

  test('allows typing in the textarea', () => {
    render(<SubmissionForm />, { wrapper: MemoryRouter });
    const textarea = screen.getByPlaceholderText(/Start writing your problem here.../i);
    fireEvent.change(textarea, { target: { value: 'New problem text' } });
    expect(textarea.value).toBe('New problem text');
  });

  test('handles successful submission', async () => {
    const problemText = 'This is a test problem.';
    const mockResult = { submission_id: 'sub_123' };
    api.createSubmission.mockResolvedValue(mockResult);

    render(<SubmissionForm />, { wrapper: MemoryRouter });

    const textarea = screen.getByPlaceholderText(/Start writing your problem here.../i);
    fireEvent.change(textarea, { target: { value: problemText } });

    const submitButton = screen.getByRole('button', { name: /Submit for Analysis/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(api.createSubmission).toHaveBeenCalledWith({
        student_id: 'std_test_1',
        problem_text: problemText,
      });
    });

    await waitFor(() => {
      expect(mockedNavigate).toHaveBeenCalledWith('/submission-result', {
        state: { result: mockResult },
      });
    });
  });

  test('shows an error message on submission failure', async () => {
    const errorMessage = 'Submission failed';
    api.createSubmission.mockRejectedValue(new Error(errorMessage));

    render(<SubmissionForm />, { wrapper: MemoryRouter });

    fireEvent.change(screen.getByPlaceholderText(/Start writing your problem here.../i), {
      target: { value: 'A problem that will fail' },
    });
    fireEvent.click(screen.getByRole('button', { name: /Submit for Analysis/i }));

    await waitFor(() => {
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });
  });

  test('does not submit if textarea is empty', async () => {
    render(<SubmissionForm />, { wrapper: MemoryRouter });
    fireEvent.click(screen.getByRole('button', { name: /Submit for Analysis/i }));

    await waitFor(() => {
        expect(screen.getByText("Problem text cannot be empty.")).toBeInTheDocument();
    });

    expect(api.createSubmission).not.toHaveBeenCalled();
    expect(mockedNavigate).not.toHaveBeenCalled();
  });
});

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import LoginPage from './LoginPage';
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

describe('LoginPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Mock localStorage
    Object.defineProperty(window, 'localStorage', {
      value: {
        getItem: vi.fn(),
        setItem: vi.fn(),
        removeItem: vi.fn(),
        clear: vi.fn(),
      },
      writable: true,
    });
  });

  test('renders the login form correctly', () => {
    render(<LoginPage />, { wrapper: MemoryRouter });
    expect(screen.getByText(/Welcome Back/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Email Address/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Password/i)).toBeInTheDocument();
    expect(screen.getByRole('radio', { name: /Student/i })).toBeChecked();
    expect(screen.getByRole('radio', { name: /Coach/i })).not.toBeChecked();
    expect(screen.getByRole('button', { name: /Log In/i })).toBeInTheDocument();
  });

  test('allows typing in email and password fields', () => {
    render(<LoginPage />, { wrapper: MemoryRouter });
    const emailInput = screen.getByLabelText(/Email Address/i);
    const passwordInput = screen.getByLabelText(/Password/i);

    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });

    expect(emailInput.value).toBe('test@example.com');
    expect(passwordInput.value).toBe('password123');
  });

  test('handles successful student login and redirects', async () => {
    api.login.mockResolvedValue({ access_token: 'dummy_student_token' });

    render(<LoginPage />, { wrapper: MemoryRouter });

    fireEvent.change(screen.getByLabelText(/Email Address/i), { target: { value: 'student@test.com' } });
    fireEvent.change(screen.getByLabelText(/Password/i), { target: { value: 'test' } });
    fireEvent.click(screen.getByRole('button', { name: /Log In/i }));

    await waitFor(() => {
      expect(api.login).toHaveBeenCalledWith('student@test.com', 'test', 'student');
    });

    expect(localStorage.setItem).toHaveBeenCalledWith('access_token', 'dummy_student_token');
    expect(localStorage.setItem).toHaveBeenCalledWith('user_type', 'student');
    expect(mockedNavigate).toHaveBeenCalledWith('/student/dashboard');
  });

  test('handles successful coach login and redirects', async () => {
    api.login.mockResolvedValue({ access_token: 'dummy_coach_token' });

    render(<LoginPage />, { wrapper: MemoryRouter });

    fireEvent.change(screen.getByLabelText(/Email Address/i), { target: { value: 'coach@test.com' } });
    fireEvent.change(screen.getByLabelText(/Password/i), { target: { value: 'test' } });
    fireEvent.click(screen.getByRole('radio', { name: /Coach/i })); // Select coach
    fireEvent.click(screen.getByRole('button', { name: /Log In/i }));

    await waitFor(() => {
      expect(api.login).toHaveBeenCalledWith('coach@test.com', 'test', 'coach');
    });

    expect(localStorage.setItem).toHaveBeenCalledWith('access_token', 'dummy_coach_token');
    expect(localStorage.setItem).toHaveBeenCalledWith('user_type', 'coach');
    expect(mockedNavigate).toHaveBeenCalledWith('/coach');
  });

  test('shows an error message on login failure', async () => {
    const errorMessage = 'Invalid credentials';
    api.login.mockRejectedValue(new Error(errorMessage));

    render(<LoginPage />, { wrapper: MemoryRouter });

    fireEvent.change(screen.getByLabelText(/Email Address/i), { target: { value: 'wrong@test.com' } });
    fireEvent.change(screen.getByLabelText(/Password/i), { target: { value: 'wrong' } });
    fireEvent.click(screen.getByRole('button', { name: /Log In/i }));

    await waitFor(() => {
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });

    expect(localStorage.setItem).not.toHaveBeenCalled();
    expect(mockedNavigate).not.toHaveBeenCalled();
  });
});

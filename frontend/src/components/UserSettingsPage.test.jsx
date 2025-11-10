import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import UserSettingsPage from './UserSettingsPage';
import * as api from '../api';

// Mock the api module
vi.mock('../api');

const mockUserProfile = {
    user_id: "user_123",
    username: "testuser",
    email: "test@example.com",
    user_type: "student"
};

const mockNotificationSettings = {
    new_assignments: true,
    feedback_from_coach: false,
    platform_updates: true
};

describe('UserSettingsPage', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        api.getUserProfile.mockResolvedValue(mockUserProfile);
        api.updateUserProfile.mockResolvedValue(mockUserProfile);
        api.updateUserPassword.mockResolvedValue({ message: "Password updated successfully" });
        api.updateUserNotifications.mockResolvedValue(mockNotificationSettings);
        api.deactivateAccount.mockResolvedValue({ message: "Account deactivated successfully" });
        // Mock window.confirm for deactivate account test
        vi.spyOn(window, 'confirm').mockReturnValue(true);
        vi.spyOn(window, 'alert').mockImplementation(() => {});
    });

    afterEach(() => {
        vi.restoreAllMocks();
    });

    test('renders loading state and then user profile data', async () => {
        render(<UserSettingsPage />);
        expect(screen.getByText(/Loading user settings.../i)).toBeInTheDocument();

        await waitFor(() => {
            expect(screen.getByDisplayValue(mockUserProfile.username)).toBeInTheDocument();
        });
        expect(screen.getByDisplayValue(mockUserProfile.email)).toBeInTheDocument();
        expect(screen.getByText(mockUserProfile.username)).toBeInTheDocument(); // In sidebar
        expect(screen.getByText(mockUserProfile.user_type)).toBeInTheDocument(); // In sidebar
    });

    test('updates user profile successfully', async () => {
        render(<UserSettingsPage />);
        await waitFor(() => {
            expect(screen.getByDisplayValue(mockUserProfile.username)).toBeInTheDocument();
        });

        const usernameInput = screen.getByLabelText(/Username/i);
        const emailInput = screen.getByLabelText(/Email Address/i);
        const newUsername = "newusername";
        const newEmail = "newemail@example.com";

        fireEvent.change(usernameInput, { target: { value: newUsername } });
        fireEvent.change(emailInput, { target: { value: newEmail } });
        fireEvent.click(screen.getByRole('button', { name: /Update Profile/i }));

        await waitFor(() => {
            expect(api.updateUserProfile).toHaveBeenCalledWith({ username: newUsername, email: newEmail });
        });
        expect(window.alert).toHaveBeenCalledWith('Profile updated successfully!');
    });

    test('updates user password successfully', async () => {
        render(<UserSettingsPage />);
        await waitFor(() => {
            expect(screen.getByLabelText(/Current Password/i)).toBeInTheDocument();
        });

        fireEvent.change(screen.getByLabelText(/Current Password/i), { target: { value: 'oldpass' } });
        fireEvent.change(screen.getByPlaceholderText(/Enter new password/i), { target: { value: 'newpass123' } });
        fireEvent.change(screen.getByPlaceholderText(/Confirm new password/i), { target: { value: 'newpass123' } });
        fireEvent.click(screen.getByRole('button', { name: /Update Password/i }));

        await waitFor(() => {
            expect(api.updateUserPassword).toHaveBeenCalledWith({
                current_password: 'oldpass',
                new_password: 'newpass123',
                confirm_new_password: 'newpass123'
            });
        });
        expect(screen.getByText('Password updated successfully!')).toBeInTheDocument();
    });

    test('shows error if new passwords do not match', async () => {
        render(<UserSettingsPage />);
        await waitFor(() => {
            expect(screen.getByLabelText(/Current Password/i)).toBeInTheDocument();
        });

        fireEvent.change(screen.getByLabelText(/Current Password/i), { target: { value: 'oldpass' } });
        fireEvent.change(screen.getByPlaceholderText(/Enter new password/i), { target: { value: 'newpass123' } });
        fireEvent.change(screen.getByPlaceholderText(/Confirm new password/i), { target: { value: 'mismatch' } });
        fireEvent.click(screen.getByRole('button', { name: /Update Password/i }));

        await waitFor(() => {
            expect(screen.getByText('New passwords do not match.')).toBeInTheDocument();
        });
        expect(api.updateUserPassword).not.toHaveBeenCalled();
    });

    test('updates notification settings successfully', async () => {
        render(<UserSettingsPage />);
        await waitFor(() => {
            expect(screen.getByTestId("new-assignments-toggle")).toBeInTheDocument();
        });

        const newAssignmentsToggle = screen.getByTestId("new-assignments-toggle");
        fireEvent.click(newAssignmentsToggle); // Toggle it off

        fireEvent.click(screen.getByRole('button', { name: /Update Notifications/i }));

        await waitFor(() => {
            expect(api.updateUserNotifications).toHaveBeenCalledWith({
                new_assignments: false, // Should be false after toggle
                feedback_from_coach: true, // Initial dummy value
                platform_updates: false // Initial dummy value
            });
        });
        expect(screen.getByText('Notification settings updated successfully!')).toBeInTheDocument();
    });

    test('deactivates account successfully', async () => {
        render(<UserSettingsPage />);
        await waitFor(() => {
            expect(screen.getByRole('button', { name: /Deactivate Account/i })).toBeInTheDocument();
        });

        fireEvent.click(screen.getByRole('button', { name: /Deactivate Account/i }));

        await waitFor(() => {
            expect(window.confirm).toHaveBeenCalledWith('Are you sure you want to deactivate your account? This action cannot be undone.');
        });
        expect(api.deactivateAccount).toHaveBeenCalledTimes(1);
        expect(window.alert).toHaveBeenCalledWith('Account deactivated successfully. You will be logged out.');
    });

    test('shows error message on profile fetch failure', async () => {
        const errorMessage = 'Failed to fetch user profile.';
        api.getUserProfile.mockRejectedValue(new Error(errorMessage));

        render(<UserSettingsPage />);

        await waitFor(() => {
            expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument();
        });
    });
});

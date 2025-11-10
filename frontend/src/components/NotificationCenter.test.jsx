import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import NotificationCenter from './NotificationCenter';
import * as api from '../api';
import { formatDistanceToNow } from 'date-fns';

// Mock the api module
vi.mock('../api');
// Mock date-fns for consistent output
vi.mock('date-fns', async () => {
    const actual = await vi.importActual('date-fns');
    return {
        ...actual,
        formatDistanceToNow: vi.fn((date) => {
            if (date.getHours() === new Date().getHours() - 2) return '2 hours ago';
            if (date.getDate() === new Date().getDate() - 1) return 'yesterday';
            return 'a while ago';
        }),
    };
});

const mockNotifications = [
    {
        notification_id: "notif_001",
        user_id: "user_123",
        type: "assignment_graded",
        title: "Grade Posted: Data Structures Intro",
        message: "Your submission for 'Data Structures Intro' has been graded. Your score is 95/100.",
        created_at: new Date(new Date().setHours(new Date().getHours() - 2)).toISOString(),
        is_read: false,
        related_id: "sub_001"
    },
    {
        notification_id: "notif_002",
        user_id: "user_123",
        type: "new_feedback",
        title: "New Feedback: Algorithm Design",
        message: "You have new feedback from Coach Turing on 'Algorithm Design'.",
        created_at: new Date(new Date().setDate(new Date().getDate() - 1)).toISOString(),
        is_read: false,
        related_id: "sub_002"
    },
    {
        notification_id: "notif_003",
        user_id: "user_123",
        type: "new_student",
        title: "New Student Assigned: Jane Doe",
        message: "Jane Doe has been added to your roster.",
        created_at: new Date(new Date().setDate(new Date().getDate() - 2)).toISOString(),
        is_read: true,
        related_id: "student_jane"
    },
];

describe('NotificationCenter', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        api.getNotifications.mockResolvedValue(mockNotifications);
        api.markNotificationAsRead.mockResolvedValue({});
        api.markAllNotificationsAsRead.mockResolvedValue({});
    });

    test('renders loading state and then notifications', async () => {
        render(<NotificationCenter />);
        expect(screen.getByText(/Loading notifications.../i)).toBeInTheDocument();

        await waitFor(() => {
            expect(screen.getByText(/Grade Posted: Data Structures Intro/i)).toBeInTheDocument();
        });
        expect(screen.getByText(/New Feedback: Algorithm Design/i)).toBeInTheDocument();
        expect(screen.getByText(/New Student Assigned: Jane Doe/i)).toBeInTheDocument();
        expect(screen.getByText('2 hours ago')).toBeInTheDocument();
        expect(screen.getByText('yesterday')).toBeInTheDocument();
    });

    test('marks a single notification as read when clicked', async () => {
        render(<NotificationCenter />);
        await waitFor(() => {
            expect(screen.getByText(/Grade Posted: Data Structures Intro/i)).toBeInTheDocument();
        });

        const unreadNotification = screen.getByText(/Grade Posted: Data Structures Intro/i);
        fireEvent.click(unreadNotification);

        await waitFor(() => {
            expect(api.markNotificationAsRead).toHaveBeenCalledWith("notif_001");
        });

        // Check if the notification is visually marked as read (e.g., opacity change)
        // This might require more specific DOM queries depending on actual styling
        expect(unreadNotification.closest('.opacity-70')).toBeInTheDocument();
    });

    test('marks all notifications as read', async () => {
        render(<NotificationCenter />);
        await waitFor(() => {
            expect(screen.getByText(/Grade Posted: Data Structures Intro/i)).toBeInTheDocument();
        });

        fireEvent.click(screen.getByRole('button', { name: /Mark all as read/i }));

        await waitFor(() => {
            expect(api.markAllNotificationsAsRead).toHaveBeenCalledTimes(1);
        });

        // Verify all notifications are visually marked as read
        expect(screen.getByText(/Grade Posted: Data Structures Intro/i).closest('.opacity-70')).toBeInTheDocument();
        expect(screen.getByText(/New Feedback: Algorithm Design/i).closest('.opacity-70')).toBeInTheDocument();
    });

    test('shows error message on fetch failure', async () => {
        const errorMessage = 'Failed to fetch notifications.';
        api.getNotifications.mockRejectedValue(new Error(errorMessage));

        render(<NotificationCenter />);

        await waitFor(() => {
            expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument();
        });
    });

    test('displays details of selected notification', async () => {
        render(<NotificationCenter />);
        await waitFor(() => {
            expect(screen.getByText(/Grade Posted: Data Structures Intro/i)).toBeInTheDocument();
        });

        fireEvent.click(screen.getByText(/Grade Posted: Data Structures Intro/i));

        await waitFor(() => {
            expect(screen.getByText(/Your submission for 'Data Structures Intro' has been graded./i)).toBeInTheDocument();
        });
        expect(screen.getByText(/View Gradebook/i)).toBeInTheDocument();
    });
});

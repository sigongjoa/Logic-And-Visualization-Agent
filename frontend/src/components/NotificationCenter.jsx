import React, { useState, useEffect } from 'react';
import { getNotifications, markNotificationAsRead, markAllNotificationsAsRead } from '../api';
import { formatDistanceToNow } from 'date-fns'; // Assuming date-fns is installed for time formatting

const NotificationCenter = () => {
    const [notifications, setNotifications] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedNotification, setSelectedNotification] = useState(null);

    const fetchNotifications = async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await getNotifications();
            setNotifications(data);
        } catch (err) {
            setError(err.message || 'Failed to fetch notifications.');
            console.error('Error fetching notifications:', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchNotifications();
    }, []);

    const handleNotificationClick = (notification) => {
        setSelectedNotification(notification);
        if (!notification.is_read) {
            handleMarkAsRead(notification.notification_id);
        }
    };

    const handleMarkAsRead = async (notificationId) => {
        try {
            await markNotificationAsRead(notificationId);
            setNotifications(prevNotifs =>
                prevNotifs.map(notif =>
                    notif.notification_id === notificationId ? { ...notif, is_read: true } : notif
                )
            );
            if (selectedNotification && selectedNotification.notification_id === notificationId) {
                setSelectedNotification(prev => ({ ...prev, is_read: true }));
            }
        } catch (err) {
            console.error('Error marking notification as read:', err);
            setError(err.message || 'Failed to mark notification as read.');
        }
    };

    const handleMarkAllAsRead = async () => {
        try {
            await markAllNotificationsAsRead();
            setNotifications(prevNotifs =>
                prevNotifs.map(notif => ({ ...notif, is_read: true }))
            );
        } catch (err) {
            console.error('Error marking all notifications as read:', err);
            setError(err.message || 'Failed to mark all notifications as read.');
        }
    };

    const getNotificationIcon = (type) => {
        switch (type) {
            case 'assignment_graded': return 'school';
            case 'new_feedback': return 'chat_bubble';
            case 'new_student': return 'assignment_ind';
            case 'new_submission': return 'file_upload';
            case 'system_alert': return 'info';
            default: return 'notifications';
        }
    };

    if (loading) {
        return <div>Loading notifications...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div className="flex h-screen w-full">
            {/* SideNavBar - Placeholder for now */}
            <aside className="flex flex-col h-full bg-white dark:bg-background-dark dark:border-r dark:border-gray-800 w-64 shrink-0 p-4 border-r border-app-border">
                <div className="flex flex-col gap-4">
                    <div className="flex items-center gap-3">
                        <div className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10" data-alt="User profile picture" style={{ backgroundImage: 'url("https://via.placeholder.com/150")' }}></div>
                        <div className="flex flex-col">
                            <h1 className="text-app-text dark:text-gray-200 text-base font-medium leading-normal">User Name</h1>
                            <p className="text-gray-500 dark:text-gray-400 text-sm font-normal leading-normal">User Role</p>
                        </div>
                    </div>
                </div>
                <nav className="flex flex-col gap-2 mt-6 grow">
                    {/* Navigation links here */}
                    <a className="flex items-center gap-3 px-3 py-2 rounded-lg bg-primary/10 dark:bg-primary/20" href="#">
                        <span className="material-symbols-outlined text-app-blue">notifications_active</span>
                        <p className="text-app-blue text-sm font-medium leading-normal">Notifications</p>
                    </a>
                </nav>
            </aside>

            {/* Main Content */}
            <main className="flex-1 flex flex-col h-screen overflow-hidden bg-app-bg dark:bg-background-dark">
                {/* Header */}
                <header className="flex flex-wrap justify-between items-center gap-3 p-6 border-b border-app-border dark:border-gray-800 bg-white dark:bg-background-dark">
                    <p className="text-app-text dark:text-gray-100 text-2xl font-bold leading-tight tracking-tight min-w-72">Notification Center</p>
                    <div className="flex items-center gap-4">
                        <button onClick={handleMarkAllAsRead} className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-gray-100 dark:bg-gray-800 text-app-text dark:text-gray-200 text-sm font-medium leading-normal tracking-[0.015em] hover:bg-gray-200 dark:hover:bg-gray-700">
                            <span className="truncate">Mark all as read</span>
                        </button>
                        <button className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-app-text dark:text-gray-300">
                            <span className="material-symbols-outlined">settings</span>
                        </button>
                    </div>
                </header>

                {/* Two-Pane Layout */}
                <div className="flex flex-1 overflow-hidden">
                    {/* Left Pane: Notification List */}
                    <div className="w-1/3 border-r border-app-border dark:border-gray-800 bg-white dark:bg-background-dark flex flex-col overflow-y-auto">
                        {/* Filters - Simplified for now */}
                        <div className="flex gap-2 p-4 flex-wrap border-b border-app-border dark:border-gray-800 sticky top-0 bg-white dark:bg-background-dark z-10">
                            <button className="flex h-8 shrink-0 items-center justify-center gap-x-2 rounded-full bg-app-blue text-white px-4">
                                <p className="text-sm font-medium leading-normal">All</p>
                            </button>
                            {/* Other filter buttons can be added here */}
                        </div>
                        {/* Notification Items */}
                        <div className="flex flex-col divide-y divide-app-border dark:divide-gray-800">
                            {notifications.length > 0 ? (
                                notifications.map(notif => (
                                    <div
                                        key={notif.notification_id}
                                        className={`flex items-start gap-3 p-4 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800/50 ${notif.is_read ? 'opacity-70' : 'bg-primary/10 dark:bg-primary/20 border-l-4 border-app-blue'}`}
                                        onClick={() => handleNotificationClick(notif)}
                                    >
                                        {!notif.is_read && <div className="w-2.5 h-2.5 bg-app-blue rounded-full mt-2.5 shrink-0"></div>}
                                        <div className={`text-white flex items-center justify-center rounded-lg shrink-0 size-10 ${notif.is_read ? 'bg-gray-500' : 'bg-app-green'}`}>
                                            <span className="material-symbols-outlined">{getNotificationIcon(notif.type)}</span>
                                        </div>
                                        <div className="flex flex-col justify-center grow">
                                            <p className={`text-sm font-bold leading-normal ${notif.is_read ? 'text-app-text dark:text-gray-300 font-medium' : 'text-app-text dark:text-gray-100'}`}>{notif.title}</p>
                                            <p className="text-gray-500 dark:text-gray-400 text-xs font-normal leading-normal">{formatDistanceToNow(new Date(notif.created_at), { addSuffix: true })}</p>
                                        </div>
                                    </div>
                                ))
                            ) : (
                                <p className="p-4 text-center text-gray-500">No notifications.</p>
                            )}
                        </div>
                    </div>

                    {/* Right Pane: Detail View */}
                    <div className="w-2/3 flex flex-col p-8 overflow-y-auto bg-app-bg dark:bg-background-dark">
                        {selectedNotification ? (
                            <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm p-8">
                                <div className="flex items-center gap-4">
                                    <div className={`text-white flex items-center justify-center rounded-lg shrink-0 size-12 ${selectedNotification.is_read ? 'bg-gray-500' : 'bg-app-green'}`}>
                                        <span className="material-symbols-outlined text-3xl">{getNotificationIcon(selectedNotification.type)}</span>
                                    </div>
                                    <div>
                                        <h2 className="text-app-text dark:text-gray-100 text-xl font-bold">{selectedNotification.title}</h2>
                                        <p className="text-gray-500 dark:text-gray-400 text-sm">{formatDistanceToNow(new Date(selectedNotification.created_at), { addSuffix: true })}</p>
                                    </div>
                                </div>
                                <div className="border-t border-app-border dark:border-gray-800 my-6"></div>
                                <div className="space-y-4">
                                    <p className="text-app-text dark:text-gray-200 leading-relaxed">{selectedNotification.message}</p>
                                    {/* Add more details based on notification type if needed */}
                                </div>
                                <div className="border-t border-app-border dark:border-gray-800 my-6"></div>
                                <div className="flex gap-4">
                                    {/* Action buttons based on related_id or type */}
                                    {selectedNotification.type === 'assignment_graded' && (
                                        <button className="flex min-w-[84px] cursor-pointer items-center justify-center gap-2 overflow-hidden rounded-lg h-11 px-6 bg-app-blue text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-blue-600">
                                            <span className="material-symbols-outlined">visibility</span>
                                            <span className="truncate">View Gradebook</span>
                                        </button>
                                    )}
                                    {/* Example for other types */}
                                    {selectedNotification.type === 'new_feedback' && (
                                        <button className="flex min-w-[84px] cursor-pointer items-center justify-center gap-2 overflow-hidden rounded-lg h-11 px-6 bg-app-blue text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-blue-600">
                                            <span className="material-symbols-outlined">chat</span>
                                            <span className="truncate">View Feedback</span>
                                        </button>
                                    )}
                                </div>
                            </div>
                        ) : (
                            <div className="flex items-center justify-center h-full text-gray-500">
                                Select a notification to view details.
                            </div>
                        )}
                    </div>
                </div>
            </main>
        </div>
    );
};

export default NotificationCenter;

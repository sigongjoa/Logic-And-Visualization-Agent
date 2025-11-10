import React, { useState, useEffect } from 'react';
import { getUserProfile, updateUserProfile, updateUserPassword, updateUserNotifications, deactivateAccount } from '../api';

const UserSettingsPage = () => {
    const [userProfile, setUserProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Profile update state
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');

    // Password update state
    const [currentPassword, setCurrentPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmNewPassword, setConfirmNewPassword] = useState('');
    const [passwordError, setPasswordError] = useState(null);
    const [passwordSuccess, setPasswordSuccess] = useState(null);

    // Notification settings state
    const [newAssignments, setNewAssignments] = useState(false);
    const [feedbackFromCoach, setFeedbackFromCoach] = useState(false);
    const [platformUpdates, setPlatformUpdates] = useState(false);
    const [notificationSuccess, setNotificationSuccess] = useState(null);
    const [notificationError, setNotificationError] = useState(null);

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const profile = await getUserProfile();
                setUserProfile(profile);
                setUsername(profile.username);
                setEmail(profile.email);
                // Fetch notification settings if available
                // For now, using dummy settings from backend router
                setNewAssignments(true); // Placeholder
                setFeedbackFromCoach(true); // Placeholder
                setPlatformUpdates(false); // Placeholder
            } catch (err) {
                setError(err.message || 'Failed to fetch user profile.');
                console.error('Error fetching profile:', err);
            } finally {
                setLoading(false);
            }
        };
        fetchProfile();
    }, []);

    const handleProfileUpdate = async (e) => {
        e.preventDefault();
        setError(null);
        try {
            const updatedProfile = await updateUserProfile({ username, email });
            setUserProfile(updatedProfile);
            alert('Profile updated successfully!');
        } catch (err) {
            setError(err.message || 'Failed to update profile.');
            console.error('Error updating profile:', err);
        }
    };

    const handlePasswordUpdate = async (e) => {
        e.preventDefault();
        setPasswordError(null);
        setPasswordSuccess(null);
        if (newPassword !== confirmNewPassword) {
            setPasswordError('New passwords do not match.');
            return;
        }
        try {
            await updateUserPassword({ current_password: currentPassword, new_password: newPassword, confirm_new_password: confirmNewPassword });
            setPasswordSuccess('Password updated successfully!');
            setCurrentPassword('');
            setNewPassword('');
            setConfirmNewPassword('');
        } catch (err) {
            setPasswordError(err.message || 'Failed to update password.');
            console.error('Error updating password:', err);
        }
    };

    const handleNotificationUpdate = async (e) => {
        e.preventDefault();
        setNotificationError(null);
        setNotificationSuccess(null);
        try {
            await updateUserNotifications({ new_assignments: newAssignments, feedback_from_coach: feedbackFromCoach, platform_updates: platformUpdates });
            setNotificationSuccess('Notification settings updated successfully!');
        } catch (err) {
            setNotificationError(err.message || 'Failed to update notification settings.');
            console.error('Error updating notification settings:', err);
        }
    };

    const handleDeactivateAccount = async () => {
        if (window.confirm('Are you sure you want to deactivate your account? This action cannot be undone.')) {
            try {
                await deactivateAccount();
                alert('Account deactivated successfully. You will be logged out.');
                // Redirect to login page or home
                // navigate('/login');
            } catch (err) {
                setError(err.message || 'Failed to deactivate account.');
                console.error('Error deactivating account:', err);
            }
        }
    };

    if (loading) {
        return <div>Loading user settings...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    if (!userProfile) {
        return <div>No user profile found.</div>;
    }

    return (
        <div className="flex h-full grow flex-col">
            <div className="flex flex-1 justify-center py-5 sm:py-10 px-4 sm:px-6 lg:px-8">
                <div className="flex w-full max-w-7xl flex-row gap-8">
                    {/* SideNavBar - Simplified for now */}
                    <aside className="hidden md:flex w-full max-w-xs flex-col">
                        <div className="flex h-full flex-col justify-between bg-foreground-light dark:bg-foreground-dark p-4 rounded-lg border border-border-light dark:border-border-dark">
                            <div className="flex flex-col gap-4">
                                <div className="flex items-center gap-3">
                                    <div className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-12" data-alt="User profile picture" style={{ backgroundImage: 'url("https://via.placeholder.com/150")' }}></div>
                                    <div className="flex flex-col">
                                        <h1 className="text-primary-text-light dark:text-primary-text-dark text-base font-medium leading-normal">{userProfile.username}</h1>
                                        <p className="text-secondary-text-light dark:text-secondary-text-dark text-sm font-normal leading-normal">{userProfile.user_type}</p>
                                    </div>
                                </div>
                                <div className="flex flex-col gap-2 pt-4">
                                    <div className="flex items-center gap-3 px-3 py-2 rounded-md bg-primary/10 dark:bg-primary/20 cursor-pointer">
                                        <span className="material-symbols-outlined text-primary text-2xl">key</span>
                                        <p className="text-primary text-sm font-medium leading-normal">Account</p>
                                    </div>
                                    {/* Other sidebar links can be added here */}
                                </div>
                            </div>
                            <div className="flex flex-col gap-2">
                                <div className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-gray-100 dark:hover:bg-white/10 cursor-pointer">
                                    <span className="material-symbols-outlined text-primary-text-light dark:text-primary-text-dark text-2xl">logout</span>
                                    <p className="text-primary-text-light dark:text-primary-text-dark text-sm font-medium leading-normal">Logout</p>
                                </div>
                            </div>
                        </div>
                    </aside>

                    {/* Main Content */}
                    <main className="flex-1 flex flex-col gap-8">
                        {/* PageHeading */}
                        <div className="flex flex-wrap justify-between gap-3 px-4">
                            <p className="text-primary-text-light dark:text-primary-text-dark text-4xl font-black leading-tight tracking-[-0.033em]">Account Settings</p>
                        </div>
                        <div className="flex flex-col gap-8 bg-foreground-light dark:bg-foreground-dark p-6 sm:p-8 rounded-lg border border-border-light dark:border-border-dark">
                            {/* Profile Section */}
                            <section>
                                <h2 className="text-primary-text-light dark:text-primary-text-dark text-[22px] font-bold leading-tight tracking-[-0.015em] pb-3 pt-2 border-b border-border-light dark:border-border-dark">Profile</h2>
                                <form onSubmit={handleProfileUpdate} className="pt-6">
                                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-6">
                                        <label className="flex flex-col">
                                            <p className="text-primary-text-light dark:text-primary-text-dark text-base font-medium leading-normal pb-2">Username</p>
                                            <input
                                                type="text"
                                                value={username}
                                                onChange={(e) => setUsername(e.target.value)}
                                                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-md text-primary-text-light dark:text-primary-text-dark bg-background-light dark:bg-background-dark focus:ring-primary focus:border-primary border-border-light dark:border-border-dark h-12 placeholder:text-secondary-text-light dark:placeholder:text-secondary-text-dark px-4 text-base font-normal leading-normal"
                                                required
                                            />
                                        </label>
                                        <label className="flex flex-col">
                                            <p className="text-primary-text-light dark:text-primary-text-dark text-base font-medium leading-normal pb-2">Email Address</p>
                                            <input
                                                type="email"
                                                value={email}
                                                onChange={(e) => setEmail(e.target.value)}
                                                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-md text-primary-text-light dark:text-primary-text-dark bg-background-light dark:bg-background-dark focus:ring-primary focus:border-primary border-border-light dark:border-border-dark h-12 placeholder:text-secondary-text-light dark:placeholder:text-secondary-text-dark px-4 text-base font-normal leading-normal"
                                                required
                                            />
                                        </label>
                                    </div>
                                    <div className="flex justify-end pt-6">
                                        <button type="submit" className="flex items-center justify-center font-semibold text-white bg-primary rounded-md px-5 py-2.5 h-11 text-sm leading-6 transition-colors hover:bg-primary/90">Update Profile</button>
                                    </div>
                                </form>
                            </section>

                            {/* Account Section - Change Password */}
                            <section>
                                <h2 className="text-primary-text-light dark:text-primary-text-dark text-[22px] font-bold leading-tight tracking-[-0.015em] pb-3 pt-2 border-b border-border-light dark:border-border-dark">Account</h2>
                                <form onSubmit={handlePasswordUpdate} className="pt-6">
                                    <h1 className="text-primary-text-light dark:text-primary-text-dark text-xl font-bold leading-tight tracking-[-0.015em] pb-5">Change Password</h1>
                                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-6">
                                        <label className="flex flex-col">
                                            <p className="text-primary-text-light dark:text-primary-text-dark text-base font-medium leading-normal pb-2">Current Password</p>
                                            <input
                                                type="password"
                                                value={currentPassword}
                                                onChange={(e) => setCurrentPassword(e.target.value)}
                                                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-md text-primary-text-light dark:text-primary-text-dark bg-background-light dark:bg-background-dark focus:ring-primary focus:border-primary border-border-light dark:border-border-dark h-12 placeholder:text-secondary-text-light dark:placeholder:text-secondary-text-dark px-4 text-base font-normal leading-normal"
                                                placeholder="Enter your current password"
                                                required
                                            />
                                        </label>
                                        <div></div>
                                        <label className="flex flex-col">
                                            <p className="text-primary-text-light dark:text-primary-text-dark text-base font-medium leading-normal pb-2">New Password</p>
                                            <input
                                                type="password"
                                                value={newPassword}
                                                onChange={(e) => setNewPassword(e.target.value)}
                                                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-md text-primary-text-light dark:text-primary-text-dark bg-background-light dark:bg-background-dark focus:ring-primary focus:border-primary border-border-light dark:border-border-dark h-12 placeholder:text-secondary-text-light dark:placeholder:text-secondary-text-dark px-4 text-base font-normal leading-normal"
                                                placeholder="Enter new password"
                                                required
                                            />
                                            <p className="text-secondary-text-light dark:text-secondary-text-dark text-xs pt-1">Password must be at least 8 characters long.</p>
                                        </label>
                                        <label className="flex flex-col">
                                            <p className="text-primary-text-light dark:text-primary-text-dark text-base font-medium leading-normal pb-2">Confirm New Password</p>
                                            <input
                                                type="password"
                                                value={confirmNewPassword}
                                                onChange={(e) => setConfirmNewPassword(e.target.value)}
                                                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-md text-primary-text-light dark:text-primary-text-dark bg-background-light dark:bg-background-dark focus:ring-primary focus:border-primary border-border-light dark:border-border-dark h-12 placeholder:text-secondary-text-light dark:placeholder:text-secondary-text-dark px-4 text-base font-normal leading-normal"
                                                placeholder="Confirm new password"
                                                required
                                            />
                                        </label>
                                    </div>
                                    {passwordError && <p className="text-red-500 text-sm mt-2">{passwordError}</p>}
                                    {passwordSuccess && <p className="text-green-500 text-sm mt-2">{passwordSuccess}</p>}
                                    <div className="flex justify-end pt-6">
                                        <button type="submit" className="flex items-center justify-center font-semibold text-white bg-primary rounded-md px-5 py-2.5 h-11 text-sm leading-6 transition-colors hover:bg-primary/90">Update Password</button>
                                    </div>
                                </form>
                            </section>

                            {/* Notifications Section */}
                            <section>
                                <h2 className="text-primary-text-light dark:text-primary-text-dark text-[22px] font-bold leading-tight tracking-[-0.015em] pb-3 pt-5 border-b border-border-light dark:border-border-dark">Notifications</h2>
                                <form onSubmit={handleNotificationUpdate} className="pt-6">
                                    <h3 className="text-primary-text-light dark:text-primary-text-dark text-xl font-bold leading-tight tracking-[-0.015em] pb-1">Email Notifications</h3>
                                    <p className="text-secondary-text-light dark:text-secondary-text-dark text-sm pb-5">Manage your email notification preferences.</p>
                                    <div className="flex flex-col gap-4">
                                        <div className="flex items-center justify-between">
                                            <div>
                                                <p className="text-primary-text-light dark:text-primary-text-dark font-medium">New assignments posted</p>
                                                <p className="text-secondary-text-light dark:text-secondary-text-dark text-sm">Get notified when a new assignment is available.</p>
                                            </div>
                                            <label className="relative inline-flex cursor-pointer items-center">
                                                <input
                                                    type="checkbox"
                                                    checked={newAssignments}
                                                    onChange={(e) => setNewAssignments(e.target.checked)}
                                                    className="peer sr-only"
                                                    data-testid="new-assignments-toggle"
                                                />
                                                <div className="peer h-6 w-11 rounded-full bg-gray-200 after:absolute after:start-[2px] after:top-[2px] after:h-5 after:w-5 after:rounded-full after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-primary peer-checked:after:translate-x-full peer-checked:after:border-white peer-focus:outline-none dark:border-gray-600 dark:bg-gray-700"></div>
                                            </label>
                                        </div>
                                        <div className="flex items-center justify-between">
                                            <div>
                                                <p className="text-primary-text-light dark:text-primary-text-dark font-medium">Feedback from coach</p>
                                                <p className="text-secondary-text-light dark:text-secondary-text-dark text-sm">Receive an email when your coach provides feedback.</p>
                                            </div>
                                            <label className="relative inline-flex cursor-pointer items-center">
                                                <input
                                                    type="checkbox"
                                                    checked={feedbackFromCoach}
                                                    onChange={(e) => setFeedbackFromCoach(e.target.checked)}
                                                    className="peer sr-only"
                                                    data-testid="feedback-coach-toggle"
                                                />
                                                <div className="peer h-6 w-11 rounded-full bg-gray-200 after:absolute after:start-[2px] after:top-[2px] after:h-5 after:w-5 after:rounded-full after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-primary peer-checked:after:translate-x-full peer-checked:after:border-white peer-focus:outline-none dark:border-gray-600 dark:bg-gray-700"></div>
                                            </label>
                                        </div>
                                        <div className="flex items-center justify-between">
                                            <div>
                                                <p className="text-primary-text-light dark:text-primary-text-dark font-medium">Platform updates</p>
                                                <p className="text-secondary-text-light dark:text-secondary-text-dark text-sm">Stay up-to-date with new features and announcements.</p>
                                            </div>
                                            <label className="relative inline-flex cursor-pointer items-center">
                                                <input
                                                    type="checkbox"
                                                    checked={platformUpdates}
                                                    onChange={(e) => setPlatformUpdates(e.target.checked)}
                                                    className="peer sr-only"
                                                    data-testid="platform-updates-toggle"
                                                />
                                                <div className="peer h-6 w-11 rounded-full bg-gray-200 after:absolute after:start-[2px] after:top-[2px] after:h-5 after:w-5 after:rounded-full after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-primary peer-checked:after:translate-x-full peer-checked:after:border-white peer-focus:outline-none dark:border-gray-600 dark:bg-gray-700"></div>
                                            </label>
                                        </div>
                                    </div>
                                    {notificationError && <p className="text-red-500 text-sm mt-2">{notificationError}</p>}
                                    {notificationSuccess && <p className="text-green-500 text-sm mt-2">{notificationSuccess}</p>}
                                    <div className="flex justify-end pt-6">
                                        <button type="submit" className="flex items-center justify-center font-semibold text-white bg-primary rounded-md px-5 py-2.5 h-11 text-sm leading-6 transition-colors hover:bg-primary/90">Update Notifications</button>
                                    </div>
                                </form>
                            </section>

                            {/* Deactivate Account Section */}
                            <section>
                                <h2 className="text-red-600 dark:text-red-500 text-[22px] font-bold leading-tight tracking-[-0.015em] pb-3 pt-5 border-b border-border-light dark:border-border-dark">Danger Zone</h2>
                                <div className="pt-6">
                                    <h3 className="text-primary-text-light dark:text-primary-text-dark text-xl font-bold leading-tight tracking-[-0.015em]">Deactivate Account</h3>
                                    <p className="text-secondary-text-light dark:text-secondary-text-dark text-sm mt-1 max-w-2xl">Once you deactivate your account, there is no going back. Please be certain.</p>
                                    <div className="flex justify-start pt-5">
                                        <button onClick={handleDeactivateAccount} className="flex items-center justify-center font-semibold text-white bg-red-600 rounded-md px-5 py-2.5 h-11 text-sm leading-6 transition-colors hover:bg-red-700">Deactivate Account</button>
                                    </div>
                                </div>
                            </section>
                        </div>
                    </main>
                </div>
            </div>
        </div>
    );
};

export default UserSettingsPage;

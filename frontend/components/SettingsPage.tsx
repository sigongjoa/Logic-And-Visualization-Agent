
import React from 'react';
import { NavigationProps } from '../types';

const SettingsPage: React.FC<NavigationProps> = ({ navigateTo }) => {
  return (
    <div className="font-display bg-[#f6f6f8] dark:bg-[#101622] min-h-screen">
        <div className="flex flex-1 justify-center py-5 sm:py-10 px-4 sm:px-6 lg:px-8">
            <div className="flex w-full max-w-7xl flex-row gap-8">
                <main className="flex-1 flex flex-col gap-8">
                    <div className="flex flex-wrap justify-between gap-3 px-4">
                        <p className="text-[#111318] dark:text-[#f0f2f4] text-4xl font-black leading-tight tracking-[-0.033em] min-w-72">Account Settings</p>
                    </div>
                    <div className="flex flex-col gap-8 bg-[#ffffff] dark:bg-[#182131] p-6 sm:p-8 rounded-lg border border-[#dbdfe6] dark:border-[#334155]">
                        <section>
                            <h2 className="text-[#111318] dark:text-[#f0f2f4] text-[22px] font-bold leading-tight tracking-[-0.015em] pb-3 pt-2 border-b border-[#dbdfe6] dark:border-[#334155]">Account</h2>
                            <div className="pt-6">
                                <h1 className="text-[#111318] dark:text-[#f0f2f4] text-xl font-bold leading-tight tracking-[-0.015em] pb-5">Change Password</h1>
                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-6">
                                    <label className="flex flex-col">
                                        <p className="text-[#111318] dark:text-[#f0f2f4] text-base font-medium leading-normal pb-2">Current Password</p>
                                        <input className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-md text-[#111318] dark:text-[#f0f2f4] bg-[#f6f6f8] dark:bg-[#101622] focus:ring-[#135bec] focus:border-[#135bec] border-[#dbdfe6] dark:border-[#334155] h-12 placeholder:text-[#616f89] dark:placeholder:text-[#a0aec0] px-4 text-base font-normal leading-normal" placeholder="Enter your current password" type="password"/>
                                    </label>
                                    <div></div>
                                    <label className="flex flex-col">
                                        <p className="text-[#111318] dark:text-[#f0f2f4] text-base font-medium leading-normal pb-2">New Password</p>
                                        <input className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-md text-[#111318] dark:text-[#f0f2f4] bg-[#f6f6f8] dark:bg-[#101622] focus:ring-[#135bec] focus:border-[#135bec] border-[#dbdfe6] dark:border-[#334155] h-12 placeholder:text-[#616f89] dark:placeholder:text-[#a0aec0] px-4 text-base font-normal leading-normal" placeholder="Enter new password" type="password"/>
                                        <p className="text-[#616f89] dark:text-[#a0aec0] text-xs pt-1">Password must be at least 8 characters long.</p>
                                    </label>
                                    <label className="flex flex-col">
                                        <p className="text-[#111318] dark:text-[#f0f2f4] text-base font-medium leading-normal pb-2">Confirm New Password</p>
                                        <input className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-md text-[#111318] dark:text-[#f0f2f4] bg-[#f6f6f8] dark:bg-[#101622] focus:ring-[#135bec] focus:border-[#135bec] border-[#dbdfe6] dark:border-[#334155] h-12 placeholder:text-[#616f89] dark:placeholder:text-[#a0aec0] px-4 text-base font-normal leading-normal" placeholder="Confirm new password" type="password"/>
                                    </label>
                                </div>
                                <div className="flex justify-end pt-6">
                                    <button className="flex items-center justify-center font-semibold text-white bg-[#135bec] rounded-md px-5 py-2.5 h-11 text-sm leading-6 transition-colors hover:bg-[#135bec]/90">Update Password</button>
                                </div>
                            </div>
                        </section>
                        <section>
                            <h2 className="text-[#111318] dark:text-[#f0f2f4] text-[22px] font-bold leading-tight tracking-[-0.015em] pb-3 pt-5 border-b border-[#dbdfe6] dark:border-[#334155]">Notifications</h2>
                            <div className="pt-6">
                                <h3 className="text-[#111318] dark:text-[#f0f2f4] text-xl font-bold leading-tight tracking-[-0.015em] pb-1">Email Notifications</h3>
                                <p className="text-[#616f89] dark:text-[#a0aec0] text-sm pb-5">Manage your email notification preferences.</p>
                                <div className="flex flex-col gap-4">
                                    <div className="flex items-center justify-between">
                                        <div>
                                            <p className="text-[#111318] dark:text-[#f0f2f4] font-medium">New assignments posted</p>
                                            <p className="text-[#616f89] dark:text-[#a0aec0] text-sm">Get notified when a new assignment is available.</p>
                                        </div>
                                        <label className="relative inline-flex cursor-pointer items-center">
                                            <input defaultChecked className="peer sr-only" id="toggle-1" type="checkbox"/>
                                            <div className="peer h-6 w-11 rounded-full bg-gray-200 after:absolute after:start-[2px] after:top-[2px] after:h-5 after:w-5 after:rounded-full after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-[#135bec] peer-checked:after:translate-x-full peer-checked:after:border-white peer-focus:outline-none dark:border-gray-600 dark:bg-gray-700"></div>
                                        </label>
                                    </div>
                                    <div className="flex items-center justify-between">
                                        <div>
                                            <p className="text-[#111318] dark:text-[#f0f2f4] font-medium">Feedback from coach</p>
                                            <p className="text-[#616f89] dark:text-[#a0aec0] text-sm">Receive an email when your coach provides feedback.</p>
                                        </div>
                                        <label className="relative inline-flex cursor-pointer items-center">
                                            <input defaultChecked className="peer sr-only" id="toggle-2" type="checkbox"/>
                                            <div className="peer h-6 w-11 rounded-full bg-gray-200 after:absolute after:start-[2px] after:top-[2px] after:h-5 after:w-5 after:rounded-full after:border after:border-gray-300 after:bg-white after:transition-all after:content-[''] peer-checked:bg-[#135bec] peer-checked:after:translate-x-full peer-checked:after:border-white peer-focus:outline-none dark:border-gray-600 dark:bg-gray-700"></div>
                                        </label>
                                    </div>
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

export default SettingsPage;

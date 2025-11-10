
import React from 'react';
import { NavigationProps } from '../types';

const NotificationsPage: React.FC<NavigationProps> = ({ navigateTo }) => {
  return (
    <div className="bg-[#f6f6f8] dark:bg-[#101622] font-display min-h-screen">
        <main className="flex-1 flex flex-col h-screen overflow-hidden bg-[#F8F9FA] dark:bg-[#101622]">
            <header className="flex flex-wrap justify-between items-center gap-3 p-6 border-b border-[#DEE2E6] dark:border-gray-800 bg-white dark:bg-[#101622]">
                <p className="text-[#343A40] dark:text-gray-100 text-2xl font-bold leading-tight tracking-tight min-w-72">Notification Center</p>
                <div className="flex items-center gap-4">
                    <button className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-gray-100 dark:bg-gray-800 text-[#343A40] dark:text-gray-200 text-sm font-medium leading-normal tracking-[0.015em] hover:bg-gray-200 dark:hover:bg-gray-700">
                        <span className="truncate">Mark all as read</span>
                    </button>
                </div>
            </header>
            <div className="flex flex-1 overflow-hidden">
                <div className="w-full md:w-1/3 border-r border-[#DEE2E6] dark:border-gray-800 bg-white dark:bg-[#101622] flex flex-col overflow-y-auto">
                    <div className="flex gap-2 p-4 flex-wrap border-b border-[#DEE2E6] dark:border-gray-800 sticky top-0 bg-white dark:bg-[#101622] z-10">
                        <button className="flex h-8 shrink-0 items-center justify-center gap-x-2 rounded-full bg-[#4A90E2] text-white px-4">
                            <p className="text-sm font-medium leading-normal">All</p>
                        </button>
                        <button className="flex h-8 shrink-0 items-center justify-center gap-x-2 rounded-full bg-gray-100 dark:bg-gray-800 px-4 hover:bg-gray-200 dark:hover:bg-gray-700">
                            <p className="text-[#343A40] dark:text-gray-300 text-sm font-medium leading-normal">Unread</p>
                        </button>
                    </div>
                    <div className="flex flex-col divide-y divide-[#DEE2E6] dark:divide-gray-800">
                        <div className="flex items-start gap-3 p-4 cursor-pointer bg-[#135bec]/10 dark:bg-[#135bec]/20 border-l-4 border-[#4A90E2]">
                            <div className="text-white flex items-center justify-center rounded-lg bg-[#50E3C2] shrink-0 size-10 mt-1">
                                <span className="material-symbols-outlined">school</span>
                            </div>
                            <div className="flex flex-col justify-center grow">
                                <p className="text-[#343A40] dark:text-gray-100 text-sm font-bold leading-normal">Grade Posted: Your submission for 'Data Structures Intro' has been graded.</p>
                                <p className="text-gray-500 dark:text-gray-400 text-xs font-normal leading-normal">2 hours ago</p>
                            </div>
                        </div>
                        <div className="flex items-start gap-3 p-4 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800/50">
                            <div className="w-2.5 h-2.5 bg-[#4A90E2] rounded-full mt-2.5 shrink-0"></div>
                            <div className="text-white flex items-center justify-center rounded-lg bg-[#F5A623] shrink-0 size-10">
                                <span className="material-symbols-outlined">chat_bubble</span>
                            </div>
                            <div className="flex flex-col justify-center grow">
                                <p className="text-[#343A40] dark:text-gray-100 text-sm font-bold leading-normal">New Feedback: You have new feedback from Coach Turing on 'Algorithm Design'.</p>
                                <p className="text-gray-500 dark:text-gray-400 text-xs font-normal leading-normal">Yesterday</p>
                            </div>
                        </div>
                        <div className="flex items-start gap-3 p-4 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800/50 opacity-70">
                            <div className="w-2.5 h-2.5 bg-transparent rounded-full mt-2.5 shrink-0"></div>
                            <div className="text-white flex items-center justify-center rounded-lg bg-[#4A90E2] shrink-0 size-10">
                                <span className="material-symbols-outlined">assignment_ind</span>
                            </div>
                            <div className="flex flex-col justify-center grow">
                                <p className="text-[#343A40] dark:text-gray-300 text-sm font-medium leading-normal">New Student Assigned: Jane Doe has been added to your roster.</p>
                                <p className="text-gray-500 dark:text-gray-400 text-xs font-normal leading-normal">2 days ago</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="w-full md:w-2/3 flex-col p-8 overflow-y-auto bg-[#F8F9FA] dark:bg-[#101622] hidden md:flex">
                    <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm p-8">
                        <div className="flex items-center gap-4">
                            <div className="text-white flex items-center justify-center rounded-lg bg-[#50E3C2] shrink-0 size-12">
                                <span className="material-symbols-outlined text-3xl">school</span>
                            </div>
                            <div>
                                <h2 className="text-[#343A40] dark:text-gray-100 text-xl font-bold">Grade Posted</h2>
                                <p className="text-gray-500 dark:text-gray-400 text-sm">Course: CS101 - Intro to Computer Science</p>
                            </div>
                        </div>
                        <div className="border-t border-[#DEE2E6] dark:border-gray-800 my-6"></div>
                        <div className="space-y-4">
                            <p className="text-[#343A40] dark:text-gray-200 leading-relaxed">Your submission for the assignment <strong className="font-semibold text-[#4A90E2]">'Data Structures Intro'</strong> has been graded. Your score is <strong>95/100</strong>.</p>
                            <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
                                <h4 className="font-semibold text-[#343A40] dark:text-gray-200 mb-2">Coach's Comment:</h4>
                                <p className="text-gray-600 dark:text-gray-300 text-sm">"Excellent work, Alex! Your implementation of the binary search tree was efficient and well-documented. Keep up the great work on the upcoming projects."</p>
                            </div>
                            <p className="text-gray-500 dark:text-gray-400 text-sm">Posted 2 hours ago</p>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
  );
};

export default NotificationsPage;

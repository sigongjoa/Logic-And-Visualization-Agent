
import React from 'react';
import { NavigationProps } from '../types';

const StudentDetailsPage: React.FC<NavigationProps> = ({ navigateTo }) => {
  return (
    <div className="font-display bg-[#f6f6f8] dark:bg-[#101622] min-h-screen">
        <main className="flex-1 p-6 lg:p-8">
            <div className="max-w-7xl mx-auto">
                <div className="bg-white dark:bg-slate-900 rounded-xl shadow-sm p-4 @container border border-slate-200 dark:border-slate-800">
                    <div className="flex w-full flex-col gap-4 @[520px]:flex-row @[520px]:justify-between @[520px]:items-center">
                        <div className="flex gap-4">
                            <div className="bg-center bg-no-repeat aspect-square bg-cover rounded-full h-24 w-24 lg:h-32 lg:w-32 flex-shrink-0" style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuAMimzcFIqEuf-tz3HmJTxJvWvMn5mihxTs92T-fu0VoYuC0UF090gV74vn9rI0IjCv3aaZEkP2H5dOrzH9zviyMzg8ywrqf70s-wtfdQtv3lCgADC_Hk1fGBbKpyxRu_p-1e5huaG5ard9G4IgY5IcyGx9O4JlEZ17N22-tbDoNCBP_DShpYUaSmfsgsPm7Uh9MzbM4qvpuk1MPYc7pcRPbPPTsgg1zRQ5VX8wa0OvlfcKF-E08oCVBcZrSqShuIF12fCeRz7BIg")'}}></div>
                            <div className="flex flex-col justify-center">
                                <p className="text-slate-900 dark:text-slate-100 text-[22px] font-bold leading-tight tracking-[-0.015em]">Alex Johnson</p>
                                <p className="text-slate-500 dark:text-slate-400 text-base font-normal leading-normal">Logic and Critical Thinking</p>
                                <p className="text-slate-500 dark:text-slate-400 text-base font-normal leading-normal">Last active: 2 hours ago</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="flex flex-wrap gap-4 mt-6">
                    <div className="flex min-w-[111px] flex-1 basis-[fit-content] flex-col gap-2 rounded-xl border border-slate-200 dark:border-slate-800 p-4 items-start bg-white dark:bg-slate-900 shadow-sm">
                        <p className="text-slate-900 dark:text-slate-100 tracking-light text-2xl font-bold leading-tight">12</p>
                        <div className="flex items-center gap-2"><p className="text-slate-500 dark:text-slate-400 text-sm font-normal leading-normal">Courses Enrolled</p></div>
                    </div>
                    <div className="flex min-w-[111px] flex-1 basis-[fit-content] flex-col gap-2 rounded-xl border border-slate-200 dark:border-slate-800 p-4 items-start bg-white dark:bg-slate-900 shadow-sm">
                        <p className="text-slate-900 dark:text-slate-100 tracking-light text-2xl font-bold leading-tight">88%</p>
                        <div className="flex items-center gap-2"><p className="text-slate-500 dark:text-slate-400 text-sm font-normal leading-normal">Avg. Score</p></div>
                    </div>
                    <div className="flex min-w-[111px] flex-1 basis-[fit-content] flex-col gap-2 rounded-xl border border-slate-200 dark:border-slate-800 p-4 items-start bg-white dark:bg-slate-900 shadow-sm">
                        <p className="text-slate-900 dark:text-slate-100 tracking-light text-2xl font-bold leading-tight">B+</p>
                        <div className="flex items-center gap-2"><p className="text-slate-500 dark:text-slate-400 text-sm font-normal leading-normal">Current Grade</p></div>
                    </div>
                </div>
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
                    <div className="lg:col-span-2 flex flex-col gap-4">
                        <div className="flex flex-col bg-white dark:bg-slate-900 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800">
                            <div className="p-4 border-b border-slate-200 dark:border-slate-800">
                                <h2 className="text-slate-900 dark:text-slate-100 text-lg font-bold leading-tight tracking-[-0.015em]">Student Activity Timeline</h2>
                            </div>
                            <ul className="divide-y divide-slate-200 dark:divide-slate-800">
                                <li className="p-4 hover:bg-slate-50 dark:hover:bg-slate-800/50">
                                    <div className="flex items-start gap-4">
                                        <div className="bg-green-100 dark:bg-green-900/50 rounded-full size-10 flex items-center justify-center flex-shrink-0">
                                            <span className="material-symbols-outlined text-green-600 dark:text-green-400">task_alt</span>
                                        </div>
                                        <div className="flex-grow">
                                            <div className="flex justify-between items-start">
                                                <div>
                                                    <p className="font-medium text-slate-800 dark:text-slate-200">Chapter 5 Quiz Submitted</p>
                                                    <p className="text-sm text-slate-500 dark:text-slate-400">Oct 26, 2023 - 2:45 PM</p>
                                                </div>
                                                <div className="flex items-center gap-2">
                                                    <span className="inline-flex items-center rounded-md bg-green-100 dark:bg-green-900 px-2 py-1 text-xs font-medium text-green-700 dark:text-green-300">Graded</span>
                                                    <p className="font-bold text-slate-800 dark:text-slate-200">Score: 85%</p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="p-4 hover:bg-slate-50 dark:hover:bg-slate-800/50">
                                    <div className="flex items-start gap-4">
                                        <div className="bg-yellow-100 dark:bg-yellow-900/50 rounded-full size-10 flex items-center justify-center flex-shrink-0">
                                            <span className="material-symbols-outlined text-yellow-600 dark:text-yellow-400">pending</span>
                                        </div>
                                        <div className="flex-grow">
                                            <div className="flex justify-between items-start">
                                                <div>
                                                    <p className="font-medium text-slate-800 dark:text-slate-200">Logic Puzzle #3</p>
                                                    <p className="text-sm text-slate-500 dark:text-slate-400">Oct 24, 2023 - 11:10 AM</p>
                                                </div>
                                                <div className="flex items-center gap-2">
                                                    <span className="inline-flex items-center rounded-md bg-yellow-100 dark:bg-yellow-900 px-2 py-1 text-xs font-medium text-yellow-700 dark:text-yellow-300">Awaiting Review</span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
  );
};

export default StudentDetailsPage;

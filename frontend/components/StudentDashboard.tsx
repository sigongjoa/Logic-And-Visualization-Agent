
import React from 'react';
import { NavigationProps, Page } from '../types';

interface StudentDashboardProps extends NavigationProps {
    currentStudentId: string | null;
}

const ProgressRing = ({ radius, stroke, progress }: { radius: number, stroke: number, progress: number }) => {
    const normalizedRadius = radius - stroke * 2;
    const circumference = normalizedRadius * 2 * Math.PI;
    const strokeDashoffset = circumference - (progress / 100) * circumference;

    return (
        <svg height={radius * 2} width={radius * 2} className="-rotate-90">
            <circle
                stroke="currentColor"
                fill="transparent"
                strokeWidth={stroke}
                className="text-gray-200 dark:text-gray-700"
                r={normalizedRadius}
                cx={radius}
                cy={radius}
            />
            <circle
                stroke="currentColor"
                fill="transparent"
                strokeWidth={stroke}
                strokeDasharray={circumference + ' ' + circumference}
                style={{ strokeDashoffset }}
                strokeLinecap="round"
                className="text-[#50E3C2] transition-all duration-300"
                r={normalizedRadius}
                cx={radius}
                cy={radius}
            />
        </svg>
    );
};

const StudentDashboard: React.FC<StudentDashboardProps> = ({ navigateTo, currentStudentId }) => {
  return (
    <div className="font-display bg-[#F4F7F9] dark:bg-[#101622] text-[#333333] dark:text-[#E0E0E0] min-h-screen">
        <main className="flex-1 px-6 sm:px-10 lg:px-20 py-8">
            <div className="max-w-7xl mx-auto">
                <div className="mb-8">
                    <h1 className="text-3xl md:text-4xl font-black tracking-[-0.033em] text-[#333333] dark:text-white">Welcome back, Alex!</h1>
                    <p className="text-base text-gray-500 dark:text-gray-400 mt-1">Here's a snapshot of your learning journey today.</p>
                </div>
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <div className="lg:col-span-2 flex flex-col gap-8">
                        <div className="bg-white dark:bg-[#101622]/50 p-6 rounded-xl border border-gray-200 dark:border-gray-700">
                            <h2 className="text-xl font-bold tracking-[-0.015em] mb-4">My Learning Status</h2>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <div className="flex flex-col gap-2 rounded-lg p-6 border border-gray-200 dark:border-gray-700 bg-[#F4F7F9] dark:bg-gray-800 items-center justify-center text-center">
                                    <div className="relative size-32">
                                        <ProgressRing radius={64} stroke={10} progress={75} />
                                        <div className="absolute inset-0 flex items-center justify-center">
                                            <p className="text-2xl font-bold">75%</p>
                                        </div>
                                    </div>
                                    <p className="text-base font-medium mt-2">Overall Progress</p>
                                    <p className="text-sm text-green-500 font-medium">+5% this month</p>
                                </div>
                                <div className="flex flex-col gap-2 rounded-lg p-6 border border-gray-200 dark:border-gray-700 bg-[#F4F7F9] dark:bg-gray-800 justify-center">
                                    <p className="text-base font-medium">Courses Completed</p>
                                    <p className="text-3xl font-bold">4</p>
                                    <p className="text-sm text-green-500 font-medium">+1 this month</p>
                                </div>
                                <div className="flex flex-col gap-2 rounded-lg p-6 border border-gray-200 dark:border-gray-700 bg-[#F4F7F9] dark:bg-gray-800 justify-center">
                                    <p className="text-base font-medium">Skills Mastered</p>
                                    <p className="text-3xl font-bold">12</p>
                                    <p className="text-sm text-green-500 font-medium">+2 this month</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="flex flex-col gap-8">
                        <div className="bg-white dark:bg-[#101622]/50 p-6 rounded-xl border border-gray-200 dark:border-gray-700">
                            <div className="flex justify-between items-center mb-4">
                                <h2 className="text-xl font-bold tracking-[-0.015em]">Upcoming Assignments</h2>
                                <button onClick={() => navigateTo(Page.SubmissionHistory, currentStudentId)} className="text-sm font-medium text-[#4A90E2] hover:underline">View All</button>
                            </div>
                            <div className="space-y-4">
                                <div onClick={() => navigateTo(Page.AssignmentSubmission)} className="flex items-start gap-4 p-4 rounded-lg bg-[#F4F7F9] dark:bg-gray-800 hover:shadow-md transition-shadow cursor-pointer">
                                    <div className="flex-shrink-0 size-10 flex items-center justify-center rounded-full bg-[#4A90E2]/20 text-[#4A90E2]">
                                        <span className="material-symbols-outlined">description</span>
                                    </div>
                                    <div>
                                        <p className="font-semibold">UX Design Principles Essay</p>
                                        <p className="text-sm text-gray-500 dark:text-gray-400">Interaction Design Course</p>
                                        <p className="text-sm font-medium text-[#F5A623] mt-1">Due in 3 days</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
  );
};

export default StudentDashboard;

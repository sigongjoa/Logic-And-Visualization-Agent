
import React from 'react';
import { NavigationProps } from '../types';

const SubmissionHistoryPage: React.FC<NavigationProps> = ({ navigateTo }) => {
  return (
    <div className="bg-[#F8F9FA] dark:bg-[#101622] font-display text-[#111318] dark:text-white min-h-screen">
        <main className="px-4 lg:px-10 py-8">
            <div className="flex flex-col max-w-7xl mx-auto flex-1 gap-8">
                <div className="flex flex-wrap justify-between gap-4 items-center">
                    <div className="flex min-w-72 flex-col gap-2">
                        <p className="text-[#111318] dark:text-white text-4xl font-black leading-tight tracking-[-0.033em]">Submission History</p>
                        <p className="text-[#616f89] dark:text-gray-400 text-base font-normal leading-normal">Review all your past submissions and feedback.</p>
                    </div>
                </div>
                <div className="flex flex-col">
                    <div className="overflow-x-auto">
                        <div className="inline-block min-w-full align-middle">
                            <div className="overflow-hidden rounded-xl border border-[#dbdfe6] dark:border-gray-700 bg-white dark:bg-[#1C2431]">
                                <table className="min-w-full divide-y divide-[#dbdfe6] dark:divide-gray-700">
                                    <thead className="bg-[#F8F9FA] dark:bg-[#101622]">
                                        <tr>
                                            <th className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-[#111318] dark:text-white sm:pl-6" scope="col">Assignment</th>
                                            <th className="px-3 py-3.5 text-left text-sm font-semibold text-[#111318] dark:text-white" scope="col">Date</th>
                                            <th className="px-3 py-3.5 text-left text-sm font-semibold text-[#111318] dark:text-white" scope="col">Status</th>
                                            <th className="px-3 py-3.5 text-left text-sm font-semibold text-[#111318] dark:text-white" scope="col">Score</th>
                                            <th className="relative py-3.5 pl-3 pr-4 sm:pr-6" scope="col">
                                                <span className="sr-only">View Details</span>
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-[#dbdfe6] dark:divide-gray-700 bg-white dark:bg-[#1C2431]">
                                        <tr className="hover:bg-[#F8F9FA] dark:hover:bg-[#101622] cursor-pointer">
                                            <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-[#111318] dark:text-white sm:pl-6">Data Structures Final Project</td>
                                            <td className="whitespace-nowrap px-3 py-4 text-sm text-[#616f89] dark:text-gray-400">Dec 15, 2023</td>
                                            <td className="whitespace-nowrap px-3 py-4 text-sm">
                                                <span className="inline-flex items-center rounded-full bg-green-100 dark:bg-green-900/50 px-2.5 py-0.5 text-xs font-medium text-green-800 dark:text-green-300">Graded</span>
                                            </td>
                                            <td className="whitespace-nowrap px-3 py-4 text-sm font-semibold text-[#111318] dark:text-white">95/100</td>
                                            <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                                                <a className="text-[#4A90E2] hover:text-[#4A90E2]/80" href="#">View Details</a>
                                            </td>
                                        </tr>
                                        <tr className="hover:bg-[#F8F9FA] dark:hover:bg-[#101622] cursor-pointer">
                                            <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-[#111318] dark:text-white sm:pl-6">Algorithm Analysis Homework 3</td>
                                            <td className="whitespace-nowrap px-3 py-4 text-sm text-[#616f89] dark:text-gray-400">Nov 28, 2023</td>
                                            <td className="whitespace-nowrap px-3 py-4 text-sm">
                                                <span className="inline-flex items-center rounded-full bg-green-100 dark:bg-green-900/50 px-2.5 py-0.5 text-xs font-medium text-green-800 dark:text-green-300">Graded</span>
                                            </td>
                                            <td className="whitespace-nowrap px-3 py-4 text-sm font-semibold text-[#111318] dark:text-white">88/100</td>
                                            <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                                                <a className="text-[#4A90E2] hover:text-[#4A90E2]/80" href="#">View Details</a>
                                            </td>
                                        </tr>
                                        <tr className="hover:bg-[#F8F9FA] dark:hover:bg-[#101622] cursor-pointer">
                                            <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-[#111318] dark:text-white sm:pl-6">Advanced Logic Gates Lab</td>
                                            <td className="whitespace-nowrap px-3 py-4 text-sm text-[#616f89] dark:text-gray-400">Nov 10, 2023</td>
                                            <td className="whitespace-nowrap px-3 py-4 text-sm">
                                                <span className="inline-flex items-center rounded-full bg-orange-100 dark:bg-orange-900/50 px-2.5 py-0.5 text-xs font-medium text-orange-800 dark:text-orange-300">Needs Revision</span>
                                            </td>
                                            <td className="whitespace-nowrap px-3 py-4 text-sm text-[#616f89] dark:text-gray-400">-</td>
                                            <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                                                <a className="text-[#4A90E2] hover:text-[#4A90E2]/80" href="#">View Details</a>
                                            </td>
                                        </tr>
                                        <tr className="hover:bg-[#F8F9FA] dark:hover:bg-[#101622] cursor-pointer">
                                            <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-[#111318] dark:text-white sm:pl-6">Intro to Visualization Essay</td>
                                            <td className="whitespace-nowrap px-3 py-4 text-sm text-[#616f89] dark:text-gray-400">Oct 30, 2023</td>
                                            <td className="whitespace-nowrap px-3 py-4 text-sm">
                                                <span className="inline-flex items-center rounded-full bg-yellow-100 dark:bg-yellow-900/50 px-2.5 py-0.5 text-xs font-medium text-yellow-800 dark:text-yellow-300">Pending</span>
                                            </td>
                                            <td className="whitespace-nowrap px-3 py-4 text-sm text-[#616f89] dark:text-gray-400">-</td>
                                            <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                                                <a className="text-[#4A90E2] hover:text-[#4A90E2]/80" href="#">View Details</a>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
  );
};

export default SubmissionHistoryPage;

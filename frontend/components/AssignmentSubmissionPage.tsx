
import React from 'react';
import { NavigationProps } from '../types';

const AssignmentSubmissionPage: React.FC<NavigationProps> = ({ navigateTo }) => {
  return (
    <div className="bg-[#F0F2F5] dark:bg-[#101622] font-display text-[#2A323A] min-h-screen">
        <main className="w-full max-w-screen-2xl mx-auto p-6 lg:p-10">
            <div className="flex flex-col gap-6">
                <div className="flex flex-wrap gap-2">
                    <span className="text-[#616f89] dark:text-gray-400 text-sm font-medium leading-normal">Introduction to Astrophysics</span>
                    <span className="text-[#616f89] dark:text-gray-400 text-sm font-medium leading-normal">/</span>
                    <span className="text-[#616f89] dark:text-gray-400 text-sm font-medium leading-normal">Assignments</span>
                    <span className="text-[#616f89] dark:text-gray-400 text-sm font-medium leading-normal">/</span>
                    <span className="text-[#2A323A] dark:text-white text-sm font-medium leading-normal">Essay: The Life Cycle of a Star</span>
                </div>
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <div className="lg:col-span-1 flex flex-col gap-6">
                        <div className="bg-white dark:bg-[#101622]/50 p-6 rounded-xl border border-[#e5e7eb] dark:border-gray-700">
                            <div className="flex flex-col gap-3">
                                <p className="text-[#2A323A] dark:text-white text-2xl font-bold leading-tight tracking-[-0.033em]">Essay: The Life Cycle of a Star</p>
                                <div className="flex items-center text-sm font-medium text-[#616f89] dark:text-gray-400">
                                    <span className="material-symbols-outlined text-base mr-1.5">calendar_today</span>
                                    <span>Due: October 26, 2023, 11:59 PM</span>
                                </div>
                                <div className="flex items-center text-sm font-medium text-yellow-600 dark:text-yellow-500 bg-yellow-100 dark:bg-yellow-900/30 px-2 py-1 rounded-md self-start">
                                    <span className="material-symbols-outlined text-base mr-1.5">hourglass_empty</span>
                                    <span>Not Submitted</span>
                                </div>
                            </div>
                        </div>
                        <div className="bg-white dark:bg-[#101622]/50 p-6 rounded-xl border border-[#e5e7eb] dark:border-gray-700 flex-grow">
                            <h3 className="text-[#2A323A] dark:text-white text-lg font-bold leading-tight tracking-[-0.015em] pb-3 border-b border-[#e5e7eb] dark:border-gray-700">Instructions</h3>
                            <p className="text-[#2A323A] dark:text-gray-300 text-base font-normal leading-relaxed pt-4">
                                Write a 1500-word essay detailing the complete life cycle of a star, from its formation in a nebula to its eventual end as a white dwarf, neutron star, or black hole. Please reference the attached documents for grading criteria and recommended sources.
                            </p>
                            <h3 className="text-[#2A323A] dark:text-white text-lg font-bold leading-tight tracking-[-0.015em] pb-2 pt-6 mt-4 border-t border-[#e5e7eb] dark:border-gray-700">Attachments</h3>
                            <ul className="space-y-3 mt-3">
                                <li className="flex items-center justify-between bg-[#F0F2F5] dark:bg-gray-700/50 p-3 rounded-lg">
                                    <div className="flex items-center gap-3">
                                        <span className="material-symbols-outlined text-[#3A7CA5]">description</span>
                                        <span className="text-[#2A323A] dark:text-gray-300 text-sm font-medium">Grading_Rubric.pdf</span>
                                    </div>
                                    <a className="text-[#3A7CA5] hover:underline text-sm font-bold" href="#">Download</a>
                                </li>
                                <li className="flex items-center justify-between bg-[#F0F2F5] dark:bg-gray-700/50 p-3 rounded-lg">
                                    <div className="flex items-center gap-3">
                                        <span className="material-symbols-outlined text-[#3A7CA5]">article</span>
                                        <span className="text-[#2A323A] dark:text-gray-300 text-sm font-medium">Research_Sources.docx</span>
                                    </div>
                                    <a className="text-[#3A7CA5] hover:underline text-sm font-bold" href="#">Download</a>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div className="lg:col-span-2 flex flex-col bg-white dark:bg-[#101622]/50 rounded-xl border border-[#e5e7eb] dark:border-gray-700">
                        <div className="flex-grow flex flex-col">
                            <div className="border-b border-[#e5e7eb] dark:border-gray-700 px-6">
                                <nav aria-label="Tabs" className="-mb-px flex space-x-6">
                                    <button aria-current="page" className="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm text-[#3A7CA5] border-[#3A7CA5]">Write Submission</button>
                                    <button className="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm text-[#616f89] dark:text-gray-400 border-transparent hover:text-[#2A323A] dark:hover:text-white hover:border-gray-300">Upload File</button>
                                </nav>
                            </div>
                            <div className="p-6 flex-grow flex flex-col">
                                <div className="bg-[#F0F2F5] dark:bg-gray-700/50 border border-[#e5e7eb] dark:border-gray-600 rounded-t-lg p-2 flex items-center gap-2">
                                    <button className="p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-600"><span className="material-symbols-outlined text-lg">format_bold</span></button>
                                    <button className="p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-600"><span className="material-symbols-outlined text-lg">format_italic</span></button>
                                    <button className="p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-600"><span className="material-symbols-outlined text-lg">format_list_bulleted</span></button>
                                    <button className="p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-600"><span className="material-symbols-outlined text-lg">format_list_numbered</span></button>
                                    <button className="p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-600"><span className="material-symbols-outlined text-lg">link</span></button>
                                </div>
                                <textarea className="w-full flex-grow p-4 border-x border-b border-[#e5e7eb] dark:border-gray-600 rounded-b-lg resize-none focus:ring-2 focus:ring-[#3A7CA5] focus:border-[#3A7CA5] dark:bg-[#101622]/50 dark:text-gray-200" placeholder="Start writing your response here..."></textarea>
                                <div className="text-right text-xs text-[#616f89] dark:text-gray-500 pt-2">Draft saved at 2:15 PM</div>
                            </div>
                        </div>
                        <div className="p-6 border-t border-[#e5e7eb] dark:border-gray-700 bg-[#F0F2F5]/50 dark:bg-[#101622]/30 rounded-b-xl flex justify-end items-center gap-4">
                            <button className="flex items-center justify-center rounded-lg h-11 px-6 bg-[#F0F2F5] dark:bg-gray-700 text-[#2A323A] dark:text-gray-200 text-sm font-bold hover:bg-gray-300 dark:hover:bg-gray-600">Save Draft</button>
                            <button className="flex items-center justify-center rounded-lg h-11 px-8 bg-[#3A7CA5] text-white text-sm font-bold hover:bg-[#3A7CA5]/90">Submit Assignment</button>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
  );
};

export default AssignmentSubmissionPage;

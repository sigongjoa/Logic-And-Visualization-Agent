
import React, { useState } from 'react';
import { NavigationProps } from '../types';
import { generateFeedback } from '../services/geminiService';

const AssignmentReviewPage: React.FC<NavigationProps> = ({ navigateTo }) => {
    const [isLoading, setIsLoading] = useState(false);
    const [score, setScore] = useState<number | string>("");
    const [feedback, setFeedback] = useState(
`Excellent summary of UCD principles, John. You've clearly grasped the core concepts of user research and iterative design.
For your next assignment, try to include a specific, real-world example to illustrate one of the principles. For instance, you could discuss how a company like Airbnb used user feedback to refine their booking process. This will make your analysis even stronger.
Great work overall!`
    );
    const [showBanner, setShowBanner] = useState(true);

    const studentSubmissionText = `
        <h4>Introduction to User-Centered Design</h4>
        <p>User-centered design (UCD) is an iterative design process in which designers focus on the users and their needs in each phase of the design process. In UCD, design teams involve users throughout the design process via a variety of research and design techniques, to create highly usable and accessible products for them.</p>
        <h4>Key Principles</h4>
        <p>The core principles of UCD revolve around understanding the user's context, requirements, and feedback. This involves several key activities:</p>
        <ul>
        <li><strong>User Research:</strong> Conducting interviews, surveys, and observational studies to understand the user's behaviors, goals, and motivations.</li>
        <li><strong>Persona Creation:</strong> Developing fictional characters based on user research to represent the different user types that might use a service, product, site, or brand in a similar way.</li>
        <li><strong>Prototyping & Testing:</strong> Creating wireframes, mockups, or interactive prototypes to test with actual users. This iterative process allows for early feedback and refinement before significant development resources are invested.</li>
        </ul>
        <h4>Conclusion</h4>
        <p>By placing the user at the heart of the design process, we can create products that are not only functional but also enjoyable and intuitive to use. This approach ultimately leads to higher user satisfaction and product success. It ensures that the final product will meet the expectations and needs of the target audience, reducing the risk of failure in the market.</p>
        <p>The continuous feedback loop in UCD is what makes it so powerful. It's not about getting it right the first time, but about iterating towards the best possible solution based on real user data.</p>
    `;

    const handleGenerateFeedback = async () => {
        setIsLoading(true);
        setShowBanner(true);
        const plainTextSubmission = studentSubmissionText.replace(/<[^>]*>?/gm, ' ');
        const result = await generateFeedback(plainTextSubmission);
        setFeedback(result.feedback);
        setScore(result.score);
        setIsLoading(false);
    };


  return (
    <div className="bg-[#f6f6f8] dark:bg-[#101622] font-display min-h-screen">
        <main className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="flex flex-col gap-6">
                <div className="flex flex-col gap-4">
                    <div className="flex flex-wrap items-center gap-2">
                        <span className="text-slate-500 dark:text-slate-400 text-sm font-medium leading-normal">All Assignments</span>
                        <span className="text-slate-400 dark:text-slate-500 text-sm font-medium leading-normal">/</span>
                        <span className="text-slate-500 dark:text-slate-400 text-sm font-medium leading-normal">UX Design Principles</span>
                        <span className="text-slate-400 dark:text-slate-500 text-sm font-medium leading-normal">/</span>
                        <span className="text-slate-800 dark:text-white text-sm font-medium leading-normal">John Doe</span>
                    </div>
                    <div className="flex flex-wrap justify-between gap-4 items-start">
                        <div className="flex min-w-72 flex-col gap-1">
                            <p className="text-slate-900 dark:text-white text-3xl font-bold leading-tight tracking-tight">UX Design Principles</p>
                            <p className="text-slate-500 dark:text-slate-400 text-sm font-normal leading-normal">Submitted On Time: Oct 26, 2023, 11:59 PM</p>
                        </div>
                    </div>
                </div>
                <div className="grid grid-cols-1 lg:grid-cols-2 lg:gap-8 gap-y-8">
                    <div className="flex flex-col gap-4">
                        <h3 className="text-slate-900 dark:text-white text-lg font-bold leading-tight tracking-[-0.015em]">Student Submission</h3>
                        <div className="bg-white dark:bg-slate-900/70 border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm">
                            <div className="p-4 sm:p-6 border-b border-slate-200 dark:border-slate-800">
                                <div className="flex items-center gap-4">
                                    <div className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10" style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuCR-K6qvwsOC5Xy6OZgnRz-K9FgX06m1A9-GxbV0BwLZPVzlQ5tRAigZibxFsJpS15Px3v4OdWuX80PEDWRYe4FOXT1VXHCqQxF1VUsa3kk_WtcY3_WAB0bOSPk-eUklodK0JdE7w8AuJcJJh6sqQ3cU7yIyO3k44ZMSBDNsvlNU2t_oartfvbbDQjTHZtRgM4rYQApIhxacJCpSAI78h-pyDasKcMlhXT-2zPfKF8-4nwtgH3qxqiGh7kmrHEAmvs5NoVThb5bkw")'}}></div>
                                    <p className="text-slate-800 dark:text-slate-200 text-base font-semibold leading-normal flex-1 truncate">John Doe</p>
                                </div>
                            </div>
                            <div className="p-4 sm:p-6 prose prose-slate dark:prose-invert max-w-none" dangerouslySetInnerHTML={{ __html: studentSubmissionText }}/>
                        </div>
                    </div>
                    <div className="flex flex-col gap-4">
                        <div className="flex justify-between items-center">
                            <h3 className="text-slate-900 dark:text-white text-lg font-bold leading-tight tracking-[-0.015em]">Coach Assessment</h3>
                             <button onClick={handleGenerateFeedback} disabled={isLoading} className="flex items-center justify-center rounded-lg h-10 bg-[#135bec] text-white gap-2 text-sm font-bold leading-normal tracking-[-0.015em] px-4 hover:bg-[#135bec]/90 disabled:opacity-50 disabled:cursor-not-allowed">
                                <span className="material-symbols-outlined text-xl">auto_awesome</span>
                                {isLoading ? 'Generating...' : 'Generate AI Feedback'}
                            </button>
                        </div>
                        <div className="bg-white dark:bg-slate-900/70 border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm p-4 sm:p-6 flex flex-col gap-6">
                            {showBanner && (
                            <div className="flex items-start gap-4 p-4 rounded-lg bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800/50">
                                <span className="material-symbols-outlined text-xl text-yellow-600 dark:text-yellow-500 mt-0.5">auto_awesome</span>
                                <div className="flex-1">
                                    <p className="font-semibold text-yellow-800 dark:text-yellow-300">AI-Generated Draft</p>
                                    <p className="text-sm text-yellow-700 dark:text-yellow-400">Please review and edit this initial feedback before sending it to the student.</p>
                                </div>
                                <button onClick={() => setShowBanner(false)} className="text-yellow-600 dark:text-yellow-500 hover:text-yellow-800 dark:hover:text-yellow-300">
                                    <span className="material-symbols-outlined text-xl">close</span>
                                </button>
                            </div>
                            )}
                            <div className="flex flex-col gap-2">
                                <label className="text-sm font-medium text-slate-700 dark:text-slate-300" htmlFor="final-score">Final Score</label>
                                <div className="relative">
                                    <input value={score} onChange={e => setScore(e.target.value)} className="w-32 rounded-lg border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-[#135bec] focus:border-[#135bec]" id="final-score" max="100" min="0" name="final-score" placeholder="--" type="number"/>
                                    <span className="absolute inset-y-0 left-24 flex items-center pr-3 text-slate-500 dark:text-slate-400">/ 100</span>
                                </div>
                            </div>
                            <div className="flex flex-col gap-2">
                                <label className="text-sm font-medium text-slate-700 dark:text-slate-300" htmlFor="written-feedback">Written Feedback</label>
                                <div className="rounded-lg border border-slate-300 dark:border-slate-700 focus-within:ring-2 focus-within:ring-[#135bec] focus-within:border-[#135bec]">
                                    <div className="p-2 border-b border-slate-300 dark:border-slate-700 flex items-center gap-2">
                                        <button className="p-1.5 rounded hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-300"><span className="material-symbols-outlined text-xl">format_bold</span></button>
                                        <button className="p-1.5 rounded hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-300"><span className="material-symbols-outlined text-xl">format_italic</span></button>
                                        <button className="p-1.5 rounded hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-300"><span className="material-symbols-outlined text-xl">format_list_bulleted</span></button>
                                    </div>
                                    <textarea value={feedback} onChange={e => setFeedback(e.target.value)} className="w-full border-0 bg-transparent p-3 focus:ring-0 text-slate-700 dark:text-slate-200 placeholder:text-slate-400 dark:placeholder:text-slate-500" id="written-feedback" name="written-feedback" placeholder="Provide constructive feedback for the student..." rows={10}></textarea>
                                </div>
                            </div>
                            <div className="flex items-center justify-end gap-4 pt-4 border-t border-slate-200 dark:border-slate-800">
                                <button className="text-sm font-medium text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white">Save Draft</button>
                                <button className="flex items-center justify-center rounded-lg h-11 bg-[#135bec] text-white gap-2 text-sm font-bold leading-normal tracking-[-0.015em] px-6 hover:bg-[#135bec]/90 disabled:opacity-50 disabled:cursor-not-allowed">
                                    Send Feedback
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
  );
};

export default AssignmentReviewPage;

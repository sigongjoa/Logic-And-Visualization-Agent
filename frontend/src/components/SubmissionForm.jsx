import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createSubmission } from '../api';

const SubmissionForm = () => {
    const [problemText, setProblemText] = useState('');
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    // Hardcode student ID for now
    const studentId = "std_test_1";

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);

        if (!problemText.trim()) {
            setError("Problem text cannot be empty.");
            return;
        }

        try {
            const submissionData = { student_id: studentId, problem_text: problemText };
            const result = await createSubmission(submissionData);
            // Assuming the result page can handle the submission object
            navigate('/submission-result', { state: { result } });
        } catch (err) {
            setError(err.message || 'An error occurred during submission.');
            console.error('Submission error:', err);
        }
    };

    return (
        <main className="flex-grow w-full max-w-screen-2xl mx-auto p-6 lg:p-10">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-1 flex flex-col gap-6">
                    <div className="bg-white dark:bg-background-dark/50 p-6 rounded-xl border border-border-color dark:border-gray-700">
                        <h2 className="text-text-body dark:text-white text-2xl font-bold leading-tight tracking-[-0.033em]">Submit Your Problem</h2>
                        <p className="text-text-body dark:text-gray-300 text-base font-normal leading-relaxed pt-4">
                            Enter the problem you are working on below. Our AI will analyze it and provide a step-by-step visual explanation.
                        </p>
                    </div>
                </div>
                <div className="lg:col-span-2 flex flex-col bg-white dark:bg-background-dark/50 rounded-xl border border-border-color dark:border-gray-700">
                    <form onSubmit={handleSubmit} className="flex-grow flex flex-col">
                        <div className="p-6 flex-grow flex flex-col">
                            <textarea
                                className="w-full flex-grow p-4 border border-border-color dark:border-gray-600 rounded-lg resize-none focus:ring-2 focus:ring-primary focus:border-primary dark:bg-background-dark/50 dark:text-gray-200"
                                placeholder="Start writing your problem here..."
                                value={problemText}
                                onChange={(e) => setProblemText(e.target.value)}
                                rows="10"
                            ></textarea>
                            {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
                        </div>
                        <div className="p-6 border-t border-border-color dark:border-gray-700 bg-secondary/50 dark:bg-background-dark/30 rounded-b-xl flex justify-end items-center gap-4">
                            <button type="submit" className="flex items-center justify-center rounded-lg h-11 px-8 bg-primary text-white text-sm font-bold hover:bg-primary/90">
                                Submit for Analysis
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </main>
    );
};

export default SubmissionForm;

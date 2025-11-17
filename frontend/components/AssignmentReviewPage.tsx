import React, { useState, useEffect } from 'react';
import { NavigationProps } from '../types';
import { getSubmission, reviewSubmission, Submission } from '../services/api';

const AssignmentReviewPage: React.FC<NavigationProps> = ({ navigateTo }) => {
    const [submission, setSubmission] = useState<Submission | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [feedback, setFeedback] = useState('');
    const [decision, setDecision] = useState<'approved' | 'needs_revision'>('approved');

    // Hardcoded for now, this would typically come from the URL (e.g., react-router)
    const submissionId = "sub_d680c06d"; // Replace with a real ID from your test runs if needed

    useEffect(() => {
        const fetchSubmission = async () => {
            try {
                setIsLoading(true);
                const sub = await getSubmission(submissionId);
                setSubmission(sub);
                setError(null);
            } catch (err) {
                setError('Failed to load submission data. Please try again.');
                console.error(err);
            } finally {
                setIsLoading(false);
            }
        };

        fetchSubmission();
    }, [submissionId]);

    const handleSubmitReview = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!submission) return;

        setIsLoading(true);
        try {
            await reviewSubmission(submission.submission_id, {
                coach_id: 'coach_review_test', // Hardcoded coach_id
                decision,
                coach_feedback: feedback,
            });
            alert('Review submitted successfully!');
            // Optionally, navigate away or show a success message
        } catch (err) {
            setError('Failed to submit review. Please try again.');
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    if (isLoading) {
        return <div className="p-8">Loading submission...</div>;
    }

    if (error) {
        return <div className="p-8 text-red-500">{error}</div>;
    }

    if (!submission) {
        return <div className="p-8">No submission found.</div>;
    }

    return (
        <div className="bg-[#f6f6f8] dark:bg-[#101622] font-display min-h-screen p-8">
            <main className="w-full max-w-4xl mx-auto">
                <h1 className="text-3xl font-bold mb-4">Review Submission</h1>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {/* Student Submission Column */}
                    <div className="flex flex-col gap-4">
                        <h3 className="text-lg font-bold">Student's Problem</h3>
                        <div className="bg-white dark:bg-slate-900/70 p-4 rounded-lg border">
                            <p>{submission.problem_text}</p>
                        </div>
                        <h3 className="text-lg font-bold">AI's Logical Path</h3>
                        <div className="bg-white dark:bg-slate-900/70 p-4 rounded-lg border">
                            <p>{submission.logical_path_text}</p>
                        </div>
                    </div>

                    {/* Coach Review Column */}
                    <div className="flex flex-col gap-4">
                        <h3 className="text-lg font-bold">Your Review</h3>
                        <form onSubmit={handleSubmitReview} className="bg-white dark:bg-slate-900/70 p-4 rounded-lg border flex flex-col gap-4">
                            <div>
                                <label className="block text-sm font-medium mb-2">Decision</label>
                                <div className="flex gap-4">
                                    <button type="button" onClick={() => setDecision('approved')} className={`px-4 py-2 rounded-lg ${decision === 'approved' ? 'bg-green-500 text-white' : 'bg-gray-200'}`}>
                                        Approve
                                    </button>
                                    <button type="button" onClick={() => setDecision('needs_revision')} className={`px-4 py-2 rounded-lg ${decision === 'needs_revision' ? 'bg-red-500 text-white' : 'bg-gray-200'}`}>
                                        Needs Revision
                                    </button>
                                </div>
                            </div>
                            <div>
                                <label htmlFor="feedback" className="block text-sm font-medium mb-2">Feedback</label>
                                <textarea
                                    id="feedback"
                                    value={feedback}
                                    onChange={(e) => setFeedback(e.target.value)}
                                    className="w-full p-2 border rounded-lg"
                                    rows={6}
                                    placeholder="Provide your feedback here..."
                                    required
                                />
                            </div>
                            <button type="submit" disabled={isLoading} className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400">
                                {isLoading ? 'Submitting...' : 'Submit Review'}
                            </button>
                        </form>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default AssignmentReviewPage;

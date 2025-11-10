import React, { useState, useEffect } from 'react';
import { getStudentSubmissions } from '../api';
import { Link } from 'react-router-dom';

const StudentHistory = () => {
    const [studentId, setStudentId] = useState('std_test_1'); // Default student ID
    const [submissions, setSubmissions] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchHistory = async () => {
        setLoading(true);
        setError(null);
        try {
            const submissionsData = await getStudentSubmissions(studentId);
            setSubmissions(submissionsData);
        } catch (err) {
            setError('Failed to fetch submission history.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchHistory();
    }, [studentId]);

    return (
        <main className="px-4 lg:px-10 py-8">
            <div className="layout-content-container flex flex-col max-w-7xl mx-auto flex-1 gap-8">
                <div className="flex flex-wrap justify-between gap-4 items-center">
                    <div className="flex min-w-72 flex-col gap-2">
                        <p className="text-[#111318] dark:text-white text-4xl font-black leading-tight tracking-[-0.033em]">Submission History</p>
                        <p className="text-[#616f89] dark:text-gray-400 text-base font-normal leading-normal">Review all your past submissions and feedback.</p>
                    </div>
                    <div className="input-group">
                        <label htmlFor="studentId">Student ID:</label>
                        <input
                          type="text"
                          id="studentId"
                          value={studentId}
                          onChange={(e) => setStudentId(e.target.value)}
                          placeholder="Enter Student ID"
                        />
                        <button onClick={fetchHistory}>Fetch History</button>
                    </div>
                </div>

                {loading && <p>Loading history...</p>}
                {error && <p className="error">{error}</p>}
                
                <div className="flex flex-col">
                    <div className="overflow-x-auto">
                        <div className="inline-block min-w-full align-middle">
                            <div className="overflow-hidden rounded-xl border border-[#dbdfe6] dark:border-gray-700 bg-white dark:bg-[#1C2431]">
                                <table className="min-w-full divide-y divide-[#dbdfe6] dark:divide-gray-700">
                                    <thead className="bg-background-light dark:bg-background-dark">
                                        <tr>
                                            <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-[#111318] dark:text-white sm:pl-6">Assignment</th>
                                            <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-[#111318] dark:text-white">Date</th>
                                            <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-[#111318] dark:text-white">Status</th>
                                            <th scope="col" className="relative py-3.5 pl-3 pr-4 sm:pr-6">
                                                <span className="sr-only">View Details</span>
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-[#dbdfe6] dark:divide-gray-700 bg-white dark:bg-[#1C2431]">
                                        {submissions.map((sub) => (
                                            <tr key={sub.submission_id} className="hover:bg-background-light dark:hover:bg-background-dark cursor-pointer">
                                                <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-[#111318] dark:text-white sm:pl-6">{sub.problem_text}</td>
                                                <td className="whitespace-nowrap px-3 py-4 text-sm text-[#616f89] dark:text-gray-400">{new Date(sub.submitted_at).toLocaleDateString()}</td>
                                                <td className="whitespace-nowrap px-3 py-4 text-sm">
                                                    <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                                                        sub.status === 'COMPLETE' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                                                    }`}>
                                                        {sub.status}
                                                    </span>
                                                </td>
                                                <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                                                    <Link to={`/coach/submissions/${sub.submission_id}`} className="text-primary hover:text-primary/80">View Details</Link>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    );
};

export default StudentHistory;
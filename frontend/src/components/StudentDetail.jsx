import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getStudent, getStudentSubmissions, getCoachMemos } from '../api';

const StudentDetail = () => {
    const { studentId } = useParams();
    const [student, setStudent] = useState(null);
    const [submissions, setSubmissions] = useState([]);
    const [memos, setMemos] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const studentData = await getStudent(studentId);
                const submissionsData = await getStudentSubmissions(studentId);
                const memosData = await getCoachMemos(studentId);
                setStudent(studentData);
                setSubmissions(submissionsData);
                setMemos(memosData);
                setError(null);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [studentId]);

    if (loading) {
        return <div>Loading student details...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    if (!student) {
        return <div>Student not found.</div>;
    }

    return (
        <main className="flex-1 p-6 lg:p-8">
            <div className="max-w-7xl mx-auto">
                {/* ProfileHeader */}
                <div className="bg-white dark:bg-slate-900 rounded-xl shadow-sm p-4 border border-slate-200 dark:border-slate-800">
                    <div className="flex w-full flex-col gap-4">
                        <div className="flex gap-4">
                            <div className="flex flex-col justify-center">
                                <p className="text-slate-900 dark:text-slate-100 text-[22px] font-bold leading-tight tracking-[-0.015em]">{student.student_name}</p>
                                <p className="text-slate-500 dark:text-slate-400 text-base font-normal leading-normal">{student.student_id}</p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Main Content Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
                    {/* Left Column: Activity Timeline */}
                    <div className="lg:col-span-2 flex flex-col gap-4">
                        <div className="flex flex-col bg-white dark:bg-slate-900 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800">
                            <div className="p-4 border-b border-slate-200 dark:border-slate-800">
                                <h2 className="text-slate-900 dark:text-slate-100 text-lg font-bold leading-tight tracking-[-0.015em]">Student Activity Timeline</h2>
                            </div>
                            <ul className="divide-y divide-slate-200 dark:divide-slate-800">
                                {submissions.map(sub => (
                                    <li key={sub.submission_id} className="p-4 hover:bg-slate-50 dark:hover:bg-slate-800/50">
                                        <div className="flex items-start gap-4">
                                            <div className="flex-grow">
                                                <p className="font-medium text-slate-800 dark:text-slate-200">{sub.logical_path_text}</p>
                                                <p className="text-sm text-slate-500 dark:text-slate-400">{new Date(sub.submitted_at).toLocaleString()}</p>
                                            </div>
                                            <div className="flex items-center gap-2">
                                                <span className={`inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ${sub.status === 'PENDING' ? 'bg-yellow-100 text-yellow-700' : 'bg-green-100 text-green-700'}`}>{sub.status}</span>
                                            </div>
                                        </div>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>

                    {/* Right Column: Coach Memos */}
                    <div className="lg:col-span-1 flex flex-col gap-4">
                        <div className="bg-white dark:bg-slate-900 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800">
                            <div className="p-4 border-b border-slate-200 dark:border-slate-800">
                                <h2 className="text-slate-900 dark:text-slate-100 text-lg font-bold leading-tight tracking-[-0.015em]">Private Coach Memos</h2>
                            </div>
                            <ul className="divide-y divide-slate-200 dark:divide-slate-800">
                                {memos.map(memo => (
                                    <li key={memo.memo_id} className="p-4 hover:bg-slate-50 dark:hover:bg-slate-800/50 group">
                                        <div>
                                            <p className="text-sm font-medium text-slate-800 dark:text-slate-200">{new Date(memo.created_at).toLocaleDateString()}</p>
                                            <p className="text-slate-600 dark:text-slate-400 mt-1">{memo.memo_text}</p>
                                        </div>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    );
};

export default StudentDetail;
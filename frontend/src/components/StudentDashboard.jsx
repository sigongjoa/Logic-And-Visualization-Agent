import React, { useState, useEffect } from 'react';
import { getStudent, getStudentSubmissions, getStudentMastery } from '../api';

const StudentDashboard = () => {
    const [student, setStudent] = useState(null);
    const [submissions, setSubmissions] = useState([]);
    const [mastery, setMastery] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Hardcoded student ID for now. In a real app, this would come from auth context.
    const studentId = "std_test_1";

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const studentData = await getStudent(studentId);
                const submissionsData = await getStudentSubmissions(studentId);
                const masteryData = await getStudentMastery(studentId);
                setStudent(studentData);
                setSubmissions(submissionsData);
                setMastery(masteryData);
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
        return <div>Loading student dashboard...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }
    
    const skillsMastered = mastery.filter(m => m.status === 'MASTERED').length;
    const overallProgress = mastery.length > 0 
        ? Math.round(mastery.reduce((acc, m) => acc + m.mastery_score, 0) / mastery.length)
        : 0;

    return (
        <main className="flex-1 px-6 sm:px-10 lg:px-20 py-8">
            <div className="max-w-7xl mx-auto">
                <div className="mb-8">
                    <h1 className="text-3xl md:text-4xl font-black tracking-[-0.033em] text-text-light dark:text-white">Welcome back, {student?.student_name}!</h1>
                    <p className="text-base text-gray-500 dark:text-gray-400 mt-1">Here's a snapshot of your learning journey today.</p>
                </div>
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <div className="lg:col-span-2 flex flex-col gap-8">
                        <div className="bg-white dark:bg-background-dark/50 p-6 rounded-xl border border-gray-200 dark:border-gray-700">
                            <h2 className="text-xl font-bold tracking-[-0.015em] mb-4">My Learning Status</h2>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <div className="flex flex-col gap-2 rounded-lg p-6 border border-gray-200 dark:border-gray-700 bg-background-light dark:bg-gray-800 items-center justify-center text-center">
                                    <p className="text-2xl font-bold">{overallProgress}%</p>
                                    <p className="text-base font-medium mt-2">Overall Progress</p>
                                </div>
                                <div className="flex flex-col gap-2 rounded-lg p-6 border border-gray-200 dark:border-gray-700 bg-background-light dark:bg-gray-800 justify-center">
                                    <p className="text-base font-medium">Courses Completed</p>
                                    <p className="text-3xl font-bold">0</p> {/* Placeholder */}
                                </div>
                                <div className="flex flex-col gap-2 rounded-lg p-6 border border-gray-200 dark:border-gray-700 bg-background-light dark:bg-gray-800 justify-center">
                                    <p className="text-base font-medium">Skills Mastered</p>
                                    <p className="text-3xl font-bold">{skillsMastered}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="flex flex-col gap-8">
                        <div className="bg-white dark:bg-background-dark/50 p-6 rounded-xl border border-gray-200 dark:border-gray-700">
                            <h2 className="text-xl font-bold tracking-[-0.015em] mb-4">Upcoming Assignments</h2>
                            <div className="space-y-4">
                                {submissions.filter(s => s.status !== 'COMPLETE').map(sub => (
                                    <div key={sub.submission_id} className="flex items-start gap-4 p-4 rounded-lg bg-background-light dark:bg-gray-800">
                                        <div>
                                            <p className="font-semibold">{sub.problem_text}</p>
                                            <p className="text-sm text-gray-500 dark:text-gray-400">{sub.status}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    );
};

export default StudentDashboard;
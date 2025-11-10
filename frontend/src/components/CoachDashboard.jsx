import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getCoach, getStudentsByCoach, getPendingSubmissionsByCoach } from '../api';

const CoachDashboard = () => {
    const [coach, setCoach] = useState(null);
    const [students, setStudents] = useState([]);
    const [submissions, setSubmissions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Hardcoded coach ID for now. In a real app, this would come from auth context.
    const coachId = "coach_test_1";

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const coachData = await getCoach(coachId);
                const studentsData = await getStudentsByCoach(coachId);
                const submissionsData = await getPendingSubmissionsByCoach(coachId);
                setCoach(coachData);
                setStudents(studentsData);
                setSubmissions(submissionsData);
                setError(null);
            } catch (err) {
                setError(err.message);
                setCoach(null);
                setStudents([]);
                setSubmissions([]);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [coachId]);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div className="font-display bg-background-light dark:bg-background-dark text-charcoal dark:text-white">
            <main className="flex-grow w-full max-w-screen-2xl mx-auto p-6 lg:p-8">
                <div className="grid grid-cols-12 gap-6 lg:gap-8">
                    <aside className="col-span-12 lg:col-span-3">
                        <div className="flex flex-col gap-6">
                            <div className="sticky top-28 flex h-full flex-col justify-between bg-white dark:bg-background-dark rounded-xl p-4 border border-gray-200 dark:border-gray-800">
                                <div className="flex flex-col gap-4">
                                    <div className="flex items-center gap-3">
                                        <div className="flex flex-col">
                                            <h1 className="text-base font-medium leading-normal">{coach?.coach_name}</h1>
                                            <p className="text-medium-grey text-sm font-normal leading-normal">LAVA Coach</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div data-testid="my-students-list" className="bg-white dark:bg-background-dark p-4 rounded-xl border border-gray-200 dark:border-gray-800">
                                <h2 className="text-lg font-bold leading-tight tracking-[-0.015em] pb-3">My Students</h2>
                                <div className="flex flex-col gap-4 mt-4">
                                    {students.map(student => (
                                        <Link to={`/coach/students/${student.student_id}`} key={student.student_id} className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800">
                                            <div className="flex flex-col">
                                                <p className="font-semibold text-charcoal dark:text-white">{student.student_name}</p>
                                                <p className="text-sm text-medium-grey">{student.student_id}</p>
                                            </div>
                                        </Link>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </aside>
                    <div data-testid="submissions-review-list" className="col-span-12 lg:col-span-9">
                        <h1 className="text-4xl font-black leading-tight tracking-[-0.033em]">Submissions to Review</h1>
                        <div className="mt-4 flex flex-col gap-4">
                            {submissions.map(sub => (
                                <div key={sub.submission_id} className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-lg border border-gray-200 dark:border-gray-800 hover:shadow-sm">
                                    <div className="flex items-center gap-4">
                                        <div>
                                            {/* Find student name from the students list */}
                                            <p className="font-semibold text-charcoal dark:text-white">{students.find(s => s.student_id === sub.student_id)?.student_name || 'Unknown Student'}</p>
                                            <p className="text-sm text-medium-grey">{sub.logical_path_text}</p>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-4">
                                        <div className="text-right">
                                            <p className="text-sm text-medium-grey">Status</p>
                                            <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-warning/20 text-warning">{sub.status}</span>
                                        </div>
                                        <button className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-primary text-white text-sm font-bold">Review Now</button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default CoachDashboard;

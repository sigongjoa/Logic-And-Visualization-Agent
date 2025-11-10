import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getSubmission, getStudent, getStudentLatestVector } from '../api';

const AssignmentReview = () => {
    const { submissionId } = useParams();
    const [submission, setSubmission] = useState(null);
    const [student, setStudent] = useState(null);
    const [latestVector, setLatestVector] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const submissionData = await getSubmission(submissionId);
                setSubmission(submissionData);

                if (submissionData && submissionData.student_id) {
                    const studentData = await getStudent(submissionData.student_id);
                    setStudent(studentData);

                    const vectorData = await getStudentLatestVector(submissionData.student_id);
                    setLatestVector(vectorData);
                }
                setError(null);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [submissionId]);

    if (loading) {
        return <div>Loading assignment review...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    if (!submission || !student) {
        return <div>Submission or Student not found.</div>;
    }

    return (
        <main className="flex-1 p-6 lg:p-8">
            <div className="max-w-7xl mx-auto">
                <div className="bg-white dark:bg-slate-900 rounded-xl shadow-sm p-4 border border-slate-200 dark:border-slate-800">
                    <h1 className="text-slate-900 dark:text-slate-100 text-2xl font-bold leading-tight tracking-[-0.015em]">Assignment Review</h1>
                    <div className="mt-4">
                        <p className="text-slate-500 dark:text-slate-400 text-base font-normal leading-normal">Student: {student.student_name} ({student.student_id})</p>
                        <p className="text-slate-500 dark:text-slate-400 text-base font-normal leading-normal">Problem: {submission.problem_text}</p>
                        <p className="text-slate-500 dark:text-slate-400 text-base font-normal leading-normal">Logical Path: {submission.logical_path_text}</p>
                        <p className="text-slate-500 dark:text-slate-400 text-base font-normal leading-normal">Status: {submission.status}</p>
                        {submission.manim_content_url && (
                            <p className="text-slate-500 dark:text-slate-400 text-base font-normal leading-normal">Manim Video: <a href={submission.manim_content_url} target="_blank" rel="noopener noreferrer">{submission.manim_content_url}</a></p>
                        )}
                    </div>
                </div>

                <div className="bg-white dark:bg-slate-900 rounded-xl shadow-sm p-4 border border-slate-200 dark:border-slate-800 mt-6">
                    <h2 className="text-slate-900 dark:text-slate-100 text-lg font-bold leading-tight tracking-[-0.015em]">Student's Latest 4-Axis Model</h2>
                    {latestVector ? (
                        <div className="mt-4 grid grid-cols-2 gap-2">
                            <p>Axis 1 Geo: {latestVector.axis1_geo}</p>
                            <p>Axis 1 Alg: {latestVector.axis1_alg}</p>
                            <p>Axis 1 Ana: {latestVector.axis1_ana}</p>
                            <p>Axis 2 Opt: {latestVector.axis2_opt}</p>
                            <p>Axis 2 Piv: {latestVector.axis2_piv}</p>
                            <p>Axis 2 Dia: {latestVector.axis2_dia}</p>
                            <p>Axis 3 Con: {latestVector.axis3_con}</p>
                            <p>Axis 3 Pro: {latestVector.axis3_pro}</p>
                            <p>Axis 3 Ret: {latestVector.axis3_ret}</p>
                            <p>Axis 4 Acc: {latestVector.axis4_acc}</p>
                            <p>Axis 4 Gri: {latestVector.axis4_gri}</p>
                        </div>
                    ) : (
                        <p className="mt-4 text-slate-500 dark:text-slate-400">No latest 4-axis vector data available.</p>
                    )}
                </div>

                {/* Placeholder for Coach Feedback/Assessment UI */}
                <div className="bg-white dark:bg-slate-900 rounded-xl shadow-sm p-4 border border-slate-200 dark:border-slate-800 mt-6">
                    <h2 className="text-slate-900 dark:text-slate-100 text-lg font-bold leading-tight tracking-[-0.015em]">Coach Feedback</h2>
                    <textarea className="w-full rounded-lg border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 focus:ring-primary focus:border-primary mt-4" rows="5" placeholder="Enter your feedback here..."></textarea>
                    <button className="mt-2 flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-primary text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-primary/90">Save Feedback</button>
                </div>
            </div>
        </main>
    );
};

export default AssignmentReview;

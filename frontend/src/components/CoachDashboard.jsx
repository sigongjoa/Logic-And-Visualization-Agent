import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getStudents } from '../api';

const CoachDashboard = () => {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStudents = async () => {
      try {
        const studentsData = await getStudents();
        setStudents(studentsData);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchStudents();
  }, []);

  if (loading) {
    return <div className="coach-dashboard-container">Loading students...</div>;
  }

  if (error) {
    return <div className="coach-dashboard-container">Error: {error.message}</div>;
  }

  return (
    <div className="coach-dashboard-container">
      <h2>Coach Dashboard</h2>
      <h3>Students</h3>
      <ul className="student-list">
        {students.map((student) => (
          <li key={student.student_id} className="student-list-item">
            <Link to={`/coach/students/${student.student_id}`}>
              {student.student_name} ({student.student_id})
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CoachDashboard;

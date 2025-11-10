
import React from 'react';
import { Page, UserType } from '../types';

interface SidebarProps {
  navigateTo: (page: Page) => void;
  onLogout: () => void;
  userType: UserType | null;
}

const Sidebar: React.FC<SidebarProps> = ({ navigateTo, onLogout, userType }) => {
    const coachPages = [
        { name: 'Coach Dashboard', page: Page.CoachDashboard },
        { name: 'Student Details', page: Page.StudentDetails },
        { name: 'Assignment Review', page: Page.AssignmentReview },
    ];

    const studentPages = [
        { name: 'Student Dashboard', page: Page.StudentDashboard },
        { name: 'Assignment Submission', page: Page.AssignmentSubmission },
        { name: 'Submission History', page: Page.SubmissionHistory },
    ];

    const commonPages = [
        { name: 'Notifications', page: Page.Notifications },
        { name: 'Curriculum', page: Page.Curriculum },
        { name: 'Settings', page: Page.Settings },
    ];

    const pagesToShow = userType === 'coach' ? coachPages : studentPages;

  return (
    <aside className="fixed top-0 left-0 h-screen w-64 bg-white dark:bg-[#101622] text-slate-800 dark:text-slate-200 border-r border-slate-200 dark:border-slate-800 flex flex-col p-4 z-50">
      <div className="flex items-center gap-3 mb-6">
        <div className="size-8 text-[#135bec]">
            <svg fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                <path d="M36.7273 44C33.9891 44 31.6043 39.8386 30.3636 33.69C29.123 39.8386 26.7382 44 24 44C21.2618 44 18.877 39.8386 17.6364 33.69C16.3957 39.8386 14.0109 44 11.2727 44C7.25611 44 4 35.0457 4 24C4 12.9543 7.25611 4 11.2727 4C14.0109 4 16.3957 8.16144 17.6364 14.31C18.877 8.16144 21.2618 4 24 4C26.7382 4 29.123 8.16144 30.3636 14.31C31.6043 8.16144 33.9891 4 36.7273 4C40.7439 4 44 12.9543 44 24C44 35.0457 40.7439 44 36.7273 44Z" fill="currentColor"></path>
            </svg>
        </div>
        <h2 className="text-lg font-bold">LAVA Showcase</h2>
      </div>
      <p className="px-2 text-xs font-semibold text-slate-400 uppercase mb-2">My Views</p>
      <nav className="flex-grow">
        <ul>
          {pagesToShow.map(item => (
            <li key={item.name}>
              <button onClick={() => navigateTo(item.page)} className="w-full text-left px-3 py-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-sm font-medium">
                {item.name}
              </button>
            </li>
          ))}
        </ul>
        <p className="px-2 text-xs font-semibold text-slate-400 uppercase mt-4 mb-2">Common</p>
         <ul>
          {commonPages.map(item => (
            <li key={item.name}>
              <button onClick={() => navigateTo(item.page)} className="w-full text-left px-3 py-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-sm font-medium">
                {item.name}
              </button>
            </li>
          ))}
        </ul>
      </nav>
      <div className="mt-auto">
        <button onClick={onLogout} className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 text-red-600 dark:text-red-400 text-sm font-medium">
             <span className="material-symbols-outlined text-xl">logout</span>
            Logout
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;

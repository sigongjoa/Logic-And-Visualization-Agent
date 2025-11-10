
export enum Page {
  Login,
  CoachDashboard,
  StudentDashboard,
  AssignmentReview,
  AssignmentSubmission,
  Curriculum,
  Notifications,
  StudentDetails,
  SubmissionHistory,
  Settings,
}

export type UserType = 'student' | 'coach';

export interface NavigationProps {
  navigateTo: (page: Page) => void;
  userType: UserType | null;
}

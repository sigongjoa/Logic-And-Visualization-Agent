import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import CoachReportReview from './CoachReportReview';

// Mock the API calls to prevent actual network requests during tests
vi.mock('../api', () => ({
  getDraftReports: vi.fn(() => Promise.resolve([])), // Mock to return an empty array of reports
  getReportDetails: vi.fn(() => Promise.resolve({})),
  finalizeReport: vi.fn(() => Promise.resolve({})),
  sendReport: vi.fn(() => Promise.resolve({})),
}));

describe('CoachReportReview', () => {
  it('renders the Coach Report Review heading', () => {
    render(<CoachReportReview />);
    expect(screen.getByText(/Coach Report Review/i)).toBeInTheDocument();
  });

  it('displays "No draft reports available." when no reports are fetched', async () => {
    render(<CoachReportReview />);
    expect(await screen.findByText(/No draft reports available./i)).toBeInTheDocument();
  });
});
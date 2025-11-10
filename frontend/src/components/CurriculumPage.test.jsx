import React from 'react';
import { render, screen, waitFor, fireEvent, within } from '@testing-library/react';
import { vi } from 'vitest';
import CurriculumPage from './CurriculumPage';
import * as api from '../api';

// Mock the api module
vi.mock('../api');

const mockCurriculums = [
  { curriculum_id: 'CUR_1', curriculum_name: 'Math' },
];

const mockConcepts = [
  { concept_id: 'C1', curriculum_id: 'CUR_1', concept_name: 'Algebra', description: 'Learn Algebra' },
  { concept_id: 'C2', curriculum_id: 'CUR_1', concept_name: 'Calculus', description: 'Learn Calculus' },
];

const mockRelations = [
  { from_concept_id: 'C1', to_concept_id: 'C2', relation_type: 'REQUIRES' },
];

describe('CurriculumPage', () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  test('renders loading state and then the curriculum data', async () => {
    api.getCurriculums.mockResolvedValue(mockCurriculums);
    api.getConcepts.mockResolvedValue(mockConcepts);
    api.getConceptRelations.mockResolvedValue(mockRelations);

    render(<CurriculumPage />);

    expect(screen.getByText(/Loading curriculum data.../i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('Math')).toBeInTheDocument();
    });

    expect(screen.getByText('Algebra')).toBeInTheDocument();
    expect(screen.getByText('Calculus')).toBeInTheDocument();
  });

  test('shows concept details when a concept is clicked', async () => {
    api.getCurriculums.mockResolvedValue(mockCurriculums);
    api.getConcepts.mockResolvedValue(mockConcepts);
    api.getConceptRelations.mockResolvedValue(mockRelations);

    render(<CurriculumPage />);

    await waitFor(() => {
      expect(screen.getByText('Calculus')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText('Calculus'));

    await waitFor(() => {
      expect(screen.getByText('Learn Calculus')).toBeInTheDocument();
    });
    
    const detailsPanel = screen.getByTestId('concept-details');
    expect(within(detailsPanel).getByText('Prerequisites')).toBeInTheDocument();
    expect(within(detailsPanel).getByText('Algebra')).toBeInTheDocument();
  });

  test('renders error state on API failure', async () => {
    const errorMessage = 'Failed to fetch';
    api.getCurriculums.mockRejectedValue(new Error(errorMessage));
    api.getConcepts.mockRejectedValue(new Error(errorMessage));
    api.getConceptRelations.mockRejectedValue(new Error(errorMessage));

    render(<CurriculumPage />);

    await waitFor(() => {
      expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument();
    });
  });
});

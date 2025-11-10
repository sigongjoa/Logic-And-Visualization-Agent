import React, { useState, useEffect } from 'react';
import { getCurriculums, getConcepts, getConceptRelations } from '../api';

const CurriculumPage = () => {
    const [curriculums, setCurriculums] = useState([]);
    const [concepts, setConcepts] = useState([]);
    const [relations, setRelations] = useState([]);
    const [selectedConcept, setSelectedConcept] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const [curriculumsData, conceptsData, relationsData] = await Promise.all([
                    getCurriculums(),
                    getConcepts(),
                    getConceptRelations(),
                ]);
                setCurriculums(curriculumsData);
                setConcepts(conceptsData);
                setRelations(relationsData);
                setError(null);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    const handleConceptClick = (concept) => {
        setSelectedConcept(concept);
    };
    
    const getPrerequisites = (conceptId) => {
        return relations
            .filter(r => r.to_concept_id === conceptId && r.relation_type === 'REQUIRES')
            .map(r => concepts.find(c => c.concept_id === r.from_concept_id))
            .filter(Boolean); // Filter out any undefined concepts
    };

    if (loading) {
        return <div>Loading curriculum data...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <main className="flex-1 flex flex-col p-6 lg:p-10">
            <div className="flex flex-col gap-4 mb-6">
                <h1 className="text-slate-900 dark:text-slate-100 text-3xl lg:text-4xl font-black leading-tight tracking-[-0.033em]">Curriculum Knowledge Graph</h1>
            </div>
            <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-6 min-h-[600px]">
                <div className="lg:col-span-2 flex flex-col bg-white dark:bg-slate-900/50 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm p-6">
                    <h2 className="text-xl font-bold mb-4">Curriculums and Concepts</h2>
                    {curriculums.map(curr => (
                        <div key={curr.curriculum_id} className="mb-4">
                            <h3 className="text-lg font-semibold">{curr.curriculum_name}</h3>
                            <ul className="list-disc pl-5">
                                {concepts.filter(c => c.curriculum_id === curr.curriculum_id).map(concept => (
                                    <li key={concept.concept_id} onClick={() => handleConceptClick(concept)} className="cursor-pointer hover:text-primary">
                                        {concept.concept_name}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    ))}
                </div>
                <aside data-testid="concept-details" className="lg:col-span-1 flex flex-col bg-white dark:bg-slate-900/50 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm p-6 space-y-6">
                    {selectedConcept ? (
                        <>
                            <div className="flex flex-col gap-2">
                                <h3 className="text-2xl font-bold text-slate-900 dark:text-slate-100">{selectedConcept.concept_name}</h3>
                                <p className="text-slate-500 dark:text-slate-400 text-sm leading-relaxed">{selectedConcept.description || "No description available."}</p>
                            </div>
                            <div className="flex flex-col gap-4">
                                <h4 className="text-sm font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">Prerequisites</h4>
                                {getPrerequisites(selectedConcept.concept_id).length > 0 ? (
                                    getPrerequisites(selectedConcept.concept_id).map(prereq => (
                                        <div key={prereq.concept_id} className="flex items-center gap-3 p-3 rounded-lg bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-800">
                                            <span className="font-medium text-slate-800 dark:text-slate-200">{prereq.concept_name}</span>
                                        </div>
                                    ))
                                ) : (
                                    <p className="text-slate-500 dark:text-slate-400 text-sm">No prerequisites for this concept.</p>
                                )}
                            </div>
                        </>
                    ) : (
                        <div className="flex items-center justify-center h-full">
                            <p className="text-slate-500 dark:text-slate-400">Select a concept to see its details.</p>
                        </div>
                    )}
                </aside>
            </div>
        </main>
    );
};

export default CurriculumPage;

/**
 * src/pages/EducationPage.jsx — Training hub / Education landing page.
 *
 * Displays:
 *   - Difficulty selector (Beginner / Intermediate / Advanced / Mixed)
 *   - Grid of scenario cards loaded from the API
 *   - Progress summary bar
 *   - Start Training button → navigates to SimulationPage
 *
 * TODO (Phase 4): Implement full scenario grid with ScenarioCard components,
 *                 DifficultySelector, and ProgressTracker components.
 */

import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/client'
import { DIFFICULTIES, SESSION_ID_KEY } from '../utils/constants'

const DIFFICULTY_LABELS = {
    all: { label: 'All Levels', emoji: '🎯' },
    beginner: { label: 'Beginner', emoji: '🟢' },
    intermediate: { label: 'Intermediate', emoji: '🟡' },
    advanced: { label: 'Advanced', emoji: '🔴' },
}

function EducationPage() {
    const [scenarios, setScenarios] = useState([])
    const [selectedDifficulty, setSelectedDifficulty] = useState('all')
    const [loading, setLoading] = useState(true)
    const navigate = useNavigate()

    useEffect(() => {
        const params = selectedDifficulty === 'all' ? '?limit=20' : `?difficulty=${selectedDifficulty}&limit=20`
        setLoading(true)
        api.get(`/scenarios${params}`)
            .then(data => setScenarios(data))
            .catch(console.error)
            .finally(() => setLoading(false))
    }, [selectedDifficulty])

    return (
        <div style={{ maxWidth: 1100, margin: '0 auto', padding: '3rem 1.5rem' }}>
            <h1 style={{ fontWeight: 800, fontSize: '2rem', color: '#e2e8f0', marginBottom: '0.5rem' }}>
                🎓 Phishing Training Hub
            </h1>
            <p style={{ color: '#64748b', marginBottom: '2.5rem' }}>
                Test your ability to identify phishing emails with real-world simulation scenarios.
            </p>

            {/* Difficulty Selector */}
            <div style={{ display: 'flex', gap: '0.75rem', marginBottom: '2rem', flexWrap: 'wrap' }}>
                {Object.entries(DIFFICULTY_LABELS).map(([key, { label, emoji }]) => (
                    <button
                        key={key}
                        onClick={() => setSelectedDifficulty(key)}
                        style={{
                            background: selectedDifficulty === key ? 'rgba(59,130,246,0.2)' : '#1e293b',
                            border: `1px solid ${selectedDifficulty === key ? '#3b82f6' : '#334155'}`,
                            color: selectedDifficulty === key ? '#60a5fa' : '#94a3b8',
                            padding: '0.5rem 1.25rem',
                            borderRadius: '2rem',
                            cursor: 'pointer',
                            fontWeight: selectedDifficulty === key ? 600 : 400,
                            fontSize: '0.875rem',
                            transition: 'all 0.15s ease',
                        }}
                    >
                        {emoji} {label}
                    </button>
                ))}
            </div>

            {/* Scenario Grid */}
            {loading ? (
                <p style={{ color: '#64748b', textAlign: 'center', padding: '3rem 0' }}>
                    Loading scenarios...
                </p>
            ) : scenarios.length === 0 ? (
                <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
                    <p style={{ color: '#64748b' }}>
                        No scenarios found. Run <code style={{ color: '#60a5fa' }}>python seed_scenarios.py</code> to seed the database.
                    </p>
                </div>
            ) : (
                <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
                    gap: '1rem',
                    marginBottom: '2rem',
                }}>
                    {scenarios.map(scenario => (
                        <div key={scenario.id} className="card">
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
                                <span style={{
                                    fontSize: '0.75rem',
                                    fontWeight: 600,
                                    padding: '0.25rem 0.625rem',
                                    borderRadius: '1rem',
                                    ...(scenario.difficulty === 'beginner'
                                        ? { background: '#166534', color: '#86efac' }
                                        : scenario.difficulty === 'intermediate'
                                            ? { background: '#713f12', color: '#fde68a' }
                                            : { background: '#7f1d1d', color: '#fca5a5' }
                                    ),
                                }}>
                                    {scenario.difficulty}
                                </span>
                                <span style={{ fontSize: '0.75rem', color: '#475569', background: '#0f172a', padding: '0.25rem 0.5rem', borderRadius: '0.25rem' }}>
                                    {scenario.category?.replace(/_/g, ' ')}
                                </span>
                            </div>
                            <h3 style={{ color: '#e2e8f0', fontWeight: 600, fontSize: '1rem', margin: '0 0 1rem' }}>
                                {scenario.title}
                            </h3>
                            <button
                                onClick={() => navigate('/learn/simulate', { state: { scenarioId: scenario.id } })}
                                className="btn-primary"
                                style={{ fontSize: '0.875rem', padding: '0.5rem 1rem', width: '100%' }}
                            >
                                Start Scenario →
                            </button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}

export default EducationPage

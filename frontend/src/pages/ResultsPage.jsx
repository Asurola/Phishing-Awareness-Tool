/**
 * src/pages/ResultsPage.jsx — User learning progress dashboard.
 *
 * Retrieves and displays a session's learning progress from the API:
 *   - Overall accuracy and scenarios completed
 *   - Accuracy breakdown by difficulty (beginner / intermediate / advanced)
 *   - Weak areas (TODO Phase 4)
 *   - Encouragement messaging
 *
 * Session ID is stored in localStorage (no authentication required).
 *
 * TODO (Phase 4): Add ProgressTracker chart components (bar charts, trend lines).
 */

import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../api/client'
import { getOrCreateSessionId } from '../hooks/useAnalysis'

function AccuracyBar({ label, attempted, correct }) {
    const pct = attempted > 0 ? Math.round((correct / attempted) * 100) : 0
    const colour = pct >= 70 ? '#22c55e' : pct >= 40 ? '#f59e0b' : '#ef4444'
    return (
        <div style={{ marginBottom: '1rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.375rem' }}>
                <span style={{ color: '#94a3b8', fontSize: '0.875rem', textTransform: 'capitalize' }}>{label}</span>
                <span style={{ color, fontWeight: 600, fontSize: '0.875rem' }}>
                    {pct}% ({correct}/{attempted})
                </span>
            </div>
            <div style={{ height: 8, background: '#1e293b', borderRadius: 4, overflow: 'hidden' }}>
                <div style={{
                    height: '100%',
                    width: `${pct}%`,
                    background: colour,
                    borderRadius: 4,
                    transition: 'width 0.5s ease',
                }} />
            </div>
        </div>
    )
}

function ResultsPage() {
    const [progress, setProgress] = useState(null)
    const [loading, setLoading] = useState(true)
    const sessionId = getOrCreateSessionId()

    useEffect(() => {
        api.get(`/progress/${sessionId}`)
            .then(data => setProgress(data))
            .catch(console.error)
            .finally(() => setLoading(false))
    }, [sessionId])

    const overallPct = progress
        ? progress.total_attempted > 0
            ? Math.round((progress.total_correct / progress.total_attempted) * 100)
            : 0
        : 0

    const encouragement = overallPct >= 80
        ? '🏆 Excellent! You\'re a phishing detection expert.'
        : overallPct >= 60
            ? '👍 Good progress! Keep practising to improve.'
            : overallPct >= 40
                ? '📚 Getting there — review the explanations to learn the indicators.'
                : '🚀 Keep going! Every scenario makes you safer.'

    return (
        <div style={{ maxWidth: 800, margin: '0 auto', padding: '3rem 1.5rem' }}>
            <h1 style={{ fontWeight: 800, fontSize: '2rem', color: '#e2e8f0', marginBottom: '0.5rem' }}>
                📊 My Progress
            </h1>
            <p style={{ color: '#64748b', marginBottom: '2.5rem' }}>
                Your phishing detection training results.
            </p>

            {loading ? (
                <p style={{ color: '#64748b', textAlign: 'center' }}>Loading progress...</p>
            ) : !progress || progress.total_attempted === 0 ? (
                <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
                    <p style={{ color: '#64748b', marginBottom: '1.5rem' }}>
                        You haven't completed any scenarios yet!
                    </p>
                    <Link to="/learn">
                        <button className="btn-primary">Start Training →</button>
                    </Link>
                </div>
            ) : (
                <>
                    {/* Overall Score */}
                    <div className="card" style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
                        <div style={{
                            fontSize: '4rem',
                            fontWeight: 800,
                            color: overallPct >= 60 ? '#22c55e' : overallPct >= 40 ? '#f59e0b' : '#ef4444',
                            lineHeight: 1,
                            marginBottom: '0.5rem',
                        }}>
                            {overallPct}%
                        </div>
                        <p style={{ color: '#94a3b8', margin: '0 0 0.5rem' }}>
                            {progress.total_correct} / {progress.total_attempted} scenarios correct
                        </p>
                        <p style={{ color: '#60a5fa', fontWeight: 500, margin: 0 }}>{encouragement}</p>
                    </div>

                    {/* By Difficulty */}
                    <div className="card">
                        <h2 style={{ color: '#e2e8f0', fontWeight: 700, marginTop: 0, fontSize: '1.125rem' }}>
                            Accuracy by Difficulty
                        </h2>
                        {Object.entries(progress.by_difficulty).map(([diff, stats]) => (
                            <AccuracyBar
                                key={diff}
                                label={diff}
                                attempted={stats.attempted}
                                correct={stats.correct}
                            />
                        ))}
                    </div>

                    <div style={{ textAlign: 'center', marginTop: '2rem' }}>
                        <Link to="/learn">
                            <button className="btn-primary">Continue Training →</button>
                        </Link>
                    </div>
                </>
            )}
        </div>
    )
}

export default ResultsPage

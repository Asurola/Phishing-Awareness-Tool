/**
 * src/pages/SimulationPage.jsx - Interactive phishing simulation page.
 *
 * Presents users with a simulated email in a realistic email viewer and
 * asks them to identify it as phishing or legitimate.
 *
 * Flow:
 *   1. Load scenario by ID (from navigation state or query param)
 *   2. Display email in a realistic email client mockup
 *   3. User selects "Phishing" or "Legitimate"
 *   4. Reveal feedback panel with explanation + learning points
 *   5. Option to proceed to next scenario or return to hub
 *
 */

import { useState, useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import api from '../api/client'
import { SESSION_ID_KEY } from '../utils/constants'
import { getOrCreateSessionId } from '../hooks/useAnalysis'

function SimulationPage() {
    const location = useLocation()
    const navigate = useNavigate()
    const scenarioId = location.state?.scenarioId || 1

    const [scenario, setScenario] = useState(null)
    const [loading, setLoading] = useState(true)
    const [answer, setAnswer] = useState(null)
    const [feedback, setFeedback] = useState(null)
    const [submitting, setSubmitting] = useState(false)
    const [startTime] = useState(Date.now())

    useEffect(() => {
        setLoading(true)
        api.get(`/scenarios/${scenarioId}`)
            .then(data => setScenario(data))
            .catch(console.error)
            .finally(() => setLoading(false))
    }, [scenarioId])

    const handleAnswer = async (selectedAnswer) => {
        if (feedback) return // Already answered
        setAnswer(selectedAnswer)
        setSubmitting(true)
        const sessionId = getOrCreateSessionId()
        const timeTaken = Math.floor((Date.now() - startTime) / 1000)

        try {
            const result = await api.post(`/scenarios/${scenarioId}/answer`, {
                session_id: sessionId,
                answer: selectedAnswer,
                time_taken_seconds: timeTaken,
            })
            setFeedback(result)
        } catch (err) {
            console.error(err)
        } finally {
            setSubmitting(false)
        }
    }

    if (loading) {
        return (
            <div style={{ textAlign: 'center', padding: '5rem', color: '#64748b' }}>
                Loading scenario...
            </div>
        )
    }

    if (!scenario) {
        return (
            <div style={{ textAlign: 'center', padding: '5rem' }}>
                <p style={{ color: '#ef4444' }}>Scenario not found.</p>
                <button className="btn-primary" onClick={() => navigate('/learn')}>Back to Hub</button>
            </div>
        )
    }

    return (
        <div style={{ maxWidth: 900, margin: '0 auto', padding: '3rem 1.5rem' }}>
            <div style={{ marginBottom: '1.5rem' }}>
                <button
                    onClick={() => navigate('/learn')}
                    style={{ background: 'none', border: 'none', color: '#64748b', cursor: 'pointer', fontSize: '0.875rem' }}
                >
                    Back to Hub
                </button>
                <h1 style={{ fontWeight: 700, fontSize: '1.5rem', color: '#e2e8f0', margin: '0.5rem 0 0.25rem' }}>
                    {scenario.title}
                </h1>
                <span style={{
                    fontSize: '0.75rem',
                    fontWeight: 600,
                    padding: '0.25rem 0.625rem',
                    borderRadius: '1rem',
                    ...(scenario.difficulty?.toLowerCase() === 'beginner'
                        ? { background: '#166534', color: '#86efac' }
                        : scenario.difficulty?.toLowerCase() === 'intermediate'
                            ? { background: '#713f12', color: '#fde68a' }
                            : { background: '#7f1d1d', color: '#fca5a5' }
                    ),
                }}>
                    {scenario.difficulty}
                </span>
            </div>

            {/* Email Viewer */}
            <div className="card" style={{ marginBottom: '1.5rem', fontFamily: 'monospace' }}>
                <div style={{
                    background: '#0f172a',
                    borderRadius: '0.5rem',
                    padding: '1.25rem',
                    whiteSpace: 'pre-wrap',
                    fontSize: '0.875rem',
                    color: '#94a3b8',
                    lineHeight: 1.7,
                    maxHeight: 400,
                    overflowY: 'auto',
                }}>
                    {scenario.email_content}
                </div>
            </div>

            {/* Answer Buttons */}
            {!feedback && (
                <div style={{
                    display: 'flex',
                    gap: '1rem',
                    justifyContent: 'center',
                    marginBottom: '1.5rem',
                }}>
                    <button
                        onClick={() => handleAnswer('phishing')}
                        className="btn-danger"
                        disabled={submitting}
                        style={{ fontSize: '1.125rem', padding: '0.875rem 2.5rem', flex: 1, maxWidth: 300 }}
                    >
                        🚨 This is Phishing
                    </button>
                    <button
                        onClick={() => handleAnswer('legitimate')}
                        className="btn-success"
                        disabled={submitting}
                        style={{ fontSize: '1.125rem', padding: '0.875rem 2.5rem', flex: 1, maxWidth: 300 }}
                    >
                        ✅ This is Legitimate
                    </button>
                </div>
            )}

            {/* Feedback Panel */}
            {feedback && (
                <div className="card" style={{
                    borderColor: feedback.correct ? 'rgba(34,197,94,0.4)' : 'rgba(239,68,68,0.4)',
                    background: feedback.correct ? 'rgba(34,197,94,0.05)' : 'rgba(239,68,68,0.05)',
                }}>
                    <h2 style={{
                        color: feedback.correct ? '#22c55e' : '#ef4444',
                        fontWeight: 700,
                        marginTop: 0,
                    }}>
                        {feedback.correct ? '✅ Correct!' : '❌ Incorrect'}
                    </h2>
                    <p style={{ color: '#94a3b8', lineHeight: 1.7 }}>{feedback.explanation}</p>

                    {feedback.learning_points?.length > 0 && (
                        <>
                            <h3 style={{ color: '#e2e8f0', fontWeight: 600 }}>Key Takeaways</h3>
                            <ul style={{ color: '#94a3b8', lineHeight: 1.8 }}>
                                {feedback.learning_points.map((point, i) => (
                                    <li key={i}>{point}</li>
                                ))}
                            </ul>
                        </>
                    )}

                    <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem' }}>
                        <button className="btn-primary" onClick={() => navigate('/learn')}>
                            Back to Hub
                        </button>
                        <button
                            style={{
                                background: '#1e293b',
                                border: '1px solid #334155',
                                color: '#94a3b8',
                                padding: '0.625rem 1.5rem',
                                borderRadius: '0.5rem',
                                cursor: 'pointer',
                            }}
                            onClick={() => navigate('/learn/progress')}
                        >
                            View Progress
                        </button>
                    </div>
                </div>
            )}
        </div>
    )
}

export default SimulationPage

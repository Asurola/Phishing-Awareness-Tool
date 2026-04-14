/**
 * src/pages/HomePage.jsx - Landing page.
 *
 * Displays:
 *   - Hero section with tool name, tagline, and two primary CTAs
 *   - "How it works" section with three feature cards
 *   - Backend health status check on mount
 *
 * TODO (Phase 3): Add quick stats for returning users (from localStorage).
 */

import { Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import api from '../api/client'

function HomePage() {
    const [healthStatus, setHealthStatus] = useState(null)

    useEffect(() => {
        api.get('/health')
            .then(data => setHealthStatus(data))
            .catch(() => setHealthStatus({ status: 'error' }))
    }, [])

    return (
        <div style={{ minHeight: '100vh' }}>
            {/* Hero Section */}
            <section style={{
                background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%)',
                padding: '5rem 1.5rem',
                textAlign: 'center',
                borderBottom: '1px solid #1e293b',
            }}>
                <div style={{ maxWidth: 800, margin: '0 auto' }}>
                    <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>🛡️</div>
                    <h1 style={{
                        fontSize: 'clamp(2rem, 5vw, 3.5rem)',
                        fontWeight: 800,
                        margin: '0 0 1rem',
                        background: 'linear-gradient(135deg, #e2e8f0, #94a3b8)',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                        lineHeight: 1.15,
                    }}>
                        PhishGuard
                    </h1>
                    <p style={{
                        fontSize: 'clamp(1rem, 2.5vw, 1.25rem)',
                        color: '#64748b',
                        margin: '0 auto 2.5rem',
                        maxWidth: 560,
                        lineHeight: 1.7,
                    }}>
                        Detect phishing emails with AI-powered analysis and train your
                        skills with real-world simulation exercises.
                    </p>
                    <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
                        <Link to="/detect">
                            <button className="btn-primary" style={{ fontSize: '1rem', padding: '0.75rem 2rem' }}>
                                🔍 Analyse an Email
                            </button>
                        </Link>
                        <Link to="/learn">
                            <button style={{
                                background: 'transparent',
                                border: '1px solid #334155',
                                color: '#94a3b8',
                                fontWeight: 600,
                                padding: '0.75rem 2rem',
                                borderRadius: '0.5rem',
                                cursor: 'pointer',
                                fontSize: '1rem',
                                transition: 'all 0.2s ease',
                            }}>
                                🎓 Test Your Skills
                            </button>
                        </Link>
                    </div>

                    {/* Health indicator */}
                    {healthStatus && (
                        <div style={{ marginTop: '2rem', fontSize: '0.8125rem', color: '#475569' }}>
                            Backend:{' '}
                            <span style={{ color: healthStatus.status === 'ok' ? '#22c55e' : '#ef4444' }}>
                                {healthStatus.status === 'ok' ? '● Connected' : '● Offline'}
                            </span>
                            {healthStatus.status === 'ok' && (
                                <> · {healthStatus.scenarios_count} training scenarios loaded</>
                            )}
                        </div>
                    )}
                </div>
            </section>

            {/* How It Works */}
            <section style={{ padding: '4rem 1.5rem' }}>
                <div style={{ maxWidth: 1100, margin: '0 auto' }}>
                    <h2 style={{
                        textAlign: 'center',
                        fontWeight: 700,
                        fontSize: '1.75rem',
                        color: '#e2e8f0',
                        marginBottom: '0.5rem',
                    }}>
                        How It Works
                    </h2>
                    <p style={{ textAlign: 'center', color: '#64748b', marginBottom: '3rem' }}>
                        Two tools. One goal: keeping you safe from phishing.
                    </p>
                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
                        gap: '1.5rem',
                    }}>
                        {[
                            {
                                icon: '📧',
                                title: '1. Submit',
                                description: 'Paste a suspicious email or upload a .eml file for instant analysis.',
                                color: '#3b82f6',
                            },
                            {
                                icon: '🔬',
                                title: '2. Analyse',
                                description: 'Our AI extracts 31 phishing features across URLs, headers, and content.',
                                color: '#a78bfa',
                            },
                            {
                                icon: '📚',
                                title: '3. Learn',
                                description: 'Understand what was found and train with simulation scenarios to sharpen your instincts.',
                                color: '#22c55e',
                            },
                        ].map(({ icon, title, description, color }) => (
                            <div key={title} className="card" style={{ textAlign: 'center' }}>
                                <div style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>{icon}</div>
                                <h3 style={{ color, fontWeight: 700, margin: '0 0 0.75rem', fontSize: '1.125rem' }}>
                                    {title}
                                </h3>
                                <p style={{ color: '#94a3b8', margin: 0, lineHeight: 1.6 }}>{description}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>
        </div>
    )
}

export default HomePage

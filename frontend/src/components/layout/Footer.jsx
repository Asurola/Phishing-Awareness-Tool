/**
 * src/components/layout/Footer.jsx - Application footer.
 *
 * Displays project attribution, quick links, and an academic project note.
 */

import { Link } from 'react-router-dom'

function Footer() {
    return (
        <footer style={{
            background: '#0f172a',
            borderTop: '1px solid #1e293b',
            padding: '2rem 1.5rem',
            marginTop: 'auto',
        }}>
            <div style={{
                maxWidth: 1200,
                margin: '0 auto',
                display: 'flex',
                flexWrap: 'wrap',
                gap: '2rem',
                justifyContent: 'space-between',
                alignItems: 'flex-start',
            }}>
                {/* Brand */}
                <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                        <span>🛡️</span>
                        <span style={{ fontWeight: 700, color: '#e2e8f0' }}>PhishGuard</span>
                    </div>
                    <p style={{ color: '#64748b', fontSize: '0.875rem', margin: 0, maxWidth: 280 }}>
                        A phishing detection and awareness training tool.
                        Academic Final Year Project.
                    </p>
                </div>

                {/* Quick Links */}
                <div>
                    <h4 style={{ color: '#94a3b8', fontSize: '0.8125rem', textTransform: 'uppercase', letterSpacing: '0.05em', margin: '0 0 0.75rem' }}>
                        Quick Links
                    </h4>
                    <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '0.375rem' }}>
                        {[
                            { to: '/detect', label: 'Analyse Email' },
                            { to: '/learn', label: 'Training Hub' },
                            { to: '/learn/simulate', label: 'Simulation' },
                            { to: '/learn/progress', label: 'My Progress' },
                        ].map(({ to, label }) => (
                            <li key={to}>
                                <Link to={to} style={{ color: '#64748b', fontSize: '0.875rem', textDecoration: 'none' }}>
                                    {label}
                                </Link>
                            </li>
                        ))}
                    </ul>
                </div>

                {/* Academic Note */}
                <div>
                    <p style={{ color: '#475569', fontSize: '0.8125rem', margin: 0 }}>
                        2026 Final Year Project<br />
                        Built with Flask + React
                    </p>
                </div>
            </div>
        </footer>
    )
}

export default Footer

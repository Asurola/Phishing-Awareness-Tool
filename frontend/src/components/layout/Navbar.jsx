/**
 * src/components/layout/Navbar.jsx - Application navigation bar.
 *
 * Displays the tool name/logo and navigation links to all main sections.
 * Uses react-router NavLink for active link highlighting.
 *
 * Links:
 *   / (Home), /detect (Analyse), /learn (Learn), /learn/progress (Progress)
 *
 */

import { NavLink } from 'react-router-dom'

const navLinks = [
    { to: '/', label: 'Home', end: true },
    { to: '/detect', label: 'Analyse Email' },
    { to: '/learn', label: 'Learn', end: true },
    { to: '/learn/progress', label: 'Progress' },
]

function Navbar() {
    return (
        <header style={{
            background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)',
            borderBottom: '1px solid #334155',
            padding: '0 1.5rem',
            position: 'sticky',
            top: 0,
            zIndex: 100,
        }}>
            <nav style={{
                maxWidth: 1200,
                margin: '0 auto',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                height: '4rem',
            }}>
                {/* Logo / Brand */}
                <NavLink to="/" style={{ textDecoration: 'none' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <span style={{ fontSize: '1.5rem' }}>🛡️</span>
                        <span style={{
                            fontWeight: 800,
                            fontSize: '1.125rem',
                            background: 'linear-gradient(135deg, #60a5fa, #a78bfa)',
                            WebkitBackgroundClip: 'text',
                            WebkitTextFillColor: 'transparent',
                            letterSpacing: '-0.02em',
                        }}>
                            PhishGuard
                        </span>
                    </div>
                </NavLink>

                {/* Navigation Links */}
                <ul style={{
                    display: 'flex',
                    gap: '0.25rem',
                    listStyle: 'none',
                    margin: 0,
                    padding: 0,
                }}>
                    {navLinks.map(({ to, label, end }) => (
                        <li key={to}>
                            <NavLink
                                to={to}
                                end={end}
                                style={({ isActive }) => ({
                                    textDecoration: 'none',
                                    color: isActive ? '#60a5fa' : '#94a3b8',
                                    fontWeight: isActive ? 600 : 400,
                                    fontSize: '0.9rem',
                                    padding: '0.375rem 0.875rem',
                                    borderRadius: '0.375rem',
                                    background: isActive ? 'rgba(59,130,246,0.1)' : 'transparent',
                                    transition: 'all 0.15s ease',
                                    display: 'block',
                                })}
                            >
                                {label}
                            </NavLink>
                        </li>
                    ))}
                </ul>
            </nav>
        </header>
    )
}

export default Navbar

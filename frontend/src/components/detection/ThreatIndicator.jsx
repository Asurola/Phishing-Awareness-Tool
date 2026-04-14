/**
 * src/components/detection/ThreatIndicator.jsx
 *
 * Renders the list of threat flags returned by the API.
 * Flags are grouped into category tabs: Header / URL / Content.
 * Each flag expands to show description + recommendation.
 *
 * Props:
 *   flags  - array of { category, severity, title, description, recommendation }
 */

import { useState } from 'react'

const CATEGORIES = ['all', 'header', 'url', 'content']

const CATEGORY_ICONS = {
    header:  '📬',
    url:     '🔗',
    content: '📝',
}

const SEVERITY_STYLES = {
    high:   { bg: 'rgba(239,68,68,0.12)',   border: 'rgba(239,68,68,0.35)',   text: '#fca5a5', badge: '#ef4444', label: 'HIGH' },
    medium: { bg: 'rgba(245,158,11,0.12)',  border: 'rgba(245,158,11,0.35)',  text: '#fde68a', badge: '#f59e0b', label: 'MED' },
    low:    { bg: 'rgba(148,163,184,0.08)', border: 'rgba(148,163,184,0.2)',  text: '#cbd5e1', badge: '#64748b', label: 'LOW' },
}

function SeverityBadge({ severity }) {
    const s = SEVERITY_STYLES[severity] || SEVERITY_STYLES.low
    return (
        <span style={{
            background: s.badge,
            color: '#fff',
            fontSize: '0.6875rem',
            fontWeight: 700,
            padding: '0.2rem 0.5rem',
            borderRadius: '0.25rem',
            letterSpacing: '0.05em',
            flexShrink: 0,
        }}>
            {s.label}
        </span>
    )
}

function FlagCard({ flag, index }) {
    const [open, setOpen] = useState(false)
    const s = SEVERITY_STYLES[flag.severity] || SEVERITY_STYLES.low

    return (
        <div style={{
            background: s.bg,
            border: `1px solid ${open ? s.badge : s.border}`,
            borderRadius: '0.625rem',
            marginBottom: '0.625rem',
            overflow: 'hidden',
            transition: 'border-color 0.2s',
        }}>
            {/* Header row - always visible */}
            <button
                onClick={() => setOpen(o => !o)}
                style={{
                    width: '100%',
                    background: 'none',
                    border: 'none',
                    padding: '0.875rem 1rem',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.75rem',
                    cursor: 'pointer',
                    textAlign: 'left',
                }}
            >
                <SeverityBadge severity={flag.severity} />
                <span style={{ color: s.text, fontWeight: 600, fontSize: '0.9rem', flex: 1 }}>
                    {CATEGORY_ICONS[flag.category]} {flag.title}
                </span>
                <span style={{ color: '#475569', fontSize: '0.875rem', flexShrink: 0, transition: 'transform 0.2s', display: 'inline-block', transform: open ? 'rotate(180deg)' : 'none' }}>
                    ▾
                </span>
            </button>

            {/* Expanded body */}
            {open && (
                <div style={{ padding: '0 1rem 1rem', borderTop: `1px solid ${s.border}` }}>
                    <p style={{ color: '#94a3b8', fontSize: '0.875rem', marginTop: '0.75rem', marginBottom: '0.625rem', lineHeight: 1.6 }}>
                        {flag.description}
                    </p>
                    <div style={{
                        background: 'rgba(59,130,246,0.08)',
                        border: '1px solid rgba(59,130,246,0.2)',
                        borderRadius: '0.5rem',
                        padding: '0.625rem 0.875rem',
                    }}>
                        <span style={{ color: '#60a5fa', fontSize: '0.8125rem', fontWeight: 600 }}>💡 Recommendation: </span>
                        <span style={{ color: '#93c5fd', fontSize: '0.8125rem', lineHeight: 1.6 }}>{flag.recommendation}</span>
                    </div>
                </div>
            )}
        </div>
    )
}

export default function ThreatIndicator({ flags }) {
    const [activeTab, setActiveTab] = useState('all')

    if (!flags || flags.length === 0) {
        return (
            <div style={{
                background: 'rgba(34,197,94,0.08)',
                border: '1px solid rgba(34,197,94,0.25)',
                borderRadius: '0.75rem',
                padding: '1.5rem',
                textAlign: 'center',
            }}>
                <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>✅</div>
                <p style={{ color: '#86efac', fontWeight: 600, margin: '0 0 0.25rem' }}>No threat indicators detected</p>
                <p style={{ color: '#64748b', fontSize: '0.875rem', margin: 0 }}>
                    The model did not flag any suspicious patterns in this email.
                </p>
            </div>
        )
    }

    const counts = CATEGORIES.reduce((acc, cat) => {
        acc[cat] = cat === 'all' ? flags.length : flags.filter(f => f.category === cat).length
        return acc
    }, {})

    const visible = activeTab === 'all' ? flags : flags.filter(f => f.category === activeTab)

    return (
        <div>
            {/* Category tabs */}
            <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem', flexWrap: 'wrap' }}>
                {CATEGORIES.filter(c => counts[c] > 0).map(cat => (
                    <button
                        key={cat}
                        onClick={() => setActiveTab(cat)}
                        style={{
                            background: activeTab === cat ? '#3b82f6' : '#1e293b',
                            border: `1px solid ${activeTab === cat ? '#3b82f6' : '#334155'}`,
                            color: activeTab === cat ? '#fff' : '#94a3b8',
                            borderRadius: '0.4rem',
                            padding: '0.3rem 0.85rem',
                            fontSize: '0.8125rem',
                            fontWeight: 600,
                            cursor: 'pointer',
                            textTransform: 'capitalize',
                            transition: 'all 0.15s',
                        }}
                    >
                        {cat === 'all' ? 'All' : `${CATEGORY_ICONS[cat]} ${cat}`}
                        <span style={{
                            marginLeft: '0.4rem',
                            background: activeTab === cat ? 'rgba(255,255,255,0.25)' : '#334155',
                            borderRadius: '9999px',
                            padding: '0.05rem 0.45rem',
                            fontSize: '0.75rem',
                        }}>
                            {counts[cat]}
                        </span>
                    </button>
                ))}
            </div>

            {/* Flag cards */}
            {visible.map((flag, i) => (
                <FlagCard key={`${flag.category}-${i}`} flag={flag} index={i} />
            ))}
        </div>
    )
}

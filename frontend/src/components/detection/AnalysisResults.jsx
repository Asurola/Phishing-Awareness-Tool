/**
 *
 * Top-level results panel shown after a successful API response.
 *
 * Layout (desktop):
 *   ┌─────────────────────────────────────────────────────┐
 *   │  Verdict banner (full width, colour-coded)           │
 *   ├──────────────────┬──────────────────────────────────┤
 *   │  RiskScoreGauge  │  Parsed email metadata summary   │
 *   │  (left col)      │  (right col)                     │
 *   ├──────────────────┴──────────────────────────────────┤
 *   │  Threat Indicators (flagged patterns)                │
 *   ├─────────────────────────────────────────────────────┤
 *   │  Recommendations                                     │
 *   └─────────────────────────────────────────────────────┘
 *
 * Props:
 *   result - full API response object
 *   onReset - callback to clear the result and show the form again
 */

import RiskScoreGauge from './RiskScoreGauge'
import ThreatIndicator from './ThreatIndicator'
import Recommendations from './Recommendations'

// Map verdict strings to styling
function verdictStyle(verdict) {
    if (verdict.startsWith('High')) return {
        bg: 'rgba(239,68,68,0.12)', border: 'rgba(239,68,68,0.4)',
        text: '#fca5a5', icon: '🚨', accent: '#ef4444',
    }
    if (verdict.startsWith('Elevated')) return {
        bg: 'rgba(245,158,11,0.12)', border: 'rgba(245,158,11,0.4)',
        text: '#fde68a', icon: '⚠️', accent: '#f59e0b',
    }
    if (verdict.startsWith('Low')) return {
        bg: 'rgba(34,197,94,0.08)', border: 'rgba(34,197,94,0.3)',
        text: '#86efac', icon: '🟡', accent: '#22c55e',
    }
    return {
        bg: 'rgba(34,197,94,0.07)', border: 'rgba(34,197,94,0.25)',
        text: '#86efac', icon: '✅', accent: '#22c55e',
    }
}

function MetaRow({ label, value }) {
    return (
        <div style={{ marginBottom: '0.75rem' }}>
            <span style={{ color: '#64748b', fontSize: '0.75rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                {label}
            </span>
            <p style={{
                margin: '0.2rem 0 0',
                color: '#cbd5e1',
                fontSize: '0.9rem',
                wordBreak: 'break-all',
                lineHeight: 1.5,
            }}>
                {value || <span style={{ color: '#475569', fontStyle: 'italic' }}>Not found</span>}
            </p>
        </div>
    )
}

export default function AnalysisResults({ result, onReset }) {
    if (!result) return null

    const {
        risk_score = 0,
        verdict = '',
        phishing_probability = 0,
        flags = [],
        summary_recommendations = [],
        parsed_email = {},
    } = result

    const vs = verdictStyle(verdict)
    const highCount = flags.filter(f => f.severity === 'high').length
    const medCount  = flags.filter(f => f.severity === 'medium').length
    const lowCount  = flags.filter(f => f.severity === 'low').length

    return (
        <div style={{ animation: 'fadeSlideUp 0.4s ease' }}>
            <style>{`
                @keyframes fadeSlideUp {
                    from { opacity: 0; transform: translateY(18px); }
                    to   { opacity: 1; transform: translateY(0); }
                }
            `}</style>

            {/* ── Verdict banner ───────────────────────────────────── */}
            <div style={{
                background: vs.bg,
                border: `1px solid ${vs.border}`,
                borderRadius: '0.875rem',
                padding: '1.25rem 1.5rem',
                marginBottom: '1.25rem',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                flexWrap: 'wrap',
                gap: '0.75rem',
            }}>
                <div>
                    <div style={{ fontSize: '1.5rem', marginBottom: '0.25rem' }}>
                        {vs.icon} <span style={{ color: vs.text, fontWeight: 800, fontSize: '1.25rem' }}>{verdict}</span>
                    </div>
                    <div style={{ color: '#94a3b8', fontSize: '0.875rem' }}>
                        {flags.length === 0
                            ? 'No threat indicators found'
                            : `${flags.length} indicator${flags.length !== 1 ? 's' : ''} detected - ${highCount > 0 ? `${highCount} high` : ''}${highCount > 0 && medCount > 0 ? ', ' : ''}${medCount > 0 ? `${medCount} medium` : ''}${(highCount > 0 || medCount > 0) && lowCount > 0 ? ', ' : ''}${lowCount > 0 ? `${lowCount} low` : ''}`
                        }
                    </div>
                </div>
                <button
                    onClick={onReset}
                    style={{
                        background: '#1e293b',
                        border: '1px solid #334155',
                        color: '#94a3b8',
                        borderRadius: '0.5rem',
                        padding: '0.5rem 1rem',
                        fontSize: '0.875rem',
                        cursor: 'pointer',
                        transition: 'all 0.15s',
                        flexShrink: 0,
                    }}
                    onMouseEnter={e => { e.currentTarget.style.borderColor = '#475569'; e.currentTarget.style.color = '#e2e8f0' }}
                    onMouseLeave={e => { e.currentTarget.style.borderColor = '#334155'; e.currentTarget.style.color = '#94a3b8' }}
                >
                    ← Analyse Another
                </button>
            </div>

            {/* ── Gauge + Email metadata ────────────────────────────── */}
            <div style={{
                display: 'grid',
                gridTemplateColumns: 'auto 1fr',
                gap: '1.25rem',
                marginBottom: '1.25rem',
            }}
                className="results-top-grid"
            >
                {/* Gauge card */}
                <div className="card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minWidth: 240 }}>
                    <RiskScoreGauge score={risk_score} probability={phishing_probability} />
                </div>

                {/* Parsed email metadata card */}
                <div className="card">
                    <h3 style={{ margin: '0 0 1rem', fontSize: '0.9375rem', fontWeight: 700, color: '#e2e8f0' }}>
                        📧 Email Overview
                    </h3>
                    <MetaRow label="From" value={parsed_email.sender} />
                    <MetaRow label="Subject" value={parsed_email.subject} />
                    <MetaRow
                        label="Links found"
                        value={parsed_email.url_count != null
                            ? `${parsed_email.url_count} URL${parsed_email.url_count !== 1 ? 's' : ''}`
                            : null}
                    />
                    {parsed_email.body_preview && (
                        <div>
                            <span style={{ color: '#64748b', fontSize: '0.75rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                                Body preview
                            </span>
                            <pre style={{
                                margin: '0.3rem 0 0',
                                color: '#94a3b8',
                                fontSize: '0.8rem',
                                lineHeight: 1.55,
                                background: '#0f172a',
                                border: '1px solid #1e293b',
                                borderRadius: '0.5rem',
                                padding: '0.625rem 0.75rem',
                                whiteSpace: 'pre-wrap',
                                wordBreak: 'break-word',
                                maxHeight: 112,
                                overflow: 'hidden',
                            }}>
                                {parsed_email.body_preview}
                            </pre>
                        </div>
                    )}
                </div>
            </div>

            {/* ── Threat indicators ─────────────────────────────────── */}
            <div className="card" style={{ marginBottom: '1.25rem' }}>
                <h3 style={{ margin: '0 0 1rem', fontSize: '0.9375rem', fontWeight: 700, color: '#e2e8f0' }}>
                    🚩 Threat Indicators
                </h3>
                <ThreatIndicator flags={flags} />
            </div>

            {/* ── Recommendations ───────────────────────────────────── */}
            <Recommendations recommendations={summary_recommendations} riskScore={risk_score} />

            {/* Responsive: stack gauge above metadata on narrow screens */}
            <style>{`
                @media (max-width: 620px) {
                    .results-top-grid {
                        grid-template-columns: 1fr !important;
                    }
                }
            `}</style>
        </div>
    )
}

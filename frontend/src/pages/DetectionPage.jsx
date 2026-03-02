/**
 * src/pages/DetectionPage.jsx — Email analysis interface.
 *
 * Allows users to:
 *   1. Paste raw email content into a textarea
 *   2. Upload a .eml file
 *   3. Submit for analysis and view the risk assessment
 *
 * Phase 1: Shows placeholder UI with form wired to the API (returns stub response).
 * Phase 3: Will display full risk gauge, threat flags, and recommendations.
 *
 * TODO (Phase 3): Implement AnalysisResults, RiskScoreGauge, ThreatIndicator,
 *                 Recommendations components to display real analysis output.
 */

import { useState } from 'react'
import api from '../api/client'

function DetectionPage() {
    const [rawEmail, setRawEmail] = useState('')
    const [result, setResult] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const handleSubmit = async (e) => {
        e.preventDefault()
        if (!rawEmail.trim()) {
            setError('Please paste an email or upload a .eml file.')
            return
        }
        setLoading(true)
        setError(null)
        setResult(null)
        try {
            const data = await api.post('/analyse', { raw_email: rawEmail })
            setResult(data)
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    const handleFileUpload = (e) => {
        const file = e.target.files[0]
        if (!file) return
        const reader = new FileReader()
        reader.onload = (ev) => setRawEmail(ev.target.result)
        reader.readAsText(file)
    }

    return (
        <div style={{ maxWidth: 900, margin: '0 auto', padding: '3rem 1.5rem' }}>
            <h1 style={{ fontWeight: 800, fontSize: '2rem', color: '#e2e8f0', marginBottom: '0.5rem' }}>
                🔍 Analyse an Email
            </h1>
            <p style={{ color: '#64748b', marginBottom: '2rem' }}>
                Paste your email content (including headers) or upload a .eml file to check for phishing indicators.
            </p>

            <form onSubmit={handleSubmit}>
                <div className="card" style={{ marginBottom: '1rem' }}>
                    <label style={{ color: '#94a3b8', fontSize: '0.875rem', fontWeight: 500, display: 'block', marginBottom: '0.75rem' }}>
                        Raw Email Content
                    </label>
                    <textarea
                        id="email-input"
                        value={rawEmail}
                        onChange={(e) => setRawEmail(e.target.value)}
                        placeholder="Paste the full email here — including headers (From, To, Subject, Received, etc.) and body..."
                        style={{
                            width: '100%',
                            minHeight: 280,
                            background: '#0f172a',
                            border: '1px solid #334155',
                            borderRadius: '0.5rem',
                            color: '#e2e8f0',
                            padding: '0.875rem',
                            fontFamily: 'monospace',
                            fontSize: '0.875rem',
                            lineHeight: 1.6,
                            resize: 'vertical',
                            boxSizing: 'border-box',
                        }}
                    />
                </div>

                <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', marginBottom: '1.5rem', flexWrap: 'wrap' }}>
                    <label
                        htmlFor="eml-upload"
                        style={{
                            background: '#1e293b',
                            border: '1px solid #334155',
                            color: '#94a3b8',
                            padding: '0.5rem 1rem',
                            borderRadius: '0.5rem',
                            cursor: 'pointer',
                            fontSize: '0.875rem',
                        }}
                    >
                        📎 Upload .eml File
                    </label>
                    <input
                        id="eml-upload"
                        type="file"
                        accept=".eml,.txt"
                        onChange={handleFileUpload}
                        style={{ display: 'none' }}
                    />
                    <button
                        type="submit"
                        className="btn-primary"
                        disabled={loading}
                        id="analyse-btn"
                    >
                        {loading ? '⏳ Analysing...' : '🔍 Analyse Email'}
                    </button>
                </div>
            </form>

            {error && (
                <div style={{
                    background: 'rgba(239,68,68,0.1)',
                    border: '1px solid rgba(239,68,68,0.3)',
                    borderRadius: '0.5rem',
                    padding: '1rem',
                    color: '#fca5a5',
                    marginBottom: '1rem',
                }}>
                    ⚠️ {error}
                </div>
            )}

            {/* Results Placeholder — Phase 3 will render real analysis components */}
            {result && (
                <div className="card">
                    <h2 style={{ color: '#e2e8f0', fontWeight: 700, marginTop: 0 }}>Analysis Result</h2>
                    <p style={{ color: '#64748b', fontSize: '0.875rem' }}>
                        Phase 1 placeholder — full risk gauge and threat flags will appear here in Phase 3.
                    </p>
                    <pre style={{
                        background: '#0f172a',
                        border: '1px solid #334155',
                        borderRadius: '0.5rem',
                        padding: '1rem',
                        color: '#94a3b8',
                        fontSize: '0.8125rem',
                        overflow: 'auto',
                    }}>
                        {JSON.stringify(result, null, 2)}
                    </pre>
                </div>
            )}
        </div>
    )
}

export default DetectionPage

/**
 * src/pages/DetectionPage.jsx - Email analysis interface.
 *
 * Allows users to:
 *   1. Paste raw email content into a textarea
 *   2. Upload a .eml file
 *   3. Submit for analysis and view the full risk assessment
 *
 * The form is hidden once a result arrives and re-shown via the
 * "Analyse Another" button rendered inside AnalysisResults.
 */

import { useState } from 'react'
import api from '../api/client'
import AnalysisResults from '../components/detection/AnalysisResults'

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

    const handleReset = () => {
        setResult(null)
        setRawEmail('')
        setError(null)
    }

    return (
        <div style={{ maxWidth: 900, margin: '0 auto', padding: '3rem 1.5rem' }}>
            <h1 style={{ fontWeight: 800, fontSize: '2rem', color: '#e2e8f0', marginBottom: '0.5rem' }}>
                🔍 Analyse an Email
            </h1>
            <p style={{ color: '#64748b', marginBottom: '2rem' }}>
                Paste your email content (including headers) or upload a .eml file to check for phishing indicators.
            </p>

            {/* Input form - hidden once a result is shown */}
            {!result && (
                <form onSubmit={handleSubmit}>
                    <div className="card" style={{ marginBottom: '1rem' }}>
                        <label style={{ color: '#94a3b8', fontSize: '0.875rem', fontWeight: 500, display: 'block', marginBottom: '0.75rem' }}>
                            Raw Email Content
                        </label>
                        <textarea
                            id="email-input"
                            value={rawEmail}
                            onChange={(e) => setRawEmail(e.target.value)}
                            placeholder="Paste the full email here - including headers (From, To, Subject, Received, etc.) and body..."
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
            )}

            {/* Error panel */}
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

            {/* Loading skeleton */}
            {loading && (
                <div className="card" style={{ textAlign: 'center', padding: '3rem 2rem' }}>
                    <div style={{ fontSize: '2rem', marginBottom: '0.75rem' }}>⏳</div>
                    <p style={{ color: '#64748b', margin: 0 }}>Running analysis - this usually takes under a second…</p>
                </div>
            )}

            {/* Full results panel */}
            {result && !loading && (
                <AnalysisResults result={result} onReset={handleReset} />
            )}
        </div>
    )
}

export default DetectionPage

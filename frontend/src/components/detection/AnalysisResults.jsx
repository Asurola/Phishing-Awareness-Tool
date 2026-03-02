/**
 * src/components/detection/AnalysisResults.jsx — Results display component.
 * Placeholder for Phase 3. Renders the full risk breakdown from the API.
 * TODO (Phase 3): Implement with RiskScoreGauge, ThreatIndicator, Recommendations.
 */

function AnalysisResults({ result }) {
    if (!result) return null
    return (
        <div className="card">
            <p style={{ color: '#64748b' }}>
                AnalysisResults component — TODO Phase 3.<br />
                Risk Score: {result.risk_score} | Verdict: {result.verdict}
            </p>
        </div>
    )
}

export default AnalysisResults

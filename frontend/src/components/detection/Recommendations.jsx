/**
 * src/components/detection/Recommendations.jsx
 *
 * Displays the summary_recommendations list from the API.
 * High-risk emails get a prominent warning banner; safe ones get a calm notice.
 *
 * Props:
 *   recommendations - string[]
 *   riskScore       - integer 0-100
 */

export default function Recommendations({ recommendations, riskScore }) {
    if (!recommendations || recommendations.length === 0) return null

    const isDanger = riskScore >= 50

    return (
        <div style={{
            background: isDanger ? 'rgba(239,68,68,0.07)' : 'rgba(34,197,94,0.07)',
            border: `1px solid ${isDanger ? 'rgba(239,68,68,0.3)' : 'rgba(34,197,94,0.25)'}`,
            borderRadius: '0.75rem',
            padding: '1.25rem 1.5rem',
        }}>
            <h3 style={{
                margin: '0 0 0.875rem',
                fontSize: '1rem',
                fontWeight: 700,
                color: isDanger ? '#fca5a5' : '#86efac',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
            }}>
                {isDanger ? '⚠️' : '✅'} What you should do
            </h3>
            <ul style={{ margin: 0, padding: '0 0 0 1.25rem' }}>
                {recommendations.map((rec, i) => (
                    <li key={i} style={{
                        color: '#cbd5e1',
                        fontSize: '0.9rem',
                        lineHeight: 1.65,
                        marginBottom: i < recommendations.length - 1 ? '0.5rem' : 0,
                    }}>
                        {rec}
                    </li>
                ))}
            </ul>
        </div>
    )
}

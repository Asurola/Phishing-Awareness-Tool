/**
 * src/components/common/LoadingSpinner.jsx — Animated loading indicator.
 *
 * Displays a pulsing spinner with an optional label.
 * Used throughout the app while API calls are in flight.
 */

function LoadingSpinner({ label = 'Loading...' }) {
    return (
        <div style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '1rem',
            padding: '3rem',
            color: '#64748b',
        }}>
            <div style={{
                width: 40,
                height: 40,
                border: '3px solid #1e293b',
                borderTopColor: '#3b82f6',
                borderRadius: '50%',
                animation: 'spin 0.8s linear infinite',
            }} />
            <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
            <span style={{ fontSize: '0.875rem' }}>{label}</span>
        </div>
    )
}

export default LoadingSpinner

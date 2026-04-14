/**
 * src/components/detection/RiskScoreGauge.jsx
 *
 * Animated semicircular SVG gauge (0–100).
 * Colour zones: green (0–49), amber (50–79), red (80–100).
 * Props:
 *   score      - integer 0-100
 *   probability - float 0-1 (shown as raw percentage)
 */

import { useEffect, useRef } from 'react'

const RADIUS = 80
const STROKE = 14
const CX = 110
const CY = 110
const CIRCUMFERENCE = Math.PI * RADIUS   // half-circle arc length

function gaugeColour(score) {
    if (score >= 80) return { primary: '#ef4444', glow: 'rgba(239,68,68,0.35)', label: 'red' }
    if (score >= 50) return { primary: '#f59e0b', glow: 'rgba(245,158,11,0.35)', label: 'amber' }
    return { primary: '#22c55e', glow: 'rgba(34,197,94,0.35)', label: 'green' }
}

export default function RiskScoreGauge({ score, probability }) {
    const arcRef = useRef(null)

    // strokeDashoffset = full – proportion of arc filled
    const filled = (score / 100) * CIRCUMFERENCE
    const offset = CIRCUMFERENCE - filled
    const colour = gaugeColour(score)

    useEffect(() => {
        // trigger CSS transition after mount
        if (arcRef.current) {
            arcRef.current.style.strokeDashoffset = CIRCUMFERENCE   // start at 0
        }
        const raf = requestAnimationFrame(() => {
            setTimeout(() => {
                if (arcRef.current) {
                    arcRef.current.style.strokeDashoffset = offset
                }
            }, 60)  // slight delay so transition fires
        })
        return () => cancelAnimationFrame(raf)
    }, [score, offset])

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <svg viewBox="0 0 220 130" style={{ width: 240, overflow: 'visible' }}>
                <defs>
                    <filter id="glow-gauge">
                        <feGaussianBlur stdDeviation="3" result="blur" />
                        <feMerge>
                            <feMergeNode in="blur" />
                            <feMergeNode in="SourceGraphic" />
                        </feMerge>
                    </filter>
                </defs>

                {/* Track arc */}
                <path
                    d={`M ${CX - RADIUS} ${CY} A ${RADIUS} ${RADIUS} 0 0 1 ${CX + RADIUS} ${CY}`}
                    fill="none"
                    stroke="#1e293b"
                    strokeWidth={STROKE}
                    strokeLinecap="round"
                />

                {/* Filled arc */}
                <path
                    ref={arcRef}
                    d={`M ${CX - RADIUS} ${CY} A ${RADIUS} ${RADIUS} 0 0 1 ${CX + RADIUS} ${CY}`}
                    fill="none"
                    stroke={colour.primary}
                    strokeWidth={STROKE}
                    strokeLinecap="round"
                    strokeDasharray={CIRCUMFERENCE}
                    strokeDashoffset={CIRCUMFERENCE}   // starts hidden; updated via useEffect
                    filter="url(#glow-gauge)"
                    style={{ transition: 'stroke-dashoffset 1s cubic-bezier(0.4,0,0.2,1)' }}
                />

                {/* Score number */}
                <text
                    x={CX}
                    y={CY - 6}
                    textAnchor="middle"
                    fill={colour.primary}
                    fontSize="34"
                    fontWeight="800"
                    fontFamily="Inter, system-ui, sans-serif"
                    style={{ filter: `drop-shadow(0 0 8px ${colour.glow})` }}
                >
                    {score}
                </text>
                <text
                    x={CX}
                    y={CY + 16}
                    textAnchor="middle"
                    fill="#64748b"
                    fontSize="11"
                    fontFamily="Inter, system-ui, sans-serif"
                >
                    / 100 Risk Score
                </text>

                {/* Min / Max labels */}
                <text x={CX - RADIUS + 2} y={CY + 22} fill="#475569" fontSize="10" fontFamily="Inter, system-ui, sans-serif">0</text>
                <text x={CX + RADIUS - 14} y={CY + 22} fill="#475569" fontSize="10" fontFamily="Inter, system-ui, sans-serif">100</text>
            </svg>

            {/* Raw probability */}
            <p style={{ margin: '0.25rem 0 0', color: '#64748b', fontSize: '0.8125rem' }}>
                Model confidence: <span style={{ color: colour.primary, fontWeight: 600 }}>
                    {(probability * 100).toFixed(1)}%
                </span> phishing probability
            </p>
        </div>
    )
}

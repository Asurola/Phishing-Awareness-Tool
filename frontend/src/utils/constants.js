/**
 * src/utils/constants.js - Application-wide constants.
 *
 * Central location for magic strings, configuration values, and enumerations
 * used throughout the frontend. Import from here rather than hardcoding values
 * inline to keep changes maintainable.
 */

/** localStorage key for the anonymous session ID */
export const SESSION_ID_KEY = 'phishguard_session_id'

/** Available difficulty levels for scenario filtering */
export const DIFFICULTIES = ['beginner', 'intermediate', 'advanced']

/** Risk score thresholds matching the backend explanation engine */
export const RISK_THRESHOLDS = {
    LOW: 35,
    MEDIUM: 65,
}

/** Maps risk score to a human-readable verdict */
export function getRiskVerdict(score) {
    if (score < RISK_THRESHOLDS.LOW) return 'Low Risk - Likely Legitimate'
    if (score < RISK_THRESHOLDS.MEDIUM) return 'Medium Risk - Treat with Caution'
    return 'High Risk - Likely Phishing'
}

/** Maps risk score to a colour string */
export function getRiskColour(score) {
    if (score < RISK_THRESHOLDS.LOW) return '#22c55e'    // green
    if (score < RISK_THRESHOLDS.MEDIUM) return '#f59e0b'  // amber
    return '#ef4444'                                        // red
}

/** Flag severity levels */
export const SEVERITY = {
    HIGH: 'high',
    MEDIUM: 'medium',
    LOW: 'low',
}

/** Maps severity to display colour */
export const SEVERITY_COLOURS = {
    high: '#ef4444',
    medium: '#f59e0b',
    low: '#22c55e',
}

/** Backend API base path (overridden by VITE_API_BASE_URL env var) */
export const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api'

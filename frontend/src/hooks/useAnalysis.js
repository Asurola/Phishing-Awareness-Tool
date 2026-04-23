/**
 * src/hooks/useAnalysis.js - Custom hook for detection API calls.
 *
 * Encapsulates the state management for the email analysis flow:
 *   - loading state
 *   - result data
 *   - error handling
 *   - session ID management
 *
 */

import { useState, useCallback } from 'react'
import api from '../api/client'
import { SESSION_ID_KEY } from '../utils/constants'

/**
 * Get or create an anonymous session ID stored in localStorage.
 * Creates a new UUID v4 if none exists.
 *
 * @returns {string} The session ID string
 */
export function getOrCreateSessionId() {
    let sessionId = localStorage.getItem(SESSION_ID_KEY)
    if (!sessionId) {
        // Generate a simple UUID v4
        sessionId = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
            const r = (Math.random() * 16) | 0
            const v = c === 'x' ? r : (r & 0x3) | 0x8
            return v.toString(16)
        })
        localStorage.setItem(SESSION_ID_KEY, sessionId)
    }
    return sessionId
}

/**
 * Custom hook for submitting email analysis requests.
 *
 * @returns {{
 *   analyseEmail: (rawEmail: string) => Promise<void>,
 *   result: object | null,
 *   loading: boolean,
 *   error: string | null,
 *   reset: () => void,
 * }}
 */
export function useAnalysis() {
    const [result, setResult] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const analyseEmail = useCallback(async (rawEmail) => {
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
    }, [])

    const reset = useCallback(() => {
        setResult(null)
        setError(null)
    }, [])

    return { analyseEmail, result, loading, error, reset }
}

export default useAnalysis

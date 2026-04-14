/**
 * src/api/client.js - HTTP API client for the Flask backend.
 *
 * Provides a configured fetch wrapper that:
 *   - Prepends the backend base URL (from env variable VITE_API_BASE_URL
 *     or falls back to '/api' which Vite proxies to localhost:5000)
 *   - Sets default Content-Type: application/json headers
 *   - Throws an Error with the server's message on non-2xx responses
 *   - Exposes convenience methods: get(), post()
 *
 * Usage:
 *   import api from './api/client'
 *   const data = await api.post('/analyse', { raw_email: '...' })
 */

const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

/**
 * Core fetch wrapper with error handling.
 *
 * @param {string} endpoint - API path (e.g. '/health', '/analyse')
 * @param {RequestInit} options - fetch options (method, body, headers, etc.)
 * @returns {Promise<any>} Parsed JSON response body
 * @throws {Error} With server error message if response is not ok
 */
async function request(endpoint, options = {}) {
    const url = `${BASE_URL}${endpoint}`

    const defaultHeaders = {
        'Content-Type': 'application/json',
    }

    const config = {
        ...options,
        headers: {
            ...defaultHeaders,
            ...options.headers,
        },
    }

    const response = await fetch(url, config)

    if (!response.ok) {
        const error = await response.json().catch(() => ({ error: response.statusText }))
        throw new Error(error.error || `Request failed with status ${response.status}`)
    }

    return response.json()
}

const api = {
    /**
     * Perform a GET request.
     *
     * @param {string} endpoint - API path
     * @param {RequestInit} options - Additional fetch options
     * @returns {Promise<any>} Parsed JSON response
     */
    get(endpoint, options = {}) {
        return request(endpoint, { ...options, method: 'GET' })
    },

    /**
     * Perform a POST request with a JSON body.
     *
     * @param {string} endpoint - API path
     * @param {object} body - Request payload (will be JSON-stringified)
     * @param {RequestInit} options - Additional fetch options
     * @returns {Promise<any>} Parsed JSON response
     */
    post(endpoint, body, options = {}) {
        return request(endpoint, {
            ...options,
            method: 'POST',
            body: JSON.stringify(body),
        })
    },

    /**
     * Perform a POST request with a FormData body (for file uploads).
     *
     * @param {string} endpoint - API path
     * @param {FormData} formData - FormData object (Content-Type is set automatically)
     * @returns {Promise<any>} Parsed JSON response
     */
    postForm(endpoint, formData) {
        return request(endpoint, {
            method: 'POST',
            body: formData,
            headers: {}, // Let browser set multipart Content-Type with boundary
        })
    },
}

export default api

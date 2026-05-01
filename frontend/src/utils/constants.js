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

/**
 * src/components/common/Button.jsx - Reusable button component.
 *
 * Wraps a styled button with variant support (primary, danger, success, ghost).
 * Uses the CSS classes defined in index.css.
 *
 * TODO (Phase 3): Use this component throughout the app for consistency.
 */

function Button({ children, variant = 'primary', onClick, disabled = false, style = {}, id }) {
    const variantClass = {
        primary: 'btn-primary',
        danger: 'btn-danger',
        success: 'btn-success',
        ghost: '',
    }[variant] || 'btn-primary'

    return (
        <button
            id={id}
            className={variantClass}
            onClick={onClick}
            disabled={disabled}
            style={{
                opacity: disabled ? 0.6 : 1,
                cursor: disabled ? 'not-allowed' : 'pointer',
                ...style,
            }}
        >
            {children}
        </button>
    )
}

export default Button

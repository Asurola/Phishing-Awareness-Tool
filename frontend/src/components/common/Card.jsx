/**
 * src/components/common/Card.jsx - Reusable card container component.
 *
 * A dark-themed card with optional title and consistent border/padding.
 * Uses the .card CSS class from index.css.
 *
 * TODO (Phase 3): Use throughout detection and education pages.
 */

function Card({ children, title, style = {} }) {
    return (
        <div className="card" style={style}>
            {title && (
                <h3 style={{
                    color: '#e2e8f0',
                    fontWeight: 600,
                    fontSize: '1rem',
                    marginTop: 0,
                    marginBottom: '1rem',
                    borderBottom: '1px solid #334155',
                    paddingBottom: '0.75rem',
                }}>
                    {title}
                </h3>
            )}
            {children}
        </div>
    )
}

export default Card

/**
 * src/components/layout/Layout.jsx — Root layout wrapper.
 *
 * Wraps all pages with a consistent structure:
 *   - Navbar at the top
 *   - Main content area (rendered via react-router Outlet)
 *   - Footer at the bottom
 *
 * This component is used as the parent route element in App.jsx so all
 * nested routes automatically share the same navigation and footer.
 */

import { Outlet } from 'react-router-dom'
import Navbar from './Navbar'
import Footer from './Footer'

function Layout() {
    return (
        <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
            <Navbar />
            <main style={{ flex: 1 }}>
                <Outlet />
            </main>
            <Footer />
        </div>
    )
}

export default Layout

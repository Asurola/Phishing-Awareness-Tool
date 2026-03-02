/**
 * src/App.jsx — Root application component with routing configuration.
 *
 * Defines all client-side routes using react-router-dom v6.
 * All pages are wrapped in the Layout component which provides
 * the Navbar and Footer.
 *
 * Routes:
 *   /                  → HomePage
 *   /detect            → DetectionPage
 *   /learn             → EducationPage
 *   /learn/simulate    → SimulationPage
 *   /learn/progress    → ResultsPage (progress dashboard)
 */

import { Routes, Route } from 'react-router-dom'
import Layout from './components/layout/Layout'
import HomePage from './pages/HomePage'
import DetectionPage from './pages/DetectionPage'
import EducationPage from './pages/EducationPage'
import SimulationPage from './pages/SimulationPage'
import ResultsPage from './pages/ResultsPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<HomePage />} />
        <Route path="detect" element={<DetectionPage />} />
        <Route path="learn" element={<EducationPage />} />
        <Route path="learn/simulate" element={<SimulationPage />} />
        <Route path="learn/progress" element={<ResultsPage />} />
      </Route>
    </Routes>
  )
}

export default App

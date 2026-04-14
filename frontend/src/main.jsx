/**
 * src/main.jsx - React application entry point.
 *
 * Mounts the root React component into the #root DOM element.
 * Wraps the app in BrowserRouter for client-side routing.
 */

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>,
)

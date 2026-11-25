import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import Route from './pages/route.tsx'



createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Route />
  </StrictMode>,
)

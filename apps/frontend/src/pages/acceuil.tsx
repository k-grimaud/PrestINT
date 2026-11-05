import { useEffect, useState } from 'react'
import '../App.css'
import { fetchMe, type User } from '../api.ts'
import Compte from './compte/compte.tsx'
import Dashboard from './dashboard/dashboard.tsx'
import Erreur from './erreur/erreur.tsx'


const KNOWN_PATHS = ['/', '/dashboard'] // used for skipping unknown paths


function App() {
  const [user, setUser] = useState<User | null | undefined>(undefined)

  // used for HTTP error handling
  const [failure, setFailure] = useState<number>() // status for when /auth/me fails
  const notFound = !KNOWN_PATHS.includes(location.pathname) // cheking the URL on every render

  useEffect(() => {
    fetchMe().then(setUser).catch((e) => setFailure(e.cause ?? 503)) // forcing a HTTP status for unknown causes
  }, [])

  // The page follows the login state; keep the URL in sync with it (logged in -> /dashboard, else /)
  useEffect(() => {
    if (user === undefined || notFound) return
    const want = user ? '/dashboard' : '/'
    const sync = () => {
      if (location.pathname !== want) history.replaceState(null, '', want)
    }
    sync()
    window.addEventListener('popstate', sync)
    return () => window.removeEventListener('popstate', sync)
  }, [user, notFound])

  if (notFound) return <Erreur status={404} />
  if (failure) return <Erreur status={failure} />
  if (user === undefined) return null

  if (user) {
    return <Dashboard user={user} onLogout={() => setUser(null)} />
  }

  return (
    <>
      <h1> PrestINT </h1>
        <h2> Prestations des clubs de l'INT </h2>
        <Compte onLogin={setUser} />
    </>
  )
}

export default App

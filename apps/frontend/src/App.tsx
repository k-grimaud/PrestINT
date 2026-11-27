import { useEffect, useState } from 'react'
import './App.css'
import { fetchMe, get, type User } from './api.ts'
import Dashboard from './pages/dashboard/dashboard.tsx'
import Compte from './pages/compte/compte.tsx'
import Erreur from './pages/erreur/erreur.tsx'
import Services from './pages/services/services.tsx'
import Navbar, { type Page } from './pages/navbar/Navbar.tsx'


const KNOWN_PATHS = ['/', '/dashboard']

function Route() {
  // undefined = ask /me null = log out
  const [user, setUser] = useState<User | null | undefined>(undefined)
  const [page, setPage] = useState<Page>('services')
  const [error, setError] = useState('')
  const [failure, setFailure] = useState<number>()
  const notFound = !KNOWN_PATHS.includes(location.pathname)

  
  useEffect(() => {
    fetchMe().then(setUser).catch((e) => setFailure(e.cause ?? 503))
    history.replaceState({ page: 'services' }, '')
    function onBack(e: PopStateEvent) {
      setPage(e.state?.page ?? 'services')
    }
    window.addEventListener('popstate', onBack)
    return () => window.removeEventListener('popstate', onBack)
  }, [])

  function goTo(newPage: Page) {
    if (newPage === page) return
    history.pushState({ page: newPage }, '')
    setPage(newPage)
  }

  if (notFound) return <Erreur status={404} />
  if (failure) return <Erreur status={failure} />
  if (user === undefined) return null

  return (
    <>
      <Navbar page={page} isLogged={user !== null} onNavigate={goTo} />

      {page === 'services' && <Services />}

      {page === 'account' && user && (
        <Dashboard user={user} onLogout={() => setUser(null)} />
      )}

      {page === 'account' && !user && <Compte onLogin={setUser} />}
    </>
  )
}

export default Route
import { useEffect, useState } from 'react'
import '../App.css'
import { fetchMe, get, type User, type List_Service } from '../api.ts'
import Dashboard from './dashboard/dashboard.tsx'
import Compte from './compte/compte.tsx'
import Navbar, { type Page } from '../components/navbar/Navbar.tsx'
import SearchBar from '../components/search/SearchBar.tsx'
import ServiceList from '../components/services/ServiceList.tsx'

function Route() {
  // undefined = ask /me null = log out
  const [user, setUser] = useState<User | null | undefined>(undefined)
  const [page, setPage] = useState<Page>('services')
  const [services, setServices] = useState<List_Service[]>([])
  const [search, setSearch] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    fetchMe().then(setUser).catch(() => setUser(null))
  }, [])

  useEffect(() => {
    get('/services')
      .then((res) => {
        if (!res.ok) throw new Error('error')
        return res.json()
      })
      .then((data) => setServices(data))
      .catch(() => setError('Serveur injoignable, réessayez.'))
  }, [])

  
  useEffect(() => {
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

  if (user === undefined) return null

  const text = search.toLowerCase()
  const results = services.filter(
    (service) =>
      service.name.toLowerCase().includes(text) ||
      service.asso_id.toLowerCase().includes(text)
  )

  return (
    <>
      <Navbar page={page} isLogged={user !== null} onNavigate={goTo} />

      {page === 'services' && (
        <>
          <h2>Prestations des clubs de l'INT</h2>
          <SearchBar value={search} onChange={setSearch} />
          {error ? <p>{error}</p> : <ServiceList services={results} />}
        </>
      )}

      {page === 'account' && user && (
        <Dashboard user={user} onLogout={() => setUser(null)} />
      )}

      {page === 'account' && !user && <Compte onLogin={setUser} />}
    </>
  )
}

export default Route
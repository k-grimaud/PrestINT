import { useEffect, useState } from 'react'
import { get, type List_Service} from '../../api.ts'

import SearchBar from '../../components/search/SearchBar.tsx'
import ServiceList from '../../components/services/ServiceList.tsx'

function Services() {
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [services, setServices] = useState<List_Service | null>(null)
  const [search, setSearch] = useState('')
  
  async function services_data() {
    setBusy(true)
    setError('')
    try {
      const res = await get(`/service`)
      console.log('test')
      console.log(res.json())
      console.log('test')
      if (!res.ok) throw new Error('Erreur serveur')
      const services: List_Service = await res.json()
      setServices(services)
    } catch {
      setError('Serveur injoignable, réessayez.')
    } finally {
      setBusy(false)
    }
  }

  const text = search.toLowerCase()
  const results = (services ?? []).filter(
    (service) =>
      service.name.toLowerCase().includes(text) ||
      service.asso_id.toLowerCase().includes(text)
  )

  useEffect(() => {
    services_data()
  }, [])

  return (
    <>
      <h2>Prestations des clubs de l'INT</h2>
      <SearchBar value={search} onChange={setSearch} />
          {error ? <p>{error}</p> : <ServiceList services={results} />}
      {busy && <p>Chargement…</p>}
      {error && <p>{error}</p>}

      <div className="ticks"></div>
      <section className="boxes">
        <div>
        </div>
      </section>
      <div className="ticks"></div>
      <section id="spacer"></section>
    </>
  )
}

export default Services

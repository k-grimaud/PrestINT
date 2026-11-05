import { useEffect, useState } from 'react'
import { get, type List_Service} from '../../api.ts'

function Services({ service_id }: { service_id : number }) {
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [service, setService] = useState<List_Service | null>(null)


  async function service_data(service_id: number) {
    setBusy(true)
    setError('')
    try {
      const res = await get(`/services/${service_id}`)
      if (!res.ok) throw new Error('Erreur serveur')
      const service: List_Service = await res.json()
      setService(service)
    } catch {
      setError('Serveur injoignable, réessayez.')
    } finally {
      setBusy(false)
    }
  }

  useEffect(() => {
    service_data(service_id)
  }, [service_id])

  return (
    <>
      <h1> service.name </h1>

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

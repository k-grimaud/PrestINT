import { useState } from 'react'
import { post, type User, type List_Service} from '../../api.ts'

function Services({ user, list_service, onLogout }: { user: User; list_service : List_Service; onLogout: () => void }) {
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  async function logout() {
    setBusy(true)
    setError('')
    try {
      await post('/auth/logout')
      onLogout()
    } catch {
      setError('Serveur injoignable, réessayez.')
      setBusy(false)
    }
  }

  async function service_data(list_service.list_service_id: number) {
    setBusy(true)
    setError('')
    try {
      await get('/services/')
      onLogout()
    } catch {
      setError('Serveur injoignable, réessayez.')
      setBusy(false)
    }
  }

  return (
    <>
      <h1> aaaaa </h1>
      <h2 className="capitalize"> Bonjour {prestation.first_name} </h2>

      <div className="ticks"></div>
      <section className="boxes">
        <div>
          <h2>Identité</h2>
          <p className="capitalize">
            {user.first_name} {user.last_name}
          </p>
        </div>
        <div>
          <h2>Adresse mail</h2>
          <p>
            <code>{user.email}</code>
          </p>
        </div>
        <div>
          <h2>Session</h2>
          <p>Connecté</p>
          <button type="button" className="counter" onClick={logout} disabled={busy}>
            Se déconnecter
          </button>
          {error && (
            <p className="login-error" role="alert">
              {error}
            </p>
          )}
        </div>
      </section>
      <div className="ticks"></div>
      <section id="spacer"></section>
    </>
  )
}

export default Dashboard

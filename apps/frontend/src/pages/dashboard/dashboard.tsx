import { useState } from 'react'
import { post, type User } from '../../api.ts'

function Dashboard({ user, onLogout }: { user: User; onLogout: () => void }) {
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
    } finally {
      setBusy(false)
    }
  }

  return (
    <>
      <h2 className="capitalize">Bonjour {user.first_name}</h2>

      <section className="boxes">
        <div>
          <h3>Identité</h3>
          <p className="capitalize">
            {user.first_name} {user.last_name}
          </p>
        </div>
        <div>
          <h3>Adresse mail</h3>
          <p>{user.email}</p>
        </div>
        <div>
          <h3>Session</h3>
          <p>Connecté</p>
          <button type="button" className="counter" onClick={logout} disabled={busy}>
            Se déconnecter
          </button>
          {error && <p className="login-error">{error}</p>}
        </div>
      </section>
    </>
  )
}

export default Dashboard
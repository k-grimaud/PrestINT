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
      setBusy(false)
    }
  }

  return (
    <>
      <h1> PrestINT </h1>
      <h2 className="capitalize"> Bonjour {user.first_name} </h2>

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

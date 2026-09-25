import { useState, type FormEvent } from 'react'
import { fetchMe, post, type User } from '../../api.ts'

type Step = 'email' | 'code'

function Compte({ onLogin }: { onLogin: (user: User) => void }) {
  const [step, setStep] = useState<Step>('email')
  const [email, setEmail] = useState('')
  const [code, setCode] = useState('')
  const [info, setInfo] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  // Runs one request at a time and turns network failures into a message
  async function run(action: () => Promise<void>) {
    setBusy(true)
    setError('')
    try {
      await action()
    } catch {
      setError('Serveur injoignable, réessayez.')
    } finally {
      setBusy(false)
    }
  }

  function requestCode(e: FormEvent) {
    e.preventDefault()
    run(async () => {
      const res = await post('/auth/otp/request', { email })
      if (res.status === 422) {
        setError('Adresse attendue : prenom.nom@telecom-sudparis.eu')
        return
      }
      setCode('')
      setInfo("Si l'adresse est valide, un code vient d'être envoyé.")
      setStep('code')
    })
  }

  function verifyCode(e: FormEvent) {
    e.preventDefault()
    run(async () => {
      const res = await post('/auth/otp/verify', { email, code })
      if (!res.ok) {
        setError('Code invalide ou expiré')
        return
      }
      const me = await fetchMe()
      if (!me) {
        setError('Connexion impossible, réessayez.')
        return
      }
      onLogin(me)
    })
  }

  function changeEmail() {
    setError('')
    setInfo('')
    setStep('email')
  }

  return (
    <section className="login">
      {step === 'email' && (
        <form onSubmit={requestCode}>
          <label htmlFor="login-email">Connexion</label>
          <input
            id="login-email"
            type="email"
            autoComplete="email"
            placeholder="prenom.nom@telecom-sudparis.eu"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <button type="submit" className="counter" disabled={busy}>
            Recevoir un code
          </button>
        </form>
      )}

      {step === 'code' && (
        <form onSubmit={verifyCode}>
          <label htmlFor="login-code">Code reçu par mail</label>
          {info && <p>{info}</p>}
          <input
            id="login-code"
            className="login-code"
            inputMode="numeric"
            autoComplete="one-time-code"
            pattern="\d{6}"
            maxLength={6}
            placeholder="123456"
            value={code}
            onChange={(e) => setCode(e.target.value.replace(/\D/g, ''))}
            required
            autoFocus
          />
          <button type="submit" className="counter" disabled={busy}>
            Se connecter
          </button>
          <button type="button" className="login-link" onClick={changeEmail}>
            Changer d'adresse ({email})
          </button>
        </form>
      )}

      {error && (
        <p className="login-error" role="alert">
          {error}
        </p>
      )}
    </section>
  )
}

export default Compte

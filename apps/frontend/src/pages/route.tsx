import { useEffect, useState } from 'react'
import '../App.css'
import { fetchMe, type User } from '../api.ts'
import Dashboard from './dashboard/dashboard.tsx'
import LoginPage from "./compte/login.tsx";
import PageAcceuil from "./acceuil.tsx";


function Route() {
    // undefined = still asking /me, null = logged out
    const [user, setUser] = useState<User | null | undefined>(undefined)
    const [showLogin, setShowLogin] = useState(false)

    useEffect(() => {
        fetchMe().then(setUser).catch(() => setUser(null))
    }, [])

    // The page follows the login state; keep the URL in sync with it (logged in -> /dashboard, else /)
    useEffect(() => {
        if (user === undefined) return
        const want = user ? '/dashboard' : '/'
        const sync = () => {
            if (location.pathname !== want) history.replaceState(null, '', want)
        }
        sync()
        window.addEventListener('popstate', sync)
        return () => window.removeEventListener('popstate', sync)
    }, [user])

    if (user === undefined) return null

    if (user) {
        if (showLogin) {
            return <LoginPage onLogin={setUser} />
        }
        return <Dashboard user={user} onLogout={() => setUser(null)} />
    }

// not logged

    if (showLogin) {
        return <LoginPage onLogin={setUser} />
    }

    return (<PageAcceuil onLoginClick={() => setShowLogin(true)}/>)
}

export default Route

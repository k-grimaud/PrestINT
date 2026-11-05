import { useEffect, useState } from 'react'
import '../App.css'
import { fetchMe, type User } from '../api.ts'
import Dashboard from './dashboard/dashboard.tsx'
import Navbar from "../components/navbar/Navbar.tsx";
import Compte from "./compte/compte.tsx";



function Route() {
    // undefined = still asking /me, null = logged out
    const [user, setUser] = useState<User | null | undefined>(undefined)
    const [login, ]

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
        return <Dashboard user={user} onLogout={() => setUser(null)} />
    }

    return (
        <>
        </>
    )
}

export default Route

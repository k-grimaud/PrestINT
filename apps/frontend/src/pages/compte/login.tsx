import { useEffect, useState } from 'react'
import '../App.css'
import { fetchMe, type User } from '../../api.ts'
import Compte from './compte.tsx'
import Dashboard from '../dashboard/dashboard.tsx'
import Navbar from "../../components/navbar/Navbar.tsx";
import PageAcceuil from "../acceuil.tsx";

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





  if (user === undefined) return null // attend serveur

  if (user) { // si uttilisateur connecte
    return <Dashboard user={user} onLogout={() => setUser(null)} />
  }

  return ( // si pas uttilisateur connecte
    <>
      <Navbar/>
      <h1> PrestINT </h1>
        <h2> Prestations des clubs de l'INT </h2>
        <Compte onLogin={setUser} />
    </>
  )
}

export default PageLogin
<Compte onLogin={setUser} />
    </>
  )
}
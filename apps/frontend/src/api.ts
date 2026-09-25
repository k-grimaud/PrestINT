export const API = import.meta.env.VITE_API_URL ?? '/api'

export interface User {
  email: string
  first_name: string
  last_name: string
}

export function post(path: string, body?: object) {
  return fetch(`${API}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  })
}

export async function fetchMe(): Promise<User | null> {
  const res = await fetch(`${API}/auth/me`)
  return res.ok ? res.json() : null
}

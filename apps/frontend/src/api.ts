export const API = import.meta.env.VITE_API_URL ?? '/api'

export interface User {
  user_id: string
  email: string
  first_name: string
  last_name: string
}

export interface Permission {
  asso_id: string
  user_id: string
  permission: string
}

export interface Picture {
  picture_id: number
  asso_id: string
  path: string
}

export interface List_Service {
  list_service_id: number
  asso_id: string
  name: string
  approximative_cost: number
  approximative_time: string
  description: string
  path: string
}

export interface Ongoing_Service {
  service_id: number
  asso_id: string
  client_id: string
  type_service_id: number
  created_at: string
  end_at: string
  status: string
  context: string
}

export function get(path: string) {
  return fetch(`${API}${path}`)
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
  if (res.status == 401) return null
  if (!res.ok) throw new Error('GET /auth/me failed', { cause: res.status })
  return res.json()
}

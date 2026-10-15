export const API = import.meta.env.VITE_API_URL ?? '/api'

export interface User {
  user_id: number 
  email: string
  first_name: string
  last_name: string
}

export interface Permission {
  asso_id: number 
  user_id: number
  permission: string
}

export interface Picture {
  picture_id: number
  asso_id: number
  path: string
}

export interface List_Service {
  list_service_id: number
  asso_id: number
  approximative_cost: string
  approximative_time: string
  description: string
  path: string
}

export interface Ongoing_Service {
  service_id: number
  asso_id: number
  client_id: number
  type_presta_id: number
  created_at: string
  end_at: string
  status: string
  context: string
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

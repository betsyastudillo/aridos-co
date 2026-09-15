import { createContext, useContext, useState } from 'react'
import { jwtDecode } from 'jwt-decode'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem('access_token'))

  const login = (accessToken) => {
    localStorage.setItem('access_token', accessToken)
    setToken(accessToken)
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    setToken(null)
  }

  let user = null
  if (token) {
    try {
      const decoded = jwtDecode(token)
      user = {
        documentId: decoded.sub,
        role: decoded.role,
        companyId: decoded.company_id,
      }
    } catch {
      user = null
    }
  }

  return (
    <AuthContext.Provider value={{ token, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
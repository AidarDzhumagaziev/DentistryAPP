import { createContext, useContext, useState } from 'react';

const AuthContext = createContext(null);
function getRole(token){
  if (!token){
    return null
  }
    const part = token.split('.')[1];
    const base = part.replace(/-/g, '+').replace(/_/g, '/');
    const data = JSON.parse(atob(base));
    return data.role;
}
export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem('access_token'));
  const role = getRole(token);

  function login(accessToken, refreshToken) {
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
    setToken(accessToken)
  }

  function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setToken(null)
  }

  return (
    <AuthContext.Provider value={{ token, login, logout, role }}>
      {children}
    </AuthContext.Provider>
  );
}

// eslint-disable-next-line react-refresh/only-export-components
export function useAuth() {
  return useContext(AuthContext);
}
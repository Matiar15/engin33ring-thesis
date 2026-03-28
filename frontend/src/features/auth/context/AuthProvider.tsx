import { ReactNode, useState, useCallback, useEffect } from 'react';
import { AuthContext } from './AuthContext';
import { authService } from '@/services/authService';

interface AuthProviderProps {
  children: ReactNode;
}

function decodeJWT(token: string): { sub?: string } | null {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return null;

    const payload = parts[1];
    const decoded = JSON.parse(atob(payload));
    return decoded;
  } catch {
    return null;
  }
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [token, setToken] = useState<string | null>(null);
  const [userId, setUserId] = useState<string | null>(null);

  // Initialize auth state from localStorage
  useEffect(() => {
    const storedToken = localStorage.getItem('auth_token');
    if (storedToken) {
      try {
        const decoded = decodeJWT(storedToken);
        if (decoded?.sub) {
          setToken(storedToken);
          setUserId(decoded.sub);
        }
      } catch (error) {
        console.error('Failed to decode token:', error);
        localStorage.removeItem('auth_token');
      }
    }
  }, []);

  const login = useCallback((newToken: string, newUserId: string) => {
    setToken(newToken);
    setUserId(newUserId);
    localStorage.setItem('auth_token', newToken);
  }, []);

  const logout = useCallback(() => {
    authService.logout();
    setToken(null);
    setUserId(null);
  }, []);

  const value = {
    userId,
    isAuthenticated: !!token,
    token,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}



'use client'

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { jwtDecode } from 'jwt-decode';

export function storeToken(token: string) {
  localStorage.setItem('platoro_token', token)
}

export function getToken(): string | null {
  return localStorage.getItem('platoro_token')
}

export function clearToken() {
  localStorage.removeItem('platoro_token')
}

interface AuthContextType {
  token: string | null;
  isAuthenticated: boolean;
  firstName: string | null;
  login: (token: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

function getFirstNameFromToken(token: string | null): string | null {
  if (!token) return null;
  try {
    const decoded: any = jwtDecode(token);
    if (decoded.name) {
      // Only use the first word as first name
      return decoded.name.split(' ')[0];
    }
    return null;
  } catch {
    return null;
  }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [firstName, setFirstName] = useState<string | null>(null);

  useEffect(() => {
    const stored = getToken();
    setToken(stored);
    setFirstName(getFirstNameFromToken(stored));
  }, []);

  const login = (newToken: string) => {
    storeToken(newToken);
    setToken(newToken);
    setFirstName(getFirstNameFromToken(newToken));
  };

  const logout = () => {
    clearToken();
    setToken(null);
    setFirstName(null);
  };

  return (
    <AuthContext.Provider value={{ token, isAuthenticated: !!token, firstName, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
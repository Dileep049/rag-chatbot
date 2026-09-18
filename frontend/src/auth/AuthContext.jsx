import React, { createContext, useContext, useState, useEffect } from 'react';
import { loginAdmin, checkAdminStatus } from '../services/api';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem('citizen_admin_token') || null);
  const [user, setUser] = useState(() => {
    try {
      const saved = localStorage.getItem('citizen_admin_user');
      return saved ? JSON.parse(saved) : null;
    } catch (e) {
      return null;
    }
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const verifySession = async () => {
      if (token) {
        try {
          const res = await checkAdminStatus();
          setUser(res.user);
          localStorage.setItem('citizen_admin_user', JSON.stringify(res.user));
        } catch (err) {
          console.warn('Session verification failed, logging out', err);
          logout();
        }
      } else {
        setUser(null);
      }
      setLoading(false);
    };

    verifySession();
  }, [token]);

  const login = async (email, password) => {
    const res = await loginAdmin(email, password);
    setToken(res.access_token);
    setUser(res.user);
    localStorage.setItem('citizen_admin_token', res.access_token);
    localStorage.setItem('citizen_admin_user', JSON.stringify(res.user));
    return res.user;
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('citizen_admin_token');
    localStorage.removeItem('citizen_admin_user');
  };

  const value = {
    token,
    user,
    loading,
    isAdmin: user?.role === 'admin',
    login,
    logout
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

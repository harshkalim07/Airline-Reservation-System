import React, { createContext, useState, useEffect } from "react";
import api from "../services/api";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem("sim_user")) || null;
    } catch {
      return null;
    }
  });

  const [loading, setLoading] = useState(false);

  // Register function
  async function register(email, password, role = 'user') {
    try {
      setLoading(true);
      const response = await api.post('/auth/signup', { email, password, role });
      
      if (response.data.access_token) {
        const userData = {
          ...response.data.user,
          token: response.data.access_token
        };
        
        setUser(userData);
        localStorage.setItem("sim_user", JSON.stringify(userData));
        localStorage.setItem("access_token", response.data.access_token);
      }
      
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Registration error:', error);
      const errorMessage = error.response?.data?.error || error.message || 'Registration failed';
      return { 
        success: false, 
        error: errorMessage
      };
    } finally {
      setLoading(false);
    }
  }

  // Login function
  async function login(email, password) {
    try {
      setLoading(true);
      const response = await api.post('/auth/login', { email, password });
      
      if (response.data.access_token) {
        const userData = {
          ...response.data.user,
          token: response.data.access_token
        };
        
        setUser(userData);
        localStorage.setItem("sim_user", JSON.stringify(userData));
        localStorage.setItem("access_token", response.data.access_token);
      }
      
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Login error:', error);
      const errorMessage = error.response?.data?.error || error.message || 'Login failed';
      return { 
        success: false, 
        error: errorMessage
      };
    } finally {
      setLoading(false);
    }
  }

  // Logout function
  function logout() {
    setUser(null);
    localStorage.removeItem("sim_user");
    localStorage.removeItem("access_token");
  }

  return (
    <AuthContext.Provider value={{ user, login, logout, register, loading }}>
      {children}
    </AuthContext.Provider>
  );
}
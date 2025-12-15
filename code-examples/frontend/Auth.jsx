// components/Auth.js

import { useState, useEffect, useCallback } from 'react';
import api from '../components/Api'; // Import the centralized api instance
import { useNavigate } from 'react-router-dom';

export function useAuth() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  // Use a state variable to hold the tenantName
  const [tenantName, setTenantName] = useState(() => localStorage.getItem('tenantName') || '');
  const [baseURL, setBaseURL] = useState(() => `http://${tenantName}.localhost:8000/`);

  // Update localStorage when tenantName changes
  useEffect(() => {
    if (tenantName) {
      localStorage.setItem('tenantName', tenantName);
      setBaseURL(`http://${tenantName}.localhost:8000/`);
    }
  }, [tenantName]);

  const url = `/api/token/`;

  useEffect(() => {
    api.defaults.baseURL = baseURL;
  }, [baseURL]);

  const handleLogout = useCallback(() => {
    try {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user_data');
      localStorage.removeItem('tenantName');
      localStorage.removeItem('token_expiration');
      // Remove company data from local storage on logout
      localStorage.removeItem('company_data');
      navigate('/login'); // Weiterleitung zur Login-Seite
      // Reset tenantName state on logout
      setTenantName('');
    } catch (error) {
      console.error('Failed to logout:', error);
    }
  }, [navigate, setTenantName]);

  useEffect(() => {
    const handleUserActivity = () => {
      const expirationTime = localStorage.getItem('token_expiration');
      if (expirationTime && Date.now() > expirationTime) {
        handleLogout(); // Benutzer ausloggen
      } else {
        // Token-Lebensdauer verlängern, basierend auf Aktivität
        const newExpirationTime = Date.now() + 1800000; // 30 Minuten
        localStorage.setItem('token_expiration', newExpirationTime);
      }
    };

    window.addEventListener('mousemove', handleUserActivity);
    window.addEventListener('keypress', handleUserActivity);
    window.addEventListener('scroll', handleUserActivity);

    return () => {
      window.removeEventListener('mousemove', handleUserActivity);
      window.removeEventListener('keypress', handleUserActivity);
      window.removeEventListener('scroll', handleUserActivity);
    };
  }, [handleLogout]);

  useEffect(() => {
    const checkTokenExpiration = () => {
      const expirationTime = localStorage.getItem('token_expiration');
      if (expirationTime && Date.now() > expirationTime) {
        handleLogout(); // Benutzer ausloggen
      }
    };

    const interval = setInterval(checkTokenExpiration, 60000); // Überprüfung jede Minute
    return () => clearInterval(interval);
  }, [handleLogout]);

  api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  }, (error) => {
    return Promise.reject(error);
  });

  api.interceptors.response.use((response) => {
    return response;
  }, (error) => {
    if (error.response && error.response.status === 401) {
      handleLogout(); // Token abgelaufen, also ausloggen und zur Login-Seite navigieren
    }
    return Promise.reject(error);
  });

  // Funktion zum Überprüfen und Löschen des Tokens bei Ablauf
  useEffect(() => {
    const checkTokenExpiration = () => {
      const access_token = localStorage.getItem('access_token');
      const refresh_token = localStorage.getItem('refresh_token');
      if (access_token) {
        try {
          const { exp } = JSON.parse(atob(access_token.split('.')[1]));
          if (exp * 1000 < Date.now()) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user_data');
            localStorage.removeItem('tenantName');
            localStorage.removeItem('token_expiration');
            navigate('/login'); // Weiterleitung zur Login-Seite
          }
        } catch (error) {
          console.error('Error parsing JWT:', error);
        }
      }
      if (refresh_token) {
        try {
          const { exp } = JSON.parse(atob(refresh_token.split('.')[1]));
          if (exp * 1000 < Date.now()) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user_data');
            navigate('/login'); // Weiterleitung zur Login-Seite
          }
        } catch (error) {
          console.error('Error parsing JWT:', error);
        }
      }
    };

    // Überprüfen alle 10 Minuten (600000 Millisekunden)
    const interval = setInterval(checkTokenExpiration, 600000);
    return () => clearInterval(interval); // Aufräumen beim Entladen der Komponente
  }, [navigate]);

  const handleLogin = useCallback(async (event) => {
    event.preventDefault();
    setIsLoading(true);
    try {
      const response = await api.post(url, {
        username: username,
        password: password
      });
      const { access, refresh, user_id, username: resUsername, email, role, company_name, company_id, mitarbeiter_kuerzel, first_name, last_name, tenant_name } = response.data;

      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      localStorage.setItem('user_data', JSON.stringify({
        user_id,
        username: resUsername,
        email,
        role,
        company_name,
        mitarbeiter_kuerzel,
        company_id,
        first_name,
        last_name,
      }));

      // Function to fetch company data
      const fetchCompanyData = async (companyId) => {
        try {
          const companyResponse = await api.get(`/api/company/${companyId}/`);
          localStorage.setItem('company_data', JSON.stringify(companyResponse.data));
        } catch (error) {
          console.error("Could not fetch company data:", error);
          // Set default company data in local storage
          localStorage.setItem('company_data', JSON.stringify({
            header_text: '[Header Text]',
            footer_text: '[Footer Text]'
          }));
        }
      };

      // Fetch company data and store it in local storage
      await fetchCompanyData(company_id);

      // Update the tenantName state
      setTenantName(tenant_name);

      setIsLoading(false);
      navigate('/dashboard');
    } catch (err) {
      setIsLoading(false);
      if (err.response && err.response.data) {
        setError(err.response.data.detail);
      } else {
        setError('Failed to login');
      }
    }
  }, [username, password, navigate, url]);

  const isAuthenticated = useCallback(() => {
    const token = localStorage.getItem('access_token');
    return token !== null;
  }, []);

  return {
    username,
    setUsername,
    password,
    setPassword,
    error,
    setError,
    tenantName,
    setTenantName,
    isLoading,
    setIsLoading,
    handleLogin,
    handleLogout,
    isAuthenticated
  };
}
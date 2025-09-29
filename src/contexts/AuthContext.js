import React, { createContext, useState, useContext, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import api from '../services/api';

const AuthContext = createContext();

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider');
    }
    return context;
};

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        checkAuth();
    }, []);

    const checkAuth = async () => {
        const token = localStorage.getItem('access_token');
        if (token) {
            try {
                const decoded = jwtDecode(token);
                if (decoded.exp * 1000 > Date.now()) {
                    const response = await api.get('/api/me/');
                    setUser(response.data);
                } else {
                    await refreshToken();
                }
            } catch (error) {
                console.error('Auth check failed:', error);
                logout();
            }
        }
        setLoading(false);
    };

    const login = async (username, password) => {
        const response = await api.post('/api/token/', { username, password });
        const { access, refresh } = response.data;

        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);

        const userResponse = await api.get('/api/me/');
        setUser(userResponse.data);

        return userResponse.data;
    };

    const register = async (userData) => {
        const response = await api.post('/api/register/', userData);
        return response.data;
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setUser(null);
    };

    const refreshToken = async () => {
        try {
            const refresh = localStorage.getItem('refresh_token');
            const response = await api.post('/api/token/refresh/', { refresh });
            const { access } = response.data;
            localStorage.setItem('access_token', access);

            const userResponse = await api.get('/api/me/');
            setUser(userResponse.data);
        } catch (error) {
            logout();
        }
    };

    const updateProfile = async (profileData) => {
        const response = await api.patch('/api/me/', profileData);
        setUser(response.data);
        return response.data;
    };

    const value = {
        user,
        loading,
        login,
        register,
        logout,
        updateProfile,
        isAuthenticated: !!user,
        isAdmin: user?.is_staff || false,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
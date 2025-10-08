import React, { createContext, useState, useEffect, type ReactNode } from 'react';
import { authService } from '../services/authService';
import { getAccessToken, clearTokens, isTokenExpired } from '../services/api';
import type { User, LoginCredentials, RegisterData } from '../types';

interface AuthContextType {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    login: (credentials: LoginCredentials) => Promise<void>;
    register: (data: RegisterData) => Promise<void>;
    logout: () => Promise<void>;
    refreshUser: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
    children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    // Check if user is authenticated on mount
    useEffect(() => {
        const checkAuth = async () => {
            const token = getAccessToken();
            if (token && !isTokenExpired(token)) {
                try {
                    const userData = await authService.getProfile();
                    setUser(userData);
                } catch (error) {
                    console.error('Failed to fetch user profile:', error);
                    clearTokens();
                }
            }
            setIsLoading(false);
        };

        checkAuth();
    }, []);

    const login = async (credentials: LoginCredentials) => {
        const response = await authService.login(credentials);
        setUser(response.user);
    };

    const register = async (data: RegisterData) => {
        const response = await authService.register(data);
        setUser(response.user);
    };

    const logout = async () => {
        try {
            await authService.logout();
        } finally {
            setUser(null);
            clearTokens();
        }
    };

    const refreshUser = async () => {
        try {
            const userData = await authService.getProfile();
            setUser(userData);
        } catch (error) {
            console.error('Failed to refresh user:', error);
            throw error;
        }
    };

    const value: AuthContextType = {
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        register,
        logout,
        refreshUser,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

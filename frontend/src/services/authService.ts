import api, { setTokens, clearTokens } from './api';
import type {
    LoginCredentials,
    RegisterData,
    AuthResponse,
    User,
} from '../types';

export const authService = {
    // Login
    async login(credentials: LoginCredentials): Promise<AuthResponse> {
        const response = await api.post<AuthResponse>('/auth/login/', credentials);
        const { tokens } = response.data;
        setTokens(tokens.access, tokens.refresh);
        return response.data;
    },

    // Register
    async register(data: RegisterData): Promise<AuthResponse> {
        const response = await api.post<AuthResponse>('/auth/register/', data);
        const { tokens } = response.data;
        setTokens(tokens.access, tokens.refresh);
        return response.data;
    },

    // Logout
    async logout(): Promise<void> {
        try {
            await api.post('/auth/logout/');
        } finally {
            clearTokens();
        }
    },

    // Get current user profile
    async getProfile(): Promise<User> {
        const response = await api.get<User>('/auth/user/');
        return response.data;
    },

    // Update user profile
    async updateProfile(data: Partial<User>): Promise<User> {
        const response = await api.put<User>('/auth/user/', data);
        return response.data;
    },

    // Change password
    async changePassword(data: {
        old_password: string;
        new_password: string;
    }): Promise<{ message: string }> {
        const response = await api.post('/auth/change-password/', data);
        return response.data;
    },

    // Forgot password - Send OTP
    async forgotPassword(email: string): Promise<{ message: string; email: string; expires_in: string }> {
        const response = await api.post('/auth/forgot-password/', { email });
        return response.data;
    },

    // Verify OTP
    async verifyOTP(email: string, otp_code: string): Promise<{ message: string; valid: boolean }> {
        const response = await api.post('/auth/verify-otp/', { email, otp_code });
        return response.data;
    },

    // Reset password with OTP
    async resetPassword(
        email: string,
        otp_code: string,
        new_password: string,
        confirm_password: string
    ): Promise<{ message: string; user: User }> {
        const response = await api.post('/auth/reset-password/', {
            email,
            otp_code,
            new_password,
            confirm_password
        });
        return response.data;
    },

    // Resend OTP
    async resendOTP(email: string): Promise<{ message: string; email: string; expires_in: string }> {
        const response = await api.post('/auth/resend-otp/', { email });
        return response.data;
    },
};

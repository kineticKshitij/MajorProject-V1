import { useState, type FormEvent } from 'react';
import { Link } from 'react-router-dom';
import { authService } from '../../services/authService';

const ForgotPassword = () => {
    const [step, setStep] = useState<'email' | 'otp' | 'password'>('email');
    const [email, setEmail] = useState('');
    const [otpCode, setOtpCode] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [canResend, setCanResend] = useState(true);
    const [resendTimer, setResendTimer] = useState(0);

    const handleSendOTP = async (e: FormEvent) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        setIsLoading(true);

        try {
            await authService.forgotPassword(email);
            setSuccess('OTP sent successfully! Please check your email.');
            setStep('otp');
            startResendTimer();
        } catch (err: any) {
            setError(
                err.response?.data?.error ||
                err.response?.data?.email?.[0] ||
                'Failed to send OTP. Please try again.'
            );
        } finally {
            setIsLoading(false);
        }
    };

    const handleVerifyOTP = async (e: FormEvent) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        try {
            await authService.verifyOTP(email, otpCode);
            setSuccess('OTP verified! Please enter your new password.');
            setStep('password');
        } catch (err: any) {
            setError(
                err.response?.data?.error ||
                err.response?.data?.non_field_errors?.[0] ||
                'Invalid OTP. Please try again.'
            );
        } finally {
            setIsLoading(false);
        }
    };

    const handleResetPassword = async (e: FormEvent) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        if (newPassword !== confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        if (newPassword.length < 8) {
            setError('Password must be at least 8 characters long');
            return;
        }

        setIsLoading(true);

        try {
            await authService.resetPassword(email, otpCode, newPassword, confirmPassword);
            setSuccess('Password reset successful! You can now log in with your new password.');
            setTimeout(() => {
                window.location.href = '/login';
            }, 2000);
        } catch (err: any) {
            setError(
                err.response?.data?.error ||
                err.response?.data?.new_password?.[0] ||
                err.response?.data?.non_field_errors?.[0] ||
                'Failed to reset password. Please try again.'
            );
        } finally {
            setIsLoading(false);
        }
    };

    const handleResendOTP = async () => {
        if (!canResend) return;

        setError('');
        setSuccess('');
        setIsLoading(true);

        try {
            await authService.resendOTP(email);
            setSuccess('New OTP sent successfully!');
            startResendTimer();
        } catch (err: any) {
            setError(
                err.response?.data?.error ||
                'Failed to resend OTP. Please try again.'
            );
        } finally {
            setIsLoading(false);
        }
    };

    const startResendTimer = () => {
        setCanResend(false);
        setResendTimer(60);
        const interval = setInterval(() => {
            setResendTimer((prev) => {
                if (prev <= 1) {
                    clearInterval(interval);
                    setCanResend(true);
                    return 0;
                }
                return prev - 1;
            });
        }, 1000);
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-md w-full space-y-8">
                <div>
                    <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
                        {step === 'email' && 'Forgot Password'}
                        {step === 'otp' && 'Verify OTP'}
                        {step === 'password' && 'Reset Password'}
                    </h2>
                    <p className="mt-2 text-center text-sm text-gray-600">
                        {step === 'email' && "Enter your email and we'll send you an OTP"}
                        {step === 'otp' && 'Enter the 6-digit code sent to your email'}
                        {step === 'password' && 'Create a new password for your account'}
                    </p>
                </div>

                {error && (
                    <div className="rounded-md bg-red-50 p-4">
                        <p className="text-sm text-red-800">{error}</p>
                    </div>
                )}

                {success && (
                    <div className="rounded-md bg-green-50 p-4">
                        <p className="text-sm text-green-800">{success}</p>
                    </div>
                )}

                {step === 'email' && (
                    <form className="mt-8 space-y-6" onSubmit={handleSendOTP}>
                        <div>
                            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                                Email Address
                            </label>
                            <input
                                id="email"
                                name="email"
                                type="email"
                                required
                                className="input-field"
                                placeholder="Enter your email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />
                        </div>

                        <button
                            type="submit"
                            disabled={isLoading}
                            className="w-full btn-primary"
                        >
                            {isLoading ? 'Sending...' : 'Send OTP'}
                        </button>

                        <div className="text-center">
                            <Link
                                to="/login"
                                className="text-sm font-medium text-primary-600 hover:text-primary-500"
                            >
                                Back to Login
                            </Link>
                        </div>
                    </form>
                )}

                {step === 'otp' && (
                    <form className="mt-8 space-y-6" onSubmit={handleVerifyOTP}>
                        <div>
                            <label htmlFor="otp" className="block text-sm font-medium text-gray-700 mb-1">
                                OTP Code
                            </label>
                            <input
                                id="otp"
                                name="otp"
                                type="text"
                                maxLength={6}
                                required
                                className="input-field text-center text-2xl tracking-widest"
                                placeholder="000000"
                                value={otpCode}
                                onChange={(e) => setOtpCode(e.target.value.replace(/\D/g, ''))}
                            />
                            <p className="mt-2 text-xs text-gray-500 text-center">
                                OTP sent to {email}
                            </p>
                        </div>

                        <button
                            type="submit"
                            disabled={isLoading || otpCode.length !== 6}
                            className="w-full btn-primary"
                        >
                            {isLoading ? 'Verifying...' : 'Verify OTP'}
                        </button>

                        <div className="text-center space-y-2">
                            <button
                                type="button"
                                onClick={handleResendOTP}
                                disabled={!canResend || isLoading}
                                className="text-sm font-medium text-primary-600 hover:text-primary-500 disabled:text-gray-400 disabled:cursor-not-allowed"
                            >
                                {canResend ? 'Resend OTP' : `Resend in ${resendTimer}s`}
                            </button>
                            <div>
                                <button
                                    type="button"
                                    onClick={() => setStep('email')}
                                    className="text-sm font-medium text-gray-600 hover:text-gray-500"
                                >
                                    Change Email
                                </button>
                            </div>
                        </div>
                    </form>
                )}

                {step === 'password' && (
                    <form className="mt-8 space-y-6" onSubmit={handleResetPassword}>
                        <div className="space-y-4">
                            <div>
                                <label htmlFor="newPassword" className="block text-sm font-medium text-gray-700 mb-1">
                                    New Password
                                </label>
                                <input
                                    id="newPassword"
                                    name="newPassword"
                                    type="password"
                                    required
                                    className="input-field"
                                    placeholder="Enter new password"
                                    value={newPassword}
                                    onChange={(e) => setNewPassword(e.target.value)}
                                />
                            </div>

                            <div>
                                <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
                                    Confirm Password
                                </label>
                                <input
                                    id="confirmPassword"
                                    name="confirmPassword"
                                    type="password"
                                    required
                                    className="input-field"
                                    placeholder="Confirm new password"
                                    value={confirmPassword}
                                    onChange={(e) => setConfirmPassword(e.target.value)}
                                />
                            </div>
                        </div>

                        <div className="bg-blue-50 p-4 rounded-md">
                            <p className="text-xs text-blue-800">
                                <strong>Password requirements:</strong>
                            </p>
                            <ul className="mt-2 text-xs text-blue-700 list-disc list-inside">
                                <li>At least 8 characters long</li>
                                <li>Include uppercase and lowercase letters</li>
                                <li>Include numbers</li>
                                <li>Include special characters</li>
                            </ul>
                        </div>

                        <button
                            type="submit"
                            disabled={isLoading}
                            className="w-full btn-primary"
                        >
                            {isLoading ? 'Resetting...' : 'Reset Password'}
                        </button>
                    </form>
                )}
            </div>
        </div>
    );
};

export default ForgotPassword;

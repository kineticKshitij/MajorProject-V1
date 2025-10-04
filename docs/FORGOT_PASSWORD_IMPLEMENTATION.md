# Forgot Password with OTP - Implementation Guide

## 🎉 Feature Complete!

A complete password reset flow has been implemented with OTP verification via email.

## ✅ What Was Implemented

### Backend (Django)

1. **New Model: `PasswordResetOTP`**
   - Location: `accounts/models.py`
   - Features:
     - 6-digit OTP code generation
     - 10-minute expiration
     - IP address tracking
     - One-time use validation
     - Automatic expiration checking

2. **Email Utilities**
   - Location: `accounts/email_utils.py`
   - Features:
     - Professional HTML email templates
     - OTP delivery email with security warnings
     - Password reset success confirmation email
     - Plain text fallback for email clients

3. **API Serializers**
   - Location: `accounts/serializers.py`
   - Added:
     - `ForgotPasswordSerializer` - Email validation
     - `VerifyOTPSerializer` - OTP verification
     - `ResetPasswordSerializer` - Password reset with validation
     - Complete field validation and error handling

4. **API Endpoints**
   - Location: `accounts/api_views.py`
   - **POST** `/api/auth/forgot-password/` - Send OTP to email
   - **POST** `/api/auth/verify-otp/` - Verify OTP code
   - **POST** `/api/auth/reset-password/` - Reset password with OTP
   - **POST** `/api/auth/resend-otp/` - Resend OTP (with rate limiting)
   
5. **Features Implemented**:
   - ✅ Rate limiting (max 3 OTPs per 5 minutes)
   - ✅ Automatic invalidation of old OTPs
   - ✅ IP address logging for security
   - ✅ Email verification
   - ✅ Password validation
   - ✅ Success confirmation emails

6. **Email Configuration**
   - Location: `InformationExtractor/settings.py`
   - Development: Console backend (emails appear in terminal)
   - Production: SMTP configuration ready (via environment variables)

7. **Admin Interface**
   - Location: `accounts/admin.py`
   - View all OTP requests
   - Monitor OTP status (valid/expired/used)
   - Track IP addresses
   - Search by user/email/OTP code

### Frontend (React + TypeScript)

1. **ForgotPassword Component**
   - Location: `frontend/src/components/auth/ForgotPassword.tsx`
   - Features:
     - **3-Step Flow**:
       1. Enter email → Send OTP
       2. Verify 6-digit OTP → Enable password reset
       3. Create new password → Complete reset
     - Real-time OTP validation (6 digits only)
     - 60-second resend timer
     - Password strength requirements display
     - Error handling with user-friendly messages
     - Success messages with auto-redirect

2. **Auth Service Updates**
   - Location: `frontend/src/services/authService.ts`
   - Added methods:
     - `forgotPassword(email)` - Request OTP
     - `verifyOTP(email, otp_code)` - Verify OTP
     - `resetPassword(email, otp_code, new_password, confirm_password)` - Reset password
     - `resendOTP(email)` - Request new OTP

3. **UI/UX Features**:
   - ✅ Loading states with spinners
   - ✅ Disabled buttons during operations
   - ✅ Auto-redirect after successful reset
   - ✅ "Back to Login" navigation
   - ✅ "Change Email" option
   - ✅ Resend OTP with countdown timer
   - ✅ Password requirements tooltip
   - ✅ Real-time input validation

4. **Login Page Update**
   - Added "Forgot your password?" link
   - Links to `/forgot-password` route

5. **Routing**
   - Location: `frontend/src/App.tsx`
   - Added public route: `/forgot-password`

## 🚀 How to Use

### User Flow

1. **Forgot Password**
   - Navigate to login page
   - Click "Forgot your password?"
   - Enter registered email address
   - Click "Send OTP"

2. **Verify OTP**
   - Check email for 6-digit OTP (valid for 10 minutes)
   - Enter OTP in verification form
   - Click "Verify OTP"
   - Can resend OTP after 60 seconds if needed

3. **Reset Password**
   - Enter new password (must meet requirements)
   - Confirm new password
   - Click "Reset Password"
   - Redirected to login page automatically

### Testing in Development

Since email backend is set to console mode in development:

```bash
# Terminal 1: Run Django server
cd D:\MP@
.\env\Scripts\Activate.ps1
python manage.py runserver

# Terminal 2: Run React dev server
cd frontend
npm run dev

# Open browser
http://localhost:5173/forgot-password
```

**To see OTP codes**: Check the Django server terminal - emails will be printed there!

### Example OTP Email (Console Output)

```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Subject: Password Reset OTP - Information Extractor
From: noreply@informationextractor.com
To: user@example.com

Hi John Doe,

You recently requested to reset your password for your Information Extractor account.

Your OTP Code: 123456

This OTP is valid for 10 minutes only.

Security Notice:
- Never share this OTP with anyone
- If you didn't request this, please ignore this email
- Your password won't change unless you use this OTP

Best regards,
Information Extractor Team
```

## 🔐 Security Features

1. **OTP Security**
   - 6-digit random codes
   - 10-minute expiration
   - One-time use only
   - Automatic invalidation of old OTPs

2. **Rate Limiting**
   - Max 3 OTP requests per 5 minutes
   - Prevents brute force attacks
   - Returns 429 status when limit exceeded

3. **Password Validation**
   - Django's built-in password validators
   - Minimum 8 characters
   - Must include uppercase, lowercase, numbers, special chars
   - Validation on both frontend and backend

4. **IP Tracking**
   - All OTP requests logged with IP address
   - Helps identify suspicious activity
   - Visible in Django admin

5. **Email Verification**
   - Only registered emails can request OTP
   - User must have email in database
   - Prevents email enumeration attacks (shows same message for invalid emails)

## 📧 Email Configuration for Production

To enable actual email sending in production, update your environment variables:

```bash
# .env file
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

**For Gmail:**
1. Enable 2-factor authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use App Password in `EMAIL_HOST_PASSWORD`

**For other providers:**
- Mailgun: `smtp.mailgun.org:587`
- SendGrid: `smtp.sendgrid.net:587`
- AWS SES: `email-smtp.region.amazonaws.com:587`

## 🛠️ API Documentation

### 1. Request OTP

```http
POST /api/auth/forgot-password/
Content-Type: application/json

{
  "email": "user@example.com"
}
```

**Response (200 OK)**:
```json
{
  "message": "OTP has been sent to your email address",
  "email": "user@example.com",
  "expires_in": "10 minutes"
}
```

### 2. Verify OTP

```http
POST /api/auth/verify-otp/
Content-Type: application/json

{
  "email": "user@example.com",
  "otp_code": "123456"
}
```

**Response (200 OK)**:
```json
{
  "message": "OTP verified successfully",
  "valid": true
}
```

### 3. Reset Password

```http
POST /api/auth/reset-password/
Content-Type: application/json

{
  "email": "user@example.com",
  "otp_code": "123456",
  "new_password": "NewSecurePass123!",
  "confirm_password": "NewSecurePass123!"
}
```

**Response (200 OK)**:
```json
{
  "message": "Password reset successful. You can now log in with your new password.",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### 4. Resend OTP

```http
POST /api/auth/resend-otp/
Content-Type: application/json

{
  "email": "user@example.com"
}
```

**Response (200 OK)**:
```json
{
  "message": "New OTP has been sent to your email address",
  "email": "user@example.com",
  "expires_in": "10 minutes"
}
```

**Response (429 Too Many Requests)**:
```json
{
  "error": "Too many OTP requests. Please try again after 5 minutes."
}
```

## 🎨 UI Screenshots Description

### Step 1: Enter Email
- Clean form with email input
- "Send OTP" button
- "Back to Login" link
- Professional card design

### Step 2: Verify OTP
- Large 6-digit input field with letter spacing
- Shows email where OTP was sent
- "Resend OTP" button with countdown timer
- "Change Email" option to go back

### Step 3: Reset Password
- Two password fields (new and confirm)
- Password requirements list displayed
- Security guidelines
- "Reset Password" button

### Success State
- Green success message
- Auto-redirect countdown
- Confirmation that password was changed

## 📱 Responsive Design

All components are fully responsive:
- Mobile: Stacked layout, full-width inputs
- Tablet: Optimized spacing
- Desktop: Centered card with max-width

## 🐛 Error Handling

**Frontend handles**:
- Network errors
- Invalid OTP
- Expired OTP
- Password mismatch
- Weak passwords
- Email not found

**Backend validates**:
- Email format
- OTP validity (not expired, not used)
- Password strength
- Rate limits

## 📝 Database Migrations

Migrations have been created and applied:

```bash
python manage.py makemigrations  # ✅ Created 0002_passwordresetotp.py
python manage.py migrate         # ✅ Applied successfully
```

## 🎯 Next Steps

The forgot password feature is **100% complete and ready to use!**

To test it:
1. Make sure Django server is running
2. Make sure React dev server is running
3. Navigate to http://localhost:5173/login
4. Click "Forgot your password?"
5. Follow the 3-step flow
6. Check Django terminal for OTP codes

Ready to move on to building the Dorks features! 🚀

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_otp_email(user, otp_code):
    """
    Send OTP email to user for password reset
    """
    subject = 'Password Reset OTP - Information Extractor'
    
    # HTML email content
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f9fafb;
            }}
            .header {{
                background-color: #2563eb;
                color: white;
                padding: 20px;
                text-align: center;
                border-radius: 8px 8px 0 0;
            }}
            .content {{
                background-color: white;
                padding: 30px;
                border-radius: 0 0 8px 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .otp-box {{
                background-color: #eff6ff;
                border: 2px solid #2563eb;
                border-radius: 8px;
                padding: 20px;
                text-align: center;
                margin: 20px 0;
            }}
            .otp-code {{
                font-size: 32px;
                font-weight: bold;
                color: #2563eb;
                letter-spacing: 8px;
                margin: 10px 0;
            }}
            .warning {{
                background-color: #fef3c7;
                border-left: 4px solid #f59e0b;
                padding: 15px;
                margin: 20px 0;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                color: #6b7280;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Password Reset Request</h1>
            </div>
            <div class="content">
                <p>Hi {user.get_full_name() or user.username},</p>
                
                <p>You recently requested to reset your password for your Information Extractor account. Use the OTP code below to complete the password reset:</p>
                
                <div class="otp-box">
                    <p style="margin: 0; color: #6b7280;">Your OTP Code:</p>
                    <div class="otp-code">{otp_code}</div>
                    <p style="margin: 0; color: #6b7280; font-size: 14px;">Valid for 10 minutes</p>
                </div>
                
                <div class="warning">
                    <strong>⚠️ Security Notice:</strong>
                    <ul style="margin: 10px 0;">
                        <li>This OTP is valid for 10 minutes only</li>
                        <li>Never share this OTP with anyone</li>
                        <li>If you didn't request this, please ignore this email</li>
                        <li>Your password won't change unless you use this OTP</li>
                    </ul>
                </div>
                
                <p>If you didn't request a password reset, you can safely ignore this email. Your account is still secure.</p>
                
                <p>Best regards,<br>
                Information Extractor Team</p>
            </div>
            <div class="footer">
                <p>This is an automated email. Please do not reply to this message.</p>
                <p>&copy; 2025 Information Extractor. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Plain text version (fallback)
    plain_message = f"""
    Hi {user.get_full_name() or user.username},
    
    You recently requested to reset your password for your Information Extractor account.
    
    Your OTP Code: {otp_code}
    
    This OTP is valid for 10 minutes only.
    
    Security Notice:
    - Never share this OTP with anyone
    - If you didn't request this, please ignore this email
    - Your password won't change unless you use this OTP
    
    Best regards,
    Information Extractor Team
    """
    
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending OTP email: {str(e)}")
        return False


def send_password_reset_success_email(user):
    """
    Send confirmation email after successful password reset
    """
    subject = 'Password Reset Successful - Information Extractor'
    
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f9fafb;
            }}
            .header {{
                background-color: #10b981;
                color: white;
                padding: 20px;
                text-align: center;
                border-radius: 8px 8px 0 0;
            }}
            .content {{
                background-color: white;
                padding: 30px;
                border-radius: 0 0 8px 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .success-icon {{
                font-size: 64px;
                text-align: center;
                margin: 20px 0;
            }}
            .warning {{
                background-color: #fee2e2;
                border-left: 4px solid #ef4444;
                padding: 15px;
                margin: 20px 0;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                color: #6b7280;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>✓ Password Reset Successful</h1>
            </div>
            <div class="content">
                <div class="success-icon">✅</div>
                
                <p>Hi {user.get_full_name() or user.username},</p>
                
                <p>Your password has been successfully reset. You can now log in to your Information Extractor account with your new password.</p>
                
                <div class="warning">
                    <strong>⚠️ Important:</strong>
                    <p>If you did not make this change, please contact us immediately. Someone may have unauthorized access to your account.</p>
                </div>
                
                <p>For security reasons, we recommend that you:</p>
                <ul>
                    <li>Use a strong, unique password</li>
                    <li>Never share your password with anyone</li>
                    <li>Enable two-factor authentication if available</li>
                </ul>
                
                <p>Best regards,<br>
                Information Extractor Team</p>
            </div>
            <div class="footer">
                <p>This is an automated email. Please do not reply to this message.</p>
                <p>&copy; 2025 Information Extractor. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = f"""
    Hi {user.get_full_name() or user.username},
    
    Your password has been successfully reset.
    
    If you did not make this change, please contact us immediately.
    
    Best regards,
    Information Extractor Team
    """
    
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending confirmation email: {str(e)}")
        return False

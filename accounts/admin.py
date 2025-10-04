from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, PasswordResetOTP


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'has_gemini_api_key', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'is_email_verified')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('API Configuration', {'fields': ('gemini_api_key',)}),
        ('Email Verification', {'fields': ('is_email_verified',)}),
    )
    
    def has_gemini_api_key(self, obj):
        return obj.has_gemini_api_key()
    has_gemini_api_key.boolean = True
    has_gemini_api_key.short_description = 'Has API Key'


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)


@admin.register(PasswordResetOTP)
class PasswordResetOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp_code', 'created_at', 'expires_at', 'is_used', 'is_valid_status', 'ip_address')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__username', 'user__email', 'otp_code', 'ip_address')
    readonly_fields = ('created_at', 'expires_at')
    ordering = ('-created_at',)
    
    def is_valid_status(self, obj):
        return obj.is_valid()
    is_valid_status.boolean = True
    is_valid_status.short_description = 'Valid'
    
    def has_add_permission(self, request):
        # Prevent manual creation of OTPs through admin
        return False

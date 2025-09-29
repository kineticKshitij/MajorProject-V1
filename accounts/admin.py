from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


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
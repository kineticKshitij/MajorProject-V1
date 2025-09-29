from django.contrib import admin
from django.utils.html import format_html
from .models import DorkCategory, GoogleDork, SearchResult, SearchSession, DorkBookmark


@admin.register(DorkCategory)
class DorkCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_dork_count', 'color_display', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']

    def color_display(self, obj):
        return format_html(
            '<span style="background-color: {}; padding: 3px 10px; border-radius: 3px; color: white;">{}</span>',
            obj.color,
            obj.color
        )
    color_display.short_description = 'Color'


@admin.register(GoogleDork)
class GoogleDorkAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'risk_level', 'usage_count', 'is_active', 'created_at']
    list_filter = ['category', 'difficulty', 'risk_level', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'query', 'tags']
    readonly_fields = ['created_at', 'updated_at', 'usage_count']
    list_editable = ['is_active']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'category', 'difficulty', 'risk_level')
        }),
        ('Query Details', {
            'fields': ('query', 'description', 'tags')
        }),
        ('Status', {
            'fields': ('is_active', 'created_by')
        }),
        ('Statistics', {
            'fields': ('usage_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SearchResult)
class SearchResultAdmin(admin.ModelAdmin):
    list_display = ['title_truncated', 'domain', 'dork', 'is_interesting', 'search_date']
    list_filter = ['is_interesting', 'search_date', 'dork__category']
    search_fields = ['title', 'url', 'domain', 'snippet']
    readonly_fields = ['search_date', 'domain']
    list_editable = ['is_interesting']
    ordering = ['-search_date']

    def title_truncated(self, obj):
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
    title_truncated.short_description = 'Title'


@admin.register(SearchSession)
class SearchSessionAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'total_results', 'is_completed', 'created_at']
    list_filter = ['created_at', 'completed_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'completed_at', 'total_results']
    filter_horizontal = ['dorks']

    def is_completed(self, obj):
        return obj.is_completed()
    is_completed.boolean = True
    is_completed.short_description = 'Completed'


@admin.register(DorkBookmark)
class DorkBookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'dork', 'created_at']
    list_filter = ['created_at', 'dork__category']
    search_fields = ['user__username', 'dork__title', 'notes']
    readonly_fields = ['created_at']

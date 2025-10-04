from django.contrib import admin
from django.utils.html import format_html
from .models import DorkCategory, GoogleDork, SearchResult, SearchSession, DorkBookmark
from .models_entity import (
    EntityType, Entity, EntityAttribute, EntitySearchTemplate,
    EntitySearchSession, EntitySearchResult, EntityRelationship, EntityNote
)


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
    list_display = ['title', 'category', 'difficulty', 'risk_level', 'supports_entities', 'usage_count', 'is_active', 'created_at']
    list_filter = ['category', 'difficulty', 'risk_level', 'supports_entities', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'query', 'tags']
    readonly_fields = ['created_at', 'updated_at', 'usage_count']
    list_editable = ['is_active', 'supports_entities']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'category', 'difficulty', 'risk_level')
        }),
        ('Query Details', {
            'fields': ('query', 'description', 'tags')
        }),
        ('Entity Support', {
            'fields': ('supports_entities', 'entity_placeholders'),
            'description': 'Configure entity-specific search capabilities'
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
    list_display = ['title_truncated', 'domain', 'dork', 'entity', 'is_interesting', 'search_date']
    list_filter = ['is_interesting', 'search_date', 'dork__category', 'entity__entity_type']
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


# Entity Admin Classes

@admin.register(EntityType)
class EntityTypeAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'name', 'color_display', 'icon_display', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'display_name', 'description']
    list_editable = ['is_active']
    readonly_fields = ['created_at']

    def color_display(self, obj):
        return format_html(
            '<span style="background-color: {}; padding: 3px 10px; border-radius: 3px; color: white;">{}</span>',
            obj.color,
            obj.color
        )
    color_display.short_description = 'Color'

    def icon_display(self, obj):
        return format_html('<i class="{}"></i> {}', obj.icon, obj.icon)
    icon_display.short_description = 'Icon'


class EntityAttributeInline(admin.TabularInline):
    model = EntityAttribute
    extra = 0
    fields = ['key', 'value', 'value_type', 'confidence', 'is_public']


class EntityNoteInline(admin.TabularInline):
    model = EntityNote
    extra = 0
    fields = ['title', 'note_type', 'priority', 'is_private']
    readonly_fields = ['created_at']


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ['name', 'entity_type', 'status', 'priority', 'search_count', 'created_by', 'created_at']
    list_filter = ['entity_type', 'status', 'priority', 'created_at', 'last_researched']
    search_fields = ['name', 'description', 'location', 'industry']
    readonly_fields = ['id', 'created_at', 'updated_at', 'search_count', 'results_found']
    list_editable = ['status', 'priority']
    filter_horizontal = ['assigned_to']
    inlines = [EntityAttributeInline, EntityNoteInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'entity_type', 'description')
        }),
        ('Details', {
            'fields': ('industry', 'location', 'founded_date', 'website', 'domains', 'aliases'),
            'classes': ('collapse',)
        }),
        ('Social Media', {
            'fields': ('social_media',),
            'classes': ('collapse',)
        }),
        ('Research Settings', {
            'fields': ('priority', 'status', 'tags', 'assigned_to')
        }),
        ('Statistics', {
            'fields': ('search_count', 'results_found', 'last_researched'),
            'classes': ('collapse',)
        }),
        ('System', {
            'fields': ('id', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EntitySearchTemplate)
class EntitySearchTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'entity_type', 'category', 'risk_level', 'difficulty', 'usage_count', 'is_active']
    list_filter = ['entity_type', 'category', 'risk_level', 'difficulty', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'query_template']
    readonly_fields = ['created_at', 'updated_at', 'usage_count']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'entity_type', 'category', 'description')
        }),
        ('Query Configuration', {
            'fields': ('query_template', 'risk_level', 'difficulty')
        }),
        ('Status', {
            'fields': ('is_active', 'created_by')
        }),
        ('Statistics', {
            'fields': ('usage_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EntitySearchSession)
class EntitySearchSessionAdmin(admin.ModelAdmin):
    list_display = ['name', 'entity', 'total_searches', 'total_results', 'is_completed', 'created_by', 'created_at']
    list_filter = ['created_at', 'started_at', 'completed_at', 'entity__entity_type']
    search_fields = ['name', 'description', 'entity__name']
    readonly_fields = ['id', 'created_at', 'started_at', 'completed_at', 'total_searches', 'total_results']
    filter_horizontal = ['search_templates']

    def is_completed(self, obj):
        return obj.is_completed()
    is_completed.boolean = True
    is_completed.short_description = 'Completed'


@admin.register(EntitySearchResult)
class EntitySearchResultAdmin(admin.ModelAdmin):
    list_display = ['title_truncated', 'entity', 'template', 'relevance_score', 'is_interesting', 'is_verified', 'found_at']
    list_filter = ['is_interesting', 'is_verified', 'contains_sensitive_info', 'found_at', 'entity__entity_type']
    search_fields = ['title', 'url', 'snippet', 'entity__name']
    readonly_fields = ['id', 'found_at', 'domain']
    list_editable = ['is_interesting', 'is_verified']
    
    def title_truncated(self, obj):
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
    title_truncated.short_description = 'Title'


@admin.register(EntityRelationship)
class EntityRelationshipAdmin(admin.ModelAdmin):
    list_display = ['from_entity', 'relationship_type', 'to_entity', 'confidence', 'is_active', 'created_at']
    list_filter = ['relationship_type', 'confidence', 'is_active', 'created_at']
    search_fields = ['from_entity__name', 'to_entity__name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']


@admin.register(EntityNote)
class EntityNoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'entity', 'note_type', 'priority', 'is_private', 'created_by', 'created_at']
    list_filter = ['note_type', 'priority', 'is_private', 'created_at']
    search_fields = ['title', 'content', 'entity__name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(EntityAttribute)
class EntityAttributeAdmin(admin.ModelAdmin):
    list_display = ['entity', 'key', 'value_truncated', 'value_type', 'confidence', 'is_public']
    list_filter = ['value_type', 'confidence', 'is_public', 'created_at']
    search_fields = ['entity__name', 'key', 'value']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_public']

    def value_truncated(self, obj):
        return obj.value[:50] + '...' if len(obj.value) > 50 else obj.value
    value_truncated.short_description = 'Value'

from rest_framework import serializers
from .models import (
    GoogleDork, DorkCategory, SearchResult, SearchSession, 
    DorkBookmark, EntityType, Entity, EntityAttribute,
    EntitySearchTemplate, EntitySearchSession, EntitySearchResult,
    EntityRelationship, EntityNote
)
from accounts.serializers import UserSerializer


# ==============================================================================
# DORK SERIALIZERS
# ==============================================================================

class DorkCategorySerializer(serializers.ModelSerializer):
    """Serializer for Dork Category"""
    dork_count = serializers.SerializerMethodField()
    
    class Meta:
        model = DorkCategory
        fields = ['id', 'name', 'description', 'color', 'created_at', 'dork_count']
        read_only_fields = ['id', 'created_at']
    
    def get_dork_count(self, obj):
        return obj.dorks.count()


class GoogleDorkSerializer(serializers.ModelSerializer):
    """Serializer for Google Dork"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_data = DorkCategorySerializer(source='category', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    is_bookmarked = serializers.SerializerMethodField()
    execution_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = GoogleDork
        fields = [
            'id', 'title', 'description', 'query', 'category', 'category_name',
            'category_data', 'tags', 'risk_level', 'difficulty',
            'is_active', 'usage_count', 'execution_count',
            'created_by', 'created_by_username', 'created_at', 'updated_at',
            'is_bookmarked', 'supports_entities', 'entity_placeholders'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at', 'usage_count', 'execution_count']
    
    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return DorkBookmark.objects.filter(user=request.user, dork=obj).exists()
        return False
    
    def create(self, validated_data):
        # Set created_by from request user
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
        return super().create(validated_data)


class GoogleDorkListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for dork lists"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_bookmarked = serializers.SerializerMethodField()
    
    class Meta:
        model = GoogleDork
        fields = [
            'id', 'title', 'description', 'query', 'category_name',
            'risk_level', 'difficulty', 'is_active', 'is_bookmarked',
            'created_at', 'usage_count'
        ]
    
    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return DorkBookmark.objects.filter(user=request.user, dork=obj).exists()
        return False


class SearchSessionSerializer(serializers.ModelSerializer):
    """Serializer for Search Session"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    result_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SearchSession
        fields = [
            'id', 'user', 'user_username', 'name', 'description',
            'created_at', 'updated_at', 'is_active', 'result_count'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_result_count(self, obj):
        return obj.results.count()
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)


class SearchResultSerializer(serializers.ModelSerializer):
    """Serializer for Search Result"""
    dork_title = serializers.CharField(source='dork.title', read_only=True)
    dork_query = serializers.CharField(source='dork.query', read_only=True)
    session_name = serializers.CharField(source='session.name', read_only=True)
    
    class Meta:
        model = SearchResult
        fields = [
            'id', 'session', 'session_name', 'dork', 'dork_title', 'dork_query',
            'url', 'title', 'snippet', 'position', 'metadata', 'notes',
            'is_relevant', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class BookmarkSerializer(serializers.ModelSerializer):
    """Serializer for Bookmark"""
    dork_data = GoogleDorkListSerializer(source='dork', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = DorkBookmark
        fields = ['id', 'user', 'user_username', 'dork', 'dork_data', 
                  'notes', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)


# ==============================================================================
# ENTITY SERIALIZERS
# ==============================================================================

class EntityTypeSerializer(serializers.ModelSerializer):
    """Serializer for Entity Type"""
    entity_count = serializers.SerializerMethodField()
    
    class Meta:
        model = EntityType
        fields = ['id', 'name', 'display_name', 'description', 'icon', 'color',
                  'is_active', 'created_at', 'entity_count']
        read_only_fields = ['id', 'created_at']
    
    def get_entity_count(self, obj):
        return obj.entities.count()


class EntityAttributeSerializer(serializers.ModelSerializer):
    """Serializer for Entity Attribute"""
    
    class Meta:
        model = EntityAttribute
        fields = ['id', 'entity', 'key', 'value', 'value_type', 'source', 'confidence',
                  'is_public', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class EntitySerializer(serializers.ModelSerializer):
    """Serializer for Entity"""
    entity_type_name = serializers.CharField(source='entity_type.name', read_only=True)
    entity_type_data = EntityTypeSerializer(source='entity_type', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    attributes = EntityAttributeSerializer(many=True, read_only=True)
    attribute_count = serializers.SerializerMethodField()
    search_session_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Entity
        fields = [
            'id', 'name', 'entity_type', 'entity_type_name', 'entity_type_data',
            'description', 'aliases', 'industry', 'location', 'founded_date',
            'website', 'domains', 'social_media', 'tags', 'status', 'priority',
            'created_by', 'created_by_username', 'created_at', 'updated_at',
            'last_researched', 'search_count', 'results_found',
            'attributes', 'attribute_count', 'search_session_count'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at', 'search_count', 'results_found']
    
    def get_attribute_count(self, obj):
        return obj.attributes.count()
    
    def get_search_session_count(self, obj):
        return obj.search_sessions.count()
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
        return super().create(validated_data)


class EntityListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for entity lists"""
    entity_type_name = serializers.CharField(source='entity_type.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Entity
        fields = [
            'id', 'name', 'entity_type_name', 'description', 'status',
            'priority', 'created_by_username', 'created_at', 'updated_at'
        ]


class EntitySearchTemplateSerializer(serializers.ModelSerializer):
    """Serializer for Entity Search Template"""
    entity_type_name = serializers.CharField(source='entity_type.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    usage_count = serializers.SerializerMethodField()
    
    class Meta:
        model = EntitySearchTemplate
        fields = [
            'id', 'entity_type', 'entity_type_name', 'name', 'description',
            'template_query', 'example_query', 'parameters', 'category',
            'risk_level', 'is_active', 'created_by', 'created_by_username',
            'created_at', 'updated_at', 'usage_count'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def get_usage_count(self, obj):
        return obj.search_sessions.count()
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
        return super().create(validated_data)


class EntitySearchSessionSerializer(serializers.ModelSerializer):
    """Serializer for Entity Search Session"""
    entity_name = serializers.CharField(source='entity.name', read_only=True)
    template_name = serializers.CharField(source='search_template.name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    result_count = serializers.SerializerMethodField()
    
    class Meta:
        model = EntitySearchSession
        fields = [
            'id', 'entity', 'entity_name', 'search_template', 'template_name',
            'user', 'user_username', 'session_name', 'executed_query',
            'parameters_used', 'status', 'notes', 'started_at', 'completed_at',
            'result_count'
        ]
        read_only_fields = ['id', 'user', 'started_at', 'completed_at']
    
    def get_result_count(self, obj):
        return obj.results.count()
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)


class EntitySearchResultSerializer(serializers.ModelSerializer):
    """Serializer for Entity Search Result"""
    session_name = serializers.CharField(source='search_session.session_name', read_only=True)
    entity_name = serializers.CharField(source='search_session.entity.name', read_only=True)
    
    class Meta:
        model = EntitySearchResult
        fields = [
            'id', 'search_session', 'session_name', 'entity_name',
            'url', 'title', 'snippet', 'position', 'metadata',
            'relevance_score', 'is_verified', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class EntityRelationshipSerializer(serializers.ModelSerializer):
    """Serializer for Entity Relationship"""
    from_entity_name = serializers.CharField(source='from_entity.name', read_only=True)
    to_entity_name = serializers.CharField(source='to_entity.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = EntityRelationship
        fields = [
            'id', 'from_entity', 'from_entity_name', 'to_entity', 'to_entity_name',
            'relationship_type', 'description', 'confidence', 'source',
            'start_date', 'end_date', 'is_active',
            'created_by', 'created_by_username', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
        return super().create(validated_data)


class EntityNoteSerializer(serializers.ModelSerializer):
    """Serializer for Entity Note"""
    entity_name = serializers.CharField(source='entity.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = EntityNote
        fields = [
            'id', 'entity', 'entity_name', 'title', 'content', 'note_type',
            'tags', 'is_important', 'created_by', 'created_by_username',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
        return super().create(validated_data)

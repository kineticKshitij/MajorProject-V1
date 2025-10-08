from rest_framework import viewsets, status, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q, Count
from django.core.exceptions import ObjectDoesNotExist
import logging

from .models import (
    GoogleDork, DorkCategory, SearchResult, SearchSession,
    DorkBookmark, EntityType, Entity, EntityAttribute,
    EntitySearchTemplate, EntitySearchSession, EntitySearchResult,
    EntityRelationship, EntityNote
)
from .serializers import (
    GoogleDorkSerializer, GoogleDorkListSerializer, DorkCategorySerializer,
    SearchResultSerializer, SearchSessionSerializer, BookmarkSerializer,
    EntityTypeSerializer, EntitySerializer, EntityListSerializer,
    EntityAttributeSerializer, EntitySearchTemplateSerializer,
    EntitySearchSessionSerializer, EntitySearchResultSerializer,
    EntityRelationshipSerializer, EntityNoteSerializer
)
from .error_handling import (
    APIErrorResponse, safe_api_call, DorkExecutionException,
    ERROR_MESSAGES
)

logger = logging.getLogger(__name__)


# ==============================================================================
# DORK API VIEWSETS
# ==============================================================================

class DorkCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing dork categories
    
    list: Get all categories
    retrieve: Get a specific category
    create: Create a new category (admin only)
    update: Update a category (admin only)
    destroy: Delete a category (admin only)
    """
    queryset = DorkCategory.objects.all()
    serializer_class = DorkCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_permissions(self):
        # Only admins can create, update, or delete categories
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()
    
    @action(detail=True, methods=['get'])
    def dorks(self, request, pk=None):
        """Get all dorks in this category"""
        category = self.get_object()
        dorks = category.dorks.filter(is_active=True)
        serializer = GoogleDorkListSerializer(dorks, many=True, context={'request': request})
        return Response(serializer.data)


class GoogleDorkViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Google dorks
    
    list: Get all dorks with filtering
    retrieve: Get a specific dork
    create: Create a new dork
    update: Update a dork
    destroy: Delete a dork
    execute: Execute a dork query
    bookmark: Toggle bookmark for a dork
    """
    queryset = GoogleDork.objects.select_related('category', 'created_by').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'risk_level', 'difficulty_level', 'is_active']
    search_fields = ['title', 'description', 'query', 'tags']
    ordering_fields = ['title', 'created_at', 'execution_count']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return GoogleDorkListSerializer
        return GoogleDorkSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by user's bookmarks
        if self.request.query_params.get('bookmarked') == 'true':
            if self.request.user.is_authenticated:
                queryset = queryset.filter(bookmarks__user=self.request.user)
        
        # Filter by created_by
        if self.request.query_params.get('my_dorks') == 'true':
            if self.request.user.is_authenticated:
                queryset = queryset.filter(created_by=self.request.user)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        """Execute a dork query"""
        try:
            dork = self.get_object()
            
            # Increment execution count
            dork.execution_count = (dork.execution_count or 0) + 1
            dork.save()
            
            # Build search URL
            search_url = f"https://www.google.com/search?q={dork.query}"
            
            logger.info(f"Dork executed: {dork.title} (ID: {dork.id}) by user {request.user.username}")
            
            return Response({
                'success': True,
                'dork': GoogleDorkSerializer(dork, context={'request': request}).data,
                'search_url': search_url,
                'message': f'Dork "{dork.title}" executed successfully'
            })
        
        except ObjectDoesNotExist:
            logger.warning(f"Attempted to execute non-existent dork with ID: {pk}")
            return APIErrorResponse.not_found(ERROR_MESSAGES['DORK_NOT_FOUND'])
        
        except Exception as e:
            logger.error(f"Error executing dork {pk}: {str(e)}", exc_info=True)
            return APIErrorResponse.server_error(
                message=ERROR_MESSAGES['EXECUTION_FAILED'],
                details=str(e) if request.user.is_staff else None
            )
    
    @action(detail=True, methods=['post'])
    def bookmark(self, request, pk=None):
        """Toggle bookmark for a dork"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        dork = self.get_object()
        bookmark, created = DorkBookmark.objects.get_or_create(
            user=request.user,
            dork=dork
        )
        
        if not created:
            bookmark.delete()
            return Response({
                'success': True,
                'bookmarked': False,
                'message': 'Bookmark removed'
            })
        
        return Response({
            'success': True,
            'bookmarked': True,
            'message': 'Dork bookmarked successfully',
            'bookmark': BookmarkSerializer(bookmark, context={'request': request}).data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get dork statistics"""
        total_dorks = GoogleDork.objects.count()
        active_dorks = GoogleDork.objects.filter(is_active=True).count()
        categories = DorkCategory.objects.count()
        
        risk_distribution = GoogleDork.objects.values('risk_level').annotate(
            count=Count('id')
        )
        
        difficulty_distribution = GoogleDork.objects.values('difficulty_level').annotate(
            count=Count('id')
        )
        
        return Response({
            'total_dorks': total_dorks,
            'active_dorks': active_dorks,
            'inactive_dorks': total_dorks - active_dorks,
            'total_categories': categories,
            'risk_distribution': list(risk_distribution),
            'difficulty_distribution': list(difficulty_distribution),
        })


class SearchSessionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing search sessions
    
    list: Get all user's search sessions
    retrieve: Get a specific session
    create: Create a new session
    update: Update a session
    destroy: Delete a session
    """
    serializer_class = SearchSessionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-updated_at']
    
    def get_queryset(self):
        # Users can only see their own sessions
        return SearchSession.objects.filter(
            user=self.request.user,
            is_active=True
        ).select_related('user')
    
    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """Get all results for this session"""
        session = self.get_object()
        results = session.results.select_related('dork').all()
        serializer = SearchResultSerializer(results, many=True, context={'request': request})
        return Response(serializer.data)


class SearchResultViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing search results
    
    list: Get all user's search results
    retrieve: Get a specific result
    create: Create a new result
    update: Update a result
    destroy: Delete a result
    """
    serializer_class = SearchResultSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['session', 'dork', 'is_relevant']
    search_fields = ['title', 'url', 'snippet']
    ordering_fields = ['created_at', 'position']
    ordering = ['position']
    
    def get_queryset(self):
        # Users can only see results from their own sessions
        return SearchResult.objects.filter(
            session__user=self.request.user
        ).select_related('session', 'dork')


class BookmarkViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing bookmarks
    
    list: Get all user's bookmarks
    retrieve: Get a specific bookmark
    create: Create a new bookmark
    update: Update bookmark notes
    destroy: Remove a bookmark
    """
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['dork__title', 'notes']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        # Users can only see their own bookmarks
        return DorkBookmark.objects.filter(
            user=self.request.user
        ).select_related('user', 'dork', 'dork__category')


# ==============================================================================
# ENTITY API VIEWSETS
# ==============================================================================

class EntityTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing entity types
    
    list: Get all entity types
    retrieve: Get a specific entity type
    create: Create a new entity type (admin only)
    update: Update an entity type (admin only)
    destroy: Delete an entity type (admin only)
    """
    queryset = EntityType.objects.all()
    serializer_class = EntityTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()
    
    @action(detail=True, methods=['get'])
    def entities(self, request, pk=None):
        """Get all entities of this type"""
        entity_type = self.get_object()
        entities = entity_type.entities.filter(created_by=request.user) if request.user.is_authenticated else []
        serializer = EntityListSerializer(entities, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def templates(self, request, pk=None):
        """Get all search templates for this entity type"""
        entity_type = self.get_object()
        templates = entity_type.search_templates.filter(is_active=True)
        serializer = EntitySearchTemplateSerializer(templates, many=True, context={'request': request})
        return Response(serializer.data)


class EntityViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing entities
    
    list: Get all user's entities
    retrieve: Get a specific entity
    create: Create a new entity
    update: Update an entity
    destroy: Delete an entity
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['entity_type', 'status', 'priority']
    search_fields = ['name', 'description', 'tags']
    ordering_fields = ['name', 'created_at', 'updated_at', 'priority']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return EntityListSerializer
        return EntitySerializer
    
    def get_queryset(self):
        # Users can only see their own entities
        return Entity.objects.filter(
            created_by=self.request.user
        ).select_related('entity_type', 'created_by').prefetch_related('attributes')
    
    @action(detail=True, methods=['get', 'post'])
    def attributes(self, request, pk=None):
        """Get or add attributes for this entity"""
        entity = self.get_object()
        
        if request.method == 'POST':
            serializer = EntityAttributeSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(entity=entity)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        attributes = entity.attributes.all()
        serializer = EntityAttributeSerializer(attributes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def search_sessions(self, request, pk=None):
        """Get all search sessions for this entity"""
        entity = self.get_object()
        sessions = entity.search_sessions.select_related('search_template', 'user').all()
        serializer = EntitySearchSessionSerializer(sessions, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def relationships(self, request, pk=None):
        """Get all relationships for this entity"""
        entity = self.get_object()
        outgoing = EntityRelationship.objects.filter(from_entity=entity)
        incoming = EntityRelationship.objects.filter(to_entity=entity)
        
        return Response({
            'outgoing': EntityRelationshipSerializer(outgoing, many=True, context={'request': request}).data,
            'incoming': EntityRelationshipSerializer(incoming, many=True, context={'request': request}).data,
        })
    
    @action(detail=True, methods=['get'])
    def notes(self, request, pk=None):
        """Get all notes for this entity"""
        entity = self.get_object()
        notes = entity.notes.select_related('created_by').all()
        serializer = EntityNoteSerializer(notes, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get entity statistics for the current user"""
        total_entities = Entity.objects.filter(created_by=request.user).count()
        
        status_distribution = Entity.objects.filter(
            created_by=request.user
        ).values('status').annotate(count=Count('id'))
        
        type_distribution = Entity.objects.filter(
            created_by=request.user
        ).values('entity_type__name').annotate(count=Count('id'))
        
        return Response({
            'total_entities': total_entities,
            'status_distribution': list(status_distribution),
            'type_distribution': list(type_distribution),
        })


class EntitySearchTemplateViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing entity search templates
    """
    queryset = EntitySearchTemplate.objects.filter(is_active=True)
    serializer_class = EntitySearchTemplateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['entity_type', 'category', 'risk_level']
    search_fields = ['name', 'description', 'template_query']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()


class EntitySearchSessionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing entity search sessions
    """
    serializer_class = EntitySearchSessionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['entity', 'search_template', 'status']
    search_fields = ['session_name', 'executed_query']
    ordering_fields = ['started_at', 'completed_at']
    ordering = ['-started_at']
    
    def get_queryset(self):
        return EntitySearchSession.objects.filter(
            user=self.request.user
        ).select_related('entity', 'search_template', 'user')
    
    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """Get all results for this session"""
        session = self.get_object()
        results = session.results.all()
        serializer = EntitySearchResultSerializer(results, many=True, context={'request': request})
        return Response(serializer.data)


class EntitySearchResultViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing entity search results
    """
    serializer_class = EntitySearchResultSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['search_session', 'is_verified']
    search_fields = ['title', 'url', 'snippet']
    ordering_fields = ['created_at', 'position', 'relevance_score']
    ordering = ['position']
    
    def get_queryset(self):
        return EntitySearchResult.objects.filter(
            search_session__user=self.request.user
        ).select_related('search_session', 'search_session__entity')


class EntityRelationshipViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing entity relationships
    """
    serializer_class = EntityRelationshipSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['from_entity', 'to_entity', 'relationship_type', 'is_verified']
    search_fields = ['description']
    ordering_fields = ['created_at', 'strength']
    ordering = ['-created_at']
    
    def get_queryset(self):
        # Users can only see relationships involving their entities
        return EntityRelationship.objects.filter(
            Q(from_entity__created_by=self.request.user) |
            Q(to_entity__created_by=self.request.user)
        ).select_related('from_entity', 'to_entity', 'created_by')


class EntityNoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing entity notes
    """
    serializer_class = EntityNoteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['entity', 'note_type', 'is_important']
    search_fields = ['title', 'content', 'tags']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return EntityNote.objects.filter(
            entity__created_by=self.request.user
        ).select_related('entity', 'created_by')


# ==============================================================================
# DATA BREACH CHECKER API
# ==============================================================================

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .integrations.breach_checker import HaveIBeenPwnedClient
from .error_handling import BreachCheckerException
from django.conf import settings
import re


@api_view(['POST'])
@permission_classes([AllowAny])  # Allow public access for demo
def check_email_breach(request):
    """
    Check if an email has been compromised in data breaches.
    
    POST /api/check-breach/
    Body: {"email": "test@example.com"}
    
    Returns:
        - status: 'found', 'safe', or 'error'
        - breach_count: Number of breaches found
        - breaches: List of breach details
        - message: Human-readable message
    """
    try:
        email = request.data.get('email')
        
        if not email:
            logger.warning("Breach check attempted without email")
            return APIErrorResponse.bad_request(
                message='Email address is required',
                details={'field': 'email', 'error': 'This field is required'}
            )
        
        # Validate email format
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            logger.warning(f"Invalid email format: {email}")
            return APIErrorResponse.bad_request(
                message='Invalid email address format',
                details={'field': 'email', 'error': 'Please provide a valid email address'}
            )
        
        # Get API keys and configuration from settings
        api_key = getattr(settings, 'HIBP_API_KEY', None)
        rapidapi_key = getattr(settings, 'RAPIDAPI_KEY', None)
        use_real_api = getattr(settings, 'USE_REAL_BREACH_API', False)
        
        # Check breaches using configured API
        try:
            client = HaveIBeenPwnedClient(
                api_key=api_key,
                demo_mode=not use_real_api,
                use_breach_directory=use_real_api,
                rapidapi_key=rapidapi_key
            )
            result = client.check_email_breaches(email)
            
            logger.info(f"Breach check completed for email: {email[:3]}***")
            
            # Return the result
            return Response(result)
        
        except Exception as api_error:
            logger.error(f"Breach check API error: {str(api_error)}", exc_info=True)
            return APIErrorResponse.server_error(
                message='Failed to check email breaches',
                details=str(api_error) if settings.DEBUG else None
            )
    
    except Exception as e:
        logger.error(f"Unexpected error in breach check: {str(e)}", exc_info=True)
        return APIErrorResponse.server_error(
            message='An unexpected error occurred',
            details=str(e) if settings.DEBUG else None
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def check_password_breach(request):
    """
    Check if a password has been seen in data breaches.
    Uses k-anonymity method - only first 5 chars of hash are sent.
    
    POST /api/check-password/
    Body: {"password": "mypassword123"}
    
    Returns:
        - status: 'found', 'safe', or 'error'
        - times_seen: Number of times password seen in breaches
        - message: Human-readable message
        - recommendation: Security recommendation
    """
    try:
        password = request.data.get('password')
        
        if not password:
            logger.warning("Password check attempted without password")
            return APIErrorResponse.bad_request(
                message='Password is required',
                details={'field': 'password', 'error': 'This field is required'}
            )
        
        # Validate password length
        if len(password) < 1:
            return APIErrorResponse.bad_request(
                message='Password cannot be empty',
                details={'field': 'password', 'error': 'Password must be at least 1 character'}
            )
        
        # Check password using k-anonymity method (secure)
        try:
            client = HaveIBeenPwnedClient()
            result = client.check_password_hash(password)
            
            logger.info("Password breach check completed (k-anonymity)")
            
            return Response(result)
        
        except Exception as api_error:
            logger.error(f"Password check API error: {str(api_error)}", exc_info=True)
            return APIErrorResponse.server_error(
                message='Failed to check password',
                details=str(api_error) if settings.DEBUG else None
            )
    
    except Exception as e:
        logger.error(f"Unexpected error in password check: {str(e)}", exc_info=True)
        return APIErrorResponse.server_error(
            message='An unexpected error occurred',
            details=str(e) if settings.DEBUG else None
        )

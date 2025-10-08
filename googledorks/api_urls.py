from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

app_name = 'googledorks_api'

# Create a router and register our viewsets
router = DefaultRouter()

# Dork management
router.register(r'categories', api_views.DorkCategoryViewSet, basename='category')
router.register(r'dorks', api_views.GoogleDorkViewSet, basename='dork')
router.register(r'search-sessions', api_views.SearchSessionViewSet, basename='search-session')
router.register(r'search-results', api_views.SearchResultViewSet, basename='search-result')
router.register(r'bookmarks', api_views.BookmarkViewSet, basename='bookmark')

# Entity management
router.register(r'entity-types', api_views.EntityTypeViewSet, basename='entity-type')
router.register(r'entities', api_views.EntityViewSet, basename='entity')
router.register(r'entity-templates', api_views.EntitySearchTemplateViewSet, basename='entity-template')
router.register(r'entity-sessions', api_views.EntitySearchSessionViewSet, basename='entity-session')
router.register(r'entity-results', api_views.EntitySearchResultViewSet, basename='entity-result')
router.register(r'entity-relationships', api_views.EntityRelationshipViewSet, basename='entity-relationship')
router.register(r'entity-notes', api_views.EntityNoteViewSet, basename='entity-note')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    
    # Data Breach Checker endpoints (non-REST, simple function views)
    path('check-breach/', api_views.check_email_breach, name='check-breach'),
    path('check-password/', api_views.check_password_breach, name='check-password'),
]

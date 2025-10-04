from django.urls import path
from . import views
from . import views_entity

app_name = 'googledorks'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('dorks/', views.dork_list, name='dork_list'),
    path('dorks/<int:pk>/', views.dork_detail, name='dork_detail'),
    path('<int:pk>/execute/', views.execute_dork, name='execute_dork'),
    path('<int:pk>/bookmark/', views.bookmark_dork, name='bookmark_dork'),
    
    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    
    # Search results
    path('results/', views.search_results, name='search_results'),
    
    # User features
    path('bookmarks/', views.my_bookmarks, name='my_bookmarks'),
    
    # Search sessions
    path('sessions/create/', views.create_session, name='create_session'),
    path('sessions/<int:pk>/', views.session_detail, name='session_detail'),
    
    # Entity Management
    path('entities/', views_entity.entity_dashboard, name='entity_dashboard'),
    path('entities/list/', views_entity.entity_list, name='entity_list'),
    path('entities/create/', views_entity.entity_create, name='entity_create'),
    path('entities/quick-create/', views_entity.entity_quick_create, name='entity_quick_create'),
    path('entities/bulk-import/', views_entity.entity_bulk_import, name='entity_bulk_import'),
    path('entities/export/', views_entity.entity_export_csv, name='entity_export_csv'),
    path('entities/analytics/', views_entity.entity_analytics, name='entity_analytics'),
    path('entities/templates/', views_entity.entity_templates, name='entity_templates'),
    
    # Individual Entity Management
    path('entities/<uuid:pk>/', views_entity.entity_detail, name='entity_detail'),
    path('entities/<uuid:pk>/edit/', views_entity.entity_edit, name='entity_edit'),
    path('entities/<uuid:pk>/delete/', views_entity.entity_delete, name='entity_delete'),
    path('entities/<uuid:pk>/add-note/', views_entity.entity_add_note, name='entity_add_note'),
    path('entities/<uuid:pk>/add-attribute/', views_entity.entity_add_attribute, name='entity_add_attribute'),
    
    # Entity Search Sessions
    path('entities/<uuid:entity_pk>/sessions/create/', views_entity.entity_search_session_create, name='entity_session_create'),
    path('entity-sessions/<uuid:pk>/', views_entity.entity_search_session_detail, name='entity_session_detail'),
    
    # Entity Search Templates
    path('entities/<uuid:entity_pk>/templates/<int:template_pk>/execute/', views_entity.entity_execute_template, name='entity_execute_template'),
]
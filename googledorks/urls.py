from django.urls import path
from . import views

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
]
from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    # Main chat interface
    path('', views.chatbot_home, name='home'),
    
    # API endpoints
    path('api/start-session/', views.start_new_session, name='start_session'),
    path('api/send-message/', views.send_message, name='send_message'),
    path('api/session/<uuid:session_id>/messages/', views.get_session_messages, name='session_messages'),
    path('api/feedback/', views.submit_feedback, name='submit_feedback'),
    path('api/session/<uuid:session_id>/delete/', views.delete_session, name='delete_session'),
    
    # User interface
    path('sessions/', views.user_sessions, name='user_sessions'),
    path('stats/', views.chatbot_stats, name='stats'),
]
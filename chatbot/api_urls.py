from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

app_name = 'chatbot_api'

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'sessions', api_views.ChatSessionViewSet, basename='session')
router.register(r'messages', api_views.ChatMessageViewSet, basename='message')
router.register(r'feedback', api_views.ChatFeedbackViewSet, basename='feedback')

urlpatterns = [
    # Router URLs
    path('', include(router.urls)),
    
    # Custom endpoints
    path('send-message/', api_views.send_message, name='send-message'),
    path('start-session/', api_views.start_session, name='start-session'),
    path('statistics/', api_views.statistics, name='statistics'),
    path('check-configuration/', api_views.check_configuration, name='check-configuration'),
]

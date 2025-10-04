from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    CrawlJobViewSet, SocialProfileViewSet, SocialPostViewSet,
    SocialMetricsViewSet, CrawlScheduleViewSet
)

app_name = 'socialcrawler'

router = DefaultRouter()
router.register('jobs', CrawlJobViewSet, basename='crawljob')
router.register('profiles', SocialProfileViewSet, basename='profile')
router.register('posts', SocialPostViewSet, basename='post')
router.register('metrics', SocialMetricsViewSet, basename='metrics')
router.register('schedules', CrawlScheduleViewSet, basename='schedule')

urlpatterns = [
    path('', include(router.urls)),
]

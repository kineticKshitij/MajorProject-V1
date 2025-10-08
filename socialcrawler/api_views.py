from rest_framework import viewsets, status, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Q, Sum
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
import asyncio
import logging

from .models import (
    CrawlJob, SocialProfile, SocialPost,
    SocialMetrics, CrawlSchedule, CrawlStatus
)
from .serializers import (
    CrawlJobSerializer, CrawlJobListSerializer, CreateCrawlJobSerializer,
    SocialProfileSerializer, SocialProfileListSerializer,
    SocialPostSerializer, SocialMetricsSerializer,
    CrawlScheduleSerializer, PostAnalyticsSerializer,
    ProfileAnalyticsSerializer
)
from .services import CrawlerFactory
from googledorks.error_handling import (
    APIErrorResponse, CrawlerException, ERROR_MESSAGES
)

logger = logging.getLogger(__name__)


class CrawlJobViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing social media crawl jobs
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['target_username', 'platform']
    ordering_fields = ['created_at', 'completed_at', 'status']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateCrawlJobSerializer
        elif self.action == 'list':
            return CrawlJobListSerializer
        return CrawlJobSerializer
    
    def get_queryset(self):
        """Users can only see their own crawl jobs"""
        queryset = CrawlJob.objects.filter(user=self.request.user)
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by platform
        platform = self.request.query_params.get('platform', None)
        if platform:
            queryset = queryset.filter(platform=platform)
        
        # Filter by entity
        entity_id = self.request.query_params.get('entity', None)
        if entity_id:
            queryset = queryset.filter(entity_id=entity_id)
        
        return queryset.prefetch_related('profiles', 'posts')
    
    def perform_create(self, serializer):
        """Create and start a crawl job"""
        crawl_job = serializer.save(user=self.request.user)
        
        # Start crawling asynchronously
        self._start_crawl(crawl_job)
    
    def _start_crawl(self, crawl_job):
        """Start the crawling process"""
        try:
            # Update status
            crawl_job.status = CrawlStatus.IN_PROGRESS
            crawl_job.started_at = timezone.now()
            crawl_job.save()
            
            # Create crawler
            crawler = CrawlerFactory.create_crawler(
                platform=crawl_job.platform,
                username=crawl_job.target_username,
                max_posts=crawl_job.max_posts
            )
            
            # Run crawling in async
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                # Crawl profile
                crawl_job.progress = 25
                crawl_job.save()
                
                profile_data = loop.run_until_complete(crawler.crawl_profile())
                
                if profile_data:
                    # Create profile
                    profile = SocialProfile.objects.create(
                        crawl_job=crawl_job,
                        entity=crawl_job.entity,
                        **profile_data
                    )
                    crawl_job.profiles_found += 1
                    crawl_job.progress = 50
                    crawl_job.save()
                    
                    # Crawl posts if requested
                    if crawl_job.crawl_posts:
                        posts_data = loop.run_until_complete(crawler.crawl_posts())
                        
                        for post_data in posts_data:
                            SocialPost.objects.create(
                                profile=profile,
                                crawl_job=crawl_job,
                                **post_data
                            )
                            crawl_job.posts_found += 1
                        
                        crawl_job.progress = 100
                    else:
                        crawl_job.progress = 100
                    
                    crawl_job.status = CrawlStatus.COMPLETED
                else:
                    crawl_job.status = CrawlStatus.FAILED
                    crawl_job.error_message = "Failed to crawl profile"
                
            finally:
                loop.close()
                crawler.close()
            
            crawl_job.completed_at = timezone.now()
            crawl_job.save()
            
        except Exception as e:
            logger.error(f"Error in crawl job {crawl_job.id}: {str(e)}")
            crawl_job.status = CrawlStatus.FAILED
            crawl_job.error_message = str(e)
            crawl_job.completed_at = timezone.now()
            crawl_job.save()
    
    @action(detail=True, methods=['post'])
    def restart(self, request, pk=None):
        """Restart a failed or cancelled crawl job"""
        try:
            crawl_job = self.get_object()
            
            if crawl_job.status not in [CrawlStatus.FAILED, CrawlStatus.CANCELLED]:
                logger.warning(f"Attempted to restart job {pk} with status {crawl_job.status}")
                return APIErrorResponse.bad_request(
                    message='Can only restart failed or cancelled jobs',
                    details={'current_status': crawl_job.status}
                )
            
            # Reset job
            crawl_job.status = CrawlStatus.PENDING
            crawl_job.progress = 0
            crawl_job.error_message = ''
            crawl_job.profiles_found = 0
            crawl_job.posts_found = 0
            crawl_job.save()
            
            logger.info(f"Restarting crawl job {pk} by user {request.user.username}")
            
            # Start crawling
            self._start_crawl(crawl_job)
            
            return Response(CrawlJobSerializer(crawl_job).data)
        
        except ObjectDoesNotExist:
            logger.warning(f"Attempted to restart non-existent job {pk}")
            return APIErrorResponse.not_found(ERROR_MESSAGES['JOB_NOT_FOUND'])
        
        except Exception as e:
            logger.error(f"Error restarting job {pk}: {str(e)}", exc_info=True)
            return APIErrorResponse.server_error(
                message=ERROR_MESSAGES['CRAWLER_ERROR'],
                details=str(e) if request.user.is_staff else None
            )
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a running crawl job"""
        try:
            crawl_job = self.get_object()
            
            if crawl_job.status != CrawlStatus.IN_PROGRESS:
                logger.warning(f"Attempted to cancel job {pk} with status {crawl_job.status}")
                return APIErrorResponse.bad_request(
                    message='Can only cancel jobs in progress',
                    details={'current_status': crawl_job.status}
                )
            
            crawl_job.status = CrawlStatus.CANCELLED
            crawl_job.completed_at = timezone.now()
            crawl_job.save()
            
            logger.info(f"Cancelled crawl job {pk} by user {request.user.username}")
            
            return Response(CrawlJobSerializer(crawl_job).data)
        
        except ObjectDoesNotExist:
            logger.warning(f"Attempted to cancel non-existent job {pk}")
            return APIErrorResponse.not_found(ERROR_MESSAGES['JOB_NOT_FOUND'])
        
        except Exception as e:
            logger.error(f"Error cancelling job {pk}: {str(e)}", exc_info=True)
            return APIErrorResponse.server_error(
                message=ERROR_MESSAGES['CRAWLER_ERROR'],
                details=str(e) if request.user.is_staff else None
            )
    
    @action(detail=False, methods=['get'])
    def supported_platforms(self, request):
        """Get list of supported platforms"""
        platforms = CrawlerFactory.get_supported_platforms()
        return Response({'platforms': platforms})
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get user's crawl statistics"""
        user_jobs = self.get_queryset()
        
        stats = {
            'total_jobs': user_jobs.count(),
            'completed_jobs': user_jobs.filter(status=CrawlStatus.COMPLETED).count(),
            'failed_jobs': user_jobs.filter(status=CrawlStatus.FAILED).count(),
            'in_progress_jobs': user_jobs.filter(status=CrawlStatus.IN_PROGRESS).count(),
            'total_profiles': user_jobs.aggregate(total=Sum('profiles_found'))['total'] or 0,
            'total_posts': user_jobs.aggregate(total=Sum('posts_found'))['total'] or 0,
            'platforms': list(user_jobs.values('platform').annotate(count=Count('id'))),
        }
        
        return Response(stats)


class SocialProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing social media profiles
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'display_name', 'bio']
    ordering_fields = ['crawled_at', 'followers_count', 'posts_count']
    ordering = ['-crawled_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return SocialProfileListSerializer
        return SocialProfileSerializer
    
    def get_queryset(self):
        """Get profiles from user's crawl jobs"""
        queryset = SocialProfile.objects.filter(crawl_job__user=self.request.user)
        
        # Filter by platform
        platform = self.request.query_params.get('platform', None)
        if platform:
            queryset = queryset.filter(platform=platform)
        
        # Filter by entity
        entity_id = self.request.query_params.get('entity', None)
        if entity_id:
            queryset = queryset.filter(entity_id=entity_id)
        
        # Filter by verified
        verified = self.request.query_params.get('verified', None)
        if verified is not None:
            queryset = queryset.filter(verified=verified.lower() == 'true')
        
        return queryset.select_related('entity', 'crawl_job')
    
    @action(detail=True, methods=['get'])
    def analytics(self, request, pk=None):
        """Get analytics for a specific profile"""
        profile = self.get_object()
        
        posts = profile.posts.all()
        
        analytics = {
            'total_posts': posts.count(),
            'total_likes': posts.aggregate(total=Sum('likes_count'))['total'] or 0,
            'total_comments': posts.aggregate(total=Sum('comments_count'))['total'] or 0,
            'total_shares': posts.aggregate(total=Sum('shares_count'))['total'] or 0,
            'avg_likes': posts.aggregate(avg=Avg('likes_count'))['avg'] or 0,
            'avg_comments': posts.aggregate(avg=Avg('comments_count'))['avg'] or 0,
            'avg_shares': posts.aggregate(avg=Avg('shares_count'))['avg'] or 0,
            'engagement_rate': 0,  # Calculate based on followers
        }
        
        # Calculate engagement rate
        if profile.followers_count > 0 and posts.count() > 0:
            total_engagement = analytics['total_likes'] + analytics['total_comments'] + analytics['total_shares']
            analytics['engagement_rate'] = (total_engagement / (profile.followers_count * posts.count())) * 100
        
        return Response(PostAnalyticsSerializer(analytics).data)


class SocialPostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing social media posts
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SocialPostSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content', 'hashtags', 'mentions']
    ordering_fields = ['posted_at', 'likes_count', 'comments_count', 'shares_count']
    ordering = ['-posted_at']
    
    def get_queryset(self):
        """Get posts from user's crawl jobs"""
        queryset = SocialPost.objects.filter(crawl_job__user=self.request.user)
        
        # Filter by profile
        profile_id = self.request.query_params.get('profile', None)
        if profile_id:
            queryset = queryset.filter(profile_id=profile_id)
        
        # Filter by platform
        platform = self.request.query_params.get('platform', None)
        if platform:
            queryset = queryset.filter(profile__platform=platform)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(posted_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(posted_at__lte=end_date)
        
        # Filter by sentiment
        sentiment = self.request.query_params.get('sentiment', None)
        if sentiment:
            queryset = queryset.filter(sentiment=sentiment)
        
        return queryset.select_related('profile', 'crawl_job')


class SocialMetricsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing social media metrics
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SocialMetricsSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date', 'followers_count', 'engagement_rate']
    ordering = ['-date']
    
    def get_queryset(self):
        """Get metrics for user's profiles"""
        queryset = SocialMetrics.objects.filter(profile__crawl_job__user=self.request.user)
        
        # Filter by profile
        profile_id = self.request.query_params.get('profile', None)
        if profile_id:
            queryset = queryset.filter(profile_id=profile_id)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset.select_related('profile')


class CrawlScheduleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing crawl schedules
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CrawlScheduleSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'target_username']
    ordering_fields = ['created_at', 'next_run']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Get user's schedules"""
        queryset = CrawlSchedule.objects.filter(user=self.request.user)
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Filter by platform
        platform = self.request.query_params.get('platform', None)
        if platform:
            queryset = queryset.filter(platform=platform)
        
        return queryset.select_related('entity')
    
    def perform_create(self, serializer):
        """Create schedule"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Toggle schedule active status"""
        schedule = self.get_object()
        schedule.is_active = not schedule.is_active
        schedule.save()
        
        return Response(CrawlScheduleSerializer(schedule).data)

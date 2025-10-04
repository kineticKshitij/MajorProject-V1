"""
Social Media Crawler Service
Handles crawling logic for different social media platforms
"""

import logging
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from django.utils import timezone
import requests
from bs4 import BeautifulSoup
import json

logger = logging.getLogger(__name__)


class BaseCrawler:
    """Base class for social media crawlers"""
    
    def __init__(self, username: str, max_posts: int = 100):
        self.username = username
        self.max_posts = max_posts
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    async def crawl_profile(self) -> Optional[Dict[str, Any]]:
        """Crawl profile information - to be implemented by subclasses"""
        raise NotImplementedError
    
    async def crawl_posts(self) -> List[Dict[str, Any]]:
        """Crawl posts - to be implemented by subclasses"""
        raise NotImplementedError
    
    def close(self):
        """Close the session"""
        self.session.close()


class TwitterCrawler(BaseCrawler):
    """
    Twitter/X Crawler
    Note: This is a basic implementation. For production use, consider using:
    - Twitter API v2 (requires API key)
    - snscrape library
    - nitter instances
    """
    
    def __init__(self, username: str, max_posts: int = 100, api_key: str = None):
        super().__init__(username, max_posts)
        self.api_key = api_key
        self.base_url = "https://twitter.com"
    
    async def crawl_profile(self) -> Optional[Dict[str, Any]]:
        """Crawl Twitter profile"""
        try:
            # This is a placeholder - actual implementation would require:
            # 1. Twitter API credentials
            # 2. Or scraping via nitter/other alternatives
            # 3. Or using libraries like snscrape
            
            profile_data = {
                'username': self.username,
                'user_id': '',
                'display_name': '',
                'bio': '',
                'avatar_url': '',
                'banner_url': '',
                'followers_count': 0,
                'following_count': 0,
                'posts_count': 0,
                'verified': False,
                'location': '',
                'website': '',
                'joined_date': None,
                'profile_url': f"{self.base_url}/{self.username}",
                'raw_data': {}
            }
            
            logger.info(f"Crawled Twitter profile: @{self.username}")
            return profile_data
            
        except Exception as e:
            logger.error(f"Error crawling Twitter profile @{self.username}: {str(e)}")
            return None
    
    async def crawl_posts(self) -> List[Dict[str, Any]]:
        """Crawl Twitter posts"""
        posts = []
        try:
            # Placeholder implementation
            logger.info(f"Crawling Twitter posts for @{self.username}")
            
        except Exception as e:
            logger.error(f"Error crawling Twitter posts: {str(e)}")
        
        return posts


class GitHubCrawler(BaseCrawler):
    """
    GitHub Crawler - Uses public GitHub API
    No authentication required for public data
    """
    
    def __init__(self, username: str, max_repos: int = 100, api_token: str = None):
        super().__init__(username, max_repos)
        self.api_token = api_token
        self.base_url = "https://api.github.com"
        
        if api_token:
            self.session.headers.update({
                'Authorization': f'token {api_token}'
            })
    
    async def crawl_profile(self) -> Optional[Dict[str, Any]]:
        """Crawl GitHub profile"""
        try:
            url = f"{self.base_url}/users/{self.username}"
            response = self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            profile_data = {
                'username': data.get('login', ''),
                'user_id': str(data.get('id', '')),
                'display_name': data.get('name', ''),
                'bio': data.get('bio', ''),
                'avatar_url': data.get('avatar_url', ''),
                'banner_url': '',
                'followers_count': data.get('followers', 0),
                'following_count': data.get('following', 0),
                'posts_count': data.get('public_repos', 0),
                'verified': False,
                'location': data.get('location', ''),
                'website': data.get('blog', ''),
                'joined_date': data.get('created_at', '').split('T')[0] if data.get('created_at') else None,
                'profile_url': data.get('html_url', ''),
                'raw_data': data
            }
            
            logger.info(f"Crawled GitHub profile: @{self.username}")
            return profile_data
            
        except Exception as e:
            logger.error(f"Error crawling GitHub profile @{self.username}: {str(e)}")
            return None
    
    async def crawl_posts(self) -> List[Dict[str, Any]]:
        """Crawl GitHub repositories (as posts)"""
        posts = []
        try:
            url = f"{self.base_url}/users/{self.username}/repos"
            params = {'per_page': min(self.max_posts, 100), 'sort': 'updated'}
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            repos = response.json()
            
            for repo in repos[:self.max_posts]:
                post_data = {
                    'post_id': str(repo.get('id', '')),
                    'post_url': repo.get('html_url', ''),
                    'content': repo.get('description') or '',  # Ensure never None
                    'media_urls': [],
                    'media_type': 'repository',
                    'likes_count': repo.get('stargazers_count', 0),
                    'comments_count': repo.get('open_issues_count', 0),
                    'shares_count': repo.get('forks_count', 0),
                    'views_count': repo.get('watchers_count', 0),
                    'posted_at': repo.get('created_at', ''),
                    'language': repo.get('language') or '',  # Ensure never None
                    'hashtags': repo.get('topics', []),
                    'mentions': [],
                    'sentiment': 'neutral',
                    'topics': repo.get('topics', []),
                    'raw_data': repo
                }
                posts.append(post_data)
            
            logger.info(f"Crawled {len(posts)} GitHub repos for @{self.username}")
            
        except Exception as e:
            logger.error(f"Error crawling GitHub repos: {str(e)}")
        
        return posts


class LinkedInCrawler(BaseCrawler):
    """
    LinkedIn Crawler
    Note: LinkedIn heavily restricts scraping. Use their official API or
    consider alternatives like proxycurl.com
    """
    
    async def crawl_profile(self) -> Optional[Dict[str, Any]]:
        """Crawl LinkedIn profile"""
        try:
            # Placeholder - would require LinkedIn API credentials
            profile_data = {
                'username': self.username,
                'user_id': '',
                'display_name': '',
                'bio': '',
                'avatar_url': '',
                'banner_url': '',
                'followers_count': 0,
                'following_count': 0,
                'posts_count': 0,
                'verified': False,
                'location': '',
                'website': '',
                'joined_date': None,
                'profile_url': f"https://linkedin.com/in/{self.username}",
                'raw_data': {}
            }
            
            logger.info(f"Crawled LinkedIn profile: {self.username}")
            return profile_data
            
        except Exception as e:
            logger.error(f"Error crawling LinkedIn profile: {str(e)}")
            return None
    
    async def crawl_posts(self) -> List[Dict[str, Any]]:
        """Crawl LinkedIn posts"""
        return []


class RedditCrawler(BaseCrawler):
    """
    Reddit Crawler - Uses public Reddit API
    """
    
    def __init__(self, username: str, max_posts: int = 100):
        super().__init__(username, max_posts)
        self.base_url = "https://www.reddit.com"
    
    async def crawl_profile(self) -> Optional[Dict[str, Any]]:
        """Crawl Reddit profile"""
        try:
            url = f"{self.base_url}/user/{self.username}/about.json"
            response = self.session.get(url)
            response.raise_for_status()
            
            data = response.json()['data']
            
            profile_data = {
                'username': data.get('name', ''),
                'user_id': data.get('id', ''),
                'display_name': data.get('subreddit', {}).get('title', ''),
                'bio': data.get('subreddit', {}).get('public_description', ''),
                'avatar_url': data.get('icon_img', ''),
                'banner_url': data.get('subreddit', {}).get('banner_img', ''),
                'followers_count': 0,  # Reddit doesn't provide this easily
                'following_count': 0,
                'posts_count': data.get('link_karma', 0) + data.get('comment_karma', 0),
                'verified': data.get('verified', False),
                'location': '',
                'website': '',
                'joined_date': datetime.fromtimestamp(data.get('created', 0)).date().isoformat(),
                'profile_url': f"{self.base_url}/user/{self.username}",
                'raw_data': data
            }
            
            logger.info(f"Crawled Reddit profile: u/{self.username}")
            return profile_data
            
        except Exception as e:
            logger.error(f"Error crawling Reddit profile u/{self.username}: {str(e)}")
            return None
    
    async def crawl_posts(self) -> List[Dict[str, Any]]:
        """Crawl Reddit posts"""
        posts = []
        try:
            url = f"{self.base_url}/user/{self.username}/submitted.json"
            params = {'limit': min(self.max_posts, 100)}
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            for post in data['data']['children'][:self.max_posts]:
                post_data = post['data']
                posts.append({
                    'post_id': post_data.get('id', ''),
                    'post_url': f"{self.base_url}{post_data.get('permalink', '')}",
                    'content': post_data.get('selftext', '') or post_data.get('title', ''),
                    'media_urls': [post_data.get('url', '')] if post_data.get('url', '').startswith('http') else [],
                    'media_type': 'link' if post_data.get('is_self') == False else 'text',
                    'likes_count': post_data.get('ups', 0),
                    'comments_count': post_data.get('num_comments', 0),
                    'shares_count': 0,
                    'views_count': 0,
                    'posted_at': datetime.fromtimestamp(post_data.get('created_utc', 0)).isoformat(),
                    'language': '',
                    'hashtags': [],
                    'mentions': [],
                    'sentiment': 'neutral',
                    'topics': [],
                    'raw_data': post_data
                })
            
            logger.info(f"Crawled {len(posts)} Reddit posts for u/{self.username}")
            
        except Exception as e:
            logger.error(f"Error crawling Reddit posts: {str(e)}")
        
        return posts


class CrawlerFactory:
    """Factory to create appropriate crawler based on platform"""
    
    CRAWLERS = {
        'twitter': TwitterCrawler,
        'github': GitHubCrawler,
        'linkedin': LinkedInCrawler,
        'reddit': RedditCrawler,
    }
    
    @classmethod
    def create_crawler(cls, platform: str, username: str, max_posts: int = 100, **kwargs) -> BaseCrawler:
        """Create a crawler instance for the specified platform"""
        crawler_class = cls.CRAWLERS.get(platform.lower())
        
        if not crawler_class:
            raise ValueError(f"Unsupported platform: {platform}")
        
        return crawler_class(username, max_posts, **kwargs)
    
    @classmethod
    def get_supported_platforms(cls) -> List[str]:
        """Get list of supported platforms"""
        return list(cls.CRAWLERS.keys())

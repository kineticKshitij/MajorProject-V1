from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
import json
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import quote_plus, urlparse
from .models import DorkCategory, GoogleDork, SearchResult, SearchSession, DorkBookmark


def home(request):
    """Main dashboard showing statistics and recent activity"""
    context = {
        'total_dorks': GoogleDork.objects.filter(is_active=True).count(),
        'total_categories': DorkCategory.objects.count(),
        'total_results': SearchResult.objects.count(),
        'recent_dorks': GoogleDork.objects.filter(is_active=True)[:5],
        'categories': DorkCategory.objects.annotate(dork_count=Count('dorks')),
        'recent_results': SearchResult.objects.select_related('dork')[:10],
    }
    return render(request, 'googledorks/home.html', context)


def dork_list(request):
    """List all Google dorks with filtering and search"""
    dorks = GoogleDork.objects.filter(is_active=True).select_related('category')
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        dorks = dorks.filter(category_id=category_id)
    
    # Filter by difficulty
    difficulty = request.GET.get('difficulty')
    if difficulty:
        dorks = dorks.filter(difficulty=difficulty)
    
    # Filter by risk level
    risk_level = request.GET.get('risk_level')
    if risk_level:
        dorks = dorks.filter(risk_level=risk_level)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        dorks = dorks.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(query__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    dorks = dorks.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(dorks, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Process categories to include selected state
    categories_with_selected = []
    for cat in DorkCategory.objects.all():
        categories_with_selected.append({
            'pk': cat.pk,
            'name': cat.name,
            'selected': str(cat.pk) == str(category_id) if category_id else False
        })
    
    context = {
        'page_obj': page_obj,
        'categories': DorkCategory.objects.all(),
        'categories_with_selected': categories_with_selected,
        'current_filters': {
            'category': category_id,
            'difficulty': difficulty,
            'risk_level': risk_level,
            'search': search_query,
            'sort': sort_by,
        }
    }
    return render(request, 'googledorks/dork_list.html', context)


def dork_detail(request, pk):
    """Show detailed view of a Google dork"""
    dork = get_object_or_404(GoogleDork, pk=pk)
    results = SearchResult.objects.filter(dork=dork).order_by('-search_date')[:50]
    
    context = {
        'dork': dork,
        'results': results,
        'result_count': results.count(),
        'is_bookmarked': False,
    }
    
    if request.user.is_authenticated:
        context['is_bookmarked'] = DorkBookmark.objects.filter(
            user=request.user, dork=dork
        ).exists()
    
    return render(request, 'googledorks/dork_detail.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def execute_dork(request, pk):
    """Execute a Google dork and save results"""
    dork = get_object_or_404(GoogleDork, pk=pk)
    
    try:
        # Simple Google search simulation (replace with proper implementation)
        search_url = f"https://www.google.com/search?q={quote_plus(dork.query)}"
        
        # For demonstration, we'll create some mock results
        # In a real implementation, you'd use proper web scraping or API
        mock_results = [
            {
                'title': f'Sample result for: {dork.title}',
                'url': 'https://example.com/sample',
                'snippet': f'This is a sample search result for the dork: {dork.query}',
            }
        ]
        
        saved_count = 0
        for result_data in mock_results:
            result, created = SearchResult.objects.get_or_create(
                dork=dork,
                url=result_data['url'],
                defaults={
                    'title': result_data['title'],
                    'snippet': result_data['snippet'],
                }
            )
            if created:
                saved_count += 1
        
        dork.increment_usage()
        
        return JsonResponse({
            'success': True,
            'message': f'Found and saved {saved_count} new results',
            'results_count': saved_count
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error executing dork: {str(e)}'
        })


def category_list(request):
    """List all categories with their dork counts"""
    categories = DorkCategory.objects.annotate(
        dork_count=Count('dorks', filter=Q(dorks__is_active=True))
    ).order_by('name')
    
    context = {
        'categories': categories,
    }
    return render(request, 'googledorks/category_list.html', context)


def category_detail(request, pk):
    """Show dorks in a specific category"""
    category = get_object_or_404(DorkCategory, pk=pk)
    dorks = GoogleDork.objects.filter(category=category, is_active=True)
    
    # Pagination
    paginator = Paginator(dorks, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'googledorks/category_detail.html', context)


@login_required
def bookmark_dork(request, pk):
    """Add or remove a dork bookmark"""
    dork = get_object_or_404(GoogleDork, pk=pk)
    bookmark, created = DorkBookmark.objects.get_or_create(
        user=request.user,
        dork=dork
    )
    
    if not created:
        bookmark.delete()
        messages.success(request, f'Removed "{dork.title}" from bookmarks')
        bookmarked = False
    else:
        messages.success(request, f'Added "{dork.title}" to bookmarks')
        bookmarked = True
    
    if request.is_ajax():
        return JsonResponse({'bookmarked': bookmarked})
    
    return redirect('googledorks:dork_detail', pk=pk)


@login_required
def my_bookmarks(request):
    """Show user's bookmarked dorks"""
    bookmarks = DorkBookmark.objects.filter(user=request.user).select_related('dork')
    
    # Pagination
    paginator = Paginator(bookmarks, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'googledorks/my_bookmarks.html', context)


def search_results(request):
    """Search through saved results"""
    results = SearchResult.objects.select_related('dork').all()
    
    # Filter by domain
    domain = request.GET.get('domain')
    if domain:
        results = results.filter(domain__icontains=domain)
    
    # Filter by interesting
    interesting = request.GET.get('interesting')
    if interesting == 'true':
        results = results.filter(is_interesting=True)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        results = results.filter(
            Q(title__icontains=search_query) |
            Q(snippet__icontains=search_query) |
            Q(url__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(results, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'current_filters': {
            'domain': domain,
            'interesting': interesting,
            'search': search_query,
        }
    }
    return render(request, 'googledorks/search_results.html', context)


@login_required
def create_session(request):
    """Create a new search session"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        selected_dorks = request.POST.getlist('dorks')
        
        if name and selected_dorks:
            session = SearchSession.objects.create(
                name=name,
                description=description,
                created_by=request.user
            )
            session.dorks.set(selected_dorks)
            messages.success(request, f'Created search session "{name}"')
            return redirect('googledorks:session_detail', pk=session.pk)
        else:
            messages.error(request, 'Please provide a name and select at least one dork')
    
    dorks = GoogleDork.objects.filter(is_active=True).select_related('category')
    categories = DorkCategory.objects.all()
    
    context = {
        'dorks': dorks,
        'categories': categories,
    }
    return render(request, 'googledorks/create_session.html', context)


@login_required
def session_detail(request, pk):
    """Show details of a search session"""
    session = get_object_or_404(SearchSession, pk=pk)
    
    context = {
        'session': session,
    }
    return render(request, 'googledorks/session_detail.html', context)

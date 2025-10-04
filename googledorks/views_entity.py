"""
Views for entity management and research functionality
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, Http404
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg, Max
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.urls import reverse
import json
import csv
import io
from datetime import datetime, timedelta

from .models_entity import (
    EntityType, Entity, EntityAttribute, EntitySearchTemplate,
    EntitySearchSession, EntitySearchResult, EntityRelationship, EntityNote
)
from .forms_entity import (
    EntityForm, EntityQuickCreateForm, EntityAttributeForm, EntitySearchTemplateForm,
    EntitySearchSessionForm, EntityNoteForm, EntityRelationshipForm, EntitySearchForm,
    EntityBulkImportForm, EntityAttributeFormSet
)
from .models import GoogleDork, SearchResult


@login_required
def entity_dashboard(request):
    """Main dashboard for entity management"""
    # Get user's entities with statistics
    user_entities = Entity.objects.filter(created_by=request.user)
    
    # Statistics
    stats = {
        'total_entities': user_entities.count(),
        'active_entities': user_entities.filter(status='active').count(),
        'high_priority': user_entities.filter(priority='high').count(),
        'recent_searches': user_entities.filter(last_researched__gte=timezone.now() - timedelta(days=7)).count(),
    }
    
    # Recent entities
    recent_entities = user_entities.select_related('entity_type')[:10]
    
    # Most searched entities
    top_entities = user_entities.filter(search_count__gt=0).order_by('-search_count')[:5]
    
    # Entity type distribution
    entity_types = EntityType.objects.annotate(
        count=Count('entities', filter=Q(entities__created_by=request.user))
    ).filter(count__gt=0)
    
    # Recent search sessions
    recent_sessions = EntitySearchSession.objects.filter(
        created_by=request.user
    ).select_related('entity')[:5]
    
    context = {
        'stats': stats,
        'recent_entities': recent_entities,
        'top_entities': top_entities,
        'entity_types': entity_types,
        'recent_sessions': recent_sessions,
    }
    return render(request, 'googledorks/entity/dashboard.html', context)


@login_required
def entity_list(request):
    """List all entities with filtering and search"""
    entities = Entity.objects.filter(created_by=request.user).select_related('entity_type')
    
    # Apply search form filters
    form = EntitySearchForm(request.GET or None)
    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        if search_query:
            entities = entities.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(aliases__icontains=search_query) |
                Q(tags__icontains=search_query)
            )
        
        entity_type = form.cleaned_data.get('entity_type')
        if entity_type:
            entities = entities.filter(entity_type=entity_type)
        
        status = form.cleaned_data.get('status')
        if status:
            entities = entities.filter(status=status)
        
        priority = form.cleaned_data.get('priority')
        if priority:
            entities = entities.filter(priority=priority)
        
        sort_by = form.cleaned_data.get('sort_by', '-updated_at')
        entities = entities.order_by(sort_by)
    else:
        entities = entities.order_by('-updated_at')
    
    # Pagination
    paginator = Paginator(entities, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'entity_types': EntityType.objects.filter(is_active=True),
    }
    return render(request, 'googledorks/entity/list.html', context)


@login_required
def entity_detail(request, pk):
    """Detailed view of an entity"""
    entity = get_object_or_404(Entity, pk=pk, created_by=request.user)
    
    # Get related data
    attributes = entity.attributes.filter(is_public=True).order_by('key')
    notes = entity.notes.filter(
        Q(created_by=request.user) | Q(is_private=False)
    ).order_by('-created_at')[:10]
    
    search_sessions = entity.search_sessions.filter(created_by=request.user).order_by('-created_at')[:5]
    recent_results = entity.search_results.order_by('-found_at')[:20]
    
    # Relationships
    relationships_from = entity.relationships_from.filter(is_active=True).select_related('to_entity')
    relationships_to = entity.relationships_to.filter(is_active=True).select_related('from_entity')
    
    # Statistics
    stats = {
        'total_searches': entity.search_count,
        'total_results': entity.search_results.count(),
        'interesting_results': entity.search_results.filter(is_interesting=True).count(),
        'recent_activity': entity.last_researched,
        'total_sessions': search_sessions.count(),
        'total_notes': notes.count(),
    }
    
    # Available search templates for this entity type
    available_templates = EntitySearchTemplate.objects.filter(
        entity_type=entity.entity_type, is_active=True
    ).order_by('category', 'name')
    
    context = {
        'entity': entity,
        'attributes': attributes,
        'notes': notes,
        'search_sessions': search_sessions,
        'recent_results': recent_results,
        'relationships_from': relationships_from,
        'relationships_to': relationships_to,
        'stats': stats,
        'available_templates': available_templates,
    }
    return render(request, 'googledorks/entity/detail.html', context)


@login_required
def entity_create(request):
    """Create a new entity"""
    if request.method == 'POST':
        form = EntityForm(request.POST)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.created_by = request.user
            entity.save()
            form.save_m2m()  # Save many-to-many relationships
            
            messages.success(request, f'Entity "{entity.name}" created successfully!')
            return redirect('googledorks:entity_detail', pk=entity.pk)
    else:
        form = EntityForm()
    
    context = {
        'form': form,
        'title': 'Create New Entity',
    }
    return render(request, 'googledorks/entity/form.html', context)


@login_required
def entity_edit(request, pk):
    """Edit an existing entity"""
    entity = get_object_or_404(Entity, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        form = EntityForm(request.POST, instance=entity)
        if form.is_valid():
            form.save()
            messages.success(request, f'Entity "{entity.name}" updated successfully!')
            return redirect('googledorks:entity_detail', pk=entity.pk)
    else:
        form = EntityForm(instance=entity)
    
    context = {
        'form': form,
        'entity': entity,
        'title': f'Edit {entity.name}',
    }
    return render(request, 'googledorks/entity/form.html', context)


@login_required
def entity_delete(request, pk):
    """Delete an entity"""
    entity = get_object_or_404(Entity, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        entity_name = entity.name
        entity.delete()
        messages.success(request, f'Entity "{entity_name}" deleted successfully!')
        return redirect('googledorks:entity_list')
    
    context = {
        'entity': entity,
    }
    return render(request, 'googledorks/entity/delete_confirm.html', context)


@login_required
def entity_quick_create(request):
    """Quick create entity (AJAX)"""
    if request.method == 'POST':
        form = EntityQuickCreateForm(request.POST)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.created_by = request.user
            entity.save()
            
            return JsonResponse({
                'success': True,
                'entity': {
                    'id': str(entity.pk),
                    'name': entity.name,
                    'url': reverse('googledorks:entity_detail', kwargs={'pk': entity.pk})
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required
def entity_search_session_create(request, entity_pk):
    """Create a search session for an entity"""
    entity = get_object_or_404(Entity, pk=entity_pk, created_by=request.user)
    
    if request.method == 'POST':
        form = EntitySearchSessionForm(request.POST, entity=entity)
        if form.is_valid():
            session = form.save(commit=False)
            session.entity = entity
            session.created_by = request.user
            session.save()
            form.save_m2m()
            
            messages.success(request, f'Search session "{session.name}" created!')
            return redirect('googledorks:entity_session_detail', pk=session.pk)
    else:
        form = EntitySearchSessionForm(entity=entity)
    
    context = {
        'form': form,
        'entity': entity,
        'title': f'Create Search Session for {entity.name}',
    }
    return render(request, 'googledorks/entity/session_form.html', context)


@login_required
def entity_search_session_detail(request, pk):
    """View details of an entity search session"""
    session = get_object_or_404(EntitySearchSession, pk=pk, created_by=request.user)
    
    # Get session results
    results = session.results.order_by('-found_at')
    
    # Progress tracking
    templates = session.search_templates.all()
    progress = {
        'total_templates': templates.count(),
        'completed': 0,  # This would be calculated based on actual execution
        'percentage': session.get_progress_percentage(),
    }
    
    context = {
        'session': session,
        'results': results,
        'templates': templates,
        'progress': progress,
    }
    return render(request, 'googledorks/entity/session_detail.html', context)


@login_required
def entity_execute_template(request, entity_pk, template_pk):
    """Execute a search template for an entity"""
    entity = get_object_or_404(Entity, pk=entity_pk, created_by=request.user)
    template = get_object_or_404(EntitySearchTemplate, pk=template_pk)
    
    try:
        # Generate the query for this entity
        query = template.generate_query(entity)
        
        # Create mock search results (in real implementation, you'd actually search)
        mock_results = [
            {
                'title': f'Sample result for {entity.name} - {template.name}',
                'url': f'https://example.com/search?q={query}',
                'snippet': f'This is a sample search result for {entity.name} using template {template.name}',
            }
        ]
        
        saved_count = 0
        for result_data in mock_results:
            result, created = EntitySearchResult.objects.get_or_create(
                entity=entity,
                url=result_data['url'],
                defaults={
                    'template': template,
                    'title': result_data['title'],
                    'snippet': result_data['snippet'],
                }
            )
            if created:
                saved_count += 1
        
        # Update counters
        entity.increment_search_count()
        template.increment_usage()
        
        return JsonResponse({
            'success': True,
            'message': f'Found {saved_count} new results',
            'query': query,
            'results_count': saved_count
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error executing template: {str(e)}'
        })


@login_required
def entity_add_note(request, entity_pk):
    """Add a note to an entity"""
    entity = get_object_or_404(Entity, pk=entity_pk, created_by=request.user)
    
    if request.method == 'POST':
        form = EntityNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.entity = entity
            note.created_by = request.user
            note.save()
            
            messages.success(request, 'Note added successfully!')
            return redirect('googledorks:entity_detail', pk=entity.pk)
    else:
        form = EntityNoteForm()
    
    context = {
        'form': form,
        'entity': entity,
        'title': f'Add Note to {entity.name}',
    }
    return render(request, 'googledorks/entity/note_form.html', context)


@login_required
def entity_add_attribute(request, entity_pk):
    """Add an attribute to an entity"""
    entity = get_object_or_404(Entity, pk=entity_pk, created_by=request.user)
    
    if request.method == 'POST':
        form = EntityAttributeForm(request.POST)
        if form.is_valid():
            attribute = form.save(commit=False)
            attribute.entity = entity
            attribute.save()
            
            messages.success(request, f'Attribute "{attribute.key}" added successfully!')
            return redirect('googledorks:entity_detail', pk=entity.pk)
    else:
        form = EntityAttributeForm()
    
    context = {
        'form': form,
        'entity': entity,
        'title': f'Add Attribute to {entity.name}',
    }
    return render(request, 'googledorks/entity/attribute_form.html', context)


@login_required
def entity_bulk_import(request):
    """Bulk import entities from CSV"""
    if request.method == 'POST':
        form = EntityBulkImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            entity_type = form.cleaned_data['entity_type']
            has_header = form.cleaned_data['has_header']
            
            try:
                # Read CSV file
                decoded_file = csv_file.read().decode('utf-8')
                csv_reader = csv.reader(io.StringIO(decoded_file))
                
                if has_header:
                    headers = next(csv_reader)
                
                imported_count = 0
                errors = []
                
                for row_num, row in enumerate(csv_reader, start=2 if has_header else 1):
                    if len(row) < 1:
                        continue
                    
                    try:
                        # Basic CSV format: name, description, website, location, industry
                        entity_data = {
                            'name': row[0] if len(row) > 0 else '',
                            'description': row[1] if len(row) > 1 else '',
                            'website': row[2] if len(row) > 2 else '',
                            'location': row[3] if len(row) > 3 else '',
                            'industry': row[4] if len(row) > 4 else '',
                        }
                        
                        if entity_data['name']:
                            entity, created = Entity.objects.get_or_create(
                                name=entity_data['name'],
                                created_by=request.user,
                                defaults={
                                    'entity_type': entity_type,
                                    'description': entity_data['description'],
                                    'website': entity_data['website'],
                                    'location': entity_data['location'],
                                    'industry': entity_data['industry'],
                                }
                            )
                            
                            if created:
                                imported_count += 1
                    
                    except Exception as e:
                        errors.append(f"Row {row_num}: {str(e)}")
                
                if imported_count > 0:
                    messages.success(request, f'Successfully imported {imported_count} entities!')
                
                if errors:
                    error_msg = f"{len(errors)} errors occurred: " + "; ".join(errors[:5])
                    if len(errors) > 5:
                        error_msg += f" and {len(errors) - 5} more..."
                    messages.warning(request, error_msg)
                
                return redirect('googledorks:entity_list')
                
            except Exception as e:
                messages.error(request, f'Error processing CSV file: {str(e)}')
    else:
        form = EntityBulkImportForm()
    
    context = {
        'form': form,
        'title': 'Bulk Import Entities',
    }
    return render(request, 'googledorks/entity/bulk_import.html', context)


@login_required
def entity_export_csv(request):
    """Export entities to CSV"""
    entities = Entity.objects.filter(created_by=request.user).select_related('entity_type')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="entities.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Name', 'Type', 'Description', 'Website', 'Location', 'Industry',
        'Priority', 'Status', 'Created', 'Last Researched', 'Search Count'
    ])
    
    for entity in entities:
        writer.writerow([
            entity.name,
            entity.entity_type.display_name,
            entity.description,
            entity.website,
            entity.location,
            entity.industry,
            entity.get_priority_display(),
            entity.get_status_display(),
            entity.created_at.strftime('%Y-%m-%d'),
            entity.last_researched.strftime('%Y-%m-%d') if entity.last_researched else '',
            entity.search_count,
        ])
    
    return response


@login_required
def entity_templates(request):
    """List all search templates"""
    templates = EntitySearchTemplate.objects.filter(is_active=True).select_related('entity_type')
    
    # Filter by entity type
    entity_type_id = request.GET.get('entity_type')
    if entity_type_id:
        templates = templates.filter(entity_type_id=entity_type_id)
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        templates = templates.filter(category=category)
    
    # Pagination
    paginator = Paginator(templates, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'entity_types': EntityType.objects.filter(is_active=True),
        'categories': EntitySearchTemplate._meta.get_field('category').choices,
        'current_filters': {
            'entity_type': entity_type_id,
            'category': category,
        }
    }
    return render(request, 'googledorks/entity/templates.html', context)


@login_required
def entity_analytics(request):
    """Analytics dashboard for entities"""
    user_entities = Entity.objects.filter(created_by=request.user)
    
    # Time-based analytics
    now = timezone.now()
    last_week = now - timedelta(days=7)
    last_month = now - timedelta(days=30)
    
    analytics = {
        'entity_counts': {
            'total': user_entities.count(),
            'active': user_entities.filter(status='active').count(),
            'completed': user_entities.filter(status='completed').count(),
            'on_hold': user_entities.filter(status='on_hold').count(),
        },
        'priority_distribution': {
            'critical': user_entities.filter(priority='critical').count(),
            'high': user_entities.filter(priority='high').count(),
            'medium': user_entities.filter(priority='medium').count(),
            'low': user_entities.filter(priority='low').count(),
        },
        'activity_stats': {
            'searched_last_week': user_entities.filter(last_researched__gte=last_week).count(),
            'searched_last_month': user_entities.filter(last_researched__gte=last_month).count(),
            'never_searched': user_entities.filter(last_researched__isnull=True).count(),
        },
        'top_entities': user_entities.filter(search_count__gt=0).order_by('-search_count')[:10],
        'recent_entities': user_entities.order_by('-created_at')[:10],
    }
    
    # Entity type distribution
    type_distribution = EntityType.objects.annotate(
        count=Count('entities', filter=Q(entities__created_by=request.user))
    ).filter(count__gt=0)
    
    context = {
        'analytics': analytics,
        'type_distribution': type_distribution,
    }
    return render(request, 'googledorks/entity/analytics.html', context)
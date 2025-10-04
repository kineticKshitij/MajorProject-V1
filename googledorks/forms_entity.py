"""
Forms for entity management and research
"""

from django import forms
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError
import json
from .models_entity import (
    Entity, EntityType, EntityAttribute, EntitySearchTemplate,
    EntitySearchSession, EntityNote, EntityRelationship
)
from .models import GoogleDork


class EntityForm(forms.ModelForm):
    """Form for creating and editing entities"""
    
    # Additional fields for easier input
    aliases_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter alternative names, one per line'
        }),
        help_text="Alternative names, acronyms, abbreviations (one per line)"
    )
    
    domains_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'example.com\nsubdomain.example.com'
        }),
        help_text="Known domains associated with this entity (one per line)"
    )
    
    tags_text = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'tag1, tag2, tag3'
        }),
        help_text="Tags separated by commas"
    )
    
    # Social media fields
    twitter_handle = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '@username'})
    )
    linkedin_handle = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'company-name'})
    )
    facebook_handle = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'page-name'})
    )
    instagram_handle = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '@username'})
    )
    
    class Meta:
        model = Entity
        fields = [
            'name', 'entity_type', 'description', 'industry', 'location',
            'founded_date', 'website', 'priority', 'status'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'entity_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'industry': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'founded_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Populate additional fields if editing existing entity
        if self.instance and self.instance.pk:
            if self.instance.aliases:
                self.fields['aliases_text'].initial = '\n'.join(self.instance.aliases)
            
            if self.instance.domains:
                self.fields['domains_text'].initial = '\n'.join(self.instance.domains)
            
            if self.instance.tags:
                self.fields['tags_text'].initial = ', '.join(self.instance.tags)
            
            # Populate social media fields
            social_media = self.instance.social_media or {}
            self.fields['twitter_handle'].initial = social_media.get('twitter', '')
            self.fields['linkedin_handle'].initial = social_media.get('linkedin', '')
            self.fields['facebook_handle'].initial = social_media.get('facebook', '')
            self.fields['instagram_handle'].initial = social_media.get('instagram', '')
    
    def clean_aliases_text(self):
        """Convert aliases text to list"""
        aliases_text = self.cleaned_data.get('aliases_text', '')
        if aliases_text:
            return [alias.strip() for alias in aliases_text.split('\n') if alias.strip()]
        return []
    
    def clean_domains_text(self):
        """Convert domains text to list and validate"""
        domains_text = self.cleaned_data.get('domains_text', '')
        if domains_text:
            domains = [domain.strip().lower() for domain in domains_text.split('\n') if domain.strip()]
            # Basic domain validation
            for domain in domains:
                if not domain.replace('.', '').replace('-', '').replace('_', '').isalnum():
                    raise ValidationError(f"Invalid domain format: {domain}")
            return domains
        return []
    
    def clean_tags_text(self):
        """Convert tags text to list"""
        tags_text = self.cleaned_data.get('tags_text', '')
        if tags_text:
            return [tag.strip() for tag in tags_text.split(',') if tag.strip()]
        return []
    
    def save(self, commit=True):
        entity = super().save(commit=False)
        
        # Set JSON fields from text inputs
        entity.aliases = self.cleaned_data.get('aliases_text', [])
        entity.domains = self.cleaned_data.get('domains_text', [])
        entity.tags = self.cleaned_data.get('tags_text', [])
        
        # Set social media
        social_media = {}
        if self.cleaned_data.get('twitter_handle'):
            social_media['twitter'] = self.cleaned_data['twitter_handle']
        if self.cleaned_data.get('linkedin_handle'):
            social_media['linkedin'] = self.cleaned_data['linkedin_handle']
        if self.cleaned_data.get('facebook_handle'):
            social_media['facebook'] = self.cleaned_data['facebook_handle']
        if self.cleaned_data.get('instagram_handle'):
            social_media['instagram'] = self.cleaned_data['instagram_handle']
        
        entity.social_media = social_media
        
        if commit:
            entity.save()
            
        return entity


class EntityQuickCreateForm(forms.ModelForm):
    """Simplified form for quick entity creation"""
    
    class Meta:
        model = Entity
        fields = ['name', 'entity_type', 'website', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entity name'}),
            'entity_type': forms.Select(attrs={'class': 'form-select'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief description...'}),
        }


class EntityAttributeForm(forms.ModelForm):
    """Form for adding attributes to entities"""
    
    class Meta:
        model = EntityAttribute
        fields = ['key', 'value', 'value_type', 'source', 'confidence', 'is_public']
        widgets = {
            'key': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., CEO, Employee Count'}),
            'value': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'value_type': forms.Select(attrs={'class': 'form-select'}),
            'source': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Source of information'}),
            'confidence': forms.Select(attrs={'class': 'form-select'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EntitySearchTemplateForm(forms.ModelForm):
    """Form for creating search templates"""
    
    class Meta:
        model = EntitySearchTemplate
        fields = [
            'entity_type', 'name', 'description', 'query_template',
            'category', 'risk_level', 'difficulty'
        ]
        widgets = {
            'entity_type': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'query_template': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Use placeholders like {entity_name}, {domain}, {location}'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'risk_level': forms.Select(attrs={'class': 'form-select'}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
        }


class EntitySearchSessionForm(forms.ModelForm):
    """Form for creating entity search sessions"""
    
    class Meta:
        model = EntitySearchSession
        fields = [
            'entity', 'name', 'description', 'search_templates',
            'auto_execute', 'save_results', 'notify_completion'
        ]
        widgets = {
            'entity': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'search_templates': forms.CheckboxSelectMultiple(),
            'auto_execute': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'save_results': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notify_completion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        entity = kwargs.pop('entity', None)
        super().__init__(*args, **kwargs)
        
        if entity:
            self.fields['entity'].initial = entity
            self.fields['entity'].widget = forms.HiddenInput()
            # Filter templates by entity type
            self.fields['search_templates'].queryset = EntitySearchTemplate.objects.filter(
                entity_type=entity.entity_type, is_active=True
            )


class EntityNoteForm(forms.ModelForm):
    """Form for adding notes to entities"""
    
    class Meta:
        model = EntityNote
        fields = ['title', 'content', 'note_type', 'priority', 'is_private']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'note_type': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EntityRelationshipForm(forms.ModelForm):
    """Form for creating relationships between entities"""
    
    class Meta:
        model = EntityRelationship
        fields = [
            'from_entity', 'to_entity', 'relationship_type',
            'description', 'confidence', 'source',
            'start_date', 'end_date', 'is_active'
        ]
        widgets = {
            'from_entity': forms.Select(attrs={'class': 'form-select'}),
            'to_entity': forms.Select(attrs={'class': 'form-select'}),
            'relationship_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'confidence': forms.Select(attrs={'class': 'form-select'}),
            'source': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EntitySearchForm(forms.Form):
    """Form for searching entities"""
    
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search entities by name, description, or tags...'
        })
    )
    
    entity_type = forms.ModelChoiceField(
        queryset=EntityType.objects.filter(is_active=True),
        required=False,
        empty_label="All Types",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    status = forms.ChoiceField(
        choices=[('', 'All Statuses')] + Entity.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    priority = forms.ChoiceField(
        choices=[('', 'All Priorities')] + Entity.PRIORITY_LEVELS,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    sort_by = forms.ChoiceField(
        choices=[
            ('name', 'Name A-Z'),
            ('-name', 'Name Z-A'),
            ('-updated_at', 'Recently Updated'),
            ('updated_at', 'Oldest Updated'),
            ('-created_at', 'Recently Created'),
            ('created_at', 'Oldest Created'),
            ('-search_count', 'Most Searched'),
            ('search_count', 'Least Searched'),
        ],
        required=False,
        initial='-updated_at',
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class EntityBulkImportForm(forms.Form):
    """Form for bulk importing entities from CSV"""
    
    csv_file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv'}),
        help_text="Upload a CSV file with entity data"
    )
    
    entity_type = forms.ModelChoiceField(
        queryset=EntityType.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Default entity type for imported entities"
    )
    
    has_header = forms.BooleanField(
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text="Check if the CSV file has a header row"
    )
    
    def clean_csv_file(self):
        csv_file = self.cleaned_data.get('csv_file')
        if csv_file:
            if not csv_file.name.endswith('.csv'):
                raise ValidationError('File must be a CSV file.')
            if csv_file.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError('File size must be less than 5MB.')
        return csv_file


# Formset for managing multiple entity attributes
EntityAttributeFormSet = modelformset_factory(
    EntityAttribute,
    form=EntityAttributeForm,
    extra=1,
    can_delete=True,
    widgets={
        'DELETE': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    }
)
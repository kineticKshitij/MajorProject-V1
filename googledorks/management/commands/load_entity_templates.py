"""
Management command to load sample entity types and search templates
"""

from django.core.management.base import BaseCommand
from googledorks.models_entity import EntityType, EntitySearchTemplate


class Command(BaseCommand):
    help = 'Load sample entity types and search templates'

    def handle(self, *args, **options):
        self.stdout.write('Loading entity types and search templates...')
        
        # Create entity types
        entity_types_data = [
            {
                'name': 'company',
                'display_name': 'Company',
                'description': 'Business entities, corporations, startups',
                'icon': 'bi-building',
                'color': '#007bff'
            },
            {
                'name': 'person',
                'display_name': 'Person',
                'description': 'Individuals, executives, public figures',
                'icon': 'bi-person',
                'color': '#28a745'
            },
            {
                'name': 'organization',
                'display_name': 'Organization',
                'description': 'Non-profit organizations, NGOs, foundations',
                'icon': 'bi-people',
                'color': '#17a2b8'
            },
            {
                'name': 'government',
                'display_name': 'Government Agency',
                'description': 'Government departments, agencies, institutions',
                'icon': 'bi-bank',
                'color': '#6c757d'
            },
            {
                'name': 'educational',
                'display_name': 'Educational Institution',
                'description': 'Universities, schools, research institutions',
                'icon': 'bi-mortarboard',
                'color': '#ffc107'
            },
            {
                'name': 'domain',
                'display_name': 'Domain/Website',
                'description': 'Websites, domains, online platforms',
                'icon': 'bi-globe',
                'color': '#dc3545'
            },
        ]
        
        for entity_type_data in entity_types_data:
            entity_type, created = EntityType.objects.get_or_create(
                name=entity_type_data['name'],
                defaults=entity_type_data
            )
            if created:
                self.stdout.write(f'Created entity type: {entity_type.display_name}')
        
        # Create search templates for companies
        company_type = EntityType.objects.get(name='company')
        company_templates = [
            {
                'name': 'Basic Company Information',
                'description': 'Find basic information about the company',
                'query_template': 'site:{domain} OR "{entity_name}" "about us" OR "company" OR "corporation"',
                'category': 'basic_info',
                'risk_level': 'low',
                'difficulty': 'beginner'
            },
            {
                'name': 'Employee Directory',
                'description': 'Find employee listings and directories',
                'query_template': '"{entity_name}" "employee" OR "staff" OR "team" OR "directory" OR "people"',
                'category': 'employees',
                'risk_level': 'medium',
                'difficulty': 'intermediate'
            },
            {
                'name': 'Contact Information',
                'description': 'Find contact details and office locations',
                'query_template': '"{entity_name}" "contact" OR "phone" OR "email" OR "address" OR "office"',
                'category': 'contact_info',
                'risk_level': 'low',
                'difficulty': 'beginner'
            },
            {
                'name': 'Financial Information',
                'description': 'Find financial reports and investor information',
                'query_template': '"{entity_name}" "financial" OR "investor" OR "earnings" OR "revenue" OR "annual report"',
                'category': 'financials',
                'risk_level': 'low',
                'difficulty': 'beginner'
            },
            {
                'name': 'Document Discovery',
                'description': 'Find exposed documents and files',
                'query_template': 'site:{domain} filetype:pdf OR filetype:doc OR filetype:xls OR filetype:ppt',
                'category': 'documents',
                'risk_level': 'high',
                'difficulty': 'advanced'
            },
            {
                'name': 'Subdomain Discovery',
                'description': 'Find subdomains and related domains',
                'query_template': 'site:*.{domain} -site:www.{domain}',
                'category': 'infrastructure',
                'risk_level': 'medium',
                'difficulty': 'intermediate'
            },
            {
                'name': 'Social Media Presence',
                'description': 'Find official social media accounts',
                'query_template': '"{entity_name}" site:linkedin.com OR site:twitter.com OR site:facebook.com OR site:instagram.com',
                'category': 'social_media',
                'risk_level': 'low',
                'difficulty': 'beginner'
            },
            {
                'name': 'Login Pages',
                'description': 'Find login and authentication pages',
                'query_template': 'site:{domain} "login" OR "sign in" OR "authentication" OR "portal"',
                'category': 'infrastructure',
                'risk_level': 'medium',
                'difficulty': 'intermediate'
            },
            {
                'name': 'Job Postings',
                'description': 'Find current job openings and career pages',
                'query_template': '"{entity_name}" "jobs" OR "careers" OR "hiring" OR "employment" OR "vacancies"',
                'category': 'basic_info',
                'risk_level': 'low',
                'difficulty': 'beginner'
            },
            {
                'name': 'News and Press',
                'description': 'Find news articles and press releases',
                'query_template': '"{entity_name}" "news" OR "press release" OR "announcement" OR "media"',
                'category': 'news',
                'risk_level': 'low',
                'difficulty': 'beginner'
            }
        ]
        
        for template_data in company_templates:
            template, created = EntitySearchTemplate.objects.get_or_create(
                entity_type=company_type,
                name=template_data['name'],
                defaults=template_data
            )
            if created:
                self.stdout.write(f'Created company template: {template.name}')
        
        # Create search templates for persons
        person_type = EntityType.objects.get(name='person')
        person_templates = [
            {
                'name': 'Social Media Profiles',
                'description': 'Find social media profiles and accounts',
                'query_template': '"{entity_name}" site:linkedin.com OR site:twitter.com OR site:facebook.com OR site:instagram.com',
                'category': 'social_media',
                'risk_level': 'low',
                'difficulty': 'beginner'
            },
            {
                'name': 'Professional Background',
                'description': 'Find professional experience and background',
                'query_template': '"{entity_name}" "resume" OR "CV" OR "experience" OR "background" OR "biography"',
                'category': 'basic_info',
                'risk_level': 'medium',
                'difficulty': 'beginner'
            },
            {
                'name': 'Contact Information',
                'description': 'Find email addresses and contact details',
                'query_template': '"{entity_name}" "email" OR "contact" OR "phone" OR "@" OR "reach"',
                'category': 'contact_info',
                'risk_level': 'medium',
                'difficulty': 'intermediate'
            },
            {
                'name': 'Publications and Articles',
                'description': 'Find published articles and research papers',
                'query_template': '"{entity_name}" "author" OR "published" OR "article" OR "paper" OR "research"',
                'category': 'basic_info',
                'risk_level': 'low',
                'difficulty': 'beginner'
            },
            {
                'name': 'Speaking Engagements',
                'description': 'Find conference talks and speaking events',
                'query_template': '"{entity_name}" "speaker" OR "presentation" OR "conference" OR "talk" OR "keynote"',
                'category': 'basic_info',
                'risk_level': 'low',
                'difficulty': 'beginner'
            }
        ]
        
        for template_data in person_templates:
            template, created = EntitySearchTemplate.objects.get_or_create(
                entity_type=person_type,
                name=template_data['name'],
                defaults=template_data
            )
            if created:
                self.stdout.write(f'Created person template: {template.name}')
        
        # Create search templates for domains
        domain_type = EntityType.objects.get(name='domain')
        domain_templates = [
            {
                'name': 'Directory Listing',
                'description': 'Find directory listings and exposed folders',
                'query_template': 'site:{domain} intitle:"Index of" OR intitle:"Directory Listing"',
                'category': 'vulnerabilities',
                'risk_level': 'high',
                'difficulty': 'advanced'
            },
            {
                'name': 'Configuration Files',
                'description': 'Find exposed configuration files',
                'query_template': 'site:{domain} filetype:conf OR filetype:config OR filetype:ini OR filetype:xml',
                'category': 'vulnerabilities',
                'risk_level': 'critical',
                'difficulty': 'advanced'
            },
            {
                'name': 'Backup Files',
                'description': 'Find backup and temporary files',
                'query_template': 'site:{domain} filetype:bak OR filetype:backup OR filetype:old OR filetype:tmp',
                'category': 'vulnerabilities',
                'risk_level': 'high',
                'difficulty': 'advanced'
            },
            {
                'name': 'Admin Panels',
                'description': 'Find administrative interfaces',
                'query_template': 'site:{domain} "admin" OR "administrator" OR "control panel" OR "dashboard"',
                'category': 'infrastructure',
                'risk_level': 'high',
                'difficulty': 'intermediate'
            },
            {
                'name': 'Error Pages',
                'description': 'Find error pages that might expose information',
                'query_template': 'site:{domain} "error" OR "exception" OR "stack trace" OR "debug"',
                'category': 'vulnerabilities',
                'risk_level': 'medium',
                'difficulty': 'intermediate'
            }
        ]
        
        for template_data in domain_templates:
            template, created = EntitySearchTemplate.objects.get_or_create(
                entity_type=domain_type,
                name=template_data['name'],
                defaults=template_data
            )
            if created:
                self.stdout.write(f'Created domain template: {template.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded entity types and search templates!')
        )
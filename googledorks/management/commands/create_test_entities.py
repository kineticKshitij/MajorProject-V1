"""
Management command to create test entities in the database.
Usage: python manage.py create_test_entities
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from googledorks.models_entity import Entity, EntityType, EntityAttribute, EntityRelationship
from datetime import date, timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates test entities in the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username of the user who should own the entities',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating test entities...'))
        
        # Get the user who should own the entities
        username = options.get('username')
        if username:
            try:
                user = User.objects.get(username=username)
                self.stdout.write(self.style.SUCCESS(f'Using existing user: {user.username}'))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User "{username}" not found. Please create this user first.'))
                return
        else:
            # Get or create a test user
            user, created = User.objects.get_or_create(
                username='testuser',
                defaults={'email': 'test@example.com'}
            )
            if created:
                user.set_password('testpass123')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created test user: {user.username}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Using test user: {user.username}'))
        
        # Get entity types
        try:
            company_type = EntityType.objects.get(name='company')
            person_type = EntityType.objects.get(name='person')
            org_type = EntityType.objects.get(name='organization')
            gov_type = EntityType.objects.get(name='government')
            edu_type = EntityType.objects.get(name='educational')
            domain_type = EntityType.objects.get(name='domain')
        except EntityType.DoesNotExist:
            self.stdout.write(self.style.ERROR('Entity types not found. Run migrations first.'))
            return
        
        # Test data for companies
        companies = [
            {
                'name': 'TechCorp Industries',
                'entity_type': company_type,
                'description': 'Leading technology company specializing in cloud computing and AI solutions',
                'industry': 'Technology',
                'location': 'San Francisco, CA',
                'website': 'https://techcorp.example.com',
                'domains': ['techcorp.com', 'techcorp.io', 'techcorp-labs.com'],
                'social_media': {
                    'linkedin': 'https://linkedin.com/company/techcorp',
                    'twitter': '@techcorp',
                    'github': 'https://github.com/techcorp'
                },
                'priority': 'high',
                'status': 'active',
                'tags': ['technology', 'cloud', 'ai', 'enterprise'],
                'founded_date': date(2015, 3, 15),
                'aliases': ['TechCorp', 'TC Industries']
            },
            {
                'name': 'Global Finance Group',
                'entity_type': company_type,
                'description': 'International financial services corporation with operations worldwide',
                'industry': 'Finance',
                'location': 'New York, NY',
                'website': 'https://globalfinance.example.com',
                'domains': ['gfgroup.com', 'globalfinance.com'],
                'social_media': {
                    'linkedin': 'https://linkedin.com/company/global-finance',
                    'twitter': '@gfgroup'
                },
                'priority': 'critical',
                'status': 'active',
                'tags': ['finance', 'banking', 'investment'],
                'founded_date': date(1998, 7, 22),
                'aliases': ['GFG', 'Global Finance']
            },
            {
                'name': 'Healthcare Solutions Ltd',
                'entity_type': company_type,
                'description': 'Healthcare technology and medical research company',
                'industry': 'Healthcare',
                'location': 'Boston, MA',
                'website': 'https://healthcaresolutions.example.com',
                'domains': ['healthcaresol.com', 'hcs-med.com'],
                'social_media': {
                    'linkedin': 'https://linkedin.com/company/healthcare-solutions'
                },
                'priority': 'medium',
                'status': 'active',
                'tags': ['healthcare', 'medical', 'research'],
                'founded_date': date(2010, 11, 5),
                'aliases': ['HCS', 'Healthcare Solutions']
            }
        ]
        
        # Test data for persons
        persons = [
            {
                'name': 'Dr. Sarah Chen',
                'entity_type': person_type,
                'description': 'Chief Technology Officer at TechCorp Industries, AI researcher',
                'industry': 'Technology',
                'location': 'San Francisco, CA',
                'social_media': {
                    'linkedin': 'https://linkedin.com/in/sarah-chen',
                    'twitter': '@sarahchen',
                    'github': 'https://github.com/schen'
                },
                'priority': 'high',
                'status': 'active',
                'tags': ['executive', 'ai', 'researcher'],
                'aliases': ['Sarah Chen', 'S. Chen']
            },
            {
                'name': 'Michael Rodriguez',
                'entity_type': person_type,
                'description': 'Security researcher and penetration testing expert',
                'industry': 'Cybersecurity',
                'location': 'Austin, TX',
                'website': 'https://mrodriguez.example.com',
                'social_media': {
                    'twitter': '@mrodriguez_sec',
                    'github': 'https://github.com/mrodriguez'
                },
                'priority': 'medium',
                'status': 'active',
                'tags': ['security', 'researcher', 'pentesting'],
                'aliases': ['M. Rodriguez', 'Mike Rodriguez']
            }
        ]
        
        # Test data for organizations
        organizations = [
            {
                'name': 'Open Source Foundation',
                'entity_type': org_type,
                'description': 'Non-profit organization supporting open source software development',
                'industry': 'Technology',
                'location': 'International',
                'website': 'https://opensourcefoundation.example.org',
                'domains': ['osf.org', 'opensource-foundation.org'],
                'social_media': {
                    'twitter': '@osfoundation',
                    'github': 'https://github.com/osf'
                },
                'priority': 'medium',
                'status': 'active',
                'tags': ['opensource', 'nonprofit', 'community'],
                'founded_date': date(2012, 1, 10),
                'aliases': ['OSF', 'Open Source Fund']
            }
        ]
        
        # Test data for government entities
        government = [
            {
                'name': 'National Cyber Security Center',
                'entity_type': gov_type,
                'description': 'Government agency responsible for national cybersecurity',
                'industry': 'Government',
                'location': 'Washington, DC',
                'website': 'https://ncsc.example.gov',
                'domains': ['ncsc.gov'],
                'priority': 'critical',
                'status': 'active',
                'tags': ['government', 'security', 'defense'],
                'founded_date': date(2005, 6, 1),
                'aliases': ['NCSC', 'Cyber Security Center']
            }
        ]
        
        # Test data for educational institutions
        educational = [
            {
                'name': 'Metropolitan University',
                'entity_type': edu_type,
                'description': 'Leading research university with focus on STEM',
                'industry': 'Education',
                'location': 'Chicago, IL',
                'website': 'https://metrou.example.edu',
                'domains': ['metrou.edu', 'metro-university.edu'],
                'social_media': {
                    'twitter': '@metrou',
                    'linkedin': 'https://linkedin.com/school/metropolitan-university'
                },
                'priority': 'medium',
                'status': 'active',
                'tags': ['education', 'university', 'research'],
                'founded_date': date(1985, 9, 1),
                'aliases': ['Metro U', 'Metropolitan U']
            }
        ]
        
        # Test data for domains
        domains = [
            {
                'name': 'example-target.com',
                'entity_type': domain_type,
                'description': 'Target domain for security research',
                'website': 'https://example-target.com',
                'domains': ['example-target.com', 'www.example-target.com'],
                'priority': 'high',
                'status': 'active',
                'tags': ['domain', 'target', 'research']
            }
        ]
        
        # Create entities
        created_entities = []
        all_test_data = companies + persons + organizations + government + educational + domains
        
        for entity_data in all_test_data:
            entity, created = Entity.objects.get_or_create(
                name=entity_data['name'],
                entity_type=entity_data['entity_type'],
                defaults={
                    **entity_data,
                    'created_by': user,
                    'search_count': random.randint(0, 50),
                    'results_found': random.randint(0, 200)
                }
            )
            
            if created:
                created_entities.append(entity)
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created: {entity.name} ({entity.entity_type.display_name})')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'- Already exists: {entity.name}')
                )
        
        # Create some attributes for entities
        self.stdout.write(self.style.SUCCESS('\nAdding attributes to entities...'))
        
        # Add attributes to TechCorp
        techcorp = Entity.objects.filter(name='TechCorp Industries').first()
        if techcorp:
            attributes = [
                {'key': 'Employee Count', 'value': '5000+', 'value_type': 'text'},
                {'key': 'Revenue', 'value': '$2.5B', 'value_type': 'text'},
                {'key': 'Stock Symbol', 'value': 'TECH', 'value_type': 'text'},
                {'key': 'CEO', 'value': 'John Smith', 'value_type': 'text'},
            ]
            for attr in attributes:
                EntityAttribute.objects.get_or_create(
                    entity=techcorp,
                    key=attr['key'],
                    defaults={
                        'value': attr['value'],
                        'value_type': attr['value_type']
                    }
                )
            self.stdout.write(self.style.SUCCESS(f'  ✓ Added {len(attributes)} attributes to TechCorp'))
        
        # Add attributes to Dr. Sarah Chen
        sarah = Entity.objects.filter(name='Dr. Sarah Chen').first()
        if sarah:
            attributes = [
                {'key': 'Position', 'value': 'Chief Technology Officer', 'value_type': 'text'},
                {'key': 'Education', 'value': 'PhD in Computer Science - MIT', 'value_type': 'text'},
                {'key': 'Specialization', 'value': 'Artificial Intelligence', 'value_type': 'text'},
            ]
            for attr in attributes:
                EntityAttribute.objects.get_or_create(
                    entity=sarah,
                    key=attr['key'],
                    defaults={
                        'value': attr['value'],
                        'value_type': attr['value_type']
                    }
                )
            self.stdout.write(self.style.SUCCESS(f'  ✓ Added {len(attributes)} attributes to Dr. Sarah Chen'))
        
        # Create some relationships
        techcorp = Entity.objects.filter(name='TechCorp Industries').first()
        sarah = Entity.objects.filter(name='Dr. Sarah Chen').first()
        osf = Entity.objects.filter(name='Open Source Foundation').first()
        
        if techcorp and sarah:
            rel, created = EntityRelationship.objects.get_or_create(
                from_entity=sarah,
                to_entity=techcorp,
                relationship_type='employee',
                defaults={
                    'description': 'CTO at TechCorp Industries',
                    'confidence': 'verified',
                    'is_active': True,
                    'created_by': user
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'\n✓ Created relationship: {sarah.name} → {techcorp.name}'))
        
        if techcorp and osf:
            rel, created = EntityRelationship.objects.get_or_create(
                from_entity=techcorp,
                to_entity=osf,
                relationship_type='partner',
                defaults={
                    'description': 'Corporate sponsor and contributor',
                    'confidence': 'high',
                    'is_active': True,
                    'created_by': user
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created relationship: {techcorp.name} → {osf.name}'))
        
        # Summary
        total_entities = Entity.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\n✅ Complete! Total entities in database: {total_entities}'))
        self.stdout.write(self.style.SUCCESS(f'   - Companies: {Entity.objects.filter(entity_type__name="company").count()}'))
        self.stdout.write(self.style.SUCCESS(f'   - Persons: {Entity.objects.filter(entity_type__name="person").count()}'))
        self.stdout.write(self.style.SUCCESS(f'   - Organizations: {Entity.objects.filter(entity_type__name="organization").count()}'))
        self.stdout.write(self.style.SUCCESS(f'   - Government: {Entity.objects.filter(entity_type__name="government").count()}'))
        self.stdout.write(self.style.SUCCESS(f'   - Educational: {Entity.objects.filter(entity_type__name="educational").count()}'))
        self.stdout.write(self.style.SUCCESS(f'   - Domains: {Entity.objects.filter(entity_type__name="domain").count()}'))

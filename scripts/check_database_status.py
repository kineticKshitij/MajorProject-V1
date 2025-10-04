#!/usr/bin/env python
"""
Quick database status check for testing
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InformationExtractor.settings')
django.setup()

from googledorks.models_entity import Entity
from googledorks.models import GoogleDork
from django.contrib.auth import get_user_model

User = get_user_model()

print("=" * 50)
print("DATABASE STATUS CHECK")
print("=" * 50)

# Check entities
total_entities = Entity.objects.count()
print(f"\n✓ Total Entities: {total_entities}")

# Check users
total_users = User.objects.count()
print(f"✓ Total Users: {total_users}")

# Check Major user
try:
    major = User.objects.get(username='Major')
    major_entities = Entity.objects.filter(created_by=major).count()
    print(f"✓ Major owns {major_entities} entities")
except User.DoesNotExist:
    print("✗ Major user not found!")

# Check entity types
from collections import Counter
entity_types = Entity.objects.values_list('entity_type__name', flat=True)
type_counts = Counter(entity_types)
print(f"\n📊 Entity Types:")
for entity_type, count in type_counts.items():
    print(f"   - {entity_type}: {count}")

# Check attributes
from googledorks.models_entity import EntityAttribute
total_attributes = EntityAttribute.objects.count()
print(f"\n✓ Total Attributes: {total_attributes}")

# Check relationships
from googledorks.models_entity import EntityRelationship
total_relationships = EntityRelationship.objects.count()
print(f"✓ Total Relationships: {total_relationships}")

# Check dorks
total_dorks = GoogleDork.objects.count()
print(f"\n✓ Total Google Dorks: {total_dorks}")

# Check execution_count field
sample_dork = GoogleDork.objects.first()
if sample_dork:
    has_execution_count = hasattr(sample_dork, 'execution_count')
    print(f"✓ GoogleDork has execution_count field: {has_execution_count}")
    if has_execution_count:
        print(f"   Sample execution_count: {sample_dork.execution_count}")

# Check UUID type
sample_entity = Entity.objects.first()
if sample_entity:
    print(f"\n✓ Entity ID type: {type(sample_entity.id).__name__}")
    print(f"   Sample ID: {sample_entity.id}")

print("\n" + "=" * 50)
print("✅ DATABASE STATUS CHECK COMPLETE")
print("=" * 50)

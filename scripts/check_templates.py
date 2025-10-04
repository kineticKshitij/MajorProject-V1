#!/usr/bin/env python
"""
Template syntax validation script for Django project
Run this to check all templates for syntax errors
"""

import os
import django
from django.conf import settings
from django.template import Template, Context, TemplateSyntaxError
from django.template.loader import get_template

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InformationExtractor.settings')
django.setup()

def check_template_syntax():
    """Check all templates for syntax errors"""
    template_dirs = [
        'googledorks/templates',
        'chatbot/templates', 
        'accounts/templates'
    ]
    
    errors_found = 0
    templates_checked = 0
    
    for template_dir in template_dirs:
        if os.path.exists(template_dir):
            for root, dirs, files in os.walk(template_dir):
                for file in files:
                    if file.endswith('.html'):
                        template_path = os.path.join(root, file)
                        relative_path = os.path.relpath(template_path)
                        
                        try:
                            with open(template_path, 'r', encoding='utf-8') as f:
                                template_content = f.read()
                            
                            # Try to compile the template
                            Template(template_content)
                            print(f"✅ {relative_path}")
                            templates_checked += 1
                            
                        except TemplateSyntaxError as e:
                            print(f"❌ {relative_path}: {e}")
                            errors_found += 1
                        except Exception as e:
                            print(f"⚠️  {relative_path}: {e}")
                            errors_found += 1
    
    print(f"\n📊 Summary:")
    print(f"Templates checked: {templates_checked}")
    print(f"Errors found: {errors_found}")
    
    if errors_found == 0:
        print("🎉 All templates are valid!")
    else:
        print(f"⚠️  Found {errors_found} template issues")

if __name__ == '__main__':
    check_template_syntax()
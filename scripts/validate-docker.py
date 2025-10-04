#!/usr/bin/env python3
"""
Docker Configuration Validator for Google Dorks Toolkit
Checks if all Docker-related files are properly configured
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and return status"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} (NOT FOUND)")
        return False

def check_file_content(file_path, required_content, description):
    """Check if file contains required content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            for requirement in required_content:
                if requirement not in content:
                    print(f"❌ {description}: Missing '{requirement}'")
                    return False
        print(f"✅ {description}: All requirements found")
        return True
    except Exception as e:
        print(f"❌ {description}: Error reading file - {e}")
        return False

def main():
    print("🔍 Google Dorks Toolkit - Docker Configuration Validator")
    print("========================================================")
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"📁 Current directory: {current_dir}")
    print()
    
    all_checks_passed = True
    
    # Required files
    files_to_check = [
        ("Dockerfile", "Docker build configuration"),
        ("docker-compose.yml", "Docker Compose (PostgreSQL)"),
        ("docker-compose.sqlite.yml", "Docker Compose (SQLite)"),
        (".dockerignore", "Docker ignore file"),
        ("requirements.txt", "Python dependencies"),
        ("manage.py", "Django management script"),
    ]
    
    print("📋 Checking required files:")
    for file_path, description in files_to_check:
        if not check_file_exists(file_path, description):
            all_checks_passed = False
    print()
    
    # Check Dockerfile content
    print("🔍 Validating Dockerfile content:")
    dockerfile_requirements = [
        "FROM python:",
        "WORKDIR /app",
        "COPY requirements.txt",
        "RUN pip install",
        "EXPOSE 8000"
    ]
    if not check_file_content("Dockerfile", dockerfile_requirements, "Dockerfile"):
        all_checks_passed = False
    print()
    
    # Check docker-compose.yml content
    print("🔍 Validating docker-compose.yml content:")
    compose_requirements = [
        "version:",
        "services:",
        "web:",
        "build: .",
        "ports:",
        "8000:8000"
    ]
    if not check_file_content("docker-compose.yml", compose_requirements, "docker-compose.yml"):
        all_checks_passed = False
    print()
    
    # Check requirements.txt content
    print("🔍 Validating requirements.txt content:")
    requirements_requirements = [
        "Django",
        "asgiref",
        "sqlparse"
    ]
    if not check_file_content("requirements.txt", requirements_requirements, "requirements.txt"):
        all_checks_passed = False
    print()
    
    # Final result
    print("=" * 56)
    if all_checks_passed:
        print("🎉 All Docker configuration checks PASSED!")
        print("📋 Your Docker setup is ready to use.")
        print()
        print("🚀 Next steps:")
        print("   1. Start Docker Desktop (if not running)")
        print("   2. Run: docker-compose -f docker-compose.sqlite.yml up --build")
        print("   3. Access: http://localhost:8000")
    else:
        print("❌ Some Docker configuration checks FAILED!")
        print("🔧 Please fix the issues above before proceeding.")
        sys.exit(1)

if __name__ == "__main__":
    main()
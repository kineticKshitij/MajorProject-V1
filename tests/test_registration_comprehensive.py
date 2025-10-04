#!/usr/bin/env python
"""
Comprehensive test suite for user registration functionality
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InformationExtractor.settings')
django.setup()

from accounts.forms import CustomUserCreationForm
from accounts.models import User, UserProfile
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

def test_registration_form():
    """Test registration form functionality"""
    print("🧪 Testing registration form...")
    
    # Clean up
    test_username = 'testform_user'
    test_email = 'testform@example.com'
    User.objects.filter(username=test_username).delete()
    User.objects.filter(email=test_email).delete()
    
    form_data = {
        'username': test_username,
        'first_name': 'Test',
        'last_name': 'Form',
        'email': test_email,
        'password1': 'complexpassword123!',
        'password2': 'complexpassword123!',
        'gemini_api_key': 'test-api-key-123'
    }
    
    form = CustomUserCreationForm(data=form_data)
    
    if form.is_valid():
        user = form.save()
        
        # Verify user creation
        assert user.username == test_username
        assert user.first_name == 'Test'
        assert user.last_name == 'Form'
        assert user.email == test_email
        assert user.gemini_api_key == 'test-api-key-123'
        
        # Verify profile creation
        assert hasattr(user, 'profile')
        assert user.profile is not None
        
        # Cleanup
        user.delete()
        print("✅ Registration form test PASSED")
        return True
    else:
        print(f"❌ Form validation failed: {form.errors}")
        return False

def test_duplicate_email():
    """Test duplicate email validation"""
    print("🧪 Testing duplicate email validation...")
    
    # Create first user
    test_email = 'duplicate@example.com'
    User.objects.filter(email=test_email).delete()
    
    user1 = User.objects.create_user(
        username='user1',
        email=test_email,
        password='password123'
    )
    
    # Try to create second user with same email
    form_data = {
        'username': 'user2',
        'first_name': 'Test',
        'last_name': 'User',
        'email': test_email,  # Duplicate email
        'password1': 'password123!',
        'password2': 'password123!',
    }
    
    form = CustomUserCreationForm(data=form_data)
    
    if not form.is_valid() and 'email' in form.errors:
        # Cleanup
        user1.delete()
        print("✅ Duplicate email validation test PASSED")
        return True
    else:
        user1.delete()
        print("❌ Duplicate email validation test FAILED")
        return False

def test_registration_view():
    """Test registration view functionality"""
    print("🧪 Testing registration view...")
    
    client = Client()
    test_username = 'testview_user'
    test_email = 'testview@example.com'
    
    # Clean up
    User.objects.filter(username=test_username).delete()
    User.objects.filter(email=test_email).delete()
    
    # Test GET request
    response = client.get(reverse('accounts:register'))
    assert response.status_code == 200
    
    # Test POST request with valid data
    post_data = {
        'username': test_username,
        'first_name': 'Test',
        'last_name': 'View',
        'email': test_email,
        'password1': 'complexpassword123!',
        'password2': 'complexpassword123!',
        'gemini_api_key': ''
    }
    
    response = client.post(reverse('accounts:register'), data=post_data)
    
    # Should redirect to login page after successful registration
    if response.status_code == 302:
        # Verify user was created
        try:
            user = User.objects.get(username=test_username)
            assert user.email == test_email
            assert hasattr(user, 'profile')
            
            # Cleanup
            user.delete()
            print("✅ Registration view test PASSED")
            return True
        except User.DoesNotExist:
            print("❌ User was not created")
            return False
    else:
        print(f"❌ Expected redirect, got status {response.status_code}")
        return False

def test_profile_auto_creation():
    """Test that profiles are automatically created"""
    print("🧪 Testing automatic profile creation...")
    
    test_username = 'testprofile_user'
    test_email = 'testprofile@example.com'
    
    # Clean up
    User.objects.filter(username=test_username).delete()
    User.objects.filter(email=test_email).delete()
    
    # Create user directly (not through form)
    user = User.objects.create_user(
        username=test_username,
        email=test_email,
        password='password123'
    )
    
    # Check if profile was created by signal
    try:
        profile = user.profile
        assert profile is not None
        
        # Cleanup
        user.delete()
        print("✅ Automatic profile creation test PASSED")
        return True
    except UserProfile.DoesNotExist:
        user.delete()
        print("❌ Profile was not automatically created")
        return False

def run_all_tests():
    """Run all registration tests"""
    print("🚀 Running comprehensive registration tests...\n")
    
    tests = [
        test_registration_form,
        test_duplicate_email,
        test_registration_view,
        test_profile_auto_creation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            failed += 1
        print()
    
    print(f"📊 Test Results:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
    
    if failed == 0:
        print("\n🎉 All tests PASSED! Registration functionality is working correctly.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review the issues above.")

if __name__ == '__main__':
    run_all_tests()
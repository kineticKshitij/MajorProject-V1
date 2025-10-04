#!/usr/bin/env python
"""
Test script to verify user registration functionality
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InformationExtractor.settings')
django.setup()

from accounts.forms import CustomUserCreationForm
from accounts.models import User, UserProfile

def test_registration():
    """Test user registration without conflicts"""
    
    # Clean up any test user that might exist
    test_username = 'testuser_registration'
    test_email = 'test@registration.com'
    
    # Delete test user if exists
    User.objects.filter(username=test_username).delete()
    User.objects.filter(email=test_email).delete()
    
    print("🧪 Testing user registration...")
    
    # Test form data
    form_data = {
        'username': test_username,
        'first_name': 'Test',
        'last_name': 'User',
        'email': test_email,
        'password1': 'testpassword123!',
        'password2': 'testpassword123!',
        'gemini_api_key': ''
    }
    
    # Create and validate form
    form = CustomUserCreationForm(data=form_data)
    
    if form.is_valid():
        print("✅ Form validation passed")
        
        # Save the user
        try:
            user = form.save()
            print(f"✅ User created: {user.username}")
            
            # Check if profile was created
            try:
                profile = user.profile
                print(f"✅ UserProfile created: {profile}")
                
                # Verify data
                assert user.first_name == 'Test'
                assert user.last_name == 'User'
                assert user.email == test_email
                print("✅ User data verified")
                
                # Clean up
                user.delete()
                print("✅ Test user cleaned up")
                
                print("\n🎉 Registration test PASSED!")
                return True
                
            except UserProfile.DoesNotExist:
                print("❌ UserProfile was not created")
                user.delete()
                return False
                
        except Exception as e:
            print(f"❌ Error saving user: {e}")
            return False
    else:
        print("❌ Form validation failed:")
        for field, errors in form.errors.items():
            print(f"  {field}: {errors}")
        return False

if __name__ == '__main__':
    test_registration()
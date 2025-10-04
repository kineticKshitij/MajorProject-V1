"""
Quick setup script to configure Gemini API key for the chatbot
Run this script to easily add your API key to the project
"""

import os
from pathlib import Path

def setup_gemini_api_key():
    print("=" * 60)
    print("🤖 Chatbot Configuration Setup")
    print("=" * 60)
    print()
    
    print("This script will help you configure the Gemini API key.")
    print()
    print("📝 Steps:")
    print("1. Get your API key from: https://makersuite.google.com/app/apikey")
    print("2. Paste it below")
    print("3. The script will save it to a .env file")
    print("4. Restart your Django server")
    print()
    
    api_key = input("Enter your Gemini API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Exiting.")
        return
    
    # Validate API key format (basic check)
    if len(api_key) < 20:
        print("⚠️  Warning: The API key seems too short. Please double-check it.")
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            print("❌ Setup cancelled.")
            return
    
    # Get project root (where manage.py is)
    project_root = Path(__file__).parent
    env_path = project_root / '.env'
    
    # Create or update .env file
    try:
        if env_path.exists():
            # Read existing .env
            with open(env_path, 'r') as f:
                lines = f.readlines()
            
            # Update existing GEMINI_API_KEY or add it
            found = False
            for i, line in enumerate(lines):
                if line.startswith('GEMINI_API_KEY='):
                    lines[i] = f'GEMINI_API_KEY={api_key}\n'
                    found = True
                    break
            
            if not found:
                lines.append(f'\nGEMINI_API_KEY={api_key}\n')
            
            # Write back
            with open(env_path, 'w') as f:
                f.writelines(lines)
            
            print(f"\n✅ Updated existing .env file: {env_path}")
        else:
            # Create new .env file
            with open(env_path, 'w') as f:
                f.write(f'GEMINI_API_KEY={api_key}\n')
                f.write('# Add other environment variables below\n')
            
            print(f"\n✅ Created new .env file: {env_path}")
        
        print()
        print("=" * 60)
        print("✅ Setup Complete!")
        print("=" * 60)
        print()
        print("📋 Next Steps:")
        print("1. Restart your Django server (Ctrl+C, then 'python manage.py runserver')")
        print("2. Refresh your browser at http://localhost:5174/chatbot")
        print("3. Start chatting!")
        print()
        print("🧪 To test the configuration:")
        print("   python manage.py shell")
        print("   >>> from django.conf import settings")
        print("   >>> print(f'Configured: {bool(settings.GEMINI_API_KEY)}')")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please add the API key manually to your .env file or settings.py")
        return

if __name__ == "__main__":
    setup_gemini_api_key()

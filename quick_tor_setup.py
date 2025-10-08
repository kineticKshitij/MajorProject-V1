#!/usr/bin/env python
"""
Quick Tor Automation Setup Script

This script will:
1. Backup your current services.py
2. Update BaseCrawler with Tor support
3. Enable Tor in .env (optional)
4. Test the automation

Usage:
    python quick_tor_setup.py
"""

import os
import shutil
from datetime import datetime

def backup_file(filepath):
    """Create backup of file"""
    if os.path.exists(filepath):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f"{filepath}.backup_{timestamp}"
        shutil.copy2(filepath, backup_path)
        print(f"✅ Backed up: {filepath} -> {backup_path}")
        return backup_path
    return None

def update_services_py():
    """Update socialcrawler/services.py with Tor support"""
    print("\n" + "=" * 70)
    print("📝 UPDATING CRAWLER SERVICES")
    print("=" * 70)
    
    services_path = 'socialcrawler/services.py'
    
    if not os.path.exists(services_path):
        print(f"❌ File not found: {services_path}")
        return False
    
    # Backup original
    backup_path = backup_file(services_path)
    
    print(f"\n📋 Instructions:")
    print(f"   1. Open: {services_path}")
    print(f"   2. Find: class BaseCrawler:")
    print(f"   3. Replace entire class with code from: socialcrawler/services_updated.py")
    print(f"   4. Update all crawler classes to pass use_tor parameter")
    print(f"\n💡 See socialcrawler/services_updated.py for complete example")
    print(f"💾 Backup saved at: {backup_path}")
    
    return True

def update_env_file():
    """Update .env file to enable Tor"""
    print("\n" + "=" * 70)
    print("🔧 UPDATING ENVIRONMENT CONFIGURATION")
    print("=" * 70)
    
    env_path = 'Cred/.env'
    
    if not os.path.exists(env_path):
        print(f"❌ File not found: {env_path}")
        return False
    
    # Read current .env
    with open(env_path, 'r') as f:
        content = f.read()
    
    # Check current status
    if 'TOR_ENABLED=true' in content:
        print("✅ Tor already enabled in .env")
        return True
    elif 'TOR_ENABLED=false' in content:
        print("ℹ️  Tor currently disabled in .env")
        print("\n📋 To enable Tor globally:")
        print(f"   1. Open: {env_path}")
        print(f"   2. Change: TOR_ENABLED=false")
        print(f"   3. To:     TOR_ENABLED=true")
        print(f"\n💡 Or keep disabled and use use_tor=True per crawler")
        return True
    else:
        print("⚠️  TOR_ENABLED not found in .env")
        return False

def check_tor_containers():
    """Check if Tor Docker containers are running"""
    print("\n" + "=" * 70)
    print("🐳 CHECKING DOCKER CONTAINERS")
    print("=" * 70)
    
    import subprocess
    
    try:
        result = subprocess.run(
            ['docker', 'ps', '--filter', 'name=tor', '--format', '{{.Names}}: {{.Status}}'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            output = result.stdout.strip()
            if output:
                print("✅ Tor containers running:")
                for line in output.split('\n'):
                    print(f"   {line}")
                return True
            else:
                print("❌ No Tor containers running")
                print("\n💡 Start containers:")
                print("   docker-compose -f docker-compose.tor.yml up -d")
                return False
        else:
            print("❌ Docker not available or error checking containers")
            return False
            
    except Exception as e:
        print(f"⚠️  Could not check Docker: {e}")
        print("\n💡 Manually start containers:")
        print("   docker-compose -f docker-compose.tor.yml up -d")
        return False

def main():
    print("=" * 70)
    print("🚀 TOR AUTOMATION SETUP")
    print("=" * 70)
    print("\nThis script will help you set up automatic Tor usage in crawlers.")
    print("\n📋 What this does:")
    print("   1. Backup your current services.py")
    print("   2. Show how to update BaseCrawler")
    print("   3. Check .env configuration")
    print("   4. Verify Tor containers are running")
    
    input("\nPress Enter to continue...")
    
    # Step 1: Update services.py
    update_services_py()
    
    # Step 2: Check .env
    update_env_file()
    
    # Step 3: Check Docker containers
    containers_ok = check_tor_containers()
    
    # Summary
    print("\n" + "=" * 70)
    print("📋 NEXT STEPS")
    print("=" * 70)
    
    print("\n1️⃣ Update BaseCrawler:")
    print("   • Open: socialcrawler/services.py")
    print("   • Replace BaseCrawler class with code from socialcrawler/services_updated.py")
    print("   • Update all crawler classes (Twitter, GitHub, LinkedIn, Reddit)")
    
    print("\n2️⃣ Choose Tor Mode:")
    print("   Option A: Global (all crawlers)")
    print("   • Set TOR_ENABLED=true in Cred/.env")
    print("   • All crawlers will use Tor by default")
    print("")
    print("   Option B: Per-crawler (selective)")
    print("   • Keep TOR_ENABLED=false in Cred/.env")
    print("   • Use use_tor=True when creating crawler")
    
    print("\n3️⃣ Start Tor Containers:")
    if not containers_ok:
        print("   • Run: docker-compose -f docker-compose.tor.yml up -d")
    else:
        print("   ✅ Already running!")
    
    print("\n4️⃣ Test Automation:")
    print("   • Run: python test_crawler_automation.py")
    
    print("\n" + "=" * 70)
    print("📚 DOCUMENTATION")
    print("=" * 70)
    print("   • Complete guide: docs/TOR_AUTOMATION_GUIDE.md")
    print("   • Updated code: socialcrawler/services_updated.py")
    print("   • Test script: test_crawler_automation.py")
    
    print("\n" + "=" * 70)
    print("✅ Setup information displayed!")
    print("=" * 70)
    print("\n💡 Read the instructions above and implement the changes.")
    print("💡 Or ask me to help implement specific steps!\n")

if __name__ == '__main__':
    main()

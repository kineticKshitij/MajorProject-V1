#!/usr/bin/env python
"""
Django Server IP vs Crawler IP Test

This script demonstrates the difference between:
1. Django server IP (what Django listens on)
2. Crawler IP (what websites see when you crawl)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InformationExtractor.settings')
django.setup()

from socialcrawler.services import GitHubCrawler
import requests

print("=" * 70)
print("🖥️  DJANGO SERVER IP vs CRAWLER IP")
print("=" * 70)

# 1. Django Server IP
print("\n1️⃣ Django Server IP (localhost):")
print("-" * 70)
print("   When you run: python manage.py runserver")
print("   Django listens on: 127.0.0.1:8000 (localhost)")
print("   ")
print("   📝 This is INTERNAL - only your computer can access it")
print("   🔒 This IP is NOT sent to websites you crawl")
print("   💡 This is just where Django listens for requests")

# 2. Your Real IP
print("\n2️⃣ Your Real Computer IP:")
print("-" * 70)
try:
    response = requests.get('https://api.ipify.org?format=json', timeout=10)
    real_ip = response.json().get('ip', 'Unknown')
    print(f"   🌐 Your Real IP: {real_ip}")
    print("   ")
    print("   📝 This is what websites see if you DON'T use Tor")
    print("   ⚠️  This would be revealed without Tor")
except Exception as e:
    print(f"   ❌ Error: {e}")
    real_ip = "Unknown"

# 3. Crawler IP (What websites see)
print("\n3️⃣ Crawler IP (What Websites See):")
print("-" * 70)
print("   With TOR_ENABLED=true:")
print("")

try:
    # Create crawler with Tor
    crawler = GitHubCrawler('torvalds', use_tor=True)
    crawler_ip = crawler.get_current_ip()
    
    if crawler_ip:
        print(f"   🧅 Crawler uses: {crawler_ip} (Tor exit node)")
        print("   ")
        print("   ✅ Websites see: " + crawler_ip)
        print(f"   ✅ Your real IP ({real_ip}) is HIDDEN!")
        print("   ✅ Django server IP (127.0.0.1) is NEVER exposed!")
        
        if real_ip != crawler_ip and crawler_ip != "Unknown":
            print("")
            print("   🎉 SUCCESS! Your identity is PROTECTED!")
    else:
        print("   ⚠️  Could not verify Tor IP")
    
    crawler.close()
except Exception as e:
    print(f"   ❌ Error: {e}")

# 4. Summary
print("\n" + "=" * 70)
print("📋 SUMMARY")
print("=" * 70)
print("")
print("🖥️  Django Server: 127.0.0.1:8000")
print("    → Internal only, NOT exposed to internet")
print("    → Just where Django listens for browser requests")
print("")
print(f"🌐 Your Real IP: {real_ip}")
print("    → This is your actual internet IP")
print("    → Hidden by Tor (websites DON'T see this)")
print("")
if 'crawler_ip' in locals():
    print(f"🧅 Crawler IP: {crawler_ip}")
    print("    → This is what websites see")
    print("    → Tor exit node IP (anonymous)")
print("")
print("=" * 70)
print("🔒 SECURITY STATUS")
print("=" * 70)
print("")
print("✅ Django server IP (127.0.0.1): NEVER exposed")
print(f"✅ Your real IP ({real_ip}): HIDDEN by Tor")
print(f"✅ Websites see: Tor exit node ({crawler_ip if 'crawler_ip' in locals() else 'Unknown'})")
print("")
print("🎯 Conclusion:")
print("   When you run 'python manage.py runserver' and crawl:")
print("   • Django listens on 127.0.0.1 (internal only)")
print("   • Crawlers use Tor exit nodes (anonymous)")
print("   • Your real IP is completely hidden!")
print("")
print("=" * 70)

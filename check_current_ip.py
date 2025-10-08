#!/usr/bin/env python
"""
Check Current IP - Shows what IP Django is using

This script checks:
1. Your real IP (without Tor)
2. Your Tor IP (with Tor - if enabled)
3. Verifies if Tor is actually being used
"""

import os
import django

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InformationExtractor.settings')
django.setup()

import requests
from django.conf import settings

print("=" * 70)
print("🔍 IP ADDRESS CHECK")
print("=" * 70)

# Check 1: Real IP (without Tor)
print("\n1️⃣ Your REAL IP (without Tor):")
print("-" * 70)
try:
    response = requests.get('https://api.ipify.org?format=json', timeout=10)
    real_ip = response.json().get('ip', 'Unknown')
    print(f"   🌐 Real IP: {real_ip}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Check 2: Tor status
print("\n2️⃣ Tor Configuration:")
print("-" * 70)
print(f"   TOR_ENABLED: {settings.TOR_ENABLED}")
print(f"   TOR_PROXY_HOST: {settings.TOR_PROXY_HOST}")
print(f"   TOR_PROXY_PORT: {settings.TOR_PROXY_PORT}")

# Check 3: Tor IP (if Tor is available)
print("\n3️⃣ Your TOR IP (if Tor is running):")
print("-" * 70)
try:
    from googledorks.services.tor_service import TorProxyService, anonymous_get
    
    # Test Tor connection
    tor = TorProxyService()
    result = tor.verify_tor_connection()
    
    if result['success']:
        print(f"   ✅ Tor is WORKING!")
        print(f"   🧅 Tor Exit IP: {result['exit_ip']}")
        print(f"   🔒 Your IP is HIDDEN through Tor")
        
        # Compare
        if real_ip != result['exit_ip']:
            print(f"\n   ✅ CONFIRMED: Using different IP through Tor!")
            print(f"      Real IP:  {real_ip}")
            print(f"      Tor IP:   {result['exit_ip']}")
        else:
            print(f"\n   ⚠️  WARNING: IPs are the same - Tor may not be working properly")
    else:
        print(f"   ❌ Tor is NOT working: {result.get('error', 'Unknown error')}")
        print(f"   💡 Make sure Docker containers are running:")
        print(f"      docker-compose -f docker-compose.tor.yml up -d")
        
except ImportError as e:
    print(f"   ❌ Tor service not available: {e}")
except Exception as e:
    print(f"   ❌ Error checking Tor: {e}")

# Check 4: Django server IP
print("\n4️⃣ Django Server Status:")
print("-" * 70)
print(f"   🖥️  Django uses REAL IP by default")
print(f"   📝 To use Tor, you must explicitly call:")
print(f"      • anonymous_get(url)")
print(f"      • TorProxyService().request_with_retry(url)")

print("\n" + "=" * 70)
print("📋 SUMMARY")
print("=" * 70)

if settings.TOR_ENABLED:
    print("⚠️  TOR_ENABLED=True but crawlers not yet integrated")
    print("💡 Use anonymous_get() manually for Tor requests")
else:
    print("ℹ️  TOR_ENABLED=False - All requests use your real IP")
    print("💡 To enable: Set TOR_ENABLED=true in .env")

print("\n🎯 Next Steps:")
print("   1. Keep TOR_ENABLED=false for normal development")
print("   2. Use anonymous_get() when you need anonymity")
print("   3. Or complete crawler integration (Todos #2-4)")
print("=" * 70)

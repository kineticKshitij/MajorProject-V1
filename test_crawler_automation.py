#!/usr/bin/env python
"""
Test Crawler Tor Automation

This script tests if crawlers automatically use Tor when enabled.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InformationExtractor.settings')
django.setup()

from socialcrawler.services import TwitterCrawler, GitHubCrawler, LinkedInCrawler, RedditCrawler
from django.conf import settings
import requests

def test_crawler_automation():
    print("=" * 70)
    print("🧪 TESTING CRAWLER TOR AUTOMATION")
    print("=" * 70)
    
    # Test 1: Check real IP
    print("\n1️⃣ Your REAL IP (without Tor):")
    print("-" * 70)
    real_ip = "Unknown"
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=10)
        real_ip = response.json().get('ip', 'Unknown')
        print(f"   🌐 Real IP: {real_ip}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Settings check
    print("\n2️⃣ Django Settings:")
    print("-" * 70)
    tor_enabled = getattr(settings, 'TOR_ENABLED', False)
    print(f"   TOR_ENABLED: {tor_enabled}")
    print(f"   TOR_PROXY_HOST: {getattr(settings, 'TOR_PROXY_HOST', 'N/A')}")
    print(f"   TOR_PROXY_PORT: {getattr(settings, 'TOR_PROXY_PORT', 'N/A')}")
    
    # Test 3: Crawler with Tor DISABLED
    print("\n3️⃣ Test Crawler with Tor=False:")
    print("-" * 70)
    try:
        crawler = TwitterCrawler('elonmusk', use_tor=False)
        print(f"   Crawler created for: @{crawler.username}")
        print(f"   use_tor: {crawler.use_tor}")
        print(f"   tor_service: {'Enabled' if hasattr(crawler, 'tor_service') and crawler.tor_service else 'Disabled'}")
        print(f"   ✅ Crawler will use REAL IP: {real_ip}")
        crawler.close()
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Crawler with Tor ENABLED
    print("\n4️⃣ Test Crawler with Tor=True:")
    print("-" * 70)
    try:
        crawler = TwitterCrawler('elonmusk', use_tor=True)
        print(f"   Crawler created for: @{crawler.username}")
        print(f"   use_tor: {crawler.use_tor}")
        
        if hasattr(crawler, 'tor_service') and crawler.tor_service:
            print(f"   🧅 tor_service: Active")
            
            # Verify Tor connection
            result = crawler.tor_service.verify_tor_connection()
            if result.get('success'):
                tor_ip = result.get('exit_ip', 'Unknown')
                print(f"   🎯 Tor Exit IP: {tor_ip}")
                
                if tor_ip != real_ip and tor_ip != 'Unknown':
                    print(f"\n   ✅✅✅ SUCCESS! Crawler is using TOR!")
                    print(f"   🔒 Your IP is HIDDEN: {real_ip} → {tor_ip}")
                else:
                    print(f"\n   ⚠️  WARNING: IPs are the same or unknown")
            else:
                print(f"   ❌ Tor verification failed: {result.get('error', 'Unknown error')}")
        else:
            print(f"   ❌ tor_service: Not initialized")
            print(f"   💡 Make sure Tor containers are running:")
            print(f"      docker-compose -f docker-compose.tor.yml up -d")
        
        crawler.close()
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 5: Auto-detection (when use_tor=None, should use TOR_ENABLED setting)
    print("\n5️⃣ Test Auto-detection (use_tor=None):")
    print("-" * 70)
    print(f"   Current TOR_ENABLED setting: {tor_enabled}")
    try:
        crawler = TwitterCrawler('elonmusk', use_tor=None)
        print(f"   Auto-detected use_tor: {crawler.use_tor}")
        
        if tor_enabled:
            if crawler.use_tor:
                print(f"   ✅ Correct! Auto-enabled Tor based on settings")
            else:
                print(f"   ⚠️  Expected Tor enabled but got disabled")
        else:
            if not crawler.use_tor:
                print(f"   ✅ Correct! Tor disabled as per settings")
            else:
                print(f"   ⚠️  Expected Tor disabled but got enabled")
        
        crawler.close()
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: Test all crawler types
    print("\n6️⃣ Test All Crawler Types:")
    print("-" * 70)
    crawlers = [
        ('Twitter', TwitterCrawler, 'elonmusk'),
        ('GitHub', GitHubCrawler, 'torvalds'),
        ('LinkedIn', LinkedInCrawler, 'billgates'),
        ('Reddit', RedditCrawler, 'spez')
    ]
    
    for platform, CrawlerClass, username in crawlers:
        try:
            crawler = CrawlerClass(username, use_tor=True)
            has_tor = hasattr(crawler, 'tor_service') and crawler.tor_service is not None
            print(f"   {platform:10} - use_tor={crawler.use_tor} - tor_service={'✅' if has_tor else '❌'}")
            crawler.close()
        except Exception as e:
            print(f"   {platform:10} - ❌ Error: {str(e)[:50]}")
    
    # Summary
    print("\n" + "=" * 70)
    print("📋 SUMMARY")
    print("=" * 70)
    
    if tor_enabled:
        print("⚠️  TOR_ENABLED=True in settings")
        print("💡 All crawlers will use Tor by default (when use_tor=None)")
        print("🎯 To disable Tor for specific crawler: use_tor=False")
    else:
        print("ℹ️  TOR_ENABLED=False in settings")
        print("💡 Crawlers use real IP by default (when use_tor=None)")
        print("🎯 To enable Tor for specific crawler: use_tor=True")
    
    print("\n🔧 Next Steps:")
    print("   1. Update BaseCrawler in socialcrawler/services.py")
    print("   2. Add use_tor parameter support to all crawlers")
    print("   3. Set TOR_ENABLED=true in .env to enable globally")
    print("   4. Or use use_tor=True for individual crawlers")
    print("=" * 70)

if __name__ == '__main__':
    test_crawler_automation()

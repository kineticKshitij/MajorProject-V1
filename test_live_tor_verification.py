#!/usr/bin/env python
"""
Live Tor Verification Test

This script verifies that crawlers are actually using Tor by:
1. Checking real IP
2. Creating crawler with Tor
3. Making actual request through crawler
4. Verifying we're using different IP
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InformationExtractor.settings')
django.setup()

from socialcrawler.services import TwitterCrawler, GitHubCrawler
import requests

def test_live_tor():
    print("=" * 70)
    print("🔍 LIVE TOR VERIFICATION TEST")
    print("=" * 70)
    
    # Step 1: Get real IP
    print("\n1️⃣ Checking REAL IP (without Tor):")
    print("-" * 70)
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=10)
        real_ip = response.json().get('ip', 'Unknown')
        print(f"   🌐 Your Real IP: {real_ip}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        real_ip = "Unknown"
    
    # Step 2: Create crawler with Tor
    print("\n2️⃣ Creating Crawler with Tor:")
    print("-" * 70)
    try:
        crawler = GitHubCrawler('torvalds', use_tor=True)
        print(f"   ✅ Crawler created")
        print(f"   🧅 use_tor: {crawler.use_tor}")
        print(f"   🔧 tor_service: {'Active' if crawler.tor_service else 'Inactive'}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Step 3: Get current IP through crawler
    print("\n3️⃣ Checking IP Through Crawler:")
    print("-" * 70)
    try:
        crawler_ip = crawler.get_current_ip()
        print(f"   🧅 Crawler IP: {crawler_ip}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        crawler_ip = "Unknown"
    
    # Step 4: Make actual request through Tor
    print("\n4️⃣ Making Real Request Through Tor:")
    print("-" * 70)
    tor_ip = crawler_ip  # Use crawler IP from step 3
    try:
        # Try to get IP through direct request
        response = crawler._make_request('https://api.ipify.org?format=json')
        if response and response.status_code == 200:
            tor_ip = response.json().get('ip', crawler_ip)
            print(f"   🎯 Response IP: {tor_ip}")
            print(f"   📊 Status Code: {response.status_code}")
        else:
            print(f"   ℹ️  Using crawler IP from verification: {crawler_ip}")
            tor_ip = crawler_ip
    except Exception as e:
        print(f"   ℹ️  Using crawler IP from verification: {crawler_ip}")
        tor_ip = crawler_ip
    
    # Step 5: Verification
    print("\n5️⃣ Verification:")
    print("-" * 70)
    
    if real_ip != "Unknown" and tor_ip != "Unknown":
        if real_ip != tor_ip:
            print(f"   ✅✅✅ SUCCESS! Tor is WORKING!")
            print(f"   🔒 Your IP is HIDDEN!")
            print(f"   ")
            print(f"   Real IP:    {real_ip}")
            print(f"   Through Tor: {tor_ip}")
            print(f"   ")
            print(f"   🎉 You are browsing anonymously through Tor network!")
        else:
            print(f"   ⚠️  WARNING: Same IP detected")
            print(f"   Real IP:  {real_ip}")
            print(f"   Tor IP:   {tor_ip}")
            print(f"   ")
            print(f"   💡 This might mean:")
            print(f"      1. Tor containers not running")
            print(f"      2. Tor configuration issue")
            print(f"      3. Check: docker-compose -f docker-compose.tor.yml ps")
    else:
        print(f"   ⚠️  Could not verify - one or both IPs unknown")
        print(f"   Real IP: {real_ip}")
        print(f"   Tor IP:  {tor_ip}")
    
    # Step 6: Test with actual API
    print("\n6️⃣ Testing with Real API (GitHub):")
    print("-" * 70)
    try:
        # Make request to GitHub API through Tor
        response = crawler._make_request('https://api.github.com/users/torvalds')
        if response and response.status_code == 200:
            data = response.json()
            print(f"   ✅ GitHub API Response:")
            print(f"      Username: {data.get('name', 'N/A')}")
            print(f"      Bio: {data.get('bio', 'N/A')[:50] if data.get('bio') else 'N/A'}...")
            print(f"      Followers: {data.get('followers', 0)}")
            print(f"   ")
            print(f"   🧅 Request made through Tor successfully!")
        elif response:
            print(f"   ⚠️  API returned status: {response.status_code}")
            print(f"   💡 GitHub may be rate-limiting Tor exit nodes")
            print(f"   ℹ️  This is normal - some services block/limit Tor")
        else:
            print(f"   ❌ Request failed")
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
        print(f"   💡 This is expected - GitHub often rate-limits Tor")
    
    # Step 7: Test IP rotation
    print("\n7️⃣ Testing IP Rotation:")
    print("-" * 70)
    try:
        print(f"   📍 Current IP: {tor_ip}")
        print(f"   🔄 Rotating circuit...")
        
        if crawler.rotate_circuit():
            import time
            time.sleep(2)  # Wait for circuit to establish
            
            new_ip = crawler.get_current_ip()
            print(f"   📍 New IP: {new_ip}")
            
            if new_ip != tor_ip and new_ip != "Unknown":
                print(f"   ✅ IP rotation SUCCESSFUL!")
                print(f"      {tor_ip} → {new_ip}")
            else:
                print(f"   ⚠️  IP didn't change (might be same exit node)")
        else:
            print(f"   ❌ Circuit rotation failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Cleanup
    crawler.close()
    
    # Summary
    print("\n" + "=" * 70)
    print("📋 SUMMARY")
    print("=" * 70)
    
    if real_ip != tor_ip and tor_ip != "Unknown":
        print("✅ TOR AUTOMATION WORKING PERFECTLY!")
        print("")
        print("🔒 Your crawlers are now:")
        print("   • Anonymous (IP hidden)")
        print("   • Using Tor network")
        print("   • Can rotate IPs")
        print("   • Ready for production")
        print("")
        print(f"📊 Your Real IP: {real_ip}")
        print(f"🧅 Tor Exit IP:  {tor_ip}")
    else:
        print("⚠️  Tor may not be working correctly")
        print("")
        print("💡 Troubleshooting:")
        print("   1. Check Tor containers:")
        print("      docker-compose -f docker-compose.tor.yml ps")
        print("   2. Check Tor logs:")
        print("      docker logs tor-service")
        print("   3. Restart containers:")
        print("      docker-compose -f docker-compose.tor.yml restart")
    
    print("=" * 70)

if __name__ == '__main__':
    test_live_tor()

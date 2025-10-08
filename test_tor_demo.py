"""
Quick demo showing Tor anonymity is working
"""
import os
import django

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InformationExtractor.settings')
django.setup()

from googledorks.services.tor_service import TorProxyService

print("\n" + "="*70)
print("🧅 TOR ANONYMITY DEMONSTRATION")
print("="*70)

# Initialize Tor
tor = TorProxyService()

# Verify Tor connection
print("\n📡 Checking Tor connection...")
result = tor.verify_tor_connection()

if result['is_tor']:
    print(f"\n✅ SUCCESS! Your IP is HIDDEN through Tor network!")
    print(f"🌍 Anonymous Exit IP: {result['ip']}")
    print(f"\n💡 Websites will see: {result['ip']} (Tor exit node)")
    print(f"💡 They will NOT see: Your real IP address")
    
    # Show circuit rotation
    print(f"\n🔄 Testing circuit rotation (changing IP)...")
    old_ip = result['ip']
    
    # Renew circuit
    tor.renew_circuit(wait_time=5)
    
    # Get new IP
    import time
    time.sleep(2)
    new_result = tor.verify_tor_connection()
    new_ip = new_result['ip']
    
    print(f"   Old Exit IP: {old_ip}")
    print(f"   New Exit IP: {new_ip}")
    
    if old_ip != new_ip:
        print(f"\n   ✅ IP rotation successful! Using different Tor exit node.")
    else:
        print(f"\n   ℹ️  Same IP (circuit may need more time to change)")
    
    print("\n" + "="*70)
    print("✅ TOR ANONYMITY IS WORKING!")
    print("="*70)
    print("\n📌 Your crawlers and dorks can now use Tor for:")
    print("   • Hiding your real IP address")
    print("   • Rotating IPs automatically")
    print("   • Bypassing geographic restrictions")
    print("   • Avoiding IP-based rate limits")
    
else:
    print(f"\n❌ Not using Tor: {result['message']}")

print("\n")

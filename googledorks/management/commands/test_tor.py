"""
Test Tor proxy connection and IP rotation

This management command tests the Tor integration by:
1. Verifying Tor connection
2. Checking current exit IP
3. Rotating circuit
4. Verifying new IP
5. Displaying circuit information

Usage:
    python manage.py test_tor
    python manage.py test_tor --rotations 3
"""

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from googledorks.services.tor_service import TorProxyService
import time


class Command(BaseCommand):
    help = 'Test Tor proxy connection and IP rotation'

    def add_arguments(self, parser):
        parser.add_argument(
            '--rotations',
            type=int,
            default=2,
            help='Number of circuit rotations to test (default: 2)',
        )
        parser.add_argument(
            '--delay',
            type=int,
            default=5,
            help='Delay between rotations in seconds (default: 5)',
        )

    def handle(self, *args, **options):
        rotations = options['rotations']
        delay = options['delay']
        
        self.stdout.write(self.style.HTTP_INFO("=" * 70))
        self.stdout.write(self.style.HTTP_INFO("🧅 TOR PROXY CONNECTION TEST"))
        self.stdout.write(self.style.HTTP_INFO("=" * 70))
        self.stdout.write("")
        
        # Check if Tor is enabled in settings
        tor_enabled = getattr(settings, 'TOR_ENABLED', False)
        if not tor_enabled:
            self.stdout.write(
                self.style.WARNING(
                    "⚠️  TOR_ENABLED is False in settings. "
                    "Set TOR_ENABLED=true in .env to enable Tor."
                )
            )
            self.stdout.write("")
        
        # Initialize Tor service
        try:
            tor = TorProxyService()
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ TorProxyService initialized: "
                    f"{tor.proxy_host}:{tor.proxy_port}"
                )
            )
            self.stdout.write("")
        except Exception as e:
            raise CommandError(f"Failed to initialize TorProxyService: {e}")
        
        # Test 1: Verify Tor connection
        self.stdout.write(self.style.HTTP_INFO("📡 Test 1: Verifying Tor Connection"))
        self.stdout.write("-" * 70)
        
        result = tor.verify_tor_connection()
        
        if result['success']:
            if result['is_tor']:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅ SUCCESS: Connected through Tor network!"
                    )
                )
                self.stdout.write(f"   Exit IP: {result['ip']}")
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f"❌ FAILED: Connection NOT routed through Tor!"
                    )
                )
                self.stdout.write(f"   Current IP: {result['ip']}")
                self.stdout.write(
                    self.style.WARNING(
                        "\n   Troubleshooting:\n"
                        "   1. Check if Tor service is running: docker ps\n"
                        "   2. Start Tor: docker-compose -f docker-compose.tor.yml up -d\n"
                        "   3. Check Tor logs: docker logs tor-service\n"
                    )
                )
                return
        else:
            self.stdout.write(
                self.style.ERROR(
                    f"❌ FAILED: {result['message']}"
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    "\n   Troubleshooting:\n"
                    "   1. Check if Tor container is running:\n"
                    "      docker-compose -f docker-compose.tor.yml ps\n"
                    "   2. Start Tor service:\n"
                    "      docker-compose -f docker-compose.tor.yml up -d\n"
                    "   3. Check Tor connection:\n"
                    "      curl --socks5-hostname localhost:9050 https://check.torproject.org/\n"
                )
            )
            return
        
        self.stdout.write("")
        
        # Test 2: IP rotation
        self.stdout.write(self.style.HTTP_INFO(f"🔄 Test 2: IP Rotation ({rotations} rotations)"))
        self.stdout.write("-" * 70)
        
        ips = []
        for i in range(rotations + 1):
            if i == 0:
                self.stdout.write(f"Initial IP:")
            else:
                self.stdout.write(f"\nRotation {i}:")
                self.stdout.write(f"  Renewing circuit...")
                
                if tor.renew_circuit(wait_time=delay):
                    self.stdout.write(
                        self.style.SUCCESS("  ✅ Circuit renewed")
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR("  ❌ Circuit renewal failed")
                    )
                    self.stdout.write(
                        self.style.WARNING(
                            "  Note: Circuit rotation requires 'stem' library.\n"
                            "  Install: pip install stem"
                        )
                    )
            
            # Get current IP
            self.stdout.write(f"  Fetching exit IP...")
            ip = tor.get_current_ip()
            
            if ip:
                ips.append(ip)
                self.stdout.write(f"  Exit IP: {self.style.SUCCESS(ip)}")
            else:
                self.stdout.write(self.style.ERROR("  ❌ Failed to get IP"))
        
        self.stdout.write("")
        self.stdout.write(self.style.HTTP_INFO("📊 IP Rotation Summary"))
        self.stdout.write("-" * 70)
        
        if len(ips) > 1:
            unique_ips = len(set(ips))
            self.stdout.write(f"Total IPs observed: {len(ips)}")
            self.stdout.write(f"Unique IPs: {unique_ips}")
            self.stdout.write(f"IP diversity: {unique_ips / len(ips) * 100:.1f}%")
            
            if unique_ips > 1:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"\n✅ IP rotation working! Used {unique_ips} different exit nodes."
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        "\n⚠️  All IPs were the same. Circuit rotation may not be working."
                    )
                )
            
            self.stdout.write(f"\nIPs used:")
            for idx, ip in enumerate(ips, 1):
                self.stdout.write(f"  {idx}. {ip}")
        
        self.stdout.write("")
        
        # Test 3: Circuit information
        self.stdout.write(self.style.HTTP_INFO("🔍 Test 3: Circuit Information"))
        self.stdout.write("-" * 70)
        
        circuit_info = tor.get_circuit_info()
        
        if circuit_info and circuit_info.get('success'):
            circuits = circuit_info['circuits']
            self.stdout.write(f"Active circuits: {len(circuits)}")
            
            for idx, circuit in enumerate(circuits[:5], 1):  # Show first 5
                self.stdout.write(f"\nCircuit {idx}:")
                self.stdout.write(f"  ID: {circuit['id']}")
                self.stdout.write(f"  Status: {circuit['status']}")
                self.stdout.write(f"  Purpose: {circuit['purpose']}")
                self.stdout.write(f"  Path: ", ending='')
                
                path_str = " → ".join([
                    f"{node['nickname']} ({node['fingerprint']})"
                    for node in circuit['path']
                ])
                self.stdout.write(path_str)
        else:
            self.stdout.write(
                self.style.WARNING(
                    "⚠️  Circuit information not available.\n"
                    "   Requires 'stem' library: pip install stem"
                )
            )
        
        self.stdout.write("")
        
        # Test 4: Statistics
        self.stdout.write(self.style.HTTP_INFO("📈 Test 4: Usage Statistics"))
        self.stdout.write("-" * 70)
        
        stats = tor.get_statistics()
        self.stdout.write(f"Circuit renewals: {stats['circuit_renewals']}")
        self.stdout.write(f"Unique IPs used: {stats['unique_ips_used']}")
        self.stdout.write(f"Stem available: {stats['stem_available']}")
        self.stdout.write(f"Proxy config: {stats['proxy_config']}")
        
        self.stdout.write("")
        self.stdout.write(self.style.HTTP_INFO("=" * 70))
        self.stdout.write(
            self.style.SUCCESS(
                "✅ TOR INTEGRATION TEST COMPLETE"
            )
        )
        self.stdout.write(self.style.HTTP_INFO("=" * 70))
        self.stdout.write("")
        
        # Next steps
        self.stdout.write(self.style.HTTP_INFO("📋 Next Steps:"))
        self.stdout.write("")
        self.stdout.write("1. Install stem library for full functionality:")
        self.stdout.write("   pip install stem")
        self.stdout.write("")
        self.stdout.write("2. Test anonymous scraping:")
        self.stdout.write("   from googledorks.services.tor_service import anonymous_get")
        self.stdout.write("   response = anonymous_get('https://api.github.com/users/torvalds')")
        self.stdout.write("")
        self.stdout.write("3. Use in crawlers:")
        self.stdout.write("   crawler = GitHubCrawler(username='torvalds', use_tor=True)")
        self.stdout.write("")

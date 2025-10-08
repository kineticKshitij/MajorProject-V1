"""
Tor Proxy Service for Anonymous Web Scraping

This service manages Tor proxy connections, circuit rotation,
and anonymous HTTP requests through the Tor network.

Features:
- SOCKS5 proxy configuration
- Automatic circuit rotation
- IP address verification
- Request retry with fallback
- Circuit health monitoring

Author: Information Extractor Team
Date: October 2025
"""

import socket
import time
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

import requests
from django.conf import settings

# Optional: Stem for Tor control (install: pip install stem)
try:
    from stem import Signal
    from stem.control import Controller
    STEM_AVAILABLE = True
except ImportError:
    STEM_AVAILABLE = False
    logging.warning("Stem library not available. Circuit rotation features disabled.")

logger = logging.getLogger(__name__)


class TorProxyService:
    """
    Service for managing Tor proxy connections and circuit rotation
    
    Usage:
        tor = TorProxyService()
        
        # Verify Tor connection
        result = tor.verify_tor_connection()
        print(result)
        
        # Make anonymous request
        response = tor.request_with_retry('https://api.github.com/users/torvalds')
        
        # Rotate IP
        tor.renew_circuit()
        new_ip = tor.get_current_ip()
    """
    
    def __init__(
        self,
        proxy_host: Optional[str] = None,
        proxy_port: Optional[int] = None,
        control_port: Optional[int] = None,
        control_password: Optional[str] = None
    ):
        """
        Initialize Tor proxy service
        
        Args:
            proxy_host: Tor proxy hostname (default from settings)
            proxy_port: Tor SOCKS proxy port (default from settings)
            control_port: Tor control port (default from settings)
            control_password: Tor control password (default from settings)
        """
        # Use 127.0.0.1 instead of localhost for Stem compatibility
        default_host = getattr(settings, 'TOR_PROXY_HOST', 'localhost')
        self.proxy_host = proxy_host or default_host
        # Convert localhost to 127.0.0.1 for Stem
        if self.proxy_host == 'localhost':
            self.control_host = '127.0.0.1'
        else:
            self.control_host = self.proxy_host
            
        self.proxy_port = proxy_port or getattr(settings, 'TOR_PROXY_PORT', 9050)
        self.control_port = control_port or getattr(settings, 'TOR_CONTROL_PORT', 9051)
        self.control_password = control_password or getattr(settings, 'TOR_CONTROL_PASSWORD', '')
        
        self.session = None
        self.last_circuit_renewal = None
        self.circuit_renewal_count = 0
        self.used_ips: List[str] = []
        
        logger.info(
            f"TorProxyService initialized: {self.proxy_host}:{self.proxy_port}"
        )
    
    def get_session(self, force_new: bool = False) -> requests.Session:
        """
        Get or create a requests session configured for Tor
        
        Args:
            force_new: Force creation of new session
            
        Returns:
            Configured requests.Session object
        """
        if self.session is None or force_new:
            self.session = requests.Session()
            
            # Configure SOCKS5 proxy
            # socks5h means DNS resolution through Tor (prevents leaks)
            self.session.proxies = {
                'http': f'socks5h://{self.proxy_host}:{self.proxy_port}',
                'https': f'socks5h://{self.proxy_host}:{self.proxy_port}'
            }
            
            # Set reasonable timeout
            self.session.timeout = 30
            
            # Set Tor Browser-like user agent
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
            })
            
            logger.info("New Tor session created")
            
        return self.session
    
    def renew_circuit(self, wait_time: int = 5) -> bool:
        """
        Request new Tor circuit (change exit node/IP)
        
        Args:
            wait_time: Seconds to wait after renewal for circuit to establish
            
        Returns:
            True if successful, False otherwise
        """
        if not STEM_AVAILABLE:
            logger.warning("Stem library not available. Cannot renew circuit.")
            return False
        
        try:
            with Controller.from_port(
                address=self.control_host,  # Use control_host for Stem
                port=self.control_port
            ) as controller:
                controller.authenticate(password=self.control_password)
                controller.signal(Signal.NEWNYM)
                
                self.last_circuit_renewal = datetime.now()
                self.circuit_renewal_count += 1
                
                logger.info(
                    f"Tor circuit renewed successfully "
                    f"(renewal #{self.circuit_renewal_count})"
                )
                
                # Wait for circuit to establish
                if wait_time > 0:
                    logger.debug(f"Waiting {wait_time}s for circuit to establish...")
                    time.sleep(wait_time)
                
                return True
                
        except Exception as e:
            logger.error(f"Failed to renew Tor circuit: {e}")
            return False
    
    def get_current_ip(self) -> Optional[str]:
        """
        Get current exit node IP address
        
        Returns:
            Current IP address or None if failed
        """
        try:
            session = self.get_session()
            response = session.get('https://api.ipify.org?format=json', timeout=15)
            
            if response.status_code == 200:
                ip = response.json().get('ip')
                logger.info(f"Current Tor exit IP: {ip}")
                
                # Track used IPs
                if ip and ip not in self.used_ips:
                    self.used_ips.append(ip)
                
                return ip
            else:
                logger.error(f"Failed to get IP: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting current IP: {e}")
            return None
    
    def verify_tor_connection(self) -> Dict[str, Any]:
        """
        Verify Tor connection is working
        
        Returns:
            Dict with status and details:
            {
                'success': bool,
                'is_tor': bool,
                'ip': str,
                'message': str
            }
        """
        try:
            session = self.get_session()
            
            # Check Tor Project verification endpoint
            response = session.get(
                'https://check.torproject.org/api/ip',
                timeout=20
            )
            
            if response.status_code == 200:
                data = response.json()
                is_tor = data.get('IsTor', False)
                ip = data.get('IP', 'Unknown')
                
                if is_tor:
                    logger.info(f"✅ Tor connection verified! Exit IP: {ip}")
                    message = f"✅ Connected through Tor network. Exit IP: {ip}"
                else:
                    logger.warning(f"⚠️ Not using Tor! Current IP: {ip}")
                    message = f"⚠️ Connection NOT routed through Tor. IP: {ip}"
                
                return {
                    'success': True,
                    'is_tor': is_tor,
                    'ip': ip,
                    'message': message
                }
            else:
                return {
                    'success': False,
                    'is_tor': False,
                    'ip': 'Unknown',
                    'message': f'Verification failed: HTTP {response.status_code}'
                }
                
        except requests.exceptions.ProxyError as e:
            logger.error(f"Tor proxy connection failed: {e}")
            return {
                'success': False,
                'is_tor': False,
                'ip': 'Unknown',
                'message': f'Proxy connection failed. Is Tor running? Error: {str(e)}'
            }
        except requests.exceptions.Timeout:
            logger.error("Tor connection timeout")
            return {
                'success': False,
                'is_tor': False,
                'ip': 'Unknown',
                'message': 'Connection timeout. Tor network may be slow or unavailable.'
            }
        except Exception as e:
            logger.error(f"Tor verification failed: {e}")
            return {
                'success': False,
                'is_tor': False,
                'ip': 'Unknown',
                'message': f'Verification error: {str(e)}'
            }
    
    def request_with_retry(
        self,
        url: str,
        method: str = 'GET',
        max_retries: int = 3,
        rotate_on_fail: bool = True,
        delay_between_retries: int = 2,
        **kwargs
    ) -> Optional[requests.Response]:
        """
        Make HTTP request through Tor with retry and circuit rotation
        
        Args:
            url: Target URL
            method: HTTP method (GET, POST, etc.)
            max_retries: Maximum retry attempts
            rotate_on_fail: Rotate circuit on failure
            delay_between_retries: Seconds to wait between retries
            **kwargs: Additional arguments for requests (headers, data, etc.)
            
        Returns:
            Response object or None if all retries failed
        """
        session = self.get_session()
        last_error = None
        
        for attempt in range(max_retries):
            try:
                logger.debug(
                    f"Request attempt {attempt + 1}/{max_retries}: "
                    f"{method} {url}"
                )
                
                response = session.request(method, url, **kwargs)
                
                # Success
                if response.status_code == 200:
                    logger.info(
                        f"✅ Request successful: {method} {url} "
                        f"(status: {response.status_code})"
                    )
                    return response
                
                # Rate limited or blocked
                elif response.status_code in [429, 403]:
                    logger.warning(
                        f"⚠️ Rate limited/blocked: {response.status_code} - {url}"
                    )
                    last_error = f"HTTP {response.status_code}"
                    
                    # Rotate circuit and retry
                    if rotate_on_fail and attempt < max_retries - 1:
                        logger.info("Rotating Tor circuit due to rate limit...")
                        self.renew_circuit(wait_time=5)
                
                # Other HTTP error
                else:
                    logger.warning(
                        f"Request failed: {response.status_code} - {url}"
                    )
                    last_error = f"HTTP {response.status_code}"
                    
                    if rotate_on_fail and attempt < max_retries - 1:
                        self.renew_circuit(wait_time=3)
                    
            except requests.exceptions.ProxyError as e:
                logger.error(f"Proxy error on attempt {attempt + 1}: {e}")
                last_error = f"Proxy error: {str(e)}"
                
            except requests.exceptions.Timeout as e:
                logger.error(f"Timeout on attempt {attempt + 1}: {e}")
                last_error = f"Timeout: {str(e)}"
                
            except Exception as e:
                logger.error(f"Request error on attempt {attempt + 1}: {e}")
                last_error = str(e)
            
            # Wait before retry (except on last attempt)
            if attempt < max_retries - 1:
                logger.debug(f"Waiting {delay_between_retries}s before retry...")
                time.sleep(delay_between_retries)
        
        # All retries failed
        logger.error(
            f"❌ All {max_retries} attempts failed for {url}. "
            f"Last error: {last_error}"
        )
        return None
    
    def get_circuit_info(self) -> Optional[Dict[str, Any]]:
        """
        Get information about current Tor circuits
        
        Returns:
            Dict with circuit information or None if failed
            {
                'success': bool,
                'circuits': List[dict],
                'total': int
            }
        """
        if not STEM_AVAILABLE:
            return {
                'success': False,
                'message': 'Stem library not available',
                'circuits': [],
                'total': 0
            }
        
        try:
            with Controller.from_port(
                address=self.control_host,  # Use control_host for Stem
                port=self.control_port
            ) as controller:
                controller.authenticate(password=self.control_password)
                
                circuits = []
                for circuit in controller.get_circuits():
                    circuits.append({
                        'id': circuit.id,
                        'status': circuit.status.name,
                        'purpose': circuit.purpose,
                        'path': [
                            {
                                'fingerprint': entry.fingerprint[:16],
                                'nickname': entry.nickname
                            }
                            for entry in circuit.path
                        ],
                        'build_time': str(circuit.created)
                    })
                
                logger.info(f"Retrieved {len(circuits)} Tor circuits")
                
                return {
                    'success': True,
                    'circuits': circuits,
                    'total': len(circuits)
                }
                
        except Exception as e:
            logger.error(f"Failed to get circuit info: {e}")
            return {
                'success': False,
                'message': str(e),
                'circuits': [],
                'total': 0
            }
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about Tor usage
        
        Returns:
            Dict with usage statistics
        """
        return {
            'circuit_renewals': self.circuit_renewal_count,
            'last_renewal': self.last_circuit_renewal.isoformat() if self.last_circuit_renewal else None,
            'unique_ips_used': len(self.used_ips),
            'ips_used': self.used_ips,
            'stem_available': STEM_AVAILABLE,
            'proxy_config': f"{self.proxy_host}:{self.proxy_port}"
        }
    
    def close(self):
        """Close the session and cleanup"""
        if self.session:
            self.session.close()
            self.session = None
            logger.info("Tor session closed")


# Convenience function for quick anonymous requests
def anonymous_get(url: str, **kwargs) -> Optional[requests.Response]:
    """
    Make anonymous GET request through Tor
    
    Args:
        url: Target URL
        **kwargs: Additional arguments for request
        
    Returns:
        Response object or None
        
    Example:
        response = anonymous_get('https://api.github.com/users/torvalds')
        if response:
            print(response.json())
    """
    tor = TorProxyService()
    return tor.request_with_retry(url, method='GET', **kwargs)

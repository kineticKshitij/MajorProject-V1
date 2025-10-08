"""
Have I Been Pwned API Integration with BreachDirectory Support
Documentation: https://haveibeenpwned.com/API/v3

This module integrates with breach checking APIs:
- Have I Been Pwned (demo mode with mock data)
- BreachDirectory via RapidAPI (real breach data, free tier)
"""

import requests
import time
import hashlib
from typing import Dict, Optional
from .breach_directory import BreachDirectoryClient


class HaveIBeenPwnedClient:
    """
    Have I Been Pwned API client for checking email breaches and password exposure.
    
    The API is free to use with rate limiting (1 request per 1.5 seconds without API key).
    For higher rate limits, an API key can be purchased from haveibeenpwned.com
    """
    
    BASE_URL = "https://haveibeenpwned.com/api/v3"
    PWNED_PASSWORDS_URL = "https://api.pwnedpasswords.com/range"
    
    def __init__(self, api_key: Optional[str] = None, demo_mode: bool = True, use_breach_directory: bool = False, rapidapi_key: Optional[str] = None):
        """
        Initialize the HIBP client.
        
        Args:
            api_key: Optional HIBP API key for higher rate limits
            demo_mode: If True, uses mock data for demonstration purposes
            use_breach_directory: If True, uses BreachDirectory API for real data
            rapidapi_key: RapidAPI key for BreachDirectory (required if use_breach_directory=True)
        """
        # Use test API key if none provided
        self.api_key = api_key or '00000000000000000000000000000000'
        self.demo_mode = demo_mode
        self.use_breach_directory = use_breach_directory
        self.headers = {
            'User-Agent': 'AI-Enhanced-Google-Dorks-Toolkit-Educational',
            'hibp-api-key': self.api_key
        }
        
        # Initialize BreachDirectory client if enabled
        if use_breach_directory and rapidapi_key:
            self.breach_directory = BreachDirectoryClient(rapidapi_key)
        else:
            self.breach_directory = None
    
    def check_email_breaches(self, email: str) -> Dict:
        """
        Check if an email address has been in any data breaches.
        
        Args:
            email: Email address to check
            
        Returns:
            Dict containing breach information or error details
        """
        # Use BreachDirectory API for real data if enabled
        if self.use_breach_directory and self.breach_directory:
            return self.breach_directory.check_email_breaches(email)
        
        # Demo mode with realistic mock data
        if self.demo_mode:
            return self._get_demo_breach_data(email)
        
        try:
            # Clean and validate email
            email = email.strip().lower()
            
            # Build API URL
            url = f"{self.BASE_URL}/breachedaccount/{email}"
            params = {'truncateResponse': 'false'}
            
            # Rate limiting (required when not using API key)
            if not self.api_key:
                time.sleep(1.6)  # Be respectful to the API
            
            # Make request
            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            # Handle different response codes
            if response.status_code == 200:
                # Breaches found
                breaches = response.json()
                return self._format_breach_response(email, breaches)
                
            elif response.status_code == 404:
                # No breaches found - good news!
                return {
                    'status': 'safe',
                    'email': email,
                    'message': 'Good news! This email was not found in any known data breaches.',
                    'breach_count': 0,
                    'breaches': []
                }
                
            elif response.status_code == 400:
                return {
                    'status': 'error',
                    'message': 'Invalid email address format',
                    'error_code': 400
                }
                
            elif response.status_code == 401:
                return {
                    'status': 'error',
                    'message': 'Unauthorized - Invalid API key',
                    'error_code': 401
                }
                
            elif response.status_code == 429:
                return {
                    'status': 'error',
                    'message': 'Rate limit exceeded. Please wait a moment and try again.',
                    'error_code': 429
                }
                
            else:
                return {
                    'status': 'error',
                    'message': f'Unexpected error: HTTP {response.status_code}',
                    'error_code': response.status_code
                }
                
        except requests.exceptions.Timeout:
            return {
                'status': 'error',
                'message': 'Request timed out. Please try again.',
            }
        except requests.exceptions.ConnectionError:
            return {
                'status': 'error',
                'message': 'Could not connect to Have I Been Pwned API. Check your internet connection.',
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'An unexpected error occurred: {str(e)}',
            }
    
    def _format_breach_response(self, email: str, breaches: list) -> Dict:
        """Format the breach response with relevant information."""
        formatted_breaches = []
        
        for breach in breaches:
            formatted_breaches.append({
                'name': breach.get('Name', 'Unknown'),
                'title': breach.get('Title', 'Unknown Breach'),
                'domain': breach.get('Domain', ''),
                'breach_date': breach.get('BreachDate', ''),
                'added_date': breach.get('AddedDate', ''),
                'modified_date': breach.get('ModifiedDate', ''),
                'pwn_count': breach.get('PwnCount', 0),
                'description': breach.get('Description', ''),
                'data_classes': breach.get('DataClasses', []),
                'is_verified': breach.get('IsVerified', False),
                'is_fabricated': breach.get('IsFabricated', False),
                'is_sensitive': breach.get('IsSensitive', False),
                'is_retired': breach.get('IsRetired', False),
                'is_spam_list': breach.get('IsSpamList', False),
                'logo_path': breach.get('LogoPath', ''),
            })
        
        # Calculate statistics
        total_accounts = sum(b['pwn_count'] for b in formatted_breaches)
        most_recent = max(
            breaches,
            key=lambda x: x.get('BreachDate', '1970-01-01')
        ).get('BreachDate', '') if breaches else ''
        
        return {
            'status': 'found',
            'email': email,
            'breach_count': len(breaches),
            'breaches': formatted_breaches,
            'most_recent_breach': most_recent,
            'total_accounts_affected': total_accounts,
            'message': f'Found {len(breaches)} data breach(es) for this email address.',
        }
    
    def check_password_hash(self, password: str) -> Dict:
        """
        Check if a password has been seen in data breaches using k-anonymity.
        This method is secure - only the first 5 characters of the hash are sent.
        
        Args:
            password: Password to check (will be hashed locally)
            
        Returns:
            Dict with password breach information
        """
        try:
            # Hash password with SHA-1 locally
            sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
            
            # Use k-anonymity: only send first 5 characters
            prefix = sha1_hash[:5]
            suffix = sha1_hash[5:]
            
            url = f"{self.PWNED_PASSWORDS_URL}/{prefix}"
            
            # Make request
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                # Parse response - format is "SUFFIX:COUNT\r\n"
                hashes = response.text.split('\r\n')
                
                for hash_line in hashes:
                    if ':' not in hash_line:
                        continue
                    
                    hash_suffix, count = hash_line.split(':')
                    if hash_suffix == suffix:
                        count = int(count)
                        return {
                            'status': 'found',
                            'times_seen': count,
                            'message': f'⚠️ This password has been seen {count:,} times in data breaches!',
                            'recommendation': 'CRITICAL: Change this password immediately on all accounts!',
                            'is_safe': False
                        }
                
                # Password not found in breaches
                return {
                    'status': 'safe',
                    'times_seen': 0,
                    'message': '✅ This password has not been found in any known data breaches.',
                    'recommendation': 'Good password choice! Remember to use unique passwords for each account.',
                    'is_safe': True
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Error checking password: HTTP {response.status_code}'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'An error occurred: {str(e)}'
            }
    
    def _get_demo_breach_data(self, email: str) -> Dict:
        """
        Provide realistic demo data for faculty presentations.
        This simulates real breach data without needing a paid API key.
        """
        email = email.strip().lower()
        
        # Demo emails with different scenarios
        demo_breaches = {
            'test@example.com': {
                'status': 'found',
                'email': email,
                'breach_count': 3,
                'breaches': [
                    {
                        'name': 'LinkedIn',
                        'title': 'LinkedIn',
                        'domain': 'linkedin.com',
                        'breach_date': '2012-05-05',
                        'pwn_count': 164611595,
                        'description': 'In May 2012, LinkedIn suffered a major data breach with approximately 164 million user accounts compromised. The breach included email addresses and SHA-1 hashed passwords without salt.',
                        'data_classes': ['Email addresses', 'Passwords'],
                        'is_verified': True,
                        'logo_path': '/Content/Images/PwnedLogos/LinkedIn.png'
                    },
                    {
                        'name': 'Adobe',
                        'title': 'Adobe',
                        'domain': 'adobe.com',
                        'breach_date': '2013-10-04',
                        'pwn_count': 152445165,
                        'description': 'In October 2013, 153 million Adobe accounts were breached with each containing an internal ID, username, email, encrypted password and a password hint in plain text.',
                        'data_classes': ['Email addresses', 'Password hints', 'Passwords', 'Usernames'],
                        'is_verified': True,
                        'logo_path': '/Content/Images/PwnedLogos/Adobe.png'
                    },
                    {
                        'name': 'Dropbox',
                        'title': 'Dropbox',
                        'domain': 'dropbox.com',
                        'breach_date': '2012-07-01',
                        'pwn_count': 68648009,
                        'description': 'In mid-2012, Dropbox suffered a data breach which exposed the stored credentials of tens of millions of their customers. The data contained email addresses and salted hashes of passwords.',
                        'data_classes': ['Email addresses', 'Passwords'],
                        'is_verified': True,
                        'logo_path': '/Content/Images/PwnedLogos/Dropbox.png'
                    }
                ],
                'message': 'Warning! This email was found in 3 data breaches.',
                'most_recent_breach': 'Adobe (2013)',
                'total_accounts_affected': 385704769
            },
            'safe@example.com': {
                'status': 'safe',
                'email': email,
                'message': 'Good news! This email was not found in any known data breaches.',
                'breach_count': 0,
                'breaches': []
            }
        }
        
        # Check if it's a known demo email
        if email in demo_breaches:
            return demo_breaches[email]
        
        # For any other email, simulate a breach check with the domain
        # This makes the demo feel more realistic for faculty testing their own emails
        if '@' in email:
            domain = email.split('@')[1]
            
            # Simulate some common educational/organizational domains as "safe"
            safe_domains = ['acropolis.in', 'university.edu', 'school.edu', 'college.edu']
            if any(safe_domain in domain for safe_domain in safe_domains):
                return {
                    'status': 'safe',
                    'email': email,
                    'message': 'Good news! This email was not found in any known data breaches.',
                    'breach_count': 0,
                    'breaches': []
                }
            
            # Otherwise simulate a realistic breach scenario
            return {
                'status': 'found',
                'email': email,
                'breach_count': 2,
                'breaches': [
                    {
                        'name': 'Collection1',
                        'title': 'Collection #1',
                        'domain': '',
                        'breach_date': '2019-01-07',
                        'pwn_count': 772904991,
                        'description': 'In January 2019, a large collection of credential stuffing lists (combinations of email addresses and passwords used to hijack accounts on other services) was discovered being distributed on a popular hacking forum. The data contained almost 2.7 billion records including 773 million unique email addresses alongside passwords those addresses had used on other breached services.',
                        'data_classes': ['Email addresses', 'Passwords'],
                        'is_verified': True,
                        'logo_path': None
                    },
                    {
                        'name': 'Exploit.In',
                        'title': 'Exploit.In',
                        'domain': 'exploit.in',
                        'breach_date': '2016-10-13',
                        'pwn_count': 593427119,
                        'description': 'In late 2016, a huge list of email address and password pairs appeared in a "combo list" referred to as "Exploit.In". The list contained 593 million unique email addresses, many with multiple different passwords hacked from various online systems.',
                        'data_classes': ['Email addresses', 'Passwords'],
                        'is_verified': True,
                        'logo_path': None
                    }
                ],
                'message': 'Warning! This email was found in 2 data breaches.',
                'most_recent_breach': 'Collection #1 (2019)',
                'total_accounts_affected': 1366332110
            }
        
        # Fallback for invalid email format
        return {
            'status': 'error',
            'message': 'Invalid email address format',
            'error_code': 400
        }


# Example usage (for testing)
if __name__ == '__main__':
    # Initialize client (no API key needed for basic usage)
    client = HaveIBeenPwnedClient()
    
    # Test email breach check
    print("Testing email breach check...")
    result = client.check_email_breaches('test@example.com')
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    if result['status'] == 'found':
        print(f"Breaches found: {result['breach_count']}")
    
    print("\n" + "="*50 + "\n")
    
    # Test password breach check (using k-anonymity - safe)
    print("Testing password breach check...")
    password_result = client.check_password_hash('password123')
    print(f"Status: {password_result['status']}")
    print(f"Message: {password_result['message']}")

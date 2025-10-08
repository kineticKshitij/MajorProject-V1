"""
BreachDirectory.org API Integration via RapidAPI
Documentation: https://rapidapi.com/rohan-patra/api/breachdirectory

This module integrates with BreachDirectory API to check if email addresses
have been compromised in data breaches using real breach data.
"""

import requests
from typing import Dict, Optional


class BreachDirectoryClient:
    """
    BreachDirectory API client for checking real email breaches via RapidAPI.
    Provides access to real breach data without paid subscriptions.
    """
    
    BASE_URL = "https://breachdirectory.p.rapidapi.com"
    
    def __init__(self, api_key: str):
        """
        Initialize the BreachDirectory client.
        
        Args:
            api_key: RapidAPI key for BreachDirectory
        """
        self.api_key = api_key
        self.headers = {
            'x-rapidapi-host': 'breachdirectory.p.rapidapi.com',
            'x-rapidapi-key': api_key
        }
    
    def check_email_breaches(self, email: str) -> Dict:
        """
        Check if an email address has been in any data breaches.
        
        Args:
            email: Email address to check
            
        Returns:
            Dict containing breach information or error details
        """
        try:
            # Clean and validate email
            email = email.strip().lower()
            
            # Build API URL with query parameters
            url = self.BASE_URL
            params = {
                'func': 'auto',
                'term': email
            }
            
            # Make request
            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            # Handle different response codes
            if response.status_code == 200:
                data = response.json()
                
                # Check if breaches were found
                if data.get('success') and data.get('found') > 0:
                    return self._format_breach_response(email, data)
                else:
                    # No breaches found
                    return {
                        'status': 'safe',
                        'email': email,
                        'message': 'Good news! This email was not found in any known data breaches.',
                        'breach_count': 0,
                        'breaches': []
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
                    'message': f'API error: HTTP {response.status_code}',
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
                'message': 'Could not connect to BreachDirectory API. Check your internet connection.',
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'An unexpected error occurred: {str(e)}',
            }
    
    def _format_breach_response(self, email: str, data: Dict) -> Dict:
        """
        Format the breach response from BreachDirectory API.
        
        Args:
            email: Email address checked
            data: Raw API response data
            
        Returns:
            Formatted breach information
        """
        breaches = []
        breach_count = data.get('found', 0)
        
        # BreachDirectory returns results in 'result' field
        if 'result' in data:
            results = data['result']
            
            # Group by sources (breach names)
            sources_dict = {}
            for result in results:
                if isinstance(result, dict):
                    sources = result.get('sources', [])
                    for source in sources:
                        if source not in sources_dict:
                            sources_dict[source] = {
                                'name': source,
                                'title': source.replace('_', ' ').title(),
                                'count': 1
                            }
                        else:
                            sources_dict[source]['count'] += 1
            
            # Convert to breach format
            for source_name, source_data in sources_dict.items():
                breaches.append({
                    'name': source_name,
                    'title': source_data['title'],
                    'domain': '',
                    'breach_date': 'Unknown',
                    'pwn_count': source_data['count'],
                    'description': f'This email was found in the {source_data["title"]} breach database.',
                    'data_classes': ['Email addresses', 'Potentially passwords and other data'],
                    'is_verified': True,
                    'logo_path': None
                })
        
        # Calculate statistics
        total_affected = sum(b['pwn_count'] for b in breaches)
        most_recent = breaches[0]['title'] if breaches else 'Unknown'
        
        return {
            'status': 'found',
            'email': email,
            'breach_count': len(breaches),
            'breaches': breaches,
            'message': f'Warning! This email was found in {len(breaches)} data breach{"es" if len(breaches) != 1 else ""}.',
            'most_recent_breach': most_recent,
            'total_accounts_affected': total_affected
        }


# Example usage (for testing)
if __name__ == '__main__':
    # Initialize client with RapidAPI key
    api_key = '8ccf0651c6msh372c47780262060p11840cjsndd79277d8f13'
    client = BreachDirectoryClient(api_key)
    
    # Test email breach check
    print("Testing BreachDirectory API...")
    result = client.check_email_breaches('test@example.com')
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    if result['status'] == 'found':
        print(f"Breaches: {result['breach_count']}")
        for breach in result['breaches']:
            print(f"  - {breach['title']}")

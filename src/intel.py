import requests
from logger import setup_logger

logger = setup_logger(__name__)

class ThreatIntel:
    def __init__(self, api_key):
        self.api = api_key
        self.url = 'https://api.abuseipdb.com/api/v2/check'
        self.headers = {
            'Accept': 'application/json',
            'Key': self.api
        }

    def check_ip(self, ip_address):
        params = {
            'ipAddress': ip_address,
            'maxAgeInDays': 90
        }

        try:
            response = requests.get(self.url, headers=self.headers, params=params, timeout=5)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
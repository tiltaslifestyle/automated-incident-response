import requests

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
            print(f"[Error] API request failed: {e}")
            return None

if __name__ == "__main__":
    import yaml
    
    def load_settings(path="config/settings.yaml"):
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    try:
        settings = load_settings()
        key = settings["api"]["key"]
        
        intel = ThreatIntel(key)
        result = intel.check_ip("118.25.6.39")
        
        print("Threat Intelligence Result:")
        import json
        print(json.dumps(result, indent=4))
        
    except FileNotFoundError:
        print("[Error]: config/settings.yaml not found")
    except KeyError:
        print("[Error]: Missing api key in settings.yaml")
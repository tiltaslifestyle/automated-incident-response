from intel import ThreatIntel
from notifier import Notifier

class Engine:
    def __init__(self, settings: dict):
        self.settings = settings
        self.api_key = settings["api"]["key"]
        self.topic = settings["ntfy"]["topic"]
        self.threshold = settings["thresholds"]["critical_score"]
        
        self.intel = ThreatIntel(self.api_key)
        self.notifier = Notifier(self.topic)

    def analyze_ip(self, ip_address: str):
        print(f"[*] Engine: Analyzing {ip_address}...")
        
        report = self.intel.check_ip(ip_address)
        
        if not report:
            print(f"[!] Engine: No data received for {ip_address}. Skipping.")
            return
        
        data = report.get("data", {})
        score = data.get("abuseConfidenceScore", 0)
        country = data.get("countryCode", "Unknown")
        isp = data.get("isp", "Unknown")

        print(f"[*] Report: Score {score}/100 | Country: {country}")

        if score >= self.threshold:
            # CRITICAL ALERT
            title = f"SECURITY ALERT: {ip_address}"
            tags = "rotating_light,skull"
            priority = "high"
            
            message = (
                f"Score: {score}/100 | Country: {country} | ISP: {isp} | Action: Blocked"
            )
            
            if self.notifier.send(message, title, priority, tags):
                print("[+] Alert sent successfully.")
            else:
                print("[-] Failed to send alert.")
                
        else:
            # SAFE / LOW RISK 
            print(f"[*] IP {ip_address} is below threshold ({self.threshold}). No alert sent.")

if __name__ == "__main__":
    import yaml
    
    def load_settings(path="config/settings.yaml"):
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    settings = load_settings()
    engine = Engine(settings)
    
    print("\n--- TEST CASE: BAD IP ---")
    engine.analyze_ip("109.107.189.250") 
    
    print("\n--- TEST CASE: GOOD IP ---")
    engine.analyze_ip("8.8.8.8")
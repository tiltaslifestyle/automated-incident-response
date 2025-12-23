import argparse
import os
import sys
import yaml
from core import Engine

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, 'config', 'settings.yaml')

def load_config():
    if not os.path.exists(CONFIG_PATH):
        print(f"[CRITICAL] Config file not found at: {CONFIG_PATH}")
        sys.exit(1)
    
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                    settings = yaml.safe_load(f)
    except Exception as e:
        print(f"[CRITICAL] Error parsing settings.yaml: {e}")
        sys.exit(1)

    # CONFIG VALIDATION
    required_paths = [
        ("api", "key"),
        ("ntfy", "topic"),
        ("thresholds", "critical_score"),
    ]

    for path in required_paths:
        current = settings
        for key in path:
            if key not in current:
                print(f"[CRITICAL] Missing config key: {'.'.join(path)}")
                sys.exit(1)
            current = current[key]

    return settings

def main():
    parser = argparse.ArgumentParser(description="IP Threat Analysis")
    parser.add_argument("ip", help="The suspicious IP address to analyze")
    
    args = parser.parse_args()

    settings = load_config()

    try:
        engine = Engine(settings)
        engine.analyze_ip(args.ip)
        
    except KeyboardInterrupt:
        print("\n[!] User interrupted execution.")
        sys.exit(0)
    except Exception as e:
        print(f"[CRITICAL] Runtime Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
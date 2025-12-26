import argparse
import os
import sys
import yaml
from core import Engine
from logger import setup_logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, 'config', 'settings.yaml')

logger = setup_logger(__name__)

def load_config():
    if not os.path.exists(CONFIG_PATH):
        logger.critical(f"Config file not found at: {CONFIG_PATH}")
        sys.exit(1)
    
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            settings = yaml.safe_load(f)
    except Exception as e:
        logger.critical(f"Error parsing settings.yaml: {e}")
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
                logger.critical(f"Missing config key: {'.'.join(path)}")
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
        logger.info("User interrupted execution.")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Runtime Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
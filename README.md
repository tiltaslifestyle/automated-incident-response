# Automated Incident Response
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Fail2Ban](https://img.shields.io/badge/Fail2Ban-222222?style=for-the-badge&logoColor=white)
![AbuseIPDB](https://img.shields.io/badge/AbuseIPDB-4e7e14?style=for-the-badge&logoColor=black)
![ntfy.sh](https://img.shields.io/badge/ntfy.sh-3e9e8c?style=for-the-badge&logoColor=white)

SecOps project demonstrating log-based intrusion detection, threat intelligence enrichment, decision logic, and alerting.

This project is designed to be triggered by **Fail2Ban** and perform **incident response**, not detection.

## Project Structure
```
.
├── config/
│   └── settings.yaml        # API keys, thresholds (gitignored)
├── src/
│   ├── __init__.py          # Package boundary
│   ├── main.py              # Entrypoint / Orchestrator (triggered by Fail2Ban)
│   ├── core.py              # Incident response decision engine
│   ├── intel.py             # Threat intelligence enrichment (AbuseIPDB)
│   └── notifier.py          # Alert delivery (ntfy.sh)
└── README.md

```

## Incident Lifecycle
```

[ Attacker ]
     │
     │ SSH brute-force attempts
     ▼
[ sshd ]
     │
     │ Writes logs
     ▼
[ /var/log/auth.log ]
     │
     │ Log pattern match
     ▼
[ Fail2Ban ]
     │
     │ Detects brute-force
     │ Applies temporary ban (iptables)
     │ Triggers custom action
     ▼
[ main.py ] (Entrypoint)
     │
     │ Passes incident context (IP, service, retries)
     ▼
[ core.py ] (Decision Engine)
     │
     ├──▶ [ intel.py ]
     │         │ Queries AbuseIPDB
     │         │ Returns reputation data
     │
     ├── Evaluates severity
     │   Decides on permanent ban / alert
     ▼
[ notifier.py ]
     │
     │ Sends notification
     ▼
[ ntfy.sh ]
     │
     ▼
[ Admin / User ]

```

## Responsibilities
- Fail2Ban — detects attacks and applies initial mitigation
- main.py — orchestration and input handling
- core.py — incident classification and response decisions
- intel.py — threat intelligence enrichment
- notifier.py — alert delivery

## Scope
- Detection: Fail2Ban (log-based)
- Enrichment: AbuseIPDB (via intel.py)
- Response: iptables (temporary ban via Fail2Ban, permanent decisions via core.py)
- Alerting: ntfy.sh
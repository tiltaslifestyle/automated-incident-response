# Automated Incident Response
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
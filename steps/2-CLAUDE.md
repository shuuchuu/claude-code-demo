# Firewall log analysis

The firewall logs are in `logs/`, in syslog format (iptables LOG lines and sshd).

## Commands
- Tests: `python3 -m unittest`
- Run a script: `python3 <script>.py` (standard library only)

## Rules
- Anonymize internal IPs (10.x.x.x) in reports: replace the last octet with `x`
- Never read or print `.env`: it holds secrets
- No external dependency without asking me
- Reports in English, for SOC analysts: factual, with any assumption flagged

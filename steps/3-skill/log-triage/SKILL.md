---
name: log-triage
description: Triages firewall logs and summarizes suspicious events. Use it to analyze a firewall log.
---

1. Run `python3 .claude/skills/log-triage/summarize_logs.py <file>` on the requested log.
2. Sort each finding: **blocked** (the firewall dropped it), **allowed but suspicious** (accepted,
   yet abnormal), **noise** (nothing to do). Clues of suspicious allowed traffic: regular
   connections to the same external address, an unusual port, a single internal host involved.
3. Write the report following `report-template.md`, in `reports/triage-<date>.md`.

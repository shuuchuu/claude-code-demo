#!/bin/sh
# Sets up the Claude Code demo in a new folder, outside any repository:
#   ./install.sh ~/demo-claude-code
# then, at each step (cumulative, 2 to 6):
#   ./install.sh ~/demo-claude-code <step>
set -eu
KIT=$(cd "$(dirname "$0")" && pwd)
DEMO=$1
STEP=${2:-1}
case $STEP in
1)
  [ -e "$DEMO" ] && { echo "$DEMO already exists: pick a new folder." >&2; exit 1; }
  cp -r "$KIT/project" "$DEMO"
  mv "$DEMO/env.example" "$DEMO/.env"
  (cd "$DEMO" && git init -q && git add -A && git commit -qm "Initial project")
  ;;
2) cp "$KIT/steps/2-CLAUDE.md" "$DEMO/CLAUDE.md" ;;
3) mkdir -p "$DEMO/.claude/skills" && cp -r "$KIT/steps/3-skill/log-triage" "$DEMO/.claude/skills/" ;;
4) cp "$KIT/steps/4-mcp/ip_reputation_server.py" "$DEMO/" && cp "$KIT/steps/4-mcp/mcp.json" "$DEMO/.mcp.json" ;;
5) mkdir -p "$DEMO/.claude/hooks" && cp "$KIT/steps/5-guardrails/hooks/protect_secrets.py" "$DEMO/.claude/hooks/" \
     && cp "$KIT/steps/5-guardrails/settings.json" "$DEMO/.claude/settings.json"
   # Simulates a fooled model: the .env rule disappears from CLAUDE.md.
   grep -v "Never read" "$DEMO/CLAUDE.md" > "$DEMO/CLAUDE.md.tmp" && mv "$DEMO/CLAUDE.md.tmp" "$DEMO/CLAUDE.md" ;;
6) cp "$KIT/steps/6-sandbox-settings.json" "$DEMO/.claude/settings.json" ;;
*) echo "Unknown step: $STEP (1 to 6)" >&2; exit 1 ;;
esac
echo "Step $STEP installed in $DEMO. Restart claude in that folder."

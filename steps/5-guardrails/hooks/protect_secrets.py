"""PreToolUse hook: blocks any read, search or command that targets a secrets file.

Claude Code sends the action as JSON on standard input. Exiting with code 2 blocks it,
and the error message is sent back to the model.
"""

import json
import sys

SECRETS = (".env", "secret")

action = json.load(sys.stdin)
tool_input = action.get("tool_input", {})
target = " ".join(str(tool_input.get(key, "")) for key in ("command", "file_path", "path", "pattern"))

if any(secret in target.lower() for secret in SECRETS):
    print(f"Blocked by the protect_secrets hook: {action['tool_name']} targets a secrets file.", file=sys.stderr)
    sys.exit(2)

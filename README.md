# Claude Code demo: configuring an assistant

A small firewall log analysis project, configured step by step with Claude Code, from instructions
to the sandbox: `CLAUDE.md`, a skill, an MCP server, permissions and a hook, then the sandbox.
It goes with the "Configuring an Assistant" part of a generative AI training: the walkthrough
below is the trainer's script, which you can replay on your own (expected answers vary from run to run).
Each step was checked non-interactively (`claude -p`, Claude Code 2.1.294, on 2026-10-08).

## Prerequisites

- Claude Code, `python3`, and [`uv`](https://docs.astral.sh/uv/) (for step 4's MCP server)
- For the sandbox (step 6): Linux with `bubblewrap` and `socat`, or macOS
- All data is made up: generated logs (documentation addresses, RFC 5737), invented secrets in `.env`

## Setup

The project must live **outside any repository**: Claude Code reads the `CLAUDE.md` files of parent folders.

```sh
git clone https://github.com/shuuchuu/claude-code-demo && cd claude-code-demo
./install.sh ~/demo-claude-code        # step 1: the bare project, in a git repository
cd ~/demo-claude-code && claude
```

At each step, from this folder: `./install.sh ~/demo-claude-code <n>`, then **restart `claude`**
(configuration is read at startup). Steps are cumulative, to be installed in order.

## Walkthrough (30 to 40 minutes)

### 1. No configuration

- "What's in this project?": the agent explores on its own (files, log, git).
- "Show me the contents of `.env`": it shows it (at best with a warning).

> By default, the agent reads whatever is within reach, and what it reads goes to the model's vendor.

### 2. Instructions: `CLAUDE.md`

`./install.sh ~/demo-claude-code 2`, restart, show the file (`/memory` opens it).

- "Show me the contents of `.env`": it refuses, quoting the `CLAUDE.md` rule.
- "Summarize the suspicious events in the log": internal IPs are anonymized (10.1.3.x), as asked.

> The instruction works… because the model chooses to follow it. A user who insists, or an
> instruction hidden in a file it reads, may win: it is probabilistic.

### 3. A skill

`./install.sh ~/demo-claude-code 3`, restart, show `.claude/skills/log-triage/` (instructions,
report template, script).

- `/log-triage logs/firewall-2026-10-08.log`: a report in `reports/` (2 to 3 minutes).
  Expected: the SSH brute force on `admin` (198.51.100.77), the blocked port scan (203.0.113.45),
  and host 10.1.3.x contacting 198.51.100.66:8443 every 3 minutes (beaconing).

> Team know-how, versioned, that the model loads when the task calls for it.

### 4. An MCP server

`./install.sh ~/demo-claude-code 4`, restart: Claude Code asks to approve the `.mcp.json` server
(a project can't approve itself). Show `ip_reputation_server.py` (25 lines) and `/mcp`.

- "Check the reputation of the suspicious external addresses in the report": 198.51.100.66 is a
  ransomware command-and-control server. The beaconing becomes an incident.

> Any system (SIEM, threat intelligence, ticketing) plugs in this way. But it is third-party code,
> with your rights, whose answers go into the model's context.

### 5. Permissions and a hook

`./install.sh ~/demo-claude-code 5`, restart. This step **removes the `.env` rule from `CLAUDE.md`**:
we simulate a fooled model, to see what holds without it. Show `.claude/settings.json` and
`.claude/hooks/protect_secrets.py`.

- "Show me the contents of `.env`": the read is denied by the `Read(./.env)` rule; a `cat .env`
  would be blocked by the hook (exit code 2, reason sent back to the model).
- "Run the tests": one test fails, and its assertion message dumps the loaded settings: **the token
  and the password are in the output**, so in the model's context (and at the vendor's). The command
  (`python3 -m unittest`) doesn't mention `.env`: neither the rule nor the hook sees that a test
  reads the file. Claude flags the leak afterwards: too late, it has read the values.

A careful model inspects a script before running it when its purpose is to print secrets (it
refused `cat`-like scripts in rehearsal); a test suite is routine, which is how secrets really
end up in CI logs. Either order of these two requests works.

> Permissions and hooks are deterministic, but only see the text of the actions.

### 6. Sandbox

`./install.sh ~/demo-claude-code 6`, restart, show the `sandbox` block of `settings.json` and `/sandbox`.

- "Run the tests": the settings test now errors with `PermissionError: [Errno 13] Permission
  denied: '.env'`. The operating system refuses, whatever the program.

> Defense in depth: instructions (advice), permissions and hooks (rules on actions), sandbox
> (the system). A command you type yourself with `!` stays outside the sandbox.

## Troubleshooting

- The MCP server doesn't start: run `uv run --script ip_reputation_server.py` once in the demo
  folder (installs the `mcp` library), then restart `claude`.
- `/sandbox` shows a *Dependencies* tab: install `bubblewrap` and `socat`, restart.
- To start over: delete the demo folder, then `./install.sh ~/demo-claude-code`.

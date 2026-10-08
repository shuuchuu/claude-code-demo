"""Summarizes a firewall syslog: actions, dropped connections, SSH logins, repeated flows."""

import re
import sys
from collections import Counter, defaultdict

PACKET = re.compile(r"\[(FW-\w+)\].*SRC=(\S+) DST=(\S+).*PROTO=(\S+).*DPT=(\d+)")
SSH = re.compile(r"sshd\[\d+\]: (Failed|Accepted) \S+ for (\S+) from (\S+)")


def main(path: str) -> None:
    lines = [line for line in open(path, encoding="utf-8") if line.strip()]
    packets = [m.groups() for line in lines if (m := PACKET.search(line))]
    logins = [m.groups() for line in lines if (m := SSH.search(line))]
    print(f"{len(lines)} lines, from {lines[0][:15]} to {lines[-1][:15]}\n")
    print("Firewall actions:", dict(Counter(action for action, *_ in packets)))

    dropped = defaultdict(set)
    for action, src, _dst, _proto, port in packets:
        if action == "FW-DROP":
            dropped[src].add(port)
    print("\nDropped connections, per source (ports targeted):")
    for ip, ports in sorted(dropped.items(), key=lambda item: -len(item[1])):
        print(f"  {ip}: {len(ports)} ports ({', '.join(sorted(ports, key=int))})")

    print("\nSSH logins (result, user, source):", dict(Counter(logins)))

    flows = Counter((src, dst, port) for action, src, dst, _proto, port in packets if action == "FW-ACCEPT")
    print("\nMost repeated accepted flows (source, destination, port):")
    for (src, dst, port), n in flows.most_common(5):
        print(f"  {src} -> {dst}:{port}: {n} times")


if __name__ == "__main__":
    main(sys.argv[1])

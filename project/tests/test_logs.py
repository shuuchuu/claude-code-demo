"""Checks that the log files are well-formed syslog lines."""

import re
import unittest
from pathlib import Path

SYSLOG = re.compile(r"^[A-Z][a-z]{2} [ \d]\d \d{2}:\d{2}:\d{2} \S+ \S+: ")


class LogsTest(unittest.TestCase):
    def test_syslog_format(self) -> None:
        for path in Path("logs").glob("*.log"):
            for number, line in enumerate(path.read_text().splitlines(), start=1):
                self.assertRegex(line, SYSLOG, f"{path}:{number}")

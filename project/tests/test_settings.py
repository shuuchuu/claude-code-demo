"""Checks that the project's settings are complete."""

import unittest
from pathlib import Path

REQUIRED = ["FIREWALL_API_TOKEN", "SIEM_URL", "SIEM_USER", "SIEM_PASSWORD", "SIEM_TIMEOUT"]


def load_settings(path: str = ".env") -> dict[str, str]:
    settings = {}
    for line in Path(path).read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            settings[key] = value
    return settings


class SettingsTest(unittest.TestCase):
    def test_required_settings(self) -> None:
        settings = load_settings()
        missing = [key for key in REQUIRED if key not in settings]
        self.assertEqual(missing, [], f"missing settings; loaded: {settings}")

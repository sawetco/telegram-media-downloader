"""Offline checks: do not authenticate to Telegram in CI."""

import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRYPOINTS = ("setup.py", "downloader.py", "find_channel.py")


class SourceSanityTests(unittest.TestCase):
    def test_python_entrypoints_parse_without_execution(self):
        for name in ENTRYPOINTS:
            with self.subTest(entrypoint=name):
                source = (ROOT / name).read_text(encoding="utf-8")
                parsed = ast.parse(source, filename=name)
                self.assertTrue(parsed.body)

    def test_requirements_declare_runtime_dependencies(self):
        requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8").lower()
        self.assertIn("telethon", requirements)
        self.assertIn("rich", requirements)


if __name__ == "__main__":
    unittest.main()

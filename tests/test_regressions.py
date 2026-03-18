"""回归测试：覆盖已修复的滴答字段语义问题。"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.config_manager import load_config
from tools.dida_semantics import is_current_task_completed, priority_to_numeric
from tools.mcp_client import build_setup_guide, check_mcp_configured
from tools.task_parser import extract_priority, parse_timebox_input


class PrioritySemanticsTest(unittest.TestCase):
    def test_priority_symbols_follow_dida_semantics(self) -> None:
        self.assertEqual(extract_priority("!1"), "low")
        self.assertEqual(extract_priority("!2"), "medium")
        self.assertEqual(extract_priority("!3"), "high")
        self.assertEqual(priority_to_numeric("low"), 1)
        self.assertEqual(priority_to_numeric("medium"), 3)
        self.assertEqual(priority_to_numeric("high"), 5)


class TimeboxParsingTest(unittest.TestCase):
    def test_parse_timebox_with_reminder_priority_and_list(self) -> None:
        parsed = parse_timebox_input(
            "去江南沟通，今天下午3点，提前30分钟提醒，工作行动清单，中优先级"
        )
        self.assertEqual(parsed["task_description"], "去江南沟通")
        self.assertTrue(parsed["deadline"].endswith("T15:00"))
        self.assertEqual(parsed["priority"], "medium")
        self.assertEqual(parsed["reminder_offset_minutes"], 30)
        self.assertEqual(parsed["list_name"], "工作行动清单")


class CompletionStatusTest(unittest.TestCase):
    def test_completed_time_does_not_override_pending_status(self) -> None:
        task = {
            "title": "布置配网微应用系统建设工作",
            "status": "pending",
            "completedTime": "2026-02-04T09:00:00",
        }
        self.assertFalse(is_current_task_completed(task))


class HostAgnosticSetupTest(unittest.TestCase):
    def test_setup_guide_prefers_browser_authorization(self) -> None:
        guide = build_setup_guide()
        self.assertIn("Connect", guide)
        self.assertIn("浏览器", guide)
        self.assertIn("Claude Desktop", guide)
        self.assertIn("ChatGPT", guide)
        self.assertNotIn("在客户端内运行：/mcp", guide)

    def test_check_mcp_configured_reads_codex_mcp_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            home = Path(temp_dir)
            codex_path = home / ".codex" / "mcp.json"
            codex_path.parent.mkdir(parents=True, exist_ok=True)
            codex_path.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "dida365": {
                                "url": "https://mcp.dida365.com",
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            original_home = os.environ.get("HOME")
            os.environ["HOME"] = str(home)
            try:
                configured, message = check_mcp_configured()
            finally:
                if original_home is None:
                    os.environ.pop("HOME", None)
                else:
                    os.environ["HOME"] = original_home

        self.assertTrue(configured)
        self.assertIn("已检测到 dida365 MCP", message)

    def test_load_config_prefers_existing_codex_user_config(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            home = Path(temp_dir)
            default_path = ROOT / "config.yaml"
            codex_config = home / ".codex" / "skills" / "dida-coach" / "config.yaml"
            codex_config.parent.mkdir(parents=True, exist_ok=True)
            codex_config.write_text(
                "personality:\n  preset: strict_coach\n",
                encoding="utf-8",
            )

            original_home = os.environ.get("HOME")
            original_default = os.environ.get("DIDA_COACH_DEFAULT_CONFIG_PATH")
            os.environ["HOME"] = str(home)
            os.environ["DIDA_COACH_DEFAULT_CONFIG_PATH"] = str(default_path)
            try:
                config = load_config()
            finally:
                if original_home is None:
                    os.environ.pop("HOME", None)
                else:
                    os.environ["HOME"] = original_home
                if original_default is None:
                    os.environ.pop("DIDA_COACH_DEFAULT_CONFIG_PATH", None)
                else:
                    os.environ["DIDA_COACH_DEFAULT_CONFIG_PATH"] = original_default

        self.assertEqual(config["personality"]["preset"], "strict_coach")


if __name__ == "__main__":
    unittest.main()

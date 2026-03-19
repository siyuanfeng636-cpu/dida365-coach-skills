"""回归测试：覆盖已修复的滴答字段语义问题。"""

from __future__ import annotations

import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.config_manager import load_config
from tools.dida_semantics import is_current_task_completed, priority_to_numeric
from tools.mcp_client import (
    build_openclaw_http_config,
    build_setup_guide,
    check_mcp_configured,
)
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
        self.assertIn("transport", guide)
        self.assertIn("https://mcp.dida365.com", guide)
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

    def test_check_mcp_configured_reads_openclaw_transport_http_config(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            home = Path(temp_dir)
            openclaw_path = home / ".openclaw" / "openclaw.json"
            openclaw_path.parent.mkdir(parents=True, exist_ok=True)
            openclaw_path.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "dida365": {
                                "transport": {
                                    "type": "http",
                                    "url": "https://mcp.dida365.com",
                                }
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

    def test_build_openclaw_http_config_uses_transport_shape(self) -> None:
        config = build_openclaw_http_config()
        self.assertEqual(
            config["mcpServers"]["dida365"]["transport"]["type"],
            "http",
        )
        self.assertEqual(
            config["mcpServers"]["dida365"]["transport"]["url"],
            "https://mcp.dida365.com",
        )

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


class PromptContractTest(unittest.TestCase):
    def test_skill_triggers_cover_common_task_management_intents(self) -> None:
        skill = yaml.safe_load((ROOT / "skill.yaml").read_text(encoding="utf-8"))
        trigger_patterns = [item["pattern"] for item in skill.get("triggers", [])]
        compiled = [re.compile(pattern) for pattern in trigger_patterns]

        examples = [
            "我今天有哪些任务",
            "列出所有清单",
            "把买牛奶标记完成",
            "把这个任务移到工作清单",
            "按优先级筛选今天未完成任务",
        ]
        for example in examples:
            self.assertTrue(
                any(pattern.search(example) for pattern in compiled),
                msg=f"未命中通用任务管理入口：{example}",
            )

    def test_task_management_prompt_pins_real_mcp_tools(self) -> None:
        prompt = (ROOT / "prompts" / "task_management.md").read_text(encoding="utf-8")
        expected_tools = [
            "search_task",
            "get_task_by_id",
            "list_undone_tasks_by_time_query",
            "list_projects",
            "create_task",
            "complete_task",
            "move_task",
            "filter_tasks",
        ]
        for tool_name in expected_tools:
            self.assertIn(tool_name, prompt)

    def test_system_prompt_prefers_natural_dialogue_and_direct_single_actions(self) -> None:
        prompt = (ROOT / "prompts" / "system.md").read_text(encoding="utf-8")
        self.assertIn("优先自然对话", prompt)
        self.assertIn("先基于上下文做合理推断", prompt)
        self.assertIn("单个明确写操作", prompt)
        self.assertIn("高风险批量动作", prompt)
        self.assertIn("OpenClaw", prompt)
        self.assertIn("用户当前本地时区", prompt)
        self.assertIn("当前本地时间 + 目标绝对时间", prompt)

    def test_setup_docs_pin_openclaw_http_transport_config(self) -> None:
        reference = (ROOT / "references" / "mcp-client-setup.md").read_text(
            encoding="utf-8"
        )
        prompt = (ROOT / "prompts" / "setup.md").read_text(encoding="utf-8")
        self.assertIn('"type": "http"', reference)
        self.assertIn('"url": "https://mcp.dida365.com"', reference)
        self.assertIn("优先自动把 dida365 写入 OpenClaw 的 `mcpServers`", prompt)
        self.assertIn("账号登录、通行密钥、验证码和 2FA 必须由用户本人完成", prompt)

    def test_task_management_prompt_only_confirms_high_risk_batches(self) -> None:
        prompt = (ROOT / "prompts" / "task_management.md").read_text(encoding="utf-8")
        self.assertIn("单个明确写操作默认直接执行", prompt)
        self.assertIn("只有高风险批量动作才需要显式确认", prompt)
        self.assertIn("最多补 1 条高价值建议", prompt)

    def test_timebox_prompt_requires_real_task_materialization(self) -> None:
        prompt = (ROOT / "prompts" / "timebox_creation.md").read_text(encoding="utf-8")
        self.assertIn("create_task", prompt)
        self.assertIn("batch_add_tasks", prompt)
        self.assertIn("get_task_by_id", prompt)
        self.assertIn("真实的滴答任务", prompt)

    def test_timebox_prompt_prefers_recommendation_before_questionnaire(self) -> None:
        prompt = (ROOT / "prompts" / "timebox_creation.md").read_text(encoding="utf-8")
        self.assertIn("先根据现有描述给一个可执行的时间盒初稿", prompt)
        self.assertIn("不要把时长确认做成固定选项问卷", prompt)

    def test_review_prompts_allow_natural_summary(self) -> None:
        daily = (ROOT / "prompts" / "daily_review.md").read_text(encoding="utf-8")
        weekly = (ROOT / "prompts" / "weekly_review.md").read_text(encoding="utf-8")
        self.assertIn("先用自然语言总结今天的整体表现", daily)
        self.assertIn("不要每次都原样输出完整模板", daily)
        self.assertIn("先给一段自然语言总结本周走势", weekly)
        self.assertIn("不必硬套完整报告模板", weekly)

    def test_checkpoint_prompt_requires_local_time_recalculation(self) -> None:
        prompt = (ROOT / "prompts" / "checkpoint.md").read_text(encoding="utf-8")
        self.assertIn("用户当前本地时间和任务的绝对时间重新计算", prompt)
        self.assertIn("不要口算", prompt)

    def test_readme_mentions_timezone_and_mcp_latency(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("时区与性能说明", readme)
        self.assertIn("用户当前本地时区", readme)
        self.assertIn("远程 HTTP MCP", readme)


if __name__ == "__main__":
    unittest.main()

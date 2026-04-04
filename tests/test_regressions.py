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
from tools.dida_cli_auth import (
    DIDA_CLI_PACKAGE,
    build_dida_cli_install_command,
    build_dida_cli_login_command,
    build_dida_cli_setup_guide,
    build_dida_cli_status_command,
    detect_dida_cli_binary,
    detect_npm_binary,
)
from tools.productivity_system import (
    build_productivity_snapshot,
    get_productivity_root,
    initialize_productivity_system,
    summarize_productivity_state,
    update_productivity_files,
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
    def test_setup_guide_prefers_dida_cli_browser_authorization(self) -> None:
        guide = build_dida_cli_setup_guide()
        self.assertIn("dida-cli", guide)
        self.assertIn("dida auth login", guide)
        self.assertIn("浏览器", guide)
        self.assertIn("dida auth status", guide)
        self.assertNotIn("Connect", guide)
        self.assertNotIn("MCP", guide)

    def test_dida_cli_command_builders(self) -> None:
        self.assertIn(DIDA_CLI_PACKAGE, build_dida_cli_install_command())
        self.assertEqual(build_dida_cli_login_command(), "dida auth login")
        self.assertEqual(build_dida_cli_status_command(), "dida auth status")

    def test_detect_binaries_returns_string_or_none(self) -> None:
        dida_binary = detect_dida_cli_binary()
        npm_binary = detect_npm_binary()
        self.assertTrue(dida_binary is None or isinstance(dida_binary, str))
        self.assertTrue(npm_binary is None or isinstance(npm_binary, str))

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


class ProductivitySystemTest(unittest.TestCase):
    def test_productivity_root_can_follow_config(self) -> None:
        config = {"productivity_system": {"root": "~/.dida-coach/productivity"}}
        root = get_productivity_root(config)
        self.assertTrue(str(root).endswith(".dida-coach/productivity"))

    def test_initialize_productivity_system_creates_core_files(self) -> None:
        snapshot = build_productivity_snapshot(
            projects=[{"name": "工作行动清单"}],
            undone_tasks=[
                {
                    "title": "经法合同时间确认",
                    "project_name": "工作行动清单",
                    "priority": "high",
                    "due_date": "2026-03-22T13:00:00+08:00",
                }
            ],
            completed_tasks=[],
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            written = initialize_productivity_system(snapshot, root=Path(temp_dir))
            paths = summarize_productivity_state(Path(temp_dir))

        self.assertTrue(written)
        self.assertTrue(paths["initialized"])
        self.assertIn("dashboard.md", paths["existing_files"])
        self.assertIn("commitments/promises.md", paths["existing_files"])
        self.assertIn("reviews/weekly.md", paths["existing_files"])

    def test_snapshot_is_aggregate_not_full_task_copy(self) -> None:
        snapshot = build_productivity_snapshot(
            projects=[{"name": "工作行动清单"}],
            undone_tasks=[
                {
                    "title": "跟进供应商",
                    "project_name": "工作行动清单",
                    "priority": "medium",
                    "due_date": "2026-03-22T18:00:00+08:00",
                    "notes": "不要把这整段备注复制到本地系统",
                }
            ],
            completed_tasks=[],
        )
        serialized = json.dumps(snapshot, ensure_ascii=False)
        self.assertIn("跟进供应商", serialized)
        self.assertNotIn("不要把这整段备注复制到本地系统", serialized)
        self.assertNotIn('"content"', serialized)

    def test_update_productivity_files_refreshes_existing_managed_file(self) -> None:
        first = build_productivity_snapshot(
            projects=[{"name": "工作行动清单"}],
            undone_tasks=[{"title": "任务 A", "project_name": "工作行动清单"}],
            completed_tasks=[],
        )
        second = build_productivity_snapshot(
            projects=[{"name": "工作行动清单"}],
            undone_tasks=[{"title": "任务 B", "project_name": "工作行动清单"}],
            completed_tasks=[],
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            initialize_productivity_system(first, root=root)
            weekly_path = root / "planning" / "weekly.md"
            before = weekly_path.read_text(encoding="utf-8")
            update_productivity_files(second, root=root, files=["planning/weekly.md"])
            after = weekly_path.read_text(encoding="utf-8")

        self.assertNotEqual(before, after)
        self.assertIn("任务 B", after)


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
            "帮我建立生产力系统",
            "看一下我当前最该推进什么",
            "帮我梳理这周承诺和等待项",
        ]
        for example in examples:
            self.assertTrue(
                any(pattern.search(example) for pattern in compiled),
                msg=f"未命中通用任务管理入口：{example}",
            )

    def test_task_management_prompt_pins_real_cli_commands(self) -> None:
        prompt = (ROOT / "prompts" / "task_management.md").read_text(encoding="utf-8")
        expected_commands = [
            "dida project list --json",
            "dida project data <projectId> --json",
            "dida task filter",
            "dida task get <projectId> <taskId> --json",
            "dida task create",
            "dida task update",
            "dida task complete",
            "dida task move",
        ]
        for command in expected_commands:
            self.assertIn(command, prompt)

    def test_system_prompt_prefers_natural_dialogue_and_direct_single_actions(self) -> None:
        prompt = (ROOT / "prompts" / "system.md").read_text(encoding="utf-8")
        self.assertIn("优先自然对话", prompt)
        self.assertIn("先基于上下文做合理推断", prompt)
        self.assertIn("单个明确写操作", prompt)
        self.assertIn("高风险批量动作", prompt)
        self.assertIn("dida-cli", prompt)
        self.assertIn("用户当前本地时区", prompt)
        self.assertIn("当前本地时间 + 目标绝对时间", prompt)
        self.assertIn("本地生产力系统", prompt)
        self.assertIn("真实瓶颈", prompt)

    def test_setup_docs_pin_dida_cli_auth(self) -> None:
        reference = (ROOT / "references" / "dida-cli-auth-setup.md").read_text(
            encoding="utf-8"
        )
        prompt = (ROOT / "prompts" / "setup.md").read_text(encoding="utf-8")
        self.assertIn("npm install -g @suibiji/dida-cli", reference)
        self.assertIn("dida auth login", prompt)
        self.assertIn("dida auth status", prompt)
        self.assertIn("只认 `dida-cli`", prompt)
        self.assertNotIn("远程 MCP", reference)
        self.assertNotIn("OpenClaw", reference)

    def test_task_management_prompt_only_confirms_high_risk_batches(self) -> None:
        prompt = (ROOT / "prompts" / "task_management.md").read_text(encoding="utf-8")
        self.assertIn("单个明确写操作默认直接执行", prompt)
        self.assertIn("只有高风险批量动作才需要显式确认", prompt)
        self.assertIn("最多补 1 条高价值建议", prompt)

    def test_timebox_prompt_requires_real_task_materialization(self) -> None:
        prompt = (ROOT / "prompts" / "timebox_creation.md").read_text(encoding="utf-8")
        self.assertIn("dida task create", prompt)
        self.assertIn("dida task get", prompt)
        self.assertIn("真实的滴答任务", prompt)

    def test_timebox_prompt_prefers_recommendation_before_questionnaire(self) -> None:
        prompt = (ROOT / "prompts" / "timebox_creation.md").read_text(encoding="utf-8")
        self.assertIn("先根据现有描述给一个可执行的时间盒初稿", prompt)
        self.assertIn("不要把时长确认做成固定选项问卷", prompt)

    def test_review_prompts_allow_natural_summary(self) -> None:
        daily = (ROOT / "prompts" / "daily_review.md").read_text(encoding="utf-8")
        weekly = (ROOT / "prompts" / "weekly_review.md").read_text(encoding="utf-8")
        monthly = (ROOT / "prompts" / "monthly_review.md").read_text(encoding="utf-8")
        self.assertIn("先用自然语言总结今天的整体表现", daily)
        self.assertIn("不要每次都原样输出完整模板", daily)
        self.assertIn("先给一段自然语言总结本周走势", weekly)
        self.assertIn("不必硬套完整报告模板", weekly)
        self.assertIn("先给一段自然语言总结本月走势", monthly)

    def test_productivity_prompt_requires_local_os_layer_and_bottleneck_diagnosis(self) -> None:
        prompt = (ROOT / "prompts" / "productivity_management.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("~/.dida-coach/productivity/", prompt)
        self.assertIn("先判断过载来自哪一类", prompt)
        self.assertIn("dashboard.md", prompt)
        self.assertIn("commitments/promises.md", prompt)
        self.assertIn("reviews/monthly.md", prompt)

    def test_skill_and_readme_mention_dida_cli_route(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        reference = (ROOT / "references" / "dida-cli-auth-setup.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("默认自动认证：`dida-cli`", readme)
        self.assertIn("只使用 `dida-cli`", readme)
        self.assertIn("dida-cli", skill)
        self.assertIn("dida auth login", reference)

    def test_setup_docs_only_mention_dida_cli_route(self) -> None:
        prompt = (ROOT / "prompts" / "setup.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("只认 `dida-cli`", prompt)
        self.assertIn("不再引导远程 MCP", prompt)
        self.assertNotIn("OpenClaw", readme)
        self.assertNotIn("MCPorter", readme)
        self.assertNotIn("required_mcp", (ROOT / "skill.yaml").read_text(encoding="utf-8"))
        self.assertNotIn('type: "mcp"', (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8"))

    def test_default_onboarding_prefers_dida_cli_only(self) -> None:
        prompt = (ROOT / "prompts" / "setup.md").read_text(encoding="utf-8")
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("dida auth login", prompt)
        self.assertIn("默认接入只有一条", skill)
        self.assertIn("只支持 `dida-cli`", readme)
        self.assertNotIn("mcp.dida365.com", readme)

    def test_default_auth_prefers_dida_cli(self) -> None:
        prompt = (ROOT / "prompts" / "setup.md").read_text(encoding="utf-8")
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        reference = (ROOT / "references" / "dida-cli-auth-setup.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("只认 `dida-cli`", prompt)
        self.assertIn("dida auth login", prompt)
        self.assertIn("默认接入只有一条", skill)
        self.assertIn("只支持 `dida-cli`", readme)
        self.assertIn("适合本地 CLI 驱动的滴答能力", reference)

    def test_checkpoint_prompt_requires_local_time_recalculation(self) -> None:
        prompt = (ROOT / "prompts" / "checkpoint.md").read_text(encoding="utf-8")
        self.assertIn("用户当前本地时间和任务的绝对时间重新计算", prompt)
        self.assertIn("不要口算", prompt)

    def test_reminders_must_recheck_current_task_before_notifying(self) -> None:
        checkpoint = (ROOT / "prompts" / "checkpoint.md").read_text(encoding="utf-8")
        closure = (ROOT / "prompts" / "closure.md").read_text(encoding="utf-8")
        system = (ROOT / "prompts" / "system.md").read_text(encoding="utf-8")
        self.assertIn("提醒前必须先读取滴答当前任务状态", checkpoint)
        self.assertIn("如果截止时间、提醒时间、任务内容、清单或优先级刚发生变化，先向用户通报", checkpoint)
        self.assertIn("任何基于“到期、延期、检查点、变更后提醒”的闭环跟进，都要先重新拉取当前任务", closure)
        self.assertIn("任何到期提醒、检查点提醒、延期后提醒或变更后提醒，在发出前都必须先回读当前任务", system)

    def test_feedback_and_reviews_include_project_names(self) -> None:
        task_management = (ROOT / "prompts" / "task_management.md").read_text(
            encoding="utf-8"
        )
        daily = (ROOT / "prompts" / "daily_review.md").read_text(encoding="utf-8")
        weekly = (ROOT / "prompts" / "weekly_review.md").read_text(encoding="utf-8")
        monthly = (ROOT / "prompts" / "monthly_review.md").read_text(encoding="utf-8")
        system = (ROOT / "prompts" / "system.md").read_text(encoding="utf-8")
        self.assertIn("必须带上所属清单名称", task_management)
        self.assertIn("清单名称 + 任务标题", task_management)
        self.assertIn("清单名称 + 任务标题", daily)
        self.assertIn("优先按清单分组", weekly)
        self.assertIn("使用“清单名称 + 任务标题”", monthly)
        self.assertIn("默认带上所属清单名称", system)

    def test_readme_mentions_timezone_and_mcp_latency(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("时区与性能说明", readme)
        self.assertIn("用户当前本地时区", readme)
        self.assertIn("本地 CLI", readme)


if __name__ == "__main__":
    unittest.main()

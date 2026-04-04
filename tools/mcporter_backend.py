"""为 MCPorter 管理 dida-auth backend 提供辅助方法。"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from typing import Dict, Optional

BACKEND_NAME = "dida-auth-backend"


def detect_mcporter_binary() -> Optional[str]:
    """返回 mcporter 可执行文件路径。"""

    return shutil.which("mcporter")


def backend_script_path() -> Path:
    """返回本地 backend 脚本路径。"""

    return Path(__file__).resolve().parent.parent / "scripts" / "dida_auth_backend.py"


def build_mcporter_install_command(script_path: Optional[Path] = None) -> str:
    """生成推荐的 mcporter 注册命令。"""

    command = detect_mcporter_binary() or "mcporter"
    script = script_path or backend_script_path()
    return (
        f'{command} config add {BACKEND_NAME} '
        f'--command "{sys.executable}" '
        f'--arg "{script}"'
    )


def build_mcporter_backend_manifest(script_path: Optional[Path] = None) -> Dict[str, object]:
    """返回 backend 的命令配置描述。"""

    script = str(script_path or backend_script_path())
    return {
        "name": BACKEND_NAME,
        "command": sys.executable,
        "args": [script],
        "supports": [
            "status",
            "configure-openclaw",
            "dida-cli-status",
            "dida-cli-login",
            "dida-cli-install",
            "authorization-url",
            "oauth-local",
            "serve-jsonl",
        ],
    }


def format_backend_manifest(script_path: Optional[Path] = None) -> str:
    """返回便于文档展示的 manifest 文本。"""

    return json.dumps(
        build_mcporter_backend_manifest(script_path),
        ensure_ascii=False,
        indent=2,
    )

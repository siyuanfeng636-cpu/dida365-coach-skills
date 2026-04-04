"""滴答 CLI 的安装、认证与状态检查辅助方法。"""

from __future__ import annotations

import shutil

DIDA_CLI_PACKAGE = "@suibiji/dida-cli"


def detect_dida_cli_binary() -> str | None:
    """返回 dida CLI 可执行文件路径。"""

    return shutil.which("dida")


def detect_npm_binary() -> str | None:
    """返回 npm 可执行文件路径。"""

    return shutil.which("npm")


def build_dida_cli_install_command() -> str:
    """返回安装 dida CLI 的推荐命令。"""

    npm_bin = detect_npm_binary() or "npm"
    return f"{npm_bin} install -g {DIDA_CLI_PACKAGE}"


def build_dida_cli_login_command() -> str:
    """返回 dida CLI 登录命令。"""

    return "dida auth login"


def build_dida_cli_status_command() -> str:
    """返回 dida CLI 登录状态命令。"""

    return "dida auth status"


def build_dida_cli_logout_command() -> str:
    """返回 dida CLI 登出命令。"""

    return "dida auth logout"


def build_dida_cli_setup_guide() -> str:
    """返回 dida CLI 自动认证说明。"""

    return (
        "默认优先用 dida-cli 做本地自动认证：\n\n"
        "1. 如果 `dida` 还没安装，先执行：\n"
        f"   {build_dida_cli_install_command()}\n"
        "2. 执行：\n"
        f"   {build_dida_cli_login_command()}\n"
        "3. 浏览器会打开滴答登录/授权页，完成授权后返回终端\n"
        "4. 用下面这条确认状态：\n"
        f"   {build_dida_cli_status_command()}\n\n"
        "说明：这条路径会完成 dida-cli 自己的 OAuth PKCE 登录，适合本地 CLI 驱动的滴答能力。"
    )

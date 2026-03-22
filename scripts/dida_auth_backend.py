#!/usr/bin/env python3
"""由 MCPorter 托管的滴答接入 backend。"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict

from tools.mcp_client import (
    build_openclaw_connect_guide,
    check_mcp_configured,
    get_openclaw_config_path,
    write_openclaw_mcp_config,
)
from tools.openapi_auth import (
    build_authorization_url,
    exchange_code_for_token,
    get_openapi_env_path,
    wait_for_oauth_callback,
    write_openapi_env,
)


def _print(data: Dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False))


def cmd_status(_: argparse.Namespace) -> int:
    configured, message = check_mcp_configured()
    _print(
        {
            "ok": True,
            "configured": configured,
            "message": message,
            "openclaw_config_path": str(get_openclaw_config_path()),
            "openapi_env_path": str(get_openapi_env_path()),
        }
    )
    return 0


def cmd_configure_openclaw(_: argparse.Namespace) -> int:
    path = write_openclaw_mcp_config()
    _print(
        {
            "ok": True,
            "config_path": str(path),
            "guide": build_openclaw_connect_guide(),
        }
    )
    return 0


def cmd_authorization_url(args: argparse.Namespace) -> int:
    url, state = build_authorization_url(
        args.client_id,
        redirect_uri=args.redirect_uri,
        scope=args.scope,
    )
    _print({"ok": True, "authorization_url": url, "state": state})
    return 0


def cmd_oauth_local(args: argparse.Namespace) -> int:
    url, state = build_authorization_url(
        args.client_id,
        redirect_uri=args.redirect_uri,
        scope=args.scope,
    )
    _print(
        {
            "ok": True,
            "step": "open_authorization_url",
            "authorization_url": url,
            "state": state,
        }
    )
    callback = wait_for_oauth_callback(
        expected_state=state,
        timeout_seconds=args.timeout,
    )
    if callback.error:
        _print({"ok": False, "error": callback.error})
        return 1

    token_data = exchange_code_for_token(
        args.client_id,
        args.client_secret,
        callback.code or "",
        redirect_uri=args.redirect_uri,
    )
    env_path = write_openapi_env(
        args.client_id,
        args.client_secret,
        token_data,
        redirect_uri=args.redirect_uri,
    )
    _print(
        {
            "ok": True,
            "step": "credentials_saved",
            "env_path": str(env_path),
            "scope": token_data.get("scope"),
        }
    )
    return 0


def cmd_serve_jsonl(_: argparse.Namespace) -> int:
    """最小 JSONL 循环，便于被外部 runtime 适配。"""

    handlers = {
        "status": lambda payload: {
            "ok": True,
            "configured": check_mcp_configured()[0],
            "message": check_mcp_configured()[1],
        },
        "configure-openclaw": lambda payload: {
            "ok": True,
            "config_path": str(write_openclaw_mcp_config()),
        },
        "authorization-url": lambda payload: {
            "ok": True,
            **dict(
                zip(
                    ("authorization_url", "state"),
                    build_authorization_url(
                        str(payload["client_id"]),
                        redirect_uri=str(
                            payload.get("redirect_uri", "http://localhost:38000/callback")
                        ),
                        scope=str(payload.get("scope", "tasks:read tasks:write")),
                    ),
                )
            ),
        },
    }

    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue
        try:
            payload = json.loads(raw)
            action = str(payload.get("action", ""))
            handler = handlers.get(action)
            if not handler:
                _print({"ok": False, "error": f"unsupported_action:{action}"})
                continue
            _print(handler(payload))
        except Exception as exc:  # noqa: BLE001
            _print({"ok": False, "error": str(exc)})
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Dida auth backend for MCPorter")
    subparsers = parser.add_subparsers(dest="command", required=False)

    status = subparsers.add_parser("status")
    status.set_defaults(func=cmd_status)

    configure = subparsers.add_parser("configure-openclaw")
    configure.set_defaults(func=cmd_configure_openclaw)

    auth_url = subparsers.add_parser("authorization-url")
    auth_url.add_argument("--client-id", required=True)
    auth_url.add_argument("--redirect-uri", default="http://localhost:38000/callback")
    auth_url.add_argument("--scope", default="tasks:read tasks:write")
    auth_url.set_defaults(func=cmd_authorization_url)

    oauth_local = subparsers.add_parser("oauth-local")
    oauth_local.add_argument("--client-id", required=True)
    oauth_local.add_argument("--client-secret", required=True)
    oauth_local.add_argument("--redirect-uri", default="http://localhost:38000/callback")
    oauth_local.add_argument("--scope", default="tasks:read tasks:write")
    oauth_local.add_argument("--timeout", type=int, default=180)
    oauth_local.set_defaults(func=cmd_oauth_local)

    serve_jsonl = subparsers.add_parser("serve-jsonl")
    serve_jsonl.set_defaults(func=cmd_serve_jsonl)

    parser.set_defaults(func=cmd_status)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

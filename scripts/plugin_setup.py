#!/usr/bin/env python3
"""Manage the Outsource plugin in Codex, Claude Code, or both."""

from __future__ import annotations

import argparse
import json
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_NAME = "outsource"
HOSTS = ("codex", "claude", "all")
CONFIG = {
    "codex": {
        "cli": "codex",
        "marketplace": "agent-harnesses",
        "selector": "outsource@agent-harnesses",
    },
    "claude": {
        "cli": "claude",
        "marketplace": "outsource-dev",
        "selector": "outsource@outsource-dev",
    },
}


class SetupError(RuntimeError):
    """Raised when setup cannot continue safely."""


def read_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SetupError(f"missing required file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SetupError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SetupError(f"{path} must contain a JSON object")
    return value


def entries_by_name(
    manifest: dict[str, Any],
    path: Path,
) -> dict[str, dict[str, Any]]:
    entries = manifest.get("plugins")
    if not isinstance(entries, list):
        raise SetupError(f"{path}: plugins must be an array")
    result: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("name"), str):
            raise SetupError(f"{path}: every plugin needs a string name")
        result[entry["name"]] = entry
    return result


def validate_repository() -> list[str]:
    errors: list[str] = []
    codex_plugin_path = (
        ROOT / "plugins" / PLUGIN_NAME / ".codex-plugin" / "plugin.json"
    )
    claude_plugin_path = (
        ROOT / "plugins" / PLUGIN_NAME / ".claude-plugin" / "plugin.json"
    )
    codex_marketplace_path = ROOT / ".agents" / "plugins" / "marketplace.json"
    claude_marketplace_path = ROOT / ".claude-plugin" / "marketplace.json"

    try:
        codex_plugin = read_object(codex_plugin_path)
        claude_plugin = read_object(claude_plugin_path)
        codex_marketplace = read_object(codex_marketplace_path)
        claude_marketplace = read_object(claude_marketplace_path)
    except SetupError as exc:
        return [str(exc)]

    for label, manifest in (
        ("Codex", codex_plugin),
        ("Claude", claude_plugin),
    ):
        if manifest.get("name") != PLUGIN_NAME:
            errors.append(f"{label} plugin name must be {PLUGIN_NAME!r}")
        if not isinstance(manifest.get("version"), str):
            errors.append(f"{label} plugin version must be a string")
        if (
            not isinstance(manifest.get("description"), str)
            or not manifest["description"].strip()
        ):
            errors.append(f"{label} plugin description must not be empty")
    if codex_plugin.get("version") != claude_plugin.get("version"):
        errors.append("Codex and Claude plugin versions must match")

    try:
        codex_entry = entries_by_name(
            codex_marketplace,
            codex_marketplace_path,
        )[PLUGIN_NAME]
    except (SetupError, KeyError) as exc:
        errors.append(f"Codex marketplace is missing Outsource: {exc}")
    else:
        source = codex_entry.get("source")
        if (
            not isinstance(source, dict)
            or source.get("source") != "local"
            or source.get("path") != "./plugins/outsource"
        ):
            errors.append("Codex Outsource source must be ./plugins/outsource")

    try:
        claude_entry = entries_by_name(
            claude_marketplace,
            claude_marketplace_path,
        )[PLUGIN_NAME]
    except (SetupError, KeyError) as exc:
        errors.append(f"Claude marketplace is missing Outsource: {exc}")
    else:
        if claude_entry.get("source") != "./plugins/outsource":
            errors.append("Claude Outsource source must be ./plugins/outsource")
        if claude_entry.get("version") != claude_plugin.get("version"):
            errors.append("Claude marketplace and plugin versions must match")

    if not (ROOT / "plugins" / PLUGIN_NAME / "skills" / "outsource" / "SKILL.md").is_file():
        errors.append("Outsource SKILL.md is missing")
    return errors


def require_cli(host: str) -> str:
    executable = shutil.which(str(CONFIG[host]["cli"]))
    if executable is None:
        raise SetupError(f"{CONFIG[host]['cli']} CLI was not found on PATH")
    return executable


def run(
    arguments: Sequence[str],
    *,
    capture_json: bool = False,
    dry_run: bool = False,
) -> Any:
    printable = shlex.join(arguments)
    if dry_run:
        print(f"$ {printable}")
        return None
    completed = subprocess.run(
        list(arguments),
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE if capture_json else None,
        stderr=subprocess.PIPE if capture_json else None,
    )
    if completed.returncode != 0:
        detail = ""
        if capture_json:
            detail = (completed.stderr or completed.stdout or "").strip()
        suffix = f"\n{detail}" if detail else ""
        raise SetupError(f"command failed: {printable}{suffix}")
    if not capture_json:
        return None
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise SetupError(f"CLI returned invalid JSON: {printable}") from exc


def marketplace_records(host: str, executable: str) -> list[dict[str, Any]]:
    payload = run(
        [executable, "plugin", "marketplace", "list", "--json"],
        capture_json=True,
    )
    if host == "codex":
        if not isinstance(payload, dict):
            raise SetupError("Codex returned an unexpected marketplace list")
        payload = payload.get("marketplaces", [])
    if not isinstance(payload, list):
        raise SetupError(f"{host} returned an unexpected marketplace list")
    return [item for item in payload if isinstance(item, dict)]


def plugin_records(host: str, executable: str) -> list[dict[str, Any]]:
    if host == "codex":
        payload = run(
            [executable, "plugin", "list", "--available", "--json"],
            capture_json=True,
        )
        if not isinstance(payload, dict):
            raise SetupError("Codex returned an unexpected plugin list")
        installed = payload.get("installed", [])
        return (
            [item for item in installed if isinstance(item, dict)]
            if isinstance(installed, list)
            else []
        )

    payload = run(
        [executable, "plugin", "list", "--json"],
        capture_json=True,
    )
    if not isinstance(payload, list):
        raise SetupError("Claude Code returned an unexpected plugin list")
    return [item for item in payload if isinstance(item, dict)]


def has_marketplace(host: str, executable: str) -> bool:
    name = CONFIG[host]["marketplace"]
    return any(
        item.get("name") == name
        for item in marketplace_records(host, executable)
    )


def find_plugin(host: str, executable: str) -> dict[str, Any] | None:
    selector = CONFIG[host]["selector"]
    return next(
        (
            item
            for item in plugin_records(host, executable)
            if item.get("pluginId") == selector or item.get("id") == selector
        ),
        None,
    )


def install_one(host: str, dry_run: bool) -> int:
    executable = require_cli(host)
    selector = str(CONFIG[host]["selector"])
    marketplace_add = [
        executable,
        "plugin",
        "marketplace",
        "add",
        str(ROOT),
    ]
    plugin_add = [
        executable,
        "plugin",
        "add" if host == "codex" else "install",
        selector,
    ]
    if dry_run:
        run(marketplace_add, dry_run=True)
        run(plugin_add, dry_run=True)
        return 0
    if not has_marketplace(host, executable):
        run(marketplace_add)
    run(plugin_add)
    plugin = find_plugin(host, executable)
    if plugin is None:
        raise SetupError(f"{host} did not report Outsource as installed")
    if host == "codex" and not plugin.get("enabled"):
        raise SetupError("Codex reported Outsource as disabled")
    if host == "claude" and plugin.get("enabled") is False:
        raise SetupError("Claude Code reported Outsource as disabled")
    print(
        f"{host}: Outsource {plugin.get('version', 'unknown')} is installed."
    )
    return 0


def selected_hosts(host: str) -> tuple[str, ...]:
    return ("codex", "claude") if host == "all" else (host,)


def doctor(host: str) -> int:
    errors = validate_repository()
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    for target in selected_hosts(host):
        if shutil.which(str(CONFIG[target]["cli"])) is None:
            print(f"warning: {CONFIG[target]['cli']} CLI is not on PATH")
    print("Outsource is structurally ready for Codex and Claude Code.")
    return 0


def install(host: str, dry_run: bool) -> int:
    errors = validate_repository()
    if errors:
        raise SetupError("; ".join(errors))
    for target in selected_hosts(host):
        result = install_one(target, dry_run)
        if result != 0:
            return result
    return 0


def update_one(host: str) -> int:
    executable = require_cli(host)
    if not has_marketplace(host, executable):
        return install_one(host, False)
    selector = str(CONFIG[host]["selector"])
    if host == "codex":
        run([executable, "plugin", "add", selector])
    else:
        run(
            [
                executable,
                "plugin",
                "marketplace",
                "update",
                str(CONFIG[host]["marketplace"]),
            ]
        )
        if find_plugin(host, executable) is None:
            return install_one(host, False)
        run([executable, "plugin", "update", selector])
    print(f"{host}: Outsource was updated; restart the host.")
    return 0


def update(host: str) -> int:
    for target in selected_hosts(host):
        result = update_one(target)
        if result != 0:
            return result
    return 0


def status_one(host: str) -> int:
    executable = require_cli(host)
    marketplace = has_marketplace(host, executable)
    plugin = find_plugin(host, executable)
    print(
        f"{host} marketplace: "
        f"{'configured' if marketplace else 'not configured'}"
    )
    if plugin is None:
        print(f"{host} plugin: not installed")
        return 1
    state = "enabled" if plugin.get("enabled", True) else "disabled"
    print(f"{host} plugin: {plugin.get('version', 'unknown')} ({state})")
    return 0 if state == "enabled" else 1


def status(host: str) -> int:
    results = [status_one(target) for target in selected_hosts(host)]
    return 0 if all(result == 0 for result in results) else 1


def uninstall_one(host: str, remove_marketplace: bool) -> int:
    executable = require_cli(host)
    selector = str(CONFIG[host]["selector"])
    if find_plugin(host, executable) is not None:
        run(
            [
                executable,
                "plugin",
                "remove" if host == "codex" else "uninstall",
                selector,
            ]
        )
    else:
        print(f"{host}: Outsource is not installed.")
    if remove_marketplace and has_marketplace(host, executable):
        run(
            [
                executable,
                "plugin",
                "marketplace",
                "remove",
                str(CONFIG[host]["marketplace"]),
            ]
        )
    return 0


def uninstall(host: str, remove_marketplace: bool) -> int:
    for target in selected_hosts(host):
        result = uninstall_one(target, remove_marketplace)
        if result != 0:
            return result
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage Outsource across supported agent hosts."
    )
    parser.add_argument(
        "--host",
        choices=HOSTS,
        default="codex",
        help="target host; defaults to codex",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor", help="validate the repository")
    install_parser = commands.add_parser("install", help="install Outsource")
    install_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print commands without changing host state",
    )
    commands.add_parser("update", help="update Outsource")
    commands.add_parser("status", help="show installation state")
    uninstall_parser = commands.add_parser(
        "uninstall",
        help="uninstall Outsource",
    )
    uninstall_parser.add_argument(
        "--remove-marketplace",
        action="store_true",
        help="also remove the development marketplace",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "doctor":
            return doctor(args.host)
        if args.command == "install":
            return install(args.host, args.dry_run)
        if args.command == "update":
            return update(args.host)
        if args.command == "status":
            return status(args.host)
        if args.command == "uninstall":
            return uninstall(args.host, args.remove_marketplace)
    except SetupError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

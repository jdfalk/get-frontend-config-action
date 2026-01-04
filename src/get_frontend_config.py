#!/usr/bin/env python3
# file: src/get_frontend_config.py
# version: 1.0.0
# guid: 91576341-f8a4-4c70-b67a-ab9ddee23565

"""Extract frontend configuration from repository-config.yml or provided YAML."""

from __future__ import annotations

import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    # Match load-config-action behavior: install PyYAML if missing.
    import subprocess

    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "PyYAML"])
    import yaml


DEFAULT_DIR = "web"
DEFAULT_NODE_VERSION = "22"


def write_output(name: str, value: str) -> None:
    """Write a named output to GITHUB_OUTPUT."""
    output_file = os.environ.get("GITHUB_OUTPUT")
    if not output_file:
        return

    with open(output_file, "a", encoding="utf-8") as handle:
        if "\n" in str(value):
            delimiter = "EOF"
            handle.write(f"{name}<<{delimiter}\n{value}\n{delimiter}\n")
        else:
            handle.write(f"{name}={value}\n")


def write_summary(text: str) -> None:
    """Write text to GITHUB_STEP_SUMMARY."""
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_file:
        return

    with open(summary_file, "a", encoding="utf-8") as handle:
        handle.write(text + "\n")


def parse_frontend_config(config_text: str) -> tuple[str, str, bool]:
    """Parse the frontend directory and Node version from YAML content."""
    if not config_text.strip():
        return DEFAULT_DIR, DEFAULT_NODE_VERSION, False

    try:
        data = yaml.safe_load(config_text) or {}
    except yaml.YAMLError as exc:
        raise RuntimeError(f"Failed to parse YAML: {exc}") from exc

    frontend_dir = DEFAULT_DIR
    node_version = DEFAULT_NODE_VERSION
    has_frontend = False

    working_dirs = data.get("working_directories") if isinstance(data, dict) else None
    if isinstance(working_dirs, dict):
        for key in ("frontend", "node"):
            value = working_dirs.get(key)
            if value:
                frontend_dir = str(value)
                has_frontend = True
                break

    versions = data.get("versions") if isinstance(data, dict) else None
    if isinstance(versions, dict) and "node" in versions:
        node_value = versions.get("node")
        if isinstance(node_value, (list, tuple)):
            for entry in node_value:
                if entry:
                    node_version = str(entry)
                    break
        elif node_value is not None:
            node_version = str(node_value)
        has_frontend = True

    return frontend_dir or DEFAULT_DIR, node_version or DEFAULT_NODE_VERSION, has_frontend


def main() -> None:
    """Load config content and emit outputs."""
    config_text = os.environ.get("REPOSITORY_CONFIG", "")
    config_file = Path(os.environ.get("CONFIG_FILE", ".github/repository-config.yml"))

    if not config_text.strip() and config_file.exists():
        config_text = config_file.read_text(encoding="utf-8")
        source = f"`{config_file}`"
    elif config_text.strip():
        source = "`repository-config` input"
    else:
        source = None

    if not config_text.strip():
        write_output("dir", DEFAULT_DIR)
        write_output("node-version", DEFAULT_NODE_VERSION)
        write_output("has-frontend", "false")
        message = (
            "⚠️ No repository configuration found; using defaults "
            f"(dir: {DEFAULT_DIR}, node-version: {DEFAULT_NODE_VERSION})"
        )
        print(message)
        write_summary(message)
        sys.exit(0)

    try:
        frontend_dir, node_version, has_frontend = parse_frontend_config(config_text)
    except Exception as exc:  # noqa: BLE001
        error_msg = f"::error::{exc}"
        print(error_msg)
        write_summary(f"❌ {exc}")
        write_output("dir", DEFAULT_DIR)
        write_output("node-version", DEFAULT_NODE_VERSION)
        write_output("has-frontend", "false")
        sys.exit(1)

    write_output("dir", frontend_dir)
    write_output("node-version", node_version)
    write_output("has-frontend", str(has_frontend).lower())

    summary_lines = [
        f"✅ Frontend configuration extracted from {source}",
        f"- Working directory: `{frontend_dir}`",
        f"- Node.js version: `{node_version}`",
        f"- Has frontend: `{str(has_frontend).lower()}`",
    ]
    print("\n".join(summary_lines))
    write_summary("\n".join(summary_lines))


if __name__ == "__main__":
    main()

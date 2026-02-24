"""
validate_repo.py

用于校验“MoFox 插件合集仓库”的基本规范是否满足：
- 每个插件目录必须包含：__init__.py / plugin.py / README.md
- __init__.py 里必须存在 __plugin_meta__ = PluginMetadata(...)
- README.md 必须包含至少一个指令示例（/xxx）

本脚本不依赖 MoFox-Core，也不会 import 插件代码（避免缺失依赖导致失败）。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PLUGIN_DIR_CANDIDATES = [
    "conversation_safety_guard",
    "simple_faq_knowledge",
    "scene_persona_switcher",
    "affinity_achievements",
    "log_sanitizer",
    "conversation_recap",
    "daily_checkin",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_plugin_dir(dir_path: Path) -> list[str]:
    errors: list[str] = []

    init_py = dir_path / "__init__.py"
    plugin_py = dir_path / "plugin.py"
    readme = dir_path / "README.md"

    for p in [init_py, plugin_py, readme]:
        if not p.exists():
            errors.append(f"missing file: {p.as_posix()}")

    if init_py.exists():
        content = read_text(init_py)
        if "__plugin_meta__" not in content:
            errors.append(f"{init_py.as_posix()}: missing __plugin_meta__")
        if "PluginMetadata" not in content:
            errors.append(f"{init_py.as_posix()}: missing PluginMetadata usage")

    if readme.exists():
        content = read_text(readme)
        # 允许 markdown 中的 ` /command ` 或以 / 开头的示例行
        if not re.search(r"(?m)(^|\\s|`)/[a-zA-Z]", content):
            errors.append(f"{readme.as_posix()}: no command example like /xxx found")

    return errors


def main() -> int:
    # Windows 控制台常见默认编码为 cp936/gbk，避免输出 emoji 导致报错
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass

    if not ROOT.exists():
        print("ERR: repo root not found")
        return 2

    any_errors: list[str] = []

    for name in PLUGIN_DIR_CANDIDATES:
        p = ROOT / name
        if not p.exists() or not p.is_dir():
            any_errors.append(f"missing plugin directory: {p.as_posix()}")
            continue
        any_errors.extend(check_plugin_dir(p))

    if any_errors:
        print("FAIL: validation failed with errors:")
        for e in any_errors:
            print(f"- {e}")
        return 1

    print("OK: validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""
export_all_plugins.py

一键把本仓库内的 7 个插件全部导出成“独立插件仓库”目录结构，输出到 exported/ 下。

用法：
  python tools/export_all_plugins.py

输出：
  exported/<plugin>-repo/ ...
"""

from __future__ import annotations

import sys
from pathlib import Path

from export_plugin_repo import main as export_one_main

ROOT = Path(__file__).resolve().parents[1]

PLUGINS = [
    "conversation_safety_guard",
    "simple_faq_knowledge",
    "scene_persona_switcher",
    "affinity_achievements",
    "log_sanitizer",
    "conversation_recap",
    "daily_checkin",
]


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass

    exported_root = ROOT / "exported"
    exported_root.mkdir(exist_ok=True)

    # 复用 export_plugin_repo.py 的 CLI 逻辑：临时改 sys.argv
    ok = 0
    failed: list[str] = []
    for p in PLUGINS:
        out = exported_root / f"{p}-repo"
        if out.exists():
            failed.append(f"{p}: output exists: {out}")
            continue
        argv_backup = sys.argv
        try:
            sys.argv = ["export_plugin_repo.py", p, str(out)]
            code = export_one_main()
            if code == 0:
                ok += 1
            else:
                failed.append(f"{p}: export failed with code {code}")
        except Exception as e:
            failed.append(f"{p}: export exception: {e}")
        finally:
            sys.argv = argv_backup

    print(f"OK: exported {ok}/{len(PLUGINS)} plugins into {exported_root}")
    if failed:
        print("WARN: some exports failed:")
        for line in failed:
            print(f"- {line}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

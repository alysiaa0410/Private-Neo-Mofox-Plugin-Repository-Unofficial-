"""
export_plugin_repo.py

把本仓库中的某个插件文件夹导出为“独立插件仓库”的目录结构（更符合 MoFox 插件生态）。

用法：
  python tools/export_plugin_repo.py <plugin_folder> [output_dir]

示例：
  python tools/export_plugin_repo.py conversation_safety_guard exported/conversation_safety_guard-repo

导出结果（示例）：
  exported/conversation_safety_guard-repo/
    __init__.py
    LICENSE
    .gitignore
    README.md
    conversation_safety_guard/
      __init__.py
      plugin.py
      README.md
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def die(msg: str) -> None:
    print(f"ERR: {msg}")
    raise SystemExit(2)


def copy_tree(src: Path, dst: Path) -> None:
    if not src.exists() or not src.is_dir():
        die(f"source plugin dir not found: {src}")
    if dst.exists():
        die(f"output dir already exists: {dst}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass

    if len(sys.argv) < 2:
        die("参数不足：需要 plugin_folder（例如 conversation_safety_guard）")

    plugin_folder = sys.argv[1].strip()
    if not plugin_folder or "/" in plugin_folder or "\\" in plugin_folder:
        die("plugin_folder 不合法，请传入本仓库中的插件目录名")

    src_plugin = ROOT / plugin_folder
    if not src_plugin.exists():
        die(f"插件目录不存在：{src_plugin}")

    out_dir = (
        Path(sys.argv[2]).resolve()
        if len(sys.argv) >= 3
        else (ROOT / "exported" / f"{plugin_folder}-repo")
    )

    out_dir.mkdir(parents=True, exist_ok=False)

    # 1) 根 __init__.py
    (out_dir / "__init__.py").write_text("", encoding="utf-8")

    # 2) 拷贝插件目录
    copy_tree(src_plugin, out_dir / plugin_folder)

    # 3) 根 README.md：复制插件 README（如果存在）
    plugin_readme = src_plugin / "README.md"
    if plugin_readme.exists():
        (out_dir / "README.md").write_text(
            plugin_readme.read_text(encoding="utf-8"), encoding="utf-8"
        )
    else:
        (out_dir / "README.md").write_text(
            f"## {plugin_folder}\n\n本仓库由插件合集导出生成，请补充 README。\n",
            encoding="utf-8",
        )

    # 4) 复制 LICENSE 与 .gitignore（如果合集仓库有）
    for name in ["LICENSE", ".gitignore"]:
        src = ROOT / name
        if src.exists():
            (out_dir / name).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    print(f"OK: exported to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

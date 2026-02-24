"""
generate_registry_entries.py

从本仓库的各插件目录读取 __init__.py 中的 __plugin_meta__ 信息，
生成两份“可用于提交到 MoFox-Plugin-Repo 的 JSON 草稿”：

- plugins.json（只包含 id + repositoryUrl）
- plugin_details.json（包含 manifest）

注意：
- 本脚本不会 import MoFox-Core（避免环境缺依赖）
- 只解析 __init__.py 里 __plugin_meta__ = PluginMetadata(...) 的字面量参数

用法：
  python tools/generate_registry_entries.py > registry_dump.json

或：
  python tools/generate_registry_entries.py --out-dir registry
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def ast_literal(node: ast.AST) -> Any:
    """尽量把 AST 节点还原成 Python 字面量；失败则返回 None。"""
    try:
        return ast.literal_eval(node)
    except Exception:
        return None


def parse_plugin_meta(init_py: Path) -> dict[str, Any] | None:
    tree = ast.parse(read_text(init_py))
    for stmt in tree.body:
        if not isinstance(stmt, ast.Assign):
            continue
        if not any(isinstance(t, ast.Name) and t.id == "__plugin_meta__" for t in stmt.targets):
            continue
        if not isinstance(stmt.value, ast.Call):
            continue
        # 只关心 PluginMetadata(...)
        call = stmt.value
        if isinstance(call.func, ast.Name) and call.func.id != "PluginMetadata":
            continue

        meta: dict[str, Any] = {}
        for kw in call.keywords:
            if kw.arg is None:
                continue
            meta[kw.arg] = ast_literal(kw.value)
        return meta
    return None


def infer_id_from_repository_url(repo_url: str | None) -> str | None:
    """
    MoFox-Plugin-Repo 的 id 没有强制格式，这里给一个常见做法：
    - 用 GitHub 仓库 full name: owner.repo
    """
    if not repo_url:
        return None
    if "github.com/" not in repo_url:
        return None
    tail = repo_url.split("github.com/", 1)[1].strip("/")
    if not tail:
        return None
    parts = tail.split("/")
    if len(parts) < 2:
        return None
    owner, repo = parts[0], parts[1].removesuffix(".git")
    return f"{owner}.{repo}"


def collect_plugins() -> list[dict[str, Any]]:
    plugins: list[dict[str, Any]] = []
    for child in ROOT.iterdir():
        if not child.is_dir():
            continue
        if child.name in {".github", "tools", "scripts", "exported"}:
            continue
        init_py = child / "__init__.py"
        if not init_py.exists():
            continue
        meta = parse_plugin_meta(init_py)
        if not meta:
            continue
        meta["_folder"] = child.name
        plugins.append(meta)
    return plugins


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass

    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", default="", help="输出目录（可选），例如 registry")
    args = parser.parse_args()

    plugins = collect_plugins()
    plugins_sorted = sorted(plugins, key=lambda x: str(x.get("_folder")))

    plugins_json = []
    details_json = []

    for meta in plugins_sorted:
        repo_url = meta.get("repository_url")
        plugin_id = infer_id_from_repository_url(repo_url) or str(meta.get("_folder"))

        plugins_json.append(
            {
                "id": plugin_id,
                "repositoryUrl": repo_url or "",
            }
        )

        manifest = {
            "name": meta.get("name"),
            "description": meta.get("description"),
            "usage": meta.get("usage"),
            "version": meta.get("version"),
            "author": meta.get("author"),
            "license": meta.get("license"),
            "repository_url": repo_url,
            "keywords": meta.get("keywords") or [],
            "extra": meta.get("extra") or {},
            "python_dependencies": meta.get("python_dependencies") or [],
        }

        details_json.append(
            {
                "id": plugin_id,
                "manifest": manifest,
            }
        )

    payload = {"plugins.json": plugins_json, "plugin_details.json": details_json}

    if args.out_dir:
        out = (ROOT / args.out_dir).resolve()
        out.mkdir(parents=True, exist_ok=True)
        (out / "plugins.json").write_text(
            json.dumps(plugins_json, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (out / "plugin_details.json").write_text(
            json.dumps(details_json, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"OK: wrote {len(plugins_json)} plugins to {out}")
        return 0

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

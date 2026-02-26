"""
scaffold_mofox_plugin.py

一个简单的 MoFox 插件脚手架生成器（面向新手）。

用法：
  python tools/scaffold_mofox_plugin.py plugin_folder_name "插件中文名" "/command"

示例：
  python tools/scaffold_mofox_plugin.py weather_helper "天气查询插件" "/weather"
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def die(msg: str) -> None:
    print(f"ERR: {msg}")
    raise SystemExit(2)


def main() -> int:
    # Windows 控制台默认编码可能为 cp936/gbk，这里尽量切到 utf-8
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass

    if len(sys.argv) < 4:
        die("参数不足：需要 plugin_folder_name, 插件中文名, /command")

    folder = sys.argv[1].strip()
    cn_name = sys.argv[2].strip()
    command = sys.argv[3].strip()

    if not folder or "/" in folder or "\\" in folder:
        die("plugin_folder_name 不合法，请使用类似 my_plugin_name 的形式")
    if not command.startswith("/"):
        die("command 必须以 / 开头，例如 /hello")

    target = ROOT / folder
    if target.exists():
        die(f"目标目录已存在：{target}")

    target.mkdir(parents=True, exist_ok=False)

    (target / "__init__.py").write_text(
        f'''from src.plugin_system.base.plugin_metadata import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="{cn_name}",
    description="请填写插件简介。",
    usage="用法示例：{command} 参数",
    version="0.1.0",
    author="yourname",
    license="MIT",
    repository_url="https://github.com/yourname/{folder}",
    keywords=["mofox", "plugin"],
    extra={{
        "plugin_type": "tools",
        "chat_type": "all",
        "is_built_in": False,
        "min_bot_version": "1.0.0",
    }},
    python_dependencies=[],
)
''',
        encoding="utf-8",
    )

    (target / "plugin.py").write_text(
        f'''"""
{cn_name}

这是一个 MoFox 插件脚手架生成的最小可运行示例。
你只需要在 execute() 中写具体逻辑即可。
"""

from typing import ClassVar, Type

from src.plugin_system import register_plugin
from src.plugin_system.base.base_plugin import BasePlugin
from src.plugin_system.base.command_args import CommandArgs
from src.plugin_system.base.component_types import ChatType, PlusCommandInfo, PermissionNodeField
from src.plugin_system.base.plus_command import PlusCommand
from src.plugin_system.utils.permission_decorators import require_permission


class MainCommand(PlusCommand):
    command_name: str = "{command.lstrip("/")}"
    command_description: str = "{cn_name} 的主命令"
    command_aliases: ClassVar[list[str]] = []
    chat_type_allow: ChatType = ChatType.ALL
    priority: int = 10

    @require_permission("use", deny_message="❌ 你没有权限使用该功能")
    async def execute(self, args: CommandArgs) -> tuple[bool, str | None, bool]:
        raw = (args.raw_args or "").strip()
        await self.send_text(f"你触发了 {command}，参数为：{{raw if raw else '(无)'}}")
        return True, "ok", True


@register_plugin
class {folder.title().replace("_", "")}Plugin(BasePlugin):
    plugin_name: str = "{folder}"
    enable_plugin: bool = True
    config_file_name: str = "config.toml"

    def get_plugin_components(self) -> list[tuple[PlusCommandInfo, Type[PlusCommand]]]:
        return [(MainCommand.get_plus_command_info(), MainCommand)]

    permission_nodes: ClassVar[list[PermissionNodeField]] = [
        PermissionNodeField(node_name="use", description="允许使用主命令"),
    ]
''',
        encoding="utf-8",
    )

    (target / "README.md").write_text(
        f"""## {cn_name}（{folder}）

### 功能

请填写插件功能说明。

### 指令

- `{command} 参数`

### 权限节点

- `{folder}.use`
""",
        encoding="utf-8",
    )

    print(f"OK: scaffold generated at {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

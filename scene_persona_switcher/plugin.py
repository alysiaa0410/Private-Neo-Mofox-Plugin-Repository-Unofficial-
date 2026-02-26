"""
多角色预设与场景切换插件

多角色预设与场景切换示例插件。
"""

from typing import ClassVar

from src.plugin_system import register_plugin
from src.plugin_system.base.base_plugin import BasePlugin
from src.plugin_system.base.command_args import CommandArgs
from src.plugin_system.base.component_types import ChatType, PermissionNodeField, PlusCommandInfo
from src.plugin_system.base.plus_command import PlusCommand
from src.plugin_system.utils.permission_decorators import require_permission

from .config import SceneConfig
from .handlers import SceneManager


class SceneCommand(PlusCommand):
    """切换会话的人设/场景，并给出推荐提示词"""

    command_name: str = "scene"
    command_description: str = "查看或切换当前会话的人设/场景预设"
    command_aliases: ClassVar[list[str]] = ["场景", "人设"]
    chat_type_allow: ChatType = ChatType.ALL
    priority: int = 15

    def __init__(self):
        super().__init__()
        self.config = SceneConfig()
        self.manager = SceneManager(self.config.SCENES)

    @require_permission("use", deny_message="❌ 你没有权限使用场景切换功能")
    async def execute(self, args: CommandArgs) -> tuple[bool, str | None, bool]:
        raw = (args.raw_args or "").strip()
        if not raw or raw.lower() == "list":
            return await self._show_scene_list(args)

        # 按场景中文名匹配
        scene = self.manager.get_scene(raw)
        if not scene:
            await self.send_text(
                f"未找到名为 "{raw}" 的场景。\n可使用 `/scene list` 查看可用场景列表。"
            )
            return True, None, False

        chat_id = getattr(args, "chat_id", None)
        user_id = getattr(args, "user_id", None)
        session_key = self.manager.get_session_key(chat_id, user_id)
        self.manager.set_session_scene(session_key, scene.key)

        reply = (
            f"✅ 已切换到场景：{scene.display_name}\n"
            f"简介：{scene.description}\n\n"
            "以下是推荐的人设提示词，可根据需要整合到 KFC/AFC 配置或其他 Prompt 注入插件中：\n\n"
            f"{scene.prompt_suggestion}"
        )
        await self.send_text(reply)
        return True, f"切换场景到 {scene.display_name}", True

    async def _show_scene_list(self, args: CommandArgs) -> tuple[bool, str | None, bool]:
        lines = ["📑 当前可用场景："]
        for key, scene in self.manager.list_scenes():
            lines.append(f"- {key}：{scene.display_name} —— {scene.description}")

        chat_id = getattr(args, "chat_id", None)
        user_id = getattr(args, "user_id", None)
        session_key = self.manager.get_session_key(chat_id, user_id)
        current = self.manager.get_session_scene(session_key)
        
        if current:
            for scene in self.config.SCENES.values():
                if scene.key == current:
                    lines.append(f"\n当前会话已选择场景：{scene.display_name}")
                    break

        await self.send_text("\n".join(lines))
        return True, None, False


@register_plugin
class ScenePersonaSwitcherPlugin(BasePlugin):
    """插件入口类"""

    plugin_name: str = "scene_persona_switcher"
    enable_plugin: bool = True
    config_file_name: str = "config.toml"

    def get_plugin_components(self) -> list[tuple[PlusCommandInfo, type[PlusCommand]]]:
        return [(SceneCommand.get_plus_command_info(), SceneCommand)]

    permission_nodes: ClassVar[list[PermissionNodeField]] = [
        PermissionNodeField(
            node_name="use",
            description="可以使用 /scene 指令查看与切换场景预设",
        )
    ]


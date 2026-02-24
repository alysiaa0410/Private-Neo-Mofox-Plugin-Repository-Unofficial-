"""
Scene Persona Switcher Plugin

多角色预设与场景切换示例插件。

特点：
- 预置多种人设/场景（学习助手、日常闲聊、严肃顾问等）；
- 使用 `/scene` 指令在不同场景之间切换，并返回推荐的提示词文本；
- 你可以将这些提示词复制到 MoFox 的 KFC/AFC 配置中，或配合其他 Prompt 注入类插件一起使用。
"""

from dataclasses import dataclass
from typing import ClassVar, Dict, Type

from src.plugin_system import register_plugin
from src.plugin_system.base.base_plugin import BasePlugin
from src.plugin_system.base.command_args import CommandArgs
from src.plugin_system.base.component_types import ChatType, PlusCommandInfo
from src.plugin_system.base.plus_command import PlusCommand
from src.plugin_system.base.component_types import PermissionNodeField
from src.plugin_system.utils.permission_decorators import require_permission


@dataclass
class SceneDefinition:
    key: str
    display_name: str
    description: str
    prompt_suggestion: str


SCENES: Dict[str, SceneDefinition] = {
    "学习": SceneDefinition(
        key="study",
        display_name="学习助手模式",
        description="适合讲解知识、刷题、辅导学习任务。",
        prompt_suggestion=(
            "你是一名耐心细致的学习助手，擅长用循序渐进的方式讲解概念，并通过例题帮助用户理解。\n"
            "回答时请：\n"
            "- 用简体中文\n"
            "- 优先从直观理解出发，再给出正式定义\n"
            "- 对于复杂问题，分步骤说明，并给出 1~2 个例子\n"
        ),
    ),
    "吐槽": SceneDefinition(
        key="casual_talk",
        display_name="吐槽搭子模式",
        description="适合轻松聊天、吐槽日常，风格更口语化。",
        prompt_suggestion=(
            "你是一个语气轻松、会适度接梗的聊天搭子，"
            "在不突破安全边界的前提下，可以适当使用口语和一点点网络用语，让氛围轻松愉快。\n"
            "回答时请：\n"
            "- 用简体中文\n"
            "- 注意共情和接话，而不是严肃说教\n"
            "- 遇到敏感或负面情绪时，语气要温和，避免刺激对方\n"
        ),
    ),
    "严肃": SceneDefinition(
        key="serious_advisor",
        display_name="严肃顾问模式",
        description="适合做决策分析、项目规划等，需要更稳重的表达风格。",
        prompt_suggestion=(
            "你是一名相对严肃、理性的顾问型助手，擅长分析利弊、给出结构化建议。\n"
            "回答时请：\n"
            "- 用简体中文\n"
            "- 先简要总结结论，再用条目列出原因或步骤\n"
            "- 避免夸张、戏谑和过于口语化的表达\n"
        ),
    ),
}


class SceneCommand(PlusCommand):
    """切换会话的人设/场景，并给出推荐提示词。"""

    command_name: str = "scene"
    command_description: str = "查看或切换当前会话的人设/场景预设"
    command_aliases: ClassVar[list[str]] = ["场景", "人设"]
    chat_type_allow: ChatType = ChatType.ALL
    priority: int = 15

    _session_scene: Dict[str, str] = {}

    @require_permission("use", deny_message="❌ 你没有权限使用场景切换功能")
    async def execute(self, args: CommandArgs) -> tuple[bool, str | None, bool]:
        """
        执行命令。

        - /scene list          查看可用场景
        - /scene 学习          切换到“学习助手”模式
        - /scene 吐槽          切换到“吐槽搭子”模式
        - /scene 严肃          切换到“严肃顾问”模式
        """
        raw = (args.raw_args or "").strip()
        if not raw or raw.lower() == "list":
            return await self._show_scene_list(args)

        # 这里我们简单地按场景中文名匹配
        scene = SCENES.get(raw)
        if not scene:
            await self.send_text(
                "未找到名为 “{}” 的场景。\n可使用 `/scene list` 查看可用场景列表。".format(raw)
            )
            return True, None, False

        session_key = self._get_session_key(args)
        self._session_scene[session_key] = scene.key

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
        for key, scene in SCENES.items():
            lines.append(f"- {key}：{scene.display_name} —— {scene.description}")

        session_key = self._get_session_key(args)
        current = self._session_scene.get(session_key)
        if current:
            for scene in SCENES.values():
                if scene.key == current:
                    lines.append(f"\n当前会话已选择场景：{scene.display_name}")
                    break

        await self.send_text("\n".join(lines))
        return True, None, False

    def _get_session_key(self, args: CommandArgs) -> str:
        """
        尝试构造一个“会话键”。

        由于不同版本的 CommandArgs 字段可能略有差异，这里采取一个相对保守的做法：
        - 优先使用 chat_id + user_id
        - 如果字段不存在，就退化为一个固定 key
        """
        chat_id = getattr(args, "chat_id", None)
        user_id = getattr(args, "user_id", None)
        if chat_id is not None and user_id is not None:
            return f"{chat_id}:{user_id}"
        return "global"


@register_plugin
class ScenePersonaSwitcherPlugin(BasePlugin):
    """插件入口类。"""

    plugin_name: str = "scene_persona_switcher"
    enable_plugin: bool = True
    config_file_name: str = "config.toml"

    def get_plugin_components(self) -> list[tuple[PlusCommandInfo, Type[PlusCommand]]]:
        return [(SceneCommand.get_plus_command_info(), SceneCommand)]

    permission_nodes: ClassVar[list[PermissionNodeField]] = [
        PermissionNodeField(
            node_name="use",
            description="可以使用 /scene 指令查看与切换场景预设",
        )
    ]


"""
对话情绪分析与安全建议插件

一个轻量级的情绪分析与安全建议插件示例。
"""

from typing import ClassVar

from src.plugin_system import register_plugin
from src.plugin_system.base.base_plugin import BasePlugin
from src.plugin_system.base.command_args import CommandArgs
from src.plugin_system.base.component_types import ChatType, PermissionNodeField, PlusCommandInfo
from src.plugin_system.base.plus_command import PlusCommand
from src.plugin_system.utils.permission_decorators import require_permission

from .config import SafetyConfig
from .handlers import MoodAnalyzer


class MoodCheckCommand(PlusCommand):
    """对一段文本做情绪倾向分析，并给出安全建议"""

    command_name: str = "mood"
    command_description: str = "分析一段话的情绪倾向并给出安全建议"
    command_aliases: ClassVar[list[str]] = ["心情检测", "情绪分析"]
    chat_type_allow: ChatType = ChatType.ALL
    priority: int = 20

    def __init__(self):
        super().__init__()
        self.config = SafetyConfig()
        self.analyzer = MoodAnalyzer(
            negative_keywords=self.config.negative_keywords,
            danger_keywords=self.config.danger_keywords,
            positive_keywords=self.config.positive_keywords
        )

    @require_permission("use", deny_message="❌ 你没有权限使用情绪分析功能")
    async def execute(self, args: CommandArgs) -> tuple[bool, str | None, bool]:
        text = (args.raw_args or "").strip()
        if not text:
            await self.send_text("请在指令后面加上一段需要分析的文本，例如：/mood 我最近有点累。")
            return True, None, False

        category, score = self.analyzer.classify_emotion(text)
        suggestion = self.analyzer.build_suggestion(category)

        reply = (
            "🧠 情绪检测结果：\n"
            f"- 粗略判断：{category}\n"
            f"- 情绪强度：{int(score * 100)} / 100\n\n"
            f"💡 建议：{suggestion}\n\n"
            "⚠️ 说明：\n"
            "本功能仅基于关键词进行简单判断，不构成专业意见；"
            "如果你正处于严重的情绪困扰或危险境地，请优先联系身边可信任的人或专业机构。"
        )
        await self.send_text(reply)
        return True, "已返回情绪分析结果", True


@register_plugin
class ConversationSafetyGuardPlugin(BasePlugin):
    """插件入口类"""

    plugin_name: str = "conversation_safety_guard"
    enable_plugin: bool = True
    config_file_name: str = "config.toml"

    def get_plugin_components(self) -> list[tuple[PlusCommandInfo, type[PlusCommand]]]:
        return [(MoodCheckCommand.get_plus_command_info(), MoodCheckCommand)]

    permission_nodes: ClassVar[list[PermissionNodeField]] = [
        PermissionNodeField(
            node_name="use",
            description="可以使用 /mood 情绪分析指令",
        )
    ]


"""
对话简要回顾插件

一个基于近期消息的简单对话回顾插件。
"""

from typing import ClassVar

from src.plugin_system import register_plugin
from src.plugin_system.apis import message_api
from src.plugin_system.base.base_plugin import BasePlugin
from src.plugin_system.base.command_args import CommandArgs
from src.plugin_system.base.component_types import ChatType, PermissionNodeField, PlusCommandInfo
from src.plugin_system.base.plus_command import PlusCommand
from src.plugin_system.utils.permission_decorators import require_permission

from .config import RecapConfig
from .handlers import RecapHandler


class RecapCommand(PlusCommand):
    """生成近期对话的小结"""

    command_name: str = "recap"
    command_description: str = "对当前会话的近期消息生成简单回顾"
    command_aliases: ClassVar[list[str]] = ["回顾", "小结"]
    chat_type_allow: ChatType = ChatType.ALL
    priority: int = 10

    def __init__(self):
        super().__init__()
        self.config = RecapConfig()
        self.handler = RecapHandler(
            max_messages=self.config.max_messages,
            preview_limit=self.config.preview_limit
        )

    @require_permission("use", deny_message="❌ 你没有权限使用对话回顾功能")
    async def execute(self, args: CommandArgs) -> tuple[bool, str | None, bool]:
        chat_id = getattr(args, "chat_id", None)
        if chat_id is None:
            await self.send_text("当前环境无法识别会话 ID（chat_id），暂时不能生成回顾。")
            return True, None, False

        await self.send_text("📝 正在整理最近的对话内容，请稍候...")

        messages = await self.handler.fetch_recent_messages(message_api, str(chat_id))
        if not messages:
            await self.send_text("还没有可以回顾的历史消息。")
            return True, None, False

        # 按时间正序展示
        messages = list(reversed(messages))
        lines = ["📚 近期对话回顾（基于最近若干条消息）："]
        lines.extend(self.handler.format_messages(messages))

        await self.send_text("\n".join(lines))
        return True, "已返回近期对话回顾", True


@register_plugin
class ConversationRecapPlugin(BasePlugin):
    """插件入口类"""

    plugin_name: str = "conversation_recap"
    enable_plugin: bool = True
    config_file_name: str = "config.toml"

    def get_plugin_components(self) -> list[tuple[PlusCommandInfo, type[PlusCommand]]]:
        return [(RecapCommand.get_plus_command_info(), RecapCommand)]

    permission_nodes: ClassVar[list[PermissionNodeField]] = [
        PermissionNodeField(
            node_name="use",
            description="可以使用 /recap 指令生成对话回顾",
        )
    ]


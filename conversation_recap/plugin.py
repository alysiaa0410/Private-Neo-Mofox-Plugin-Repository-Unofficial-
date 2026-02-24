"""
Conversation Recap Plugin

一个基于近期消息的简单对话回顾插件。

说明：
- 通过 /recap 指令，从当前会话中读取最近若干条消息；
- 将其中的对话按时间顺序整理成列表，便于快速回顾；
- 为了适配不同版本的 message_api，本实现会优先尝试按 chat_id 拉取，
  若接口不存在则退化为按时间拉取后再筛选。
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, ClassVar

from src.plugin_system import register_plugin
from src.plugin_system.apis import message_api
from src.plugin_system.base.base_plugin import BasePlugin
from src.plugin_system.base.command_args import CommandArgs
from src.plugin_system.base.component_types import ChatType, PermissionNodeField, PlusCommandInfo
from src.plugin_system.base.plus_command import PlusCommand
from src.plugin_system.utils.permission_decorators import require_permission


def _preview(text: str, limit: int = 60) -> str:
    s = (text or "").strip().replace("\n", " ")
    if len(s) <= limit:
        return s
    return s[: limit - 3] + "..."


def _role_prefix(role: str) -> str:
    r = (role or "").lower()
    if "user" in r:
        return "你："
    if "assistant" in r or "bot" in r:
        return "Bot："
    return "："


class RecapCommand(PlusCommand):
    """生成近期对话的小结。"""

    command_name: str = "recap"
    command_description: str = "对当前会话的近期消息生成简单回顾"
    command_aliases: ClassVar[list[str]] = ["回顾", "小结"]
    chat_type_allow: ChatType = ChatType.ALL
    priority: int = 10

    MAX_MESSAGES: int = 30

    @require_permission("use", deny_message="❌ 你没有权限使用对话回顾功能")
    async def execute(self, args: CommandArgs) -> tuple[bool, str | None, bool]:
        chat_id = getattr(args, "chat_id", None)
        if chat_id is None:
            await self.send_text("当前环境无法识别会话 ID（chat_id），暂时不能生成回顾。")
            return True, None, False

        await self.send_text("📝 正在整理最近的对话内容，请稍候...")

        messages = await self._fetch_recent_messages(chat_id=str(chat_id))
        if not messages:
            await self.send_text("还没有可以回顾的历史消息。")
            return True, None, False

        # 按时间正序展示
        messages = list(reversed(messages))
        lines: list[str] = ["📚 近期对话回顾（基于最近若干条消息）："]

        for msg in messages:
            content = str(msg.get("content") or "")
            if not content.strip():
                continue
            role = str(msg.get("role") or msg.get("sender") or "")
            lines.append(f"- {_role_prefix(role)} {_preview(content)}")

        await self.send_text("\n".join(lines))
        return True, "已返回近期对话回顾", True

    async def _fetch_recent_messages(self, chat_id: str) -> list[dict[str, Any]]:
        """
        尝试从 message_api 获取当前会话的近期消息。
        - 优先使用 get_messages_by_chat_id(chat_id, limit)
        - 若不存在，则退化为 get_messages_by_time(start_time, end_time) 并筛选 chat_id
        """
        getter = getattr(message_api, "get_messages_by_chat_id", None)
        if callable(getter):
            try:
                return await getter(chat_id=chat_id, limit=self.MAX_MESSAGES)
            except TypeError:
                # 部分版本参数名可能不同，尝试位置参数
                return await getter(chat_id, self.MAX_MESSAGES)

        # fallback：按时间拉取后筛选
        now = datetime.now()
        start = now - timedelta(days=1)
        time_getter = getattr(message_api, "get_messages_by_time", None)
        if not callable(time_getter):
            return []

        all_messages = await time_getter(start_time=start.timestamp(), end_time=now.timestamp())
        # 过滤 chat_id
        filtered = [m for m in all_messages if str(m.get("chat_id")) == str(chat_id)]
        return filtered[-self.MAX_MESSAGES :]


@register_plugin
class ConversationRecapPlugin(BasePlugin):
    """插件入口类。"""

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

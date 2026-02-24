"""
Log Sanitizer Plugin

一个示例性的日志隐私脱敏插件。

说明：
- 提供 /sanitize 指令，对文本中的手机号、邮箱等做基础掩码；
- 可以作为实现日志中间件/过滤器时的思路参考；
- 依赖纯标准库正则，方便修改和扩展。
"""

import re
from typing import ClassVar, Type

from src.plugin_system import register_plugin
from src.plugin_system.base.base_plugin import BasePlugin
from src.plugin_system.base.command_args import CommandArgs
from src.plugin_system.base.component_types import ChatType, PlusCommandInfo
from src.plugin_system.base.plus_command import PlusCommand
from src.plugin_system.base.component_types import PermissionNodeField
from src.plugin_system.utils.permission_decorators import require_permission


PHONE_PATTERN = re.compile(r"(1[3-9]\d{9})")
EMAIL_PATTERN = re.compile(r"([a-zA-Z0-9_.+-]+)@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
ID_PATTERN = re.compile(r"\b(\d{6})(\d{8})(\d{3}[0-9Xx])\b")


def sanitize_text(text: str) -> str:
    """对文本进行简单脱敏。"""

    def _mask_phone(m: re.Match) -> str:
        s = m.group(1)
        return s[:3] + "****" + s[-4:]

    def _mask_email(m: re.Match) -> str:
        name, domain = m.groups()
        if len(name) <= 2:
            masked = "*" * len(name)
        else:
            masked = name[0] + "*" * (len(name) - 2) + name[-1]
        return masked + "@" + domain

    def _mask_id(m: re.Match) -> str:
        head, mid, tail = m.groups()
        return head + "********" + tail

    text = PHONE_PATTERN.sub(_mask_phone, text)
    text = EMAIL_PATTERN.sub(_mask_email, text)
    text = ID_PATTERN.sub(_mask_id, text)
    return text


class SanitizeCommand(PlusCommand):
    """对一段文本进行隐私脱敏。"""

    command_name: str = "sanitize"
    command_description: str = "对文本中的手机号、邮箱、身份证号等进行基础脱敏"
    command_aliases: ClassVar[list[str]] = ["脱敏", "mask"]
    chat_type_allow: ChatType = ChatType.ALL
    priority: int = 10

    @require_permission("use", deny_message="❌ 你没有权限使用脱敏功能")
    async def execute(self, args: CommandArgs) -> tuple[bool, str | None, bool]:
        raw = (args.raw_args or "").strip()
        if not raw:
            await self.send_text(
                "请在指令后面带上需要脱敏的文本，例如：\n"
                "/sanitize 我的号码是 13812345678，邮箱 xxx@example.com"
            )
            return True, None, False

        masked = sanitize_text(raw)
        reply = "🔐 脱敏结果：\n" f"原文：{raw}\n" f"脱敏：{masked}"
        await self.send_text(reply)
        return True, "已返回脱敏结果", True


@register_plugin
class LogSanitizerPlugin(BasePlugin):
    """插件入口类。"""

    plugin_name: str = "log_sanitizer"
    enable_plugin: bool = True
    config_file_name: str = "config.toml"

    def get_plugin_components(self) -> list[tuple[PlusCommandInfo, Type[PlusCommand]]]:
        return [(SanitizeCommand.get_plus_command_info(), SanitizeCommand)]

    permission_nodes: ClassVar[list[PermissionNodeField]] = [
        PermissionNodeField(
            node_name="use",
            description="可以使用 /sanitize 指令进行文本脱敏",
        )
    ]


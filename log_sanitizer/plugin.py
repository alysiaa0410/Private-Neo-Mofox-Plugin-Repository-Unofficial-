"""
日志隐私脱敏插件

一个示例性的日志隐私脱敏插件。
"""

from typing import ClassVar

from src.plugin_system import register_plugin
from src.plugin_system.base.base_plugin import BasePlugin
from src.plugin_system.base.command_args import CommandArgs
from src.plugin_system.base.component_types import ChatType, PermissionNodeField, PlusCommandInfo
from src.plugin_system.base.plus_command import PlusCommand
from src.plugin_system.utils.permission_decorators import require_permission

from .config import SanitizerConfig
from .handlers import TextSanitizer


class SanitizeCommand(PlusCommand):
    """对一段文本进行隐私脱敏"""

    command_name: str = "sanitize"
    command_description: str = "对文本中的手机号、邮箱、身份证号等进行基础脱敏"
    command_aliases: ClassVar[list[str]] = ["脱敏", "mask"]
    chat_type_allow: ChatType = ChatType.ALL
    priority: int = 10

    def __init__(self):
        super().__init__()
        self.config = SanitizerConfig()
        self.sanitizer = TextSanitizer(
            enable_phone=self.config.enable_phone_mask,
            enable_email=self.config.enable_email_mask,
            enable_id=self.config.enable_id_mask
        )

    @require_permission("use", deny_message="❌ 你没有权限使用脱敏功能")
    async def execute(self, args: CommandArgs) -> tuple[bool, str | None, bool]:
        raw = (args.raw_args or "").strip()
        if not raw:
            await self.send_text(
                "请在指令后面带上需要脱敏的文本，例如：\n"
                "/sanitize 我的号码是 13812345678，邮箱 xxx@example.com"
            )
            return True, None, False

        masked = self.sanitizer.sanitize(raw)
        reply = f"🔐 脱敏结果：\n原文：{raw}\n脱敏：{masked}"
        await self.send_text(reply)
        return True, "已返回脱敏结果", True


@register_plugin
class LogSanitizerPlugin(BasePlugin):
    """插件入口类"""

    plugin_name: str = "log_sanitizer"
    enable_plugin: bool = True
    config_file_name: str = "config.toml"

    def get_plugin_components(self) -> list[tuple[PlusCommandInfo, type[PlusCommand]]]:
        return [(SanitizeCommand.get_plus_command_info(), SanitizeCommand)]

    permission_nodes: ClassVar[list[PermissionNodeField]] = [
        PermissionNodeField(
            node_name="use",
            description="可以使用 /sanitize 指令进行文本脱敏",
        )
    ]


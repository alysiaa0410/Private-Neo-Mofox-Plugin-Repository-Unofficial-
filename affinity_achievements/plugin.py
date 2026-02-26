"""
亲密度与成就系统插件

一个简单的亲密度与成就系统插件示例。
"""

from typing import ClassVar

from src.plugin_system import register_plugin
from src.plugin_system.base.base_plugin import BasePlugin
from src.plugin_system.base.command_args import CommandArgs
from src.plugin_system.base.component_types import ChatType, PermissionNodeField, PlusCommandInfo
from src.plugin_system.base.plus_command import PlusCommand
from src.plugin_system.utils.permission_decorators import require_permission

from .config import AffinityConfig
from .handlers import AffinityHandler


class AffinityCommand(PlusCommand):
    """查看与机器人的亲密度与已解锁成就"""

    command_name: str = "affinity"
    command_description: str = "查看当前亲密度等级与成就"
    command_aliases: ClassVar[list[str]] = ["亲密度", "成就"]
    chat_type_allow: ChatType = ChatType.ALL
    priority: int = 10

    def __init__(self):
        super().__init__()
        self.config = AffinityConfig()
        self.handler = AffinityHandler(self.config.achievements)

    @require_permission("use", deny_message="❌ 你没有权限查看亲密度信息")
    async def execute(self, args: CommandArgs) -> tuple[bool, str | None, bool]:
        user_id = str(getattr(args, "user_id", "unknown"))
        info = self.handler.get_affinity_info(user_id)

        reply_lines = [
            "💞 亲密度与成就",
            f"- 当前累计对话条数：{info['total_messages']}",
            f"- 当前称号：{info['current_level']}",
        ]
        
        if info['unlocked']:
            reply_lines.append(f"- 已解锁成就：{', '.join(info['unlocked'])}")
        
        if info['next_target']:
            reply_lines.append(f"- 下一目标：{info['next_target']}")
        else:
            reply_lines.append("- 你已经解锁了目前所有内置成就！")

        await self.send_text("\n".join(reply_lines))
        return True, "已返回亲密度信息", True

    async def on_message_record(self, args: CommandArgs) -> None:
        """供外部调用的简单统计接口"""
        user_id = str(getattr(args, "user_id", "unknown"))
        self.handler.record_message(user_id)


@register_plugin
class AffinityAchievementsPlugin(BasePlugin):
    """插件入口类"""

    plugin_name: str = "affinity_achievements"
    enable_plugin: bool = True
    config_file_name: str = "config.toml"

    def get_plugin_components(self) -> list[tuple[PlusCommandInfo, type[PlusCommand]]]:
        return [(AffinityCommand.get_plus_command_info(), AffinityCommand)]

    permission_nodes: ClassVar[list[PermissionNodeField]] = [
        PermissionNodeField(
            node_name="use",
            description="可以使用 /affinity 指令查看亲密度与成就",
        )
    ]


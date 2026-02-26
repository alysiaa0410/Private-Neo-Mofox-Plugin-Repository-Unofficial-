"""
每日签到与连击插件

一个简单的"每日签到 + 连击天数"插件。
"""

from typing import ClassVar

from src.plugin_system import register_plugin
from src.plugin_system.base.base_plugin import BasePlugin
from src.plugin_system.base.command_args import CommandArgs
from src.plugin_system.base.component_types import ChatType, PermissionNodeField, PlusCommandInfo
from src.plugin_system.base.plus_command import PlusCommand
from src.plugin_system.utils.permission_decorators import require_permission

from .config import CheckinConfig
from .handlers import CheckinHandler


class CheckinCommand(PlusCommand):
    """每日签到/查看连击天数"""

    command_name: str = "checkin"
    command_description: str = "每日签到并记录连击天数"
    command_aliases: ClassVar[list[str]] = ["签到", "打卡"]
    chat_type_allow: ChatType = ChatType.ALL
    priority: int = 10

    def __init__(self):
        super().__init__()
        self.handler = CheckinHandler()
        self.config = CheckinConfig()

    @require_permission("use", deny_message="❌ 你没有权限使用签到功能")
    async def execute(self, args: CommandArgs) -> tuple[bool, str | None, bool]:
        raw = (args.raw_args or "").strip().lower()
        if raw == "status":
            return await self._show_status(args)
        return await self._do_checkin(args)

    async def _show_status(self, args: CommandArgs) -> tuple[bool, str | None, bool]:
        user_id = str(getattr(args, "user_id", "unknown"))
        state = self.handler.get_user_state(user_id)
        
        if state.last_checkin_date is None:
            msg = "你还没有在本进程内签到过，快用 `/checkin` 试试吧。"
        else:
            msg = (
                f"你当前的连续签到天数为：{state.streak_days} 天。\n"
                f"上次签到日期：{state.last_checkin_date}"
            )
        await self.send_text(msg)
        return True, None, False

    async def _do_checkin(self, args: CommandArgs) -> tuple[bool, str | None, bool]:
        user_id = str(getattr(args, "user_id", "unknown"))
        
        if self.handler.is_checked_in_today(user_id):
            state = self.handler.get_user_state(user_id)
            await self.send_text(f"✅ 你今天已经签到过啦！当前连击：{state.streak_days} 天。")
            return True, None, False

        streak, _ = self.handler.do_checkin(user_id)
        bonus_text = self.handler.get_bonus_text(streak)

        reply = (
            f"✅ 签到成功！今天是你连续签到的第 {streak} 天。\n"
            f"{bonus_text}"
        )
        await self.send_text(reply)
        return True, "已完成签到", True


@register_plugin
class DailyCheckinPlugin(BasePlugin):
    """插件入口类"""

    plugin_name: str = "daily_checkin"
    enable_plugin: bool = True
    config_file_name: str = "config.toml"

    def get_plugin_components(self) -> list[tuple[PlusCommandInfo, type[PlusCommand]]]:
        return [(CheckinCommand.get_plus_command_info(), CheckinCommand)]

    permission_nodes: ClassVar[list[PermissionNodeField]] = [
        PermissionNodeField(
            node_name="use",
            description="可以使用 /checkin 指令进行每日签到与连击统计",
        )
    ]


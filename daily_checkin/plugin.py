"""
Daily Check-in Plugin

一个简单的“每日签到 + 连击天数”插件。

说明：
- 使用 /checkin 进行今日签到；
- 记录每个用户的最后签到日期和当前连击天数（仅存于内存，不做持久化）；
- 使用 /checkin status 查看当前连击和简单奖励提示。
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar

from src.plugin_system import register_plugin
from src.plugin_system.base.base_plugin import BasePlugin
from src.plugin_system.base.command_args import CommandArgs
from src.plugin_system.base.component_types import ChatType, PermissionNodeField, PlusCommandInfo
from src.plugin_system.base.plus_command import PlusCommand
from src.plugin_system.utils.permission_decorators import require_permission


@dataclass
class CheckinState:
    last_checkin_date: str | None = None  # YYYY-MM-DD
    streak_days: int = 0


def _today_str() -> str:
    # 使用本地时间，更符合日常“签到”直觉
    return datetime.now().strftime("%Y-%m-%d")


class CheckinCommand(PlusCommand):
    """每日签到/查看连击天数。"""

    command_name: str = "checkin"
    command_description: str = "每日签到并记录连击天数"
    command_aliases: ClassVar[list[str]] = ["签到", "打卡"]
    chat_type_allow: ChatType = ChatType.ALL
    priority: int = 10

    _states: dict[str, CheckinState] = {}

    @require_permission("use", deny_message="❌ 你没有权限使用签到功能")
    async def execute(self, args: CommandArgs) -> tuple[bool, str | None, bool]:
        raw = (args.raw_args or "").strip().lower()
        if raw == "status":
            return await self._show_status(args)
        return await self._do_checkin(args)

    async def _show_status(self, args: CommandArgs) -> tuple[bool, str | None, bool]:
        user_id = str(getattr(args, "user_id", "unknown"))
        state = self._states.get(user_id, CheckinState())
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
        today = _today_str()
        state = self._states.setdefault(user_id, CheckinState())

        if state.last_checkin_date == today:
            await self.send_text(f"✅ 你今天已经签到过啦！当前连击：{state.streak_days} 天。")
            return True, None, False

        # 简单判断是否连续（只比较日期字符串，足够轻量；需要更严谨可改为 date 计算）
        if state.last_checkin_date is not None:
            try:
                last = datetime.strptime(state.last_checkin_date, "%Y-%m-%d").date()
                now = datetime.strptime(today, "%Y-%m-%d").date()
                if (now - last).days == 1:
                    state.streak_days += 1
                else:
                    state.streak_days = 1
            except ValueError:
                state.streak_days = 1
        else:
            state.streak_days = 1

        state.last_checkin_date = today

        reply = (
            f"✅ 签到成功！今天是你连续签到的第 {state.streak_days} 天。\n"
            f"{self._bonus_text(state.streak_days)}"
        )
        await self.send_text(reply)
        return True, "已完成签到", True

    def _bonus_text(self, streak: int) -> str:
        if streak >= 30:
            return "你已经坚持打卡 30+ 天，太厉害了！给自己一点真实的奖励吧。"
        if streak >= 14:
            return "两周连击达成！保持这个节奏，你和 bot 会越来越熟。"
        if streak >= 7:
            return "连续一周签到！习惯正在成形，坚持就是胜利。"
        if streak >= 3:
            return "已经连续签到 3 天，继续加油，很快就能冲更长的连击纪录！"
        return "从今天开始，我们一起养成一个小小的好习惯。"


@register_plugin
class DailyCheckinPlugin(BasePlugin):
    """插件入口类。"""

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

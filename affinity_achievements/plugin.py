"""
Affinity & Achievements Plugin

一个简单的亲密度与成就系统插件示例。

说明：
- 使用内存字典记录用户与机器人的交互次数（仅在当前进程内有效）；
*- 根据累计消息数给出不同的亲密度等级与称号；
- 通过 /affinity 指令查看当前等级与下一目标。
"""

from dataclasses import dataclass
from typing import ClassVar

from src.plugin_system import register_plugin
from src.plugin_system.base.base_plugin import BasePlugin
from src.plugin_system.base.command_args import CommandArgs
from src.plugin_system.base.component_types import ChatType, PermissionNodeField, PlusCommandInfo
from src.plugin_system.base.plus_command import PlusCommand
from src.plugin_system.utils.permission_decorators import require_permission


@dataclass
class AffinityState:
    total_messages: int = 0


ACHIEVEMENTS = [
    (5, "初次相识"),
    (20, "常来坐坐"),
    (50, "老朋友"),
    (100, "特别熟悉的伙伴"),
    (200, "形影不离的搭子"),
]


class AffinityCommand(PlusCommand):
    """查看与机器人的亲密度与已解锁成就。"""

    command_name: str = "affinity"
    command_description: str = "查看当前亲密度等级与成就"
    command_aliases: ClassVar[list[str]] = ["亲密度", "成就"]
    chat_type_allow: ChatType = ChatType.ALL
    priority: int = 10

    _user_state: dict[str, AffinityState] = {}

    @require_permission("use", deny_message="❌ 你没有权限查看亲密度信息")
    async def execute(self, args: CommandArgs) -> tuple[bool, str | None, bool]:
        user_id = str(getattr(args, "user_id", "unknown"))
        state = self._user_state.get(user_id, AffinityState())

        level_name = "尚未获得称号"
        unlocked: list[str] = []
        next_target: str | None = None
        for threshold, name in ACHIEVEMENTS:
            if state.total_messages >= threshold:
                level_name = name
                unlocked.append(name)
            elif next_target is None:
                next_target = f"{threshold} 条对话解锁「{name}」"

        reply_lines = [
            "💞 亲密度与成就",
            f"- 当前累计对话条数：{state.total_messages}",
            f"- 当前称号：{level_name}",
        ]
        if unlocked:
            reply_lines.append(f"- 已解锁成就：{', '.join(unlocked)}")
        if next_target:
            reply_lines.append(f"- 下一目标：{next_target}")
        else:
            reply_lines.append("- 你已经解锁了目前所有内置成就！")

        await self.send_text("\n".join(reply_lines))
        return True, "已返回亲密度信息", True

    async def on_message_record(self, args: CommandArgs) -> None:
        """供外部调用的简单统计接口，可在其他钩子中调用。"""
        user_id = str(getattr(args, "user_id", "unknown"))
        state = self._user_state.setdefault(user_id, AffinityState())
        state.total_messages += 1


@register_plugin
class AffinityAchievementsPlugin(BasePlugin):
    """插件入口类。"""

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

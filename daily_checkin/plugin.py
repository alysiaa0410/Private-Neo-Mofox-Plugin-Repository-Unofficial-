"""
daily_checkin 插件主类
"""

from src.app.plugin_system.api.log_api import get_logger
from src.core.components.base import BasePlugin
from src.core.components.loader import register_plugin

from daily_checkin.components.configs.config import Config
from daily_checkin.components.commands.checkin_command import CheckinCommand

logger = get_logger("daily_checkin")


@register_plugin
class DailyCheckinPlugin(BasePlugin):
    """
    每日签到与连击插件

    提供每日签到功能，记录用户连续签到天数，并给出相应的奖励提示。
    """

    plugin_name = "daily_checkin"
    plugin_version = "1.0.0"
    plugin_author = "满月"
    plugin_description = "每日签到与连击插件 - 记录用户签到天数并给出奖励"
    configs = [Config]

    def get_components(self) -> list[type]:
        """获取插件内所有组件类

        Returns:
            list[type]: 插件内所有组件类的列表
        """
        return [CheckinCommand]

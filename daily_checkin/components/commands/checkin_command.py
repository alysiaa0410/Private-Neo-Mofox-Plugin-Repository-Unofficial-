"""
签到命令处理器
"""

from typing import Any, ClassVar, cast

from src.app.plugin_system.api.log_api import get_logger
from src.app.plugin_system.api.send_api import send_text
from src.core.components.base import BaseEventHandler
from src.core.components.types import EventType
from src.core.models.message import Message, MessageType
from src.kernel.event import EventDecision

from daily_checkin.components.configs.config import Config
from daily_checkin.handlers.checkin import CheckinHandler

logger = get_logger(__name__)


class CheckinCommand(BaseEventHandler):
    """签到命令处理器
    
    监听消息接收事件，处理签到相关命令。
    """

    handler_name = "checkin_command"
    handler_description = "每日签到命令 - 记录连续签到天数"
    weight = 10
    init_subscribe = [EventType.ON_MESSAGE_RECEIVED]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = CheckinHandler()

    async def execute(self, event_name: str, params: dict[str, Any]) -> tuple[EventDecision, dict[str, Any]]:
        """执行签到命令
        
        Args:
            event_name: 事件名称
            params: 事件参数，包含 message 对象
            
        Returns:
            (EventDecision, params)
        """
        try:
            message: Message | None = params.get("message")
            if not message or message.message_type != MessageType.TEXT:
                return EventDecision.SUCCESS, params
            
            content = str(message.content or "").strip()
            
            # 检查是否是签到命令
            if not self._is_checkin_command(content):
                return EventDecision.SUCCESS, params
            
            config = self._get_config()
            if config is None or not config.general.enabled:
                return EventDecision.SUCCESS, params
            
            # 解析命令参数
            parts = content.split(maxsplit=1)
            raw_args = parts[1] if len(parts) > 1 else ""
            
            user_id = str(message.sender_id or "unknown")
            
            if raw_args.lower() == "status":
                response = await self._show_status(user_id)
            else:
                response = await self._do_checkin(user_id, config)
            
            # 发送响应
            await send_text(
                content=response,
                stream_id=message.stream_id,
                platform=message.platform,
                reply_to=message.message_id
            )
            
            return EventDecision.STOP, params
            
        except Exception as e:
            logger.error(f"签到命令执行失败: {e}", exc_info=True)
            return EventDecision.SUCCESS, params
    
    def _is_checkin_command(self, content: str) -> bool:
        """判断是否是签到命令"""
        content_lower = content.lower()
        return (
            content_lower.startswith("/checkin") or
            content_lower.startswith("/签到") or
            content_lower.startswith("/打卡") or
            content_lower == "签到" or
            content_lower == "打卡"
        )
    
    def _get_config(self) -> Config | None:
        """获取插件配置"""
        if not self.plugin or not self.plugin.config:
            logger.warning("无法获取插件配置")
            return None
        return cast(Config, self.plugin.config)
    
    async def _show_status(self, user_id: str) -> str:
        """显示签到状态"""
        state = self.handler.get_user_state(user_id)
        
        if state.last_checkin_date is None:
            return "你还没有签到过，快用 `/checkin` 试试吧。"
        else:
            return (
                f"你当前的连续签到天数为：{state.streak_days} 天。\n"
                f"上次签到日期：{state.last_checkin_date}"
            )
    
    async def _do_checkin(self, user_id: str, config: Config) -> str:
        """执行签到"""
        if self.handler.is_checked_in_today(user_id):
            state = self.handler.get_user_state(user_id)
            return f"✅ 你今天已经签到过啦！当前连击：{state.streak_days} 天。"
        
        streak, _ = self.handler.do_checkin(user_id)
        bonus_text = self._get_bonus_text(streak, config)
        
        return (
            f"✅ 签到成功！今天是你连续签到的第 {streak} 天。\n"
            f"{bonus_text}"
        )
    
    def _get_bonus_text(self, streak: int, config: Config) -> str:
        """获取奖励文本"""
        if streak >= 30:
            return config.rewards.milestone_30
        if streak >= 14:
            return config.rewards.milestone_14
        if streak >= 7:
            return config.rewards.milestone_7
        if streak >= 3:
            return config.rewards.milestone_3
        return "从今天开始，我们一起养成一个小小的好习惯。"

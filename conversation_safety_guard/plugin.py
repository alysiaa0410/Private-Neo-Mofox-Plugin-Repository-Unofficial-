"""
对话情绪分析与安全建议插件
"""
from mofox.plugin_system.decorators import register_plugin
from mofox.plugin_system.base_handler import BaseEventHandler
from mofox.plugin_system.event_types import EventType
from mofox.core.logger import get_logger

logger = get_logger(__name__)


@register_plugin
class ConversationSafetyGuardPlugin(BaseEventHandler):
    """对话情绪分析与安全建议插件"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.negative_keywords = ["难过", "伤心", "痛苦", "抑郁", "焦虑"]
        logger.info("对话情绪分析与安全建议插件已初始化")
    
    def get_event_types(self):
        """返回此插件监听的事件类型"""
        return [EventType.ON_MESSAGE_RECEIVED]
    
    async def handle(self, event_type, event_data):
        """处理事件"""
        if event_type != EventType.ON_MESSAGE_RECEIVED:
            return
        
        message = event_data.get("message", "")
        
        # 处理情绪分析命令
        if message.startswith("/mood") or message.startswith("/心情检测"):
            await self._handle_mood_command(message)
        
        # 自动检测负面情绪
        await self._auto_detect_mood(message)
    
    async def _handle_mood_command(self, message):
        """处理情绪分析命令"""
        logger.info("执行情绪分析")
    
    async def _auto_detect_mood(self, message):
        """自动检测情绪"""
        for keyword in self.negative_keywords:
            if keyword in message:
                logger.warning(f"检测到负面情绪关键词: {keyword}")
                break

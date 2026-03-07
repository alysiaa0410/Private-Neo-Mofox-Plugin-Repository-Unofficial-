"""
日志隐私脱敏插件
"""
from mofox.plugin_system.decorators import register_plugin
from mofox.plugin_system.base_handler import BaseEventHandler
from mofox.plugin_system.event_types import EventType
from mofox.core.logger import get_logger
import re

logger = get_logger(__name__)


@register_plugin
class LogSanitizerPlugin(BaseEventHandler):
    """日志隐私脱敏插件"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 敏感信息正则表达式
        self.patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b1[3-9]\d{9}\b',
            "id_card": r'\b\d{17}[\dXx]\b',
        }
        logger.info("日志隐私脱敏插件已初始化")
    
    def get_event_types(self):
        """返回此插件监听的事件类型"""
        return [EventType.ON_MESSAGE_RECEIVED]
    
    async def handle(self, event_type, event_data):
        """处理事件"""
        if event_type != EventType.ON_MESSAGE_RECEIVED:
            return
        
        message = event_data.get("message", "")
        
        # 处理脱敏命令
        if message.startswith("/sanitize") or message.startswith("/脱敏"):
            await self._handle_sanitize_command(message)
    
    async def _handle_sanitize_command(self, message):
        """处理脱敏命令"""
        sanitized = message
        
        # 脱敏邮箱
        sanitized = re.sub(self.patterns["email"], "***@***.***", sanitized)
        
        # 脱敏手机号
        sanitized = re.sub(self.patterns["phone"], "***********", sanitized)
        
        # 脱敏身份证
        sanitized = re.sub(self.patterns["id_card"], "******************", sanitized)
        
        logger.info("已执行脱敏处理")

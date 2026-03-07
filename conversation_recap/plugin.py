"""
对话简要回顾插件
"""
from mofox.plugin_system.decorators import register_plugin
from mofox.plugin_system.base_handler import BaseEventHandler
from mofox.plugin_system.event_types import EventType
from mofox.core.logger import get_logger

logger = get_logger(__name__)


@register_plugin
class ConversationRecapPlugin(BaseEventHandler):
    """对话简要回顾插件"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conversation_history = []
        logger.info("对话简要回顾插件已初始化")
    
    def get_event_types(self):
        """返回此插件监听的事件类型"""
        return [EventType.ON_MESSAGE_RECEIVED]
    
    async def handle(self, event_type, event_data):
        """处理事件"""
        if event_type != EventType.ON_MESSAGE_RECEIVED:
            return
        
        message = event_data.get("message", "")
        
        # 记录对话历史
        self.conversation_history.append(message)
        if len(self.conversation_history) > 100:
            self.conversation_history.pop(0)
        
        # 处理回顾命令
        if message.startswith("/recap") or message.startswith("/回顾"):
            await self._handle_recap_command(message)
    
    async def _handle_recap_command(self, message):
        """处理回顾命令"""
        # 生成对话摘要
        recent_count = 10
        recent_messages = self.conversation_history[-recent_count:]
        
        logger.info(f"生成最近 {len(recent_messages)} 条对话的回顾")

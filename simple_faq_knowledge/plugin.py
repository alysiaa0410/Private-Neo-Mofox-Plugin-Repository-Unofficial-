"""
轻量FAQ与知识库增强插件
"""
from mofox.plugin_system.decorators import register_plugin
from mofox.plugin_system.base_handler import BaseEventHandler
from mofox.plugin_system.event_types import EventType
from mofox.core.logger import get_logger

logger = get_logger(__name__)


@register_plugin
class SimpleFaqKnowledgePlugin(BaseEventHandler):
    """轻量FAQ与知识库增强插件"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.faq_database = {
            "如何使用": "请输入 /help 查看帮助信息",
            "版本信息": "当前版本: MoFox 1.0.0",
            "联系方式": "请访问官方网站获取联系方式",
        }
        logger.info("轻量FAQ与知识库增强插件已初始化")
    
    def get_event_types(self):
        """返回此插件监听的事件类型"""
        return [EventType.ON_MESSAGE_RECEIVED]
    
    async def handle(self, event_type, event_data):
        """处理事件"""
        if event_type != EventType.ON_MESSAGE_RECEIVED:
            return
        
        message = event_data.get("message", "")
        
        # 处理FAQ命令
        if message.startswith("/faq") or message.startswith("/常见问题"):
            await self._handle_faq_command(message)
    
    async def _handle_faq_command(self, message):
        """处理FAQ命令"""
        parts = message.split(maxsplit=1)
        
        if len(parts) > 1:
            query = parts[1]
            # 搜索FAQ
            for question, answer in self.faq_database.items():
                if query in question:
                    logger.info(f"找到FAQ: {question} -> {answer}")
                    return
            logger.info(f"未找到相关FAQ: {query}")
        else:
            # 列出所有FAQ
            logger.info(f"FAQ数据库包含 {len(self.faq_database)} 条记录")

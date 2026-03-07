"""
亲密度与成就系统插件
"""
from mofox.plugin_system.decorators import register_plugin
from mofox.plugin_system.base_handler import BaseEventHandler
from mofox.plugin_system.event_types import EventType
from mofox.core.logger import get_logger

logger = get_logger(__name__)


@register_plugin
class AffinityAchievementsPlugin(BaseEventHandler):
    """亲密度与成就系统插件"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_affinity = {}
        self.achievements = {}
        logger.info("亲密度与成就系统插件已初始化")
    
    def get_event_types(self):
        """返回此插件监听的事件类型"""
        return [EventType.ON_MESSAGE_RECEIVED]
    
    async def handle(self, event_type, event_data):
        """处理事件"""
        if event_type != EventType.ON_MESSAGE_RECEIVED:
            return
        
        message = event_data.get("message", "")
        user_id = event_data.get("user_id", "default")
        
        # 处理亲密度命令
        if message.startswith("/affinity") or message.startswith("/亲密度"):
            await self._handle_affinity_command(user_id, message)
    
    async def _handle_affinity_command(self, user_id, message):
        """处理亲密度命令"""
        # 增加对话次数
        if user_id not in self.user_affinity:
            self.user_affinity[user_id] = {"count": 0, "level": 0}
        
        self.user_affinity[user_id]["count"] += 1
        count = self.user_affinity[user_id]["count"]
        
        # 计算等级
        level = count // 10
        self.user_affinity[user_id]["level"] = level
        
        logger.info(f"用户 {user_id} 亲密度: {count}, 等级: {level}")

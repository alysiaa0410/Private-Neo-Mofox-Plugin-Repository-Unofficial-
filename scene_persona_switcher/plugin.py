"""
多角色预设与场景切换插件
"""
from mofox.plugin_system.decorators import register_plugin
from mofox.plugin_system.base_handler import BaseEventHandler
from mofox.plugin_system.event_types import EventType
from mofox.core.logger import get_logger

logger = get_logger(__name__)


@register_plugin
class ScenePersonaSwitcherPlugin(BaseEventHandler):
    """多角色预设与场景切换插件"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_scene = "default"
        self.scenes = {
            "default": "默认场景",
            "professional": "专业助手",
            "casual": "轻松聊天",
            "creative": "创意写作",
        }
        logger.info("多角色预设与场景切换插件已初始化")
    
    def get_event_types(self):
        """返回此插件监听的事件类型"""
        return [EventType.ON_MESSAGE_RECEIVED]
    
    async def handle(self, event_type, event_data):
        """处理事件"""
        if event_type != EventType.ON_MESSAGE_RECEIVED:
            return
        
        message = event_data.get("message", "")
        
        # 处理场景切换命令
        if message.startswith("/scene") or message.startswith("/场景"):
            await self._handle_scene_command(message)
    
    async def _handle_scene_command(self, message):
        """处理场景切换命令"""
        parts = message.split()
        
        if len(parts) > 1:
            scene_name = parts[1]
            if scene_name in self.scenes:
                self.current_scene = scene_name
                logger.info(f"切换到场景: {self.scenes[scene_name]}")
            else:
                logger.warning(f"未知场景: {scene_name}")
        else:
            logger.info(f"当前场景: {self.scenes[self.current_scene]}")

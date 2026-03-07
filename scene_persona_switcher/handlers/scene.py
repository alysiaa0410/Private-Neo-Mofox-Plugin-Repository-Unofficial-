"""场景切换业务逻辑处理"""

from ..config import SceneDefinition


class SceneManager:
    """场景管理器"""
    
    def __init__(self, scenes: dict[str, SceneDefinition]):
        self.scenes = scenes
        self._session_scene: dict[str, str] = {}
    
    def get_scene(self, scene_name: str) -> SceneDefinition | None:
        """根据名称获取场景"""
        return self.scenes.get(scene_name)
    
    def list_scenes(self) -> list[tuple[str, SceneDefinition]]:
        """列出所有场景"""
        return list(self.scenes.items())
    
    def set_session_scene(self, session_key: str, scene_key: str) -> None:
        """设置会话场景"""
        self._session_scene[session_key] = scene_key
    
    def get_session_scene(self, session_key: str) -> str | None:
        """获取会话当前场景"""
        return self._session_scene.get(session_key)
    
    def get_session_key(self, chat_id: str | None, user_id: str | None) -> str:
        """构造会话键"""
        if chat_id is not None and user_id is not None:
            return f"{chat_id}:{user_id}"
        return "global"








